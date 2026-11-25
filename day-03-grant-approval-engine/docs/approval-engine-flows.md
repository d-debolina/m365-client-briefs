# GRANT – the flows

The rule: **one engine, many thin forms.** Each form has a small parent flow. All approval logic sits in three
child flows and one scheduled flow, inside the GRANT Platform solution.

## 1. Parent flow per form (thin)
Trigger: Dataverse *When a row is added or modified* on `grt_request`, filter `status eq Submitted` and `form = <code>`.
1. Call **GRANT – Resolve route** with the request ID.
2. If it returns `budget_ok = false`, set status **Returned** with the message "Only X USD left on <line>" and stop.
3. Call **GRANT – Run stage** for stage 1.
That's it. Adding form 17 means copying this flow and changing one filter value.

## 2. Child flow: GRANT – Resolve route
Inputs: request ID. Outputs: JSON array of stages, `budget_ok`, `available`.
1. Get the request and its form row.
2. If the form needs a budget check: list open commitments + actuals for the budget line, compare with the amount.
3. List `grt_approvalrule` rows for the process where min ≤ amount ≤ max and (department = request dept or `*`) and
   (project = request project or `*`). Keep the most specific row per stage.
4. For each stage: get the role holder (department first, then `*`) → active delegation? use delegate →
   requester or already used? use alternate → still invalid? return `NEEDS_ADMIN`.
5. Return the stages. (This is exactly what `scripts/grant_engine.py` does, so test the matrix there first.)

## 3. Child flow: GRANT – Run stage
Inputs: request ID, stage number, approver.
1. Add a `grt_approvalstep` row (outcome = Pending, assigned on = now).
2. **Create an approval** (Approvals connector, *Custom responses – wait for one response*) with three options:
   **Approve**, **Return for correction**, **Reject**. Put the request number, amount and a deep link to the
   back-office app in the details.
3. **Wait for an approval** immediately after (keep create and wait next to each other).
4. Update the step row with outcome, comments and responded on.
5. Switch on outcome:
   - Approve → next stage exists? call *Run stage* again : set request **Approved**, create the commitment row.
   - Return → increase return count; over `MAX_RETURNS`? Reject : set status **Returned** and notify the requester.
     When they resubmit, the parent flow starts again **from stage 1** (simplest, easiest to audit).
   - Reject → set request **Rejected**, notify requester.

Why create + wait instead of *Start and wait*? It gives you the approval ID straight away, so the scheduled flow
below can cancel and reassign it.

## 4. Scheduled flow: GRANT – Reminders and escalation (every hour)
1. List `grt_approvalstep` rows with outcome = Pending.
2. Older than `REMINDER_AFTER_HOURS` and no reminder yet → Teams message to the approver.
3. Older than `ESCALATE_AFTER_HOURS` → cancel the approval, set escalated = yes, start a new step for the
   role's **alternate**.
4. Approvals can only wait 28 days. Anything still pending after 21 days gets flagged to the GRANT admin.

## Ownership and environments
- Dev and Prod environments, both with Dataverse. Prod is a **managed environment** (needed for pipelines targets).
- Deploy with **Pipelines in Power Platform**, managed solutions only, no edits in Prod.
- In Prod, flows are owned by the client's **service principal application user**. Premium flows owned by a
  service principal need a licensed co-owner set as the flow's *user license*, or they get suspended.
- Every connection goes through a **connection reference**, and tenant-specific values (site URL, admin group)
  through **environment variables**. Approvers, thresholds and rates stay in Dataverse tables, so the client changes
  them without a deployment.
