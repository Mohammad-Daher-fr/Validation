from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Iterable, List, Set, Union


# Un "morceau" iSoup = une transition de l'automate de propriété
@dataclass(frozen=True)
class iPiece:
    name: str
    guard: Callable[[Any, Any], bool]  # (sys_cfg, prop_state) -> bool
    effect: Callable[[Any, Any], Any]  # (sys_cfg, prop_state) -> prop_state (ou list)


@dataclass
class iSoup:
    pieces: List[iPiece]
    init: List[Any]
    accepting: Set[Any]


class iSoupSemantics:
    def __init__(self, isoup: iSoup):
        self.isoup = isoup

    def initials(self) -> List[Any]:
        return list(self.isoup.init)

    def accepting(self, prop_state: Any) -> bool:
        return prop_state in self.isoup.accepting

    def actions(self, sys_cfg: Any, prop_state: Any) -> List[iPiece]:
        # Ordre déterministe: on garde l'ordre de self.isoup.pieces
        out: List[iPiece] = []
        for p in self.isoup.pieces:
            if p.guard(sys_cfg, prop_state):
                out.append(p)
        return out

    def execute(self, action: iPiece, sys_cfg: Any, prop_state: Any) -> Iterable[Any]:
        res = action.effect(sys_cfg, prop_state)
        if isinstance(res, list):
            return res
        return [res]
