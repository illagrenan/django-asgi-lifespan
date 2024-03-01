# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

from typing import cast

from django.apps import AppConfig

from django_asgi_lifespan.register import register_lifespan_manager
from django_asgi_lifespan.signals import asgi_shutdown, asgi_startup
from django_asgi_lifespan.types import LifespanManager

from .handlers import (
    ASGILifespanSignalHandler,
    dummy_lifespan_manager,
    httpx_lifespan_manager,
)


class TestAppConfig(AppConfig):
    name = "tests.django_test_application.test_app"

    def ready(self):
        register_lifespan_manager(
            context_manager=cast(LifespanManager, httpx_lifespan_manager)
        )
        register_lifespan_manager(
            context_manager=cast(LifespanManager, dummy_lifespan_manager)
        )

        signal_handler = ASGILifespanSignalHandler(app_config=self)

        asgi_startup.connect(signal_handler.startup, weak=False)
        asgi_shutdown.connect(signal_handler.shutdown, weak=False)
