# DOCKET – site architecture

Three sites, joined to one hub. The split is the security design: **internal case work, client collaboration and
firm-wide data never share a permission boundary.**

| Site | Type | Who | External sharing | Holds |
|---|---|---|---|---|
| **DOCKET Hub** | Communication site (hub) | Everyone in the firm | Off | Navigation, Power BI dashboard page, how-to pages |
| **Clients & Retainers** | Team site (no M365 group) | Partners, practice managers, finance | Off | Lists: *Clients*, *Retainers*, *Allocations* |
| **Case files** | Team site (no M365 group) | Practice groups | **Off** | Library *Case files* with one **document set per case** |
| **Client Share** | Team site (no M365 group) | Case teams + named guests | **New and existing guests** only | One folder per case that collaborates externally |

## Lists (Clients & Retainers site)
| List | Columns |
|---|---|
| Clients | Client ID, name, segment (choice), status (Prospect/Active/Dormant), relationship partner (person) |
| Retainers | Retainer ID, client (lookup), scope, monthly fee, included hours, start, end, hours used this month (number, updated by flow) |
| Allocations | Case ID, person, week start, planned hours |

## Case files library
- Content type **Case** (based on *Document set*) with shared columns: Case ID, Client, Practice, Lead, Retainer,
  Restricted (yes/no), Status. Shared columns push down to every document in the set.
- Allowed content types inside a Case: Letter, Contract, Evidence, Note of advice, Invoice backup.
- Default content for a new Case: `00 Engagement`, `01 Correspondence`, `02 Drafts`, `03 Final` folders.
- Views: *My open cases* (Lead = [Me]), *By practice*, *Restricted* (visible to partners only).
- Keep the library under the 5,000-item list view threshold per view: index Case ID, Practice, Status, Lead.

## Permissions
| Group | Case files | Clients & Retainers | Client Share |
|---|---|---|---|
| DOCKET-Partners | Full control | Edit | Edit |
| DOCKET-Commercial / -Employment / -Disputes | Edit (inherited on non-restricted cases) | Read | Edit on own practice folders |
| DOCKET-Finance | Read | Edit | — |
| DOCKET-CASE-xxxx-Team | Edit on that one document set only | — | — |
| Guests | — | — | Edit or View on one folder, expiring |

**Restricted cases** (ethical wall, sensitive HR matters): the flow breaks inheritance on that document set and grants
only the case team group plus the partners. That's one unique scope per restricted case. Microsoft supports up to
50,000 unique scopes per library and recommends staying under 5,000 for performance, and every individually shared
file counts too, which is why sharing happens in Client Share and not in Case files.

## External access (Client Share)
- Site sharing: **New and existing guests**. Default link type: **Specific people**. No *Anyone* links.
- Guest access expires automatically (site setting, for example 90 days), and the case lead can extend it.
- Since the SharePoint one-time passcode retirement (rolled out to commercial tenants in October 2026), guests are
  Microsoft Entra B2B guests. Check that Entra B2B collaboration settings allow the client domains.
- Optional: apply a sensitivity label to the site that enforces guest settings, and restricted site access
  (requires SharePoint Advanced Management or a Copilot licence in the tenant).
