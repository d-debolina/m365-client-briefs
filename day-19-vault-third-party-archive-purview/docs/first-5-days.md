# First 5 days of validation (what the client asked for)

1. **Day 1**: Data model: export 50 representative items (email, chat, SMS, with/without attachments). Hash them (`integrity_manifest.py`).
2. **Day 2**: Path decision: confirm whether a native/partner data connector exists; if not, prototype import into a test mailbox. Licences and roles checked.
3. **Day 3**: Import the 50 items; verify sender, recipients, dates, attachments, custodians, and that items are searchable.
4. **Day 4**: Retention + hold: auto-apply a retention label, create a case via Graph, add custodians, apply hold, run a search, export.
5. **Day 5**: Compare manifests (before vs after export), document gaps, write the production roadmap (volume, throttling, delta sync, monitoring, who enforces holds in each system).
