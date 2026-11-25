"""Generates fictional PROBE sample data (Day 31): Salesforce-style users, roles, accounts and referrals.

python scripts/make_data.py   -> writes data/*.csv
Every person, clinic and "patient" here is invented. Never test with real PHI outside the client's tenant.
"""
import csv, random, pathlib

random.seed(32)
DATA = pathlib.Path(__file__).resolve().parents[1] / "data"
DATA.mkdir(exist_ok=True)


def write(name, rows):
    with open(DATA / name, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    print(f"{name}: {len(rows)} rows")


# Role hierarchy: VP > Manager West / Manager East > reps. Compliance and Integration sit outside it.
users = [
    {"UserId": "U-VP", "Name": "Vera Contoso", "Role": "VP Sales", "ReportsToRole": "", "Profile": "Sales Leader",
     "ViewAllReferrals": "No", "FLS_DiagnosisNotes": "No", "Notes": "sees everything below her in the hierarchy"},
    {"UserId": "U-MW", "Name": "Marco Fabrikam", "Role": "Manager West", "ReportsToRole": "VP Sales", "Profile": "Sales Manager",
     "ViewAllReferrals": "No", "FLS_DiagnosisNotes": "No", "Notes": ""},
    {"UserId": "U-ME", "Name": "Mei Northwind", "Role": "Manager East", "ReportsToRole": "VP Sales", "Profile": "Sales Manager",
     "ViewAllReferrals": "No", "FLS_DiagnosisNotes": "No", "Notes": ""},
    {"UserId": "U-R1", "Name": "Rafa Tailspin", "Role": "Rep West", "ReportsToRole": "Manager West", "Profile": "Sales Rep",
     "ViewAllReferrals": "No", "FLS_DiagnosisNotes": "No", "Notes": ""},
    {"UserId": "U-R2", "Name": "Rina Litware", "Role": "Rep West", "ReportsToRole": "Manager West", "Profile": "Sales Rep",
     "ViewAllReferrals": "No", "FLS_DiagnosisNotes": "No", "Notes": ""},
    {"UserId": "U-R3", "Name": "Rob Adatum", "Role": "Rep East", "ReportsToRole": "Manager East", "Profile": "Sales Rep",
     "ViewAllReferrals": "No", "FLS_DiagnosisNotes": "No", "Notes": ""},
    {"UserId": "U-R4", "Name": "Ruth Proseware", "Role": "Rep East", "ReportsToRole": "Manager East", "Profile": "Sales Rep",
     "ViewAllReferrals": "No", "FLS_DiagnosisNotes": "No", "Notes": ""},
    {"UserId": "U-CO", "Name": "Cal Woodgrove", "Role": "Compliance", "ReportsToRole": "", "Profile": "Compliance Auditor",
     "ViewAllReferrals": "Yes", "FLS_DiagnosisNotes": "Yes", "Notes": "read-only, View All on Referral"},
    {"UserId": "U-INT", "Name": "Integration User", "Role": "", "ReportsToRole": "", "Profile": "System Administrator",
     "ViewAllReferrals": "Yes", "FLS_DiagnosisNotes": "Yes", "Notes": "THE RISK: if the agent uses this connection, everyone sees everything"},
]
write("salesforce_users.csv", users)

reps = ["U-R1", "U-R2", "U-R3", "U-R4"]
clinics = ["Harbour Family Clinic", "Maple Physio", "Riverside Dental", "Oak Street Pharmacy", "Lakeside Imaging",
           "Northwind Rehab", "Hilltop Pediatrics", "Fabrikam Eye Care", "Contoso Sleep Lab", "Tailspin Orthopedics",
           "Litware Dermatology", "Adatum Cardiology"]
accounts = [{"AccountId": f"ACC-{i+1:03d}", "Name": nm, "OwnerId": reps[i % 4],
             "Region": "West" if reps[i % 4] in ("U-R1", "U-R2") else "East",
             "AnnualVolume": random.randrange(20, 400, 10)} for i, nm in enumerate(clinics)]
write("accounts.csv", accounts)

given = ["Alex", "Blair", "Casey", "Drew", "Emery", "Finley", "Gray", "Harper", "Indy", "Jules", "Kit", "Lane"]
refs = []
for i in range(36):
    acc = accounts[i % len(accounts)]
    refs.append({"ReferralId": f"REF-{i+1:03d}", "AccountId": acc["AccountId"], "OwnerId": acc["OwnerId"],
                 "PatientAlias": f"{random.choice(given)} T{random.randint(100, 999)} (fictional)",
                 "Product": random.choice(["Knee brace", "CPAP kit", "Glucose monitor", "Hearing aid"]),
                 "Status": random.choice(["New", "Contacted", "Fitted", "Closed"]),
                 "DiagnosisNotes": random.choice(["[fictional] post-op follow-up", "[fictional] chronic condition",
                                                  "[fictional] screening result pending", "[fictional] no notes"])})
write("referrals.csv", refs)
