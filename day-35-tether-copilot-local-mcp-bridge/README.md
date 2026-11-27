# Day 35 · TETHER – Tunnelled, Entra-Trusted Host Execution Relay

Bringing a Windows app's existing MCP server to Microsoft 365 Copilot and Copilot Studio, without opening a single
inbound port on the customer's machine: API Management checks the user's Entra ID token, Azure Relay carries the
call to a small bridge service that dials out on 443, and the bridge only lets through tools the user's role
allows, inside approved workspaces, with a two-step confirmation for anything that changes data.
Built around a fictional product (**Fabrikam Automate**) and fictional customers (**Contoso**, **Northwind**).

> All people, customers, tools and keys here are fictional. Use a trial tenant and a throwaway Azure subscription.

## What's inside
| Path | What it is |
|---|---|
| `data/tools.json` | The 5 MCP tools with `readOnlyHint` / `destructiveHint` annotations |
| `data/users.csv` | 4 fictional users, their customer and role (Reader / Operator / Admin) |
| `data/policy.json` | Role → tools, customer → workspaces, approved scripts, confirmation timeout |
| `scripts/tether_gate.py` | The bridge's policy gate: role-filtered `tools/list`, workspace and path fences, two-step confirmation codes bound to user + arguments, audit log |
| `tests/test_gate.py` | 7 tests (readers never see write tools, codes expire and can't be reused for other arguments or users, customers are isolated, `..\` paths and unknown scripts are refused) |
| `bridge/apim-policy.xml` | **Untested sketch** of the API Management policy (token check, tenant → hybrid connection, SAS signing, rate limit) |
| `bridge/TetherListener.cs` | **Untested sketch** of the Windows bridge service (Azure Relay listener → localhost MCP) |
| `docs/decision-record.md` | Copilot Studio MCP vs custom connector + gateway vs declarative agent vs Copilot connector |
| `docs/it-admin-setup.md` | Setup outline for a customer IT admin |
| `out/audit-log.jsonl` | Output of the demo run |
| `architecture.*` | Diagram (PNG / SVG / editable DOT) |

## How to use
1. `python scripts/make_sample_data.py` (re)creates the data files.
2. `python scripts/tether_gate.py` prints a demo conversation (read, write with confirmation, replayed code refused, other customer's workspace refused).
3. `python -m pytest tests` runs the checks.
4. The two files in `bridge/` show the shape of the real build. They were **not compiled or deployed** here: check every policy element and SDK call against Microsoft Learn before you use them.

Feature status (Copilot Studio MCP, declarative-agent MCP plugins, federated Copilot connectors, Azure Relay limits)
was checked on Microsoft Learn on 27 Nov 2026. Re-check before you build.
