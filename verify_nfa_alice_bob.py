from __future__ import annotations
import argparse
from typing import Any, Dict, List, Optional, Sequence, Tuple
from bfs import bfs
from ls2rg import LS2RG
from soup_lang import SoupSemantics
from alice_bob_soup_models import get_model
from StepSynchronousProduct import StepSynchronousProduct
from isoup_lang import iSoupSemantics
from nfa_properties import (
    build_never_cond_pattern1,
    build_never_cond_pattern2,
    cond_exclusion,
    make_cond_deadlock,
)

import os

PY_CMD = "python" if os.name == "nt" else "python3"


def reconstruct_path(goal: Any, parent: Dict[Any, Any]) -> List[Any]:
    path: List[Any] = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent.get(cur)
    return list(reversed(path))


def edge_labels(path: Sequence[Any], rg: Any) -> List[str]:
    return [rg.label(path[i], path[i + 1]) for i in range(len(path) - 1)]


def project_system_trace(path: Sequence[Any]) -> List[Any]:
    # path nodes are (lhs_state, rhs_state); first lhs may be None
    out = []
    for lhs, _ in path:
        if lhs is not None:
            out.append(lhs)
    return out


def project_system_actions(labels: Sequence[str]) -> List[str]:
    # label is like "a1||cond" or "init||true" or "stutter||cond"
    return [lab.split("||", 1)[0] for lab in labels]


def build_property(prop: str, pattern: int, sys_sem: SoupSemantics):
    prop_u = prop.upper()
    if prop_u == "P1":
        cond = cond_exclusion
    elif prop_u == "P2":
        cond = make_cond_deadlock()
    else:
        raise ValueError(f"Propriété inconnue: {prop}")

    if pattern == 1:
        return build_never_cond_pattern1(cond)
    if pattern == 2:
        return build_never_cond_pattern2(cond)
    raise ValueError(f"Patron inconnu: {pattern}")


def verify_one(model: str, prop: str, pattern: int) -> Dict[str, Any]:
    # 1) système
    soup = get_model(model)
    sys_sem = SoupSemantics(soup)

    # 2) propriété iSoup (NFA)
    isoup = build_property(prop, pattern, sys_sem)
    prop_sem = iSoupSemantics(isoup)

    # 3) produit
    prod = StepSynchronousProduct(sys_sem, prop_sem)
    prod_rg = LS2RG(prod, keep_labels=True)

    opaque: Dict[str, Any] = {"parent": {}, "goal": None}

    def on_entry(parent: Optional[Any], node: Any, opaque_dict: Dict[str, Any]) -> bool:
        opaque_dict["parent"][node] = parent
        # node = (lhs_state, prop_state)
        if prop_sem.accepting(node[1]):
            opaque_dict["goal"] = node
            return True
        return False

    opaque_out, visited = bfs(prod_rg, opaque, on_entry)

    goal = opaque_out["goal"]
    if goal is None:
        return {
            "sat": True,
            "visited": len(visited),
            "counterexample": None,
        }

    path = reconstruct_path(goal, opaque_out["parent"])
    labels = edge_labels(path, prod_rg)
    sys_states = project_system_trace(path)
    sys_actions = project_system_actions(labels)

    return {
        "sat": False,
        "visited": len(visited),
        "counterexample": {
            "product_path": path,
            "edge_labels": labels,
            "sys_states": sys_states,
            "sys_actions": sys_actions,
            "accepting_node": goal,
        },
    }


def md_block(lines: List[str]) -> str:
    return "\n".join(lines) + "\n"


def fmt_sys_trace(sys_states: List[Any], sys_actions: List[str]) -> List[str]:
    """
    Retourne une trace lisible au format:
      s0 --a0--> s1
      s1 --a1--> s2
    Hypothèse: len(sys_states) = len(sys_actions) (+0 ou +1 selon présence init).
    On corrige automatiquement si l'action "init" existe sans état précédent.
    """
    if not sys_states:
        return ["(empty)"]

    # Cas typique NFA: sys_states ne contient pas forcément l'état initial "None",
    # et sys_actions contient souvent "init" en première position.
    # Si on a une action de plus que d'états-1, on transforme init en stutter sur s0.
    if len(sys_actions) == len(sys_states):
        # ex: ss=[s0,s1,s2], sa=[init,a1,b1] -> on veut s0--init-->s0 puis s0--a1-->s1 ...
        ss = [sys_states[0]] + sys_states
        sa = sys_actions
    else:
        ss = sys_states
        sa = sys_actions

    lines: List[str] = []
    for i, a in enumerate(sa):
        if i + 1 < len(ss):
            lines.append(f"{ss[i]} --{a}--> {ss[i+1]}")
        else:
            lines.append(f"{ss[i]} --{a}--> ?")
    return lines


def write_report(results: List[Dict[str, Any]], out_path: str) -> None:
    lines: List[str] = []
    lines.append("# VerificationNFAAliceBob")
    lines.append("")
    lines.append("Ce fichier est généré par `verify_nfa_alice_bob.py`.")
    lines.append("")
    lines.append("## Exécution rapide")
    lines.append("")
    lines.append(
        "Pour lancer **tous** les scénarios (AB1..AB5 × (P1,P2) × (Patron 1,2)) :"
    )
    lines.append("```bash")
    lines.append(f"{PY_CMD} verify_nfa_alice_bob.py --all")
    lines.append("```")
    lines.append("")

    # Explication patrons
    lines.append("## Différence entre Patron 1 et Patron 2")
    lines.append("")
    lines.append(
        "- **Patron 1** : boucle `true` sur l’état T. Le produit contient potentiellement plus de transitions (non-déterminisme supplémentaire)."
    )
    lines.append(
        "- **Patron 2** : boucle `!cond` sur T. Le produit est plus *contraint* : une seule transition depuis T selon la valeur de `cond` (souvent moins de branchements)."
    )
    lines.append(
        "- Les deux reconnaissent l’idée « `cond` arrive au moins une fois », mais l’**impact pratique** se voit via `visited` (nombre d’états explorés) et parfois le **contre-exemple** trouvé en premier (à cause de l’ordre des actions)."
    )
    lines.append("")

    lines.append("## Résultats")
    lines.append("")

    for r in results:
        model, prop, pattern = r["model"], r["prop"], r["pattern"]
        cmd = f"{PY_CMD} verify_nfa_alice_bob.py --model {model} --prop {prop} --pattern {pattern}"

        lines.append(f"### {model} — {prop} — Patron {pattern}")
        lines.append("")
        lines.append("Commande reproductible :")
        lines.append("```bash")
        lines.append(cmd)
        lines.append("```")
        lines.append("")
        lines.append(f"- États explorés (visited) : **{r['visited']}**")

        if r["sat"]:
            lines.append("- Résultat : **SAT** (pas de contre-exemple)")
            lines.append("")
        else:
            lines.append("- Résultat : **VIOLÉ** (contre-exemple trouvé)")
            ce = r["counterexample"]
            lines.append("")
            lines.append("Trace (projection système) :")
            lines.append("```text")
            # imprime états + actions
            # sys_states a longueur = nb configs rencontrées (sans le None initial)
            # sys_actions a longueur = nb arêtes; la première peut être "init"
            ss = ce["sys_states"]
            sa = ce["sys_actions"]
            for line in fmt_sys_trace(ss, sa):
                lines.append(line)
            lines.append("```")
            lines.append("")
            lines.append("Labels du produit :")
            lines.append("```text")
            for lab in ce["edge_labels"]:
                lines.append(lab)
            lines.append("```")
            lines.append("")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md_block(lines))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--all",
        action="store_true",
        help="Vérifier tous les couples AB1..AB5 × (P1,P2) × (Patron1,Patron2).",
    )
    parser.add_argument("--model", type=str, default=None, help="AB1..AB5")
    parser.add_argument("--prop", type=str, default=None, help="P1 ou P2")
    parser.add_argument("--pattern", type=int, default=None, help="1 ou 2")
    parser.add_argument("--out", type=str, default="VerificationNFAAliceBob.md")
    args = parser.parse_args()

    results: List[Dict[str, Any]] = []

    if args.all:
        models = ["AB1", "AB2", "AB3", "AB4", "AB5"]
        props = ["P1", "P2"]
        patterns = [1, 2]
        for m in models:
            for p in props:
                for pat in patterns:
                    res = verify_one(m, p, pat)
                    res.update({"model": m, "prop": p, "pattern": pat})
                    results.append(res)
        write_report(results, args.out)
        print(f"[OK] Rapport écrit dans: {args.out}")
        return

    # mode unitaire
    if args.model is None or args.prop is None or args.pattern is None:
        raise SystemExit("Utilise --all ou bien --model ABk --prop P1/P2 --pattern 1/2")

    res = verify_one(args.model, args.prop, args.pattern)
    res.update({"model": args.model, "prop": args.prop, "pattern": args.pattern})
    write_report([res], args.out)
    print(f"[OK] Rapport écrit dans: {args.out}")


if __name__ == "__main__":
    main()
