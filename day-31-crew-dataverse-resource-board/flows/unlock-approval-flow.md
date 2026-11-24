# CREW · Flows

## 1. Unlock gate (Teams + Outlook approval)
Trigger: **Dataverse – When a row is added** on `crew_unlockrequest` (columns: project, reason, requested by, hours needed).
The custom page's **Request unlock** button just creates this row.

1. **Get a row by ID** – the project, to find the yard's planning lead (lookup on the business unit).
2. **Approvals – Start and wait for an approval**, type *Approve/Reject – First to respond*,
   assigned to the planning lead. Title: `Unlock <project> for <hours> h?` Details: reason + the tasks that will change.
   The approval appears in Teams (Approvals app + chat card) and Outlook (actionable message).
3. **Condition** outcome = Approve
   - Yes: **Update a row** `crew_project.crew_unlockeduntil` = `addHours(utcNow(), hours)`;
     update the request to *Approved*; post in the project channel.
   - No: update the request to *Rejected* with the comment.
4. The `LockGuard` plug-in reads `crew_unlockeduntil`, so edits work only inside the window.
   A nightly flow (below) re-checks that windows have closed.

> Use a **connection reference** for Dataverse and Approvals, and an environment variable for the channel ID,
> so the same flow deploys from Dev to Test to Prod without edits.

## 2. Rule-driven notifications
Table `crew_notificationrule` (table, condition column, operator, value, recipients group, template).
A **When a row is added, modified or deleted** flow per watched table filters with the rule rows and sends
**Office 365 Outlook – Send an email (V2)**. New rules don't need a new flow.

## 3. Nightly checks and weekly snapshots
- **Recurrence** 02:00 – list tasks where `crew_enddate` < today and status ≠ Done → set *Late*;
  list projects with `crew_unlockeduntil` in the past → clear it.
- **Recurrence** Sunday 22:00 – call the custom API `crew_RecalculateDemand` (no scenario), then copy
  `crew_weeklycapacity` rows into `crew_capacitysnapshot` with the snapshot date (for trend charts).

## 4. Excel / SharePoint imports through staging
1. **SharePoint – When a file is created** in *CREW Imports* → **Excel – List rows present in a table**.
2. For each row, **Add a row** to `crew_importstaging` with the raw JSON.
3. A synchronous plug-in (or a child flow) validates: required columns, crew ID exists, week is a Monday,
   hours ≤ 60. Valid → upsert into the real table by alternate key; invalid → status *Error* with the reason.
4. Email the uploader a summary: `n` imported, `m` rejected, link to the staging view.
