from __future__ import annotations

import ctypes

from ctypes.util import find_library
from typing import Callable
from typing import TypeVar
from typing import get_type_hints


_F = TypeVar("_F", bound=Callable)


def cfunc(clib: str | ctypes.CDLL) -> Callable[[_F], _F]:
    """
    Decorator to bind a Python function signature to a C function from a shared library.

    Args:
        clib (str | ctypes.CDLL): The name of the C library (as a string) or a ctypes.CDLL instance.

    Returns:
        Callable[[_F], _F]: A decorator that replaces the Python function with the corresponding C function,
        setting its argument and return types based on the Python type hints.

    Examples:
        >>> from cbridge import cfunc
        >>> from cbridge import types
        >>> from cbridge.types import pointer
        >>> @cfunc("c")
        ... def time(t: types.Pointer[types.ctime_t]) -> types.ctime_t: ...
        >>> print(time(None))
        >>> 1727433600
    """
    clib = ctypes.CDLL(find_library(clib)) if isinstance(clib, str) else clib

    def wrapper(func: _F) -> _F:
        hints = get_type_hints(func)
        restype = hints.pop("return", None)
        argtypes = list(hints.values())
        cfunc = getattr(clib, func.__name__)
        cfunc.restype = restype
        cfunc.argtypes = tuple(argtypes)
        return cfunc

    return wrapper
