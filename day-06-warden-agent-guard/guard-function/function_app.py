"""WARDEN – minimal external threat-detection endpoint for Copilot Studio (demo only).

Implements the two endpoints Copilot Studio calls: POST /validate and POST /analyze-tool-execution.
Check the current request schema on Microsoft Learn ("Build a runtime threat detection system
for Copilot Studio agents") before using; field names below are illustrative.
Auth: Copilot Studio calls with an Entra token (federated identity credential). Validate it in
production. This sample only shows the decision logic.
"""
import json, re
import azure.functions as func

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

ALLOWED_DOMAINS = {"contoso.example"}
BLOCKED_TOOL_WORDS = ("delete",)

@app.route(route="validate", methods=["POST"])
def validate(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(json.dumps({"isSuccessful": True, "status": "OK"}), mimetype="application/json")

@app.route(route="analyze-tool-execution", methods=["POST"])
def analyze(req: func.HttpRequest) -> func.HttpResponse:
    body = req.get_json()
    text = json.dumps(body).lower()
    tool = json.dumps(body.get("toolDefinition", {})).lower()

    if any(w in tool for w in BLOCKED_TOOL_WORDS):
        return _block(101, "Delete operations are not allowed for agents in this environment.")
    for email in re.findall(r"[\w.+-]+@([\w-]+\.[\w.]+)", text):
        if email not in ALLOWED_DOMAINS:
            return _block(112, f"External recipient domain '{email}' is not allowed.")
    return func.HttpResponse(json.dumps({"blockAction": False}), mimetype="application/json")

def _block(code, reason):
    return func.HttpResponse(json.dumps({"blockAction": True, "reasonCode": code, "reason": reason}),
                             mimetype="application/json")
