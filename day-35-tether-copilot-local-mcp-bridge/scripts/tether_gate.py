"""TETHER policy gate: the checks the local bridge runs on every tool call, before the Windows app sees it.

- tools/list is filtered by the caller's role (an agent can only misuse a tool it has)
- workspaces are scoped per customer, scripts come from an allowlist
- every tool that is not readOnly needs a two-step confirmation: the first call returns a short-lived
  confirmation code and a plain-language summary; the agent must show it, and only a second call with
  confirm=<code> from the SAME user, for the SAME arguments, runs it
Run:  python scripts/tether_gate.py   (prints a demo conversation and writes out/audit-log.jsonl)
"""
import csv, hashlib, hmac, json, pathlib, time

ROOT = pathlib.Path(__file__).resolve().parents[1]
SECRET = b"demo-only-secret-rotate-me"   # real build: per-install key from DPAPI / Key Vault, never in code


def load():
    tools = {t["name"]: t for t in json.loads((ROOT / "data/tools.json").read_text())}
    policy = json.loads((ROOT / "data/policy.json").read_text())
    with open(ROOT / "data/users.csv") as f:
        users = {r["upn"].lower(): r for r in csv.DictReader(f)}
    return tools, policy, users


class Gate:
    def __init__(self, now=time.time):
        self.tools, self.policy, self.users = load()
        self.now = now
        self.audit = []

    # ---- discovery -------------------------------------------------------------
    def list_tools(self, upn):
        user = self.users.get(upn.lower())
        if not user:
            return []
        allowed = self.policy["roles"][user["role"]]
        return [{k: v for k, v in self.tools[t].items() if k != "args"} for t in allowed]

    # ---- confirmation codes ----------------------------------------------------
    def _code(self, upn, tool, args, issued):
        msg = json.dumps([upn.lower(), tool, args, issued], sort_keys=True).encode()
        return f"{issued}.{hmac.new(SECRET, msg, hashlib.sha256).hexdigest()[:10]}"

    def _code_ok(self, upn, tool, args, code):
        try:
            issued = int(code.split(".")[0])
        except (ValueError, AttributeError):
            return False
        fresh = self.now() - issued <= self.policy["confirmation_ttl_seconds"]
        return fresh and hmac.compare_digest(code, self._code(upn, tool, args, issued))

    # ---- the call ---------------------------------------------------------------
    def call(self, upn, tool, args, confirm=None):
        result = self._decide(upn, tool, args, confirm)
        self.audit.append({"at": int(self.now()), "user": upn, "tool": tool, "args": args, "outcome": result["status"]})
        return result

    def _decide(self, upn, tool, args, confirm):
        user = self.users.get(upn.lower())
        if not user:
            return {"status": "denied", "reason": "Unknown user. Ask your IT admin to assign a TETHER role."}
        if tool not in self.tools:
            return {"status": "denied", "reason": f"No tool called {tool}."}
        if tool not in self.policy["roles"][user["role"]]:
            return {"status": "denied", "reason": f"Your role ({user['role']}) can't use {tool}."}
        ws = args.get("workspace")
        if ws not in self.policy["workspaces"].get(user["customer"], []):
            return {"status": "denied", "reason": f"Workspace '{ws}' isn't approved for {user['customer']}."}
        if tool == "run_script" and args.get("script") not in self.policy["approved_scripts"]:
            return {"status": "denied", "reason": "That script isn't in the approved catalogue."}
        if "path" in args and (".." in args["path"] or args["path"].startswith(("/", "\\")) or ":" in args["path"]):
            return {"status": "denied", "reason": "Paths must stay inside the workspace."}

        if not self.tools[tool]["annotations"].get("readOnlyHint", False):
            if confirm is None:
                code = self._code(upn, tool, args, int(self.now()))
                return {"status": "needs_confirmation", "confirm_code": code,
                        "summary": f"{self.tools[tool]['title']} in '{ws}' with {json.dumps({k: v for k, v in args.items() if k != 'workspace'})}. "
                                   f"Reply 'yes' to run it. The code expires in {self.policy['confirmation_ttl_seconds']} seconds."}
            if not self._code_ok(upn, tool, args, confirm):
                return {"status": "denied", "reason": "Confirmation code is wrong, expired, or for different arguments. Ask again."}
        return {"status": "allowed", "forward_to_app": {"tool": tool, "args": args, "run_as": upn}}

    def save_audit(self, path=ROOT / "out/audit-log.jsonl"):
        path.parent.mkdir(exist_ok=True)
        path.write_text("".join(json.dumps(a) + "\n" for a in self.audit))


if __name__ == "__main__":
    g = Gate()
    print("Tools Ben (Reader) sees:", [t["name"] for t in g.list_tools("ben.okafor@contoso.example")])
    print("Tools Chloe (Admin) sees:", [t["name"] for t in g.list_tools("chloe.martin@contoso.example")])
    aisha = "aisha.rahman@contoso.example"
    print(g.call(aisha, "search_files", {"workspace": "finance-exports", "query": "march"}))
    step1 = g.call(aisha, "set_variable", {"workspace": "nightly-jobs", "name": "RETRY_LIMIT", "value": "5"})
    print(step1)
    print(g.call(aisha, "set_variable", {"workspace": "nightly-jobs", "name": "RETRY_LIMIT", "value": "9"}, confirm=step1["confirm_code"]))
    print(g.call(aisha, "set_variable", {"workspace": "nightly-jobs", "name": "RETRY_LIMIT", "value": "5"}, confirm=step1["confirm_code"]))
    print(g.call(aisha, "search_files", {"workspace": "orders", "query": "*"}))
    g.save_audit()
    print("audit log:", len(g.audit), "entries → out/audit-log.jsonl")
