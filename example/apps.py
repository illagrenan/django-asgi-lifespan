import httpx
from django.apps import AppConfig

from django_asgi_lifespan.signals import asgi_shutdown, asgi_startup

from .handlers import ASGILifespanSignalHandler


class ExampleAppConfig(AppConfig):
    httpx_client: httpx.AsyncClient

    def ready(self):
        handler = ASGILifespanSignalHandler(app_config=self)

        asgi_startup.connect(handler.startup, weak=False)
        asgi_shutdown.connect(handler.shutdown, weak=False)
