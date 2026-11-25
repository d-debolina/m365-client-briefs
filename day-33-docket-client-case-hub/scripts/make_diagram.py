"""Draws architecture.dot/.svg/.png for Day 33 DOCKET with the series helpers in tools/diagrams.py."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "tools"))
from diagrams import n, b, cluster, render

body = (
    n("staff", b("Fee earners", "partners · associates · paralegals"), "user")
    + n("guest", b("Client contacts", "Entra B2B guests"), "user")
    + cluster("m365", "SharePoint Online – DOCKET hub", "m365",
        n("hub", b("DOCKET Hub", "communication site · navigation<br/>dashboard page"), "m365")
        + n("lists", b("Clients &amp; Retainers site", "Clients · Retainers · Allocations lists<br/>sharing off"), "m365")
        + n("cases", b("Case files site", "one document set per case<br/>restricted cases: own permissions<br/>sharing off"), "m365")
        + n("share", b("Client Share site", "folder per case · Specific people links<br/>guest expiry"), "m365"))
    + cluster("pp", "Power Platform (standard connectors)", "pp",
        n("f1", b("Flow: New case", "create document set · set metadata<br/>break inheritance if restricted"), "pp")
        + n("f2", b("Flow: Retainer hours", "daily · alert at 80%"), "pp")
        + n("f3", b("Flow: Guest review", "weekly · closed cases"), "pp"))
    + n("pbi", b("Power BI dashboard", "team load · cases · retainers · access"), "m365")
    + n("plan", b("docket_plan.py", "permission plan · scope check<br/>allocation table"), "doc")
    + """  staff -> hub; hub -> lists; hub -> cases;
  staff -> f1 [label="open a case"]; f1 -> cases; f1 -> share [style=dashed, label="if external"];
  lists -> f2 [dir=back]; f3 -> share [label="remove stale guests"];
  guest -> share [label="one folder only"];
  lists -> pbi; cases -> pbi [style=dotted];
  plan -> cases [style=dotted, label="design check"];
"""
)

render("day-33-docket-client-case-hub",
       "Day 33 · DOCKET — Document sets, Oversight, Cases, Keys, External access, Tracking",
       "A client, retainer and case hub on SharePoint, Lists, Power Automate and Power BI",
       body)
