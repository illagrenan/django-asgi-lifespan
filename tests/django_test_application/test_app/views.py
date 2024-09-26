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


async def app_config_view(*_) -> HttpResponse:
    httpx_client: httpx.AsyncClient = apps.get_app_config("test_app").httpx_client
    assert isinstance(httpx_client, httpx.AsyncClient)

    if httpx_client.is_closed:
        return HttpResponse(
            "HTTPX Client from app config is closed",
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
            content_type="text/plain",
        )
    else:
        assert not httpx_client.is_closed, "HTTPX Client is closed"
        await httpx_client.head("https://www.example.com/")

        return HttpResponse(
            f"OK app config ✅ ({timezone.now()})",
            status=HTTPStatus.OK,
            content_type="text/plain; charset=utf-8",
        )


async def scope_state_view(request) -> HttpResponse:
    assert request.state
    assert request.state["httpx_client_from_user"]
    assert isinstance(request.state["httpx_client_from_user"], httpx.AsyncClient)

    httpx_client = request.state["httpx_client_from_user"]

    if httpx_client.is_closed:
        return HttpResponse(
            "HTTPX Client from state is closed",
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
            content_type="text/plain",
        )
    else:
        assert not httpx_client.is_closed, "HTTPX Client is closed"

        response = await httpx_client.head("https://www.example.com/")
        response.raise_for_status()

        return HttpResponse(
            f"OK state ✅ ({timezone.now()}); ID of client: {id(httpx_client)}",
            status=HTTPStatus.OK,
            content_type="text/plain; charset=utf-8",
        )
