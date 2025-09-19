from __future__ import annotations

import pytest

from django_asgi_lifespan.asgi import get_asgi_application
from django_asgi_lifespan.handler import LifespanASGIHandler


@pytest.fixture(scope="session")
def application() -> LifespanASGIHandler:
    return get_asgi_application()
