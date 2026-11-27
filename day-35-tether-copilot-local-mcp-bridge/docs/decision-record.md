# Decision record: how TETHER plugs a local MCP server into Microsoft Copilot

**Context.** A Windows CLI/automation app already ships an MCP server (works with other AI clients).
Customers want to search files, read file info, update variables and run scripts from Microsoft 365 Copilot or
Copilot Studio, without exposing their servers to the internet. It ships to many customers, so setup must be
repeatable and IT-friendly, respect user permissions, and confirm anything that changes data.

## Options
| Option | Good | Watch out |
|---|---|---|
| **A. Copilot Studio → MCP server (onboarding wizard)** | Reuses the existing MCP server; tools appear automatically; OAuth 2.0 supported | Streamable HTTP transport only (SSE dropped after Aug 2025); server URL must be reachable from the cloud; per-environment setup in each customer tenant |
| **B. Power Platform custom connector (MCP) + on-premises data gateway** | Gateway supports custom connectors; connector can be certified for cross-tenant use | Gateway is another Windows service to run and patch; connector packaging per release |
| **C. Declarative agent for Microsoft 365 Copilot + MCP plugin** (Agents Toolkit / Work IQ Dev Tools) | Lives inside Microsoft 365 Copilot; built-in confirmation prompts driven by `readOnlyHint` | Needs Microsoft 365 Copilot licences to be useful; app package deployed by each customer's admin |
| **D. Copilot connector (synced or federated)** | Great for *knowledge* | Read-only. Federated (MCP) connectors are early-access preview. Can't run commands, so not enough on its own |

## Decision
One MCP endpoint, two front ends: **A** for customers who build in Copilot Studio and **C** for customers who live
in Microsoft 365 Copilot. Both reach the same cloud URL: **Azure API Management** (Entra token check, tenant →
relay routing, rate limit) → **Azure Relay Hybrid Connection** → **TETHER bridge** on the customer's machine
(outbound 443 only) → the app's MCP server on localhost.

## Consequences
- No inbound firewall rule, no VPN, one Hybrid Connection per customer install (max 25 listeners each).
- Relay HTTP requests must answer within 60 seconds: long scripts return a job id and a `get_job_status` tool.
- Confirmation is enforced **in the bridge** (two-step code), not just in the agent's instructions, so it holds
  for every front end.
- Dev tunnels are fine for the demo, not for production.
