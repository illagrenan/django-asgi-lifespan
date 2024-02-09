# -*- encoding: utf-8 -*-
# ! python3

"""Subclass of Django ASGIHandler with ASGI Lifespan support."""

from __future__ import annotations

import inspect
import logging
from typing import Final

from asgiref.typing import (
    ASGIReceiveCallable,
    ASGIReceiveEvent,
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
    lifespan_state = {}

    async def __call__(
        self, scope: Scope, receive: ASGIReceiveCallable, send: ASGISendCallable
    ) -> None:
        """
        If scope type is lifespan, handle lifespan request.
        Otherwise, delegate to the superclass' call method.

        The base Django `ASGIHandler` can only handle http scope.
        """
        if scope["type"] == "lifespan":
            await self._handle_lifespan(scope, receive, send)
        elif scope['type'] == 'http':
            # Add the lifespan state to the HTTP scope
            scope.setdefault('state', {}).update(self.lifespan_state)
            await super().__call__(scope, receive, send)
        else:
            await super().__call__(scope, receive, send)

    async def _handle_lifespan(
        self,
        scope: LifespanScope,
        receive: ASGIReceiveCallable,
        send: ASGISendCallable,
    ) -> None:
        """Process lifespan request events."""
        while True:
            message: ASGIReceiveEvent = await receive()

            match message["type"]:
                case "lifespan.startup":
                    await self._process_lifespan_event(signals.asgi_startup, scope)
                    await send(
                        LifespanStartupCompleteEvent(type="lifespan.startup.complete")
                    )
                case "lifespan.shutdown":
                    print("shutdown is called!")
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
        """
        logger.debug("Dispatching signal: %s", signal)

        if callable(getattr(signal, "asend", None)):
            logger.debug("Awaiting signal using native `asend` method: %s", signal)
            await signal.asend(self.__class__, scope=scope)
        else:
            logger.debug("Sending signal using synchronous `send` method: %s", signal)
            response = signal.send(self.__class__, scope=scope)

            for _, response in response:
                if not response:
                    continue

                if inspect.isawaitable(response):
                    await response
                else:
                    response()
