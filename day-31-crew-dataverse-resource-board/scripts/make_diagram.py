"""Draws architecture.dot/.svg/.png for Day 31 CREW with the series helpers in tools/diagrams.py."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "tools"))
from diagrams import n, b, cluster, render

body = (
    n("planner", b("Planner", "North / South yard"), "user")
    + n("lead", b("Planning lead", "approves unlocks"), "user")
    + n("xl", b("Excel / API / imports", "the back doors"), "user")
    + cluster("pp", "Power Platform environment (managed)", "pp",
        n("mda", b("Model-driven app", "custom pages: Resource Board · Look-ahead<br/>What-if · Tools &amp; rentals"), "pp")
        + n("dv", b("Dataverse", "projects · tasks · crew · demand<br/>scenarios · capacity · staging"), "pp")
        + n("plug", b("C# plug-ins", "LockGuard (PreValidation)<br/>WorkdayMath (PreOperation)"), "pp")
        + n("capi", b("Custom API", "crew_RecalculateDemand"), "pp")
        + n("flows", b("Cloud flows", "unlock approval · rules<br/>nightly checks · imports"), "pp"))
    + cluster("az", "Azure", "azure",
        n("fn", b("Planning engine", "Azure Function · managed identity"), "azure"))
    + cluster("m365", "Microsoft 365", "m365",
        n("teams", b("Teams + Outlook", "approval cards · notifications"), "m365")
        + n("sp", b("SharePoint", "Excel import library"), "m365")
        + n("sg", b("Entra security groups", "→ Dataverse group teams"), "m365"))
    + n("tests", b("Acceptance tests", "engine/test_planning_engine.py"), "doc")
    + """  planner -> mda; mda -> dv;
  xl -> dv [label="edits", style=dashed];
  dv -> plug [label="every create / update / delete"];
  plug -> dv [label="block if locked", style=dashed];
  mda -> capi [label="Recalculate / What-if"]; capi -> fn; fn -> dv [label="weekly capacity rows"];
  mda -> flows [label="Request unlock"]; flows -> teams; teams -> lead; lead -> teams [style=dashed];
  flows -> dv [label="unlocked until …"];
  sp -> flows [label="new file"]; flows -> dv [label="via staging"];
  sg -> dv [label="security roles", style=dotted];
  tests -> fn [label="expected numbers", style=dotted];
"""
)

render("day-31-crew-dataverse-resource-board",
       "Day 31 · CREW — Capacity, Resources, Equipment &amp; Weeks",
       "Dataverse resource board where a locked plan stays locked, with a planning engine you can test",
       body)
