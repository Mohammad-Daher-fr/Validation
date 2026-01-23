from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, List, Tuple

from language_semantics import Action, LanguageSemantics
from isoup_lang import iPiece, iSoupSemantics


@dataclass(frozen=True)
class ConfigProdActionData:
    lhs_target: Any
    rhs_action: iPiece
    lhs_label: str  # "init" | nom action | "stutter"


# état produit = (lhs_state, rhs_state)
# lhs_state peut être None dans l'état initial spécial (voir initial()).
ProdState = Tuple[Any, Any]


class ConfigurationSynchronousProduct(LanguageSemantics):
    def __init__(self, lhs: LanguageSemantics, rhs: iSoupSemantics):
        self.lhs = lhs
        self.rhs = rhs

    def initials(self) -> List[ProdState]:
        # état initial spécial: (None, rhs_init)
        return [(None, rc) for rc in self.rhs.initial()]

    def actions(self, source: ProdState) -> List[Action]:
        synchronous: List[Action] = []
        lhs_source, rhs_source = source

        # Cas initial: on "lit" une configuration initiale du système
        if lhs_source is None:
            for lhs_init in self.lhs.initials():
                rhs_actions = self.rhs.actions(lhs_init, rhs_source)
                for ra in rhs_actions:
                    synchronous.append(
                        Action(
                            name=f"init||{ra.name}",
                            data=ConfigProdActionData(
                                lhs_target=lhs_init, rhs_action=ra, lhs_label="init"
                            ),
                            weight=1,
                        )
                    )
            return synchronous

        # Cas général: on avance le système puis on fait avancer la propriété
        lhs_actions = self.lhs.actions(lhs_source)
        number_of_actions = len(lhs_actions)

        for la in lhs_actions:
            lhs_targets = list(self.lhs.execute(lhs_source, la))
            if not lhs_targets:
                number_of_actions -= 1
                continue

            for lt in lhs_targets:
                rhs_actions = self.rhs.actions(lt, rhs_source)
                for ra in rhs_actions:
                    synchronous.append(
                        Action(
                            name=f"{la.name}||{ra.name}",
                            data=ConfigProdActionData(
                                lhs_target=lt, rhs_action=ra, lhs_label=la.name
                            ),
                            weight=1,
                        )
                    )

        # Deadlock (aucune action système) => stutter (reste sur place)
        if number_of_actions == 0:
            rhs_actions = self.rhs.actions(lhs_source, rhs_source)
            for ra in rhs_actions:
                synchronous.append(
                    Action(
                        name=f"stutter||{ra.name}",
                        data=ConfigProdActionData(
                            lhs_target=lhs_source, rhs_action=ra, lhs_label="stutter"
                        ),
                        weight=1,
                    )
                )

        return synchronous

    def execute(self, state: ProdState, action: Action) -> Iterable[ProdState]:
        lhs_source, rhs_source = state
        if not isinstance(action.data, ConfigProdActionData):
            raise TypeError("Action.data doit être ConfigProdActionData")

        lhs_target = action.data.lhs_target
        rhs_act = action.data.rhs_action

        rhs_targets = list(self.rhs.execute(rhs_act, lhs_target, rhs_source))
        return [(lhs_target, rt) for rt in rhs_targets]
