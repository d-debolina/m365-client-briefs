# SWITCH runbook – Google Workspace to Microsoft 365 for a small team

Fictional client: **Fabrikam Creative**, 6 people, one domain (`fabrikamcreative.example`).
The client owns the domain, billing and the Global Administrator accounts from day one.

## Milestone 1 – Discovery and costed plan (the client keeps this whatever happens next)
- Client creates the Microsoft 365 tenant and buys the licences in their own name; you get a named admin account (not a shared one).
- Inventory: `data/users.csv`, `data/shared-drives.csv`, `data/groups-and-aliases.csv`, `data/connected-workflows.csv`, `data/external-links.csv`.
- Run `python scripts/switch_plan.py` → readiness report, batch CSVs, drive destinations, link replacements.
- Plan states: expected downtime (none for mail if routing subdomains are used; a short read-only window for files on cutover day),
  exclusions (Google Sites, Maps, chat history, group mail history, comments on Docs), and the rollback below.

## Milestone 2 – One-user pilot (live mail stays at Google)
1. Add and verify the domain in Microsoft 365, but **don't** change MX yet.
2. Create the two routing subdomains (Google → `m365.` and `gws.`) and the mail user for the pilot person.
3. EAC → Migration → Add migration batch → Google Workspace (Gmail) migration → automated prerequisites → `out/gmail-batch-pilot.csv`.
4. Migration Manager → Google Workspace → migrate the pilot's drive plus one client folder from `Clients`.
5. Test: mail, calendar, contacts, rules; converted Docs/Sheets/Slides open in Office; one guest opens the client folder; security settings apply.
6. **Client signs off the pilot** before any production change.

## Milestone 3 – Migration and reconciliation
- Wave 1: the other five mailboxes (`out/gmail-batch-wave1.csv`). Assign licences within 30 days of the mail user becoming a mailbox.
- Drives: personal drives → OneDrive, shared drives → a **folder** in each SharePoint library (`out/drive-destinations.csv`).
- Turn on file-level permission migration if the pilot showed you need it (off by default; files inherit folder permissions).
- Reconcile with the Migration Manager reports and the Gmail batch statistics. Record every exception.

## Cutover (one agreed after-hours window)
1. Complete the Gmail batches when they show **Synced**.
2. Final Migration Manager delta pass.
3. Change MX, SPF, DKIM and autodiscover to Microsoft 365 (lower the MX TTL to 300 s a few days earlier).
4. Recreate groups and aliases (`data/groups-and-aliases.csv`).
5. Reshare client folders (`out/link-replacements.csv`) and send clients the new links.

## Rollback (until written sign-off)
- Google Workspace stays paid and untouched until sign-off. Rollback = point MX back to Google (that's why the TTL is low)
  and tell users to use Gmail. Mail that arrived in Microsoft 365 in the meantime is exported with a PST or forwarded back.
- Never cancel Google Workspace or delete Google data before the client signs off in writing.

## Milestone 4 – Testing, recovery and handover
- Teams external call from the meeting room; Google Ads, GA4 and Tag Manager still open with Cloud Identity Free identities.
- Microsoft 365 Backup policy on; **prove a restore**: one email and one file.
- Google archive retrieval demo (Google-side export or Vault, depending on the client's plan).
- Five working days of support; admin guide (`docs/admin-guide-outline.md`) and a recorded walkthrough.
