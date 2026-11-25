# LIFT runbook

## Before
1. **Assess** with the Microsoft 365 Assessment tool (the old SharePoint Modernization Scanner is legacy; only use it to read old reports).
2. Run `plan_waves.py` on the inventory → archive / in place / restructure.
3. Freeze changes on wave sites for the cutover window; communicate.

## Wave 1-2: in place
- Groupify blockers to check: publishing feature on, incompatible template, already group-connected, JS custom actions.
- Transform a **representative** set of pages first; validate every generated page before expanding (pages are created as drafts).
- SharePoint 2013 workflows: rebuild in Power Automate (they're retired in SharePoint Online; check Microsoft's retirement notice for the exact dates).

## Wave 3: restructure
- Subsites/publishing/permission sprawl → new flat sites under a hub, copied with ShareGate (metadata, versions, permissions).
- Redirect old URLs (site swap or link to new site from the old one).

## After
- Compare permissions before/after; fix broken inheritance on purpose, not by accident.
- Lock or archive the source (Microsoft 365 Archive for cold sites).
