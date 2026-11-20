# File server → SharePoint readiness checklist (SHELF)

## Before you move anything
- [ ] Run `readiness_scan.py` on an inventory export and fix: long paths, invalid characters, PST/Access/temp files
- [ ] Archive or delete files nobody has touched in 3+ years (usually 30–50 %)
- [ ] Design **one site per team/department**, a hub for navigation, and **no deeper than 3–4 folder levels**
- [ ] Agree 3–5 metadata columns per library (Client, Year, Doc type) to replace deep folders
- [ ] Check permissions: map share ACLs to site membership groups, not to individual users

## Sync & devices
- [ ] Use **Add shortcut to My files**, not the Sync button. Hide the Sync button tenant-wide.
- [ ] Turn on Files On-Demand and Known Folder Move. Turn on sync health reporting.
- [ ] Keep each user's total synced items under ~300,000 (the same limit applies to shortcuts)
- [ ] Exclude the OneDrive folder from real-time antivirus scanning (ask security first)
- [ ] iPad: OneDrive app + Files app integration; teach "Favourites" and "Pin to Quick access"

## Search
- [ ] Map metadata to managed properties; add a search vertical or PnP Modern Search page per department
- [ ] Pin key folders as "Quick access" / add Highlighted content web parts

## Copilot
- [ ] Run Data access governance reports (oversharing, "Everyone except external users")
- [ ] Turn on Restricted Content Discovery for sites still under review
- [ ] Apply sensitivity labels to HR/Finance sites before Copilot rollout
- [ ] (Restricted SharePoint Search is retiring: since 31 July 2026 it can't be newly enabled. Use RCD instead.)

## Moving files later
- [ ] Use **Move to** (keeps version history). Per operation: up to 100 GB and 30,000 files
- [ ] For bulk moves: SharePoint Migration Manager / SPMT (free) or ShareGate (paid)
