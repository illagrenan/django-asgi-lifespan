# Original idea

Thanks to [this great answer on StackOverflow](https://stackoverflow.com/a/72634224/752142), this package was created.

# Source code

* The idea to use [Django signals](https://docs.djangoproject.com/en/dev/topics/signals/) in the ASGI handler comes from this closed pull request: [https://github.com/django/django/pull/13636](https://github.com/django/django/pull/13636)
* The implementation of lifespan handling is based on the code sample [from ASGI specification](https://asgi.readthedocs.io/en/latest/specs/lifespan.html).
* The design and usage is inspired by [Starlette](https://www.starlette.io/lifespan/) and [FastAPI](https://fastapi.tiangolo.com/advanced/events/).

# Package and repository structure

This package is based on [waynerv/cookiecutter-pypackage](https://github.com/waynerv/cookiecutter-pypackage) ([Cookiecutter](https://github.com/audreyr/cookiecutter) template). The main difference from the original template is that this project does not use [Pre-commit hooks](https://pre-commit.com/). All dev tools can be run manually via [Taskfiles](https://github.com/illagrenan/django-asgi-lifespan/blob/main/Taskfile.yml).
