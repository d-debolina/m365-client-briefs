# DOCKET – allocation and oversight dashboard (Power BI)

Sources: SharePoint Online lists *Clients*, *Retainers*, *Allocations* and the *Case files* library (document set
properties). For a quick start, `out/allocation-dashboard.csv` from `scripts/docket_plan.py` has the same shape.

## Pages
1. **Team load:** planned hours vs capacity per person this week (bar + target line), OVER / LOW flags, open cases per person.
2. **Cases:** open cases by practice and status, cases without an allocation, oldest open cases.
3. **Retainers:** hours used vs included per retainer this month, renewals in the next 60 days.
4. **Access:** restricted cases count and Client Share folders with guests on closed cases (from flow 3's list).

## Measures (DAX)
```
Planned Hours = SUM ( Allocations[Hours] )
Capacity = SUM ( Staff[WeeklyCapacityHours] )
Utilisation % = DIVIDE ( [Planned Hours], [Capacity] )
Over Allocated = IF ( [Planned Hours] > [Capacity], "OVER", IF ( [Utilisation %] < 0.5, "LOW", "" ) )
Retainer Burn % = DIVIDE ( SUM ( Retainers[HoursUsedThisMonth] ), SUM ( Retainers[IncludedHours] ) )
```

## Security
Publish to a workspace only partners and practice managers can see. Restricted cases show only Case ID and practice
in the dataset, not titles (filter them in Power Query), so the dashboard can't leak what the ethical wall hides.
