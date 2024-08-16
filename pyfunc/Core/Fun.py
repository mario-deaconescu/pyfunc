from dataclasses import dataclass
from typing import ParamSpec, TypeVar, Concatenate, Unpack, Generic
from functools import partial
from collections.abc import Callable


@dataclass
class single[T, U]:
    _value: Callable[[T], U]

    def __rrshift__(self, other: T) -> U:
        return self._value(other)

    def __call__(self, value: T) -> U:
        return self._value(value)


def fun1[T, U](f: Callable[[T], U]) -> single[T, U]:
    return single(f)


@fun1
def curry[T, * P, U](function: Callable[[T, *P], U]) -> Callable[[*P], Callable[[T], U]]:
    return lambda *p: lambda t: function(t, *p)
