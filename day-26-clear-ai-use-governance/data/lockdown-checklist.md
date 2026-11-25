# Folder lockdown checklist (for the IT lead)

Score = sensitivity × exposure (+2 if a Copilot test prompt surfaced it). Highest first.

| # | Site › folder | Sensitivity | Who can open it now | Should be | Score | Action | Done |
|---|---|---|---|---|---|---|---|
| 1 | HR › Employee files | HR | Everyone except external users | HR team (named) | 11 | Fix now: remove broad access, grant the named group only, then re-run the Copilot test prompt | ☐ |
| 2 | Clients › Tailspin Toys | Client – confidential | Anyone link | Engagement team | 11 | Fix now: remove broad access, grant the named group only, then re-run the Copilot test prompt | ☐ |
| 3 | HR › Salary reviews 2026 | HR | Whole firm group | Partners + HR Manager | 8 | Fix now: remove broad access, grant the named group only, then re-run the Copilot test prompt | ☐ |
| 4 | Clients › Proseware Ltd | Client – confidential | Department + guests | Engagement team + 2 client guests | 6 | Fix now: remove broad access, grant the named group only, then re-run the Copilot test prompt | ☐ |
| 5 | Finance › Management accounts | Finance | Whole firm group | Partners + Finance | 6 | Fix now: remove broad access, grant the named group only, then re-run the Copilot test prompt | ☐ |
| 6 | Operations › Old intranet export 2021 | Internal | Everyone except external users | Archive (read-only) | 5 | Fix this month: tighten to the department group; ask the owner to confirm members | ☐ |
| 7 | Clients › Northwind Traders | Client – confidential | Department | Engagement team | 3 | Fix this month: tighten to the department group; ask the owner to confirm members | ☐ |
| 8 | HR › Policies (published) | Internal | Whole firm group | Whole firm group | 2 | Keep: review again at the next quarterly check | ☐ |
| 9 | Finance › Supplier invoices | Finance | Department | Finance team | 2 | Keep: review again at the next quarterly check | ☐ |
| 10 | Operations › Process docs | Internal | Whole firm group | Whole firm group | 2 | Keep: review again at the next quarterly check | ☐ |
| 11 | Partners › Partner meeting minutes | Finance | Department | Partners only | 2 | Keep: review again at the next quarterly check | ☐ |
| 12 | Clients › Contoso Pharma | Client – confidential | Named people | Engagement team | 0 | Keep: review again at the next quarterly check | ☐ |

**Summary:** 5 fix now · 2 fix this month · 5 keep. After each change, repeat the same Copilot test prompt as a user who should *not* see the folder.
