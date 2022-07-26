"""Unit test package for django-asgi-lifespan."""

import asyncio
import logging
import sys

from typing import Final

logger: Final = logging.getLogger(__name__)

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    logger.info("Installed `%r` as a loop policy.", asyncio.WindowsSelectorEventLoopPolicy)
