import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
import grant_engine as g

FORMS, MATRIX = g.load("forms-catalogue.csv"), g.load("approval-matrix.csv")
HOLDERS, DELEG, BUDGET = g.load("role-holders.csv"), g.load("delegations.csv"), g.load("budget-lines.csv")
REQS = {r["request_id"]: r for r in g.load("sample-requests.csv")}


def run(rid):
    return g.resolve(REQS[rid], FORMS, MATRIX, HOLDERS, DELEG, BUDGET)


def test_sixteen_forms_two_releases():
    assert len(FORMS) == 16
    assert sum(f["release"] == "1" for f in FORMS) == 5


def test_amount_adds_stages():
    small = g.route_rules(MATRIX, "PROCURE", "Logistics", "PRJ-EDU", 900)
    big = g.route_rules(MATRIX, "PROCURE", "Logistics", "PRJ-EDU", 30000)
    assert [r["stage"] for r in small] == ["1", "2"]
    assert [r["approver_role"] for r in big][-1] == "COUNTRY_DIRECTOR"


def test_project_rule_adds_donor_compliance():
    roles = [s["role"] for s in run("PR-01004")["stages"]]
    assert "DONOR_COMPLIANCE" in roles and "FINANCE_MANAGER" in roles


def test_budget_blocks_overspend():
    r = run("TA-01003")
    assert r["budget_ok"] is False and r["available"] == 300


def test_delegation_applies_in_window_only():
    in_window = run("PR-01005")["stages"]
    assert in_window[0]["approver"].startswith("amina") and in_window[0]["note"] == "Field visit"
    outside = run("TA-01002")["stages"]
    assert outside[1]["approver"].startswith("omar")


def test_no_self_approval_and_no_duplicates():
    for rid in REQS:
        r = run(rid)
        people = [s["approver"] for s in r["stages"]]
        assert REQS[rid]["requester"] not in people
        assert len(people) == len(set(people))
