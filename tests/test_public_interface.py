from __future__ import annotations

from unittest.mock import MagicMock, patch

from django.core.handlers.asgi import ASGIHandler
from django.dispatch import Signal

from django_asgi_lifespan.asgi import get_asgi_application
from django_asgi_lifespan.signals import asgi_lifespan, asgi_shutdown, asgi_startup


def test_custom_get_asgi_application_returns_asgi_handler() -> None:
    assert isinstance(get_asgi_application(), ASGIHandler)


@patch("django_asgi_lifespan.asgi.django.setup")
def test_custom_get_asgi_application_returns_asgi_handler_calls_django_setup(
    mocked_django_setup: MagicMock,
) -> None:
    assert not mocked_django_setup.called
    get_asgi_application()
    assert mocked_django_setup.called


def test_signals_are_defined() -> None:
    assert isinstance(asgi_startup, Signal)
    assert isinstance(asgi_shutdown, Signal)
    assert isinstance(asgi_lifespan, Signal)
