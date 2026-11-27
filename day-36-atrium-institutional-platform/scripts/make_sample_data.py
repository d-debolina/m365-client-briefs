"""Fictional sample data for Day 36 ATRIUM (Contoso Institute: an academic body plus a commercial arm, one tenant)."""
import csv, json, pathlib, random

D = pathlib.Path(__file__).resolve().parents[1] / "data"
D.mkdir(exist_ok=True)
random.seed(36)

# group, module, home (hub/site), main store, automation, premium?, phase, notes
modules = [
    ("Governance", "Executive & board", "Governance hub / Board site", "Library + Decisions list", "Meeting pack flow", "No", 2, "Private site, owners = executive office"),
    ("Governance", "Strategy & KPIs", "Governance hub / Strategy site", "KPI list", "Monthly KPI reminder", "No", 3, "Power BI Pro for authors"),
    ("Governance", "Minutes & decision tracking", "Governance hub / Board site", "Decisions list", "Action follow-up flow", "No", 2, "Decision log feeds KPIs"),
    ("Governance", "Policies & procedures", "Home hub / Policies site", "Policy library (versions + approval)", "Policy review cycle", "No", 1, "Bilingual titles, review date column"),
    ("Documents", "Document management", "Every site", "Content types + managed metadata", "-", "No", 1, "One term store, shared content types"),
    ("Documents", "Correspondence (in / out)", "Records hub / Correspondence site", "Correspondence list + letters library", "Reference number + approval flow", "No", 1, "THE pilot module in this post"),
    ("Documents", "Digital archive", "Records hub / Archive site", "Archive library + retention labels", "Move-on-close flow", "No", 3, "Retention via Microsoft 365 E3 labels"),
    ("Operations", "Human resources", "Operations hub / HR site", "HR requests list", "Multi-level approvals", "No", 2, "See Day 6 HIRE pattern"),
    ("Operations", "Finance & budgeting", "Operations hub / Finance site", "Budget requests list", "Approval with budget check", "No", 3, "ERP stays the system of record"),
    ("Operations", "Procurement & tendering", "Operations hub / Procurement site", "Requests + Tenders lists", "Approval + tender clock", "No", 3, "See Day 3 GRANT engine"),
    ("Operations", "Ticketing & service desk", "Operations hub / Service desk site", "Tickets list", "Routing + SLA escalation", "No", 2, "Teams adaptive cards"),
    ("Operations", "Approval engine (shared)", "Platform site", "Approval matrix list", "One reusable child flow", "No", 1, "Used by every module"),
    ("Academic", "Academic management", "Academic hub / Programmes site", "Programmes + Courses lists", "Course change approval", "No", 4, "SIS stays independent"),
    ("Academic", "Research & innovation", "Academic hub / Research site", "Projects + Grants lists", "Grant deadline reminders", "No", 4, ""),
    ("Academic", "Student affairs", "Academic hub / Student affairs site", "Cases list (no student records)", "Case routing", "No", 4, "Read-only SIS reporting only"),
    ("Academic", "Quality & accreditation", "Academic hub / Quality site", "Evidence library + Standards list", "Evidence request flow", "No", 4, ""),
    ("Knowledge", "Knowledge management", "Knowledge hub", "Wiki pages + FAQ list", "-", "No", 2, "Owners per topic, review dates"),
    ("Knowledge", "AI assistant", "Copilot Studio", "SharePoint knowledge (permission-trimmed)", "-", "Credits", 5, "After permissions are clean"),
]
with open(D / "modules.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["group", "module", "home", "main_store", "automation", "premium", "phase", "notes"])
    w.writerows(modules)

sites = {
    "tenant": "contosoinstitute.example",
    "languages": {"default": "en", "extra": ["ar"], "note": "Default language can't be changed after creation; pick it per site on purpose"},
    "hubs": [
        {"name": "Home", "type": "communication", "multilingual": True, "sites": ["Policies", "News"]},
        {"name": "Governance", "type": "communication", "multilingual": True, "sites": ["Board (private team)", "Strategy"]},
        {"name": "Records", "type": "team", "multilingual": False, "sites": ["Correspondence", "Archive"]},
        {"name": "Operations", "type": "communication", "multilingual": True, "sites": ["HR", "Finance", "Procurement", "Service desk"]},
        {"name": "Academic", "type": "communication", "multilingual": True, "sites": ["Programmes", "Research", "Student affairs", "Quality"]},
        {"name": "Knowledge", "type": "communication", "multilingual": True, "sites": []},
    ],
    "entities": ["Contoso Institute (academic)", "Contoso Services (commercial)"],
    "entity_split": "Entity is a managed-metadata column + Entra security groups, not separate tenants",
}
(D / "sites.json").write_text(json.dumps(sites, indent=2, ensure_ascii=False), encoding="utf-8")

# approval matrix used by the shared approval engine
matrix = [
    ("Outgoing letter", "Contoso Institute", "Head of unit", "Secretary-General's office", "", 2),
    ("Outgoing letter", "Contoso Services", "Head of unit", "Managing director", "", 2),
    ("Incoming letter", "*", "Registry clerk (assign)", "", "", 1),
    ("Internal memo", "*", "Head of unit", "", "", 3),
    ("Policy", "*", "Policy owner", "Legal", "Executive board", 5),
]
with open(D / "approval-matrix.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["doc_type", "entity", "stage1", "stage2", "stage3", "escalate_after_days"])
    w.writerows(matrix)

subjects = [
    ("Invitation to accreditation visit", "دعوة لزيارة الاعتماد"),
    ("Request for course catalogue", "طلب دليل المقررات"),
    ("Partnership agreement draft", "مسودة اتفاقية شراكة"),
    ("Annual budget submission", "تقديم الميزانية السنوية"),
    ("Tender clarification", "توضيح بشأن المناقصة"),
    ("Visiting scholar nomination", "ترشيح باحث زائر"),
    ("Exam schedule notice", "إشعار جدول الامتحانات"),
    ("Facilities maintenance plan", "خطة صيانة المرافق"),
]
parties = ["Fabrikam University", "Northwind Ministry Liaison Office", "Tailspin Accreditation Board",
           "Wide World Importers", "Adventure Works Foundation", "Litware Research Council"]
rows = []
for i in range(1, 31):
    direction = random.choice(["Outgoing", "Incoming", "Internal memo"])
    en, ar = random.choice(subjects)
    rows.append({
        "draft_id": f"D{i:03d}", "direction": direction,
        "entity": random.choice(["Contoso Institute", "Contoso Services"]),
        "subject_en": en, "subject_ar": ar,
        "party": random.choice(parties) if direction != "Internal memo" else "Internal",
        "date": f"2027-01-{random.randint(4, 29):02d}",
        "classification": random.choice(["Internal", "Internal", "Confidential"]),
        "owner_unit": random.choice(["Registry", "Quality", "Finance", "Research", "Executive office"]),
    })
rows.sort(key=lambda r: r["date"])
with open(D / "correspondence-drafts.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print("sample data written to", D)
