# m365-client-briefs

Sample data, scripts and templates for the **"Real client brief → build"** series on Medium
by Debolina Das Gupta: <https://medium.com/@debolinad>

Every folder matches one **Day** in the series. Each Day starts from a real (anonymised) request
seen on a freelance marketplace and rebuilds it with Microsoft 365, Power Platform, Copilot Studio and Azure.

> All names, companies, CVs, policies and numbers in this repo are **fictional**. Use a developer tenant.

| Day | App | What you build | Folder |
|---|---|---|---|
| 1 | **ATLAS** – Annual Timeline of Leadership Activities & Schedules | Year-at-a-glance leadership calendar: canvas app on one SharePoint list, as a Teams tab, standard licences only | `day-01-atlas-leadership-calendar` |
| 2 | **SPRINKLE** – Site & Property Reports, INspections, Kit for Landscape Experts | Offline iPad inspection app with branded PDF reports | `day-02-sprinkle-field-inspections` |
| 3 | **GRANT** – Generic Routing, Approvals, Numbering & Tracking | One reusable approval engine for 16 nonprofit forms: Dataverse approval matrix, delegation, budget check, audit log, pipelines | `day-03-grant-approval-engine` |
| 4 | **QUOTA** – Quote-Of-Today Assistant | Copilot Studio agent inside a model-driven app that reads and writes Dataverse | `day-04-quota-estimate-agent` |
| 5 | **TRACE** – Trusted Retrieval with Answers, Citations & Evaluation | Permission-trimmed AI answers over SharePoint (SPFx + Azure Functions + Copilot Retrieval API) | `day-05-trace-sharepoint-ai-search` |
| 6 | **HIRE** – HR Intake, Requisition & Enrolment | HR Service Centre with multistage approvals | `day-06-hire-hr-service-centre` |
| 7 | **MATCH** – Making Applicants & Talent Click | Score every CV against a vacancy with AI prompts | `day-07-match-cv-shortlist` |
| 8 | **WARDEN** – Watch, Audit, Restrict & Detect ENterprise agents | Inventory, risk rules and a runtime guard for Copilot Studio agents | `day-08-warden-agent-guard` |
| 9 | **SCOUT** – Survey, Classify, Order Use-cases, Then build | AI agent readiness audit kit | `day-09-scout-agent-readiness-audit` |
| 10 | **TRIAD** – Three Routed, Independent Agents, Delivered | Multi-agent Copilot Studio: child vs connected agents with shared state | `day-10-triad-multi-agent` |
| 11 | **SHELF** – Sync, Health, Explorer & Library Fixes | File server to SharePoint: readiness scan, sync and Copilot fixes | `day-11-shelf-fileserver-to-sharepoint` |
| 12 | **PARCEL** – Parse, Assemble, Route, Check, Emit, Log | Outlook emails to a REST API with AI extraction, schema checks and retries | `day-12-parcel-email-to-api` |
| 13 | **SHIELD** – Simulate, Hunt, Inform, Enforce, Label, Dashboard | Purview DLP rollout kit for the Copilot era | `day-13-shield-purview-dlp-copilot` |
| 14 | **LEDGER** – Lookup, Engage, Document, Guide, Escalate, Report | Fintech onboarding agent: SharePoint knowledge + custom CRM connector + governance | `day-14-ledger-fintech-crm-agent` |
| 15 | **MOVER** – Map, Organise, Verify, Export, Redirect | WordPress intranet to SharePoint: IA, term set, PnP migration script | `day-15-mover-wordpress-to-sharepoint` |
| 16 | **BRIDGE** – Bound to Role, Identity & Data, Guarded End-to-end | Copilot Studio agent in any web app with SSO, signed context and per-user MCP tools | `day-16-bridge-agent-in-any-web-app` |
| 17 | **CARGO** – Cloud Attachments Routed to Guarded Objects | Power Pages large file uploads with Azure Blob Storage | `day-17-cargo-power-pages-large-files` |
| 18 | **PLAZA** – People, Links, Announcements, Zones, Analytics | Cluttered team site to modern intranet: audit, IA, home page, launch | `day-18-plaza-modern-intranet-redesign` |
| 19 | **VAULT** – Validate, Archive, Unify, Legal-hold, Trace | Third-party archive into Purview eDiscovery with Graph automation and hash checks | `day-19-vault-third-party-archive-purview` |
| 20 | **PITCH** – Personalised, Inspected, Tailored, Checked, Human-sent | AI-drafted B2B outreach from Excel with Outlook drafts and human review | `day-20-pitch-b2b-outreach-drafts` |
| 21 | **LIFT** – Locate, Inspect, Flatten, Transform | Classic to modern SharePoint: wave planner, PnP in-place, ShareGate restructure | `day-21-lift-classic-to-modern` |
| 22 | **PROOF** – Prompt, Review, Own, Organise, Finalise | Reviewing AI-generated Power Automate specs before Copilot builds them | `day-22-proof-review-copilot-flow-spec` |
| 23 | **TALLY** – Track, Assign, List, Log, Yes/no-go | Microsoft Lists validation tracker for an Azure migration | `day-23-tally-migration-validation-tracker` |
| 24 | **BATON** – Build, Assert, Test, Own, Note | Dataverse implementation spec, test matrix, CLI checks and handoff pack | `day-24-baton-dataverse-spec-tests-handoff` |
| 25 | **ECHO** – Embedded, Cross-tenant-safe, Handoff-ready Operator | Multi-tenant AI support copilot with tenant isolation tests and human handoff | `day-25-echo-multitenant-support-copilot` |
| 26 | **CLEAR** – Catalogue, Lock down, Establish one version, Approve AI work, Review | Getting a small firm's AI use under control: tool discovery, AI policy with human sign-off, one version per process, folder lockdown list | `day-26-clear-ai-use-governance` |
| 27 | **STAMP** – Submit, Template, Assemble, Make PDF | One PDF per Microsoft Forms response with standard connectors (plus a premium Word-template route) | `day-27-stamp-forms-to-pdf` |
| 28 | **SWEEP** – Scan, Weigh, Elect, Evacuate, Prove | 1.5 TB SharePoint/OneDrive duplicate cleanup: Graph inventory, hash-based plan, quarantine before delete | `day-28-sweep-sharepoint-onedrive-cleanup` |
| 29 | **NUDGE** – Next steps, Updates, Due dates, Gentle follow-ups, Evidence | Copilot Studio sales coach without a CRM: SharePoint lists as CRM-lite, saved commitments and Teams follow-up cards on the right day | `day-29-nudge-sales-next-step-agent` |
| 30 | **CREW** – Capacity, Resources, Equipment & Weeks | Dataverse resource board: plug-ins that keep a locked plan locked (even in Excel), a tested planning engine, Teams unlock approvals, pipelines | `day-30-crew-dataverse-resource-board` |
| 31 | **PROBE** – Prove Records Obey Boundaries End-to-end | Security review of a Copilot Studio agent over Salesforce health data: per-user access, prompt-injection tests, leak checker, hardening checklist | `day-31-probe-copilot-salesforce-access-review` |
| 32 | **HAUL** – Hash-checked, App-only, Unattended, Logged | Unattended file uploads from many RMM-managed PCs to one SharePoint library: certificate auth, write on one library only, hash-based skip, exit codes | `day-32-haul-rmm-files-to-sharepoint` |
| 33 | **DOCKET** – Document sets, Oversight, Cases, Keys, External access, Tracking | Client, retainer and case hub on SharePoint: document set per case, ethical wall, guest-only share site, allocation dashboard | `day-33-docket-client-case-hub` |

## Licence
Content: CC BY 4.0. Code: MIT.
