# SCOUT – AI agent readiness audit checklist

## 1. Environment
- [ ] Environment strategy (default env locked down? dev/test/prod?)
- [ ] Environment routing for makers
- [ ] Managed Environments enabled where agents run

## 2. Licensing & cost
- [ ] Who has Microsoft 365 Copilot licences (affects agent billing)
- [ ] Copilot Studio capacity or pay-as-you-go; credit caps set
- [ ] Estimated credits per use case (classic vs generative answers, actions, tenant graph grounding)

## 3. Data & knowledge
- [ ] Where the knowledge lives (SharePoint, ERP, Dataverse)
- [ ] Oversharing check before grounding on SharePoint
- [ ] Sensitivity labels and Purview DLP for Copilot

## 4. Security & governance
- [ ] Data policies (connectors, HTTP, channels, authentication)
- [ ] Agent inventory and owners
- [ ] Runtime protection / external threat detection need
- [ ] Audit in Purview, alerts in Sentinel

## 5. Integration
- [ ] Systems to connect (APIs, MCP servers, custom connectors)
- [ ] Identity model per integration (user vs maker credentials)

## 6. People & process
- [ ] Process owner per use case
- [ ] Human approval points
- [ ] Success metrics (time saved, deflection, error rate)
