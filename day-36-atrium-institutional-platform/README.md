# Day 36 · ATRIUM – Approvals, Templates, Records, Institutional knowledge, Unified hubs, Modules

A blueprint for running a whole institution (two entities, one tenant, Arabic and English) on SharePoint
Online and Power Platform, plus the first module built end to end: a bilingual correspondence register with
gap-free reference numbers (`OUT-CI-2027-00042`) and the shared approval engine every other module reuses.
Built for a fictional organisation (**Contoso Institute** and its commercial arm **Contoso Services**).

> All organisations, people, letters and parties here are fictional. Use a trial tenant.

## What's inside
| Path | What it is |
|---|---|
| `data/modules.csv` | 18 modules in 5 groups: where each lives, its store, automation, licence need and phase |
| `data/sites.json` | Six hubs, their sites, languages and how the two entities are split |
| `data/approval-matrix.csv` | Doc type × entity → approval stages and escalation days |
| `data/correspondence-drafts.csv` | 30 fictional letters and memos with English and Arabic subjects |
| `scripts/reference_numbers.py` | Simulates the SharePoint `Counters` list with ETag checks; writes `out/correspondence-register.csv` |
| `scripts/build_plan.py` | Turns `modules.csv` into `out/build-order.md` (phases + licence note) |
| `tests/test_atrium.py` | 5 tests, incl. 20 people issuing numbers at the same moment → unique, gap-free |
| `docs/architecture-one-pager.md` | The one-page architecture clients ask for in the proposal |
| `docs/correspondence-module.md` | List schema and the *Issue reference* flow, step by step |
| `docs/rtl-checklist.md` | Arabic / RTL checks for pages, forms, apps and exports |
| `architecture.*` | Diagram (PNG / SVG / editable DOT) |

## How to use
1. `python scripts/make_sample_data.py` (re)creates the data.
2. `python scripts/reference_numbers.py` and `python scripts/build_plan.py` write `out/`.
3. `python -m pytest tests` runs the checks.
4. Build the Correspondence site from `docs/correspondence-module.md`. Limits and prices were checked on
   Microsoft Learn and Microsoft's pricing pages on 27 Nov 2026; re-check them.
