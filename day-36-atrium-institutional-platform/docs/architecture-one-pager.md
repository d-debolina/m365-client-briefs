# ATRIUM: one-page architecture for an institution-wide platform on Microsoft 365

**Brief (fictional):** Contoso Institute (academic) and Contoso Services (commercial) share one Microsoft 365
tenant, 500–1,000 staff, Arabic and English. They want governance, documents and correspondence, operations
(HR, finance, procurement, service desk), academic modules, knowledge and a permission-aware AI assistant,
using built-in Microsoft 365 first, with clean ownership and handover.

## Principles
1. **Hubs, not subsites.** Six hubs (Home, Governance, Records, Operations, Academic, Knowledge). A site
   belongs to one hub; content can roll up anywhere.
2. **One information model.** Shared content types and one term store (Entity, Unit, Document type,
   Classification, Academic year). Every module reuses them.
3. **One approval engine.** A single child flow reads an approval matrix list (doc type × entity → stages,
   escalation days). Modules call it; nobody builds approvals twice.
4. **Entities are metadata + groups, not tenants.** Entity column + Entra security groups per entity.
5. **Systems of record stay put.** ERP and the student information system remain independent; ATRIUM gets
   read-only reporting only where needed.
6. **Bilingual by design.** Multilingual communication sites (English default, Arabic added), bilingual
   titles on lists, RTL tested on every page and form. Team sites created in Arabic where the team works in Arabic.
7. **AI last.** The Copilot Studio assistant arrives after permissions are clean, sites are labelled and
   oversharing is fixed. Otherwise it will happily find what people shouldn't see.

## Build order
See `out/build-order.md` (generated from `data/modules.csv`). Phase 1 = foundations + correspondence,
because it touches every unit and proves numbering, approvals, bilingual fields and records in one go.

## Ownership & handover
Everything lives in the client's tenant, built with PnP provisioning templates / site scripts and solution-aware
flows in a managed environment. Repo, admin guide, and a weekly demo per phase.
