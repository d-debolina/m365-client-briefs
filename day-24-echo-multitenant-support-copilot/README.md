# Day 24 · ECHO: Embedded, Cross-tenant-safe, Handoff-ready Operator

A multi-tenant AI support copilot (SaaS): per-tenant knowledge with hard isolation, per-tenant tools, and human handoff.

| Path | What it is |
|---|---|
| `tenants/tenants.json` | 3 fictional customer tenants: plan, enabled tools, handoff target |
| `kb/<tenant>/*.md` | Tiny per-tenant knowledge bases |
| `app/retrieval.py` | Retrieval that filters by tenant **before** ranking (pattern for Azure AI Search security filters) |
| `app/tools.py` | Per-tenant tool allow-list + handoff |
| `tests/test_isolation.py` | 6 isolation tests incl. prompt injection |
| `eval/golden-questions.jsonl` | Golden questions incl. "don't know" and "human now" |

Run: `pip install pytest && python -m pytest tests -q`
