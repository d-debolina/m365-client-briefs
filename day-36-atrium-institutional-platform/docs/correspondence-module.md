# Correspondence module (phase 1) – build notes

**List `Correspondence`** (Records hub → Correspondence site)
| Column | Type | Notes |
|---|---|---|
| Reference | Single line, read-only in forms | `OUT-CI-2027-00042`, set by the flow |
| Direction | Choice | Outgoing / Incoming / Internal memo |
| Entity | Managed metadata | Contoso Institute / Contoso Services |
| Subject (EN) / Subject (AR) | Single line ×2 | Both required for Outgoing |
| Party | Single line / lookup to Parties list | |
| Classification | Choice | Internal / Confidential (Confidential → restricted library + sensitivity label) |
| Owner unit | Managed metadata | |
| Status | Choice | Draft → Awaiting approval → Approved → Sent / Registered |
| Letter | Lookup to `Letters` library | The signed PDF lives in the library |

**Hidden list `Counters`**: Title = series key (`OUT-CI-2027`), Value = number.

**Flow `Issue reference`** (trigger: item created, trigger concurrency = 1)
1. Build the series key from Direction + Entity + year.
2. Get the counter item (create it at 0 if missing).
3. Update it to Value + 1 with the **If-Match** ETag (Send an HTTP request to SharePoint). On 412, wait and retry.
4. Write the reference back to the item.
5. Outgoing / memo → call the shared approval child flow with doc type + entity.

Trigger concurrency set to 1 already serialises the flow; the ETag check is the belt to those braces
(it also protects against a second flow or a manual edit).
