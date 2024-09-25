# -*- encoding: utf-8 -*-
# ! python3

import logging
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from typing import Callable, Final

from django_asgi_lifespan.signals import asgi_lifespan
from django_asgi_lifespan.types import State

logger: Final = logging.getLogger(__name__)


@dataclass(frozen=True)
class LifespanContextManagerSignalWrapper:
    context_manager: Callable[[], AbstractAsyncContextManager[State]]

    async def receiver(self, **_) -> Callable[[], AbstractAsyncContextManager[State]]:
        return self.context_manager


def register_lifespan_manager(
    *, context_manager: Callable[[], AbstractAsyncContextManager[State]]
) -> None:
    """
    Registers a context manager for lifecycle events
    """
    wrapper = LifespanContextManagerSignalWrapper(context_manager)
    # weak=False is important here, otherwise the receiver will be garbage collected
    asgi_lifespan.connect(wrapper.receiver, sender=None, weak=False, dispatch_uid=None)
