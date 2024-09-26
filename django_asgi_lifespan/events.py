# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import inspect
import logging
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from typing import Any, Callable, Final, List, Tuple

from asgiref.typing import LifespanScope
from django.dispatch import Signal

from django_asgi_lifespan.compat import CompatAsyncSignal
from django_asgi_lifespan.errors import MissingScopeStateError
from django_asgi_lifespan.types import State

logger: Final = logging.getLogger(__name__)


@dataclass(frozen=True)
class LifespanSender:
    pass


async def send_lifespan_signal_compat(*, signal: Signal, scope: LifespanScope) -> None:
    """
    Dispatches the given signal.
    """
    logger.debug("Dispatching signal: %s", signal)

    if callable(getattr(signal, "asend", None)):
        logger.debug("Awaiting signal using native `asend` method: %s", signal)
        await signal.asend(sender=LifespanSender, scope=scope)
    else:
        logger.debug("Sending signal using synchronous `send` method: %s", signal)
        responses = signal.send(sender=LifespanSender, scope=scope)

        # Synchronous send method returns coroutine objects, that need to be awaited
        for _, response in responses:
            if not response:
                continue

            if inspect.isawaitable(response):
                await response
            else:
                response()

    logger.debug("Signal: %s dispatched", signal)


async def send_lifespan_signal_collecting_contexts(
    signal: CompatAsyncSignal, scope: LifespanScope
) -> List[Callable[[], AbstractAsyncContextManager[State]]]:
    """
    Dispatches the given signal. Returns a list of async context managers.
    """
    logger.debug("Dispatching signal: %s", signal)

    if "state" not in scope:
        logger.warning("Missing state in scope. Cannot dispatch signal.")
        raise MissingScopeStateError("Missing state in scope. Cannot dispatch signal.")

    logger.debug(
        "Awaiting signal `%s` using compat `compat_asend_async_only` method.", signal
    )

    # List of tuple pairs [(receiver, response), ...].
    receiver_responses: List[
        Tuple[Any, Callable[[], AbstractAsyncContextManager[State]]]
    ] = await signal.compat_asend_async_only(
        LifespanSender, scope=scope, state=scope["state"]
    )
    context_managers = [context_manager for _, context_manager in receiver_responses]

    return context_managers
