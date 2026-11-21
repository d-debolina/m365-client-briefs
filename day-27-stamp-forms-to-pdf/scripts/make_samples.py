"""Create fictional form responses and render preview HTML files from templates/enrolment.html.

Run:  python scripts/make_samples.py
Open samples/*.html in a browser (or print to PDF) to check the layout before you build the flow.
"""
import csv, html, json, random, datetime as dt, pathlib

random.seed(27)
ROOT = pathlib.Path(__file__).resolve().parents[1]
FIRST = ["Avery", "Jordan", "Riley", "Sam", "Taylor", "Morgan", "Casey", "Jamie", "Alex", "Robin"]
LAST = ["Contoso", "Fabrikam", "Northwind", "Tailspin", "Litware", "Adatum", "Proseware", "Woodgrove"]
PROGRAMMES = ["Foundations", "Active Living", "Mindful Workplace", "Family Plus"]
SESSIONS = ["Weekday mornings", "Weekday evenings", "Weekends", "Online only"]

rows = []
for i in range(1, 21):
    fn, ln = random.choice(FIRST), random.choice(LAST)
    submitted = dt.datetime(2027, 2, 1, 8, 0) + dt.timedelta(hours=random.randint(0, 600))
    rows.append({
        "ResponseId": i,
        "SubmittedOn": submitted.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "FullName": f"{fn} {ln}",
        "Email": f"{fn.lower()}.{ln.lower()}@example.com",
        "Phone": f"+00 555 01{random.randint(10, 99)}",
        "DateOfBirth": dt.date(random.randint(1960, 2004), random.randint(1, 12), random.randint(1, 28)).isoformat(),
        "Programme": random.choice(PROGRAMMES),
        "StartDate": (submitted.date() + dt.timedelta(days=random.randint(7, 40))).isoformat(),
        "Sessions": json.dumps(random.sample(SESSIONS, random.randint(1, 3))),
        "EmergencyName": f"{random.choice(FIRST)} {ln}",
        "EmergencyPhone": f"+00 555 02{random.randint(10, 99)}",
        "Notes": random.choice(["", "Prefers online sessions in the first month.", "Will join with a colleague.", ""]),
        "Terms": "I agree",
    })

csv_path = ROOT / "samples" / "form-responses.csv"
with csv_path.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

tpl = (ROOT / "templates" / "enrolment.html").read_text(encoding="utf-8")
for r in rows[:3]:
    ref = f"ENR-{r['SubmittedOn'][:10].replace('-', '')}-{r['ResponseId']:04d}"
    values = dict(r, Reference=ref,
                  Sessions=", ".join(json.loads(r["Sessions"])),   # same clean-up the flow does
                  SubmittedOn=r["SubmittedOn"][:16].replace("T", " "),
                  Notes=r["Notes"] or "–")
    out = tpl
    for k, v in values.items():
        out = out.replace("{{" + k + "}}", html.escape(str(v)))   # always HTML-encode answers
    (ROOT / "samples" / f"{ref}.html").write_text(out, encoding="utf-8")
print("wrote", csv_path, "and 3 preview files")
