!!! tip

    Developers are advised to [prefer asynchronous context managers](context_manager.md). Using signals directly is fully supported, and until `v0.2.0` this was the only way to use this plugin &mdash; the only downside is that it is a more low-level way to use it.

## Before you start

This low-level approach uses ASGI lifespan signals directly. The disadvantage is that the developer has to figure out where to store the global shared state. Prefer the more modern approach via [context manager](context_manager.md) &mdash; the global state will be managed by the ASGI server.

## Example use case for lifespan signals

Consider a [Django application](https://docs.djangoproject.com/en/dev/ref/applications/) named `library`. This application retrieves book information from an external API using [HTTPX](https://www.python-httpx.org/). To ensure efficient utilization of network resources (e.g., connection pooling, see: <https://www.python-httpx.org/advanced/#why-use-a-client>), we intend to use the HTTPX client.

# Typehinting

Firstly, we're going to define a [Protocol](https://docs.python.org/3/library/typing.html#typing.Protocol) for typehinting.

This Protocol (`#!python HTTPXAppConfig`) provides an explicit interface for a request that contains a reference to an instance of `#!python httpx.AsyncClient` in its `#!python state` dictionary.

``` py hl_lines="6-7" title="types.py"
--8<-- "example/types.py"
```

# Signal receivers

Next, we create receivers for lifespan signals. A startup receiver that creates an instance of the HTTPX client, and a shutdown receiver that closes the client.

``` py hl_lines="13 16" title="handlers.py"
--8<-- "example/handlers.py"
```

Connect the receivers to the lifespan signals:

``` py hl_lines="12-15" title="apps.py"
--8<-- "example/apps.py"
```

# Access shared state in view

Now we can access the HTTPX client instance in our view:

``` py hl_lines="10-11" title="views.py"
--8<-- "example/views.py"
```
