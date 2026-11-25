# Which "connector" do you need? (VAULT decision table)

| Path | What it's for | Gives you retention / hold / eDiscovery? | Notes |
|---|---|---|---|
| **Purview data connectors** (native or partner) | Import + archive third-party data **into user mailboxes** | ✅ Litigation hold, eDiscovery, retention, records management (varies by connector) | Partner connectors need a business relationship + a provisioned service principal |
| **Custom import into mailboxes** (vendor-built, e.g. via EWS/Graph import or PST import) | When no connector exists | ✅ once items are in the mailbox | Vendor owns mapping, idempotency, throttling, item properties |
| **Microsoft 365 Copilot connectors** (formerly Graph connectors) | Index external content for **search and Copilot** | ❌ Not a compliance archive | Great for "find it", not for "preserve it" |
| **Graph eDiscovery API** | Automate cases, custodians, holds, searches, review sets, exports | n/a (operates on data already in M365) | App must be registered in the customer tenant |
| **Leave data in the archive** + federated search via the vendor's own API/MCP | Very large or regulated archives | ❌ in Purview; ✅ in the vendor system | Two systems of record: document who enforces holds |

## Field mapping (archive → mailbox item)
| Archive field | Mailbox item | Check |
|---|---|---|
| archiveId | custom extended property + in subject/body footer | Searchable in eDiscovery |
| from / to | sender / recipients | Participants condition works |
| sentUtc | sent/received date | Date range queries match |
| custodians | target mailbox(es) | One copy per custodian mailbox |
| attachments | file attachments | Counts + hashes match |
| retentionClass | retention label via auto-apply policy | Label present on item |
| legalHold | case hold on the custodian | Hold status = applied |
