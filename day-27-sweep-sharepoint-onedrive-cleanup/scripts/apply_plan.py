"""SWEEP step 3: move QUARANTINE items into a _SWEEP-Quarantine folder (dry run by default).

    python scripts/apply_plan.py <drive-id> <quarantine-folder-id> data/cleanup-plan.csv            # dry run
    GRAPH_TOKEN=... python scripts/apply_plan.py <drive-id> <quarantine-folder-id> data/cleanup-plan.csv --go

Moving (not deleting) keeps version history; apply-log.csv records each original path and lets anyone restore a file by moving it back.
Delete the quarantine folder only after the agreed waiting period and sign-off; deleted items then
sit in the recycle bin for up to 93 days, unless retention or holds keep them longer.
REVIEW rows are never touched.
"""
import csv, json, os, sys, time, urllib.request

def move(drive, item, name, target, token):
    # Duplicates often share a name, so prefix the item id to keep every name unique in quarantine.
    body = json.dumps({"parentReference": {"id": target}, "name": f"{item[-8:]}_{name}"}).encode()
    req = urllib.request.Request(f"https://graph.microsoft.com/v1.0/drives/{drive}/items/{item}", data=body,
                                 method="PATCH", headers={"Authorization": f"Bearer {token}",
                                                          "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        return r.status

def main(drive, target, plan, go=False):
    rows = [r for r in csv.DictReader(open(plan, encoding="utf-8")) if r["decision"] == "QUARANTINE"]
    rows.sort(key=lambda r: r["type"] == "folder")          # files first, folders last
    token = os.environ.get("GRAPH_TOKEN") if go else None
    w = csv.writer(open("data/apply-log.csv", "a", newline="", encoding="utf-8")) if go else None
    for r in rows:
        if not go:
            print(f"DRY RUN  would move {r['path']}")
            continue
        try:
            status = move(drive, r["id"], r["path"].rsplit("/", 1)[-1], target, token)
        except Exception as e:                               # log and carry on; re-run picks up the rest
            status = f"error: {e}"
        w.writerow([time.strftime("%Y-%m-%dT%H:%M:%S"), r["id"], r["path"], status])
        time.sleep(0.2)                                      # be gentle: avoid throttling
    print(f"{len(rows)} items {'moved' if go else 'listed (dry run)'}")

if __name__ == "__main__":
    a = sys.argv[1:]
    main(a[0], a[1], a[2], go="--go" in a)
