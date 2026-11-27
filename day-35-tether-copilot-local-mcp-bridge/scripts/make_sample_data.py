"""Creates the fictional sample data for Day 35 TETHER (Fabrikam Automate, a Windows CLI tool)."""
import csv, json, pathlib

D = pathlib.Path(__file__).resolve().parents[1] / "data"
D.mkdir(exist_ok=True)

# Tools the local MCP server exposes. Annotations follow the MCP spec (readOnlyHint / destructiveHint).
tools = [
    {"name": "search_files", "title": "Search files", "description": "Find files under an approved workspace folder by name or text.",
     "annotations": {"readOnlyHint": True}, "args": ["workspace", "query"]},
    {"name": "get_file_info", "title": "Get file info", "description": "Return size, modified date, owner and hash of one file in an approved workspace.",
     "annotations": {"readOnlyHint": True}, "args": ["workspace", "path"]},
    {"name": "list_variables", "title": "List variables", "description": "List automation variables for a workspace.",
     "annotations": {"readOnlyHint": True}, "args": ["workspace"]},
    {"name": "set_variable", "title": "Update a variable", "description": "Change the value of one automation variable. Changes data.",
     "annotations": {"readOnlyHint": False, "destructiveHint": False}, "args": ["workspace", "name", "value"]},
    {"name": "run_script", "title": "Run an approved script", "description": "Run one script from the approved script catalogue. Changes data.",
     "annotations": {"readOnlyHint": False, "destructiveHint": True}, "args": ["workspace", "script"]},
]
(D / "tools.json").write_text(json.dumps(tools, indent=2))

# Who may do what. Roles come from Entra ID app roles in the real build; here they're a CSV.
users = [
    ("aisha.rahman@contoso.example", "Contoso Ltd", "Operator"),
    ("ben.okafor@contoso.example", "Contoso Ltd", "Reader"),
    ("chloe.martin@contoso.example", "Contoso Ltd", "Admin"),
    ("dev.patel@fabrikam-customer.example", "Northwind Traders", "Operator"),
]
with open(D / "users.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["upn", "customer", "role"]); w.writerows(users)

policy = {
    "roles": {
        "Reader": ["search_files", "get_file_info", "list_variables"],
        "Operator": ["search_files", "get_file_info", "list_variables", "set_variable"],
        "Admin": ["search_files", "get_file_info", "list_variables", "set_variable", "run_script"],
    },
    "workspaces": {"Contoso Ltd": ["finance-exports", "nightly-jobs"], "Northwind Traders": ["orders"]},
    "approved_scripts": ["refresh-cache.ps1", "export-daily-report.ps1"],
    "confirmation_ttl_seconds": 120,
    "max_result_bytes": 60000,
}
(D / "policy.json").write_text(json.dumps(policy, indent=2))
print("sample data written to", D)
