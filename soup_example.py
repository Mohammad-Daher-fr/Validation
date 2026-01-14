# soup_example.py
from __future__ import annotations

from bfs import bfs
from ls2rg import LS2RG
from soup_lang import Piece, Soup, SoupSemantics

# Exemple 1 : Horloge binaire
to1 = Piece("to1", lambda c: 1, lambda c: c == 0)
to0 = Piece("to0", lambda c: 0, lambda c: c == 1)

clk = Soup([to1, to0], init=[0])
clk_sem = SoupSemantics(clk)

print("Exemple 1 : Horloge binaire")
print("Initials:", clk_sem.initials())
print(
    "From 0 -> actions:",
    clk_sem.actions(0),
    "next:",
    list(clk_sem.execute(0, clk_sem.actions(0)[0])),
)
print(
    "From 1 -> actions:",
    clk_sem.actions(1),
    "next:",
    list(clk_sem.execute(1, clk_sem.actions(1)[0])),
)


# Exemple 2 : Compteur 0 -> 1 -> 2 -> 0
inc0 = Piece("inc0", lambda c: 1, lambda c: c == 0)
inc1 = Piece("inc1", lambda c: 2, lambda c: c == 1)
reset = Piece("reset", lambda c: 0, lambda c: c == 2)

counter = Soup([inc0, inc1, reset], init=[0])
counter_sem = SoupSemantics(counter)

print("\nExemple 2 : Compteur cyclique")
x = 0
for i in range(6):
    acts = counter_sem.actions(x)
    print(f"step {i} | state={x} | actions={[a.name for a in acts]}")
    if acts:
        x = list(counter_sem.execute(x, acts[0]))[0]


# Exemple 3 : BFS sur le compteur (trouver 2)
print("\nExemple 3 : BFS sur le compteur (objectif = 2)")
graph = LS2RG(counter_sem)

opaque = {"parent": {}, "goal": None}


def on_entry(parent, node, opaque_dict):
    # mémoriser le parent pour reconstruire un chemin
    opaque_dict["parent"][node] = parent
    if node == 2:
        opaque_dict["goal"] = node
        return True
    return False


bfs(graph, opaque, on_entry)

goal = opaque["goal"]
if goal is None:
    print("Objectif non trouvé.")
else:
    # reconstruire le chemin
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = opaque["parent"].get(cur)
    path.reverse()

    print("Objectif trouvé:", goal)
    print("Chemin:", path)
