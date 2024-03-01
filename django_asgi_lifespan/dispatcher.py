# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import asyncio
import logging
from collections import ChainMap
from contextlib import AsyncExitStack
from typing import Final, List

from asgiref.typing import LifespanScope

from django_asgi_lifespan import signals
from django_asgi_lifespan.errors import MissingScopeStateError
from django_asgi_lifespan.events import (
    send_lifespan_signal_collecting_contexts,
    send_lifespan_signal_compat,
)
from django_asgi_lifespan.types import State

logger: Final = logging.getLogger(__name__)


class LifespanEventDispatcher:
    _exit_stack: AsyncExitStack

    def __init__(self):
        self._exit_stack = AsyncExitStack()

    async def startup(self, scope: LifespanScope) -> None:
        send_compat_task = asyncio.create_task(
            send_lifespan_signal_compat(signal=signals.asgi_startup, scope=scope)
        )
        send_collecting_task = asyncio.create_task(
            send_lifespan_signal_collecting_contexts(signals.asgi_lifespan, scope)
        )

        done, _ = await asyncio.wait(
            [send_compat_task, send_collecting_task],
            return_when=asyncio.ALL_COMPLETED,
        )

        # Raise exception if any, from send_compat_task
        send_compat_task.result()

        # Handle result or catch exception from send_collecting_task
        try:
            context_managers = send_collecting_task.result()
        except MissingScopeStateError:
            logger.warning("Missing state in scope.")
        else:
            # noinspection PyTypeChecker
            context_states: List[State] = await asyncio.gather(
                *(
                    self._exit_stack.enter_async_context(single_context_manager())
                    for single_context_manager in context_managers
                )
            )
            combined_states = ChainMap(*context_states)
            scope["state"].update(combined_states)

    async def shutdown(self, scope: LifespanScope) -> None:
        await asyncio.gather(
            send_lifespan_signal_compat(signal=signals.asgi_shutdown, scope=scope),
            self._exit_stack.aclose(),
        )
