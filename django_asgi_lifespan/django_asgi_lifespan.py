# -*- encoding: utf-8 -*-
# ! python3

"""Foo."""

from __future__ import annotations

import logging
from typing import Final

logger: Final = logging.getLogger(__name__)


def dummy_function():
    """Return 42."""
    logger.info("dummy_function()")
    return 42
