# QUOTA – Dataverse schema

Prefix your publisher (e.g. `qta_`). All data in /data is fictional.

| Table | Key columns | Notes |
|---|---|---|
| Opportunity (`qta_opportunity`) | name, account (text), contact, scope_summary (multiline), stage (choice), est_close_date, complexity (choice: Low/Medium/High) | Import from `data/opportunities.csv` |
| Price list item (`qta_pricelistitem`) | product_code, name, category (choice), unit, unit_price_eur (currency) | Import from `data/price_list.csv` |
| Pricing rule (`qta_pricingrule`) | complexity, multiplier (decimal), extra_hypercare_weeks (whole number) | Import from `data/pricing_rules.csv` |
| Estimate (`qta_estimate`) | name, opportunity (lookup), status (choice: Draft/Sent/Accepted), subtotal, multiplier, total (calculated) | Created by the agent |
| Estimate line (`qta_estimateline`) | estimate (lookup), price list item (lookup), quantity, line_total | Created by the agent |

Security roles: **Sales rep** (read price list, CRUD own estimates), **Sales manager** (read all). Test the agent with both.
