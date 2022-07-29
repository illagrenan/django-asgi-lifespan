# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

from django.apps import AppConfig

from django_asgi_lifespan.signals import asgi_shutdown, asgi_startup
from .handlers import ASGILifespanSignalHandler


class TestAppConfig(AppConfig):
    name = "tests.django_test_application.test_app"

    def ready(self):
        singal_handler = ASGILifespanSignalHandler(app_config=self)

        asgi_startup.connect(singal_handler.startup, weak=False)
        asgi_shutdown.connect(singal_handler.shutdown, weak=False)
