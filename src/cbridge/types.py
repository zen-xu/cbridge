# pyright: reportGeneralTypeIssues=false
import builtins
import ctypes

from collections.abc import Sequence
from typing import TYPE_CHECKING
from typing import Generic
from typing import TypeVar
from typing import overload


_T = TypeVar("_T")

if TYPE_CHECKING:
    from _ctypes import _CData
    from typing import Any
    from typing import Union

    from typing_extensions import Self

    class CData(_CData, Generic[_T]):
        def __iadd__(self, other: _T) -> Self: ...
        def __isub__(self, other: _T) -> Self: ...
        def __imul__(self, other: _T) -> Self: ...
        def __itruediv__(self, other: _T) -> Self: ...
        def __ifloordiv__(self, other: _T) -> Self: ...
        def __imod__(self, other: _T) -> Self: ...
        def __ipow__(self, other: _T) -> Self: ...
        def __ilshift__(self, other: _T) -> Self: ...
        def __irshift__(self, other: _T) -> Self: ...
        def __iand__(self, other: _T) -> Self: ...
        def __ixor__(self, other: _T) -> Self: ...
        def __ior__(self, other: _T) -> Self: ...
        def __add__(self, other: _T) -> Self: ...
        def __sub__(self, other: _T) -> Self: ...
        def __mul__(self, other: _T) -> Self: ...
        def __truediv__(self, other: _T) -> Self: ...
        def __floordiv__(self, other: _T) -> Self: ...
        def __mod__(self, other: _T) -> Self: ...
        def __pow__(self, other: _T) -> Self: ...
        def __lshift__(self, other: _T) -> Self: ...
        def __rshift__(self, other: _T) -> Self: ...
        def __and__(self, other: _T) -> Self: ...
        def __xor__(self, other: _T) -> Self: ...
        def __or__(self, other: _T) -> Self: ...
        def __neg__(self) -> Self: ...
        def __pos__(self) -> Self: ...
        def __abs__(self) -> Self: ...
        def __invert__(self) -> Self: ...

    bool = type("bool", (builtins.bool, CData), {})
    byte = type("byte", (builtins.bytes, CData), {})
    char = type("char", (builtins.bytes, CData), {})
    double = type("double", (builtins.float, CData), {})
    float = type("float", (builtins.float, CData), {})
    ubyte = type("ubyte", (builtins.bytes, CData), {})
    int = type("int", (builtins.int, CData), {})
    int8 = type("int8", (builtins.int, CData), {})
    int16 = type("int16", (builtins.int, CData), {})
    int32 = type("int32", (builtins.int, CData), {})
    int64 = type("int64", (builtins.int, CData), {})
    long = type("long", (builtins.int, CData), {})
    longdouble = type("longdouble", (builtins.float, CData), {})
    longlong = type("longlong", (builtins.float, CData), {})
    short = type("short", (builtins.int, CData), {})
    size_t = type("size_t", (builtins.int, CData), {})
    ssize_t = type("ssize_t", (builtins.int, CData), {})
    uint = type("uint", (builtins.int, CData), {})
    uint8 = type("uint8", (builtins.int, CData), {})
    uint16 = type("uint16", (builtins.int, CData), {})
    uint32 = type("uint32", (builtins.int, CData), {})
    uint64 = type("uint64", (builtins.int, CData), {})
    ulong = type("ulong", (builtins.int, CData), {})
    ulonglong = type("ulonglong", (builtins.int, CData), {})
    ushort = type("ushort", (builtins.int, CData), {})
    wchar = type("wchar", (builtins.str, CData), {})
    void_ptr = Union[ctypes.c_void_p, Any]

    _Len = TypeVar("_Len")

    class _Array(Generic[_T, _Len], ctypes.Array[_T]): ...  # type: ignore[type-var]

    Array = Union[_Array[_T, _Len], Sequence[_T]]

    class _Pointer(ctypes._Pointer[_T]):  #  type: ignore[type-var]
        @overload
        def __getitem__(self, index: builtins.int) -> _T: ...
        @overload
        def __getitem__(self, index: slice) -> list[_T]: ...
        def __getitem__(
            self, index: Union[builtins.int, slice]
        ) -> Union[_T, list[_T]]: ...

    Pointer = Union[_Pointer[_T], None]

    char_ptr = Union[Pointer[char], bytes]
    wchar_ptr = Union[Pointer[wchar], str]

    def pointer(obj: _T) -> Pointer[_T]: ...
else:
    CData = object
    byte = ctypes.c_byte
    bool = ctypes.c_bool
    char = ctypes.c_char
    double = ctypes.c_double
    float = ctypes.c_float
    ubyte = ctypes.c_ubyte
    int = ctypes.c_int
    int8 = ctypes.c_int8
    int16 = ctypes.c_int16
    int32 = ctypes.c_int32
    int64 = ctypes.c_int64
    long = ctypes.c_long
    longdouble = ctypes.c_longdouble
    longlong = ctypes.c_longlong
    short = ctypes.c_short
    size_t = ctypes.c_size_t
    ssize_t = ctypes.c_ssize_t
    uint = ctypes.c_uint
    uint8 = ctypes.c_uint8
    uint16 = ctypes.c_uint16
    uint32 = ctypes.c_uint32
    uint64 = ctypes.c_uint64
    ulong = ctypes.c_ulong
    ulonglong = ctypes.c_ulonglong
    ushort = ctypes.c_ushort
    wchar = ctypes.c_wchar
    void_ptr = ctypes.c_void_p
    char_ptr = ctypes.c_char_p
    wchar_ptr = ctypes.c_wchar_p

    from typing import get_args

    class Array:
        def __class_getitem__(cls, types: tuple[type[CData], int]):
            ctype, length = types
            if not isinstance(length, builtins.int):
                length = get_args(length)[0]

            return type(f"Array_{ctype.__name__}_{length}", (ctype * length, cls), {})

        def __repr__(self):
            return str(list(self))

        def __eq__(self, value: object, /) -> bool:
            if not isinstance(value, Sequence):
                return False
            return list(self) == list(value)

    class Pointer(ctypes._Pointer):
        def __class_getitem__(cls, type):
            cls = ctypes.POINTER(type)

            def pointer_repr(self):
                try:
                    _ = self.contents
                except ValueError:
                    return "nullptr"
                else:
                    return f"*{type.__name__}"

            cls.__repr__ = pointer_repr

            return cls

    pointer = ctypes.pointer

ctime_t = ulong
