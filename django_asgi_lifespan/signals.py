# -*- encoding: utf-8 -*-
# ! python3

"""ASGI lifespan Django signals for server startup and shutdown events."""

from __future__ import annotations

from typing import Final

from django.dispatch import Signal

from .compat import CompatAsyncSignal

__all__ = ["asgi_startup", "asgi_lifespan", "asgi_shutdown"]

asgi_startup: Final[Signal] = Signal()
asgi_lifespan: Final[CompatAsyncSignal] = CompatAsyncSignal()
asgi_shutdown: Final[Signal] = Signal()
