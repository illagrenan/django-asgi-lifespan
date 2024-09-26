# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Final

import httpx
from django.apps import AppConfig

from django_asgi_lifespan.types import LifespanManager

logger: Final = logging.getLogger(__name__)


@asynccontextmanager
async def httpx_lifespan_manager() -> LifespanManager:
    logger.info("Lifespan: Initializing HTTPX client.")
    state = {"httpx_client_from_user": httpx.AsyncClient(http2=False)}

    try:
        yield state
    finally:
        logger.info("Lifespan: Closing HTTPX client.")
        try:
            await asyncio.wait_for(
                asyncio.create_task(state["httpx_client_from_user"].aclose()),
                timeout=5.0,
            )
        except asyncio.TimeoutError:
            logger.info("Timeouted when waiting to close HTTPX client.", exc_info=True)


@asynccontextmanager
async def dummy_lifespan_manager():
    state = {"correct_number": 42}
    yield state


class ASGILifespanSignalHandler:
    def __init__(self, app_config: AppConfig) -> None:
        self.app_config = app_config

    async def startup(self, **kwargs):
        logger.info("Lifespan->Startup. Initializing HTTPX client.")
        self.app_config.httpx_client = httpx.AsyncClient(http2=False)

        return "this is return value from startup handler"

    async def shutdown(self, **kwargs):
        logger.info("Lifespan->Shutdown. Closing HTTPX client.")

        try:
            await asyncio.wait_for(
                asyncio.create_task(self.app_config.httpx_client.aclose()), timeout=5.0
            )
        except asyncio.TimeoutError:
            logger.info("Timeouted when waiting to close HTTPX client.", exc_info=True)
