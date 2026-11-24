"""Generates the fictional CREW sample data (Day 29).

python scripts/make_data.py            -> writes data/*.csv (plan starts Monday 2027-01-04)
python scripts/make_data.py 2027-03-01 -> shifts the 26-week plan to another Monday

All companies, people and projects are fictional (Contoso / Fabrikam style).
"""
import csv, random, sys, pathlib, datetime as dt

random.seed(31)
HERE = pathlib.Path(__file__).resolve().parents[1]
DATA = HERE / "data"
DATA.mkdir(exist_ok=True)
start = dt.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else dt.date(2027, 1, 4)
assert start.weekday() == 0, "plan must start on a Monday"
WEEKS = [start + dt.timedelta(weeks=i) for i in range(26)]
SKILLS = ["Foreman", "Journeyman", "Apprentice"]
EQUIP = ["Scissor lift", "Telehandler", "Mini excavator", "Concrete mixer"]


def write(name, rows):
    with open(DATA / name, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    print(f"{name}: {len(rows)} rows")


# Business units map to Microsoft 365 security groups in the security model
units = ["North yard", "South yard"]
first = ["Ava", "Ben", "Chloe", "Dan", "Ella", "Femi", "Gus", "Hana", "Ivan", "Jade", "Kai", "Lena",
         "Milo", "Nora", "Omar", "Pia", "Quinn", "Rosa", "Sam", "Tara", "Uma", "Vik", "Wes", "Yara"]
last = ["Contoso", "Fabrikam", "Northwind", "Tailspin", "Litware", "Adatum", "Proseware", "Woodgrove"]

crew = []
for i in range(36):
    skill = "Foreman" if i < 6 else ("Journeyman" if i < 22 else "Apprentice")
    crew.append({
        "CrewId": f"CRW-{i+1:03d}",
        "Name": f"{first[i % len(first)]} {last[(i * 3) % len(last)]}",
        "SkillLevel": skill,
        "BusinessUnit": units[i % 2],
        "HoursPerWeek": 40 if skill != "Apprentice" else 32,
    })
write("crew_members.csv", crew)

projects = []
names = ["Harbour Library", "Maple Clinic", "Riverside School", "Oak Street Flats", "Airport Hangar 3",
         "City Pool", "Northwind Depot", "Tailspin Offices", "Fabrikam Plant", "Contoso HQ Fit-out",
         "Litware Lab", "Woodgrove Bank Branch", "Adatum Warehouse", "Park Pavilion", "Station Car Park"]
for i, nm in enumerate(names):
    s = random.randint(0, 8)
    projects.append({
        "ProjectId": f"PRJ-{i+1:02d}", "Name": nm, "BusinessUnit": units[i % 2],
        "StartWeek": WEEKS[s].isoformat(), "EndWeek": WEEKS[min(25, s + random.randint(8, 17))].isoformat(),
        "PlanLocked": "Yes" if i < 5 else "No",
    })
write("projects.csv", projects)

# Weekly demand by skill (hours) and equipment (units) per project
demand = []
for p in projects:
    for w in WEEKS:
        if not (p["StartWeek"] <= w.isoformat() <= p["EndWeek"]):
            continue
        for sk, (lo, hi) in zip(SKILLS, [(8, 32), (16, 72), (0, 40)]):
            h = random.randrange(lo, hi + 1, 8)
            if h:
                demand.append({"ProjectId": p["ProjectId"], "WeekStart": w.isoformat(), "Kind": "Skill",
                               "Item": sk, "Quantity": h})
        if random.random() < 0.45:
            demand.append({"ProjectId": p["ProjectId"], "WeekStart": w.isoformat(), "Kind": "Equipment",
                           "Item": random.choice(EQUIP), "Quantity": 1})
write("weekly_demand.csv", demand)

# Owned equipment (anything above this is a rental)
fleet = [{"EquipmentType": e, "OwnedUnits": n, "RentalPerWeek": r}
         for e, n, r in zip(EQUIP, [3, 2, 2, 2], [420, 690, 560, 310])]
write("equipment_fleet.csv", fleet)

# Leave (reduces supply)
leave = []
for c in random.sample(crew, 14):
    w = random.choice(WEEKS)
    leave.append({"CrewId": c["CrewId"], "WeekStart": w.isoformat(), "HoursOff": random.choice([8, 16, 40])})
write("leave.csv", leave)

# Public holidays used by the workday maths (fictional calendar)
hol = [d for d in [dt.date(2027, 1, 1), dt.date(2027, 4, 2), dt.date(2027, 4, 5), dt.date(2027, 5, 31)]]
write("holidays.csv", [{"Date": d.isoformat(), "Name": "Company holiday"} for d in hol])

# Two-week look-ahead tasks for the locked projects (the lock demo)
tasks = []
k = 1
for p in projects[:5]:
    for j in range(4):
        d = WEEKS[2] + dt.timedelta(days=j * 2)
        tasks.append({"TaskId": f"TSK-{k:03d}", "ProjectId": p["ProjectId"],
                      "Title": random.choice(["Set out", "Pour slab", "Frame walls", "First fix", "Roof sheets",
                                              "Scaffold up", "Drainage", "Snag list"]),
                      "StartDate": d.isoformat(), "DurationWorkdays": random.randint(1, 5),
                      "Locked": p["PlanLocked"]})
        k += 1
write("lookahead_tasks.csv", tasks)
