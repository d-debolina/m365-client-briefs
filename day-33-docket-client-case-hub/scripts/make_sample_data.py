"""Writes the fictional sample data for Day 33 DOCKET into ../data.

A fictional 20-person professional services firm (Fabrikam Advisory). Everything is invented. Run:
    python scripts/make_sample_data.py
"""
import csv, pathlib, random

random.seed(33)
DATA = pathlib.Path(__file__).resolve().parents[1] / "data"
DATA.mkdir(exist_ok=True)


def write(name, header, rows):
    with open(DATA / name, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print("wrote", name, len(rows), "rows")


staff = [
    ["S01", "Hannah Price", "Partner", "Commercial", 30],
    ["S02", "Ravi Shah", "Partner", "Employment", 30],
    ["S03", "Olivia Bennett", "Senior Associate", "Commercial", 37],
    ["S04", "Tom Okafor", "Associate", "Commercial", 37],
    ["S05", "Mei Lin", "Associate", "Employment", 37],
    ["S06", "Jack Evans", "Associate", "Disputes", 37],
    ["S07", "Sofia Rossi", "Senior Associate", "Disputes", 37],
    ["S08", "Ben Carter", "Paralegal", "Commercial", 37],
    ["S09", "Aisha Khan", "Paralegal", "Disputes", 37],
    ["S10", "Leo Martin", "Trainee", "Employment", 37],
]
write("staff.csv", ["staff_id", "name", "role", "practice", "weekly_capacity_hours"], staff)

clients = [
    ["C001", "Contoso Retail Ltd", "Corporate", "Active", "S01"],
    ["C002", "Northwind Logistics", "Corporate", "Active", "S01"],
    ["C003", "Tailspin Toys", "Corporate", "Active", "S02"],
    ["C004", "Wide World Importers", "Corporate", "Active", "S07"],
    ["C005", "Adventure Works Cycles", "Corporate", "Active", "S01"],
    ["C006", "Litware Health Group", "Corporate", "Active", "S02"],
    ["C007", "Proseware Inc", "Corporate", "Dormant", "S03"],
    ["C008", "Woodgrove Bank", "Corporate", "Active", "S07"],
    ["C009", "Fourth Coffee", "SME", "Active", "S02"],
    ["C010", "Alpine Ski House", "SME", "Active", "S03"],
    ["C011", "Margie's Travel", "SME", "Active", "S06"],
    ["C012", "Lucerne Publishing", "SME", "Prospect", "S01"],
]
write("clients.csv", ["client_id", "client_name", "segment", "status", "relationship_partner"], clients)

retainers = [
    ["RET-001", "C001", "Monthly advisory", 4000, 20, "2026-01-01", "2027-12-31"],
    ["RET-002", "C002", "Contracts desk", 2500, 12, "2026-06-01", "2027-05-31"],
    ["RET-003", "C006", "Employment helpline", 3000, 15, "2026-04-01", "2027-03-31"],
    ["RET-004", "C008", "Disputes first response", 5000, 20, "2026-09-01", "2027-08-31"],
    ["RET-005", "C009", "HR policy support", 800, 4, "2026-11-01", "2027-10-31"],
]
write("retainers.csv", ["retainer_id", "client_id", "scope", "monthly_fee_gbp", "included_hours", "start", "end"], retainers)

practices = {"Commercial": ["S01", "S03", "S04", "S08"], "Employment": ["S02", "S05", "S10"],
             "Disputes": ["S06", "S07", "S09"]}
types = {"Commercial": ["Contract review", "Share purchase", "Supplier dispute advice", "Terms refresh"],
         "Employment": ["Tribunal claim", "Restructure", "Grievance investigation", "Policy review"],
         "Disputes": ["Debt recovery", "Mediation", "Pre-action letter", "Injunction"]}
cases, alloc = [], []
active = [c for c in clients if c[3] == "Active"]
for i in range(1, 31):
    cl = active[(i * 7) % len(active)]
    practice = list(practices)[i % 3]
    team = practices[practice]
    lead = team[0] if i % 4 == 0 else team[1]
    restricted = "Yes" if i in (4, 11, 17, 23, 29) else "No"          # ethical wall / sensitive
    external = "Yes" if i in (2, 5, 8, 13, 19, 26) else "No"          # client collaborates on files
    status = "Closed" if i in (1, 3, 9) else ("On hold" if i == 14 else "Open")
    retainer = next((r[0] for r in retainers if r[1] == cl[0]), "")
    cases.append([f"CASE-{2027000 + i}", cl[0], f"{random.choice(types[practice])} – {cl[1].split()[0]}",
                  practice, lead, retainer, restricted, external, status])
    if status == "Open":
        for s in team:
            hrs = random.choice([0, 1, 2, 3]) if s != lead else random.choice([3, 4, 6])
            if hrs:
                alloc.append([f"CASE-{2027000 + i}", s, "2027-04-05", hrs])
# One urgent injunction lands on Sofia: shows an over-allocation on the dashboard
urgent = next(c[0] for c in cases if c[3] == "Disputes" and c[8] == "Open")
alloc.append([urgent, "S07", "2027-04-05", 8])
write("cases.csv", ["case_id", "client_id", "case_title", "practice", "lead", "retainer_id", "restricted",
                    "external_access", "status"], cases)
write("allocations.csv", ["case_id", "staff_id", "week_start", "hours"], alloc)

# External contacts (guests). Expiry set per contact; nobody gets 'Anyone' links.
write("external-contacts.csv", ["contact", "client_id", "case_id", "access", "expires"], [
    ["legal@contoso-retail.example", "C001", "CASE-2027002", "Edit", "2027-06-30"],
    ["cfo@northwind.example", "C002", "CASE-2027005", "View", "2027-05-31"],
    ["hr@tailspin.example", "C003", "CASE-2027008", "Edit", "2027-07-31"],
    ["gc@woodgrove.example", "C008", "CASE-2027013", "View", "2027-06-15"],
    ["ops@fourthcoffee.example", "C009", "CASE-2027019", "Edit", "2027-04-30"],
    ["md@alpineski.example", "C010", "CASE-2027026", "View", "2027-09-30"],
])
