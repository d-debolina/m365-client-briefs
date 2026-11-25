"""Draws architecture.dot/.svg/.png for Day 32 GRANT with the series helpers in tools/diagrams.py."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "tools"))
from diagrams import n, b, cluster, render

body = (
    n("staff", b("Staff", "16 forms · one portal"), "user")
    + n("appr", b("Approvers", "Outlook · Teams · back-office app"), "user")
    + cluster("pp", "Power Platform – Prod (managed environment)", "pp",
        n("portal", b("Self-service canvas app", "leave · travel · purchase …"), "pp")
        + n("back", b("Back-office model-driven app", "approvers · admin area"), "pp")
        + n("parent", b("Parent flow per form", "thin: trigger + 2 calls"), "pp")
        + n("route", b("Child flow: Resolve route", "matrix · delegation · budget check"), "pp")
        + n("stage", b("Child flow: Run stage", "approve · return · reject"), "pp")
        + n("sched", b("Scheduled flow", "reminders · escalation to alternate"), "pp")
        + n("dv", b("Dataverse", "grt_request · grt_approvalrule · grt_roleholder<br/>grt_delegation · grt_approvalstep (audit)<br/>grt_budgetline · grt_commitment · grt_setting"), "pp"))
    + cluster("m365", "Microsoft 365", "m365",
        n("approvals", b("Approvals connector", "custom responses"), "m365")
        + n("sp", b("SharePoint", "attachments per request"), "m365")
        + n("pbi", b("Power BI", "budget vs committed vs actual<br/>turnaround per stage"), "m365"))
    + cluster("alm", "Delivery", "doc",
        n("dev", b("Dev environment", "unmanaged solution"), "doc")
        + n("pipe", b("Pipelines in Power Platform", "managed solution · env variables<br/>service principal owns flows"), "doc"))
    + """  staff -> portal; portal -> dv [label="submit"];
  dv -> parent [label="status = Submitted"];
  parent -> route; route -> dv [style=dashed, label="read rules"];
  parent -> stage; stage -> approvals; approvals -> appr;
  stage -> dv [label="audit step"]; sched -> approvals [style=dashed, label="cancel · reassign"];
  appr -> back [style=dotted]; back -> dv;
  portal -> sp [style=dotted, label="files"]; dv -> pbi;
  dev -> pipe; pipe -> dv [style=dotted, label="deploy"];
"""
)

render("day-32-grant-approval-engine",
       "Day 32 · GRANT — Generic Routing, Approvals, Numbering &amp; Tracking",
       "One reusable approval engine on Dataverse, many thin forms on top",
       body)
