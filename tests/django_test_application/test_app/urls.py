# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

from typing import Final

from django.urls import path

from .views import app_config_view, scope_state_view

app_name: Final = "test_app"
urlpatterns: Final = [
    path(
        "client-from-app-config",
        view=app_config_view,
        name="client_from_app_config_view",
    ),
    path(
        "client-from-scope-state",
        view=scope_state_view,
        name="client_from_scope_state_view",
    ),
]
