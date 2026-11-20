# Shared hand-off table: `triad_request` (Dataverse)

One row per request. All three agents read and write this table, so a request can move between agents
without anyone retyping it, and the main agent can answer "what's the status of TRI-1007?".

| Column | Type | Notes |
|---|---|---|
| `triad_requestid` | Autonumber | Format `TRI-{SEQNUM:4}` |
| `triad_process` | Choice | Access · Purchase · Leave |
| `triad_requester` | Lookup (User) | Always the signed-in user, never typed in |
| `triad_status` | Choice | Draft · Waiting for approval · Approved · Rejected · Done · Needs human |
| `triad_summary` | Text (200) | One line the agent writes back to the user |
| `triad_payload` | Multiline text | JSON with the process-specific fields (see examples below) |
| `triad_owneragent` | Text | KEYMASTER / BUYER / LEAVE |
| `triad_parentrequest` | Lookup (triad_request) | Links sub-requests (e.g. a laptop purchase + its access request) |

## Example payloads
```json
{"process":"Access","resource":"Finance SharePoint site","level":"Read","justification":"Q4 budget review"}
{"process":"Purchase","item":"Standing desk","qty":1,"estimate_eur":450,"cost_centre":"CC-210"}
{"process":"Leave","type":"Annual","from":"2026-12-22","to":"2026-12-24","half_day":false}
```

Security: give each agent's Dataverse connection a security role that can only create and update its
own process rows, plus read access to the status columns. The main agent only gets read access.
