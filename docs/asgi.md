To provide asynchronous support for the project, an ASGI server is necessary. The table below presents a summary of popular ASGI servers and their compatibility with this project.

!!! tip "ASGI compatibility"

    If there is an incompatibility listed in this table, **your project will work with the server as you are used to**. This plugin only handles lifespan events &mdash; if they are not provided by the ASGI server, the signals will not be handled.

    The same should be valid for other ASGI servers not listed here. If you run into any problems, [please file a Github issue](https://github.com/illagrenan/django-asgi-lifespan/issues/new).

| ASGI server                                                                                        | Lifespan support                | Lifespan scope state support             |
|----------------------------------------------------------------------------------------------------|---------------------------------|------------------------------------------|
| [Uvicorn](https://github.com/encode/uvicorn)                                                       | :fontawesome-solid-check: Yes   | :fontawesome-solid-check: Yes            |
| [gunicorn with UvicornWorker](https://www.uvicorn.org/deployment/#gunicorn)[^1]                    | :fontawesome-solid-check: Yes   | :fontawesome-solid-check: Yes            |
| [Granian](https://github.com/emmett-framework/granian)                                             | :fontawesome-solid-check: Yes   | :fontawesome-solid-check: Yes            |
| [Hypercorn](https://github.com/pgjones/hypercorn)                                                  | :fontawesome-solid-check: Yes   | :fontawesome-solid-xmark: Not compatible |
| [Daphne](https://github.com/django/daphne)                                                         | :material-alert: Not compatible | _not relevant_                           |
| [Django runserver](https://docs.djangoproject.com/en/dev/ref/django-admin/#django-admin-runserver) | :material-alert: Not compatible | _not relevant_                           |

[^1]: Please note that gunicorn does not support Windows (<https://github.com/benoitc/gunicorn/issues/524>).

## Uvicorn :material-star:

Uvicorn is the most tested ASGI server by the author of this plugin. The author uses uvicorn for development, testing and production. In production it is perfectly fine to use uvicorn without gunicorn, see:

* <https://stackoverflow.com/questions/66362199/what-is-the-difference-between-uvicorn-and-gunicornuvicorn/71546833>
* <https://github.com/encode/uvicorn/issues/303>

## Hypercorn

Hypercorn supports lifespan protocol. It does not support _lifespan scope state_, see these PRs:

* <https://github.com/pgjones/hypercorn/pull/107>
* <https://github.com/pgjones/hypercorn/pull/110>

## Daphne

Daphne does not support the lifespan protocol at all. See this issue: <https://github.com/django/daphne/issues/264>.

You can use Daphne, but asynchronous start/shutdown signals will not be handled.
