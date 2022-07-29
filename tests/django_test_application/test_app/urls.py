# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

from typing import Final

from django.urls import path

from .views import my_library_view

app_name: Final = "test_app"
urlpatterns: Final = [path("test", view=my_library_view, name="test_view")]
