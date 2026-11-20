# Reviewed flow spec (ready to hand to Copilot in the designer, step by step)

**Goal:** Supplier invoices sent to the shared mailbox *invoices@* are filed, logged and routed for approval.

**Runs as:** connection references owned by the service account `svc-flow-finance` (not a person).

1. **Trigger:** *When a new email arrives in a shared mailbox (V2)*: mailbox `invoices@contoso.example`, folder `Inbox`,
   *Include attachments* = Yes, *Only with attachments* = Yes. Trigger condition: sender domain not internal.
2. **Filter array:** keep attachments where name ends with `.pdf`. If none → move email to `Needs review`, stop.
3. **For each PDF** (concurrency 1):
   1. **Run a prompt** `extract-invoice` (JSON: supplier, invoiceNumber, invoiceDate, currency, totalGross). Missing fields → `Needs review` list.
   2. **Get items** in list `Invoice log` where `InvoiceNumber eq '{invoiceNumber}' and Supplier eq '{supplier}'`. If found → skip (idempotent).
   3. **Create file** `/Invoices/{yyyy}/{supplier}/{invoiceNumber}.pdf`.
   4. **Create item** in `Invoice log` (Microsoft List, not Excel) with link to the file and Status = New.
4. **Condition:** `totalGross` ≥ 1,000 **EUR** (convert others using the `FX rates` list) → *Start and wait for an approval*
   to the cost-centre owner from the `Suppliers` list; fallback approver `finance-lead@`; timeout 3 days → escalate.
5. **Update item** Status = Approved/Rejected/Logged.
6. **Try/Catch:** all of the above in Scope "Try"; Scope "Catch" logs `result('Try')` + flow run URL to `Flow errors` list and posts in the Finance channel.

**Acceptance tests:** (a) PDF invoice 250 EUR → logged, no approval; (b) 4,800 EUR → approval to owner; (c) same email processed twice → one file, one item;
(d) email without PDF → Needs review; (e) unknown supplier → fallback approver.
