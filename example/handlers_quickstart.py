import asyncio

import httpx

HTTPX_CLIENT = None
_signal_lock = asyncio.Lock()


async def create_httpx_client():
    global HTTPX_CLIENT  # noqa: PLW0603

    async with _signal_lock:
        if not HTTPX_CLIENT:
            HTTPX_CLIENT = httpx.AsyncClient(http2=True)


async def close_httpx_client():
    if isinstance(HTTPX_CLIENT, httpx.AsyncClient):
        await asyncio.wait_for(asyncio.create_task(HTTPX_CLIENT.aclose()), timeout=5.0)
