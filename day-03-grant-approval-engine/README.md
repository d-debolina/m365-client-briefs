# Day 3 · GRANT – Generic Routing, Approvals, Numbering & Tracking

One reusable approval engine on Dataverse and Power Automate, with many thin forms on top. Approvers, thresholds,
delegations and budget lines live in tables that admins edit, so adding form 17 doesn't mean touching the engine.
Built for a fictional humanitarian nonprofit (**Contoso Relief Foundation**) with 16 HR, travel, procurement, finance
and asset forms.

> All people, grants, budget lines and amounts here are fictional. Test in a trial or sandbox environment first.

## What's inside
| Path | What it is |
|---|---|
| `data/forms-catalogue.csv` | The 16 forms, release, process and numbering format |
| `data/approval-matrix.csv` | The approval matrix: process × department × project × amount → stages and roles |
| `data/role-holders.csv`, `data/delegations.csv` | Who holds each role (with an alternate), and time-boxed out-of-office cover |
| `data/settings.csv` | Reminder/escalation hours, return limit, per diem and quote limits |
| `data/budget-lines.csv` | Grant budget lines with budget, committed and actual spend |
| `data/sample-requests.csv` | 8 requests to replay through the engine |
| `scripts/grant_engine.py` | The routing, delegation and budget rules in plain Python (same logic as the child flow) |
| `tests/test_grant_engine.py` | 6 tests: stages by amount, project rules, budget block, delegation window, no self-approval |
| `docs/dataverse-schema.md` | Tables, numbering and security roles |
| `docs/approval-engine-flows.md` | Parent flow, child flows, reminders/escalation, ALM and ownership |
| `docs/handover-exercise.md` | The "build form 17 yourselves" exercise for the client's staff |
| `architecture.*` | Diagram (PNG / SVG / editable DOT) |

## How to use
1. `python scripts/make_sample_data.py` (re)creates the CSVs.
2. `python scripts/grant_engine.py` shows the route each sample request would take, including delegations and
   budget blocks. Change the matrix and run it again: this is the cheapest way to agree rules with Finance.
3. `python -m pytest tests` checks the rules.
4. Import the CSVs into the `grt_` tables (Dataverse → Import from CSV) and build the flows from
   `docs/approval-engine-flows.md`.
