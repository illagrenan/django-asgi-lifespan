# -*- encoding: utf-8 -*-
# ! python3

"""ASGI lifespan Django signals for server startup and shutdown events."""

from __future__ import annotations

from typing import Annotated, Final

from django.dispatch import Signal

__all__ = ["asgi_startup", "asgi_shutdown"]

asgi_startup: Final[Annotated[Signal, "asgi lifespan startup"]] = Signal()
asgi_shutdown: Final[Annotated[Signal, "asgi lifespan shutdown"]] = Signal()
