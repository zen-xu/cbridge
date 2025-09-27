import ctypes

from collections.abc import Sequence
from typing import TYPE_CHECKING
from typing import Generic
from typing import TypeVar
from typing import overload


_T = TypeVar("_T")

if TYPE_CHECKING:
    from _ctypes import _CData as CData
    from typing import Any
    from typing import Union

    bool = Union[bool, CData]
    byte = Union[bytes, CData]
    char = Union[bytes, CData]
    double = Union[float, CData]
    float = Union[float, CData]
    ubyte = Union[bytes, CData]
    int = Union[int, CData]
    int8 = Union[int, CData]
    int16 = Union[int, CData]
    int32 = Union[int, CData]
    int64 = Union[int, CData]
    long = Union[int, CData]
    longdouble = Union[float, CData]
    longlong = Union[float, CData]
    short = Union[int, CData]
    size_t = Union[int, CData]
    ssize_t = Union[int, CData]
    uint = Union[int, CData]
    uint8 = Union[int, CData]
    uint16 = Union[int, CData]
    uint32 = Union[int, CData]
    uint64 = Union[int, CData]
    ulong = Union[int, CData]
    ulonglong = Union[int, CData]
    ushort = Union[int, CData]
    wchar = Union[str, CData]
    void_ptr = Union[ctypes.c_void_p, Any]

    _Len = TypeVar("_Len")

    class _Array(Generic[_T, _Len], ctypes.Array[_T]): ...  # type: ignore[type-var]

    Array = Union[_Array[_T, _Len], Sequence[_T]]

    class _Pointer(ctypes._Pointer[_T]):  #  type: ignore[type-var]
        @overload
        def __getitem__(self, index: int) -> _T: ...
        @overload
        def __getitem__(self, index: slice) -> list[_T]: ...
        def __getitem__(self, index: int | slice) -> _T | list[_T]: ...

    Pointer = Union[_Pointer[_T], None]

    char_ptr = Pointer[char] | bytes
    wchar_ptr = Pointer[wchar] | str

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

    import builtins

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
