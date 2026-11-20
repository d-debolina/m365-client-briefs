"""Per-tenant tool allow-list + human handoff (sketch)."""
import json, pathlib
TENANTS = json.loads((pathlib.Path(__file__).resolve().parents[1] / "tenants" / "tenants.json").read_text())
def allowed_tools(tenant_id): return set(TENANTS[tenant_id]["tools"])
def call_tool(tenant_id, name, **kw):
    if name not in allowed_tools(tenant_id): raise PermissionError(f"tool {name} not enabled for {tenant_id}")
    return {"tool": name, "tenant": tenant_id, "args": kw, "result": "ok (stub)"}
def handoff(tenant_id, conversation_summary, reason):
    target = TENANTS[tenant_id]["handoff"]
    return {"handoff_to": target, "summary": conversation_summary, "reason": reason}   # never cross-tenant
