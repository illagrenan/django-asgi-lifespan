from typing import cast

from django.apps import apps
from django.http import HttpResponse

from .types import HTTPXAppConfig


async def my_library_view(*_) -> HttpResponse:
    library_app = cast(HTTPXAppConfig, apps.get_app_config("library"))
    httpx_client = library_app.httpx_client
    external_api_response = await httpx_client.get(
        "https://www.example.com/"
    )

    return HttpResponse(
        f"{external_api_response.text[:42]}",
        content_type="text/plain",
    )
