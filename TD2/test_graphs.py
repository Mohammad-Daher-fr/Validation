from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple

from bfs import bfs
from alice_bob import AB1Graph, AB2Graph, AB3Graph, CS


def explore_all_states(graph) -> Set[Any]:
    """Return the set of all states reachable from graph.roots()."""

    opaque: Dict[str, Any] = {}

    def on_entry(parent, state, opaque) -> bool:
        return False

    _, visited = bfs(graph, opaque, on_entry)
    return visited


def reconstruct_path(goal, parent: Dict[Any, Any]) -> List[Any]:
    path: List[Any] = []
    s = goal
    while s is not None:
        path.append(s)
        s = parent.get(s)
    return list(reversed(path))


def reconstruct_actions(path: Sequence[Any], graph) -> List[str]:
    actions: List[str] = []
    for i in range(len(path) - 1):
        actions.append(graph.label(path[i], path[i + 1]))
    return actions


def check_exclusion(graph):
    """Mutual exclusion property: not (Alice in CS and Bob in CS)."""

    opaque = {"bad": None, "parent": {}}

    def on_entry(parent, state, opaque) -> bool:
        opaque["parent"][state] = parent
        # Locations are always the first two components in AB1/2/3 states
        if state[0] == CS and state[1] == CS:
            opaque["bad"] = state
            return True
        return False

    bfs(graph, opaque, on_entry)

    if opaque["bad"] is None:
        return True, None, None

    path = reconstruct_path(opaque["bad"], opaque["parent"])
    actions = reconstruct_actions(path, graph)
    return False, opaque["bad"], (path, actions)


def check_deadlock(graph):
    """Deadlock property: no reachable state has 0 outgoing transitions."""

    opaque = {"dead": None, "parent": {}}

    def on_entry(parent, state, opaque) -> bool:
        opaque["parent"][state] = parent
        if len(list(graph.neighbors(state))) == 0:
            opaque["dead"] = state
            return True
        return False

    bfs(graph, opaque, on_entry)

    if opaque["dead"] is None:
        return True, None, None

    path = reconstruct_path(opaque["dead"], opaque["parent"])
    actions = reconstruct_actions(path, graph)
    return False, opaque["dead"], (path, actions)


def mark(ok: bool) -> str:
    return "OK" if ok else "X"


def print_trace(path: Sequence[Any], actions: Sequence[str]) -> None:
    for i, state in enumerate(path):
        if i < len(actions):
            print(f"  {state} --{actions[i]}-->")
        else:
            print(f"  {state}")


def run(name: str, graph) -> None:
    print("\n" + "=" * 60)
    print(f"Testing {name}")

    states = explore_all_states(graph)
    print(f"Reachable states: {len(states)}")

    excl_ok, excl_state, excl_trace = check_exclusion(graph)
    dead_ok, dead_state, dead_trace = check_deadlock(graph)

    print(f"Exclusion: {mark(excl_ok)}")
    if not excl_ok:
        print(f"  Counterexample state: {excl_state}")
        print("  Trace to exclusion:")
        print_trace(*excl_trace)

    print(f"Deadlock : {mark(dead_ok)}")
    if not dead_ok:
        print(f"  Deadlock state: {dead_state}")
        print("  Trace to deadlock:")
        print_trace(*dead_trace)


if __name__ == "__main__":
    run("AB1", AB1Graph())
    run("AB2", AB2Graph())
    run("AB3", AB3Graph())
