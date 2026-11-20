# BRIDGE sequence (technician opens a ticket)

```
Technician browser        ITSM backend (plugin)          Entra ID        Copilot Studio agent        ITSM MCP server
      |  open ticket 1007        |                           |                   |                          |
      |------------------------->| check tech can see 1007   |                   |                          |
      |                          | sign context {upn,1007,exp}                   |                          |
      |<-- panel + signed ctx ---|                           |                   |                          |
      |  MSAL sign-in (SSO) ------------------------------->|                   |                          |
      |<-------------------------------- user token --------|                   |                          |
      |  Agents SDK client: start conversation (user token) ------------------->|                          |
      |  event "ticketContext" {signedCtx} ------------------------------------>|                          |
      |                          |                           |                   | tool call (OBO token +   |
      |                          |                           |                   |  signedCtx) ------------>|
      |                          |                           |                   |         verify signature,|
      |                          |                           |                   |         upn == token upn,|
      |                          |                           |                   |         entity rights    |
      |<------------------------------------- summary + next steps -------------|<-------------------------|
```
Ticket changes in the UI → the panel sends a new signed context event (no new conversation needed).
