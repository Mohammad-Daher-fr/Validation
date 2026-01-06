from __future__ import annotations

from typing import Dict, Iterable, List, Tuple

from rooted_graph import RootedGraph


# Locations
I = "I"
W = "W"
CS = "CS"

# Flags
UP = "UP"
DOWN = "DOWN"


class LabeledRootedGraph(RootedGraph):
    """RootedGraph with edge labels (used to reconstruct traces).

    We store labels in a dictionary (src, dst) -> label.
    """

    def __init__(self) -> None:
        self._edge_label: Dict[tuple, str] = {}

    def label(self, src, dst) -> str:
        return self._edge_label.get((src, dst), "?")

    def _set_label(self, src, dst, label: str) -> None:
        self._edge_label[(src, dst)] = label


# AB1
# Alice: I --a1--> CS ; CS --a2--> I
# Bob  : I --b1--> CS ; CS --b2--> I
# Global state = (aLoc, bLoc)

StateAB1 = Tuple[str, str]


class AB1Graph(LabeledRootedGraph):
    def __init__(self) -> None:
        super().__init__()

    def roots(self) -> List[StateAB1]:
        return [(I, I)]

    def neighbors(self, state: StateAB1) -> List[StateAB1]:
        a, b = state
        out: List[StateAB1] = []

        # Alice moves
        if a == I:
            ns = (CS, b)
            out.append(ns)
            self._set_label(state, ns, "a1")
        elif a == CS:
            ns = (I, b)
            out.append(ns)
            self._set_label(state, ns, "a2")

        # Bob moves
        if b == I:
            ns = (a, CS)
            out.append(ns)
            self._set_label(state, ns, "b1")
        elif b == CS:
            ns = (a, I)
            out.append(ns)
            self._set_label(state, ns, "b2")

        return out


# AB2
# Alice:
#   I  --a1 / flagA=UP-->    W
#   W  --a2 [flagB==DOWN]--> CS
#   CS --a3 / flagA=DOWN-->  I
#
# Bob:
#   I  --b1 / flagB=UP-->    W
#   W  --b2 [flagA==DOWN]--> CS
#   CS --b3 / flagB=DOWN-->  I
#
# Global state = (aLoc, bLoc, flagA, flagB)


StateAB2 = Tuple[str, str, str, str]


class AB2Graph(LabeledRootedGraph):
    def __init__(self) -> None:
        super().__init__()

    def roots(self) -> List[StateAB2]:
        return [(I, I, DOWN, DOWN)]

    def neighbors(self, state: StateAB2) -> List[StateAB2]:
        a, b, flagA, flagB = state
        out: List[StateAB2] = []

        # Alice
        if a == I:
            ns = (W, b, UP, flagB)  # a1: raise Alice flag
            out.append(ns)
            self._set_label(state, ns, "a1")
        elif a == W:
            if flagB == DOWN:  # a2 guard
                ns = (CS, b, flagA, flagB)
                out.append(ns)
                self._set_label(state, ns, "a2")
        elif a == CS:
            ns = (I, b, DOWN, flagB)  # a3: lower Alice flag
            out.append(ns)
            self._set_label(state, ns, "a3")

        # Bob
        if b == I:
            ns = (a, W, flagA, UP)  # b1: raise Bob flag
            out.append(ns)
            self._set_label(state, ns, "b1")
        elif b == W:
            if flagA == DOWN:  # b2 guard
                ns = (a, CS, flagA, flagB)
                out.append(ns)
                self._set_label(state, ns, "b2")
        elif b == CS:
            ns = (a, I, flagA, DOWN)  # b3: lower Bob flag
            out.append(ns)
            self._set_label(state, ns, "b3")

        return out


# AB3 (Figure 10)
# Same as AB2, plus Bob has an extra transition b4:
#   b4: from W -> I if flagA == UP, and sets flagB = DOWN


StateAB3 = StateAB2


class AB3Graph(LabeledRootedGraph):
    def __init__(self) -> None:
        super().__init__()

    def roots(self) -> List[StateAB3]:
        return [(I, I, DOWN, DOWN)]

    def neighbors(self, state: StateAB3) -> List[StateAB3]:
        a, b, flagA, flagB = state
        out: List[StateAB3] = []

        # Alice (same as AB2)
        if a == I:
            ns = (W, b, UP, flagB)  # a1
            out.append(ns)
            self._set_label(state, ns, "a1")
        elif a == W:
            if flagB == DOWN:  # a2 guard
                ns = (CS, b, flagA, flagB)
                out.append(ns)
                self._set_label(state, ns, "a2")
        elif a == CS:
            ns = (I, b, DOWN, flagB)  # a3
            out.append(ns)
            self._set_label(state, ns, "a3")

        # Bob (AB2 + b4)
        if b == I:
            ns = (a, W, flagA, UP)  # b1
            out.append(ns)
            self._set_label(state, ns, "b1")

        elif b == W:
            # b2: enter CS if Alice flag is DOWN
            if flagA == DOWN:
                ns = (a, CS, flagA, flagB)
                out.append(ns)
                self._set_label(state, ns, "b2")

            # b4: if Alice flag is UP, Bob backs off to I and lowers his flag
            if flagA == UP:
                ns = (a, I, flagA, DOWN)
                out.append(ns)
                self._set_label(state, ns, "b4")

        elif b == CS:
            ns = (a, I, flagA, DOWN)  # b3
            out.append(ns)
            self._set_label(state, ns, "b3")

        return out
