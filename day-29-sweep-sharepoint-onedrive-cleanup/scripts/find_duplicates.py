"""SWEEP step 2: build a keep / quarantine plan from inventory.csv. Changes nothing in Microsoft 365.

    python scripts/find_duplicates.py data/sample-inventory.csv data/cleanup-plan.csv

Rules (in this order):
  A. Exact duplicates: same quickXorHash + same size -> keep ONE (newest; prefer the name without a device suffix).
  B. Sync-conflict copies: "Report-LAPTOP-7.xlsx" next to "Report.xlsx" with different content -> NEEDS REVIEW
     (two people may have edited different things; a human merges, the script never guesses).
  C. Empty folders (no files anywhere below them) -> quarantine.
"""
import csv, re, sys
from collections import defaultdict

DEVICE = re.compile(r"^(?P<base>.+?)-(?P<device>[A-Z0-9][A-Z0-9-]{2,})(?P<ext>\.[^.]+)?$")  # OneDrive appends -DEVICENAME

def original_name(name):
    m = DEVICE.match(name)
    return (m["base"] + (m["ext"] or ""), m["device"]) if m else (name, None)

def main(src, out):
    rows = list(csv.DictReader(open(src, encoding="utf-8")))
    files = [r for r in rows if r["type"] == "file"]
    folders = [r for r in rows if r["type"] == "folder"]
    plan = {}

    # A. exact duplicates by content hash
    by_hash = defaultdict(list)
    for f in files:
        if f["quickXorHash"]:
            by_hash[(f["quickXorHash"], f["size"])].append(f)
    for group in by_hash.values():
        if len(group) < 2:
            continue
        group.sort(key=lambda f: (original_name(f["name"])[1] is None, f["modified"]), reverse=True)
        keeper = group[0]
        plan[keeper["id"]] = ("KEEP", "newest copy of identical content", "")
        for d in group[1:]:
            plan[d["id"]] = ("QUARANTINE", "identical content", keeper["path"])

    # B. device-suffixed conflict copies with different content
    by_folder_name = {(f["path"].rsplit("/", 1)[0], f["name"].lower()): f for f in files}
    for f in files:
        base, device = original_name(f["name"])
        if not device or f["id"] in plan:
            continue
        twin = by_folder_name.get((f["path"].rsplit("/", 1)[0], base.lower()))
        if twin and twin["quickXorHash"] != f["quickXorHash"]:
            newer = f if f["modified"] > twin["modified"] else twin
            plan[f["id"]] = ("REVIEW", f"sync conflict from device {device}; content differs", twin["path"])
            plan.setdefault(twin["id"], ("REVIEW", f"original of a conflict copy; newer = {newer['name']}", f["path"]))

    # C. empty folders: no file anywhere underneath
    file_paths = [f["path"] for f in files]
    for d in folders:
        if not any(p.startswith(d["path"] + "/") for p in file_paths):
            plan[d["id"]] = ("QUARANTINE", "empty folder (no files below it)", "")

    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "path", "type", "size", "modified", "decision", "reason", "related"])
        for r in rows:
            if r["id"] in plan:
                w.writerow([r["id"], r["path"], r["type"], r["size"], r["modified"], *plan[r["id"]]])

    q = [r for r in rows if plan.get(r["id"], ("",))[0] == "QUARANTINE"]
    gb = sum(int(r["size"] or 0) for r in q if r["type"] == "file") / 1024**3
    count = lambda d: sum(1 for v in plan.values() if v[0] == d)
    print(f"Items scanned: {len(rows)}  |  keep: {count('KEEP')}  quarantine: {count('QUARANTINE')}  "
          f"review: {count('REVIEW')}  |  space to free after quarantine expires: {gb:.2f} GB")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "data/cleanup-plan.csv")
