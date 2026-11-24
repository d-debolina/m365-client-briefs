"""Generate fictional sample data for Day 28 NUDGE.

All accounts, reps and events are invented (Contoso / Fabrikam style).
Dates are relative to a fixed demo "today" so the data stays stable:
    python scripts/make_data.py            # demo today = 2027-03-16
    python scripts/make_data.py 2027-04-01 # shift everything to another day
"""
import csv, random, sys, pathlib, datetime as dt

random.seed(30)
OUT = pathlib.Path(__file__).resolve().parents[1] / "data"
TODAY = dt.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else dt.date(2027, 3, 16)

REPS = [("Avery Lin", "avery.lin@contoso.example"), ("Sam Okafor", "sam.okafor@contoso.example"),
        ("Rita Mendes", "rita.mendes@contoso.example"), ("Jonas Weber", "jonas.weber@contoso.example")]
ACCOUNTS = ["Contoso General Hospital", "Northwind Orthopaedic Clinic", "Fabrikam University Medical Centre",
            "Tailspin Day Surgery", "Woodgrove Community Hospital", "Litware Spine Institute",
            "Adventure Works Sports Clinic", "Alpine Ski Medical", "Proseware Regional Hospital",
            "Wide World Surgical Centre", "Coho Valley Hospital", "Lucerne Joint Care"]
STAGES = ["Prospect", "Evaluation", "First cases", "Adopted", "At risk"]
PRODUCTS = ["KneeFlex implant system", "SpineGuide navigation", "QuickSet bone cement", "ArthroView scope"]

# Commitment types the agent understands (see agent/playbook.md)
TYPES = {
    "Proctorship": ("How did the proctorship with {who} go?", 14, 60),
    "In-service training": ("Did the in-service for the theatre team happen, and who attended?", 3, 21),
    "Product evaluation": ("What did the evaluation committee decide?", 7, 45),
    "Value analysis meeting": ("What came out of the value analysis meeting?", 2, 30),
    "Sample delivery": ("Did the samples arrive, and has the surgeon tried them?", 3, 14),
    "Follow-up call": ("How did the call go? Any next step?", 1, 10),
}
SURGEONS = ["Dr. A. Rivera", "Dr. K. Novak", "Dr. M. Haddad", "Dr. P. Lindqvist", "Dr. S. Tanaka", "Dr. L. Moreau"]


def accounts():
    rows = []
    for i, name in enumerate(ACCOUNTS, 1):
        rep = REPS[(i - 1) % len(REPS)]
        rows.append({"AccountId": f"ACC-{i:03d}", "AccountName": name, "OwnerName": rep[0], "OwnerEmail": rep[1],
                     "Stage": random.choice(STAGES), "FocusProduct": random.choice(PRODUCTS),
                     "KeySurgeon": random.choice(SURGEONS),
                     "LastContact": (TODAY - dt.timedelta(days=random.randint(2, 75))).isoformat()})
    return rows


def commitments(accts):
    rows, n = [], 1
    for a in accts:
        for _ in range(random.randint(1, 3)):
            ctype = random.choice(list(TYPES))
            q, lo, hi = TYPES[ctype]
            event = TODAY + dt.timedelta(days=random.randint(-30, 50))
            follow = event + dt.timedelta(days=random.choice([1, 2, 3]))
            done = follow < TODAY - dt.timedelta(days=5) and random.random() < 0.7
            rows.append({
                "CommitmentId": f"CMT-{n:04d}", "AccountId": a["AccountId"], "AccountName": a["AccountName"],
                "OwnerEmail": a["OwnerEmail"], "Type": ctype,
                "Description": f"{ctype} – {a['FocusProduct']} with {a['KeySurgeon']}",
                "EventDate": event.isoformat(), "FollowUpDate": follow.isoformat(),
                "FollowUpQuestion": q.format(who=a["KeySurgeon"]),
                "Status": "Done" if done else "Open",
                "Outcome": random.choice(["Went well – surgeon wants 3 more cases", "Postponed by the hospital",
                                          "Mixed – needs a second session", "Committee approved a 3-month trial"]) if done else "",
                "NextStep": "", "CreatedBy": "NUDGE agent"})
            n += 1
    # Guarantee a couple of follow-ups due on demo day so the flow has something to send
    for r in rows[:3]:
        r["FollowUpDate"], r["Status"], r["Outcome"] = TODAY.isoformat(), "Open", ""
        r["EventDate"] = (TODAY - dt.timedelta(days=1)).isoformat()
    return rows


def activities(accts):
    kinds = ["Call", "Visit", "Email", "Case support", "Lunch & learn"]
    rows = []
    for i in range(1, 61):
        a = random.choice(accts)
        rows.append({"ActivityId": f"ACT-{i:04d}", "AccountId": a["AccountId"], "Kind": random.choice(kinds),
                     "Date": (TODAY - dt.timedelta(days=random.randint(1, 90))).isoformat(),
                     "Summary": random.choice(["Discussed pricing for 12 units", "Surgeon asked for a cadaver lab",
                                               "Theatre manager raised a sterilisation question",
                                               "Procurement wants a value analysis pack",
                                               "Covered two cases, smooth", "Competitor rep present"]),
                     "OwnerEmail": a["OwnerEmail"]})
    return sorted(rows, key=lambda r: r["Date"])


def write(name, rows):
    with open(OUT / name, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
    print(f"{name}: {len(rows)} rows")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    a = accounts()
    write("accounts.csv", a)
    write("commitments.csv", commitments(a))
    write("activities.csv", activities(a))
