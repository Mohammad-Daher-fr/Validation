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
        return sorted(list(self.ls.initials()), key=repr)

    def neighbors(self, state: Any) -> List[Any]:
        out: List[Any] = []

        acts = list(self.ls.actions(state))
        # tri stable par nom si possible, sinon repr
        acts.sort(key=lambda a: getattr(a, "name", repr(a)))

        for act in acts:
            nxts = list(self.ls.execute(state, act))
            nxts.sort(key=repr)

            for nxt in nxts:
                out.append(nxt)
                if self.keep_labels:
                    key = (state, nxt)
                    name = act.name
                    prev = self._labels.get(key)
                    # si plusieurs actions mènent au même nxt, choisir la plus petite (stable)
                    if prev is None or name < prev:
                        self._labels[key] = name

        return out

    def label(self, src: Any, dst: Any) -> str:
        """Optionnel: utile pour afficher une trace d'actions."""
        return self._labels.get((src, dst), "?")
