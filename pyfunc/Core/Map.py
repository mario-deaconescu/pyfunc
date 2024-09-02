from typing import Callable

from pyfunc import Option
from pyfunc.Core import List
from pyfunc.Core.Fun import fun1
from pyfunc.Trace import trace

t = dict


@trace
def get[T, U](d: t[T, U], k: T) -> Option.t[U]:
    match d.get(k):
        case None:
            return None
        case value:
            return Option.Some(value)


@trace
def set[T, U](d: t[T, U], k: T, v: U) -> t[T, U]:
    return {**d, k: v}


@trace
def map[T, U, V](d: t[T, U], f: Callable[[U], V]) -> t[T, V]:
    return {k: f(v) for k, v in d.items()}


@fun1
@trace
def keys[T, U](d: t[T, U]) -> List.t[T]:
    def to_list(l: list[T]) -> List.t[T]:
        match l:
            case []:
                return List.Nil()
            case [head, *tail]:
                return List.Cons(head, to_list(tail))
            case _:  # unreachable
                return List.Nil()

    return to_list(list(d.keys()))


@fun1
@trace
def values[T, U](d: t[T, U]) -> List.t[U]:
    def to_list(l: list[U]) -> List.t[U]:
        match l:
            case []:
                return List.Nil()
            case [head, *tail]:
                return List.Cons(head, to_list(tail))
            case _:  # unreachable
                return List.Nil()

    return to_list(list(d.values()))


@fun1
@trace
def items[T, U](d: t[T, U]) -> List.t[tuple[T, U]]:
    def to_list(l: list[tuple[T, U]]) -> List.t[tuple[T, U]]:
        match l:
            case []:
                return List.Nil()
            case [head, *tail]:
                return List.Cons(head, to_list(tail))
            case _:  # unreachable
                return List.Nil()

    return to_list(list(d.items()))


@trace
def foldl[T, U, V](d: t[T, U], f: Callable[[V, T, U], V], initial: V) -> V:
    def func(acc: V, item: tuple[T, U]) -> V:
        return f(acc, item[0], item[1])

    return List.foldl(items(d), initial=initial, f=func)


@trace
def foldr[T, U, V](d: t[T, U], f: Callable[[V, T, U], V], initial: V) -> V:
    def func(acc: V, item: tuple[T, U]) -> V:
        return f(acc, item[0], item[1])

    return List.foldr(items(d), func, initial)
