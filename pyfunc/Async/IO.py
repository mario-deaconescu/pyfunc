import io
from dataclasses import dataclass
from typing import Literal

from . import Effect
from . import Pipe

import aiofiles
import asyncio


@dataclass
class t:
    _value: aiofiles.threadpool.text.AsyncTextIOWrapper


def open(filename: str, mode: Literal['r', 'w']) -> Effect.t[t]:
    # Check if file exists
    if mode == 'r':
        with io.open(filename, 'r'):
            pass
    return Effect.map(asyncio.ensure_future(aiofiles.open(filename, mode=mode).__aenter__()), lambda f: t(f))


def read(io: t) -> Effect.t[str]:
    return asyncio.ensure_future(io._value.read())


def read_lines(io: t) -> Pipe.t[str]:
    async def f():
        async for line in io._value:
            yield line

    return Pipe.t(f())
