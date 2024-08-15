from dataclasses import dataclass
from typing import Optional, Callable, TypeVar


@dataclass
class Some[T]:
    _value: T


T = TypeVar('T')

t = Optional[Some[T]]


def map[T, U](optional: t[T], f: Callable[[T], U]) -> t[U]:
    match optional:
        case None:
            return None
        case Some(x):
            return Some(f(x))


def bind[T, U](optional: t[T], f: Callable[[T], t[U]]) -> t[U]:
    match optional:
        case None:
            return None
        case Some(x):
            return f(x)


def some_if[T](condition: bool, value: T) -> t[T]:
    return Some(value) if condition else None
