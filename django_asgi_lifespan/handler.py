# -*- encoding: utf-8 -*-
# ! python3

"""Subclass of Django ASGIHandler with ASGI Lifespan support."""

from __future__ import annotations

import asyncio
import logging
from collections import ChainMap
from contextlib import AsyncExitStack
from typing import Final, List

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

from . import signals
from .errors import MissingScopeStateError
from .events import dispatch_lifespan_event, dispatch_lifespan_state_context_event
from .types import State

logger: Final = logging.getLogger(__name__)
__all__ = ["LifespanASGIHandler"]


class LifespanASGIHandler(ASGIHandler):
    """A subclass of ASGIHandler that supports the ASGI Lifespan protocol."""

    exit_stack: AsyncExitStack

    def __init__(self):
        super().__init__()
        self.exit_stack = AsyncExitStack()

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

                    await dispatch_lifespan_event(
                        signal=signals.asgi_startup, scope=scope
                    )

                    try:
                        await self._handle_startup_event(scope, send)
                    except MissingScopeStateError:
                        logger.warning(
                            "Missing state in scope. Cannot dispatch signal."
                        )

                    await send(
                        LifespanStartupCompleteEvent(type="lifespan.startup.complete")
                    )

                case "lifespan.shutdown":
                    await self._handle_shutdown_event(scope, send)
                    # The return statement is important here to break the while loop
                    # and prevent the function from processing any further messages
                    # after the shutdown event.
                    # Ref.: https://asgi.readthedocs.io/en/latest/specs/lifespan.html
                    return
                case _:
                    raise ValueError(
                        f"Unknown lifespan message type: {message['type']}"
                    )

    async def _handle_startup_event(
        self, scope: LifespanScope, send: ASGISendCallable
    ) -> None:
        context_managers = await dispatch_lifespan_state_context_event(
            signals.asgi_lifespan, scope
        )

        # noinspection PyTypeChecker
        context_states: List[State] = await asyncio.gather(
            *(
                self.exit_stack.enter_async_context(single_context_manager())
                for single_context_manager in context_managers
            )
        )
        combined_states = ChainMap(*context_states)
        scope["state"].update(combined_states)

    async def _handle_shutdown_event(
        self, scope: LifespanScope, send: ASGISendCallable
    ) -> None:
        await dispatch_lifespan_event(signal=signals.asgi_shutdown, scope=scope)
        await self.exit_stack.aclose()
        await send(LifespanShutdownCompleteEvent(type="lifespan.shutdown.complete"))
