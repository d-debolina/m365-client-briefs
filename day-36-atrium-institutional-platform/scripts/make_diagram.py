"""Draws architecture.dot/.svg/.png for Day 36 ATRIUM with the series helpers in tools/diagrams.py."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "tools"))
from diagrams import n, b, cluster, render

body = (
    n("staff", b("Staff (EN / AR)", "two entities · one tenant"), "user")
    + cluster("sp", "SharePoint Online (hubs)", "m365",
        n("home", b("Home hub", "news · policies · multilingual"), "m365")
        + n("gov", b("Governance hub", "board · strategy · decisions"), "m365")
        + n("rec", b("Records hub", "Correspondence · Archive"), "m365")
        + n("ops", b("Operations hub", "HR · finance · procurement · service desk"), "m365")
        + n("aca", b("Academic hub", "programmes · research · quality"), "m365")
        + n("kn", b("Knowledge hub", "wiki · FAQ"), "m365"))
    + n("terms", b("Term store + content types", "Entity · Unit · Doc type · Classification"), "m365")
    + cluster("pp", "Power Platform (managed environment)", "pp",
        n("ref", b("Issue reference flow", "Counters list · ETag · concurrency 1"), "pp")
        + n("appr", b("Shared approval engine", "matrix list · escalation"), "pp")
        + n("pbi", b("Power BI", "KPIs · registers"), "pp"))
    + n("teams", b("Teams", "approvals · service desk cards"), "m365")
    + n("ai", b("Copilot Studio assistant", "phase 5 · permission-trimmed"), "cs")
    + n("sor", b("ERP · Student info system", "stay independent · read-only reports"), "user")
    + n("repo", b("Repo", "modules.csv · build order<br/>numbering tests · RTL checklist"), "doc")
    + """  staff -> home; home -> gov [style=invis]; staff -> teams;
  rec -> ref [label="new letter"]; ref -> appr [label="outgoing / memo"]; appr -> teams [label="approve"];
  ops -> appr; gov -> appr [style=dashed];
  terms -> rec [style=dotted]; terms -> ops [style=dotted]; terms -> aca [style=dotted];
  gov -> pbi [style=dashed]; sor -> pbi [style=dashed, label="read-only"];
  ai -> kn [label="grounded on"]; ai -> home [style=dashed];
  repo -> ref [style=dotted];
"""
)

render("day-36-atrium-institutional-platform",
       "Day 36 · ATRIUM — Approvals, Templates, Records, Institutional knowledge, Unified hubs, Modules",
       "A bilingual institutional platform on SharePoint and Power Platform: one information model, one approval engine, AI last",
       body)
