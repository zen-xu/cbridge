# cbridge

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
![GitHub License](https://img.shields.io/github/license/zen-xu/cbridge)
![PyPI - Version](https://img.shields.io/pypi/v/cbridge)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cbridge)
[![Tests](https://github.com/zen-xu/cbridge/actions/workflows/test.yaml/badge.svg)](https://github.com/zen-xu/cbridge/actions/workflows/test.yaml)
[![codecov](https://codecov.io/gh/zen-xu/cbridge/graph/badge.svg?token=6HeWXTrTvn)](https://codecov.io/gh/zen-xu/cbridge)

A Python library that provides a dataclass-like interface for creating ctypes structures, making it easier to work with C libraries and data structures in Python.

## Features

- **Dataclass-like syntax**: Define C structures using familiar Python class syntax with type hints
- **Automatic field management**: Fields are automatically converted to ctypes types based on type annotations
- **Array support**: Built-in support for fixed-size arrays with proper type checking
- **Pointer support**: Easy handling of C pointers with type safety
- **Default values**: Support for default field values and factories
- **Inheritance**: Full support for class inheritance in C structures
- **Memory layout control**: Control structure packing and alignment
- **C function binding**: Decorator for easy binding to C library functions

## Installation

```bash
pip install cbridge
```

## Quick Start

### Creating C Structures

```python
from cbridge import CStruct
from cbridge import types

class Point(CStruct):
    x: types.int32
    y: types.int32

class Rectangle(CStruct):
    top_left: Point
    bottom_right: Point
    color: types.uint32 = 0xFF0000  # Default value

# Create instances
point = Point(x=10, y=20)
rect = Rectangle(
    top_left=Point(x=0, y=0),
    bottom_right=Point(x=100, y=100)
)

print(rect)  # Rectangle(top_left=Point(x=0, y=0), bottom_right=Point(x=100, y=100), color=16711680)
```

### Working with Arrays

```python
from typing import Literal

from cbridge import CStruct
from cbridge import types


class Data(CStruct):
    id: types.int32
    values: types.Array[types.int8, Literal[4]]  # Array of 4 int8 values
    name: types.char_ptr


# Create with array data
data = Data(id=1, values=[1, 2, 3, 4], name=b"test")
print(data.values)  # [1, 2, 3, 4]
```

### C Function Binding

```python
from cbridge import cfunc
from cbridge import types

@cfunc("c")  # Bind to libc
def time(t: types.Pointer[types.ctime_t]) -> types.ctime_t: ...

# Call the C function
current_time = time(None)
print(current_time)
```

### Memory Operations

```python
import array

from cbridge import CStruct
from cbridge import types

class Point(CStruct):
    x: types.int32
    y: types.int32


# Create from buffer
buffer = array.array("B", b"\x01\x00\x00\x00\x02\x00\x00\x00")
point = Point.from_buffer(buffer)
print(point)  # Point(x=1, y=2)
```

## Advanced Usage

### Structure Packing

```python
import ctypes

from cbridge import CStruct
from cbridge import types


class DefaultPackData(CStruct):  # 1-byte alignment
    a: types.char
    b: types.int32


class Pack1Data(CStruct, pack=1):  # 1-byte alignment
    a: types.char
    b: types.int32


print(ctypes.sizeof(DefaultPackData))  # 8 bytes
print(ctypes.sizeof(Pack1Data))  # 5 bytes

```

### Default Values and Factories

```python
from typing import Literal

from cbridge import CStruct
from cbridge import field
from cbridge import types


class Config(CStruct):
    name: types.char_ptr
    timeout: types.int32 = 30
    flags: types.Array[types.int32, Literal[2]] = field(default_factory=lambda: [0, 1])


print(Config(name=b"test"))  # Config(name=b'test', timeout=30, flags=[0, 1])
```

### Pointer Operations

> [!WARNING]
> Python 3.13 and above are currently not supported forward declarations

```python
from cbridge import CStruct
from cbridge import types
from cbridge.types import pointer


class Node(CStruct):
    data: types.int32
    next: "types.Pointer[Node]"


# Create linked list
node1 = Node(data=1, next=None)
node2 = Node(data=2, next=pointer(node1))
node1.next = pointer(node2)

node = node1
data = []
for _ in range(8):
    data.append(node.data)
    node = node.next[0]   # same as *node.next
assert data == [1, 2, 1, 2, 1, 2, 1, 2]
```
