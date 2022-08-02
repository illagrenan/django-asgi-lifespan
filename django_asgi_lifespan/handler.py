# -*- encoding: utf-8 -*-
# ! python3

"""Subclass of Django ASGIHandler with ASGI Lifespan support."""

from __future__ import annotations

import inspect
import logging
from typing import Final

from asgiref.typing import (
    ASGIReceiveCallable,
    ASGISendCallable,
    LifespanScope,
    LifespanShutdownCompleteEvent,
    LifespanStartupCompleteEvent,
    Scope,
)
from django.core.asgi import ASGIHandler
from django.dispatch import Signal

from . import signals

logger: Final = logging.getLogger(__name__)
__all__ = ["LifespanASGIHandler"]


class LifespanASGIHandler(ASGIHandler):
    """Custom ASGIHandler with LIfespan Protocol support."""

    async def __call__(self, scope: Scope, receive: ASGIReceiveCallable, send: ASGISendCallable) -> None:
        """
        Handles lifespan request.

        If scope is not lifespan, calls base class. The standard Django `ASGIHandler` can only handle http scopes.

        :return: Nothing.
        """
        if scope["type"] == "lifespan":
            await self._handle_lifespan(scope, receive, send)
        else:
            await super().__call__(scope, receive, send)

    async def _handle_lifespan(
        self,
        scope: LifespanScope,
        receive: ASGIReceiveCallable,
        send: ASGISendCallable,
    ):
        """Handle a lifespan request."""
        while True:
            message = await receive()

            match message["type"]:
                case "lifespan.startup":
                    await self._handle_lifespan_event(signals.asgi_startup, scope)
                    await send(LifespanStartupCompleteEvent(type="lifespan.startup.complete"))
                case "lifespan.shutdown":
                    await self._handle_lifespan_event(signals.asgi_shutdown, scope)
                    await send(LifespanShutdownCompleteEvent(type="lifespan.shutdown.complete"))
                    return
                case _:
                    raise ValueError("Unknown lifespan message type: %s" % message["type"])

    async def _handle_lifespan_event(self, signal: Signal, scope: LifespanScope) -> None:
        """Handle a lifespan event."""
        logger.debug('Sending "%s" signal', signal)

        # [(receiver, response), ...]
        results = signal.send(self.__class__, scope=scope)

        for _, response in results:
            if not response:
                continue

            if inspect.isawaitable(response):
                await response
            else:
                response()
