# -*- encoding: utf-8 -*-
# ! python3

import logging
from typing import Final, Callable, Awaitable

from asgiref.sync import iscoroutinefunction, markcoroutinefunction
from django.core.handlers.asgi import ASGIRequest
from django.http import HttpRequest, HttpResponseBase

logger: Final = logging.getLogger(__name__)


class AsyncMiddleware:
    async_capable = True
    sync_capable = False

    def __init__(
        self, get_response: Callable[[HttpRequest], Awaitable[HttpResponseBase]]
    ) -> None:
        self.get_response = get_response

        if iscoroutinefunction(self.get_response):
            markcoroutinefunction(self)

    async def __call__(self, request: HttpRequest) -> HttpResponseBase:
        if isinstance(request, ASGIRequest):
            setattr(request, "state", request.scope["state"])
        else:
            setattr(request, "state", {})

        return await self.get_response(request)