# Migration validation list (Microsoft Lists)

| Column | Type | Settings |
|---|---|---|
| Title (renamed **ID**) | Single line | `VAL-0001` |
| Workload | Lookup → *Workloads* list | Workload owner, environment, wave live there |
| Wave | Choice | Wave 1 / Wave 2 / Wave 3 |
| Check | Choice | 10 standard checks (see CSV) |
| Owner | Person | Required |
| Status | Choice | Not started, In progress, Passed, Failed, Blocked, N/A (formatted as pills) |
| DueDate | Date | Formatted red when overdue |
| Evidence | Hyperlink | **Required when Status = Passed** (list validation formula) |
| Severity | Choice | Required when Failed/Blocked |
| Notes | Multiple lines | Append changes to existing text = Yes (audit trail) |

## List validation formula (Settings → Validation settings)
```
=IF(OR([Status]="Passed",[Status]="N/A"),NOT(ISBLANK([Evidence])),TRUE)
```
Message: "Add an evidence link before marking a check Passed or N/A."

## Views
1. **My open checks**: Owner = [Me], Status not in (Passed, N/A), sort by DueDate
2. **Wave board**: Board view grouped by Status, filtered by Wave
3. **Go/no-go**: grouped by Workload, totals: count Passed vs total
4. **Overdue**: DueDate < [Today], Status not Passed/N/A
5. **Failed & blocked**: with Severity, for the daily stand-up
