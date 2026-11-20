# TALLY flows (standard connectors only)

1. **Monday reminder** (Recurrence, Mon 08:00): Get items where Status not in (Passed, N/A) and DueDate ≤ next Friday →
   group by Owner (Select + union of emails) → one Teams chat message per owner with their list.
2. **Failed/blocked alert** (When an item is created or modified + trigger condition `Status eq 'Failed' or 'Blocked'`) →
   post adaptive card in the Migration channel with Workload, Check, Severity, Owner.
3. **Go/no-go snapshot** (manual button before each wave cutover) → count Passed/total per workload → create a news post or
   Teams message "Payroll API: 10/10 ✅ · CRM sync: 8/10 ⛔ (2 failed)".
