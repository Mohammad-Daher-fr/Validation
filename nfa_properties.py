from __future__ import annotations
from typing import Any, Callable, Tuple
from isoup_lang import iPiece, iSoup

PropState = str  # "T" ou "F"
Step = Tuple[Any, Any, Any]  # (lc, la, lt)


def build_never_cond_pattern1(cond: Callable[[Step], bool]) -> iSoup:
    """
    Patron 1:
      T --true -> T
      T --cond -> F (acceptant)
    """
    T, F = "T", "F"
    pieces = [
        iPiece(
            name="cond",
            guard=lambda step, ps: ps == T and cond(step),
            effect=lambda step, ps: F,
        ),
        iPiece(
            name="true",
            guard=lambda step, ps: ps == T,
            effect=lambda step, ps: T,
        ),
    ]
    return iSoup(pieces=pieces, init=[T], accepting={F})


def build_never_cond_pattern2(cond: Callable[[Step], bool]) -> iSoup:
    """
    Patron 2:
      T --!cond -> T
      T --cond  -> F (acceptant)
    """
    T, F = "T", "F"
    pieces = [
        iPiece(
            name="cond",
            guard=lambda step, ps: ps == T and cond(step),
            effect=lambda step, ps: F,
        ),
        iPiece(
            name="!cond",
            guard=lambda step, ps: ps == T and (not cond(step)),
            effect=lambda step, ps: T,
        ),
    ]
    return iSoup(pieces=pieces, init=[T], accepting={F})


# Conditions P1 / P2
def cond_exclusion(step: Step) -> bool:
    # On choisit de tester sur la config cible lt (entrée dans l'état dangereux)
    _, _, lt = step
    return lt[0] == "CS" and lt[1] == "CS"


def make_cond_deadlock() -> Callable[[Step], bool]:
    """
    En mode StepSynchronousProduct, quand le système n'a AUCUNE action,
    le produit génère un step de stuttering avec action.name == "stutter".
    Donc deadlock(step) <=> step.action.name == "stutter"
    """

    def deadlock(step: Step) -> bool:
        _, la, _ = step
        name = getattr(la, "name", str(la))
        return name == "stutter"

    return deadlock
