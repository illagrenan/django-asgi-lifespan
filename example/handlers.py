import httpx

from .types import HTTPXAppConfig


class ASGILifespanSignalHandler:
    app_config: HTTPXAppConfig

    def __init__(self, app_config: HTTPXAppConfig):
        self.app_config = app_config

    async def startup(self, **_):
        self.app_config.httpx_client = httpx.AsyncClient()

    async def shutdown(self, **_):
        self.app_config.httpx_client.aclose()
