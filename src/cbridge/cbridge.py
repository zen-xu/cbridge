from __future__ import annotations

import ctypes
import dataclasses as ds
import sys
import typing

from collections.abc import Sequence
from functools import wraps
from typing import TYPE_CHECKING
from typing import Any
from typing import TypeVar


if sys.version_info >= (3, 12):
    from typing import dataclass_transform
else:
    from typing_extensions import dataclass_transform

if TYPE_CHECKING:
    from .types import CData

    field = ds.field


_T = TypeVar("_T")


def new_array(ctype: type[CData], length: int) -> type[CData]:
    class Array(ctype * length):  # type: ignore[misc]
        def __repr__(self) -> str:
            return str(list(self))

        def __eq__(self, value: object, /) -> bool:
            if not isinstance(value, Sequence):
                return False
            return list(self) == list(value)

    return Array


_BaseStructMeta: type = type(ctypes.Structure)


@dataclass_transform()
class CStructMeta(_BaseStructMeta):
    def __new__(meta_self, name: str, bases: tuple[type, ...], attrs: dict[str, Any]):
        annotations = attrs.get("__annotations__", {})

        fields: list[tuple[str, type[CData]]] = []

        def get_base_fields(cls):
            fields = []
            for base in reversed(cls.__mro__):
                fields += getattr(base, "_fields_", [])
            return fields

        for base in bases:
            fields += get_base_fields(base)

        for f_name, field in annotations.items():
            if getattr(field, "__origin__", None) is typing.ClassVar:
                continue

            if isinstance(field, tuple):
                # field is array
                ctype, length = field
                if hasattr(length, "__args__"):
                    length = length.__args__[0]
                fields.append((f_name, new_array(ctype, length)))
            else:
                fields.append((f_name, field))

        if fields:
            attrs["_fields_"] = tuple(fields)

        cls = ds.dataclass()(super().__new__(meta_self, name, bases, attrs))
        origin_init = cls.__init__

        @wraps(origin_init)
        def wrapped_init(self, *args, **kwargs):
            args = list(args)
            for i, arg in enumerate(args):
                if isinstance(arg, Sequence):
                    args[i] = fields[i][1](*arg)
            args_count = len(args)
            for j, (k, v) in enumerate(kwargs.items()):
                if isinstance(v, Sequence):
                    kwargs[k] = fields[args_count + j][1](*v)

            return origin_init(self, *args, **kwargs)

        cls.__init__ = wrapped_init

        return cls


if TYPE_CHECKING:

    @dataclass_transform(field_specifiers=(field,))
    class CStruct(ctypes.Structure): ...
else:

    class CStruct(ctypes.Structure, metaclass=CStructMeta): ...
