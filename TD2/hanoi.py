from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from bfs import bfs
from rooted_graph import RootedGraph


Peg = Tuple[int, ...]
State = Tuple[Peg, Peg, Peg]


class HanoiGraph(RootedGraph):
    """Tower of Hanoi encoded as a RootedGraph.

    A state is a tuple of 3 pegs; each peg is a tuple of disk sizes.
    Disks are stored from bottom to top, so the top disk is peg[-1].
    """

    def __init__(self, n: int):
        if n <= 0:
            raise ValueError("n must be a positive integer")
        self.n = n

    def roots(self) -> List[State]:
        # Initial state: all disks on peg 0, pegs 1 and 2 empty.
        # Largest disk = n, smallest = 1.
        return [(tuple(range(self.n, 0, -1)), (), ())]

    def neighbors(self, state: State) -> List[State]:
        """All legal one-disk moves from `state`."""
        out: List[State] = []

        for i in range(3):
            if not state[i]:
                continue

            disk = state[i][-1]  # top disk of peg i

            for j in range(3):
                if i == j:
                    continue

                # Legal move: target peg is empty or has a larger top disk.
                if not state[j] or state[j][-1] > disk:
                    # Make a mutable copy
                    new_state = [list(p) for p in state]
                    new_state[i].pop()
                    new_state[j].append(disk)

                    # Convert back to tuples (hashable state)
                    out.append(tuple(tuple(p) for p in new_state))

        return out

    def is_solution(self, state: State) -> bool:
        return (
            state[0] == ()
            and state[1] == ()
            and state[2] == tuple(range(self.n, 0, -1))
        )


def solve_hanoi_bfs(n: int) -> List[State]:
    """Return a shortest solution path (list of states) for n disks."""
    graph = HanoiGraph(n)

    opaque: Dict[str, object] = {
        "graph": graph,
        "parent": {},
        "goal": None,
    }

    def on_entry(
        parent: Optional[State], state: State, opaque_dict: Dict[str, object]
    ) -> bool:
        parent_map = opaque_dict["parent"]
        assert isinstance(parent_map, dict)
        parent_map[state] = parent

        g = opaque_dict["graph"]
        assert isinstance(g, HanoiGraph)
        if g.is_solution(state):
            opaque_dict["goal"] = state
            return True
        return False

    bfs(graph, opaque, on_entry)

    goal = opaque["goal"]
    if goal is None:
        raise RuntimeError("No solution found (unexpected for Hanoi)")

    # Reconstruct path from goal to root using parent pointers
    parent_map = opaque["parent"]
    assert isinstance(parent_map, dict)

    path: List[State] = []
    s: Optional[State] = goal  # type: ignore[assignment]
    while s is not None:
        path.append(s)
        s = parent_map.get(s)

    return list(reversed(path))
