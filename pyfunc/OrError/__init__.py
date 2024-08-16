from dataclasses import dataclass
from typing import TypeVar, Callable

from pyfunc.Core import Map, List
from pyfunc.Core.Fun import fun1


@dataclass
class Ok[T]:
    _value: T


@dataclass
class Error:
    _exception: Exception


T = TypeVar('T')

t = Ok[T] | Error


@fun1
def ok[T](value: T) -> t[T]:
    return Ok(value)


@fun1
def error[T](exception: Exception) -> t[T]:
    return Error(exception)


@fun1
def ok_exn[T](value: t[T]) -> T:
    match value:
        case Ok(x):
            return x
        case Error(e):
            raise e


@fun1
def all[T](list: List.t[t[T]]) -> t[List.t[T]]:
    try:
        return ok(List.map(list, ok_exn))
    except Exception as e:
        return error(e)


@fun1
def all_map[T, U](map: Map.t[T, t[U]]) -> t[Map.t[T, U]]:
    try:
        return ok(Map.map(map, ok_exn))
    except Exception as e:
        return error(e)


@fun1
def try_with[T](f: Callable[[], T]) -> t[T]:
    try:
        return ok(f())
    except Exception as e:
        return error(e)


@fun1
def is_ok[T](value: t[T]) -> bool:
    match value:
        case Ok(_):
            return True
        case Error(_):
            return False


@fun1
def is_error[T](value: t[T]) -> bool:
    return not is_ok(value)


def map[T, U](value: t[T], f: Callable[[T], U]) -> t[U]:
    match value:
        case Ok(x):
            return Ok(f(x))
        case Error(e):
            return Error(e)


def bind[T, U](value: t[T], f: Callable[[T], t[U]]) -> t[U]:
    match value:
        case Ok(x):
            return f(x)
        case Error(e):
            return Error(e)
