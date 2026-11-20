"""Automate a Purview eDiscovery case with Microsoft Graph (v1.0 /security/cases/ediscoveryCases).
App registration in the CUSTOMER tenant (cross-tenant apps can't do this), application permission eDiscovery.ReadWrite.All,
admin consent, and the app added to an eDiscovery role group as required. Env: TENANT_ID, CLIENT_ID, CLIENT_SECRET.
Usage: pip install msal requests && python scripts/ediscovery_case.py
"""
import os, time, msal, requests
G = "https://graph.microsoft.com/v1.0/security/cases/ediscoveryCases"
app = msal.ConfidentialClientApplication(os.environ["CLIENT_ID"], authority=f"https://login.microsoftonline.com/{os.environ['TENANT_ID']}",
                                         client_credential=os.environ["CLIENT_SECRET"])
tok = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])["access_token"]
H = {"Authorization": f"Bearer {tok}", "Content-Type": "application/json"}
def post(url, body=None):
    r = requests.post(url, headers=H, json=body or {}); r.raise_for_status(); return r.json() if r.content else {}

case = post(G, {"displayName": "VAULT PoC - Fabrikam dispute", "description": "Third-party archive items imported via data connector"})
cid = case["id"]; print("case", cid)
for upn in ["lena.huber@contoso.example", "marco.rossi@contoso.example"]:
    c = post(f"{G}/{cid}/custodians", {"email": upn})
    post(f"{G}/{cid}/custodians/{c['id']}/userSources", {"email": upn, "includedSources": "mailbox"})
    print("custodian", upn)
post(f"{G}/{cid}/custodians/applyHold", {"ids": []})  # or per custodian: /custodians/{id}/applyHold
s = post(f"{G}/{cid}/searches", {"displayName": "Fabrikam + contract", "contentQuery": '(participants:"fabrikam.example") AND (subject:contract)'})
post(f"{G}/{cid}/searches/{s['id']}/estimateStatistics")
print("search started:", s["id"], "→ poll lastEstimateStatisticsOperation, then add to review set / export")
