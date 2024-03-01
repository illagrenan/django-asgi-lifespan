# Changelog

<!-- START -->
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Lifespan async context managers are now supported (inspired by [Lifespan events in FastAPI](https://fastapi.tiangolo.com/advanced/events/#lifespan>)). Global variables are no longer necessary for the state management; objects required throughout the application lifecycle are now held in the lifespan scope state. Further details can be found in [the ASGI spec](https://asgi.readthedocs.io/en/latest/specs/lifespan.html#scope). Previous signals (startup and shutdown) remain supported with no plans for their removal. The new, preferred method to manage state is via an async context manager. This new feature is supported only with Django `^5.0.3`.
- All major asgi servers have been tested, [an overview of their support is in separate page](docs/asgi.md). It is worth mentioning that the gunicorn+uvicorn combo is now working without problems.

### Changed

- Use frontmatter title & description in each language version template
- Replace broken OpenGraph image with an appropriately-sized Keep a Changelog
  image that will render properly (although in English for all languages)
- Fix OpenGraph title & description for all languages so the title and
  description when links are shared are language-appropriate

### Breaking changes

- Drop support for Django `>=4.0.0, <4.2.0` and `>=5.0.0, <5.0.3`. Supported versions include `^4.2 || ^5.0.3`.
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
