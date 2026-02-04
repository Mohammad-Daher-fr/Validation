from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Set, Tuple


@dataclass(frozen=True)
class Step:
    """Step seen by the property: after taking a system transition.
    We evaluate propositions on the target configuration.
    """

    src: Any
    action: str
    tgt: Any
    ap: Dict[str, bool]


@dataclass(frozen=True)
class PropAction:
    label: str
    target: int


class BuchiProperty:
    """iSoup-like property semantics for Buchi automate.

    - initial() -> list of initial states
    - actions(step, state) -> list of enabled PropAction
    - execute(action, step, state) -> next state (int)
    - accepting_states: set of accepting states
    """

    def __init__(
        self,
        name: str,
        initial_states: List[int],
        accepting_states: Set[int],
        transitions: Dict[int, List[Tuple[str, Callable[[Step], bool], int]]],
    ) -> None:
        self.name = name
        self._initial_states = list(initial_states)
        self.accepting_states = set(accepting_states)
        self._transitions = transitions

    def initial(self) -> List[int]:
        return list(self._initial_states)

    def is_accepting(self, st: int) -> bool:
        return st in self.accepting_states

    def actions(self, step: Step, st: int) -> List[PropAction]:
        out: List[PropAction] = []
        for lbl, guard, tgt in self._transitions.get(st, []):
            if guard(step):
                out.append(PropAction(lbl, tgt))
        # deterministic order for reproducibility
        out.sort(key=lambda a: (a.label, a.target))
        return out

    def execute(self, action: PropAction, step: Step, st: int) -> int:
        return action.target


# Atomic proposition helpers (read from step.ap)
def ap(step: Step, key: str) -> bool:
    return bool(step.ap.get(key, False))


# Buchi properties
def prop_P1_exclusion_violation() -> BuchiProperty:
    # cond := A.CS & B.CS
    # Accept if cond happens (reach bad state) and then stay there (true-loop).
    return BuchiProperty(
        name="P1",
        initial_states=[1],
        accepting_states={0},
        transitions={
            1: [
                ("cond", lambda s: ap(s, "cond"), 0),
                ("!cond", lambda s: not ap(s, "cond"), 1),
            ],
            0: [
                ("true", lambda s: True, 0),
            ],
        },
    )


def prop_P2_deadlock_violation() -> BuchiProperty:
    # Accept if deadlock becomes true.
    return BuchiProperty(
        name="P2",
        initial_states=[1],
        accepting_states={0},
        transitions={
            1: [
                ("deadlock", lambda s: ap(s, "deadlock"), 0),
                ("!deadlock", lambda s: not ap(s, "deadlock"), 1),
            ],
            0: [
                ("true", lambda s: True, 0),
            ],
        },
    )


def prop_P3_at_least_one_in_violation() -> BuchiProperty:
    # q := A.CS | B.CS
    # Violation of "GF q" is "FG !q"
    # Nondeterminism: from x on !q we can either stay in x or move to y (accepting),
    # and y loops on !q forever.
    X, Y = 0, 1
    return BuchiProperty(
        name="P3",
        initial_states=[X],
        accepting_states={Y},
        transitions={
            X: [
                ("q", lambda s: ap(s, "q"), X),
                ("!q", lambda s: not ap(s, "q"), X),
                ("!q", lambda s: not ap(s, "q"), Y),
            ],
            Y: [
                ("!q", lambda s: not ap(s, "q"), Y),
            ],
        },
    )


def prop_P4_if_wants_then_gets_in_violation() -> BuchiProperty:
    # p0 := flagA==UP ; q0 := A.CS
    # p1 := flagB==UP ; q1 := B.CS
    # Violation: F( p & G(!q) )
    S0, A_BAD, B_BAD = 0, 1, 2
    return BuchiProperty(
        name="P4",
        initial_states=[S0],
        accepting_states={A_BAD, B_BAD},
        transitions={
            S0: [
                ("true", lambda s: True, S0),
                ("p0&!q0", lambda s: ap(s, "p0") and (not ap(s, "q0")), A_BAD),
                ("p1&!q1", lambda s: ap(s, "p1") and (not ap(s, "q1")), B_BAD),
            ],
            A_BAD: [
                ("!q0", lambda s: not ap(s, "q0"), A_BAD),
            ],
            B_BAD: [
                ("!q1", lambda s: not ap(s, "q1"), B_BAD),
            ],
        },
    )


def prop_P5_uncontested_progress_violation() -> BuchiProperty:
    # Violation patterns (from the sheet):
    #  - (!aInCS & aWaiting & bNotInterested) and then always !aInCS
    #  - (aNotInterested & !bInCS & bWaiting) and then always !bInCS
    S0, A_BAD, B_BAD = 0, 1, 2
    return BuchiProperty(
        name="P5",
        initial_states=[S0],
        accepting_states={A_BAD, B_BAD},
        transitions={
            S0: [
                ("true", lambda s: True, S0),
                (
                    "!aCS&aW&bNI",
                    lambda s: (not ap(s, "aCS")) and ap(s, "aW") and ap(s, "bNI"),
                    A_BAD,
                ),
                (
                    "aNI&!bCS&bW",
                    lambda s: ap(s, "aNI") and (not ap(s, "bCS")) and ap(s, "bW"),
                    B_BAD,
                ),
            ],
            A_BAD: [
                ("!aCS", lambda s: not ap(s, "aCS"), A_BAD),
            ],
            B_BAD: [
                ("!bCS", lambda s: not ap(s, "bCS"), B_BAD),
            ],
        },
    )


PROPERTIES: Dict[str, Callable[[], BuchiProperty]] = {
    "P1": prop_P1_exclusion_violation,
    "P2": prop_P2_deadlock_violation,
    "P3": prop_P3_at_least_one_in_violation,
    "P4": prop_P4_if_wants_then_gets_in_violation,
    "P5": prop_P5_uncontested_progress_violation,
}
