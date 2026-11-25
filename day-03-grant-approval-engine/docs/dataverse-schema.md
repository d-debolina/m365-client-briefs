# GRANT – Dataverse schema (prefix `grt_`)

All tables live in one solution, **GRANT Platform**, so they move Dev → Prod as a managed solution.
The 16 forms only add their own *request detail* tables; everything below is shared.

## Shared platform tables
| Table | Key columns | Notes |
|---|---|---|
| `grt_form` | code, name, release, process (choice), numbering format, budget check (yes/no) | One row per form. New form = new row + detail table + parent flow |
| `grt_request` | number (autonumber), form, requester, department, project, budget line, amount, status, current stage, return count | **One header table for every form.** Status: Draft · Submitted · In approval · Returned · Approved · Rejected · Cancelled |
| `grt_approvalrule` | process, department, project, min/max amount, stage, approver role, on reject (return / reject), active | The approval matrix. Admins edit rows, never flows |
| `grt_roleholder` | role, department, holder (user), alternate (user) | Roles are resolved to people at run time. No emails in flows |
| `grt_delegation` | delegator, delegate, start, end, reason | Out-of-office cover, applied before the alternate |
| `grt_approvalstep` | request, stage, role, approver, outcome, comments, assigned on, responded on, escalated (yes/no) | **The audit log.** One row per stage per attempt, never updated after the response |
| `grt_budgetline` | code, grant, description, budget | One row per donor budget line |
| `grt_commitment` | budget line, request, amount, type (commitment / actual), status | Reserved when a PR/TA is approved, turned into actual when the PV is paid |
| `grt_setting` | key, value, description | Reminder and escalation hours, per diem rates, quote limits |

Budget available = budget − sum(open commitments) − sum(actuals). Use **rollup columns** on `grt_budgetline` for the
two sums (they refresh on a schedule, so the flow also recalculates on submit to avoid a race).

## Request detail tables (examples)
| Table | Columns |
|---|---|
| `grt_leave` | request, leave type, from, to, days, cover person |
| `grt_travelauth` | request, destination, purpose, from, to, per diem type, advance needed |
| `grt_purchasereq` | request, items (child table `grt_purchaseline`), delivery location, quotes needed |
| `grt_paymentvoucher` | request, payee, invoice no., PO link, GRN link, payment method |

## Numbering
Every `grt_request` gets an **autonumber** column (`GR-{SEQNUM:6}`) and each detail table carries the form-specific
number from `grt_form.numbering format` (for example `PO-{SEQNUM:6}`). Autonumber seeds are **not** carried in
solutions: run `SetAutoNumberSeed` in production after the first import if numbers must continue from a legacy system.
Autonumbers can have gaps (a started-then-cancelled record burns a number), so tell auditors that up front.

## Security roles
| Role | Can |
|---|---|
| GRANT Requester | Create own requests, read own requests and steps |
| GRANT Approver | Read requests assigned to them (via `grt_approvalstep`), respond |
| GRANT Finance | Read all requests, budget lines, commitments |
| GRANT Admin | Edit matrix, role holders, delegations, settings, forms |
