"""DOCKET planning helper: permission plan, unique-scope count and the allocation table for Power BI.

1. Permission plan: which case document sets need their own permissions, who gets in, and where external
   people work (never in the internal Case files library).
2. Unique-scope check: SharePoint supports up to 50,000 unique permission scopes per library, but Microsoft
   recommends staying under 5,000. We project how many years the design lasts at the current case volume.
3. Allocation: hours planned per person this week vs capacity, with an over-allocation flag.

Run:  python scripts/docket_plan.py     (writes out/permission-plan.csv and out/allocation-dashboard.csv)
"""
import csv, collections, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA, OUT = ROOT / "data", ROOT / "out"
RECOMMENDED_SCOPES = 5000


def load(name):
    with open(DATA / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def permission_plan(cases, staff):
    by_id = {s["staff_id"]: s for s in staff}
    rows = []
    for c in cases:
        team = sorted({s["staff_id"] for s in staff if s["practice"] == c["practice"]} | {c["lead"]})
        if c["restricted"] == "Yes":
            # Ethical wall: break inheritance on the document set, grant a case-specific group only
            access = f"DOCKET-{c['case_id']}-Team (lead {by_id[c['lead']]['name']} + named members)"
            unique = 1
        else:
            access = f"DOCKET-{c['practice']} (practice group, inherited)"
            unique = 0
        external = (f"Client Share site → folder {c['case_id']} (guests, Specific people links, expiry)"
                    if c["external_access"] == "Yes" else "none")
        rows.append({"case_id": c["case_id"], "practice": c["practice"], "restricted": c["restricted"],
                     "internal_access": access, "unique_scopes_in_case_files": unique,
                     "external_access": external, "team_size": len(team)})
    return rows


def scope_projection(plan, cases_per_year):
    restricted_share = sum(r["unique_scopes_in_case_files"] for r in plan) / max(len(plan), 1)
    per_year = cases_per_year * restricted_share
    years = RECOMMENDED_SCOPES / per_year if per_year else float("inf")
    return restricted_share, per_year, years


def allocation(allocs, staff, week):
    hours = collections.Counter()
    cases = collections.defaultdict(set)
    for a in allocs:
        if a["week_start"] == week:
            hours[a["staff_id"]] += float(a["hours"])
            cases[a["staff_id"]].add(a["case_id"])
    out = []
    for s in staff:
        cap = float(s["weekly_capacity_hours"])
        h = hours[s["staff_id"]]
        out.append({"staff_id": s["staff_id"], "name": s["name"], "practice": s["practice"], "week_start": week,
                    "planned_hours": h, "capacity": cap, "utilisation_pct": round(100 * h / cap),
                    "open_cases": len(cases[s["staff_id"]]),
                    "flag": "OVER" if h > cap else ("LOW" if h < 0.5 * cap else "")})
    return out


def write(name, rows):
    OUT.mkdir(exist_ok=True)
    with open(OUT / name, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def main():
    staff, cases, allocs = load("staff.csv"), load("cases.csv"), load("allocations.csv")
    plan = permission_plan(cases, staff)
    write("permission-plan.csv", plan)
    share, per_year, years = scope_projection(plan, cases_per_year=400)
    print(f"Restricted cases: {share:.0%} -> about {per_year:.0f} new unique scopes a year in Case files")
    print(f"By design alone, the recommended {RECOMMENDED_SCOPES} would take about {years:.0f} years. "
          f"The real risk is ad-hoc sharing: every file or folder shared on its own adds a scope too, "
          f"so keep sharing out of Case files and watch the count in the permission report.")
    dash = allocation(allocs, staff, "2027-04-05")
    write("allocation-dashboard.csv", dash)
    for d in dash:
        print(f"  {d['name']:<16} {d['planned_hours']:>5.0f} / {d['capacity']:.0f} h  {d['flag']}")


if __name__ == "__main__":
    main()
