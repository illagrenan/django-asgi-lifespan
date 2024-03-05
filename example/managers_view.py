from http import HTTPStatus

import httpx
from django.http import HttpResponse


async def example_view(request) -> HttpResponse:
    httpx_client: httpx.AsyncClient = request.state["httpx_client"]

    await httpx_client.head("https://www.example.com/")

    return HttpResponse(
        "OK",
        status=HTTPStatus.OK,
        content_type="text/plain; charset=utf-8",
    )
