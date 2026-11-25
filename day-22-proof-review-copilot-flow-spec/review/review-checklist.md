# PROOF review checklist (use on any AI-written flow spec)

| # | Check | Question to ask | Found in example |
|---|---|---|---|
| P1 | **Trigger scope** | Which mailbox/folder? Filters? Will it fire on every email? | ❌ whole Inbox, no sender/subject filter |
| P2 | **Data source of truth** | Where exactly does each value come from? | ❌ "total from the body", but invoices are PDFs |
| P3 | **Identity & connections** | Whose account runs it? Shared mailbox? Service account? | ❌ not stated |
| P4 | **Names & collisions** | What if two files have the same name? | ❌ overwrites `invoice.pdf` |
| P5 | **Thresholds & currency** | 1000 of what currency? Inclusive? | ❌ ambiguous |
| P6 | **Approver resolution** | "the manager" of whom? What if absent? Timeout? | ❌ undefined |
| P7 | **Error handling** | What happens on failure? Retry? Alert? | ❌ none |
| P8 | **Idempotency** | What if the flow runs twice for the same email? | ❌ duplicate files + rows |
| P9 | **Tables & limits** | Excel needs a table; concurrency on Excel writes | ❌ "tracker" unspecified |
| P10 | **Security & data** | Attachments with macros? External senders? DLP? | ❌ not considered |
| P11 | **Testability** | Concrete acceptance tests? | ❌ none |
