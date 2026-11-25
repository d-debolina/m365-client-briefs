# Day 30 · CREW – Capacity, Resources, Equipment & Weeks

A Dataverse resource-planning app for a construction-style business: crews by week, a two-week look-ahead,
what-if scenarios and an equipment rental forecast. The point of the post is the part most builds get wrong:
**a locked plan stays locked even when someone edits it in Excel, through the API or with an import**, because
the rule lives in a Dataverse plug-in, not in the app. The planning maths sits in a small engine with
acceptance tests that have expected numbers.

> All projects, people, rates and dates are fictional. Use a developer environment.

## What's inside
| Path | What it is |
|---|---|
| `data/*.csv` | 15 projects, 36 crew members, 26 weeks of demand by skill and equipment, leave, fleet, holidays, 20 look-ahead tasks |
| `scripts/make_data.py` | Regenerates the CSVs. `python scripts/make_data.py 2027-03-01` moves the plan to another Monday |
| `schema/schema.md` | Core tables, ownership and the security model (Entra group teams, access team template) |
| `plugins/LockGuard.cs` | PreValidation plug-in that blocks edits and deletes on locked tasks from any client |
| `plugins/WorkdayMath.cs` | PreOperation plug-in that sets the end date in working days (skips weekends and holidays) |
| `engine/planning_engine.py` | Weekly demand vs supply by skill, rentals, workday maths (pure Python) |
| `engine/test_planning_engine.py` | Acceptance tests with expected numbers |
| `engine/function_app.py` | Azure Function sketch that runs the engine against the Dataverse Web API (managed identity) |
| `flows/unlock-approval-flow.md` | Unlock gate in Teams/Outlook, rule-driven notifications, nightly checks, staging imports |
| `alm/pipelines-and-env-vars.md` | Three solutions, environment variables, Dev → Test → Prod pipeline, managed environment rules |
| `architecture.*` | Diagram (PNG / SVG / editable DOT) |

## How to use
1. `python scripts/make_data.py` and `python engine/planning_engine.py` to see the gap report.
2. `python -m unittest discover -s engine -p "test_*.py"` to run the acceptance tests.
3. Create the tables from `schema/schema.md` in a dev environment and import the CSVs.
4. Build the plug-ins (PAC CLI `pac plugin init`, add the two classes), register the steps as described in the
   file headers, then try to edit a locked task in the app **and** in *Edit in Excel*. Both are blocked.
5. Build the unlock flow from `flows/unlock-approval-flow.md` and approve an unlock in Teams.
6. Optional: deploy `engine/function_app.py` and wire the custom API `crew_RecalculateDemand` to it.
