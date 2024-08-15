import asyncio
from asyncio import Future
from typing import Callable

t = Future


def of[T](value: T) -> t[T]:
    future = Future()
    future.set_result(value)
    return future


def map[T, U](effect: t[T], f: Callable[[T], U]) -> t[U]:
    new_t: t[U] = t()
    effect.add_done_callback(
        lambda future: None if new_t.cancelled() else new_t.set_result(f(future.result())))
    return new_t


def bind[T, U](effect: t[T], f: Callable[[T], t[U]]) -> t[U]:
    new_t: t[U] = t()
    effect.add_done_callback(
        lambda future: None if new_t.cancelled() else f(future.result()).add_done_callback(
            lambda future: None if new_t.cancelled() else new_t.set_result(future.result())))
    return new_t


def after[T](delay: float, value: T) -> t[T]:
    future = Future()
    asyncio.get_event_loop().call_later(delay, future.set_result, value)
    return future


def sync[T](effect: t[T]) -> T:
    return asyncio.get_event_loop().run_until_complete(effect)