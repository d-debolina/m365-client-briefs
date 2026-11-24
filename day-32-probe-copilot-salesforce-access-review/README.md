# Day 32 · PROBE – Prove Records Obey Boundaries End-to-end

A security review kit for a Copilot Studio agent (used through Microsoft 365 Copilot) that reads a CRM holding
regulated health data. The question from the brief: *does the agent only return what each signed-in user is
allowed to see in Salesforce?* PROBE answers it with an approach plan, a test matrix with prompt-injection
cases, a checker that flags leaks, a hardening checklist and a findings report template.

> Every user, clinic and "patient" here is fictional. Run tests in a sandbox org with masked or fictional data.

## What's inside
| Path | What it is |
|---|---|
| `data/salesforce_users.csv` | 9 fictional users across roles, incl. the risky integration user |
| `data/accounts.csv`, `data/referrals.csv` | 12 accounts and 36 referrals with owners (fictional) |
| `data/sharing-model.md` | Org-wide defaults, role hierarchy, View All and field-level security used by the checker |
| `tests/test_matrix.csv` | 20 tests: baseline, cross-user, hierarchy, prompt injection, FLS, identity, logging |
| `tests/results_sample.csv` | Example run with two planted leaks (T-07 and T-10) |
| `scripts/check_results.py` | Works out what each user should see and flags extra records or fields |
| `scripts/make_data.py` | Regenerates the CSVs |
| `review/approach-plan.md` | The short written plan to send before starting |
| `review/findings-report-template.md` | Severity scale and findings table |
| `controls/hardening-checklist.md` | Identity, Salesforce, agent, transcript and logging controls |
| `architecture.*` | Diagram (PNG / SVG / editable DOT) |

## How to use
1. `python scripts/check_results.py` to see the checker flag the two planted leaks.
2. Recreate the users and sharing model in a Salesforce sandbox (or map them to the client's real roles).
3. Run every prompt in `tests/test_matrix.csv` as each test user in Microsoft 365 Copilot, and write the returned
   record IDs and fields into a results CSV with the same columns as `results_sample.csv`.
4. `python scripts/check_results.py your-results.csv` – any LEAK is a finding. Fix, rerun, attach the output to the report.
