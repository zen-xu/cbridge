import ctypes

from typing import TYPE_CHECKING
from typing import Any
from typing import Generic
from typing import TypeVar
from typing import Union


if TYPE_CHECKING:
    from _ctypes import _CData as CData

    Bool = Union[bool, CData]
    Byte = Union[bytes, CData]
    Char = Union[bytes, CData]
    Double = Union[float, CData]
    Float = Union[float, CData]
    UByte = Union[bytes, CData]
    Int = Union[int, CData]
    Int8 = Union[int, CData]
    Int16 = Union[int, CData]
    Int32 = Union[int, CData]
    Int64 = Union[int, CData]
    Long = Union[int, CData]
    LongDouble = Union[float, CData]
    LongLong = Union[float, CData]
    Short = Union[int, CData]
    SizeT = Union[int, CData]
    SSizeT = Union[int, CData]
    UInt = Union[int, CData]
    UInt8 = Union[int, CData]
    UInt16 = Union[int, CData]
    UInt32 = Union[int, CData]
    UInt64 = Union[int, CData]
    ULong = Union[int, CData]
    ULongLong = Union[int, CData]
    UShort = Union[int, CData]
    WChar = Union[str, CData]
    VoidPtr = Union[ctypes.c_void_p, Any]
    CharPtr = Union[ctypes.c_char_p, Any]
    WCharPtr = Union[ctypes.c_wchar_p, Any]
else:
    CData = object
    Byte = ctypes.c_byte
    Bool = ctypes.c_bool
    Char = ctypes.c_char
    Double = ctypes.c_double
    Float = ctypes.c_float
    UByte = ctypes.c_ubyte
    Int = ctypes.c_int
    Int8 = ctypes.c_int8
    Int16 = ctypes.c_int16
    Int32 = ctypes.c_int32
    Int64 = ctypes.c_int64
    Long = ctypes.c_long
    LongDouble = ctypes.c_longdouble
    LongLong = ctypes.c_longlong
    Short = ctypes.c_short
    SizeT = ctypes.c_size_t
    SSizeT = ctypes.c_ssize_t
    UInt = ctypes.c_uint
    UInt8 = ctypes.c_uint8
    UInt16 = ctypes.c_uint16
    UInt32 = ctypes.c_uint32
    UInt64 = ctypes.c_uint64
    ULong = ctypes.c_ulong
    ULongLong = ctypes.c_ulonglong
    UShort = ctypes.c_ushort
    WChar = ctypes.c_wchar
    VoidPtr = ctypes.c_void_p
    CharPtr = ctypes.c_char_p
    WCharPtr = ctypes.c_wchar_p


CTimeT = ULong

_T = TypeVar("_T")
_Len = TypeVar("_Len")


if TYPE_CHECKING:

    class _Array(Generic[_T, _Len]): ...

    Array = Union[_Array[_T, _Len], list[_T]]
else:

    class _Array:
        def __getitem__(
            self, type_length: tuple[type[CData], int]
        ) -> tuple[type[CData], int]:
            return type_length

    Array = _Array()
