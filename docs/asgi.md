If you want to serve your project with async support, you need an ASGI server. The following table gives an overview of commonly used ASGI servers and their compatibility with this project.

| ASGI server                                                                                        | Compatibility                            |
|----------------------------------------------------------------------------------------------------|------------------------------------------|
| [Uvicorn](https://github.com/encode/uvicorn)                                                       | :material-check: Compatible              |
| [gunicorn with UvicornWorker](https://www.uvicorn.org/deployment/#gunicorn)                        | :material-alert: Not compatible          |
| [Django runserver](https://docs.djangoproject.com/en/dev/ref/django-admin/#django-admin-runserver) | :material-help: Unknown / not tested yet |
| [Hypercorn](https://github.com/pgjones/hypercorn)                                                  | :material-help: Unknown / not tested yet |
| [Daphne](https://github.com/django/daphne)                                                         | :material-help: Unknown / not tested yet |
| [Granian](https://github.com/emmett-framework/granian)                                             | :material-help: Unknown / not tested yet |
