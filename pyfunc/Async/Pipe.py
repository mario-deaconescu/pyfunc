from collections.abc import AsyncIterable
from dataclasses import dataclass
from typing import Callable
import asyncio

from . import Effect
from ..Core.Fun import fun1


@dataclass
class t[T]:
    _value: AsyncIterable[T]


def map[T, U](pipe: t[T], f: Callable[[T], U]) -> t[U]:
    async def fun():
        async for x in pipe._value:
            yield f(x)

    return t(fun())


def iter[T](pipe: t[T], f: Callable[[T], None]) -> Effect.t[None]:
    async def fun():
        async for x in pipe._value:
            f(x)

    return asyncio.ensure_future(fun())


@fun1
def to_list[T](pipe: t[T]) -> Effect.t[list[T]]:
    async def fun():
        return [x async for x in pipe._value]

    return asyncio.ensure_future(fun())
