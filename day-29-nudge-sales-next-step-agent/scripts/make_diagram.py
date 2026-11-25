"""Draws architecture.dot/.svg/.png for Day 29 NUDGE with the series helpers in tools/diagrams.py."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "tools"))
from diagrams import n, b, cluster, render

body = (
    n("rep", b("Sales rep", "Teams on phone / laptop"), "user")
    + n("mgr", b("Sales manager"), "user")
    + cluster("cs", "Copilot Studio (standard harness)", "cs",
        n("agent", b("NUDGE agent", "generative orchestration"), "cs")
        + n("kn", b("Knowledge", "sales playbook page"), "cs")
        + n("tools", b("SharePoint connector tools", "Get items · Create item · Update item"), "cs"))
    + cluster("m365", "Microsoft 365", "m365",
        n("teams", b("Teams chat with NUDGE", "questions + follow-up cards"), "m365")
        + n("lists", b("SharePoint lists = CRM-lite", "Accounts · Commitments · Activities"), "m365")
        + n("mail", b("Outlook", "fallback e-mail"), "m365"))
    + cluster("pp", "Power Automate (standard connectors)", "pp",
        n("flow", b("Daily follow-up cloud flow", "08:00 weekdays · FollowUpDate = today"), "pp"))
    + n("csv", b("data/*.csv", "fictional sample data"), "doc")
    + """  rep -> teams [label="what next on Contoso?"];
  teams -> agent; agent -> kn [label="next-step rules"];
  agent -> tools [label="read / save commitment\\n(after rep confirms)"]; tools -> lists;
  flow -> lists [label="due today?"];
  flow -> teams [label="card as NUDGE:\\nhow did it go?"];
  teams -> flow [label="answer", style=dashed]; flow -> lists [label="Outcome · Status"];
  flow -> mail [label="agent not installed", style=dashed];
  lists -> mgr [label="list views / Power BI", style=dotted];
  csv -> lists [style=dotted];
"""
)

render("day-29-nudge-sales-next-step-agent",
       "Day 29 · NUDGE — Next steps, Updates, Due dates, Gentle follow-ups, Evidence",
       "A Copilot Studio sales coach with SharePoint lists as a CRM-lite and Teams follow-ups on the right day",
       body)
