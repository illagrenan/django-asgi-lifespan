# -*- encoding: utf-8 -*-
# ! python3
from __future__ import annotations

import inspect
import logging
from dataclasses import dataclass
from typing import Final, List, Callable, Tuple, Any

from asgiref.typing import LifespanScope
from django.dispatch import Signal

from django_asgi_lifespan.errors import MissingScopeStateError
from django_asgi_lifespan.types import LifespanManager

logger: Final = logging.getLogger(__name__)


@dataclass(frozen=True)
class LifespanSender:
    pass


async def dispatch_lifespan_event(*, signal: Signal, scope: LifespanScope) -> None:
    """
    Dispatches the given signal.
    """
    logger.debug("Dispatching signal: %s", signal)


    if callable(getattr(signal, "asend", None)):
        logger.debug("Awaiting signal using native `asend` method: %s", signal)
        await signal.asend(sender=LifespanSender, scope=scope)
    else:
        logger.debug("Sending signal using synchronous `send` method: %s", signal)
        response = signal.send(sender=LifespanSender, scope=scope)

        # Synchronous send method returns coroutine objects, that need to be awaited
        for _, response in response:
            if not response:
                continue

            if inspect.isawaitable(response):
                await response
            else:
                response()

    logger.debug("Signal: %s dispatched", signal)


async def dispatch_lifespan_state_context_event(
    signal: Signal, scope: LifespanScope
) -> List[Callable[[], LifespanManager]]:
    """
    Dispatches the given signal. Returns a list of async context managers.
    """
    logger.debug("Dispatching signal: %s", signal)

    if "state" not in scope:
        logger.warning("Missing state in scope. Cannot dispatch signal.")
        raise MissingScopeStateError("Missing state in scope. Cannot dispatch signal.")

    if signal.receivers and not callable(getattr(signal, "asend", None)):
        raise NotImplementedError("Synchronous signal dispatch is not supported.")

    logger.debug("Awaiting signal using native `asend` method: %s", signal)

    # List of tuple pairs [(receiver, response), ...].
    receiver_responses: List[Tuple[Any, Callable[[], LifespanManager]]] = (
        await signal.asend(LifespanSender, scope=scope, state=scope["state"])
    )
    context_managers = [context_manager for _, context_manager in receiver_responses]

    return context_managers
