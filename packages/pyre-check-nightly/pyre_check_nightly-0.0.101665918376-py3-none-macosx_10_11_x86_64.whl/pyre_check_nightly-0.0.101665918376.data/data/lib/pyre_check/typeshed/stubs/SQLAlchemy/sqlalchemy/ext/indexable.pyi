from typing import Any

from ..ext.hybrid import hybrid_property

class index_property(hybrid_property):
    attr_name: Any
    index: Any
    default: Any
    datatype: Any
    onebased: Any
    def __init__(self, attr_name, index, default=..., datatype: Any | None = ..., mutable: bool = ..., onebased: bool = ...): ...
    def fget(self, instance): ...
    def fset(self, instance, value) -> None: ...
    def fdel(self, instance) -> None: ...
    def expr(self, model): ...
