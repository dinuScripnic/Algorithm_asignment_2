from __future__ import annotations

from typing import Protocol, TypeVar, TypeAlias, Literal as L

class Hashable(Protocol):
    def __hash__(self) -> int: ...

ID = TypeVar("ID", bound=Hashable)

MorseStr: TypeAlias = list[L["."] | L["-"] | L[" "] | L["/"]]  # noqa