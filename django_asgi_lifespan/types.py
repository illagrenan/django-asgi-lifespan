# -*- encoding: utf-8 -*-
# ! python3

from typing import Any, AsyncContextManager, MutableMapping, TypeAlias

LifespanManager: TypeAlias = AsyncContextManager[MutableMapping[str, Any]]
State: TypeAlias = MutableMapping[str, Any]
