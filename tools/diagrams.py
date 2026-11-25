"""Consistent architecture diagrams (Graphviz) for the series.

Usage for a new day:
    import sys; sys.path.insert(0, "tools"); from diagrams import n, b, cluster, render
    body = n("u", b("User"), "user") + cluster("pp", "Power Platform", "pp", n("app", b("App"), "pp")) + "  u -> app;\n"
    render("day-08-xyz-slug", "Day 8 · XYZ — Expansion", "one-line subtitle", body)
Kinds: user, pp (Power Platform), m365, azure, cs (Copilot/AI), doc (repo files/outputs).
Escape & as &amp; and > as &gt; inside labels. Needs graphviz `dot` (apt-get install graphviz).
"""
import subprocess, pathlib, textwrap

REPO = pathlib.Path(__file__).resolve().parents[1]

# Palette per platform
C = {
    "user":  ("#F3F4F6", "#6B7280"),
    "pp":    ("#F3E8FF", "#7C3AED"),   # Power Platform
    "m365":  ("#E0F2FE", "#0369A1"),   # Microsoft 365
    "azure": ("#E0F7F4", "#0F766E"),   # Azure
    "cs":    ("#FFF1E6", "#C2410C"),   # Copilot Studio / AI
    "doc":   ("#FEF9C3", "#A16207"),   # artefacts / outputs
}

HEAD = """digraph G {
  graph [rankdir=LR, fontname="Helvetica", fontsize=20, labelloc=t, pad=0.4, nodesep=0.45, ranksep=0.7, bgcolor="white",
         label=<<b>%s</b><br/><font point-size="13" color="#6B7280">%s</font>>];
  node  [shape=box, style="rounded,filled", fontname="Helvetica", fontsize=12, margin="0.18,0.10", penwidth=1.4];
  edge  [fontname="Helvetica", fontsize=10, color="#4B5563", fontcolor="#374151", arrowsize=0.7];
"""

def n(id_, label, kind):
    fill, line = C[kind]
    return f'  {id_} [label=<{label}>, fillcolor="{fill}", color="{line}"];\n'

def cluster(name, title, kind, body):
    fill, line = C[kind]
    return (f'  subgraph cluster_{name} {{ label=<<b>{title}</b>>; fontsize=13; style="rounded,dashed"; '
            f'color="{line}"; fontcolor="{line}";\n{body}  }}\n')

KEY = '<br/><font point-size="11"><font color="#7C3AED">■ Power Platform</font>   <font color="#0369A1">■ Microsoft 365</font>   <font color="#0F766E">■ Azure</font>   <font color="#C2410C">■ Copilot / AI</font>   <font color="#A16207">■ Repo files / outputs</font></font>'
LEGEND = """  subgraph cluster_legend { label=<<b>Legend</b>>; fontsize=11; style="rounded"; color="#D1D5DB"; fontcolor="#6B7280";
    lg1 [label="Power Platform", fillcolor="#F3E8FF", color="#7C3AED", fontsize=10];
    lg2 [label="Microsoft 365", fillcolor="#E0F2FE", color="#0369A1", fontsize=10];
    lg3 [label="Azure", fillcolor="#E0F7F4", color="#0F766E", fontsize=10];
    lg4 [label="Copilot / AI", fillcolor="#FFF1E6", color="#C2410C", fontsize=10];
    lg1 -> lg2 -> lg3 -> lg4 [style=invis];
  }
"""

import re as _re
def _esc(t):
    return _re.sub(r"&(?![a-zA-Z]+;|#\d+;)", "&amp;", t) if t else t

def b(t, sub=None):
    t, sub = _esc(t), _esc(sub)
    return f"<b>{t}</b>" + (f'<br/><font point-size="10">{sub}</font>' if sub else "")

D = {}

# ---------- Day 4 QUOTA ----------
D["day-04-quota-estimate-agent"] = ("Day 4 · QUOTA — Quote-Of-Today Assistant",
  "Copilot Studio agent inside a standalone model-driven app, grounded in Dataverse",
  n("rep", b("Sales rep"), "user")
  + cluster("pp", "Power Platform environment", "pp",
      n("mda", b("Model-driven app", "standalone, agent pane"), "pp")
      + n("dv", b("Dataverse", "qta_pricelist · qta_opportunity<br/>qta_pricingrule · qta_quote"), "pp")
      + n("flow", b("Agent flow", "build quote · Word → PDF"), "pp"))
  + cluster("cs", "Copilot Studio", "cs",
      n("agent", b("QUOTA agent", "generative orchestration"), "cs")
      + n("mcp", b("Dataverse MCP server", "read_query · create_record"), "cs"))
  + cluster("m365", "Microsoft 365", "m365",
      n("appr", b("Teams approval", "discount &gt; rule threshold"), "m365")
      + n("pdf", b("Quote PDF", "SharePoint / email"), "doc"))
  + """  rep -> mda [label="asks for quote"];
  mda -> agent [label="in-app chat"];
  agent -> mcp [label="tool call"]; mcp -> dv [label="price lookup"];
  agent -> flow [label="create quote"];
  flow -> dv; flow -> appr [label="if over limit", style=dashed]; flow -> pdf;
""")

# ---------- Day 5 TRACE ----------
D["day-05-trace-sharepoint-ai-search"] = ("Day 5 · TRACE — Trusted Retrieval with Answers, Citations &amp; Evaluation",
  "Permission-trimmed RAG over SharePoint with cite-or-refuse answers",
  n("emp", b("Employee"), "user")
  + cluster("m365", "Microsoft 365", "m365",
      n("spfx", b("SPFx web part", "SharePoint / Teams"), "m365")
      + n("ret", b("Copilot Retrieval API", "POST /copilot/retrieval"), "m365")
      + n("gs", b("Graph Search API", "fallback, no Copilot licence"), "m365")
      + n("sp", b("SharePoint sites", "HR (open) · Finance (restricted)"), "m365"))
  + cluster("az", "Azure", "azure",
      n("entra", b("Entra ID", "On-Behalf-Of token"), "azure")
      + n("fn", b("Azure Function /ask", "Python, Flex Consumption"), "azure")
      + n("aoai", b("Azure OpenAI", "cite-or-refuse prompt"), "cs"))
  + n("eval", b("Eval harness", "eval-questions.csv"), "doc")
  + n("audit", b("Find-Oversharing.ps1", "PnP, run first"), "doc")
  + """  emp -> spfx [label="question"];
  spfx -> fn [label="question + user token", dir=both, taillabel="answer + citations", labelfontsize=9];
  fn -> entra [label="OBO token exchange", dir=both];
  fn -> ret [label="delegated"]; fn -> gs [style=dashed];
  ret -> sp [label="only what user can see"]; gs -> sp [style=dashed];
  fn -> aoai [label="chunks + question"];
  eval -> fn [label="10 test questions", style=dotted];
  audit -> sp [label="fix permissions", style=dotted];
""")

# ---------- Day 6 HIRE ----------
D["day-06-hire-hr-service-centre"] = ("Day 6 · HIRE — HR Intake, Requisition &amp; Enrolment",
  "Lists-first HR service centre with multistage (AI + human) approvals",
  n("mgr", b("Hiring manager"), "user")
  + n("hr", b("HR team"), "user")
  + cluster("m365", "Microsoft 365", "m365",
      n("form", b("Intake form", "Microsoft Forms / Lists form"), "m365")
      + n("req", b("SharePoint Lists", "Requisitions · ApprovalMatrix<br/>Candidates · OnboardingTasks"), "m365")
      + n("teams", b("Teams", "approval cards · notifications"), "m365")
      + n("planner", b("Planner", "onboarding checklist"), "m365"))
  + cluster("pp", "Power Platform", "pp",
      n("ms", b("Agent flow: multistage approval", "AI stage → Budget owner → HR"), "pp")
      + n("onb", b("Cloud flow", "status = Hired → create tasks"), "pp"))
  + n("ai", b("AI approval stage", "checks against ApprovalMatrix"), "cs")
  + n("bi", b("Power BI (optional)", "time-to-hire"), "doc")
  + """  mgr -> form [label="new role"]; form -> req;
  req -> ms [label="item created"]; ms -> ai [label="stage 1"];
  ms -> teams [label="stages 2-3"]; teams -> hr [style=dashed];
  ms -> req [label="status"]; req -> onb [label="Hired"]; onb -> planner;
  req -> bi [style=dotted];
""")

# ---------- Day 7 MATCH ----------
D["day-07-match-cv-shortlist"] = ("Day 7 · MATCH — Making Applicants &amp; Talent Click",
  "CV extraction and scoring with AI Builder prompts, recruiter stays in control",
  n("cand", b("Applicants"), "user")
  + n("rec", b("Recruiter"), "user")
  + cluster("m365", "Microsoft 365", "m365",
      n("lib", b("SharePoint library", "CVs (.docx / .pdf)"), "m365")
      + n("list", b("Candidates list", "structured fields + score"), "m365")
      + n("teams", b("Teams", "shortlist ready"), "m365"))
  + cluster("pp", "Power Platform", "pp",
      n("flow", b("Cloud flow", "file created trigger"), "pp")
      + n("p1", b("AI Builder prompt", "extract-cv → JSON"), "cs")
      + n("p2", b("AI Builder prompt", "score-candidate vs JD"), "cs"))
  + n("jd", b("job-description.md"), "doc")
  + """  cand -> lib [label="upload CV"]; lib -> flow; flow -> p1 [label="file text"];
  p1 -> flow [label="JSON", style=dashed]; flow -> p2; jd -> p2 [style=dotted];
  p2 -> list [label="score + reasons"]; list -> teams; teams -> rec;
  rec -> list [label="accept / override", style=dashed];
""")

# ---------- Day 2 SPRINKLE ----------
D["day-02-sprinkle-field-inspections"] = ("Day 2 · SPRINKLE — Site &amp; Property Reports, INspections, Kit for Landscape Experts",
  "Offline-first canvas app; report generated after sync",
  n("tech", b("Field technician", "phone / tablet"), "user")
  + n("client", b("Property client"), "user")
  + cluster("pp", "Power Platform", "pp",
      n("app", b("Canvas app (offline)", "checklist · photos · signature"), "pp")
      + n("prof", b("Offline profile", "Clients · Properties<br/>Controllers · Checklist items"), "pp")
      + n("dv", b("Dataverse", "Inspections · Findings"), "pp")
      + n("flow", b("Cloud flow", "Dataverse trigger: status = Submitted"), "pp"))
  + cluster("m365", "Microsoft 365", "m365",
      n("word", b("Word template", "Populate a Microsoft Word template"), "m365")
      + n("sp", b("SharePoint", "PDF archive"), "m365")
      + n("mail", b("Outlook", "report to client"), "m365"))
  + """  {rank=same; word; sp; mail; client;}
  tech -> app [label="no signal OK"]; app -> prof [label="local cache"];
  prof -> dv [label="sync when online"]; dv -> flow; flow -> word [label="fill"];
  word -> sp [label="convert to PDF"]; sp -> mail; mail -> client;
""")

# ---------- Day 8 WARDEN ----------
D["day-08-warden-agent-guard"] = ("Day 8 · WARDEN — Watch, Audit, Restrict &amp; Detect ENterprise agents",
  "Runtime guard for tool calls + tenant-wide agent inventory with risk score",
  n("user", b("Agent user"), "user")
  + n("admin", b("Platform admin"), "user")
  + cluster("cs", "Copilot Studio", "cs",
      n("agents", b("Agents", "generative orchestration"), "cs")
      + n("etd", b("External threat detection", "before each tool call"), "cs"))
  + cluster("az", "Azure", "azure",
      n("fn", b("Guard Function", "/validate · /analyze-tool-execution"), "azure")
      + n("rules", b("risk-rules.json", "R01-R06"), "doc")
      + n("arg", b("Azure Resource Graph", "PowerPlatformResources"), "azure")
      + n("kql", b("agents-query.kql", "risk score per agent"), "doc"))
  + n("tool", b("Tools / connectors", "email · delete · HTTP"), "pp")
  + n("rep", b("Report", "Power BI / Excel"), "m365")
  + """  user -> agents; agents -> etd [label="planned tool call"];
  etd -> fn [label="1 s timeout"]; rules -> fn [style=dotted];
  fn -> etd [label="blockAction", style=dashed];
  etd -> tool [label="if allowed"];
  admin -> arg [label="run query"]; kql -> arg [style=dotted]; arg -> rep [label="risky agents first"];
""")

# ---------- Day 9 SCOUT ----------
D["day-09-scout-agent-readiness-audit"] = ("Day 9 · SCOUT — Survey, Classify, Order Use-cases, Then build",
  "Advisory engagement: from interviews to a scored, costed backlog",
  n("st", b("Stakeholders", "business · IT · security"), "user")
  + cluster("in", "Discover", "m365",
      n("int", b("Interviews", "interview-questions.md"), "m365")
      + n("aud", b("Tenant audit", "audit-checklist.md<br/>licences · data · governance"), "m365"))
  + cluster("an", "Analyse", "pp",
      n("score", b("Use-case scoring", "use-case-scoring.csv<br/>value · feasibility · risk"), "pp")
      + n("cost", b("Cost model", "Copilot credits · licences"), "pp"))
  + cluster("out", "Decide", "cs",
      n("road", b("Ranked backlog", "quick wins → pilots"), "cs")
      + n("pilot", b("First pilot", "e.g. QUOTA / TRACE"), "cs"))
  + """  st -> int; st -> aud; int -> score; aud -> score; aud -> cost [style=dashed];
  score -> road; cost -> road; road -> pilot;
""")

def render(folder, title, sub, body):
    """Write architecture.dot/.svg/.png into REPO/folder. Reuse n(), b(), cluster() to build `body`."""
    dot = (HEAD % (title, sub + KEY)) + body + "}\n"
    if folder.startswith("day-05"):
        dot = dot.replace("rankdir=LR", "rankdir=TB")
    out = REPO / folder
    out.mkdir(parents=True, exist_ok=True)
    (out / "architecture.dot").write_text(dot)
    subprocess.run(["dot", "-Tsvg", "-o", str(out / "architecture.svg"), str(out / "architecture.dot")], check=True)
    subprocess.run(["dot", "-Tpng", "-Gdpi=150", "-o", str(out / "architecture.png"), str(out / "architecture.dot")], check=True)
    print("ok", folder)


if __name__ == "__main__":
    for folder, (title, sub, body) in D.items():
        render(folder, title, sub, body)
