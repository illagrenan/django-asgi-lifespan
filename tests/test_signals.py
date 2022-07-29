# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

from unittest.mock import AsyncMock, Mock

import pytest
from asgiref.testing import ApplicationCommunicator

from django_asgi_lifespan.asgi import get_asgi_application
from django_asgi_lifespan.signals import asgi_shutdown, asgi_startup


@pytest.fixture(scope="session")
def application():
    return get_asgi_application()


@pytest.mark.asyncio
async def test_lifespan_protocol_handler_sends_django_signals(application):
    startup_handler = AsyncMock()
    shutdown_handler = AsyncMock()

    asgi_startup.connect(startup_handler)
    asgi_shutdown.connect(shutdown_handler)

    assert startup_handler.call_count == 0
    assert shutdown_handler.call_count == 0
    startup_handler.assert_not_awaited()
    shutdown_handler.assert_not_awaited()

    communicator = ApplicationCommunicator(application, scope={"type": "lifespan"})
    await communicator.send_input({"type": "lifespan.startup"})
    response = await communicator.receive_output()

    assert response["type"] == "lifespan.startup.complete"
    assert startup_handler.call_count == 1
    assert shutdown_handler.call_count == 0
    startup_handler.assert_awaited_once()
    shutdown_handler.assert_not_awaited()

    await communicator.send_input({"type": "lifespan.shutdown"})
    response = await communicator.receive_output()

    assert response["type"] == "lifespan.shutdown.complete"
    assert startup_handler.call_count == 1
    assert shutdown_handler.call_count == 1
    startup_handler.assert_awaited_once()
    shutdown_handler.assert_awaited_once()

    asgi_startup.disconnect(startup_handler)
    asgi_shutdown.disconnect(shutdown_handler)

    assert startup_handler.call_count == 1
    assert shutdown_handler.call_count == 1
    startup_handler.assert_awaited_once()
    shutdown_handler.assert_awaited_once()


@pytest.mark.asyncio
async def test_lifespan_protocol_signal_handlers_can_be_sync_functions(application):
    startup_handler = Mock()
    shutdown_handler = Mock()

    asgi_startup.connect(startup_handler)
    asgi_shutdown.connect(shutdown_handler)

    assert startup_handler.call_count == 0
    assert shutdown_handler.call_count == 0

    communicator = ApplicationCommunicator(application, scope={"type": "lifespan"})
    await communicator.send_input({"type": "lifespan.startup"})
    response = await communicator.receive_output()

    assert response["type"] == "lifespan.startup.complete"
    assert startup_handler.call_count == 1
    assert shutdown_handler.call_count == 0
    startup_handler.assert_called_once()
    shutdown_handler.assert_not_called()

    await communicator.send_input({"type": "lifespan.shutdown"})
    response = await communicator.receive_output()

    assert response["type"] == "lifespan.shutdown.complete"
    assert startup_handler.call_count == 1
    assert shutdown_handler.call_count == 1
    startup_handler.assert_called_once()
    shutdown_handler.assert_called_once()

    asgi_startup.disconnect(startup_handler)
    asgi_shutdown.disconnect(shutdown_handler)

    assert startup_handler.call_count == 1
    assert shutdown_handler.call_count == 1
    startup_handler.assert_called_once()
    shutdown_handler.assert_called_once()
