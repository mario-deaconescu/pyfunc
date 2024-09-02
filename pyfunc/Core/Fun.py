from dataclasses import dataclass
from collections.abc import Callable

from pyfunc.Trace import trace


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
@trace
def curry[T, * P, U](function: Callable[[T, *P], U]) -> Callable[[*P], Callable[[T], U]]:
    return lambda *p: lambda t: function(t, *p)


id = fun1(lambda x: x)


@trace
def compose [T, U, V](f: Callable[[U], V], g: Callable[[T], U]) -> Callable[[T], V]:
    return lambda x: f(g(x))


@trace
def flip[T, U, V](f: Callable[[T, U], V]) -> Callable[[U, T], V]:
    return lambda x, y: f(y, x)


@trace
def uncurry[T, U, V](f: Callable[[T], Callable[[U], V]]) -> Callable[[T, U], V]:
    return lambda x, y: f(x)(y)


@trace
def let[* P, U](*args: *P, f: Callable[[*P], U]) -> U:
    return f(*args)
