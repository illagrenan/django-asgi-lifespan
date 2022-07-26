# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import logging
from http import HTTPStatus
from typing import Final

import httpx
from django.apps import apps
from django.http import HttpResponse

logger: Final = logging.getLogger(__name__)


async def my_library_view(*_) -> HttpResponse:
    httpx_client: httpx.AsyncClient = apps.get_app_config("test_app").httpx_client

    if httpx_client.is_closed:
        return HttpResponse(
            "HTTPX Client is closed",
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
            content_type="text/plain",
        )
    else:
        assert not httpx_client.is_closed, "HTTPX Client is closed"
        external_api_response = await httpx_client.get("https://www.example.com/")

        return HttpResponse(f"{external_api_response.text}", content_type="text/plain")
