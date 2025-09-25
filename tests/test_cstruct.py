import array

from cbridge import CStruct
from cbridge import types


class Data(CStruct):
    a: types.Int32
    b: types.Int8


def test_construct_cstruct():
    data = Data(a=1, b=2)
    assert data.a == 1
    assert data.b == 2


def test_construct_from_buffer():
    buffer = array.array("B", b"\x01\x00\x00\x00\x02\x00\x00\x00")
    data = Data.from_buffer(buffer)
    assert data == Data(a=1, b=2)


def test_compare_cstruct():
    data1 = Data(a=1, b=2)
    data2 = Data(a=1, b=2)
    data3 = Data(a=1, b=3)
    assert data1 == data2
    assert data1 != data3


def test_repr_cstruct():
    data = Data(a=1, b=2)
    assert repr(data) == "Data(a=1, b=2)"
