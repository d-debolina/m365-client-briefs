"""Writes the fictional sample data for Day 32 GRANT into ../data.

Everything here is invented (Contoso Relief Foundation, Fabrikam-style names). Run:
    python scripts/make_sample_data.py
"""
import csv, pathlib

DATA = pathlib.Path(__file__).resolve().parents[1] / "data"
DATA.mkdir(exist_ok=True)


def write(name, header, rows):
    with open(DATA / name, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print("wrote", name, len(rows), "rows")


# 16 forms in two releases, each mapped to one process code the engine understands
write("forms-catalogue.csv",
      ["form_code", "form_name", "release", "process", "numbering_format", "budget_check"],
      [
          ["LEAVE", "Leave request", 1, "HR", "LV-{SEQNUM:5}", "no"],
          ["TIME", "Monthly timesheet", 1, "HR", "TS-{SEQNUM:5}", "no"],
          ["TAUTH", "Travel authorisation", 1, "TRAVEL", "TA-{SEQNUM:5}", "yes"],
          ["TADV", "Travel advance", 1, "TRAVEL", "ADV-{SEQNUM:5}", "yes"],
          ["TEXP", "Travel expense report", 1, "TRAVEL", "TER-{SEQNUM:5}", "yes"],
          ["PR", "Purchase request", 2, "PROCURE", "PR-{SEQNUM:5}", "yes"],
          ["SRC", "Sourcing and award", 2, "PROCURE", "SA-{SEQNUM:5}", "no"],
          ["PO", "Purchase order or contract", 2, "PROCURE", "PO-{SEQNUM:6}", "yes"],
          ["GRN", "Receiving report", 2, "PROCURE", "GRN-{SEQNUM:5}", "no"],
          ["PV", "Payment voucher", 2, "FINANCE", "PV-{SEQNUM:6}", "yes"],
          ["ASSET", "Asset record", 2, "ASSETS", "AR-{SEQNUM:5}", "no"],
          ["ACOUNT", "Asset count", 2, "ASSETS", "AC-{SEQNUM:4}", "no"],
          ["AMOVE", "Asset movement", 2, "ASSETS", "AM-{SEQNUM:5}", "no"],
          ["LOSS", "Loss and theft report", 2, "ASSETS", "LT-{SEQNUM:4}", "no"],
          ["DISP", "Disposal plan", 2, "ASSETS", "DP-{SEQNUM:4}", "no"],
          ["SUPPLY", "Supplies request and stock", 2, "PROCURE", "SR-{SEQNUM:5}", "yes"],
      ])

# Approval matrix: one row per stage. '*' means "any". min/max amounts in USD.
# approver_role is resolved through role-holders.csv, never a hard-coded email.
write("approval-matrix.csv",
      ["rule_id", "process", "department", "project", "min_amount", "max_amount", "stage", "approver_role", "on_reject"],
      [
          ["R01", "HR", "*", "*", 0, 999999999, 1, "LINE_MANAGER", "return"],
          ["R02", "HR", "*", "*", 0, 999999999, 2, "HR_OFFICER", "return"],
          ["R10", "TRAVEL", "*", "*", 0, 999999999, 1, "LINE_MANAGER", "return"],
          ["R11", "TRAVEL", "*", "*", 0, 999999999, 2, "BUDGET_HOLDER", "return"],
          ["R12", "TRAVEL", "*", "*", 2500, 999999999, 3, "FINANCE_MANAGER", "reject"],
          ["R20", "PROCURE", "*", "*", 0, 999999999, 1, "BUDGET_HOLDER", "return"],
          ["R21", "PROCURE", "*", "*", 0, 999999999, 2, "PROCUREMENT_OFFICER", "return"],
          ["R22", "PROCURE", "*", "*", 5000, 999999999, 3, "FINANCE_MANAGER", "reject"],
          ["R23", "PROCURE", "*", "*", 25000, 999999999, 5, "COUNTRY_DIRECTOR", "reject"],
          ["R24", "PROCURE", "*", "PRJ-WASH", 10000, 999999999, 4, "DONOR_COMPLIANCE", "reject"],
          ["R30", "FINANCE", "*", "*", 0, 999999999, 1, "FINANCE_OFFICER", "return"],
          ["R31", "FINANCE", "*", "*", 0, 999999999, 2, "FINANCE_MANAGER", "reject"],
          ["R32", "FINANCE", "*", "*", 25000, 999999999, 3, "COUNTRY_DIRECTOR", "reject"],
          ["R40", "ASSETS", "*", "*", 0, 999999999, 1, "LOGISTICS_OFFICER", "return"],
          ["R41", "ASSETS", "*", "*", 1000, 999999999, 2, "FINANCE_MANAGER", "reject"],
      ])

# Who holds each role, by department. LINE_MANAGER is per department; others are organisation-wide ('*').
write("role-holders.csv",
      ["role", "department", "holder", "alternate"],
      [
          ["LINE_MANAGER", "Programmes", "amina.yusuf@contoso-relief.example", "omar.hassan@contoso-relief.example"],
          ["LINE_MANAGER", "Finance", "grace.mwangi@contoso-relief.example", "peter.otieno@contoso-relief.example"],
          ["LINE_MANAGER", "Logistics", "daniel.kiprop@contoso-relief.example", "amina.yusuf@contoso-relief.example"],
          ["HR_OFFICER", "*", "fatuma.ali@contoso-relief.example", "grace.mwangi@contoso-relief.example"],
          ["BUDGET_HOLDER", "*", "omar.hassan@contoso-relief.example", "amina.yusuf@contoso-relief.example"],
          ["PROCUREMENT_OFFICER", "*", "daniel.kiprop@contoso-relief.example", "peter.otieno@contoso-relief.example"],
          ["FINANCE_OFFICER", "*", "peter.otieno@contoso-relief.example", "grace.mwangi@contoso-relief.example"],
          ["FINANCE_MANAGER", "*", "grace.mwangi@contoso-relief.example", "sarah.njeri@contoso-relief.example"],
          ["COUNTRY_DIRECTOR", "*", "sarah.njeri@contoso-relief.example", "grace.mwangi@contoso-relief.example"],
          ["DONOR_COMPLIANCE", "*", "lucy.wanjiru@contoso-relief.example", "sarah.njeri@contoso-relief.example"],
          ["LOGISTICS_OFFICER", "*", "daniel.kiprop@contoso-relief.example", "peter.otieno@contoso-relief.example"],
      ])

# Time-boxed delegations (out of office). Applied before the alternate.
write("delegations.csv",
      ["delegator", "delegate", "start", "end", "reason"],
      [
          ["grace.mwangi@contoso-relief.example", "sarah.njeri@contoso-relief.example", "2027-04-05", "2027-04-16", "Annual leave"],
          ["omar.hassan@contoso-relief.example", "amina.yusuf@contoso-relief.example", "2027-04-12", "2027-04-14", "Field visit"],
      ])

# Settings that admins change without editing flows
write("settings.csv",
      ["key", "value", "description"],
      [
          ["REMINDER_AFTER_HOURS", 24, "Send a reminder if a stage is still pending after this many hours"],
          ["ESCALATE_AFTER_HOURS", 72, "Move the stage to the alternate after this many hours"],
          ["MAX_RETURNS", 3, "How many times a request can be returned for correction"],
          ["PER_DIEM_FIELD_USD", 45, "Daily allowance for field travel"],
          ["PER_DIEM_CAPITAL_USD", 80, "Daily allowance for capital-city travel"],
          ["MILEAGE_USD_PER_KM", 0.35, "Own-vehicle mileage rate"],
          ["SINGLE_QUOTE_LIMIT_USD", 1000, "Above this, sourcing needs three quotes"],
      ])

# Grant budget lines and money already reserved (commitments) or spent (actuals)
write("budget-lines.csv",
      ["budget_line", "grant", "description", "budget_usd", "committed_usd", "actual_usd"],
      [
          ["WASH-01-TRV", "PRJ-WASH", "WASH programme travel", 18000, 4200, 9100],
          ["WASH-02-SUP", "PRJ-WASH", "WASH supplies and equipment", 120000, 38000, 61500],
          ["EDU-01-TRV", "PRJ-EDU", "Education programme travel", 12000, 1500, 10200],
          ["EDU-02-MAT", "PRJ-EDU", "School materials", 45000, 9000, 22000],
          ["CORE-01-ADM", "CORE", "Core admin and office", 30000, 2500, 14800],
      ])

# Requests to replay through the engine
write("sample-requests.csv",
      ["request_id", "form_code", "requester", "department", "project", "budget_line", "amount_usd", "submitted_on"],
      [
          ["LV-01001", "LEAVE", "mary.achieng@contoso-relief.example", "Programmes", "PRJ-EDU", "", 0, "2027-04-06"],
          ["TA-01002", "TAUTH", "james.mutua@contoso-relief.example", "Programmes", "PRJ-WASH", "WASH-01-TRV", 1850, "2027-04-07"],
          ["TA-01003", "TAUTH", "james.mutua@contoso-relief.example", "Programmes", "PRJ-EDU", "EDU-01-TRV", 950, "2027-04-07"],
          ["PR-01004", "PR", "daniel.kiprop@contoso-relief.example", "Logistics", "PRJ-WASH", "WASH-02-SUP", 14800, "2027-04-08"],
          ["PR-01005", "PR", "james.mutua@contoso-relief.example", "Programmes", "PRJ-EDU", "EDU-02-MAT", 12000, "2027-04-13"],
          ["PR-01008", "PR", "james.mutua@contoso-relief.example", "Programmes", "PRJ-EDU", "EDU-02-MAT", 31000, "2027-04-21"],
          ["PV-01006", "PV", "peter.otieno@contoso-relief.example", "Finance", "CORE", "CORE-01-ADM", 3200, "2027-04-20"],
          ["AM-01007", "AMOVE", "daniel.kiprop@contoso-relief.example", "Logistics", "CORE", "", 0, "2027-04-09"],
      ])
