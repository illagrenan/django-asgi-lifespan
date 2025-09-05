# Lifespan-aware Client

Django 5.2 introduced internal changes in `django.test.AsyncClient` that causes the ASGI scope `state` to be misinterpreted as HTTP headers when passed via request kwargs. This package provides a small helper: `django_asgi_lifespan.testing.LifespanAwareAsyncClient`.

Use it in your tests to ensure `scope["state"]` is correctly injected into the ASGI scope and not treated as headers:

```python
import pytest

from django_asgi_lifespan.testing import LifespanAwareAsyncClient


@pytest.fixture
def scope_state() -> dict:
    return {}


@pytest.fixture
def async_client(scope_state: dict) -> LifespanAwareAsyncClient:
    return LifespanAwareAsyncClient(state=scope_state)


@pytest.mark.asyncio
async def test_my_view(async_client: LifespanAwareAsyncClient) -> None:
    response = await async_client.get("/some-url")
    assert response.status_code == 200
```

Why this is needed: Django [commit 083e6239538cbc34ae9781c2e70a8a8dbfcf2817](https://github.com/django/django/commit/083e6239538cbc34ae9781c2e70a8a8dbfcf2817) changed how extra request kwargs are handled in `AsyncClient`. This helper stores the lifespan `state` on the client instance and injects it into the ASGI scope, preventing it from being interpreted as headers.
