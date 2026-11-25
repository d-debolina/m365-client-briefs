"""Generate fictional sample activities for the ATLAS leadership calendar (Day 1)."""
import csv, random, datetime as dt, pathlib

random.seed(26)
OUT = pathlib.Path(__file__).resolve().parents[1] / "list" / "sample-activities.csv"
YEAR = 2027

CATEGORIES = [
    "Leadership Team Meeting", "Business Review", "Long-Range Planning", "Budget Process",
    "Board Meeting", "Executive Visit", "Town Hall", "Strategy Offsite", "Quarterly Close",
    "Risk Committee", "People Review", "Customer Summit", "Partner Day", "Audit", "Holiday / Blackout",
]
REGIONS = ["Group", "North", "South", "East", "West", "Central"]
LOCATIONS = ["Contoso HQ, Room 4.01", "Fabrikam Hub", "Online (Teams)", "Northwind Campus", "Tailspin Office"]
VIS = ["Leadership team", "All managers", "Everyone"]

rows, i = [], 1
def add(title, cat, start, end, allday=True, t1="", t2="", region="Group", vis="Leadership team"):
    global i
    rows.append({
        "ID": i, "Title": title, "Category": cat,
        "StartDate": start.isoformat(), "EndDate": end.isoformat(),
        "AllDay": "Yes" if allday else "No", "StartTime": t1, "EndTime": t2,
        "Region": region, "Location": random.choice(LOCATIONS), "Visibility": vis,
        "Description": f"Fictional sample: {title.lower()}.",
        "DocumentLink": f"https://contoso.sharepoint.com/sites/leadership/Shared%20Documents/{cat.replace(' ', '-').replace('/', '')}",
        "MeetingLink": "" if allday else "https://teams.microsoft.com/l/meetup-join/sample",
    })
    i += 1

for m in range(1, 13):
    d = dt.date(YEAR, m, 6)
    add(f"Leadership Team Meeting – {d:%b}", "Leadership Team Meeting", d, d, False, "09:00", "11:00")
for q, m in enumerate([2, 5, 8, 11], 1):
    add(f"Q{q} Business Review", "Business Review", dt.date(YEAR, m, 9), dt.date(YEAR, m, 10), region=random.choice(REGIONS[1:]))
add("Budget kick-off", "Budget Process", dt.date(YEAR, 9, 1), dt.date(YEAR, 9, 1))
add("Budget submission deadline", "Budget Process", dt.date(YEAR, 10, 15), dt.date(YEAR, 10, 15), vis="All managers")
add("Long-range plan workshop", "Long-Range Planning", dt.date(YEAR, 6, 14), dt.date(YEAR, 6, 16))
add("Strategy offsite", "Strategy Offsite", dt.date(YEAR, 3, 22), dt.date(YEAR, 3, 24))
for m in [3, 6, 9, 12]:
    add(f"Board meeting – {dt.date(YEAR, m, 1):%B}", "Board Meeting", dt.date(YEAR, m, 18), dt.date(YEAR, m, 18), False, "13:00", "17:00")
for r in REGIONS[1:]:
    m = random.randint(1, 11); d = dt.date(YEAR, m, random.randint(1, 20))
    add(f"Executive visit – {r} region", "Executive Visit", d, d + dt.timedelta(days=1), region=r)
add("Spring town hall", "Town Hall", dt.date(YEAR, 4, 7), dt.date(YEAR, 4, 7), False, "15:00", "16:00", vis="Everyone")
add("Autumn town hall", "Town Hall", dt.date(YEAR, 10, 6), dt.date(YEAR, 10, 6), False, "15:00", "16:00", vis="Everyone")
add("Annual people review", "People Review", dt.date(YEAR, 11, 22), dt.date(YEAR, 11, 26))
add("Customer summit", "Customer Summit", dt.date(YEAR, 5, 18), dt.date(YEAR, 5, 19), vis="All managers")
add("Partner day", "Partner Day", dt.date(YEAR, 9, 23), dt.date(YEAR, 9, 23))
add("External audit fieldwork", "Audit", dt.date(YEAR, 1, 25), dt.date(YEAR, 2, 5))
add("Year-end blackout", "Holiday / Blackout", dt.date(YEAR, 12, 23), dt.date(YEAR, 12, 31), vis="Everyone")
for m in [3, 6, 9, 12]:
    add(f"Quarter close – Q{m // 3}", "Quarterly Close", dt.date(YEAR, m, 28), dt.date(YEAR, m, 30))
add("Risk committee", "Risk Committee", dt.date(YEAR, 7, 8), dt.date(YEAR, 7, 8), False, "10:00", "12:00")

rows.sort(key=lambda r: r["StartDate"])
for n, r in enumerate(rows, 1):
    r["ID"] = n
with OUT.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
print(len(rows), "activities ->", OUT)
