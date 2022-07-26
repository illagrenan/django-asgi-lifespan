# -*- encoding: utf-8 -*-
# ! python3

"""Public function for ASGI Application with custom ASGI handler."""

from __future__ import annotations

import logging
from typing import Final

import django

from .handler import LifespanASGIHandler

logger: Final = logging.getLogger(__name__)
__all__ = ["get_asgi_application"]


def get_asgi_application() -> LifespanASGIHandler:
    """
    The public interface to Django's custom ASGI support that supports the lifespan protocol.

    :return: An ASGI 3 callable.
    """
    django.setup(set_prefix=False)
    return LifespanASGIHandler()
