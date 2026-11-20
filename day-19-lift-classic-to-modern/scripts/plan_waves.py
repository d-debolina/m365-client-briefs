"""LIFT wave planner: decide per site HOW to modernize and in which wave.
Usage: python scripts/plan_waves.py assessment/sites.csv > waves.csv
"""
import csv, sys
def decide(s):
    sub, pub, js = int(s["subsites"]), s["publishing"] == "True", s["custom_actions_js"] == "True"
    perms, idle, wf = int(s["unique_permission_objects"]), int(s["last_activity_days"]), int(s["workflows_2013"])
    if idle > 730: return "Archive (Microsoft 365 Archive / read-only)", 0, "No activity for 2+ years"
    if s["group_connected"] == "True" and int(s["classic_pages"]) == 0: return "Already modern: tidy only", 1, ""
    if pub or sub >= 9 or (perms > 600 and sub > 0): return "Restructure with ShareGate (new flat sites)", 3, "Publishing/subsites/permission sprawl"
    notes = []
    if js: notes.append("rebuild JS custom actions as SPFx extensions or drop")
    if wf: notes.append(f"{wf} SharePoint 2013 workflow(s) → Power Automate")
    return "In place: groupify + transform pages (PnP)", 2 if notes else 1, "; ".join(notes)
rows = list(csv.DictReader(open(sys.argv[1])))
w = csv.writer(sys.stdout); w.writerow(["wave", "site", "approach", "notes", "size_gb"])
for s in sorted(rows, key=lambda s: decide(s)[1]):
    a, wave, note = decide(s); w.writerow([wave, s["title"], a, note, s["size_gb"]])
