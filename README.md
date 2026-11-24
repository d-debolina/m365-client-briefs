# m365-client-briefs

Sample data, scripts and templates for the **"Real client brief → build"** series on Medium
by Debolina Das Gupta: <https://medium.com/@debolinad>

Every folder matches one **Day** in the series. Each Day starts from a real (anonymised) request
seen on a freelance marketplace and rebuilds it with Microsoft 365, Power Platform, Copilot Studio and Azure.

> All names, companies, CVs, policies and numbers in this repo are **fictional**. Use a developer tenant.

| Day | App | What you build | Folder |
|---|---|---|---|
| 1 | **QUOTA** – Quote-Of-Today Assistant | Copilot Studio agent inside a model-driven app that reads and writes Dataverse | `day-01-quota-estimate-agent` |
| 2 | **TRACE** – Trusted Retrieval with Answers, Citations & Evaluation | Permission-trimmed AI answers over SharePoint (SPFx + Azure Functions + Copilot Retrieval API) | `day-02-trace-sharepoint-ai-search` |
| 3 | **HIRE** – HR Intake, Requisition & Enrolment | HR Service Centre with multistage approvals | `day-03-hire-hr-service-centre` |
| 4 | **MATCH** – Making Applicants & Talent Click | Score every CV against a vacancy with AI prompts | `day-04-match-cv-shortlist` |
| 5 | **SPRINKLE** – Site & Property Reports, INspections, Kit for Landscape Experts | Offline iPad inspection app with branded PDF reports | `day-05-sprinkle-field-inspections` |
| 6 | **WARDEN** – Watch, Audit, Restrict & Detect ENterprise agents | Inventory, risk rules and a runtime guard for Copilot Studio agents | `day-06-warden-agent-guard` |
| 7 | **SCOUT** – Survey, Classify, Order Use-cases, Then build | AI agent readiness audit kit | `day-07-scout-agent-readiness-audit` |
| 8 | **TRIAD** – Three Routed, Independent Agents, Delivered | Multi-agent Copilot Studio: child vs connected agents with shared state | `day-08-triad-multi-agent` |
| 9 | **SHELF** – Sync, Health, Explorer & Library Fixes | File server to SharePoint: readiness scan, sync and Copilot fixes | `day-09-shelf-fileserver-to-sharepoint` |
| 10 | **PARCEL** – Parse, Assemble, Route, Check, Emit, Log | Outlook emails to a REST API with AI extraction, schema checks and retries | `day-10-parcel-email-to-api` |
| 11 | **SHIELD** – Simulate, Hunt, Inform, Enforce, Label, Dashboard | Purview DLP rollout kit for the Copilot era | `day-11-shield-purview-dlp-copilot` |
| 12 | **LEDGER** – Lookup, Engage, Document, Guide, Escalate, Report | Fintech onboarding agent: SharePoint knowledge + custom CRM connector + governance | `day-12-ledger-fintech-crm-agent` |
| 13 | **MOVER** – Map, Organise, Verify, Export, Redirect | WordPress intranet to SharePoint: IA, term set, PnP migration script | `day-13-mover-wordpress-to-sharepoint` |
| 14 | **BRIDGE** – Bound to Role, Identity & Data, Guarded End-to-end | Copilot Studio agent in any web app with SSO, signed context and per-user MCP tools | `day-14-bridge-agent-in-any-web-app` |
| 15 | **CARGO** – Cloud Attachments Routed to Guarded Objects | Power Pages large file uploads with Azure Blob Storage | `day-15-cargo-power-pages-large-files` |
| 16 | **PLAZA** – People, Links, Announcements, Zones, Analytics | Cluttered team site to modern intranet: audit, IA, home page, launch | `day-16-plaza-modern-intranet-redesign` |
| 17 | **VAULT** – Validate, Archive, Unify, Legal-hold, Trace | Third-party archive into Purview eDiscovery with Graph automation and hash checks | `day-17-vault-third-party-archive-purview` |
| 18 | **PITCH** – Personalised, Inspected, Tailored, Checked, Human-sent | AI-drafted B2B outreach from Excel with Outlook drafts and human review | `day-18-pitch-b2b-outreach-drafts` |
| 19 | **LIFT** – Locate, Inspect, Flatten, Transform | Classic to modern SharePoint: wave planner, PnP in-place, ShareGate restructure | `day-19-lift-classic-to-modern` |
| 20 | **PROOF** – Prompt, Review, Own, Organise, Finalise | Reviewing AI-generated Power Automate specs before Copilot builds them | `day-20-proof-review-copilot-flow-spec` |
| 21 | **TALLY** – Track, Assign, List, Log, Yes/no-go | Microsoft Lists validation tracker for an Azure migration | `day-21-tally-migration-validation-tracker` |
| 22 | **BATON** – Build, Assert, Test, Own, Note | Dataverse implementation spec, test matrix, CLI checks and handoff pack | `day-22-baton-dataverse-spec-tests-handoff` |
| 23 | **CAMPUS** – Courses, Assets, Members, Permissions, Upkeep, Strategy | SharePoint academy site: asset metadata, permissions model, governance rhythm | `day-23-campus-sharepoint-academy-site` |
| 24 | **ECHO** – Embedded, Cross-tenant-safe, Handoff-ready Operator | Multi-tenant AI support copilot with tenant isolation tests and human handoff | `day-24-echo-multitenant-support-copilot` |
| 25 | **STEWARD** – Steady, Tuned, Evidence-based, Watchful, Accountable, Reported, Documented | What a Microsoft Purview retainer looks like month by month | `day-25-steward-purview-retainer` |
| 26 | **ATLAS** – Annual Timeline of Leadership Activities & Schedules | Year-at-a-glance leadership calendar: canvas app on one SharePoint list, as a Teams tab, standard licences only | `day-26-atlas-leadership-calendar` |
| 27 | **CLEAR** – Catalogue, Lock down, Establish one version, Approve AI work, Review | Getting a small firm's AI use under control: tool discovery, AI policy with human sign-off, one version per process, folder lockdown list | `day-27-clear-ai-use-governance` |
| 28 | **STAMP** – Submit, Template, Assemble, Make PDF | One PDF per Microsoft Forms response with standard connectors (plus a premium Word-template route) | `day-28-stamp-forms-to-pdf` |
| 29 | **SWEEP** – Scan, Weigh, Elect, Evacuate, Prove | 1.5 TB SharePoint/OneDrive duplicate cleanup: Graph inventory, hash-based plan, quarantine before delete | `day-29-sweep-sharepoint-onedrive-cleanup` |
| 30 | **NUDGE** – Next steps, Updates, Due dates, Gentle follow-ups, Evidence | Copilot Studio sales coach without a CRM: SharePoint lists as CRM-lite, saved commitments and Teams follow-up cards on the right day | `day-30-nudge-sales-next-step-agent` |
| 31 | **CREW** – Capacity, Resources, Equipment & Weeks | Dataverse resource board: plug-ins that keep a locked plan locked (even in Excel), a tested planning engine, Teams unlock approvals, pipelines | `day-31-crew-dataverse-resource-board` |
| 32 | **PROBE** – Prove Records Obey Boundaries End-to-end | Security review of a Copilot Studio agent over Salesforce health data: per-user access, prompt-injection tests, leak checker, hardening checklist | `day-32-probe-copilot-salesforce-access-review` |

## Licence
Content: CC BY 4.0. Code: MIT.
