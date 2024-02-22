# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import os
import sys
from pathlib import Path

from django_asgi_lifespan.asgi import get_asgi_application

# This is here so you can run this project:
# $ poetry run uvicorn django_test_application.asgi:application --reload
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_test_application.settings")

# This is temp. fix for Granian:
sys.path.append(str(Path(__file__).parent.parent.resolve(strict=True)))

django_application = get_asgi_application()


async def application(scope, receive, send):
    if scope["type"] in {"http", "lifespan"}:
        await django_application(scope, receive, send)
    else:
        raise NotImplementedError(f"Unknown scope type {scope['type']}")
