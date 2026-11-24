"""Azure Function (Python v2 model) that runs the CREW planning engine against Dataverse.

The custom API crew_RecalculateDemand calls this endpoint (or a scheduled flow does). It reads demand, crew and
leave through the Dataverse Web API with a managed identity registered as an application user, then writes one
crew_weeklycapacity row per week and skill. Requirements: azure-functions, azure-identity, requests.
Sketch only: add paging, retries and batching before production.
"""
import os, json, datetime as dt
import azure.functions as func
import requests
from azure.identity import DefaultAzureCredential
from planning_engine import skill_gap

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)
ORG = os.environ["DATAVERSE_URL"]            # e.g. https://<your-dev-org>.crm.dynamics.com  (environment variable)
API = f"{ORG}/api/data/v9.2"


def _headers():
    token = DefaultAzureCredential().get_token(f"{ORG}/.default").token
    return {"Authorization": f"Bearer {token}", "Accept": "application/json",
            "OData-MaxVersion": "4.0", "OData-Version": "4.0", "Content-Type": "application/json"}


def _get(path):
    r = requests.get(f"{API}/{path}", headers=_headers(), timeout=30); r.raise_for_status()
    return r.json()["value"]


@app.route(route="recalculate", methods=["POST"])
def recalculate(req: func.HttpRequest) -> func.HttpResponse:
    body = req.get_json() if req.get_body() else {}
    scenario = body.get("scenarioId")       # optional What-if scenario: demand rows tagged with this scenario
    flt = f"&$filter=_crew_scenarioid_value eq {scenario}" if scenario else "&$filter=_crew_scenarioid_value eq null"
    demand = [{"WeekStart": d["crew_weekstart"][:10], "Kind": "Skill", "Item": d["crew_skilllevel@OData.Community.Display.V1.FormattedValue"],
               "Quantity": d["crew_hours"]}
              for d in _get("crew_demands?$select=crew_weekstart,crew_skilllevel,crew_hours" + flt)]
    crew = [{"CrewId": c["crew_crewmemberid"], "SkillLevel": c["crew_skilllevel@OData.Community.Display.V1.FormattedValue"],
             "HoursPerWeek": c["crew_hoursperweek"]} for c in _get("crew_crewmembers?$select=crew_skilllevel,crew_hoursperweek")]
    leave = [{"CrewId": l["_crew_crewmemberid_value"], "WeekStart": l["crew_weekstart"][:10], "HoursOff": l["crew_hoursoff"]}
             for l in _get("crew_leaves?$select=_crew_crewmemberid_value,crew_weekstart,crew_hoursoff")]
    result = skill_gap(demand, crew, leave)
    rows = [{"week": w, "skill": s, **v} for (w, s), v in result.items()]
    # Write-back to crew_weeklycapacity omitted for brevity: upsert by alternate key (week + skill + scenario).
    return func.HttpResponse(json.dumps({"calculatedAt": dt.datetime.utcnow().isoformat() + "Z", "rows": rows}),
                             mimetype="application/json")
