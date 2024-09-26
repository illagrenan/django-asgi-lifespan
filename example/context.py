from contextlib import asynccontextmanager

import httpx

from django_asgi_lifespan.types import LifespanManager


@asynccontextmanager
async def httpx_lifespan_manager() -> LifespanManager:
    state = {"httpx_client": httpx.AsyncClient()}

    try:
        yield state
    finally:
        await state["httpx_client"].aclose()
