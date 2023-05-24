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
    """A subclass of ASGIHandler that supports the ASGI Lifespan protocol."""

    async def __call__(
        self, scope: Scope, receive: ASGIReceiveCallable, send: ASGISendCallable
    ) -> None:
        """
        If scope type is lifespan, handle lifespan request.
        Otherwise, delegate to the superclass' call method.

        The base Django `ASGIHandler` can only handle http scopes.
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
        """Process lifespan request events."""
        while True:
            message = await receive()

            match message["type"]:
                case "lifespan.startup":
                    await self._process_lifespan_event(signals.asgi_startup, scope)
                    await send(
                        LifespanStartupCompleteEvent(type="lifespan.startup.complete")
                    )
                case "lifespan.shutdown":
                    await self._process_lifespan_event(signals.asgi_shutdown, scope)
                    await send(
                        LifespanShutdownCompleteEvent(type="lifespan.shutdown.complete")
                    )
                    return
                case _:
                    raise ValueError(
                        f"Unknown lifespan message type: {message['type']}"
                    )

    async def _process_lifespan_event(
        self, signal: Signal, scope: LifespanScope
    ) -> None:
        """
        Dispatch the given signal and process any responses.
        Async responses are awaited, synchronous responses are called.
        """
        logger.debug("Dispatching signal: %s", signal)

        # [(receiver, response), ...]
        response = signal.send(self.__class__, scope=scope)

        for _, response in response:
            if not response:
                continue

            if inspect.isawaitable(response):
                await response
            else:
                response()
