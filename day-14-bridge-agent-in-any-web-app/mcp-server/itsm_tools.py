"""ITSM tools exposed to the agent through an MCP server (logic only; wrap with the official MCP Python SDK).
Rule: the tool runs AS THE TECHNICIAN (identity from the validated Entra token, on-behalf-of), never as a broad service account.
"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "context"))
from signed_context import verify_context
ROOT = pathlib.Path(__file__).resolve().parents[1] / "data"
TICKETS = {t["id"]: t for t in json.loads((ROOT / "tickets.json").read_text())}
TECHS = {t["upn"]: t for t in json.loads((ROOT / "technicians.json").read_text())}
AUDIT = []

def _authorise(caller_upn: str, ticket_id: int) -> dict:
    tech = TECHS.get(caller_upn)
    t = TICKETS.get(ticket_id)
    if not tech or not t or t["entity"] not in tech["entities"]:
        AUDIT.append(("DENY", caller_upn, ticket_id)); raise PermissionError("not allowed")   # same error for 'missing' and 'forbidden'
    AUDIT.append(("ALLOW", caller_upn, ticket_id)); return t

def get_ticket_summary(caller_upn: str, context_token: str) -> dict:
    """caller_upn comes from the validated access token (OBO), context_token from the signed page context."""
    ctx = verify_context(context_token)
    if ctx["upn"] != caller_upn: raise PermissionError("context belongs to another user")
    t = _authorise(caller_upn, ctx["ticket"])
    return {"id": t["id"], "title": t["title"], "status": t["status"], "priority": t["priority"], "followups": t["followups"][-5:]}

def search_similar(caller_upn: str, text: str) -> list:
    """Only searches tickets in the caller's entities."""
    ents = set(TECHS[caller_upn]["entities"])
    return [{"id": t["id"], "title": t["title"]} for t in TICKETS.values() if t["entity"] in ents and any(w in t["title"].lower() for w in text.lower().split())][:5]
