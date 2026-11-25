# Day 14 · LEDGER: Lookup, Engage, Document, Guide, Escalate, Report

A merchant-onboarding Copilot Studio agent for a (fictional) payments company: SharePoint policies as knowledge,
a custom connector to a third-party CRM, and governance from day one.

| File | What it is |
|---|---|
| `connector/fabrikam-crm-openapi.yaml` | OpenAPI 2.0 definition for the custom connector (API key auth) |
| `mock-api/mock_crm.py` | Dependency-free mock CRM for local testing |
| `data/merchants.*` | 25 fictional merchants in different onboarding stages |
| `knowledge/*.docx` | Onboarding policy, KYC guide, follow-up playbook (upload to a SharePoint site) |
| `agent-instructions.md` | Agent instructions |
| `eval/test-questions.csv` | 10 test questions incl. confirmation, refusal and prompt-injection checks |
| `governance-checklist.md` | Environments, DLP, Key Vault, monitoring |
