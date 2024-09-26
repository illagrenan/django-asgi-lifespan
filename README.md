<h1>Django ASGI Handler with Lifespan protocol support</h1>

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![pypi](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pypi](https://img.shields.io/pypi/v/django-asgi-lifespan.svg)](https://pypi.org/project/django-asgi-lifespan/)
[![Python version](https://img.shields.io/pypi/pyversions/django-asgi-lifespan.svg?logo=python&logoColor=white&label=python)](https://pypi.org/project/django-asgi-lifespan/)
![Supported Django](https://img.shields.io/badge/django%20versions-%5E4.2%20||%20%5E5.0.3-blue.svg?logo=django&logoColor=white)
<br>
[![Build Status](https://github.com/illagrenan/django-asgi-lifespan/actions/workflows/development.yml/badge.svg)](https://github.com/illagrenan/django-asgi-lifespan/actions/workflows/development.yml)
[![codecov](https://codecov.io/gh/illagrenan/django-asgi-lifespan/branch/main/graphs/badge.svg)](https://codecov.io/github/illagrenan/django-asgi-lifespan)

* Documentation: <https://illagrenan.github.io/django-asgi-lifespan>
* PyPI: <https://pypi.org/project/django-asgi-lifespan/>
* License: [MIT](https://choosealicense.com/licenses/mit/)

## Main features

``` py hl_lines="4"  linenums="1"
async def example_view(request) -> HttpResponse:
    # The client is instanciated just once when the application starts,
    # and closed when the server shuts down
    httpx_client: httpx.AsyncClient = request.state["httpx_client"]
```

* The package includes a Django `ASGIHandler` subclass that handles the [ASGI Lifespan Protocol](https://asgi.readthedocs.io/en/latest/specs/lifespan.html) without affecting HTTP request handling.
* [Startup](https://asgi.readthedocs.io/en/latest/specs/lifespan.html#startup-receive-event)
  and [Shutdown](https://asgi.readthedocs.io/en/latest/specs/lifespan.html#shutdown-receive-event) Lifespan events are
  converted to [Django signals](https://docs.djangoproject.com/en/4.0/topics/signals/).
* The package allows for awaiting on signal receivers. This means you can set up things like an [aiohttp `ClientSession`](https://docs.aiohttp.org/en/stable/client_reference.html) or an [HTTPX `AsyncClient`](https://www.python-httpx.org/async/) when your app starts, and close them properly when your app ends. This concept is similar to [events in FastAPI](https://fastapi.tiangolo.com/advanced/events/).

## Quickstart

1. Python `^3.10 || ^3.11 || ^3.12 || ^3.13` and Django `^4.2 || ^5.0.3 || ^5.1` are supported. To install this package run:
    ```console linenums="0"
    poetry add django-asgi-lifespan@latest
    ```

    _or_

    ```console linenums="0"
    pip install --upgrade django-asgi-lifespan
    ```

2. Modify `asgi.py` to use a ASGI Lifespan compatible handler.

    ``` py title="asgi.py"
    from django_asgi_lifespan.asgi import get_asgi_application

    django_application = get_asgi_application()


    async def application(scope, receive, send):
        if scope["type"] in {"http", "lifespan"}:
            await django_application(scope, receive, send)
        else:
            raise NotImplementedError(
                f"Unknown scope type {scope['type']}"
            )
    ```

3. Add state middleware:

    ``` python hl_lines="3"
    MIDDLEWARE = [
        # ...
        "django_asgi_lifespan.middleware.LifespanStateMiddleware",
        # ...
    ]
    ```
4. Register [async context manager](https://docs.python.org/3/reference/datamodel.html#async-context-managers):

    ``` py hl_lines="8-17" title="context.py"
    from contextlib import asynccontextmanager

    import httpx

    from django_asgi_lifespan.types import LifespanManager


    @asynccontextmanager
    async def httpx_lifespan_manager() -> LifespanManager:
        state = {
            "httpx_client": httpx.AsyncClient()
        }

        try:
            yield state
        finally:
            await state["httpx_client"].aclose()
    ```

    ``` py hl_lines="12-14" title="apps.py"
    from django.apps import AppConfig

    from django_asgi_lifespan.register import register_lifespan_manager
    from .context import (
        httpx_lifespan_manager,
    )


    class ExampleAppConfig(AppConfig):

        def ready(self):
            register_lifespan_manager(
                context_manager=httpx_lifespan_manager
            )
    ```

5. Use some resource (in this case the HTTPX client) in views.

    ``` py hl_lines="8" title="views.py"
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
    ```

6. Run uvicorn:

    ```console
    uvicorn asgi:application --lifespan=on --port=8080
    ```
