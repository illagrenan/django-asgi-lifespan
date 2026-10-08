from __future__ import annotations

from unittest.mock import AsyncMock, Mock

import django
import pytest

from django_asgi_lifespan.compat import CompatAsyncSignal


@pytest.mark.skipif(
    django.VERSION < (5, 0),
    reason="Django 4.2 returns live receivers in a different shape",
)
@pytest.mark.asyncio
async def test_compat_asend_async_only_supports_year_based_django_versions(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(django, "VERSION", (2028, 0, 0, "final", 0))
    signal = CompatAsyncSignal()
    async_receiver = AsyncMock(return_value="state")
    sync_receiver = Mock()
    signal.connect(async_receiver)
    signal.connect(sync_receiver)

    responses = await signal.compat_asend_async_only(sender=None)

    assert responses == [(async_receiver, "state")]
    async_receiver.assert_awaited_once()
    sync_receiver.assert_not_called()
