"""GRANT engine rules in plain Python, so you can test the approval matrix before building any flow.

The same three rules run inside the Power Automate child flow "GRANT - Resolve route":
1. Pick the matrix rows for the request's process, department, project and amount.
   Rows for a specific department/project win over '*' rows at the same stage.
2. Turn each approver role into a person: role holder -> active delegation -> (alternate is used only on escalation).
3. Budget check: available = budget - committed - actual. The request may go ahead only if amount <= available.

Run:  python scripts/grant_engine.py        (replays data/sample-requests.csv)
"""
import csv, datetime as dt, pathlib

DATA = pathlib.Path(__file__).resolve().parents[1] / "data"


def load(name):
    with open(DATA / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _match(value, pattern):
    return pattern == "*" or pattern == value


def _specificity(row):
    return (row["department"] != "*") + (row["project"] != "*")


def route_rules(matrix, process, department, project, amount):
    """Return one matrix row per stage, most specific row winning, ordered by stage."""
    hits = [r for r in matrix
            if r["process"] == process
            and _match(department, r["department"]) and _match(project, r["project"])
            and float(r["min_amount"]) <= amount <= float(r["max_amount"])]
    best = {}
    for r in hits:
        st = int(r["stage"])
        if st not in best or _specificity(r) > _specificity(best[st]):
            best[st] = r
    return [best[s] for s in sorted(best)]


def holder_for(role_holders, role, department):
    exact = [r for r in role_holders if r["role"] == role and r["department"] == department]
    anyd = [r for r in role_holders if r["role"] == role and r["department"] == "*"]
    rows = exact or anyd
    if not rows:
        raise LookupError(f"No holder for role {role} in {department}")
    return rows[0]["holder"], rows[0]["alternate"]


def apply_delegation(delegations, person, on_date):
    for d in delegations:
        if d["delegator"] == person and d["start"] <= on_date <= d["end"]:
            return d["delegate"], d["reason"]
    return person, None


def budget_check(budget_lines, budget_line, amount):
    if not budget_line:
        return True, None
    row = next((b for b in budget_lines if b["budget_line"] == budget_line), None)
    if row is None:
        return False, None
    available = float(row["budget_usd"]) - float(row["committed_usd"]) - float(row["actual_usd"])
    return amount <= available, available


def resolve(request, forms, matrix, role_holders, delegations, budget_lines):
    form = next(f for f in forms if f["form_code"] == request["form_code"])
    amount = float(request["amount_usd"] or 0)
    result = {"request_id": request["request_id"], "process": form["process"], "stages": [], "budget_ok": True,
              "available": None}
    if form["budget_check"] == "yes":
        ok, available = budget_check(budget_lines, request["budget_line"], amount)
        result["budget_ok"], result["available"] = ok, available
        if not ok:
            return result
    seen = set()
    for rule in route_rules(matrix, form["process"], request["department"], request["project"], amount):
        holder, alternate = holder_for(role_holders, rule["approver_role"], request["department"])
        person, reason = apply_delegation(delegations, holder, request["submitted_on"])
        # Never ask the requester to approve their own request, and never ask the same person twice
        if person == request["requester"] or person in seen:
            why = "requester can't approve own request" if person == request["requester"] else "already approved an earlier stage"
            person, reason = alternate, f"{why} - alternate used"
            if person == request["requester"] or person in seen:
                person, reason = "NEEDS_ADMIN", "no valid approver - flag to GRANT admin"
        seen.add(person)
        result["stages"].append({"stage": int(rule["stage"]), "role": rule["approver_role"], "approver": person,
                                 "rule": rule["rule_id"], "note": reason, "on_reject": rule["on_reject"]})
    return result


def main():
    forms, matrix = load("forms-catalogue.csv"), load("approval-matrix.csv")
    holders, delegations, budget = load("role-holders.csv"), load("delegations.csv"), load("budget-lines.csv")
    for req in load("sample-requests.csv"):
        r = resolve(req, forms, matrix, holders, delegations, budget)
        print(f"\n{r['request_id']}  ({r['process']}, {req['amount_usd']} USD)")
        if not r["budget_ok"]:
            print(f"  BLOCKED by budget check: only {r['available']:.0f} USD left on {req['budget_line']}")
            continue
        for s in r["stages"]:
            note = f"  [{s['note']}]" if s["note"] else ""
            print(f"  stage {s['stage']}: {s['role']:<20} -> {s['approver']}  ({s['rule']}){note}")


if __name__ == "__main__":
    main()
