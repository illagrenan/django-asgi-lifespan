# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

from http import HTTPStatus

import pytest
from asgiref.testing import ApplicationCommunicator
from django.test import AsyncClient

from django_asgi_lifespan.asgi import get_asgi_application


@pytest.fixture
def communicator():
    return ApplicationCommunicator(application=get_asgi_application(), scope={"type": "lifespan"})


@pytest.fixture
def async_client():
    return AsyncClient()


@pytest.mark.asyncio
async def test_lifespan_protocol_handler_sends_django_signals(communicator, async_client):
    await communicator.send_input({"type": "lifespan.startup"})

    response = await async_client.get("/test")

    assert response.status_code == 200
    assert "Example Domain" in response.content.decode("utf-8")

    await communicator.send_input({"type": "lifespan.shutdown"})

    response = await async_client.get("/test")
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert "HTTPX Client is closed" in response.content.decode("utf-8")
