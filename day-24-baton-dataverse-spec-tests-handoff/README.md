# Day 24 · BATON: Build, Assert, Test, Own, Note

A Dataverse implementation done properly: a spec that maps rules to the right place, a test matrix with negative tests,
CLI checks, and a handoff pack the next developer actually wants.

| File | What it is |
|---|---|
| `spec/implementation-spec.md` | Fictional "Equipment Loans" spec: tables, logic placement, security, ALM |
| `tests/test-matrix.csv` | 12 tests: positive + negative per rule, security, UI, ALM |
| `tests/checkout.te.yaml` | Power Apps Test Engine example (check current schema) |
| `pipeline/build-and-check.yml` | pac CLI: export, unpack, solution checker, managed export |
| `handoff/handoff-pack.md` | Handoff checklist |
