# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import logging
from http import HTTPStatus
from typing import Final

import httpx
from django.apps import apps
from django.http import HttpResponse
from django.utils import timezone

logger: Final = logging.getLogger(__name__)


async def my_library_view(request) -> HttpResponse:
    # Access state:
    assert request.state
    assert request.state["httpx_client_from_user"]
    assert isinstance(request.state["httpx_client_from_user"], httpx.AsyncClient)
    assert not request.state[
        "httpx_client_from_user"
    ].is_closed, "HTTPX Client is closed"
    # ---------

    # Access app config:
    httpx_client: httpx.AsyncClient = apps.get_app_config("test_app").httpx_client
    # ---------

    if httpx_client.is_closed:
        return HttpResponse(
            "HTTPX Client is closed",
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
            content_type="text/plain",
        )
    else:
        assert not httpx_client.is_closed, "HTTPX Client is closed"
        await httpx_client.head("https://www.example.com/")

        return HttpResponse(
            f"OK ✅ ({timezone.now()})",
            status=HTTPStatus.OK,
            content_type="text/plain; charset=utf-8",
        )
