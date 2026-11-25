# Day 12 · PARCEL: Parse, Assemble, Route, Check, Emit, Log

Outlook emails → AI extraction → JSON schema validation → REST API, with retries and a dead-letter list.

| File | What it is |
|---|---|
| `emails/` | 22 fictional booking emails (tables, free text, lists, forwards, German, one incomplete, one newsletter) |
| `expected/` | The JSON each email should produce |
| `api-schema.json` | The (fictional) Fabrikam Freight API request schema |
| `prompt/extract-booking.md` | The prompt with JSON output |
| `scripts/regex_baseline.py` | Shows why split/regex breaks on real emails |
| `scripts/validate_and_post.py` | Validates JSON against the schema (same check as the flow) |
| `flow-outline.md` | Step-by-step flow design with Try/Catch, retry and idempotency |
