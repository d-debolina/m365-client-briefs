# Day 29 · NUDGE – Next steps, Updates, Due dates, Gentle follow-ups, Evidence

A Copilot Studio agent that tells field sales reps what to do next on an account – **without a CRM**.
Three SharePoint lists act as a "CRM-lite", the agent saves the things reps promise ("a proctorship in
two months"), and a daily cloud flow asks the rep in Teams how it went when the date comes round.

> All accounts, people and events are fictional. Use a developer tenant.

## What's inside
| Path | What it is |
|---|---|
| `data/accounts.csv` | 12 fictional hospital accounts with owner, stage and key surgeon |
| `data/commitments.csv` | 27 commitments (proctorships, in-services, evaluations…) with follow-up dates; 3 are due on the demo day |
| `data/activities.csv` | 60 past calls, visits and emails |
| `scripts/make_data.py` | Regenerates the CSVs. `python scripts/make_data.py 2027-04-01` shifts the demo "today" |
| `lists/schema.md` | Columns for the three SharePoint lists, with the indexes you need |
| `scripts/create-lists.ps1` | PnP PowerShell that creates the lists (bring your own Entra app ClientId) |
| `agent/agent-instructions.md` | Instructions to paste into Copilot Studio |
| `agent/playbook.md` | Fictional sales playbook used as the agent's knowledge |
| `flow/follow-up-flow.md` | Step-by-step daily follow-up cloud flow |
| `flow/follow-up-card.json` | The Adaptive Card the rep answers in Teams |
| `architecture.*` | Diagram (PNG / SVG / editable DOT) |

## How to use
1. Create a SharePoint site and run `scripts/create-lists.ps1`.
2. Paste the CSV rows into the lists (grid view) or import them with PnP.
3. In Copilot Studio (standard harness – proactive Teams messages need it), create **NUDGE**, paste
   `agent/agent-instructions.md`, add `agent/playbook.md` as knowledge and add the SharePoint connector
   actions *Get items*, *Create item* and *Update item* as tools.
4. Publish to Teams and install the agent for the reps.
5. Build the cloud flow from `flow/follow-up-flow.md`.
