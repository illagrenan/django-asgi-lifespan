# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

from http import HTTPStatus

import pytest
import pytest_asyncio
from asgiref.testing import ApplicationCommunicator
from django.test import AsyncClient


@pytest.fixture
def scope_state() -> dict:
    return {}


@pytest.fixture
def async_client(scope_state):
    return AsyncClient(state=scope_state)


@pytest_asyncio.fixture
async def communicator(application, scope_state):
    return ApplicationCommunicator(
        application=application,
        scope={"type": "lifespan", "state": scope_state},
    )


@pytest.mark.asyncio
async def test_integration_with_app_config(
    communicator: ApplicationCommunicator, async_client: AsyncClient
):
    await communicator.send_input({"type": "lifespan.startup"})
    assert await communicator.receive_output() == {"type": "lifespan.startup.complete"}

    response = await async_client.get("/client-from-app-config")

    assert response.status_code == HTTPStatus.OK
    assert response.content.decode("utf-8").startswith("OK app config")

    await communicator.send_input({"type": "lifespan.shutdown"})
    assert await communicator.receive_output() == {"type": "lifespan.shutdown.complete"}

    response = await async_client.get("/client-from-app-config")
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert "HTTPX Client from app config is closed" in response.content.decode("utf-8")


@pytest.mark.asyncio
async def test_integration_with_scope_state(
    communicator: ApplicationCommunicator, async_client: AsyncClient
):
    await communicator.send_input({"type": "lifespan.startup"})
    assert await communicator.receive_output() == {"type": "lifespan.startup.complete"}

    response = await async_client.get("/client-from-scope-state")

    assert response.status_code == HTTPStatus.OK
    assert response.content.decode("utf-8").startswith("OK state")

    await communicator.send_input({"type": "lifespan.shutdown"})
    assert await communicator.receive_output() == {"type": "lifespan.shutdown.complete"}

    response = await async_client.get("/client-from-scope-state")
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert "HTTPX Client from state is closed" in response.content.decode("utf-8")
