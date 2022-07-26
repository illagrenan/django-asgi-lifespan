from typing import Protocol

import httpx


class HTTPXAppConfig(Protocol):
    httpx_client: httpx.AsyncClient
