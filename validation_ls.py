from __future__ import annotations
from typing import Dict, Optional, Tuple, List

from bfs import bfs
from ls2rg import LS2RG
from hanoi_ls import HanoiLS, State


def solve_hanoi_ls(n: int) -> List[State]:
    ls = HanoiLS(n)
    rg = LS2RG(ls, keep_labels=True)

    opaque: Dict[str, object] = {
        "parent": {},
        "goal": None,
    }

    def on_entry(
        parent: Optional[State], node: State, opaque_dict: Dict[str, object]
    ) -> bool:
        parent_map = opaque_dict["parent"]
        assert isinstance(parent_map, dict)
        parent_map[node] = parent

        if ls.is_goal(node):
            opaque_dict["goal"] = node
            return True
        return False

    bfs(rg, opaque, on_entry)

    goal = opaque["goal"]
    if goal is None:
        return []

    parent_map = opaque["parent"]
    assert isinstance(parent_map, dict)

    # reconstruction chemin
    path: List[State] = []
    cur: Optional[State] = goal  # type: ignore[assignment]
    while cur is not None:
        path.append(cur)
        cur = parent_map.get(cur)
    path.reverse()
    return path


if __name__ == "__main__":
    n = 3
    path = solve_hanoi_ls(n)
    print(f"Hanoi (LS) n={n} | moves={max(0, len(path)-1)} | states={len(path)}")
    for k, s in enumerate(path):
        print(f"step {k}: {s}")
