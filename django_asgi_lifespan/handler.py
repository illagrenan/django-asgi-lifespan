# -*- encoding: utf-8 -*-
# ! python3

"""Subclass of Django ASGIHandler with ASGI Lifespan support."""

from __future__ import annotations

import logging
from typing import Final

from asgiref.typing import (
    ASGIReceiveCallable,
    ASGIReceiveEvent,
    ASGISendCallable,
    LifespanScope,
    LifespanShutdownCompleteEvent,
    LifespanShutdownFailedEvent,
    LifespanStartupCompleteEvent,
    LifespanStartupFailedEvent,
    Scope,
)
from django.core.asgi import ASGIHandler

from .dispatcher import LifespanEventDispatcher

logger: Final = logging.getLogger(__name__)
__all__ = ["LifespanASGIHandler"]


class LifespanASGIHandler(ASGIHandler):
    """A subclass of ASGIHandler that supports the ASGI Lifespan protocol."""

    _lifespan_event_dispatcher: LifespanEventDispatcher

    def __init__(self):
        super().__init__()
        self._lifespan_event_dispatcher = LifespanEventDispatcher()

    async def __call__(
        self, scope: Scope, receive: ASGIReceiveCallable, send: ASGISendCallable
    ) -> None:
        """
        If scope type is lifespan, handle lifespan request.
        Otherwise, delegate to the superclass call method.

        The base Django `ASGIHandler` can only handle http scope.
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
    ) -> None:
        """Process lifespan request events."""

        while True:
            message: ASGIReceiveEvent = await receive()

            match message["type"]:
                case "lifespan.startup":
                    try:
                        await self._lifespan_event_dispatcher.startup(scope)
                    except Exception as exc:
                        await send(
                            LifespanStartupFailedEvent(
                                type="lifespan.startup.failed", message=str(exc)
                            )
                        )
                        raise
                    else:
                        await send(
                            LifespanStartupCompleteEvent(
                                type="lifespan.startup.complete"
                            )
                        )

                case "lifespan.shutdown":
                    try:
                        await self._lifespan_event_dispatcher.shutdown(scope)
                    except Exception as exc:
                        await send(
                            LifespanShutdownFailedEvent(
                                type="lifespan.shutdown.failed", message=str(exc)
                            )
                        )
                        raise
                    else:
                        await send(
                            LifespanShutdownCompleteEvent(
                                type="lifespan.shutdown.complete"
                            )
                        )
                        # The return statement is important here to break the while loop
                        # and prevent the function from processing any further messages
                        # after the shutdown event.
                        # Ref.:
                        # https://asgi.readthedocs.io/en/latest/specs/lifespan.html
                        return

                case _:
                    raise ValueError(
                        f"Unknown lifespan message type: {message['type']}"
                    )
