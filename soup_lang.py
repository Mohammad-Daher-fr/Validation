# soup_lang.py
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Callable, Iterable, List, Sequence

from language_semantics import LanguageSemantics


Guard = Callable[[Any], bool]
Effect = Callable[[Any], Any]


@dataclass
class Piece:
    """Une règle: si guard(state) alors on peut appliquer effect(state)."""

    name: str
    effect: Effect
    guard: Guard

    def enabled(self, state: Any) -> bool:
        return bool(self.guard(state))

    def apply(self, state: Any) -> Any:
        return self.effect(state)

    def __repr__(self) -> str:
        return f"Piece({self.name})"


@dataclass
class Soup:
    """Un programme: une liste de pièces + un ensemble d'états initiaux."""

    pieces: List[Piece]
    init: List[Any]

    def __repr__(self) -> str:
        names = [p.name for p in self.pieces]
        return f"Soup(pieces={names}, init={self.init})"


class SoupSemantics(LanguageSemantics):
    """
    Sémantique du langage Soup:
      - initials() renvoie les états initiaux
      - actions(state) renvoie les pièces activables
      - execute(state, action) applique une pièce et renvoie une liste de successeurs

    Note: on utilise deepcopy pour éviter les effets de bord si l'état ou le résultat est mutable.
    """

    def __init__(self, program: Soup):
        self.program = program

    def initials(self) -> List[Any]:
        return list(self.program.init)

    def actions(self, state: Any) -> List[Piece]:
        return [p for p in self.program.pieces if p.enabled(state)]

    def execute(self, state: Any, action: Piece) -> Iterable[Any]:
        # Copie défensive (utile si state est mutable, même si guard/effect ne modifient pas)
        state_copy = deepcopy(state)

        result = action.apply(state_copy)

        # Copie défensive du résultat aussi
        return [deepcopy(result)]
