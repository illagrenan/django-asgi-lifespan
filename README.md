# Django ASGI Lifespan

[![pypi](https://img.shields.io/badge/code%20style-black-000000.svg)](ttps://github.com/psf/black)
[![pypi](https://img.shields.io/pypi/v/django-asgi-lifespan.svg)](https://pypi.org/project/django-asgi-lifespan/)
[![python](https://img.shields.io/pypi/pyversions/django-asgi-lifespan.svg)](https://pypi.org/project/django-asgi-lifespan/)
[![Build Status](https://github.com/illagrenan/django-asgi-lifespan/actions/workflows/development.yml/badge.svg)](https://github.com/illagrenan/django-asgi-lifespan/actions/workflows/development.yml)
[![codecov](https://codecov.io/gh/illagrenan/django-asgi-lifespan/branch/main/graphs/badge.svg)](https://codecov.io/github/illagrenan/django-asgi-lifespan)

Django ASGI handle with Lifespan Protocol support

* Documentation: <https://illagrenan.github.io/django-asgi-lifespan>
* GitHub: <https://github.com/illagrenan/django-asgi-lifespan>
* PyPI: <https://pypi.org/project/django-asgi-lifespan/>
* License: MIT

## Features

* This package contains a subclass of the standard Django `ASGIHandler` that can handle [ASGI Lifespan Protocol](https://asgi.readthedocs.io/en/latest/specs/lifespan.html). (Note: there is absolutely no change in handling of HTTP requests.)
* [Startup](https://asgi.readthedocs.io/en/latest/specs/lifespan.html#startup-receive-event) and [Shutdown](https://asgi.readthedocs.io/en/latest/specs/lifespan.html#shutdown-receive-event) Lifespan events are translated to standard [Django signals](https://docs.djangoproject.com/en/4.0/topics/signals/).
* Signal receivers can be awaited. This way it is possible for example to create [aiohttp ClientSession](https://docs.aiohttp.org/en/stable/client_reference.html) / [httpx client](https://www.python-httpx.org/async/) / ... when the application starts and close these resources safely when the application is shutdown. The concept is similar to events in FastAPI (<https://fastapi.tiangolo.com/advanced/events/>).
