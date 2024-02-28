!!! warning "Supported Django versions"

    This feature requires Django version `^5.0.3`.  On older versions, you must use [the signals directly](signals.md).

## How does it work

When you execute the Django project using the ASGI server (like uvicorn), it sends lifespan events at its startup. These lifespan events are ignored by the standard Django ASGI handler. The lifespan events include the lifespan scope state, which is a Python dictionary that is preserved by the ASGI server and allowed to be modified by the developer. Hence, it's a suitable location for storing global application states or shared objects. For instance, one could create a shared HTTPX async client to implement connection pooling.

## Accessing the shared state

To access the shared state within a view, your project must include middleware. This middleware assigns a new attribute to the request object, using the state it receives from the ASGI server.

```python hl_lines="3"
MIDDLEWARE = [
    # ...
    'django_asgi_lifespan.middleware.AsyncMiddleware',
    # ...
]
```

## Context manager

You must define an [async context manager](https://docs.python.org/3/reference/datamodel.html#async-context-managers). The code for this can be placed anywhere; in this example, the function is defined in the `context.py` file. The code up to the yield statement is executed when the ASGI server starts, and the remaining part is executed when the server shuts down.

``` py hl_lines="8" title="context.py"
--8<-- "example/context.py"
```

## Registering the context manager

The manager that you have just defined needs to be registered. The most suitable location for registration is [Django AppConfig](https://docs.djangoproject.com/en/dev/ref/applications/#application-configuration).

``` py hl_lines="12-14" title="apps.py"
--8<-- "example/managers_app.py"
```

## View

After the above steps, you can access the shared state in the views.

``` py hl_lines="8" title="views.py"
--8<-- "example/managers_view.py"
```
