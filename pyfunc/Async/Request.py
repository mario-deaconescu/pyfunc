import asyncio
from dataclasses import dataclass

from httpx import AsyncClient

from . import Effect
from ..Core.Fun import fun1
from ..Trace import trace


@dataclass
class t:
    _value: AsyncClient


@trace
def create_client() -> Effect.t[t]:
    return Effect.map(asyncio.ensure_future(AsyncClient().__aenter__()), lambda c: t(c))


@trace
def get(client: t, url: str) -> Effect.t[str]:
    return Effect.map(asyncio.ensure_future(client._value.get(url)), lambda r: r.text)


@fun1
@trace
def close(client: t) -> Effect.t[None]:
    return Effect.map(asyncio.ensure_future(client._value.aclose()), lambda _: None)
