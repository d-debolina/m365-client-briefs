# Day 16 · BRIDGE: Bound to Role, Identity & Data, Guarded End-to-end

Embed a Copilot Studio agent in any web app (here: a self-hosted ITSM ticket screen) with the
Microsoft 365 Agents SDK, Entra sign-in, signed page context and an MCP server that enforces per-user rights.

| File | What it is |
|---|---|
| `context/signed_context.py` | HMAC-signed, short-lived ticket context (server-side) |
| `mcp-server/itsm_tools.py` | Tool logic for the MCP server: runs as the technician, checks customer entity rights, audits |
| `tests/test_security.py` | Negative tests: other customer, tampered id, replay, expiry, cross-entity search |
| `data/*.json` | 30 fictional tickets across 3 customers, 3 technicians |
| `docs/sequence.md` | End-to-end sequence |
| `docs/security-test-matrix.md` | Release-blocking test matrix |

Run the tests: `pip install pytest && python -m pytest tests -q`

For the chat client itself, start from Microsoft's official Copilot Studio client samples for the
Microsoft 365 Agents SDK (.NET, JavaScript or Python) and add the `ticketContext` event.
