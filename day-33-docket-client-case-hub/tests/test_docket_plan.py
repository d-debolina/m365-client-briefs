import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
import docket_plan as d

STAFF, CASES, ALLOC = d.load("staff.csv"), d.load("cases.csv"), d.load("allocations.csv")
PLAN = d.permission_plan(CASES, STAFF)


def test_only_restricted_cases_break_inheritance():
    for row in PLAN:
        assert row["unique_scopes_in_case_files"] == (1 if row["restricted"] == "Yes" else 0)


def test_external_people_never_in_case_files():
    for row in PLAN:
        assert "Case files" not in row["external_access"]
        if row["external_access"] != "none":
            assert row["external_access"].startswith("Client Share site")


def test_scope_projection_is_finite_and_safe():
    share, per_year, years = d.scope_projection(PLAN, cases_per_year=400)
    assert 0 < share < 1 and years > 10


def test_allocation_flags_over_and_low():
    dash = {r["staff_id"]: r for r in d.allocation(ALLOC, STAFF, "2027-04-05")}
    assert dash["S07"]["flag"] == "OVER"
    assert any(r["flag"] == "LOW" for r in dash.values())


def test_every_open_case_has_a_lead_allocation():
    open_cases = {c["case_id"]: c["lead"] for c in CASES if c["status"] == "Open"}
    allocated = {(a["case_id"], a["staff_id"]) for a in ALLOC}
    assert all((cid, lead) in allocated for cid, lead in open_cases.items())
