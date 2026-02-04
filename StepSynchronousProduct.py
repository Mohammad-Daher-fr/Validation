from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Iterable, List, Tuple


def _sorted_by_repr(xs: Iterable[Any]) -> List[Any]:
    return sorted(list(xs), key=repr)


def _name(x: Any) -> str:
    return getattr(x, "name", repr(x))


class StutteringAction:
    name = "stutter"

    def __repr__(self) -> str:
        return "stutter"


STUTTER = StutteringAction()

Step = Tuple[Any, Any, Any]  # (lc, la, lt)


@dataclass(frozen=True)
class ProductAction:
    step: Step
    rhs_action: Any
    name: str  # ex: "a1||cond", "stutter||!cond"


class StepSynchronousProduct:
    """
    Produit synchrone basé sur les STEPS:
      - état produit : (lc, rc)
      - action produit: ProductAction(step=(lc, la, lt), rhs_action=ra)
    Interface attendue par LS2RG:
      - initials()
      - actions(c)
      - execute(c, a)
    """

    def __init__(self, lhs: Any, rhs: Any) -> None:
        self.lhs = lhs
        self.rhs = rhs

    def initials(self) -> List[Any]:
        l0 = _sorted_by_repr(self.lhs.initials())
        r0 = _sorted_by_repr(self.rhs.initials())
        return [(lc, rc) for lc in l0 for rc in r0]

    def actions(self, c: Any) -> List[ProductAction]:
        lc, rc = c
        out: List[ProductAction] = []

        lactions = sorted(list(self.lhs.actions(lc)), key=_name)

        # Si deadlock côté système -> stutter
        if not lactions:
            step: Step = (lc, STUTTER, lc)
            ractions = sorted(list(self.rhs.actions(step, rc)), key=_name)
            for ra in ractions:
                out.append(
                    ProductAction(
                        step=step, rhs_action=ra, name=f"{_name(STUTTER)}||{_name(ra)}"
                    )
                )
            return out

        # Sinon: pour chaque transition système lc --la--> lt
        for la in lactions:
            # execute(state, action)
            ltargets = _sorted_by_repr(self.lhs.execute(lc, la))
            for lt in ltargets:
                step: Step = (lc, la, lt)
                ractions = sorted(list(self.rhs.actions(step, rc)), key=_name)
                for ra in ractions:
                    out.append(
                        ProductAction(
                            step=step, rhs_action=ra, name=f"{_name(la)}||{_name(ra)}"
                        )
                    )
        return out

    def execute(self, c: Any, a: ProductAction) -> List[Any]:
        # execute(state, action)
        _, rc = c
        step = a.step
        lt = step[2]

        rtargets = _sorted_by_repr(self.rhs.execute(a.rhs_action, step, rc))
        return [(lt, rt) for rt in rtargets]
