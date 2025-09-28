from cbridge import cfunc
from cbridge import types


@cfunc("c")
def strchr(s: types.char_ptr, c: types.char) -> types.char_ptr: ...


def test_cfunc():
    assert strchr(b"hello", b"o") == b"o"


@cfunc("c", "strchr")
def c_strchr(s: types.char_ptr, c: types.char) -> types.char_ptr: ...


def test_cfunc_with_name():
    assert c_strchr(b"hello", b"o") == b"o"
