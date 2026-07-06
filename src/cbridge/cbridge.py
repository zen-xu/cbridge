from __future__ import annotations

import ctypes
import dataclasses as ds
import sys

from functools import wraps
from typing import TYPE_CHECKING
from typing import Any
from typing import ClassVar
from typing import TypeVar
from typing import get_origin
from typing import get_type_hints


if sys.version_info >= (3, 12):
    from typing import Self
    from typing import dataclass_transform
else:
    from typing_extensions import Self
    from typing_extensions import dataclass_transform


_T = TypeVar("_T")

_CStructType: type = type(ctypes.Structure)


@dataclass_transform()
class CStructType(_CStructType):
    def __new__(
        meta_self,  # type: ignore[misc]
        name: str,
        bases: tuple[type, ...],
        attrs: dict[str, Any],
        pack: int = 0,
        **extra,
    ):
        if pack:
            attrs["_pack_"] = pack
            # Python 3.14+ only allows _pack_ with the MSVC-compatible layout
            attrs["_layout_"] = "ms"
        return super().__new__(meta_self, name, bases, attrs)

    # Since Python 3.13, ctypes initializes structure storage info in tp_init
    # instead of tp_new, so field resolution (which may create pointers to the
    # class itself for forward declarations) must happen after super().__init__
    def __init__(
        cls,  # noqa: N805
        name: str,
        bases: tuple[type, ...],
        attrs: dict[str, Any],
        pack: int = 0,
        **extra,
    ):
        super().__init__(name, bases, attrs)
        fields_map = {
            f_name: f_type
            for f_name, f_type in get_type_hints(
                cls, localns={**locals(), name: cls}
            ).items()
            if get_origin(f_type) is not ClassVar
        }
        fields = list(fields_map.items())
        if fields:
            # update fields
            cls._fields_ = fields

        ds.dataclass(cls)

        @wraps(cls.__init__)  # type: ignore[misc]
        def wrapped_init(self, *args, **kwargs):
            args = list(args)

            for i, arg in enumerate(args):
                field_name = fields[i][0]
                kwargs[field_name] = arg

            # fill default values
            for field_name, _ in fields:
                if field_name in kwargs:
                    continue

                if field_option := attrs.get(field_name):
                    if isinstance(field_option, ds.Field):
                        if field_option.default is not ds.MISSING:
                            kwargs[field_name] = field_option.default
                        elif field_option.default_factory is not ds.MISSING:
                            kwargs[field_name] = field_option.default_factory()
                    else:
                        kwargs[field_name] = field_option

            for arg_name, arg_value in kwargs.items():
                field_type = fields_map[arg_name]
                if issubclass(field_type, ctypes.Array):
                    kwargs[arg_name] = field_type(*arg_value)

            return ctypes.Structure.__init__(self, **kwargs)

        cls.__init__ = wrapped_init  # type: ignore[misc]


field = ds.field

if TYPE_CHECKING:

    @dataclass_transform(field_specifiers=(field,))
    class CStruct(ctypes.Structure):
        def __init_subclass__(cls, pack: int = 0) -> None: ...

        @classmethod
        def empty(cls) -> Self:
            """Create an empty instance of the structure."""
            ...

else:

    class CStruct(ctypes.Structure, metaclass=CStructType):
        @classmethod
        def empty(cls) -> Self:
            return cls()
