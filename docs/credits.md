# Original idea

Thanks to [my question on Stackoverflow](https://stackoverflow.com/questions/72614335/how-to-share-initialize-and-close-aiohttp-clientsession-between-django-async-v) and the excellent answer I started working on this package.

# Source code

* The idea to use [Django signals](https://docs.djangoproject.com/en/dev/topics/signals/) in the ASGI handler comes from this closed pull request: [https://github.com/django/django/pull/13636](https://github.com/django/django/pull/13636)
* The implementation is also based on the code sample at [https://asgi.readthedocs.io/en/latest/specs/lifespan.html](https://asgi.readthedocs.io/en/latest/specs/lifespan.html)

# Package and repository structure

This package is based on [waynerv/cookiecutter-pypackage](https://github.com/waynerv/cookiecutter-pypackage) ([Cookiecutter](https://github.com/audreyr/cookiecutter) template). The main difference from the original template is that this project does not use [Pre-commit hooks](https://pre-commit.com/). All dev tools can be run manually via [Taskfiles](https://github.com/illagrenan/django-asgi-lifespan/blob/main/Taskfile.yml).
