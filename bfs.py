from __future__ import annotations

from collections import deque
from typing import Any, Callable, Deque, Dict, Iterable, Optional, Set, Tuple, TypeVar


Node = TypeVar("Node")
Opaque = Dict[str, Any]
OnEntry = Callable[[Optional[Node], Node, Opaque], bool]


def bfs(graph: Any, opaque: Opaque, on_entry: OnEntry) -> Tuple[Opaque, Set[Node]]:
    """Breadth-first search over a RootedGraph-like interface.

    The `graph` must implement:
      - roots() -> Iterable[Node]
      - neighbors(node: Node) -> Iterable[Node]

    The callback `on_entry(parent, node, opaque)` is invoked exactly once
    per discovered node (the first time it is visited). If it returns True,
    the exploration stops early.

    Returns:
      (opaque, visited)
    """

    first = True
    visited: Set[Node] = set()
    queue: Deque[Node] = deque()

    while first or queue:
        if first:
            parent: Optional[Node] = None
            frontier = graph.roots()
            first = False
        else:
            parent = queue.popleft()
            frontier = graph.neighbors(parent)

        frontier_list = list(frontier)
        frontier_list.sort(key=repr)  # ordre stable inter-plateforme
        for node in frontier_list:
            if node in visited:
                continue

            done = on_entry(parent, node, opaque)
            visited.add(node)
            queue.append(node)

            if done:
                return opaque, visited

    return opaque, visited


class Graph:
    """Small directed graph helper (for BFS sanity checks)."""

    def __init__(self) -> None:
        self._adj: Dict[Any, list[Any]] = {}

    def add_node(self, node: Any) -> None:
        self._adj.setdefault(node, [])

    def add_edge(self, src: Any, dst: Any) -> None:
        self.add_node(src)
        self.add_node(dst)
        self._adj[src].append(dst)

    def neighbors(self, node: Any) -> Iterable[Any]:
        return sorted(self._adj.get(node, []), key=repr)

    def roots(self) -> list[Any]:
        """Return nodes with no incoming edges (deterministic order)."""
        all_nodes = set(self._adj.keys())
        all_neighbors = {n for nbrs in self._adj.values() for n in nbrs}
        return sorted(list(all_nodes - all_neighbors), key=repr)
