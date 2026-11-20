"""Tiny mock of the fictional Fabrikam CRM for local testing (no dependencies).
Run: python mock_crm.py  → http://localhost:8080/api/v1/merchants/MER-10007  (header X-API-Key: demo-key)
For the real demo, deploy any equivalent (e.g. an Azure Function) behind HTTPS, because custom connectors need a public host.
"""
import json, pathlib, http.server, urllib.parse, datetime
DATA = json.loads((pathlib.Path(__file__).resolve().parents[1]/"data"/"merchants.json").read_text())
TASKS = {}
class H(http.server.BaseHTTPRequestHandler):
    def _send(self, code, obj):
        self.send_response(code); self.send_header("Content-Type","application/json"); self.end_headers()
        self.wfile.write(json.dumps(obj).encode())
    def _auth(self):
        if self.headers.get("X-API-Key") != "demo-key": self._send(401, {"error":"invalid key"}); return False
        return True
    def do_GET(self):
        if not self._auth(): return
        u = urllib.parse.urlparse(self.path); p = u.path.split("/")
        if u.path == "/api/v1/merchants":
            q = urllib.parse.parse_qs(u.query).get("q", [""])[0].lower()
            return self._send(200, [m for m in DATA if q in m["legalName"].lower()])
        if len(p) >= 5 and p[3] == "merchants":
            m = next((m for m in DATA if m["merchantId"] == p[4]), None)
            if not m: return self._send(404, {"error":"not found"})
            if len(p) == 6 and p[5] == "tasks": return self._send(200, TASKS.get(p[4], []))
            return self._send(200, m)
        self._send(404, {"error":"unknown path"})
    def do_POST(self):
        if not self._auth(): return
        p = self.path.split("/"); body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        t = {"taskId": f"TSK-{len(sum(TASKS.values(), []))+1:04d}", "title": body["title"][:120], "dueDate": body["dueDate"], "status": "Open"}
        TASKS.setdefault(p[4], []).append(t); self._send(201, t)
http.server.HTTPServer(("", 8080), H).serve_forever()
