# Day 23 · TALLY: Track, Assign, List, Log, Yes/no-go

A Microsoft Lists tracker for validating an Azure migration: evidence-enforced checks, owner views, formatting, reminders and a go/no-go snapshot.

| File | What it is |
|---|---|
| `list/validation-items.csv` | 120 fictional checks (12 workloads × 10 checks) |
| `list/schema.md` | Columns, validation formula, 5 views |
| `formatting/*.json` | Status pills + overdue date column formatting |
| `flow/flows.md` | Monday reminder, failed/blocked alert, go/no-go snapshot |
| `scripts/Create-TallyList.ps1` | Create the list + import with PnP PowerShell |
