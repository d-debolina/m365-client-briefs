"""Evidence integrity: hash every item before AND after import and compare. Usage:
   python scripts/integrity_manifest.py archive-export/items.json > manifest.csv
Re-run against the export from Purview (normalised to the same fields) and diff the two manifests.
"""
import json, sys, hashlib, csv
FIELDS = ["archiveId", "from", "to", "sentUtc", "subject", "body", "attachments"]
items = json.load(open(sys.argv[1], encoding="utf-8"))
w = csv.writer(sys.stdout); w.writerow(["archiveId", "sha256_recomputed", "sha256_source", "match", "custodians", "attachments"])
bad = 0
for it in items:
    h = hashlib.sha256(json.dumps({k: it[k] for k in FIELDS}, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    ok = h == it.get("sha256"); bad += not ok
    w.writerow([it["archiveId"], h, it.get("sha256"), ok, ";".join(it["custodians"]), len(it["attachments"])])
print(f"# {len(items)} items, {bad} mismatches", file=sys.stderr)
