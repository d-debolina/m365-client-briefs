"""ECHO retrieval with hard tenant isolation (logic sketch, provider-agnostic).
Production: Azure AI Search with ONE index + a filterable `tenantId` field applied on EVERY query (security filter),
or one index per tenant for strict isolation / per-tenant scaling. The tenantId ALWAYS comes from the authenticated
token (server side), never from the chat message.
"""
import pathlib, re
ROOT = pathlib.Path(__file__).resolve().parents[1] / "kb"
def _docs():
    for p in ROOT.glob("*/*.md"):
        yield {"tenantId": p.parent.name, "title": p.stem, "text": p.read_text()}
DOCS = list(_docs())
def search(tenant_id: str, query: str, k: int = 3):
    if not tenant_id: raise PermissionError("no tenant")
    words = set(re.findall(r"\w+", query.lower()))
    scored = [(len(words & set(re.findall(r"\w+", d["text"].lower() + " " + d["title"]))), d) for d in DOCS if d["tenantId"] == tenant_id]   # filter FIRST
    return [d for s, d in sorted(scored, key=lambda x: -x[0]) if s > 0][:k]
