from __future__ import annotations
from typing import Any, List
import verify_buchi_alice_bob as vb

import os

PY_CMD = "python" if os.name == "nt" else "python3"


def fmt_edge(e: vb.Edge) -> str:
    return f"{e.sys_action}||{e.prop_label}"


def fmt_trace(sys_states: List[Any], edges: List[vb.Edge]) -> str:
    lines: List[str] = []
    if not sys_states:
        return "(empty)"
    if not edges:
        return str(sys_states[0])

    # sys_states must be len(edges)+1
    for i, e in enumerate(edges):
        lines.append(f"{sys_states[i]} --{fmt_edge(e)}--> {sys_states[i+1]}")
    return "\n".join(lines)


def run_one(model: str, prop_name: str) -> dict:
    sys = vb.load_system(model)
    prop = vb.PROPERTIES[prop_name]()

    ok, visited, cex = vb.verify_buchi(sys, prop)

    r = {
        "model": model,
        "prop": prop_name,
        "visited": visited,
        "sat": ok,
        "cex": None,
    }

    if (not ok) and cex is not None:
        prefix_sys, prefix_edges, cycle_sys, cycle_edges = cex
        r["cex"] = {
            "prefix_sys": prefix_sys,
            "prefix_edges": prefix_edges,
            "cycle_sys": cycle_sys,
            "cycle_edges": cycle_edges,
        }

    return r


def write_md(results: List[dict], out_path: str) -> None:
    lines: List[str] = []
    lines.append("# VerificationBuchiAliceBob")
    lines.append("")
    lines.append(
        "Ce fichier est généré automatiquement par `verify_buchi_all_alice_bob.py`."
    )
    lines.append("")
    lines.append(
        "Une violation Büchi est un **cycle acceptant** dans le produit (système × propriété)."
    )
    lines.append("Le contre-exemple est donné sous forme :")
    lines.append("- **prefix-trace** : mène à une SCC acceptante")
    lines.append(
        "- **cyclic-suffix-trace** : boucle à l’intérieur de la SCC acceptante"
    )
    lines.append("")

    for r in results:
        m, p = r["model"], r["prop"]
        cmd = f"{PY_CMD} verify_buchi_alice_bob.py --model {m} --prop {p}"

        lines.append(f"## {m} — {p}")
        lines.append("")
        lines.append("Commande reproductible :")
        lines.append("```bash")
        lines.append(cmd)
        lines.append("```")
        lines.append("")
        lines.append(f"- visited: **{r['visited']}**")

        if r["sat"]:
            lines.append("- RESULT: **SAT** (pas de cycle acceptant)")
            lines.append("")
            continue

        lines.append("- RESULT: **VIOLÉ** (cycle acceptant trouvé)")
        lines.append("")

        ce = r["cex"]
        assert ce is not None

        lines.append("### Prefix-trace (projection système)")
        lines.append("```text")
        lines.append(fmt_trace(ce["prefix_sys"], ce["prefix_edges"]))
        lines.append("```")
        lines.append("")

        lines.append("### Cyclic-suffix-trace (projection système)")
        lines.append("```text")
        lines.append(fmt_trace(ce["cycle_sys"], ce["cycle_edges"]))
        lines.append("```")
        lines.append("")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def main() -> None:
    models = ["AB1", "AB2", "AB3", "AB4", "AB5"]
    props = ["P1", "P2", "P3", "P4", "P5"]

    results: List[dict] = []
    for m in models:
        for p in props:
            results.append(run_one(m, p))

    out = "VerificationBuchiAliceBob.md"
    write_md(results, out)
    print(f"[OK] written: {out}")


if __name__ == "__main__":
    main()
