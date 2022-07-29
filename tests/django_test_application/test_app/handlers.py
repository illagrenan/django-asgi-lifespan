# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import asyncio
import logging
from typing import Final

import httpx
from django.apps import AppConfig

logger: Final = logging.getLogger(__name__)


class ASGILifespanSignalHandler:
    def __init__(self, app_config: AppConfig) -> None:
        self.app_config = app_config

    async def startup(self, **kwargs):
        logger.info("Lifespan->Startup. Initializing HTTPX client.")
        self.app_config.httpx_client = httpx.AsyncClient(http2=False)

    async def shutdown(self, **kwargs):
        logger.info("Lifespan->Shutdown. Closing HTTPX client.")

        try:
            await asyncio.wait_for(asyncio.create_task(self.app_config.httpx_client.aclose()), timeout=5.0)
        except asyncio.TimeoutError:
            logger.info("Timeouted when waiting to close HTTPX client.", exc_info=True)
