# Day 9 · SHELF: Sync, Health, Explorer & Library Fixes

The client moved a file server to SharePoint and hit 7 problems. This folder has a readiness scanner,
tenant settings and a checklist.

| File | What it is |
|---|---|
| `data/fileshare-inventory.csv` | 6,000 fictional file-server entries (paths, sizes, dates) |
| `scripts/readiness_scan.py` | Flags long paths, bad characters, deep folders, PST/Access files, stale content |
| `scripts/tenant-settings.ps1` | Hide the Sync button + Restricted Content Discovery |
| `checklist.md` | The migration readiness checklist from the post |

Run: `python scripts/readiness_scan.py data/fileshare-inventory.csv > report.md`
