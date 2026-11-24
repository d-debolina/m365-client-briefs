"""Draws architecture.dot/.svg/.png for Day 30 PROBE with the series helpers in tools/diagrams.py."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "tools"))
from diagrams import n, b, cluster, render

body = (
    n("rep", b("Signed-in user", "rep · manager · compliance"), "user")
    + n("rev", b("Reviewer", "runs the test matrix"), "user")
    + cluster("m365", "Microsoft 365", "m365",
        n("m365c", b("Microsoft 365 Copilot", "Teams / Copilot Chat"), "m365")
        + n("entra", b("Entra ID", "SSO · who is asking"), "m365")
        + n("purview", b("Purview audit", "Copilot interactions<br/>jailbreak / XPIA flags"), "m365"))
    + cluster("cs", "Copilot Studio + Power Platform environment", "cs",
        n("agent", b("Sales insights agent", "instructions · tools"), "cs")
        + n("tool", b("Salesforce connector tools", "User authentication<br/>(per-user OAuth connection)"), "cs")
        + n("ppac", b("Environment controls", "maker credentials off · data policies<br/>transcripts + retention"), "pp")
        + n("dv", b("Dataverse", "conversation transcripts"), "pp"))
    + cluster("sf", "Salesforce org (external)", "user",
        n("app", b("Connected app", "Microsoft Power Platform<br/>admin-approved users"), "user")
        + n("sec", b("Profiles · permission sets", "sharing rules · role hierarchy<br/>field-level security"), "user")
        + n("data", b("Accounts · Referrals (PHI)", "sandbox, fictional data"), "user"))
    + n("kit", b("PROBE kit", "test_matrix.csv · check_results.py<br/>findings report"), "doc")
    + """  rep -> m365c [label="question"]; m365c -> entra [style=dotted]; m365c -> agent;
  agent -> tool [label="tool call"]; tool -> app [label="as the user"]; app -> sec;
  sec -> data [label="only what this user may see"];
  ppac -> tool [label="no author credentials", style=dashed];
  agent -> dv [label="transcript", style=dashed];
  m365c -> purview [label="audit record", style=dashed];
  rev -> kit; kit -> m365c [label="20 prompts × each test user", style=dotted];
  purview -> kit [label="evidence", style=dotted];
"""
)

render("day-30-probe-copilot-salesforce-access-review",
       "Day 30 · PROBE — Prove Records Obey Boundaries End-to-end",
       "Security review of a Copilot Studio agent over Salesforce: per-user access, leak tests and evidence",
       body)
