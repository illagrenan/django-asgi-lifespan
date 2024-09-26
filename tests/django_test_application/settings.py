# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "tests.django_test_application.test_app",
]
USE_TZ = True
ROOT_URLCONF = "tests.django_test_application.urls"
SECRET_KEY = "se3ret"  # noqa: S105
MIDDLEWARE = [
    # ...
    "django_asgi_lifespan.middleware.LifespanStateMiddleware",
    # ...
]
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
ALLOWED_HOSTS = ["*"]
