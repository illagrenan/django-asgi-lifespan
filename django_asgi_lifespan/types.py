# -*- encoding: utf-8 -*-
# ! python3

from typing import TypeAlias, AsyncContextManager, Any, MutableMapping

LifespanManager: TypeAlias = AsyncContextManager[MutableMapping[str, Any]]
State: TypeAlias = MutableMapping[str, Any]
