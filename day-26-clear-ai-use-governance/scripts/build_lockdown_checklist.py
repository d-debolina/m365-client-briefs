"""CLEAR: turn the folder access review (CSV) into a prioritised checklist for the IT lead.

Usage:  python scripts/build_lockdown_checklist.py data/folder-access-review.csv > data/lockdown-checklist.md
Read-only: it never touches Microsoft 365. The IT lead makes every change himself.
"""
import csv, sys
from collections import Counter

SENS = {"HR": 3, "Client – confidential": 3, "Finance": 2, "Internal": 1, "Public": 0}
EXPOSURE = {"Everyone except external users": 3, "Anyone link": 3, "Whole firm group": 2,
            "Department + guests": 2, "Department": 1, "Named people": 0}

def score(row):
    s = SENS.get(row["sensitivity"], 1) * EXPOSURE.get(row["current_access"], 1)
    if row["in_copilot_test"] == "yes":   # a test prompt returned content from this folder
        s += 2
    return s

def action(row, s):
    if s >= 6:
        return "Fix now: remove broad access, grant the named group only, then re-run the Copilot test prompt"
    if s >= 3:
        return "Fix this month: tighten to the department group; ask the owner to confirm members"
    return "Keep: review again at the next quarterly check"

def main(path):
    rows = list(csv.DictReader(open(path, encoding="utf-8")))
    for r in rows:
        r["score"] = score(r)
    rows.sort(key=lambda r: -r["score"])
    print("# Folder lockdown checklist (for the IT lead)\n")
    print("Score = sensitivity × exposure (+2 if a Copilot test prompt surfaced it). Highest first.\n")
    print("| # | Site › folder | Sensitivity | Who can open it now | Should be | Score | Action | Done |")
    print("|---|---|---|---|---|---|---|---|")
    for i, r in enumerate(rows, 1):
        print(f"| {i} | {r['site']} › {r['folder']} | {r['sensitivity']} | {r['current_access']} | "
              f"{r['should_be']} | {r['score']} | {action(r, r['score'])} | ☐ |")
    c = Counter("now" if r["score"] >= 6 else "month" if r["score"] >= 3 else "keep" for r in rows)
    print(f"\n**Summary:** {c['now']} fix now · {c['month']} fix this month · {c['keep']} keep. "
          "After each change, repeat the same Copilot test prompt as a user who should *not* see the folder.")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "data/folder-access-review.csv")
