from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Iterable, List


@dataclass(frozen=True)
class Action:
    """Une action possible depuis un état (optionnellement pondérée)."""

    name: str
    data: Any = None
    weight: int = 1


class LanguageSemantics(ABC):
    """Abstraction au-dessus d'un RootedGraph."""

    @abstractmethod
    def initials(self) -> List[Any]:
        """États initiaux (équivalent roots)."""
        raise NotImplementedError

    @abstractmethod
    def actions(self, state: Any) -> List[Action]:
        """Actions possibles depuis state."""
        raise NotImplementedError

    @abstractmethod
    def execute(self, state: Any, action: Action) -> Iterable[Any]:
        """Exécute action depuis state et renvoie les états successeurs."""
        raise NotImplementedError
