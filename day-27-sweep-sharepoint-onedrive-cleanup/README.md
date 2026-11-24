# Day 27 · SWEEP: Scan, Weigh, Elect, Evacuate, Prove

Cleaning up ~1.5 TB of SharePoint and OneDrive after sync problems created duplicate files and empty folders:
inventory with Microsoft Graph, decide by content hash (not by name), keep the newest copy, quarantine instead
of deleting, and prove what was done.

| File | What it is |
|---|---|
| `scripts/export_inventory.py` | Read-only Graph **delta** export of one drive to CSV (rebuilds paths from parent ids, honours Retry-After) |
| `scripts/find_duplicates.py` | Builds the KEEP / QUARANTINE / REVIEW plan: identical content, `-DEVICENAME` conflict copies, empty folders |
| `scripts/apply_plan.py` | Moves QUARANTINE items into a quarantine folder (dry run by default, logs every move) |
| `scripts/make_sample.py` | Generates the fictional sample inventory |
| `data/sample-inventory.csv` | 97 fictional items (Contoso Landscaping) with planted duplicates |
| `data/cleanup-plan.csv` | The plan generated from the sample |
| `runbook/cleanup-runbook.md` | Step-by-step runbook with the safety rules |
| `architecture.png` / `.svg` / `.dot` | Diagram |

## Quick start (no tenant needed)
```bash
python scripts/make_sample.py
python scripts/find_duplicates.py data/sample-inventory.csv data/cleanup-plan.csv
python scripts/apply_plan.py DRIVE-ID QUARANTINE-FOLDER-ID data/cleanup-plan.csv   # dry run
```
In a real (test) tenant, put a delegated Graph token with the right Files permissions in `GRAPH_TOKEN`.
Run against a copy first. All names and data are fictional.
