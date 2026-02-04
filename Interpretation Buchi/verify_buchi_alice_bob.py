from __future__ import annotations
import argparse
import importlib
from collections import deque
from dataclasses import dataclass
from typing import Any, Callable, Deque, Dict, Iterable, List, Optional, Set, Tuple
from isoup_buchi_alice_bob import PROPERTIES, BuchiProperty, PropAction, Step
from soup_lang import SoupSemantics

CANDIDATE_MODEL_MODULES = ["alice_bob_soup_models"]


def load_system(model_name: str) -> Any:
    """
    Charge un modèle ABk depuis alice_bob_soup_models.get_model()
    puis l'enveloppe dans SoupSemantics pour avoir initials/actions/execute.
    """
    m = importlib.import_module("alice_bob_soup_models")
    soup = m.get_model(model_name)  # retourne un Soup
    return SoupSemantics(soup)  # retourne la sémantique exécutable


def sys_initials(sys: Any) -> List[Any]:
    if hasattr(sys, "initials"):
        return list(sys.initials())
    if hasattr(sys, "initial"):
        return list(sys.initial())
    if hasattr(sys, "roots"):
        return list(sys.roots())
    raise RuntimeError(
        "Système: impossible de trouver une méthode initials()/initial()/roots()."
    )


def sys_actions(sys: Any, cfg: Any) -> List[Any]:
    if hasattr(sys, "actions"):
        return list(sys.actions(cfg))
    raise RuntimeError("Système: impossible de trouver une méthode actions(cfg).")


def sys_execute(sys: Any, cfg: Any, act: Any) -> List[Any]:
    if hasattr(sys, "execute"):
        # try execute(cfg, act)
        try:
            r = sys.execute(cfg, act)
            return list(r) if isinstance(r, Iterable) else [r]
        except TypeError:
            # try execute(act, cfg)
            r = sys.execute(act, cfg)
            return list(r) if isinstance(r, Iterable) else [r]
    if hasattr(sys, "neighbors"):
        # graph style
        return list(sys.neighbors(cfg))
    raise RuntimeError(
        "Système: impossible de trouver execute(cfg, act) ou neighbors(cfg)."
    )


def act_name(act: Any) -> str:
    if isinstance(act, str):
        return act
    if hasattr(act, "name"):
        return str(getattr(act, "name"))
    return repr(act)


# Atomic propositions on configurations
def tup_get(cfg: Any, i: int, default: Any) -> Any:
    try:
        return cfg[i]
    except Exception:
        return default


def compute_ap(sys: Any, cfg: Any) -> Dict[str, bool]:
    a_loc = tup_get(cfg, 0, None)
    b_loc = tup_get(cfg, 1, None)
    flagA = tup_get(cfg, 2, "DOWN")
    flagB = tup_get(cfg, 3, "DOWN")

    aCS = a_loc == "CS"
    bCS = b_loc == "CS"
    q = aCS or bCS

    acts = sys_actions(sys, cfg)
    deadlock = len(acts) == 0

    p0 = flagA == "UP"
    q0 = aCS
    p1 = flagB == "UP"
    q1 = bCS

    aW = a_loc == "W"
    bW = b_loc == "W"

    aNI = flagA == "DOWN"
    bNI = flagB == "DOWN"

    return {
        "aCS": aCS,
        "bCS": bCS,
        "cond": aCS and bCS,
        "q": q,
        "deadlock": deadlock,
        "p0": p0,
        "q0": q0,
        "p1": p1,
        "q1": q1,
        "aW": aW,
        "bW": bW,
        "aNI": aNI,
        "bNI": bNI,
    }


# Buchi product exploration + accepting cycle search
Node = Tuple[Any, int]  # (system_cfg, prop_state)


@dataclass(frozen=True)
class Edge:
    sys_action: str
    prop_label: str


def build_reachable_product(sys: Any, prop: BuchiProperty) -> Tuple[
    Set[Node],
    Dict[Node, List[Tuple[Node, Edge]]],
    Dict[Node, Tuple[Optional[Node], Edge]],
]:
    visited: Set[Node] = set()
    adj: Dict[Node, List[Tuple[Node, Edge]]] = {}
    parent: Dict[Node, Tuple[Optional[Node], Edge]] = {}

    q: Deque[Node] = deque()

    for s0 in sys_initials(sys):
        init_step = Step(src=s0, action="init", tgt=s0, ap=compute_ap(sys, s0))
        for p0 in prop.initial():
            pacts = prop.actions(init_step, p0)
            # safety: if property has no enabled transition, keep p0
            if not pacts:
                n0 = (s0, p0)
                if n0 not in visited:
                    visited.add(n0)
                    parent[n0] = (None, Edge("init", "epsilon"))
                    q.append(n0)
                continue

            for pa in pacts:
                p1 = prop.execute(pa, init_step, p0)
                n0 = (s0, p1)
                if n0 not in visited:
                    visited.add(n0)
                    parent[n0] = (None, Edge("init", pa.label))
                    q.append(n0)

    while q:
        node = q.popleft()
        s, pst = node

        outs: List[Tuple[Node, Edge]] = []
        acts = sys_actions(sys, s)
        acts_sorted = sorted(acts, key=act_name)

        if not acts_sorted:
            # stuttering to make infinite behavior possible from deadlocks
            acts_sorted = ["stutter"]

        for a in acts_sorted:
            a_name = act_name(a)
            if a_name == "stutter":
                targets = [s]
            else:
                targets = sys_execute(sys, s, a)
                # deterministic order
                targets = sorted(targets, key=lambda x: repr(x))

            for t in targets:
                step = Step(src=s, action=a_name, tgt=t, ap=compute_ap(sys, t))
                pacts = prop.actions(step, pst)
                for pa in pacts:
                    pst2 = prop.execute(pa, step, pst)
                    succ: Node = (t, pst2)
                    e = Edge(a_name, pa.label)
                    outs.append((succ, e))

                    if succ not in visited:
                        visited.add(succ)
                        parent[succ] = (node, e)
                        q.append(succ)

        adj[node] = outs

    # ensure nodes with no outgoing appear in adj
    for n in list(visited):
        adj.setdefault(n, [])

    return visited, adj, parent


def tarjan_scc(
    nodes: List[Node], adj: Dict[Node, List[Tuple[Node, Edge]]]
) -> List[List[Node]]:
    index = 0
    stack: List[Node] = []
    onstack: Set[Node] = set()
    idx: Dict[Node, int] = {}
    low: Dict[Node, int] = {}
    sccs: List[List[Node]] = []

    import sys as _sys

    _sys.setrecursionlimit(10000)

    def strongconnect(v: Node) -> None:
        nonlocal index
        idx[v] = index
        low[v] = index
        index += 1
        stack.append(v)
        onstack.add(v)

        for w, _ in adj.get(v, []):
            if w not in idx:
                strongconnect(w)
                low[v] = min(low[v], low[w])
            elif w in onstack:
                low[v] = min(low[v], idx[w])

        if low[v] == idx[v]:
            comp: List[Node] = []
            while True:
                w = stack.pop()
                onstack.remove(w)
                comp.append(w)
                if w == v:
                    break
            sccs.append(comp)

    for v in nodes:
        if v not in idx:
            strongconnect(v)

    return sccs


def scc_has_cycle(comp: List[Node], adj: Dict[Node, List[Tuple[Node, Edge]]]) -> bool:
    if len(comp) > 1:
        return True
    n = comp[0]
    for m, _ in adj.get(n, []):
        if m == n:
            return True
    return False


def find_accepting_cycle(
    prop: BuchiProperty,
    adj: Dict[Node, List[Tuple[Node, Edge]]],
    visited: Set[Node],
) -> Optional[Node]:
    nodes = list(visited)
    sccs = tarjan_scc(nodes, adj)

    # deterministic order: pick smallest SCC representative by repr
    def scc_key(c: List[Node]) -> str:
        return min(repr(x) for x in c)

    for comp in sorted(sccs, key=scc_key):
        if not scc_has_cycle(comp, adj):
            continue
        if any(prop.is_accepting(n[1]) for n in comp):
            # choose a deterministic accepting node in the SCC
            acc = sorted(
                [n for n in comp if prop.is_accepting(n[1])], key=lambda x: repr(x)
            )[0]
            return acc
    return None


def reconstruct_prefix(
    goal: Node, parent: Dict[Node, Tuple[Optional[Node], Edge]]
) -> Tuple[List[Any], List[Edge]]:
    """
    Retourne un prefix-trace bien formé:
      sys_states[i] --edge[i]--> sys_states[i+1]
    donc len(sys_states) = len(edges)+1.

    On traite l'arête initiale (prev=None) comme:
      s0 --init||...--> s0
    """
    nodes: List[Node] = []
    edges_between: List[Edge] = []
    root_edge: Optional[Edge] = None

    cur: Optional[Node] = goal
    while cur is not None:
        nodes.append(cur)
        p = parent.get(cur)
        if p is None:
            break
        prev, e = p
        if prev is None:
            root_edge = e
            break
        edges_between.append(e)
        cur = prev

    nodes.reverse()
    edges_between.reverse()

    sys_nodes = [n[0] for n in nodes]  # états système le long du chemin

    if not sys_nodes:
        return [], []

    # Si on a une arête root (init), on la transforme en stutter sur s0
    if root_edge is not None:
        sys_states = [sys_nodes[0], sys_nodes[0]] + sys_nodes[1:]
        edges = [root_edge] + edges_between
    else:
        sys_states = sys_nodes
        edges = edges_between

    return sys_states, edges


def find_cycle_from(
    start: Node,
    scc_set: Set[Node],
    adj: Dict[Node, List[Tuple[Node, Edge]]],
) -> Tuple[List[Any], List[Edge]]:
    # self-loop?
    for m, e in adj.get(start, []):
        if m == start:
            return [start[0], start[0]], [e]

    # DFS to come back to start
    stack: List[Node] = [start]
    seen: Set[Node] = {start}
    pred: Dict[Node, Tuple[Node, Edge]] = {}

    while stack:
        v = stack.pop()
        for w, e in adj.get(v, []):
            if w not in scc_set:
                continue
            if w == start:
                # reconstruct v -> ... -> start
                path_nodes: List[Node] = [start]
                path_edges: List[Edge] = []
                # unwind from v back to start
                cur = v
                path_nodes.append(cur)
                path_edges.append(e)  # edge cur -> start
                while cur != start:
                    pr = pred[cur]
                    cur2, e2 = pr
                    path_nodes.append(cur2)
                    path_edges.append(e2)
                    cur = cur2
                path_nodes.reverse()
                path_edges.reverse()
                sys_cycle = [n[0] for n in path_nodes]
                return sys_cycle, path_edges

            if w not in seen:
                seen.add(w)
                pred[w] = (v, e)
                stack.append(w)

    # Should not happen if SCC has a cycle, but keep safe fallback
    return [start[0], start[0]], [Edge("stutter", "true")]


def verify_buchi(
    sys: Any, prop: BuchiProperty
) -> Tuple[bool, int, Optional[Tuple[List[Any], List[Edge], List[Any], List[Edge]]]]:
    visited, adj, parent = build_reachable_product(sys, prop)
    acc_node = find_accepting_cycle(prop, adj, visited)

    if acc_node is None:
        return True, len(visited), None

    # prefix to accepting node
    prefix_sys, prefix_edges = reconstruct_prefix(acc_node, parent)

    # cycle inside SCC
    # rebuild SCC set containing acc_node
    nodes = list(visited)
    sccs = tarjan_scc(nodes, adj)
    scc_set: Set[Node] = set()
    for comp in sccs:
        if acc_node in comp:
            scc_set = set(comp)
            break

    cycle_sys, cycle_edges = find_cycle_from(acc_node, scc_set, adj)
    return False, len(visited), (prefix_sys, prefix_edges, cycle_sys, cycle_edges)


def print_trace(sys_states: List[Any], edges: List[Edge]) -> None:
    """
    Affiche: state --label--> next_state
    sys_states doit avoir len = len(edges)+1.
    """
    if not sys_states:
        print("(empty)")
        return

    # Cas normal
    for i, e in enumerate(edges):
        if i + 1 < len(sys_states):
            print(
                f"{sys_states[i]} --{e.sys_action}||{e.prop_label}--> {sys_states[i+1]}"
            )
        else:
            # fallback si jamais une trace est mal formée
            print(f"{sys_states[i]} --{e.sys_action}||{e.prop_label}--> ?")

    # Si aucune edge, afficher l'état seul
    if not edges:
        print(f"{sys_states[0]}")


def main() -> None:
    ap_ = argparse.ArgumentParser()
    ap_.add_argument(
        "--model", required=True, choices=["AB1", "AB2", "AB3", "AB4", "AB5"]
    )
    ap_.add_argument("--prop", required=True, choices=["P1", "P2", "P3", "P4", "P5"])
    args = ap_.parse_args()

    sys = load_system(args.model)
    prop = PROPERTIES[args.prop]()

    ok, visited_count, cex = verify_buchi(sys, prop)

    print(f"Model={args.model} | Prop={args.prop} | visited={visited_count}")
    if ok:
        print("RESULT: SAT (pas de cycle acceptant)")
        return

    print("RESULT: VIOLÉ (cycle acceptant trouvé)")
    assert cex is not None
    prefix_sys, prefix_edges, cycle_sys, cycle_edges = cex

    print("\nPrefix-trace (projection système):")
    print_trace(prefix_sys, prefix_edges)

    print("\nCyclic-suffix-trace (projection système):")
    print_trace(cycle_sys, cycle_edges)


if __name__ == "__main__":
    main()
