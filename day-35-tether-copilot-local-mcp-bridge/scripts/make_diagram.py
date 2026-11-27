"""Draws architecture.dot/.svg/.png for Day 35 TETHER with the series helpers in tools/diagrams.py."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "tools"))
from diagrams import n, b, cluster, render

body = (
    n("user", b("Customer user", "Reader · Operator · Admin"), "user")
    + cluster("cs", "Microsoft Copilot (customer tenant)", "cs",
        n("m365c", b("Microsoft 365 Copilot", "declarative agent + MCP plugin"), "cs")
        + n("mcs", b("Copilot Studio agent", "MCP tool · OAuth 2.0"), "cs"))
    + n("entra", b("Entra ID", "Tether.Invoke scope · app roles"), "m365")
    + cluster("az", "Azure (vendor subscription)", "azure",
        n("apim", b("API Management", "validate token · tid → relay<br/>rate limit · SAS signing"), "azure")
        + n("relay", b("Azure Relay", "one Hybrid Connection<br/>per customer install"), "azure")
        + n("kv", b("Key Vault", "relay Send key"), "azure"))
    + cluster("onprem", "Customer machine (no inbound ports)", "user",
        n("bridge", b("TETHER bridge service", "role filter · fences<br/>two-step confirm · audit"), "doc")
        + n("app", b("Windows app MCP server", "127.0.0.1 · search · file info<br/>variables · scripts"), "user"))
    + """  user -> m365c; user -> mcs;
  m365c -> entra [style=dashed, label="sign-in"]; mcs -> entra [style=dashed];
  m365c -> apim [label="MCP (streamable HTTP)"]; mcs -> apim [label="MCP"];
  kv -> apim [style=dotted]; apim -> relay [label="HTTPS + SAS"];
  bridge -> relay [label="outbound 443 listener", dir=back];
  bridge -> app [label="localhost only"];
"""
)

render("day-35-tether-copilot-local-mcp-bridge",
       "Day 35 · TETHER — Tunnelled, Entra-Trusted Host Execution Relay",
       "Microsoft Copilot calls a local Windows app's MCP server through Azure Relay, with no inbound ports and a confirm step for every change",
       body)
