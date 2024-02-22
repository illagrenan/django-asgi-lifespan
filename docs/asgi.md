If you want to serve your project with async support, you need an ASGI server. The following table gives an overview of commonly used ASGI servers and their compatibility with this project.


!!! tip "ASGI compatibility"

    If there is an incompatibility listed in this table, **your project will work with the server as you are used to**. This plugin only handles lifespan events &mdash; if they are not provided by the ASGI server, the signals will not be handled.

    The same should be valid for other ASGI servers not listed here. If you run into any problems, [please file a Github issue](https://github.com/illagrenan/django-asgi-lifespan/issues/new).

| ASGI server                                                                                        | Lifespan support                | Lifespan scope state support             |
|----------------------------------------------------------------------------------------------------|---------------------------------|------------------------------------------|
| [Uvicorn](https://github.com/encode/uvicorn)                                                       | :fontawesome-solid-check: OK    | :fontawesome-solid-check: OK             |
| [gunicorn with UvicornWorker](https://www.uvicorn.org/deployment/#gunicorn)[^1]                    | :fontawesome-solid-check: OK    | :fontawesome-solid-check: OK             |
| [Granian](https://github.com/emmett-framework/granian)                                             | :fontawesome-solid-check: OK    | :fontawesome-solid-check: OK             |
| [Hypercorn](https://github.com/pgjones/hypercorn)                                                  | :fontawesome-solid-check: OK    | :fontawesome-solid-xmark: Not compatible |
| [Daphne](https://github.com/django/daphne)                                                         | :material-alert: Not compatible | _not relevant_                           |
| [Django runserver](https://docs.djangoproject.com/en/dev/ref/django-admin/#django-admin-runserver) | :material-alert: Not compatible | _not relevant_                           |

[^1]: Please note that gunicorn does not support Windows (<https://github.com/benoitc/gunicorn/issues/524>).

## Hypercorn

Hypercorn supports lifespan protocol. It does not support _lifespan scope state_, see these PRs:

* <https://github.com/pgjones/hypercorn/pull/107>
* <https://github.com/pgjones/hypercorn/pull/110>

## Daphne

Daphne does not support the lifespan protocol at all. See this issue: <https://github.com/django/daphne/issues/264>.

You can use Daphne, but asynchronous start/shutdown signals will not be handled.
