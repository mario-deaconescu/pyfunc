import io
from dataclasses import dataclass
from typing import Literal

from . import Effect
from . import Pipe

import aiofiles
import asyncio

from ..Core.Fun import fun1
from ..Trace import trace


@dataclass
class t:
    _value: aiofiles.threadpool.text.AsyncTextIOWrapper


@trace
def open(filename: str, mode: Literal['r', 'w']) -> Effect.t[t]:
    # Check if file exists
    if mode == 'r':
        with io.open(filename, 'r'):
            pass
    return Effect.map(asyncio.ensure_future(aiofiles.open(filename, mode=mode).__aenter__()), lambda f: t(f))


@fun1
@trace
def read(io: t) -> Effect.t[str]:
    return asyncio.ensure_future(io._value.read())


@fun1
def read_lines(io: t) -> Pipe.t[str]:
    async def f():
        async for line in io._value:
            yield line

    return Pipe.t(f())
