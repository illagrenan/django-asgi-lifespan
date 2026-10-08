from __future__ import annotations

import asyncio
import logging
from typing import Any, Final

import django
from asgiref.sync import iscoroutinefunction
from django.dispatch import Signal
from django.dispatch.dispatcher import NO_RECEIVERS

logger: Final = logging.getLogger(__name__)


class CompatAsyncSignal(Signal):  # type: ignore[misc]
    async def compat_asend_async_only(
        self, sender: Any, **named: Any
    ) -> list[tuple[Any, Any]]:
        if (
            not self.receivers
            or self.sender_receivers_cache.get(sender) is NO_RECEIVERS
        ):
            return []

        if django.VERSION >= (5, 0):
            # Ignore sync receivers
            _, async_receivers = self._live_receivers(sender)
        else:  # Django 4.2
            async_receivers = [
                r for r in self._live_receivers(sender) if iscoroutinefunction(r)
            ]

        # Process async receivers
        async_responses = await asyncio.gather(
            *[
                receiver(signal=self, sender=sender, **named)
                for receiver in async_receivers
            ]
        )

        # Return a list of tuple pairs with the receiver and the response
        return list(zip(async_receivers, async_responses, strict=True))
