# Implementation spec: Equipment Loans (fictional, Dataverse)

## 1. Scope
Staff borrow equipment (laptops, cameras, projectors). Stores staff check out/in. Overdue loans are chased automatically.

## 2. Data model (publisher prefix `eql_`)
| Table | Key columns | Notes |
|---|---|---|
| `eql_asset` | Name (primary), AssetTag (alt key, unique), Category (choice), Status (Available/OnLoan/Repair/Retired), Location (lookup) | Alternate key on AssetTag for imports |
| `eql_loan` | Asset (lookup, required), Borrower (lookup systemuser), Out (datetime), DueBack (date), Returned (datetime), State (choice) | 1 open loan per asset (enforced in plug-in or flow + business rule) |
| `eql_location` | Name, Building, Floor | |

Relationships: Asset 1:N Loan (restrict delete), Location 1:N Asset (referential).

## 3. Business logic
| ID | Rule | Where | Why there |
|---|---|---|---|
| BL1 | DueBack ≤ Out + 30 days | Business rule (server scope) | Works in all apps + API |
| BL2 | Only one open loan per asset | Low-code plug-in (Power Fx) / classic plug-in | Must hold for imports and API too |
| BL3 | Asset Status follows loan (OnLoan/Available) | Low-code plug-in on Loan create/update | Same transaction |
| BL4 | Reminder 1 day before DueBack, escalate 3 days after | Cloud flow (scheduled) | Async, email/Teams |

## 4. Security
| Role | Asset | Loan |
|---|---|---|
| Borrower | Read (org) | Create/Read own (user) |
| Stores | Read/Write (org) | Read/Write (org) |
| Admin | Full | Full |
Column security on `eql_asset.PurchasePrice`.

## 5. Non-functional
- ALM: unmanaged in Dev only; managed in Test/Prod via Pipelines; environment variables for mailbox and escalation days.
- Performance: views indexed on Status, DueBack.
- Data: 2,000 assets, 15,000 loans/year.

## 6. Acceptance criteria → tests
See `tests/test-matrix.csv` (every rule has at least one positive and one negative test).
