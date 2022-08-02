Use case: Let's say you have a [Django application](https://docs.djangoproject.com/en/dev/ref/applications/) named `library`. This application retrieves book information from an external API using HTTPX (<https://www.python-httpx.org/>). You want to use the HTTPX Client for efficient usage of network resources (e.g.: connection pooling, see: <https://www.python-httpx.org/advanced/#why-use-a-client>).

# Types

``` py title="types.py"
--8<-- "example/types.py"
```

# Signal handlers

``` py title="handlers.py"
--8<-- "example/apps.py"
```

# Connect ASGI Lifespan signals to the handler

``` py title="apps.py"
--8<-- "example/apps.py"
```

# Access client

``` py title="views.py"
--8<-- "example/views.py"
```
