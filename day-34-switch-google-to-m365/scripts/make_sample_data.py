"""Creates the fictional discovery inventory for Day 34 SWITCH (Fabrikam Creative, 6 people).

Everything here is invented: names, domains, sizes, clients and links.
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

# Users and what discovery found in their Google accounts (sizes in GB)
write("users.csv",
  ["email", "display_name", "role", "gmail_gb", "drive_gb", "calendars", "pilot", "device"],
  [
    ["alex.morgan@fabrikamcreative.example", "Alex Morgan", "Managing director", 18.4, 62.0, 2, "no", "Windows laptop"],
    ["priya.shah@fabrikamcreative.example", "Priya Shah", "Account director", 11.2, 38.5, 1, "yes", "MacBook"],
    ["sam.okoro@fabrikamcreative.example", "Sam Okoro", "Designer", 4.9, 214.0, 1, "no", "MacBook"],
    ["lena.fischer@fabrikamcreative.example", "Lena Fischer", "Media buyer", 7.3, 21.0, 1, "no", "Windows laptop"],
    ["tom.reyes@fabrikamcreative.example", "Tom Reyes", "Copywriter", 3.1, 9.4, 1, "no", "Windows laptop"],
    ["jo.hartley@fabrikamcreative.example", "Jo Hartley", "Studio manager", 6.6, 14.2, 2, "no", "Windows laptop"],
  ])

# Shared drives -> SharePoint team sites
write("shared-drives.csv",
  ["shared_drive", "size_gb", "members", "external_shares", "target_site"],
  [
    ["Clients", 140.0, "all staff", 9, "/sites/Clients"],
    ["Studio Assets", 310.0, "Sam Okoro; Priya Shah; Alex Morgan", 2, "/sites/Studio"],
    ["Finance", 4.2, "Alex Morgan; Lena Fischer", 0, "/sites/Finance"],
    ["Templates", 1.8, "all staff", 0, "/sites/Studio"],
  ])

# Things that must keep working after the switch (the 'record what works today' list)
write("connected-workflows.csv",
  ["item", "depends_on", "owner", "after_switch", "test"],
  [
    ["Client Google Ads accounts", "staff Google identity", "Lena Fischer", "keep via Cloud Identity Free", "sign in to one client Ads account"],
    ["Client GA4 properties", "staff Google identity", "Lena Fischer", "keep via Cloud Identity Free", "open one GA4 property"],
    ["Client Tag Manager containers", "staff Google identity", "Lena Fischer", "keep via Cloud Identity Free", "open one GTM workspace"],
    ["Website contact form", "SMTP relay via Gmail", "Alex Morgan", "move to Exchange Online (SMTP AUTH or connector)", "submit test form, check office@ inbox"],
    ["Device tracking", "existing MDM / asset list", "Alex Morgan", "keep; add Intune enrolment later", "confirm all 5 laptops still report"],
    ["Invoice app emails", "sends as office@", "Alex Morgan", "update SPF and DKIM", "send one test invoice"],
    ["Calendar booking link", "Google Calendar appointment page", "Priya Shah", "replace with Microsoft Bookings", "book a test slot"],
  ])

# Google groups and aliases -> Microsoft 365 equivalents
write("groups-and-aliases.csv",
  ["google_object", "type", "members", "m365_target", "note"],
  [
    ["office@fabrikamcreative.example", "Google Group (collaborative inbox)", "Jo Hartley; Alex Morgan", "shared mailbox", "group history is not moved by the Gmail batch; export it or start fresh"],
    ["hello@fabrikamcreative.example", "user alias of Priya Shah", "Priya Shah", "proxy address on Priya's mailbox", "add before cutover"],
    ["accounts@fabrikamcreative.example", "Google Group", "Alex Morgan; Lena Fischer", "distribution list", "external senders allowed"],
  ])

# Old Google Drive links that clients still use (pilot + link replacement)
write("external-links.csv",
  ["client", "old_link_id", "shared_drive", "folder", "shared_with"],
  [
    ["Contoso Coffee", "gdrv-001", "Clients", "Contoso Coffee/2027 campaign", "marketing@contoso.example"],
    ["Northwind Outdoors", "gdrv-002", "Clients", "Northwind Outdoors/Brand refresh", "brand@northwind.example"],
    ["Tailspin Travel", "gdrv-003", "Clients", "Tailspin Travel/Spring ads", "ads@tailspin.example"],
    ["Wingtip Toys", "gdrv-004", "Clients", "Wingtip Toys/Packaging", "design@wingtip.example"],
    ["Litware Labs", "gdrv-005", "Clients", "Litware Labs/Launch video", "comms@litware.example"],
    ["Contoso Coffee", "gdrv-006", "Studio Assets", "Exports/Contoso", "marketing@contoso.example"],
  ])
