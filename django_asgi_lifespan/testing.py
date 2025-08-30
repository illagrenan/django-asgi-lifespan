# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

from django.test import AsyncClient


class LifespanAwareAsyncClient(AsyncClient):
    """
    A custom AsyncClient that correctly handles the 'state' parameter
    for lifespan-aware testing in Django 5.2+ without it being
    misinterpreted as an HTTP header.

    This is fix for this commit:
        https://github.com/django/django/commit/083e6239538cbc34ae9781c2e70a8a8dbfcf2817
    """

    def __init__(self, state: dict, **defaults):
        super().__init__(**defaults)
        # Store the state separately to prevent it from being processed as a header.
        self.state = state

    def _base_scope(self, **request) -> dict:
        """
        Accepts request kwargs, passes them to the parent method, and then
        injects the lifespan state into the resulting scope.
        """
        # Get the default scope from the parent class, passing along all request kwargs.
        scope = super()._base_scope(**request)
        scope["state"] = self.state

        return scope
