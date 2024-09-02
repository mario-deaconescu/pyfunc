from contextlib import contextmanager
from dataclasses import dataclass
from typing import TypeVar, Callable, Generator

from pyfunc.Core import Map, List
from pyfunc.Core.Fun import fun1
from pyfunc.Trace import trace


@dataclass
class Ok[T]:
    _value: T


@dataclass
class Error:
    _exception: Exception


T = TypeVar('T')

t = Ok[T] | Error


@fun1
@trace
def ok[T](value: T) -> t[T]:
    return Ok(value)


@fun1
@trace
def error[T](exception: Exception) -> t[T]:
    return Error(exception)


@fun1
@trace
def ok_exn[T](value: t[T]) -> T:
    match value:
        case Ok(x):
            return x
        case Error(e):
            raise e


@fun1
@trace
def all[T](list: List.t[t[T]]) -> t[List.t[T]]:
    try:
        return ok(List.map(list, ok_exn))
    except Exception as e:
        return error(e)


@fun1
@trace
def all_map[T, U](map: Map.t[T, t[U]]) -> t[Map.t[T, U]]:
    try:
        return ok(Map.map(map, ok_exn))
    except Exception as e:
        return error(e)


@fun1
@trace
def try_with[T](f: Callable[[], T]) -> t[T]:
    try:
        return ok(f())
    except Exception as e:
        return error(e)


@fun1
@trace
def is_ok[T](value: t[T]) -> bool:
    match value:
        case Ok(_):
            return True
        case Error(_):
            return False


@fun1
@trace
def is_error[T](value: t[T]) -> bool:
    return not is_ok(value)


@trace
def map[T, U](value: t[T], f: Callable[[T], U]) -> t[U]:
    match value:
        case Ok(x):
            return Ok(f(x))
        case Error(e):
            return Error(e)


@trace
def bind[T, U](value: t[T], f: Callable[[T], t[U]]) -> t[U]:
    match value:
        case Ok(x):
            return f(x)
        case Error(e):
            return Error(e)
