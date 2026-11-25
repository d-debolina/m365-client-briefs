r"""SHELF readiness scan: flags file-server content that will hurt in SharePoint/OneDrive.
Usage: python readiness_scan.py ../data/fileshare-inventory.csv > report.md
Export a real inventory with:  Get-ChildItem \\server\share -Recurse -File |
  Select FullName,Extension,@{n='size_mb';e={[math]::Round($_.Length/1MB,2)}},LastWriteTime | Export-Csv inventory.csv
"""
import csv, sys, collections, datetime
SITE_PREFIX = "https://contoso.sharepoint.com/sites/finance/Shared Documents/"   # roughly what each path becomes
BAD_CHARS = set('"*:<>?/\\|')
NOT_FOR_SHAREPOINT = {".pst": "Outlook archive: move to Exchange Online archive", ".mdb": "Access DB: rebuild in Dataverse/Lists or keep on a file share",
                      ".tmp": "temp file: delete"}
issues = collections.defaultdict(list); by_dept = collections.Counter(); stale = 0; total_mb = 0
today = datetime.date(2026, 11, 20)
rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
for r in rows:
    p = r["path"]; rel = p.split("\\Shares\\", 1)[-1].replace("\\", "/")
    name = rel.rsplit("/", 1)[-1]; size = float(r["size_mb"]); total_mb += size; by_dept[r["department"]] += 1
    if len(SITE_PREFIX + rel) > 400: issues["Path longer than 400 characters after migration"].append(p)
    if any(c in BAD_CHARS for c in name) or name != name.strip(): issues["Invalid character or leading/trailing space"].append(p)
    if rel.count("/") > 8: issues["Folder depth over 8 (hard to find on iPad / in search)"].append(p)
    if r["extension"] in NOT_FOR_SHAREPOINT: issues[NOT_FOR_SHAREPOINT[r["extension"]]].append(p)
    if size > 2000: issues["Files over 2 GB (slow to open/sync; consider Stream or archive)"].append(p)
    if (today - datetime.date.fromisoformat(r["last_modified"])).days > 3*365: stale += 1
print("# SHELF readiness report\n")
print(f"Files scanned: **{len(rows):,}** · total size **{total_mb/1024:,.1f} GB** · untouched for 3+ years: **{stale:,}** ({stale/len(rows):.0%}) → archive candidates\n")
print("| Issue | Files | Example |\n|---|---|---|")
for k, v in sorted(issues.items(), key=lambda kv: -len(kv[1])):
    print(f"| {k} | {len(v):,} | `{v[0][-70:]}` |")
print("\n## Files per department (one library each, keep each sync scope well under 300k items)\n")
for d, c in by_dept.most_common(): print(f"- {d}: {c:,}")
