# Day 17 · CARGO: Cloud Attachments Routed to Guarded Objects

Power Pages forms that accept large files: find which limit you're hitting, then move attachments to Azure Blob Storage safely.

| File | What it is |
|---|---|
| `diagnose/which-limit-am-i-hitting.md` | Symptom → limit → fix table |
| `infra/create-storage.sh` | Azure CLI: private storage account, RBAC for the site app, CORS, lifecycle tiers |
| `site/site-settings.csv` | Site settings for timeline + Web API uploader |
| `site/client-validation.js` | Friendly client-side size/type checks |
| `tests/make-test-files.py` + `test-plan.md` | Test files and expected results per storage option |
