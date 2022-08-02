# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

from django_asgi_lifespan.asgi import get_asgi_application

django_application = get_asgi_application()


async def application(scope, receive, send):
    if scope["type"] in {"http", "lifespan"}:
        await django_application(scope, receive, send)
    else:
        raise NotImplementedError(f"Unknown scope type {scope['type']}")
