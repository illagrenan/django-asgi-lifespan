# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

from unittest.mock import patch

from django.core.handlers.asgi import ASGIHandler
from django.dispatch import Signal

from django_asgi_lifespan.asgi import get_asgi_application
from django_asgi_lifespan.signals import asgi_shutdown, asgi_startup


def test_custom_get_asgi_application_returns_asgi_handler():
    assert isinstance(get_asgi_application(), ASGIHandler)


@patch("django_asgi_lifespan.asgi.django.setup")
def test_custom_get_asgi_application_returns_asgi_handler_calls_django_setup(
    mockend_django_setup,
):
    assert not mockend_django_setup.called
    get_asgi_application()
    assert mockend_django_setup.called


def test_signals_are_defined():
    assert isinstance(asgi_startup, Signal)
    assert isinstance(asgi_shutdown, Signal)
