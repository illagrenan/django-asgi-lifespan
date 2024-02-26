# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import pytest

from django_asgi_lifespan.asgi import get_asgi_application


@pytest.fixture(scope="session")
def application():
    return get_asgi_application()
