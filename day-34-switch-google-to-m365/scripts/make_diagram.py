"""Draws architecture.dot/.svg/.png for Day 34 SWITCH with the series helpers in tools/diagrams.py."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "tools"))
from diagrams import n, b, cluster, render

body = (
    n("team", b("Agency team", "6 people · laptops"), "user")
    + n("clients", b("Client contacts", "guests on one folder each"), "user")
    + cluster("g", "Google (source, kept until sign-off)", "user",
        n("gmail", b("Gmail", "mail · calendars · contacts"), "user")
        + n("gdrive", b("Google Drive", "My Drive · 4 shared drives"), "user")
        + n("cid", b("Cloud Identity Free", "keeps client Ads · GA4 · GTM access"), "user"))
    + cluster("m365", "Microsoft 365 Business Premium (client-owned tenant)", "m365",
        n("eac", b("EAC migration batch", "pilot → wave 1 → complete"), "m365")
        + n("mm", b("Migration Manager", "Google Drive → OneDrive / SharePoint"), "m365")
        + n("exo", b("Exchange Online", "mailboxes · shared mailbox · DL"), "m365")
        + n("od", b("OneDrive", "personal files"), "m365")
        + n("sp", b("SharePoint + Teams", "Clients · Studio · Finance sites"), "m365")
        + n("sec", b("Entra ID · Intune · Defender", "CA policies · compliance · presets"), "m365")
        + n("bkp", b("Microsoft 365 Backup", "pay-as-you-go · restore test"), "m365"))
    + n("plan", b("switch_plan.py", "batch CSVs · destinations<br/>link replacements · readiness"), "doc")
    + """  gmail -> eac [label="Gmail API"]; eac -> exo;
  gdrive -> mm [label="Microsoft 365 migration app"]; mm -> od; mm -> sp;
  team -> exo [label="after MX cutover"]; team -> sp; team -> cid [style=dashed, label="client Google tools"];
  sec -> team [style=dashed, label="sign-in & device rules"];
  clients -> sp [label="Specific people links"];
  exo -> bkp [style=dotted]; sp -> bkp [style=dotted];
  plan -> eac [style=dotted]; plan -> mm [style=dotted];
"""
)

render("day-34-switch-google-to-m365",
       "Day 34 · SWITCH — Scope, Wave-pilot, Import, Test, Cut over, Hand over",
       "Google Workspace to Microsoft 365 Business Premium for a small team, with a pilot, a rollback and a proven restore",
       body)
