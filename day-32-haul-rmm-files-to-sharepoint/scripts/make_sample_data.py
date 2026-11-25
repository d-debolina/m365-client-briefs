"""Generates fictional HAUL sample data: what sits in the PM folder on 4 client PCs, and the state file
from the previous run. Everything is invented (Fabrikam / Contoso style)."""
import csv, json, hashlib, pathlib, random
from datetime import datetime, timedelta

random.seed(31)
HERE = pathlib.Path(__file__).resolve().parents[1] / "sample"
NOW = datetime(2026, 11, 20, 9, 0)            # the simulated "run time"
PCS = ["FAB-RECEPTION-01", "FAB-SURGERY-02", "FAB-OFFICE-03", "FAB-SRV2016"]
KINDS = ["daysheet", "recall-list", "ledger-export", "claims-batch", "appointments"]

rows = []
for pc in PCS:
    for i in range(6):
        kind = random.choice(KINDS)
        age_h = random.choice([2, 5, 20, 30, 50, 70, 90, 140, 400])
        mod = NOW - timedelta(hours=age_h)
        size = random.choice([18_000, 240_000, 1_200_000, 4_800_000, 14_500_000])
        name = f"{kind}-{mod:%Y%m%d}-{i}.csv" if kind != "claims-batch" else f"{kind}-{mod:%Y%m%d}-{i}.zip"
        sha = hashlib.sha256(f"{pc}{name}v1".encode()).hexdigest().upper()
        rows.append({"pc": pc, "path": f"C:\\Fabrikam\\PM\\{name}", "name": name, "size_bytes": size,
                     "modified": mod.isoformat(timespec="minutes"), "sha256": sha,
                     "locked": "yes" if (pc == "FAB-SURGERY-02" and i == 1) else "no"})
# one file inside a sub-folder that must be ignored
rows.append({"pc": "FAB-OFFICE-03", "path": "C:\\Fabrikam\\PM\\archive\\daysheet-20261119-9.csv",
             "name": "daysheet-20261119-9.csv", "size_bytes": 20_000, "modified": (NOW - timedelta(hours=10)).isoformat(timespec="minutes"),
             "sha256": "SUBFOLDER", "locked": "no"})

with open(HERE / "pm-folder-snapshot.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

# previous run already uploaded some of the recent files (same hash) and one file that has since changed
state = {}
for r in rows:
    if r["sha256"] == "SUBFOLDER": continue
    age = (NOW - datetime.fromisoformat(r["modified"])).total_seconds() / 3600
    if 20 <= age <= 72 and random.random() < 0.6:
        state[f'{r["pc"]}|{r["path"]}'] = r["sha256"]
changed = next(r for r in rows if r["pc"] == "FAB-RECEPTION-01" and r["sha256"] != "SUBFOLDER"
               and 0 < (NOW - datetime.fromisoformat(r["modified"])).total_seconds() / 3600 <= 72)
state[f'{changed["pc"]}|{changed["path"]}'] = "OLDHASH-FILE-WAS-EDITED-SINCE"
(HERE / "state-before.json").write_text(json.dumps(state, indent=2))
print(f"{len(rows)} files, {len(state)} state entries -> {HERE}")
