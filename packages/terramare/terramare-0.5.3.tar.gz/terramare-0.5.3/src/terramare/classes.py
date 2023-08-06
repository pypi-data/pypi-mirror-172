"""Deserializer factory for a generic class."""

import dataclasses
import enum
import logging
from dataclasses import InitVar, dataclass
from typing import (
    AbstractSet,
    Any,
    ClassVar,
    Dict,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
    overload,
)

from typing_extensions import Final, final

from . import iterator_utils, type_utils
from .core import ConstructorCore, FactoryCore, InternalConstructor, InternalFactory
from .data import Context, Value
from .errors import InternalError, UnsupportedTargetTypeError, ValidationException
from .metadata import Metadata, MetadataCollection
from .pretty_printer import LoggableArguments, LoggableTarget
from .types import Target

_log = logging.getLogger(__name__)

_T_co = TypeVar("_T_co", covariant=True)
_T_in = TypeVar("_T_in")
_Target = TypeVar("_Target", bound=Target[Any])


@dataclass(frozen=True)
class _disallow_unknown_fields(Metadata[bool]):

    KEY: ClassVar[str] = f"{__name__}.allow_unknown_fields"
    DEFAULT: ClassVar[bool] = False

    @property
    def value(self) -> bool:
        return True


#: Raise :exc:`terramare.errors.ConstructorError` if there are fields present in
#: the primitive that are not defined by the decorated class.
disallow_unknown_fields = _disallow_unknown_fields()


@dataclass(init=False)
class handle_exception_types(Metadata[Tuple[Type[Exception], ...]]):
    """
    Handle the listed exception types when constructing an instance of the decorated class.

    An exception of one of these types will be caught and re-raised as a
    :exc:`terramare.errors.ValidationError` including the full construction
    context.

    >>> import attr
    >>> import terramare
    >>>
    >>> @terramare.handle_exception_types(ValueError)
    ... @attr.s(auto_attribs=True)
    ... class User:
    ...     id: int = attr.ib()
    ...     name: str
    ...
    ...     @id.validator
    ...     def positive(self, _, value):
    ...         if not value > 0:
    ...             raise ValueError("id must be positive!")
    >>>
    >>> terramare.structure({"id": 0, "name": "Alice"}, into=User)
    Traceback (most recent call last):
    ...
    terramare.errors.ConstructorError: .: id must be positive!
    ...
    """

    KEY: ClassVar[str] = f"{__name__}.handle_exception_types"
    DEFAULT: ClassVar[Tuple[Type[Exception], ...]] = ()

    _value: Tuple[Type[Exception], ...]

    @property
    def value(self) -> Tuple[Type[Exception], ...]:
        return self._value

    def __init__(self, *exceptions: Type[Exception]) -> None:
        self._value = exceptions


@enum.unique
class _FromType(enum.Enum):
    OBJECT = "object"
    ARRAY = "array"
    LEAF = "leaf"


FromType = AbstractSet[_FromType]

OBJECT: Final = frozenset({_FromType.OBJECT})
ARRAY: Final = frozenset({_FromType.ARRAY})
VALUE: Final = frozenset({_FromType.LEAF})

_AUTO_KEY: Final[str] = f"{__name__}.auto"


@dataclass(frozen=True)
class _auto(Metadata[Optional[FromType]]):
    KEY: ClassVar[str] = _AUTO_KEY
    DEFAULT: ClassVar[Optional[FromType]] = None

    @dataclass(frozen=True)
    class inner(Metadata[Optional[FromType]]):
        KEY: ClassVar[str] = _AUTO_KEY
        DEFAULT: ClassVar[Optional[FromType]] = None

        _value: FromType

        @property
        def value(self) -> FromType:
            return self._value

    @property
    def value(self) -> FromType:
        return OBJECT

    @overload
    def __call__(self, __enable: bool) -> "_auto.inner":
        ...  # pragma: no cover

    @overload
    def __call__(self, *, from_: FromType) -> "_auto.inner":
        ...  # pragma: no cover

    @overload
    def __call__(self, target: _Target) -> _Target:
        ...  # pragma: no cover

    def __call__(
        self,
        target: Optional[Union[bool, Target[_T_in]]] = None,
        from_: Optional[FromType] = None,
    ) -> Union["_auto.inner", Target[_T_in]]:
        if isinstance(target, bool):
            # First overload
            if target:
                return _auto.inner(OBJECT)
            return _auto.inner(frozenset())
        if from_ is not None:
            # Second overload
            return _auto.inner(from_)
        # Third overload
        assert target is not None
        return _auto.inner(self.value)(target)


#: Automatically create a constructor for the decorated class.
auto = _auto()


@final
@dataclass(frozen=True)
class ClassFactory(FactoryCore):
    _metadata: MetadataCollection

    @dataclass(frozen=True)
    class _Constructor(ConstructorCore[_T_co]):
        _from_object: Optional[ConstructorCore[_T_co]]
        _from_array: Optional[ConstructorCore[_T_co]]
        _from_value: Optional[ConstructorCore[_T_co]]
        _handle_exception_types: Tuple[Type[Exception], ...]

        def __call__(self, data: "Value") -> _T_co:
            def get_constructor() -> Optional[ConstructorCore[_T_co]]:
                if data.is_object() and self._from_object:
                    return self._from_object
                if data.is_array() and self._from_array:
                    return self._from_array
                return self._from_value

            constructor = get_constructor()
            if not constructor:
                constructors = []
                if self._from_object:
                    constructors.append("object")
                if self._from_array:
                    constructors.append("array")
                raise data.make_error(f"expected {' or '.join(constructors)}")
            try:
                return constructor(data)
            except self._handle_exception_types as e:  # pylint: disable=catching-non-exception
                raise data.make_error(  # pylint: disable=bad-exception-context
                    str(e)
                ) from e

    def create_constructor(
        self, factory: InternalFactory, target: Target[_T_co]
    ) -> ConstructorCore[_T_co]:
        if not hasattr(target, "__call__"):
            raise UnsupportedTargetTypeError

        try:
            _add_type_hints(target, type_utils.get_parameters(target))
        except type_utils.ParameterError as e:
            raise factory.make_error(str(e))

        fromtypes = _get_fromtypes(self._metadata, target)
        if fromtypes is None:
            raise factory.make_error("class construction not enabled for target")
        if not fromtypes:
            raise factory.make_error("class construction disabled for target")

        from_object = None
        if OBJECT <= fromtypes:
            from_object = self._create_from_object_constructor(factory, target)

        from_array = None
        if ARRAY <= fromtypes:
            from_array = self._create_from_array_constructor(factory, target)

        from_value = None
        if VALUE <= fromtypes:
            from_value = self._create_from_value_constructor(factory, target)

        return type(self)._Constructor(
            _from_object=from_object,
            _from_array=from_array,
            _from_value=from_value,
            _handle_exception_types=(
                ValidationException,
                *handle_exception_types.read(self._metadata, target),
            ),
        )

    @dataclass(frozen=True)
    class _FromObjectConstructor(ConstructorCore[_T_co]):
        _positional: Sequence["_ContextField"]
        _keyword: Mapping[str, "_Field"]
        _var_keyword: Optional[InternalConstructor[Any]]
        # Variadic positional parameters are not used by this constructor.

        _target: Target[_T_co]
        _disallow_unknown_fields: bool

        def __call__(self, data: Value) -> _T_co:
            object_data = data.as_object()

            positional = []
            # Covered on Python 3.8+ only.
            for _ in self._positional:  # pragma: no cover
                positional.append(data.context)

            keyword = {}
            for name, field in self._keyword.items():
                if isinstance(field, _ContextField):
                    keyword[name] = data.context
                    continue
                try:
                    element = object_data.pop(name)
                except KeyError:
                    if field.required:
                        raise data.make_error(
                            f"missing required field: {name}"
                        ) from None
                    continue
                keyword[name] = field.constructor(element)

            if self._var_keyword:
                while object_data:
                    name = next(iter(object_data))
                    keyword[name] = self._var_keyword(object_data.pop(name))

            if self._disallow_unknown_fields and object_data:
                keys_str = ", ".join(f'"{key}"' for key in object_data)
                raise data.make_error(f"unknown field(s): {keys_str}")

            _log.debug(
                "Instantiating %s with arguments: %s",
                LoggableTarget(self._target),
                LoggableArguments(positional, keyword),
            )
            return self._target(*positional, **keyword)  # type: ignore[call-arg]

    def _create_from_object_constructor(
        self, factory: InternalFactory, target: Target[_T_co]
    ) -> ConstructorCore[_T_co]:
        parameters = _add_type_hints(target, type_utils.get_parameters(target))

        positional = []
        # Covered on Python 3.8+ only.
        while (
            parameters
            and parameters[0].is_positional_only()
            and not parameters[0].is_variadic()
        ):  # pragma: no cover
            parameter = parameters.pop(0)
            if parameter.is_context():
                positional.append(_ContextField())
            elif parameter.is_required():
                raise factory.make_error(
                    "cannot create from-object constructor for target with required "
                    f"positional-only parameter: {parameter.name}"
                )
            # Positional parameter is optional; omit it.

        positional_only_parameters = [
            p for p in parameters if p.is_positional_only() and not p.is_variadic()
        ]
        if positional_only_parameters:  # pragma: no cover
            raise InternalError(
                f"unexpected positional-only parameters remaining: {positional_only_parameters}"
            )

        keyword: Dict[str, _Field] = {}
        var_keyword = None
        while parameters:
            parameter = parameters.pop(0)
            if parameter.is_variadic():
                # The _FromObjectConstructor doesn't use variadic positional
                # parameters.
                if parameter.is_positional():
                    pass
                # The _FromObjectConstructor doesn't use variadic context
                # parameters.
                if not parameter.is_context():
                    var_keyword = factory.create_constructor(
                        parameter.type_hint, context=f'field "{parameter.name}"'
                    )
            elif parameter.is_context():
                keyword[parameter.name] = _ContextField()
            else:
                keyword[parameter.name] = _SingleField(
                    factory.create_constructor(
                        parameter.type_hint, context=f'field "{parameter.name}"'
                    ),
                    parameter.is_required(),
                )

        if parameters:  # pragma: no cover
            raise InternalError(f"unexpected parameters remaining: {parameters}")

        return type(self)._FromObjectConstructor(
            _positional=positional,
            _keyword=keyword,
            _var_keyword=var_keyword,
            _target=target,
            _disallow_unknown_fields=disallow_unknown_fields.read(
                self._metadata, target
            ),
        )

    @dataclass(frozen=True)
    class _FromArrayConstructor(ConstructorCore[_T_co]):
        _positional: Sequence["_Field"]
        _var_positional: Optional[InternalConstructor[Any]]
        _keyword: Mapping[str, "_ContextField"]
        # Variadic keyword parameters are not used by this constructor.

        _target: Target[_T_co]
        _disallow_extra_elements: bool

        def __call__(self, data: Value) -> _T_co:
            array_data = data.as_array()
            iter_data = iter(array_data)

            positional: List[Any] = []
            for field in self._positional:
                if isinstance(field, _ContextField):
                    positional.append(data.context)
                    continue
                try:
                    element = next(iter_data)
                except StopIteration:
                    if field.required:
                        raise data.make_error(
                            f"too few elements ({len(array_data)}) - "
                            f"expected at least {self.min_elements} "
                        ) from None
                    break
                positional.append(field.constructor(element))

            if self._var_positional:
                for element in iter_data:
                    positional.append(self._var_positional(element))

            if self._disallow_extra_elements and not iterator_utils.is_empty(iter_data):
                raise data.make_error(
                    f"too many elements ({len(array_data)}) - "
                    f"expected at most {self.max_elements}"
                )

            keyword = {field: data.context for field in self._keyword}

            _log.debug(
                "Instantiating %s with arguments: %s",
                LoggableTarget(self._target),
                LoggableArguments(positional, keyword),
            )
            return self._target(*positional, **keyword)  # type: ignore[call-arg]

        @property
        def min_elements(self) -> int:
            return sum(
                1
                for field in self._positional
                if isinstance(field, _SingleField) and field.required
            )

        @property
        def max_elements(self) -> int:
            if self._var_positional:  # pragma: no cover
                raise InternalError(
                    "no maximum element count for constructor with variadic parameter"
                )
            return sum(
                1
                for field in self._positional
                if isinstance(field, _SingleField) and field.required
            )

    def _create_from_array_constructor(
        self, factory: InternalFactory, target: Target[_T_co]
    ) -> ConstructorCore[_T_co]:
        parameters = _add_type_hints(target, type_utils.get_parameters(target))

        positional: List[_Field] = []
        var_positional = None

        while parameters and parameters[0].is_positional():
            parameter = parameters.pop(0)
            if parameter.is_variadic():
                # The _FromArrayConstructor doesn't use variadic context
                # parameters.
                if not parameter.is_context():
                    var_positional = factory.create_constructor(
                        parameter.type_hint, context=f'field "{parameter.name}"'
                    )
            elif parameter.is_context():
                positional.append(_ContextField())
            else:
                positional.append(
                    _SingleField(
                        factory.create_constructor(
                            parameter.type_hint, context=f'field "{parameter.name}"'
                        ),
                        parameter.is_required(),
                    )
                )

        positional_parameters = [p for p in parameters if p.is_positional()]
        if positional_parameters:  # pragma: no cover
            raise InternalError(
                f"unexpected positional parameters remaining: {positional_parameters}"
            )

        keyword = {}
        while parameters:
            parameter = parameters.pop(0)
            if parameter.is_variadic():
                # The _FromArrayConstructor doesn't use variadic keyword
                # parameters.
                pass
            elif parameter.is_context():
                keyword[parameter.name] = _ContextField()
            elif parameter.is_required():
                raise factory.make_error(
                    "cannot create from-array constructor for target with required "
                    f"keyword-only parameter: {parameter.name}"
                )
            # Covered, despite what 'coverage' says.
            else:  # pragma: no cover
                # Keyword parameter is optional; omit it.
                pass

        if parameters:  # pragma: no cover
            raise InternalError(f"unexpected parameters remaining: {parameters}")

        return type(self)._FromArrayConstructor(
            _positional=positional,
            _var_positional=var_positional,
            _keyword=keyword,
            _target=target,
            _disallow_extra_elements=disallow_unknown_fields.read(
                self._metadata, target
            ),
        )

    @dataclass(frozen=True)
    class _FromValueConstructor(ConstructorCore[_T_co]):
        _positional: Sequence["_Field"]
        _keyword: Mapping[str, "_ContextField"]
        # Variadic parameters are not used by this constructor.

        _target: Target[_T_co]

        def __post_init__(self) -> None:
            values = [f for f in self._positional if isinstance(f, _SingleField)]
            if len(values) != 1:  # pragma: no cover
                raise InternalError(f"expected exactly one value field: {values}")

        def __call__(self, data: Value) -> _T_co:
            positional = []
            for field in self._positional:
                if isinstance(field, _ContextField):
                    positional.append(data.context)
                else:
                    positional.append(field.constructor(data))
            keyword = {field: data.context for field in self._keyword}
            _log.debug(
                "Instantiating %s with argument: %s",
                LoggableTarget(self._target),
                LoggableArguments(positional, keyword),
            )
            return self._target(*positional, **keyword)  # type: ignore[call-arg]

    def _create_from_value_constructor(
        self,
        factory: InternalFactory,
        target: Target[_T_co],
    ) -> ConstructorCore[_T_co]:
        parameters = _add_type_hints(target, type_utils.get_parameters(target))

        positional: List[_Field] = []

        def have_value() -> bool:
            return any(isinstance(f, _SingleField) for f in positional)

        while parameters and parameters[0].is_positional():
            parameter = parameters.pop(0)
            if parameter.is_context():
                if parameter.is_variadic():
                    # The _FromValueConstructor doesn't use variadic context
                    # parameters.
                    break
                positional.append(_ContextField())
            elif not have_value():
                positional.append(
                    _SingleField(
                        factory.create_constructor(
                            parameter.type_hint, context=f'field "{parameter.name}"'
                        ),
                        parameter.is_required(),
                    )
                )
            elif parameter.is_required():
                raise factory.make_error(
                    "cannot create from-value constructor for target "
                    "with more than one required parameter"
                )
            # Covered, despite what 'coverage' says.
            else:  # pragma: no cover
                # Tail optional parameter; omit.
                pass

        if not have_value():
            raise factory.make_error(
                "cannot create from-value constructor for "
                "target with no positional parameters"
            )

        positional_parameters = [p for p in parameters if p.is_positional()]
        if positional_parameters:  # pragma: no cover
            raise InternalError(
                f"unexpected positional parameters remaining: {positional_parameters}"
            )

        keyword = {}
        while parameters:
            parameter = parameters.pop(0)
            if parameter.is_variadic():
                # The _FromValueConstructor doesn't use variadic parameters.
                break
            if parameter.is_context():
                keyword[parameter.name] = _ContextField()
            elif parameter.is_required():
                raise factory.make_error(
                    "cannot create from-value constructor for "
                    "target with required keyword-only parameter"
                )
            # Keyword parameter is optional; omit it.

        if parameters:  # pragma: no cover
            raise InternalError(f"unexpected parameters remaining: {parameters}")

        return type(self)._FromValueConstructor(
            _positional=positional, _keyword=keyword, _target=target
        )


def _get_fromtypes(
    metadata: MetadataCollection, target: Target[Any]
) -> Optional[FromType]:
    from_types = auto.read(metadata, target)
    if from_types is not None:
        return from_types
    if dataclasses.is_dataclass(target) or hasattr(target, "__attrs_attrs__"):
        return OBJECT
    if _is_namedtuple(target):
        return OBJECT | ARRAY
    return None


def _is_namedtuple(target: Target[_T_co]) -> bool:
    if getattr(target, "__bases__", None) != (tuple,):
        return False
    fields = getattr(target, "_fields", None)
    return isinstance(fields, tuple) and all(isinstance(field, str) for field in fields)


@dataclass(frozen=True)
class _TypedParameter(type_utils.Parameter):
    type_hint: Target[object]

    def is_context(self) -> bool:
        return self.type_hint is Context


def _add_type_hints(
    type_: Target[object], params: Sequence[type_utils.Parameter]
) -> List[_TypedParameter]:
    type_hints = type_utils.get_type_hints(type_, params)
    return [
        _TypedParameter(p.parameter, _strip_initvar(type_hints[p.name])) for p in params
    ]


def _strip_initvar(target: Target[object]) -> Target[object]:
    # One or other of these branches is covered, depending on the Python
    # version.
    if isinstance(target, InitVar) and hasattr(target, "type"):  # pragma: no cover
        return target.type
    if target is InitVar:  # pragma: no cover
        raise type_utils.ParameterError(
            "'InitVar' is not supported before Python 3.8 as it does not "
            "contain the necessary type information - see "
            "https://bugs.python.org/issue33569."
        )
    return target


@dataclass(frozen=True)
class _SingleField:
    constructor: InternalConstructor[Any]
    required: bool


@dataclass(frozen=True)
class _ContextField:
    pass


_Field = Union[_SingleField, _ContextField]
