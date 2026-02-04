from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Iterable, List


class RootedGraph(ABC):
    """RootedGraph abstraction.

    Any graph explored by BFS must implement:
      - roots(): initial node(s)
      - neighbors(node): successor node(s)

    Nodes should be hashable if BFS uses a visited set.
    """

    @abstractmethod
    def roots(self) -> List[Any]:
        """Return the initial node(s) of the exploration."""
        raise NotImplementedError

    @abstractmethod
    def neighbors(self, node: Any) -> Iterable[Any]:
        """Return successor node(s) of `node`."""
        raise NotImplementedError
