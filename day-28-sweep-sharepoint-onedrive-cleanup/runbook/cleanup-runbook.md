# SWEEP cleanup runbook (1.5 TB, SharePoint + OneDrive)

## Before you touch anything
1. **Stop the cause.** Make sure every PC runs a current OneDrive sync app; fix the PCs that create `-DEVICENAME` copies (cached credentials, files edited offline on two devices). Otherwise duplicates come back.
2. **Check retention and holds** with the compliance owner. Under a retention policy, deleted files are copied to the Preservation Hold library and still use storage.
3. **Agree the rules in writing** with the client: what counts as a duplicate, which copy wins, how long quarantine lasts (we suggest 30 days), who signs off.
4. **Backup?** If Microsoft 365 Backup or a third-party backup exists, confirm the last good restore point.

## Run
| Step | Command / action | Output |
|---|---|---|
| 1 Inventory | `export_inventory.py <drive-id>` per library / OneDrive | `inventory.csv` |
| 2 Plan | `find_duplicates.py inventory.csv cleanup-plan.csv` | KEEP / QUARANTINE / REVIEW |
| 3 Review | Client checks the REVIEW rows (conflict copies with different content) and merges by hand | Signed-off plan |
| 4 Quarantine | `apply_plan.py <drive> <quarantine-folder> cleanup-plan.csv` (dry run), then `--go` | `apply-log.csv` |
| 5 Wait | 30 days; anyone missing a file asks, we move it back | |
| 6 Delete | Delete the quarantine folder after sign-off | Recycle bin (93 days) |
| 7 Versions | Version storage usage report + what-if, then trim if agreed | Storage freed |
| 8 Report | Before/after: items, GB, duplicates removed, open REVIEW items | One-page report |

## Never
- Never delete REVIEW items automatically.
- Never empty the second-stage recycle bin just to free space on day one.
- Never edit or delete files in the Preservation Hold library.
