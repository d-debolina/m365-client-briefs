"""Simulates one HAUL run per PC against sample/pm-folder-snapshot.csv, using the same rules as
Invoke-Haul.ps1: top-level files only, modified in the last N days, skip if the SHA-256 matches the
state file, locked files retried later, files > 10 MiB go through an upload session.
Use it to explain the logic (and to sanity-check rule changes) without touching a tenant."""
import csv, json, pathlib, sys
from datetime import datetime, timedelta

HERE = pathlib.Path(__file__).resolve().parents[1] / "sample"
NOW = datetime(2026, 11, 20, 9, 0)
SIMPLE_LIMIT = 10 * 1024 * 1024
CHUNK = 320 * 1024 * 16

def plan(rows, state, max_age_days=3, now=NOW):
    cutoff = now - timedelta(days=max_age_days)
    out = []
    for r in rows:
        rel = r["path"].split("\\PM\\", 1)[1]
        if "\\" in rel:
            continue                                        # sub-folder: never processed
        if datetime.fromisoformat(r["modified"]) < cutoff:
            continue                                        # too old
        key = f'{r["pc"]}|{r["path"]}'
        if r["locked"] == "yes":
            out.append((r, "LOCKED – retry next run")); continue
        if state.get(key) == r["sha256"]:
            out.append((r, "UNCHANGED – skipped")); continue
        size = int(r["size_bytes"])
        how = "simple PUT" if size <= SIMPLE_LIMIT else f"upload session, {-(-size // CHUNK)} chunks"
        out.append((r, f"UPLOAD ({how}) -> PM/{r['pc']}/{r['name']}"))
    return out

def exit_code(results):
    return 1 if any(a.startswith("LOCKED") for _, a in results) else 0

if __name__ == "__main__":
    rows = list(csv.DictReader(open(HERE / "pm-folder-snapshot.csv")))
    state = json.loads((HERE / "state-before.json").read_text())
    res = plan(rows, state)
    for pc in sorted({r["pc"] for r in rows}):
        mine = [(r, a) for r, a in res if r["pc"] == pc]
        print(f"\n{pc}  (exit code {exit_code(mine)})")
        for r, a in mine:
            print(f"  {r['name']:<34} {a}")
    up = sum(a.startswith("UPLOAD") for _, a in res)
    print(f"\nTotal: {up} to upload, {sum(a.startswith('UNCHANGED') for _, a in res)} unchanged, "
          f"{sum(a.startswith('LOCKED') for _, a in res)} locked")
    sys.exit(0)
