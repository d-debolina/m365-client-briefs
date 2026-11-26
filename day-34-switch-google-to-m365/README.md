# Day 34 · SWITCH – Scope, Wave-pilot, Import, Test, Cut over, Hand over

Moving a six-person team from Google Workspace to Microsoft 365 Business Premium with Teams: a paid discovery,
a one-user pilot while live mail stays at Google, mail with the Exchange admin center (EAC) Google Workspace batch,
files with Migration Manager, a small security baseline, a rollback that works until sign-off, and a restore you
actually prove. Built for a fictional agency (**Fabrikam Creative**).

> All people, clients, domains, sizes and links here are fictional. Practise in a trial tenant first.

## What's inside
| Path | What it is |
|---|---|
| `data/users.csv` | 6 people with Gmail and Drive sizes, pilot flag and device |
| `data/shared-drives.csv` | 4 shared drives → target SharePoint sites |
| `data/groups-and-aliases.csv` | Google groups and aliases → shared mailbox, distribution list, proxy address |
| `data/connected-workflows.csv` | What must keep working (client Google Ads/GA4/GTM, website form, devices…) and how to test it |
| `data/external-links.csv` | Client folders shared from Google Drive that need new links |
| `scripts/switch_plan.py` | Builds the EAC batch CSVs, Migration Manager destinations, link replacements and a readiness report |
| `out/` | Output of the script (`gmail-batch-*.csv`, `drive-destinations.csv`, `link-replacements.csv`, `readiness.txt`) |
| `tests/test_switch_plan.py` | 5 tests (one pilot user, shared drives into folders, a negative guest test per link, no blockers) |
| `docs/runbook.md` | Milestones, cutover, rollback, handover |
| `docs/security-baseline.md` | Conditional Access, Intune, Defender, sharing and backup settings for a tiny tenant |
| `docs/admin-guide-outline.md` | Handover guide outline |
| `architecture.*` | Diagram (PNG / SVG / editable DOT) |

## How to use
1. `python scripts/make_sample_data.py` (re)creates the CSVs.
2. `python scripts/switch_plan.py` writes `out/` and prints the readiness report (exit code 1 if anything is over a limit).
3. `python -m pytest tests` checks the rules.
4. Follow `docs/runbook.md`. Limits and prices in the script were checked on Microsoft Learn in Nov 2026; re-check them.
