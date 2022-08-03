# Django ASGI Handler with Lifespan protocol support

[![pypi](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pypi](https://img.shields.io/pypi/v/django-asgi-lifespan.svg)](https://pypi.org/project/django-asgi-lifespan/)
[![python](https://img.shields.io/pypi/pyversions/django-asgi-lifespan.svg)](https://pypi.org/project/django-asgi-lifespan/)
[![Build Status](https://github.com/illagrenan/django-asgi-lifespan/actions/workflows/development.yml/badge.svg)](https://github.com/illagrenan/django-asgi-lifespan/actions/workflows/development.yml)
[![codecov](https://codecov.io/gh/illagrenan/django-asgi-lifespan/branch/main/graphs/badge.svg)](https://codecov.io/github/illagrenan/django-asgi-lifespan)

* Documentation: <https://illagrenan.github.io/django-asgi-lifespan>
* PyPI: <https://pypi.org/project/django-asgi-lifespan/>
* License: MIT
    
## Features

* This package contains a subclass of the standard Django `ASGIHandler` that can
  handle [ASGI Lifespan Protocol](https://asgi.readthedocs.io/en/latest/specs/lifespan.html). (Note: there is no change in handling HTTP requests.)
* [Startup](https://asgi.readthedocs.io/en/latest/specs/lifespan.html#startup-receive-event)
  and [Shutdown](https://asgi.readthedocs.io/en/latest/specs/lifespan.html#shutdown-receive-event) Lifespan events are
  converted to [Django signals](https://docs.djangoproject.com/en/4.0/topics/signals/).
* Signal **receivers can be awaited**. This way it is possible for example to
  create [aiohttp ClientSession](https://docs.aiohttp.org/en/stable/client_reference.html)
  /[httpx client](https://www.python-httpx.org/async/) when the application starts and close these resources safely when
  the application shuts down. This concept is similar to events in
  FastAPI (<https://fastapi.tiangolo.com/advanced/events/>).

## Quickstart

**:warning: This package is experimental. Lifespan signals work correctly only under uvicorn.**

1. Install the package. Only Python 3.10 and Django 4 are supported. 

    ``` console
    $ pip install --upgrade django-asgi-lifespan
    ```

2. Modify `asgi.py` to use a ASGI Lifespan compatible handler.

    ``` py title="asgi.py"
    from django_asgi_lifespan.asgi import get_asgi_application
    
    django_application = get_asgi_application()
    
    
    async def application(scope, receive, send):
        if scope["type"] in {"http", "lifespan"}:
            await django_application(scope, receive, send)
        else:
            raise NotImplementedError(f"Unknown scope type {scope['type']}")
    ```

3. Subscribe your (async) code to the `asgi_startup` and `asgi_shutdown` Django signals that are sent when the server starts/shuts down. [See usage](https://illagrenan.github.io/django-asgi-lifespan/usage/) for a more advanced code sample.

    ``` py title="handlers.py" 
    import asyncio
    
    import httpx
    
    HTTPX_CLIENT = None
    _signal_lock = asyncio.Lock()
    
    
    async def create_httpx_client():
        global HTTPX_CLIENT
    
        async with _signal_lock:
            if not HTTPX_CLIENT:
                HTTPX_CLIENT = httpx.AsyncClient()
    
    
    async def close_httpx_client():
        if isinstance(HTTPX_CLIENT, httpx.AsyncClient):
            await asyncio.wait_for(asyncio.create_task(HTTPX_CLIENT.aclose()), timeout=5.0)
 
    ```

    ``` py title="apps.py" 
    from django.apps import AppConfig

    from django_asgi_lifespan.signals import asgi_shutdown, asgi_startup
    from .handlers_quickstart import close_httpx_client, create_httpx_client
    
    
    class ExampleAppConfig(AppConfig):
        def ready(self):
            asgi_startup.connect(create_httpx_client)
            asgi_shutdown.connect(close_httpx_client)
    ```

4. Use some resource (in this case the HTTPX client) e.g. in views.

    ``` py title="views.py" 
    from django.http import HttpResponse

    from . import handlers
    
    
    async def my_library_view(*_) -> HttpResponse:
        external_api_response = await handlers_quickstart.HTTPX_CLIENT.get("https://www.example.com/")
    
        return HttpResponse(f"{external_api_response.text[:42]}", content_type="text/plain")

    ```

5. Run uvicorn:

   :warning: Lifespan protocol is not supported if you run uvicorn via gunicorn using [`worker_class`](https://docs.gunicorn.org/en/stable/settings.html#worker-class): `gunicorn -k uvicorn.workers.UvicornWorker`. See
   other [limitations](https://illagrenan.github.io/django-asgi-lifespan/limitations/) in the documentation.

    ``` console 
    uvicorn asgi:application --lifespan=on --port=8080
    ```
