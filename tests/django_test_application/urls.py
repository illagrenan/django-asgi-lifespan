# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import logging
from typing import Final

from django.conf.urls import include
from django.urls import path

logger: Final = logging.getLogger(__name__)

urlpatterns = [
    path("", include("tests.django_test_application.test_app.urls", namespace="test_app")),
]
