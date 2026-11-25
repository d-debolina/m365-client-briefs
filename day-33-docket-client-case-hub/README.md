# Day 33 · DOCKET – Document sets, Oversight, Cases, Keys, External access, Tracking

A client, retainer and case hub for a small professional services firm, built on SharePoint Online, Microsoft Lists,
Power Automate (standard connectors) and Power BI. One document set per case, an ethical wall for restricted cases,
a separate site for client collaboration with expiring guest access, and a dashboard that shows who's overloaded.
Built for a fictional 20-person firm (**Fabrikam Advisory**).

> All clients, people, cases and fees here are fictional. Test in a trial tenant first.

## What's inside
| Path | What it is |
|---|---|
| `data/clients.csv`, `data/retainers.csv` | 12 clients and 5 retainers |
| `data/cases.csv` | 30 cases (5 restricted, 6 with external collaboration, some closed / on hold) |
| `data/staff.csv`, `data/allocations.csv` | 10 fee earners with weekly capacity and planned hours per case |
| `data/external-contacts.csv` | Client contacts with access level and expiry |
| `scripts/docket_plan.py` | Permission plan per case, unique-scope check, allocation table for Power BI |
| `out/permission-plan.csv`, `out/allocation-dashboard.csv` | Output of the script |
| `tests/test_docket_plan.py` | 5 tests (restricted cases only break inheritance, no guests in Case files, flags) |
| `docs/site-architecture.md` | Sites, lists, document set content type, permission matrix, external sharing |
| `docs/flows.md` | New case, retainer hours and guest review flows |
| `docs/powerbi-dashboard.md` | Pages, DAX measures and dataset security |
| `architecture.*` | Diagram (PNG / SVG / editable DOT) |

## How to use
1. `python scripts/make_sample_data.py` (re)creates the CSVs.
2. `python scripts/docket_plan.py` writes the permission plan and the allocation table, and prints the scope check.
3. `python -m pytest tests` checks the rules.
4. Build the sites from `docs/site-architecture.md`, import the CSVs into the lists, then build the flows.
