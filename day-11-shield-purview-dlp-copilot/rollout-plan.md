# SHIELD rollout plan (12 weeks)

| Weeks | Wave | What | Mode |
|---|---|---|---|
| 1–2 | 0 | Workshops with data owners, use-case register, label taxonomy check, custom SITs + EDM | – |
| 3–6 | 1 | Copilot location policy (UC01–UC04) | Simulation → Enforce (low disruption, high value) |
| 4–8 | 2 | Exchange / SharePoint / Teams (UC05–UC08, UC13–UC15) | Simulation → Warn → Block |
| 7–12 | 3 | Endpoint DLP: USB, upload, paste to AI sites, print (UC09–UC12) | Simulation → Warn (block only after 2 weeks < 10 % FP) |
| Ongoing | – | Monthly business review: KPIs, tuning, new use cases | – |

Rules of thumb:
- Simulation runs up to 15 days; results are kept for 30 days. Run at least one full business cycle.
- For SharePoint/OneDrive, simulation evaluates existing **and** new items; for Exchange, Teams and devices only new items.
- SIT conditions and sensitivity-label conditions can't be in the **same rule** of a Copilot policy. Use separate rules.
