from contextlib import asynccontextmanager

import httpx

from django_asgi_lifespan.types import State


@asynccontextmanager
async def httpx_lifespan_manager() -> State:
    state = {"httpx_client": httpx.AsyncClient()}

    try:
        yield state
    finally:
        await state["httpx_client"].aclose()
