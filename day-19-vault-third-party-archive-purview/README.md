# Day 19 · VAULT: Validate, Archive, Unify, Legal-hold, Trace

Bringing a third-party archive under Microsoft Purview eDiscovery and records management, with evidence integrity.

| File | What it is |
|---|---|
| `archive-export/items.json` | 40 fictional archived items (email, chat, SMS) with custodians, attachments, retention class, hold flag, SHA-256 |
| `scripts/integrity_manifest.py` | Recompute and compare hashes before/after |
| `scripts/ediscovery_case.py` | Graph eDiscovery API: case → custodians → hold → search |
| `docs/integration-paths.md` | Data connectors vs Copilot connectors vs eDiscovery API + field mapping |
| `docs/first-5-days.md` | The 5-day validation plan |
