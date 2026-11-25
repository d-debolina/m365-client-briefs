# Day 1 · ATLAS: Annual Timeline of Leadership Activities & Schedules

A year-at-a-glance leadership calendar: a Power Apps canvas app on one SharePoint list, running as a Teams tab, on standard Microsoft 365 licences.

| File | What it is |
|---|---|
| `list/schema.md` | List columns, validation, 15 categories with colours, permission model |
| `list/sample-activities.csv` | 41 fictional activities for one year |
| `app/formulas.md` | Key Power Fx: named formulas, 3 × 4 month grid, nested gallery, "+N more", filters, details panel, form validation |
| `scripts/Create-AtlasList.ps1` | Creates both lists with PnP PowerShell and imports the sample data |
| `scripts/make_sample_data.py` | Regenerates the sample CSV |
| `handover/handover-note.md` | One-page handover template (how it works, add a category, grant edit rights) |
| `architecture.png` / `.svg` / `.dot` | Architecture diagram |

## Quick start
1. Use a developer tenant. Run `scripts/Create-AtlasList.ps1 -SiteUrl <site> -ClientId <your app id>`.
2. Break permission inheritance on the list: Read for viewers, Contribute for **ATLAS Editors**.
3. Create a blank canvas app (16:9), add the SharePoint connection to both lists, and paste the formulas from `app/formulas.md`.
4. Share the app with the leadership group, then **Publish to Teams** and add it as a tab.

All names and data are fictional.
