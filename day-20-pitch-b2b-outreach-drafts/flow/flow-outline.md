# PITCH flow (Power Automate, manual or scheduled)

1. **Trigger:** Manually trigger a flow (button) or Recurrence (weekdays 08:00)
2. **List rows present in a table** (Excel Online Business): `prospects.xlsx` → table `Prospects`, filter `Status eq 'New'`, top 20
3. **List rows** from table on sheet *Offer* → Compose `Offer` JSON
4. **Apply to each** prospect (concurrency 1–5):
   1. **Run a prompt** `draft-outreach` (JSON output)
   2. **Condition** `skip` = true → Update row: Status = "Skipped (DNC)" → continue
   3. **Outlook: Draft an email message** to the prospect (NOT send) with subject/body
   4. **Update a row**: Status = "Draft ready", DraftCreated = utcNow(), store risk_flags
5. **Teams message** to the sender: "12 drafts ready in Outlook Drafts, 3 flagged for review"

Human in the loop: the salesperson opens Outlook Drafts, edits, and sends. The flow never sends.
