from dataclasses import dataclass
from typing import Optional, Callable, TypeVar

from pyfunc.Core.Fun import fun1
from pyfunc.Trace import trace


@dataclass
class Some[T]:
    _value: T


T = TypeVar('T')

t = Optional[Some[T]]


@fun1
@trace
def some[T](value: T) -> t[T]:
    return Some(value)

@trace
def map[T, U](optional: t[T], f: Callable[[T], U]) -> t[U]:
    match optional:
        case None:
            return None
        case Some(x):
            return Some(f(x))

@trace
def bind[T, U](optional: t[T], f: Callable[[T], t[U]]) -> t[U]:
    match optional:
        case None:
            return None
        case Some(x):
            return f(x)

@trace
def some_if[T](condition: bool, value: T) -> t[T]:
    return Some(value) if condition else None