# Security baseline for a 6-person Business Premium tenant

Keep it small and explainable. Test every Conditional Access policy on the pilot user first and keep two
break-glass Global Administrator accounts excluded from all policies.

| Area | Setting | Why |
|---|---|---|
| Identity | Security defaults **off** once Conditional Access policies below are on | Business Premium includes Entra ID P1 |
| Identity | CA: require MFA for all users | Phishing-resistant methods (passkeys / Authenticator) where possible |
| Identity | CA: block legacy authentication | Old IMAP/POP clients are the usual way in |
| Identity | CA: require MFA for admin roles at every sign-in | Admin accounts are the crown jewels |
| Devices | Intune enrolment for Windows and macOS; compliance: encryption, firewall, Defender on | Business Premium includes Intune Plan 1 |
| Devices | CA: require compliant device for Microsoft 365 (report-only first) | Turn on after every laptop is compliant |
| Devices | Onboard laptops to Defender for Business | Included in Business Premium |
| Email | Defender for Office 365 preset policy **Standard** | Safe Links, Safe Attachments, anti-phishing |
| Email | DKIM on, DMARC `p=none` → `quarantine` after 2 weeks of clean reports | Protects the domain the agency's clients trust |
| Sharing | SharePoint: new and existing guests only; default link = Specific people; guest expiry 90 days | Client folders are shared one by one |
| Backup | Microsoft 365 Backup policy for mailboxes and the Clients site | Needs pay-as-you-go billing through an Azure subscription |
| Admin | Client owns billing, domain registrar and Global Admin; consultant account removed after handover | The brief asks for independence |

Don't break what exists: the brief says device tracking and the website must keep working. Inventory both in
`data/connected-workflows.csv` and test them in the pilot before any policy is enforced.
