# -*- encoding: utf-8 -*-
# ! python3

from typing import TypeAlias, AsyncContextManager, Mapping, Any

LifespanManager: TypeAlias = AsyncContextManager[Mapping[str, Any]]
