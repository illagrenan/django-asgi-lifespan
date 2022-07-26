"""Unit test package for django-asgi-lifespan."""

import asyncio
import logging
import os
import sys

from typing import Final

logger: Final = logging.getLogger(__name__)


if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) # type: ignore
    logger.info(f"Installed `{asyncio.WindowsSelectorEventLoopPolicy!r}` as a loop policy.")
