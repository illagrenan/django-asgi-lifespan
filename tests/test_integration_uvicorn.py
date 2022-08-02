# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import contextlib
import threading
import time

import httpx
import pytest
import uvicorn
from uvicorn import Config


class Server(uvicorn.Server):
    """
    https://stackoverflow.com/a/64521239/752142
    """

    @contextlib.contextmanager
    def run_in_thread(self):
        thread = threading.Thread(target=self.run)
        thread.start()
        try:
            while not self.started:
                time.sleep(1e-3)
            yield
        finally:
            self.should_exit = True
            thread.join()


@pytest.fixture(scope="session")
def config():
    return Config(
        "tests.django_test_application.asgi:application",
        host="127.0.0.1",
        port=8080,
        log_level="info",
        lifespan="on",
    )


@pytest.fixture(scope="session")
def server(config):
    with Server(config=config).run_in_thread():
        yield


@pytest.mark.parametrize("execution_number", range(3))
@pytest.mark.asyncio
async def test_uvicorn_reponds(server, execution_number):
    """A simple websocket test"""
    assert httpx.get("http://127.0.0.1:8080/test").status_code == 200
