from __future__ import annotations

from copy import deepcopy
from typing import Iterable, List, Tuple

from language_semantics import Action, LanguageSemantics

Peg = Tuple[int, ...]
State = Tuple[Peg, Peg, Peg]


class HanoiLS(LanguageSemantics):
    """
    Sémantique Hanoi basée sur LanguageSemantics.

    - état = (peg0, peg1, peg2)
    - peg = tuple de disques (bas -> haut), top = peg[-1]
    - action = move i->j
    """

    def __init__(self, n: int) -> None:
        if n <= 0:
            raise ValueError("n doit être > 0")
        self.n = n

    def initials(self) -> List[State]:
        start: State = (tuple(range(self.n, 0, -1)), (), ())
        return [start]

    def actions(self, state: State) -> List[Action]:
        acts: List[Action] = []

        for i in range(3):
            if not state[i]:
                continue
            disk = state[i][-1]

            for j in range(3):
                if i == j:
                    continue
                if (not state[j]) or (state[j][-1] > disk):
                    acts.append(Action(name=f"m{i}->{j}", data=(i, j), weight=1))

        return acts

    def execute(self, state: State, action: Action) -> Iterable[State]:
        i, j = action.data

        # On passe en structure mutable, puis deepcopy (copie indépendante)
        pegs = deepcopy([list(p) for p in state])

        # Vérifications de sécurité (au cas où)
        if not pegs[i]:
            return []
        disk = pegs[i][-1]
        if pegs[j] and pegs[j][-1] < disk:
            return []

        # Appliquer l'action
        pegs[i].pop()
        pegs[j].append(disk)

        # Revenir à un état immuable (hashable pour visited dans BFS)
        nxt: State = tuple(tuple(p) for p in pegs)  # type: ignore
        return [nxt]

    def is_goal(self, state: State) -> bool:
        target = tuple(range(self.n, 0, -1))
        return state[0] == () and state[1] == () and state[2] == target
