from typing import Callable, Literal

from . import Effect
from pyfunc.Core import List


def map[T, U](list: List.t[T], f: Callable[[T], Effect.t[U]], mode: Literal['sequential', 'parallel']) -> \
        Effect.t[List.t[U]]:
    def map_sequential(list: List.t[T]) -> Effect.t[List.t[U]]:
        match list:
            case List.Nil():
                return Effect.of(List.Nil())
            case List.Cons((head, tail)):
                return Effect.bind(f(head), lambda x: Effect.map(map_sequential(tail), lambda y: List.Cons(x, y)))

    def map_parallel(list: List.t[T]) -> Effect.t[List.t[U]]:
        match list:
            case List.Nil():
                return Effect.of(List.Nil())
            case List.Cons((head, tail)):
                return Effect.bind(f(head),
                                  lambda x: Effect.bind(map_parallel(tail), lambda y: Effect.of(List.Cons(x, y))))

    match mode:
        case 'sequential':
            return map_sequential(list)
        case 'parallel':
            return map_parallel(list)


def iter[T](list: List.t[T], f: Callable[[T], Effect.t[None]], mode: Literal['sequential', 'parallel']) -> \
        Effect.t[None]:
    return Effect.map(map(list, lambda x: f(x), mode), lambda _: None)
