"""TRACE – permission-trimmed answers over SharePoint (Azure Functions, Python v2 model).

Flow: SPFx web part -> this Function (user token) -> OBO token for Graph ->
Microsoft 365 Copilot Retrieval API (security-trimmed extracts) -> LLM with cite-or-refuse prompt.
Fill in settings in local.settings.json. Sample code for a blog demo, not production.
"""
import json, os, logging
import azure.functions as func
import msal, requests

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

CCA = msal.ConfidentialClientApplication(
    os.environ["CLIENT_ID"],
    authority=f"https://login.microsoftonline.com/{os.environ['TENANT_ID']}",
    client_credential=os.environ["CLIENT_SECRET"],  # use a certificate / Key Vault reference in real life
)

SYSTEM_PROMPT = """You answer staff questions using ONLY the extracts provided.
- Cite every fact as [n] where n is the extract number.
- If the extracts do not contain the answer, reply exactly: "I couldn't find that in the documents you can access."
- Never guess. Never use outside knowledge."""

def obo_graph_token(user_token: str) -> str:
    r = CCA.acquire_token_on_behalf_of(user_token, scopes=["https://graph.microsoft.com/.default"])
    if "access_token" not in r:
        raise RuntimeError(r.get("error_description"))
    return r["access_token"]

def retrieve(graph_token: str, question: str):
    body = {"queryString": question, "dataSource": "sharePoint",
            "resourceMetadata": ["title"], "maximumNumberOfResults": 8}
    r = requests.post("https://graph.microsoft.com/v1.0/copilot/retrieval",
                      headers={"Authorization": f"Bearer {graph_token}"}, json=body, timeout=30)
    r.raise_for_status()
    hits = r.json().get("retrievalHits", [])
    extracts = []
    for h in hits:
        for e in h.get("extracts", []):
            extracts.append({"url": h["webUrl"], "title": h.get("resourceMetadata", {}).get("title", ""), "text": e["text"]})
    return extracts

def answer(question: str, extracts):
    if not extracts:
        return "I couldn't find that in the documents you can access."
    context = "\n\n".join(f"[{i+1}] ({x['title']}) {x['text']}" for i, x in enumerate(extracts))
    r = requests.post(os.environ["AOAI_ENDPOINT"],  # Azure OpenAI chat completions URL
                      headers={"api-key": os.environ["AOAI_KEY"]},
                      json={"messages": [{"role": "system", "content": SYSTEM_PROMPT},
                                         {"role": "user", "content": f"Extracts:\n{context}\n\nQuestion: {question}"}],
                            "temperature": 0}, timeout=60)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

@app.route(route="ask", methods=["POST"])
def ask(req: func.HttpRequest) -> func.HttpResponse:
    auth = req.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return func.HttpResponse("Unauthorized", status_code=401)
    question = (req.get_json() or {}).get("question", "")[:1500]
    try:
        extracts = retrieve(obo_graph_token(auth[7:]), question)
        reply = answer(question, extracts)
        sources = [{"n": i+1, "title": x["title"], "url": x["url"]} for i, x in enumerate(extracts)]
        logging.info(json.dumps({"q_len": len(question), "hits": len(extracts)}))  # no raw question logged
        return func.HttpResponse(json.dumps({"answer": reply, "sources": sources}), mimetype="application/json")
    except Exception as ex:
        logging.exception("ask failed")
        return func.HttpResponse(json.dumps({"error": str(ex)}), status_code=500, mimetype="application/json")
