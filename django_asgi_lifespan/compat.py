# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import asyncio
import logging
from typing import Any, Awaitable, Callable, Final, List, Tuple

import django
from asgiref.sync import iscoroutinefunction
from django.dispatch import Signal
from django.dispatch.dispatcher import NO_RECEIVERS

logger: Final = logging.getLogger(__name__)


class CompatAsyncSignal(Signal):
    def _get_async_only_live_receivers(
        self, sender: Any
    ) -> List[Callable[..., Awaitable[Any]]]:
        if not django.get_version().startswith("4."):
            raise ValueError("Unsupported Django version")

        non_weak_receivers = self._live_receivers(sender)
        non_weak_async_receivers = [
            receiver for receiver in non_weak_receivers if iscoroutinefunction(receiver)
        ]
        return non_weak_async_receivers

    async def compat_asend_async_only(
        self, sender: Any, **named: Any
    ) -> List[Tuple[Any, Any]]:
        if (
            not self.receivers
            or self.sender_receivers_cache.get(sender) is NO_RECEIVERS
        ):
            return []

        if django.get_version().startswith("5."):
            # Ignore sync receivers
            _, async_receivers = self._live_receivers(sender)
        elif django.get_version().startswith("4.2."):
            async_receivers = self._get_async_only_live_receivers(sender)
        else:
            raise NotImplementedError(
                f"Unsupported Django version: {django.get_version()}"
            )

        # Process async receivers
        async_responses = await asyncio.gather(
            *[
                receiver(signal=self, sender=sender, **named)
                for receiver in async_receivers
            ]
        )

        # Return a list of tuple pairs with the receiver and the response
        return list(zip(async_receivers, async_responses, strict=True))
