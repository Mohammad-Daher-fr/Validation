from __future__ import annotations
from typing import Any, Dict, Optional
from bfs import bfs
from ls2rg import LS2RG
from soup_lang import SoupSemantics
from alice_bob_soup_models import CS, get_model

"""Check minimal pour les modèles AB encodés en Soup."""


def explore(name: str) -> None:
    soup = get_model(name)
    sem = SoupSemantics(soup)
    rg = LS2RG(sem, keep_labels=True)

    opaque: Dict[str, Any] = {
        "parent": {},
        "goal_mutex": None,
        "deadlocks": [],
    }

    def on_entry(parent: Optional[Any], node: Any, opaque_dict: Dict[str, Any]) -> bool:
        opaque_dict["parent"][node] = parent

        # Violation exclusion: les deux en CS
        if node[0] == CS and node[1] == CS and opaque_dict["goal_mutex"] is None:
            opaque_dict["goal_mutex"] = node

        # Deadlock: aucun successeur
        if len(rg.neighbors(node)) == 0:
            opaque_dict["deadlocks"].append(node)

        return False  # on explore tout

    opaque_out, visited = bfs(rg, opaque, on_entry)

    print()
    print(f"{name}: {len(visited)} états atteignables")

    if opaque_out["goal_mutex"] is None:
        print("  Exclusion mutuelle: OK (pas d'état CS/CS atteignable)")
    else:
        print("  Exclusion mutuelle: VIOLEE (CS/CS atteignable)")
        print(f"    Exemple d'état: {opaque_out['goal_mutex']}")

    if opaque_out["deadlocks"]:
        print(
            f"  Deadlocks: OUI ({len(opaque_out['deadlocks'])} état(s) sans successeur)"
        )
        print(f"    Exemple: {opaque_out['deadlocks'][0]}")
    else:
        print("  Deadlocks: NON")


if __name__ == "__main__":
    for m in ["AB1", "AB2", "AB3", "AB4", "AB5"]:
        explore(m)
