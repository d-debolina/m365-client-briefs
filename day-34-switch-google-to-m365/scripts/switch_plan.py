"""Day 34 SWITCH: turn the discovery inventory into migration inputs and a readiness report.

Outputs (in out/):
  gmail-batch-pilot.csv / gmail-batch-wave1.csv  CSVs for the EAC Google Workspace migration batch (EmailAddress header)
  drive-destinations.csv                         Migration Manager source -> destination map (personal drives and shared drives)
  link-replacements.csv                          old client links -> new SharePoint folders, with the test to run as that guest
  readiness.txt                                  limits check, storage check and a Microsoft 365 Backup cost estimate

Limits used (Microsoft Learn, checked Nov 2026; re-check before a real project):
  user mailbox 100 GB on Business Premium, OneDrive default 1 TB per user,
  SharePoint tenant storage 1 TB + 10 GB per licence, Microsoft 365 Backup 0.15 USD per GiB per month.
"""
import csv, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA, OUT = ROOT / "data", ROOT / "out"
TENANT = "fabrikamcreative"          # fictional; becomes https://fabrikamcreative.sharepoint.com
MAILBOX_GB, ONEDRIVE_GB = 100, 1024
SP_BASE_GB, SP_PER_LICENCE_GB = 1024, 10
BACKUP_USD_PER_GIB = 0.15
WARN_RATIO = 0.8


def read(name):
    with open(DATA / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write(name, header, rows):
    OUT.mkdir(exist_ok=True)
    with open(OUT / name, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def onedrive_url(email):
    return f"https://{TENANT}-my.sharepoint.com/personal/" + email.replace("@", "_").replace(".", "_")


def plan(users, drives, links):
    pilot = [u["email"] for u in users if u["pilot"] == "yes"]
    wave1 = [u["email"] for u in users if u["pilot"] != "yes"]

    dest = [["personal", u["email"], onedrive_url(u["email"]) + "/Documents/Migrated from Google"] for u in users]
    # Migrate each shared drive into a FOLDER in the library, not the library root, so root permissions come across.
    dest += [["shared", d["shared_drive"], f"https://{TENANT}.sharepoint.com{d['target_site']}/Shared Documents/{d['shared_drive']}"]
             for d in drives]

    site_of = {d["shared_drive"]: d["target_site"] for d in drives}
    repl = [[l["client"], l["old_link_id"],
             f"https://{TENANT}.sharepoint.com{site_of[l['shared_drive']]}/Shared Documents/{l['shared_drive']}/{l['folder']}",
             l["shared_with"], "reshare (Specific people); open in a private window as the guest; confirm the other client folders return access denied"]
            for l in links]
    return pilot, wave1, dest, repl


def readiness(users, drives):
    lines, problems = [], 0
    for u in users:
        for label, used, limit in (("mailbox", float(u["gmail_gb"]), MAILBOX_GB), ("OneDrive", float(u["drive_gb"]), ONEDRIVE_GB)):
            ratio = used / limit
            flag = "OK" if ratio < WARN_RATIO else ("WARN" if ratio < 1 else "BLOCK")
            problems += flag != "OK"
            lines.append(f"{flag:5} {u['display_name']:<14} {label:<8} {used:7.1f} GB of {limit} GB ({ratio:.0%})")
    sp_used = sum(float(d["size_gb"]) for d in drives)
    sp_quota = SP_BASE_GB + SP_PER_LICENCE_GB * len(users)
    flag = "OK" if sp_used / sp_quota < WARN_RATIO else "WARN"
    problems += flag != "OK"
    lines.append(f"{flag:5} SharePoint tenant storage {sp_used:.1f} GB of {sp_quota} GB ({sp_used / sp_quota:.0%})")
    mail = sum(float(u["gmail_gb"]) for u in users)
    od = sum(float(u["drive_gb"]) for u in users)
    lines.append("")
    lines.append("Microsoft 365 Backup estimate (pay-as-you-go, list price, before growth and versions):")
    for label, gb in (("Mailboxes only", mail), ("Mailboxes + SharePoint", mail + sp_used), ("Everything", mail + sp_used + od)):
        lines.append(f"  {label:<24} {gb:7.1f} GiB  ~ USD {gb * BACKUP_USD_PER_GIB:7.2f} / month")
    return lines, problems


def main():
    users, drives, links = read("users.csv"), read("shared-drives.csv"), read("external-links.csv")
    pilot, wave1, dest, repl = plan(users, drives, links)
    write("gmail-batch-pilot.csv", ["EmailAddress"], [[e] for e in pilot])
    write("gmail-batch-wave1.csv", ["EmailAddress"], [[e] for e in wave1])
    write("drive-destinations.csv", ["source_type", "source", "destination"], dest)
    write("link-replacements.csv", ["client", "old_link_id", "new_folder", "guest", "test"], repl)
    lines, problems = readiness(users, drives)
    (OUT / "readiness.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"\npilot: {len(pilot)} mailbox(es) · wave 1: {len(wave1)} · drive tasks: {len(dest)} · links to replace: {len(repl)}")
    return 1 if any(l.startswith("BLOCK") for l in lines) else 0


if __name__ == "__main__":
    sys.exit(main())
