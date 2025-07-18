# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

from http import HTTPStatus

import pytest
import pytest_asyncio
from asgiref.testing import ApplicationCommunicator
from django.test import AsyncClient


class LifespanAwareAsyncClient(AsyncClient):
    """
    A custom AsyncClient that correctly handles the 'state' parameter
    for lifespan-aware testing in Django 5.2+ without it being
    misinterpreted as an HTTP header.

    This is fix for this commit:
        https://github.com/django/django/commit/083e6239538cbc34ae9781c2e70a8a8dbfcf2817
    """

    def __init__(self, state: dict, **defaults):
        super().__init__(**defaults)
        # Store the state separately to prevent it from being processed as a header.
        self.state = state

    def _base_scope(self, **request):
        """
        Accepts request kwargs, passes them to the parent method, and then
        injects the lifespan state into the resulting scope.
        """
        # Get the default scope from the parent class, passing along all request kwargs.
        scope = super()._base_scope(**request)
        scope["state"] = self.state

        return scope


@pytest.fixture
def scope_state() -> dict:
    return {}


@pytest.fixture
def async_client(scope_state):
    return LifespanAwareAsyncClient(state=scope_state)


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
    assert await communicator.receive_output(timeout=3) == {
        "type": "lifespan.startup.complete"
    }

    response = await async_client.get("/client-from-app-config")

    assert response.status_code == HTTPStatus.OK
    assert response.content.decode("utf-8").startswith("OK app config")

    await communicator.send_input({"type": "lifespan.shutdown"})
    assert await communicator.receive_output(timeout=3) == {
        "type": "lifespan.shutdown.complete"
    }

    response = await async_client.get("/client-from-app-config")
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert "HTTPX Client from app config is closed" in response.content.decode("utf-8")


@pytest.mark.asyncio
async def test_integration_with_scope_state(
    communicator: ApplicationCommunicator, async_client: AsyncClient
):
    await communicator.send_input({"type": "lifespan.startup"})
    assert await communicator.receive_output(timeout=3) == {
        "type": "lifespan.startup.complete"
    }

    response = await async_client.get("/client-from-scope-state")

    assert response.status_code == HTTPStatus.OK
    assert response.content.decode("utf-8").startswith("OK state")

    await communicator.send_input({"type": "lifespan.shutdown"})
    assert await communicator.receive_output(timeout=3) == {
        "type": "lifespan.shutdown.complete"
    }

    response = await async_client.get("/client-from-scope-state")
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert "HTTPX Client from state is closed" in response.content.decode("utf-8")
