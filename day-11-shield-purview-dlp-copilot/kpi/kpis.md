# KPIs management actually reads (one page, monthly)

1. **Coverage:** % of use cases in Enforce mode (target: wave 1 by week 8)
2. **Precision:** false-positive rate per policy (target < 10 % before moving from Warn to Block)
3. **Behaviour change:** overrides with justification per 100 users (should fall over time)
4. **Copilot protection:** prompts blocked + labelled files excluded from Copilot answers
5. **Incidents:** true-positive incidents and median time to triage

Power BI: import `activity/dlp-activity-export.csv` (in real life: Activity explorer export or the
Office 365 Management API), add a Date table, and build one page per KPI.
