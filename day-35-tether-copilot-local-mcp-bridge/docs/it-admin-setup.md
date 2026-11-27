# TETHER setup for a customer IT admin (outline)

1. **Install** the TETHER bridge service from the product installer (signed MSI). It runs as a low-privilege
   service account and only calls 127.0.0.1 and `*.servicebus.windows.net` on 443.
2. **Allow outbound** `<your-namespace>.servicebus.windows.net:443` on the firewall (DNS allow-listing is fine).
3. **Consent** to the TETHER enterprise app in Entra ID (delegated `Tether.Invoke`). Assign users to the
   app roles *Reader*, *Operator* or *Admin*.
4. **Pick workspaces** the agent may touch (folders/projects) in the bridge config. Nothing else is reachable.
5. **Copilot Studio customers:** Tools → Add a tool → Model Context Protocol → server URL from the onboarding
   email, OAuth 2.0 with the values provided. Test with a Reader account first.
6. **Microsoft 365 Copilot customers:** upload the TETHER agent package in the Microsoft 365 admin center
   (Integrated apps) and assign it to a pilot group.
7. **Check the audit log** (bridge log + APIM logs) after the first week. Rotate the relay Listen key yearly.
