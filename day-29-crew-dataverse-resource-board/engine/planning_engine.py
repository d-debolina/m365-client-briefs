"""CREW planning engine: weekly demand vs supply by skill, plus equipment rentals and workday maths.

The same logic runs in the Azure Function (see function_app.py) and in the acceptance tests.
Pure Python, no packages needed:  python engine/planning_engine.py  -> prints the gap report.
"""
import csv, pathlib, datetime as dt
from collections import defaultdict

DATA = pathlib.Path(__file__).resolve().parents[1] / "data"


def read(name):
    with open(DATA / name, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def skill_gap(demand, crew, leave):
    """Return {(week, skill): {"demand": h, "supply": h, "gap": supply - demand}}."""
    weeks = sorted({d["WeekStart"] for d in demand})
    need = defaultdict(int)
    for d in demand:
        if d["Kind"] == "Skill":
            need[(d["WeekStart"], d["Item"])] += int(d["Quantity"])
    skill_of = {c["CrewId"]: c["SkillLevel"] for c in crew}
    have = defaultdict(int)
    for w in weeks:
        for c in crew:
            have[(w, c["SkillLevel"])] += int(c["HoursPerWeek"])
    for l in leave:
        have[(l["WeekStart"], skill_of[l["CrewId"]])] -= int(l["HoursOff"])
    out = {}
    for key in sorted(set(need) | {k for k in have if k[0] in weeks}):
        out[key] = {"demand": need[key], "supply": have[key], "gap": have[key] - need[key]}
    return out


def rentals(demand, fleet):
    """Units to rent per (week, equipment type) and the cost."""
    used = defaultdict(int)
    for d in demand:
        if d["Kind"] == "Equipment":
            used[(d["WeekStart"], d["Item"])] += int(d["Quantity"])
    owned = {f["EquipmentType"]: int(f["OwnedUnits"]) for f in fleet}
    price = {f["EquipmentType"]: int(f["RentalPerWeek"]) for f in fleet}
    out = {}
    for (w, e), n in used.items():
        extra = max(0, n - owned[e])
        if extra:
            out[(w, e)] = {"units": extra, "cost": extra * price[e]}
    return out


def add_workdays(start, days, holidays):
    """Date after `days` working days (Mon-Fri, skipping holidays). Mirrors WorkdayMath in the C# plug-in."""
    d = start
    while days > 0:
        d += dt.timedelta(days=1)
        if d.weekday() < 5 and d not in holidays:
            days -= 1
    return d


if __name__ == "__main__":
    gap = skill_gap(read("weekly_demand.csv"), read("crew_members.csv"), read("leave.csv"))
    short = [(k, v) for k, v in gap.items() if v["gap"] < 0]
    print(f"{len(short)} week/skill combinations are short of people:")
    for (w, s), v in short[:12]:
        print(f"  {w}  {s:<10} demand {v['demand']:>4} h  supply {v['supply']:>4} h  gap {v['gap']:>5} h")
    r = rentals(read("weekly_demand.csv"), read("equipment_fleet.csv"))
    print(f"Rental forecast: {sum(v['units'] for v in r.values())} unit-weeks, "
          f"${sum(v['cost'] for v in r.values()):,} (fictional rates)")
