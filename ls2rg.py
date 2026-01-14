from __future__ import annotations
from typing import Any, Dict, List, Tuple

from rooted_graph import RootedGraph
from language_semantics import LanguageSemantics, Action


class LS2RG(RootedGraph):
    """
    Adaptateur: LanguageSemantics -> RootedGraph.
    neighbors(state) = union execute(state, a) pour a dans actions(state).
    """

    def __init__(self, ls: LanguageSemantics, keep_labels: bool = False) -> None:
        self.ls = ls
        self.keep_labels = keep_labels
        self._labels: Dict[Tuple[Any, Any], str] = {}

    def roots(self) -> List[Any]:
        return list(self.ls.initials())

    def neighbors(self, state: Any) -> List[Any]:
        out: List[Any] = []
        for act in self.ls.actions(state):
            for nxt in self.ls.execute(state, act):
                out.append(nxt)
                if self.keep_labels:
                    self._labels[(state, nxt)] = act.name
        return out

    def label(self, src: Any, dst: Any) -> str:
        """Optionnel: utile pour afficher une trace d'actions."""
        return self._labels.get((src, dst), "?")
