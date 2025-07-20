# Changelog

<!-- START -->
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.1] - UNRELEASED

[:material-github: Github release](https://github.com/illagrenan/django-asgi-lifespan/releases/tag/v0.4.1)

### Added

- Add support for Django 5.2 and include it in the testing matrix.

### Changed

- Update all dependencies in pyproject.toml to their latest versions.
- Migrate pyproject.toml to PEP 631 format (move dependencies from `[tool.poetry.dependencies]` to `[project]` section).
- Pin Python upper bound to 3.13 (change from `<3.15` to `<3.14`).

## [0.4.0] - 2024-10-15

[:material-github: Github release](https://github.com/illagrenan/django-asgi-lifespan/releases/tag/v0.4.0)

### Added

- Add support for Python 3.13.

## [0.3.2] - 2024-09-26

[:material-github: Github release](https://github.com/illagrenan/django-asgi-lifespan/releases/tag/v0.3.2)

### Added

- Add support for Django 5.1.
- Test examples using Pyright.

### Changed

- Fix and improve typehints. Use `AbstractAsyncContextManager` type for lifespan manager function (this should fix Pyright errors as reported in the [issue 99](https://github.com/illagrenan/django-asgi-lifespan/issues/99)).

## [0.3.1] - 2024-03-11

[:material-github: Github release](https://github.com/illagrenan/django-asgi-lifespan/releases/tag/v0.3.1)

### Changed

- `AsyncMiddleware` is now called `LifespanStateMiddleware`, the original name was too generic (it was a copy-paste from the Django documentation). The original name will remain as an alias for `LifespanStateMiddleware`, so existing installations should not be affected.

## [0.3.0] - 2024-03-05

[:material-github: Github release](https://github.com/illagrenan/django-asgi-lifespan/releases/tag/v0.3.0)

### Added

- Lifespan async context managers are now supported (inspired by [Lifespan events in FastAPI](https://fastapi.tiangolo.com/advanced/events/#lifespan>)). Global variables are no longer necessary for the state management; objects required throughout the application lifecycle are now held in the lifespan scope state. Further details can be found in [the ASGI spec](https://asgi.readthedocs.io/en/latest/specs/lifespan.html#scope). Previous signals (startup and shutdown) remain supported with no plans for their removal. The new, preferred method to manage state is via an async context manager.
- All major ASGI servers have been tested, [an overview of their support is in separate page](docs/asgi.md). It&nbsp;is worth mentioning that the gunicorn+uvicorn combo is now working without problems.
- Development: Add support for [pre-commit](https://pre-commit.com/).

### Changed

- More tests.
- Better documentation.

### Breaking changes :material-alert-box:

- Drop support for Django `>=4.0.0, <4.2.0` and `>=5.0.0, <5.0.3`. Supported versions include `^4.2 || ^5.0.3` (`^4.2` is LTS).
- If lifespan signals fail, two new events are sent to the ASGI server: `lifespan.startup.failed` and `lifespan.shutdown.failed`. This could stop servers, like uvicorn, from starting if a `lifespan.startup.failed` event happens. This update makes it easier to find and fix errors, as they are not hidden anymore.

## [0.2.0] - 2024-02-09

[:material-github: Github release](https://github.com/illagrenan/django-asgi-lifespan/releases/tag/v0.2.0)

### Added

* Support for Django 5. :tada:
  <br>
  Support for Django 5 has proven problematic due to this bug: <https://code.djangoproject.com/ticket/35174>. As soon as a new version of Django is released with a fix, a new version of this plugin will be released. At the moment, this plugin includes the Signal handler from here: <https://github.com/django/django/pull/17837>.
* Support for Python 3.12.

## [0.1.0] - 2022-08-03

[:material-github: Github release](https://github.com/illagrenan/django-asgi-lifespan/releases/tag/v0.1.0)

* Initial release.
