"""Release-blocking negative tests: run with  python -m pytest tests -q"""
import sys, pathlib, time, pytest
root = pathlib.Path(__file__).resolve().parents[1]
sys.path[:0] = [str(root / "mcp-server"), str(root / "context")]
import itsm_tools as it
from signed_context import sign_context

def first_ticket(entity): return next(t["id"] for t in it.TICKETS.values() if t["entity"] == entity)

def test_own_entity_allowed():
    tid = first_ticket("E1")
    assert it.get_ticket_summary("ana@msp.example", sign_context("ana@msp.example", tid))["id"] == tid

def test_other_customer_denied():                     # Ben only has E3
    tid = first_ticket("E1")
    with pytest.raises(PermissionError): it.get_ticket_summary("ben@msp.example", sign_context("ben@msp.example", tid))

def test_browser_tampered_ticket_id_denied():         # Ana edits the ticket id in the browser
    tok = sign_context("ana@msp.example", first_ticket("E1"))
    body, sig = tok.split(".")
    import base64, json
    d = json.loads(base64.urlsafe_b64decode(body + "=="))
    d["ticket"] = first_ticket("E3")
    forged = base64.urlsafe_b64encode(json.dumps(d).encode()).decode().rstrip("=") + "." + sig
    with pytest.raises(PermissionError): it.get_ticket_summary("ana@msp.example", forged)

def test_replayed_context_from_other_user_denied():   # Ben replays Ana's context
    tok = sign_context("ana@msp.example", first_ticket("E1"))
    with pytest.raises(PermissionError): it.get_ticket_summary("ben@msp.example", tok)

def test_expired_context_denied():
    tok = sign_context("ana@msp.example", first_ticket("E1"), ttl=-1)
    with pytest.raises(PermissionError): it.get_ticket_summary("ana@msp.example", tok)

def test_search_never_crosses_entities():
    res = it.search_similar("ben@msp.example", "printer vpn outlook backup mfa teams laptop phishing disk mailbox")
    assert all(it.TICKETS[r["id"]]["entity"] == "E3" for r in res)

def test_denials_are_audited():
    assert any(a[0] == "DENY" for a in it.AUDIT)
