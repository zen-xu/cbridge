from __future__ import annotations

import ctypes
import dataclasses as ds
import sys
import typing

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


_BaseStructMeta: type = type(ctypes.Structure)


@dataclass_transform()
class CStructMeta(_BaseStructMeta):
    def __new__(meta_self, name: str, bases: tuple[type, ...], attrs: dict[str, Any]):
        annotations = attrs.get("__annotations__", {})

        fields: list[tuple[str, type[CData]]] = []

        def get_base_fields(cls):
            fields = []
            for base in reversed(cls.__mro__):
                if hasattr(base, "_fields_"):
                    fields += list(base._fields_)
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
                fields.append((f_name, ctype * length))
            else:
                fields.append((f_name, field))

        if fields:
            attrs["_fields_"] = tuple(fields)
        cls = super().__new__(meta_self, name, bases, attrs)
        return ds.dataclass()(cls)


if TYPE_CHECKING:

    @dataclass_transform(field_specifiers=(field,))
    class CStruct(ctypes.Structure): ...
else:

    class CStruct(ctypes.Structure, metaclass=CStructMeta): ...
