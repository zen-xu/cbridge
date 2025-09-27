import array
import sys

from typing import ClassVar
from typing import Literal

import pytest

from cbridge import CStruct
from cbridge import field
from cbridge import types
from cbridge.types import pointer


class Data(CStruct):
    a: types.int32
    b: types.int8


class Data2(Data):
    c: types.float


class NestedData(CStruct):
    d1: Data
    d2: Data2


def test_construct_cstruct():
    data = Data(a=1, b=2)
    assert data.a == 1
    assert data.b == 2

    data = Data(a=1, b=256)
    assert data.b == 0


def test_construct_from_buffer():
    buffer = array.array("B", b"\x01\x00\x00\x00\x02\x00\x00\x00")
    data = Data.from_buffer(buffer)
    assert data == Data(a=1, b=2)


def test_construct_subclass():
    data = Data2(a=1, b=2, c=3.0)
    assert data.a == 1
    assert data.b == 2
    assert data.c == 3.0


def test_construct_nested_cstruct():
    data = NestedData(d1=Data(a=4, b=5), d2=Data2(a=6, b=7, c=8.0))
    assert data.d1 == Data(a=4, b=5)
    assert data.d2 == Data2(a=6, b=7, c=8.0)


def test_compare_cstruct():
    data1 = Data(a=1, b=2)
    data2 = Data(a=1, b=2)
    data3 = Data(a=1, b=3)
    assert data1 == data2
    assert data1 != data3


def test_repr_cstruct():
    data = Data(a=1, b=2)
    assert repr(data) == "Data(a=1, b=2)"


def test_array_cstruct():
    class ArrayData(CStruct):
        a: types.int
        b: types.Array[types.int8, Literal[2]]
        c: types.Array[types.int8, 2]  # type: ignore[type-var]

    data = ArrayData(1, b=(1, 2), c=(3, 4))
    assert data.a == 1
    assert data.b == [1, 2]
    assert data.b != [2, 3]
    assert data.c == [3, 4]
    assert repr(data) == f"{ArrayData.__qualname__}(a=1, b=[1, 2], c=[3, 4])"


def test_default_cstruct():
    class DefaultData(CStruct):
        a: types.int
        b: types.int = 1
        c: types.int = field(default=2)
        d: types.Array[types.int, Literal[2]] = field(default_factory=lambda: [3, 4])

    data = DefaultData(a=0)
    assert data.a == 0
    assert data.b == 1
    assert data.c == 2
    assert data.d == [3, 4]


def test_class_var_cstruct():
    class ClassVarData(CStruct):
        a: ClassVar[int]
        b: types.int

    data = ClassVarData(b=1)
    assert data.b == 1
    assert str(data) == f"{ClassVarData.__qualname__}(b=1)"


@pytest.mark.skipif(
    sys.version_info >= (3, 13),
    reason="cell structure is not supported in python3.13 or higher",
)
def test_cell_cstruct():
    class CellData(CStruct):
        id: types.int
        next: "types.Pointer[CellData]"

    c1 = CellData(id=1, next=None)
    c2 = CellData(id=2, next=pointer(c1))
    c1.next = pointer(c2)

    p = c1
    ids = []
    for _ in range(8):
        assert p is not None
        ids.append(p.id)

        assert p.next is not None
        p = p.next[0]
    assert ids == [1, 2, 1, 2, 1, 2, 1, 2]


def test_char_ptr_cstruct():
    class CharPtrData(CStruct):
        a: types.char_ptr

    data = CharPtrData(a=b"hello")
    assert data.a is not None
    assert data.a == b"hello"


def test_wchar_ptr_cstruct():
    class WCharPtrData(CStruct):
        a: types.wchar_ptr

    data = WCharPtrData(a="hello")
    assert data.a is not None
    assert data.a == "hello"
