from django.apps import AppConfig

from django_asgi_lifespan.register import register_lifespan_manager

from .context import (
    httpx_lifespan_manager,
)


class ExampleAppConfig(AppConfig):
    def ready(self):
        register_lifespan_manager(context_manager=httpx_lifespan_manager)
