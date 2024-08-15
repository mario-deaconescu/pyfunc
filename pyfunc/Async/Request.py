import asyncio
from dataclasses import dataclass

from httpx import AsyncClient

from . import Effect


@dataclass
class t:
    _value: AsyncClient


def create_client() -> Effect.t[t]:
    return Effect.map(asyncio.ensure_future(AsyncClient().__aenter__()), lambda c: t(c))


def get(client: t, url: str) -> Effect.t[str]:
    return Effect.map(asyncio.ensure_future(client._value.get(url)), lambda r: r.text)


def close(client: t) -> Effect.t[None]:
    return Effect.map(asyncio.ensure_future(client._value.aclose()), lambda _: None)
