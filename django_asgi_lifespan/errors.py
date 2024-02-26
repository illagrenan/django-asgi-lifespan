# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

from abc import ABCMeta


class BaseLifespanHandlerError(Exception, metaclass=ABCMeta):
    pass


class MissingScopeStateError(BaseLifespanHandlerError):
    pass
