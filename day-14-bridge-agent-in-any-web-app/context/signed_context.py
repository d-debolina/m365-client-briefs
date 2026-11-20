"""Server-side ticket context for the agent: never trust the browser.
The ITSM backend (plugin, PHP in real life) checks the technician may see the ticket, then signs a short-lived
context the chat client sends to the agent as an event. The MCP server verifies the signature AND re-checks rights.
"""
import hmac, hashlib, json, time, base64, os
SECRET = os.environ.get("BRIDGE_CONTEXT_KEY", "dev-only-change-me").encode()  # from Key Vault in production
def _b64(b): return base64.urlsafe_b64encode(b).decode().rstrip("=")
def _unb64(s): return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))
def sign_context(upn: str, ticket_id: int, ttl: int = 300) -> str:
    body = json.dumps({"upn": upn, "ticket": ticket_id, "exp": int(time.time()) + ttl}, separators=(",", ":")).encode()
    return _b64(body) + "." + _b64(hmac.new(SECRET, body, hashlib.sha256).digest())
def verify_context(token: str) -> dict:
    body_b64, sig_b64 = token.split(".")
    body = _unb64(body_b64)
    if not hmac.compare_digest(_unb64(sig_b64), hmac.new(SECRET, body, hashlib.sha256).digest()):
        raise PermissionError("bad signature")
    ctx = json.loads(body)
    if ctx["exp"] < time.time(): raise PermissionError("context expired")
    return ctx
