# -*- encoding: utf-8 -*-
# ! python3

import logging
from dataclasses import dataclass
from typing import Final

import django

from django_asgi_lifespan.signals import asgi_lifespan
from django_asgi_lifespan.types import LifespanManager

logger: Final = logging.getLogger(__name__)


@dataclass(frozen=True)
class LifespanContextManagerSignalWrapper:
    context_manager: LifespanManager

    async def receiver(self, **_) -> LifespanManager:
        return self.context_manager


def register_lifespan_manager(*, context_manager: LifespanManager) -> None:
    """
    Registers a context manager for lifecycle events
    """
    if django.get_version().startswith("4."):
        return

    wrapper = LifespanContextManagerSignalWrapper(context_manager)
    # weak=False is important here, otherwise the receiver will be garbage collected
    asgi_lifespan.connect(wrapper.receiver, sender=None, weak=False, dispatch_uid=None)
