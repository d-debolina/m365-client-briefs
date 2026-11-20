# Day 13 · MOVER: Map, Organise, Verify, Export, Redirect

Plan and migrate a WordPress intranet to SharePoint Online with native features only.

| File | What it is |
|---|---|
| `inventory/wp-content-inventory.csv` | 420 fictional WordPress posts/pages with views, age and a triage decision |
| `inventory/triage-summary.md` | Archive / auto-migrate / rewrite counts |
| `mapping/wp-to-sharepoint-mapping.md` | Concept mapping, "surface without duplication", 4 page templates |
| `mapping/termset-intranet-topics.csv` | Term set in SharePoint term store import format |
| `wp-export-sample/wp-json-posts.json` | Sample WordPress REST API export |
| `scripts/transform.py` | WP JSON → page manifest + redirect map |
| `scripts/Create-Pages.ps1` | PnP PowerShell: create pages, set Topic, promote news, publish (idempotent) |
| `estimate.md` | Team split and effort estimate |
