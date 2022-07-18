#!/usr/bin/env python
"""Tests for `django_asgi_lifespan` package."""

from django_asgi_lifespan.django_asgi_lifespan import dummy_function


def test_foo():
    """Test that foo does bar."""
    assert 0 < 42


def test_dummy_function():
    """Test that foo does bar."""
    assert 42 == dummy_function()
