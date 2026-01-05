from __future__ import annotations

from typing import Any, Dict, Optional

from bfs import Graph, bfs
from hanoi import solve_hanoi_bfs


def bfs_sanity_demo() -> None:
    """Small BFS demo on a toy graph (A -> {B, C}, B -> D)."""

    g = Graph()
    g.add_edge("A", "B")
    g.add_edge("A", "C")
    g.add_edge("B", "D")

    opaque: Dict[str, Any] = {"visited_count": 0, "parent": {}, "goal": None}

    def on_entry(parent: Optional[str], node: str, opaque: Dict[str, Any]) -> bool:
        opaque["visited_count"] += 1
        opaque["parent"][node] = parent
        if node == "D":
            opaque["goal"] = node
            return True
        return False

    bfs(g, opaque, on_entry)

    # Reconstruct path to D (if found)
    path = []
    s = opaque["goal"]
    while s is not None:
        path.append(s)
        s = opaque["parent"].get(s)
    path.reverse()

    print("BFS sanity check")
    print("  Visited count:", opaque["visited_count"])
    print("  Goal path:", path)


def hanoi_demo(n: int = 3) -> None:
    """Shortest Tower of Hanoi solution using BFS."""

    path = solve_hanoi_bfs(n)
    print("\nTower of Hanoi")
    print(f"  n={n}, number of moves={len(path) - 1}")
    for i, state in enumerate(path):
        print(f"  Step {i}: {state}")



if __name__ == "__main__":
    bfs_sanity_demo()
    hanoi_demo(3)
