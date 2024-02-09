# -*- encoding: utf-8 -*-
# ! python3

import asyncio
import logging
from typing import Final

from asgiref.sync import sync_to_async
from django.dispatch import Signal
from django.dispatch.dispatcher import NO_RECEIVERS

logger: Final = logging.getLogger(__name__)


class PatchedSignal(Signal):
    async def asend(self, sender, **named):
        """
        For details see:

            * https://code.djangoproject.com/ticket/35174
            * https://stackoverflow.com/q/77811591/752142
        """
        if (
            not self.receivers
            or self.sender_receivers_cache.get(sender) is NO_RECEIVERS
        ):
            return []
        sync_receivers, async_receivers = self._live_receivers(sender)
        if sync_receivers:

            @sync_to_async
            def sync_send():
                responses = []
                for receiver in sync_receivers:
                    response = receiver(signal=self, sender=sender, **named)
                    responses.append((receiver, response))
                return responses

        else:
            # >>>>>>
            # THIS IS THE PATCHED PART:
            async def sync_send():
                return []

            # <<<<<<

        responses, async_responses = await asyncio.gather(
            sync_send(),
            asyncio.gather(
                *(
                    receiver(signal=self, sender=sender, **named)
                    for receiver in async_receivers
                )
            ),
        )
        responses.extend(zip(async_receivers, async_responses))

        return responses
