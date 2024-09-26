# -*- encoding: utf-8 -*-
# ! python3

from collections.abc import AsyncGenerator, MutableMapping
from typing import Any, TypeAlias

State: TypeAlias = MutableMapping[str, Any]
LifespanManager: TypeAlias = AsyncGenerator[State, None]
