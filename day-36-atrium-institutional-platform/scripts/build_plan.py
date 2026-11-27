"""Turns data/modules.csv into a phased build order with a licence note per phase (out/build-order.md)."""
import csv, pathlib, collections

ROOT = pathlib.Path(__file__).resolve().parents[1]
PHASES = {1: "Foundations + first module", 2: "Governance & service basics", 3: "Money & records",
          4: "Academic", 5: "AI assistant"}


def plan():
    with open(ROOT / "data/modules.csv", encoding="utf-8") as f:
        mods = list(csv.DictReader(f))
    by = collections.defaultdict(list)
    for m in mods:
        by[int(m["phase"])].append(m)
    lines = ["# ATRIUM build order (generated)", ""]
    for p in sorted(by):
        lines.append(f"## Phase {p}: {PHASES[p]}")
        for m in by[p]:
            lines.append(f"- **{m['module']}** ({m['group']}) → {m['home']} · {m['main_store']} · {m['automation']}")
        premium = [m["module"] for m in by[p] if m["premium"] != "No"]
        lines.append(f"- Licences: {'standard Microsoft 365 only' if not premium else 'extra for ' + ', '.join(premium)}")
        lines.append("")
    (ROOT / "out").mkdir(exist_ok=True)
    (ROOT / "out/build-order.md").write_text("\n".join(lines), encoding="utf-8")
    return by


if __name__ == "__main__":
    by = plan()
    for p in sorted(by):
        print(f"Phase {p}: {len(by[p])} modules")
