from __future__ import annotations
from typing import Any, Callable, Set
from isoup_lang import iPiece, iSoup


PropState = str  # "T" ou "F"


def build_never_cond_pattern1(cond: Callable[[Any], bool]) -> iSoup:
    """
    Patron 1:
      T --true -> T
      T --cond -> F (acceptant)
    """
    T, F = "T", "F"
    pieces = [
        # Transition vers F d'abord => contre-exemple plus "court" (déterministe avec BFS)
        iPiece(
            name="cond",
            guard=lambda c, ps: ps == T and cond(c),
            effect=lambda c, ps: F,
        ),
        iPiece(
            name="true",
            guard=lambda c, ps: ps == T,
            effect=lambda c, ps: T,
        ),
    ]
    return iSoup(pieces=pieces, init=[T], accepting={F})


def build_never_cond_pattern2(cond: Callable[[Any], bool]) -> iSoup:
    """
    Patron 2:
      T --!cond -> T
      T --cond ->  F (acceptant)
    """
    T, F = "T", "F"
    pieces = [
        iPiece(
            name="cond",
            guard=lambda c, ps: ps == T and cond(c),
            effect=lambda c, ps: F,
        ),
        iPiece(
            name="!cond",
            guard=lambda c, ps: ps == T and (not cond(c)),
            effect=lambda c, ps: T,
        ),
    ]
    return iSoup(pieces=pieces, init=[T], accepting={F})


# Conditions P1 / P2
def cond_exclusion(sys_cfg: Any) -> bool:
    # sys_cfg = (a_loc, b_loc, flagA, flagB, turn) d'après l'étape 1
    return sys_cfg[0] == "CS" and sys_cfg[1] == "CS"


def make_cond_deadlock(sys_semantics) -> Callable[[Any], bool]:
    # deadlock(c) : aucune action possible depuis c
    return lambda sys_cfg: len(sys_semantics.actions(sys_cfg)) == 0
