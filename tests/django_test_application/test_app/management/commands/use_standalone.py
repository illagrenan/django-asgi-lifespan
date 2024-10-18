# -- encoding: utf-8 --
# ! python3

import asyncio
import logging
from contextlib import AsyncExitStack
from contextvars import ContextVar
from typing import Final, final, Optional, TypedDict

import httpx
from django.conf import settings
from django.core.management.base import BaseCommand

from ...handlers import httpx_lifespan_manager

logger: Final = logging.getLogger(__name__)

client_var: ContextVar[Optional[httpx.AsyncClient]] = ContextVar("client", default=None)
exit_stack_var: ContextVar[Optional[AsyncExitStack]] = ContextVar(
    "exit_stack", default=None
)


class LifespanState(TypedDict):
    httpx_client_from_user: httpx.AsyncClient


async def setup_httpx_client() -> None:
    logger.info("Setting up HTTPX client")

    stack = AsyncExitStack()
    exit_stack_var.set(stack)

    state: LifespanState = await stack.enter_async_context(httpx_lifespan_manager())
    client = state["httpx_client_from_user"]
    client_var.set(client)

    logger.debug("HTTPX client setup complete")


def get_httpx_client() -> httpx.AsyncClient:
    client = client_var.get()
    assert client, "Client not initialized"

    return client


async def cleanup_httpx_client() -> None:
    logger.info("Cleaning up HTTPX client")

    stack = exit_stack_var.get()

    if stack is not None:
        await stack.aclose()
    else:
        logger.warning("No exit stack found during cleanup")

    exit_stack_var.set(None)
    client_var.set(None)

    logger.debug("HTTPX client cleanup complete")


async def dummy_command_task() -> None:
    client = get_httpx_client()

    logger.info("Sending HEAD request to https://www.example.com/")

    response = await client.head("https://www.example.com/")
    response.raise_for_status()

    logger.info("Response status code: %s", response.status_code)


async def demo() -> None:
    try:
        await setup_httpx_client()
        await dummy_command_task()
    finally:
        await cleanup_httpx_client()


@final
class Command(BaseCommand):
    help: str = "Example command to use state outside of request-response cycle."

    def handle(self, *args: str, **options: str) -> None:
        logger.info("Starting command execution")
        asyncio.run(demo(), debug=settings.DEBUG)
        logger.info("Command execution completed")
