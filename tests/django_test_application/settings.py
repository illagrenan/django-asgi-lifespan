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
SECRET_KEY = "se3ret"
