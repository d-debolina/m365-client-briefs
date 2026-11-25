# LEDGER governance checklist (day one, not "later")

## Environments & ALM
- [ ] Dev, Test, Prod environments (Managed Environments on Prod)
- [ ] Agent, custom connector and environment variables in **one solution**; deploy with Power Platform Pipelines
- [ ] Connection references, not personal connections

## Data & security
- [ ] Environment DLP policy: custom connector + SharePoint + Dataverse in **Business**; block everything else (incl. HTTP)
- [ ] API key in Azure Key Vault → environment variable (secret) → custom connector (`@environmentVariables("...")`)
- [ ] Key Vault: *Key Vault Secrets User* for the Copilot Studio service, `AllowedEnvironments` / `AllowedAgents` tags
- [ ] Remember: anyone who can **edit** the agent could expose a secret used in a topic. Keep the maker group small
- [ ] SharePoint knowledge = user authentication: people only get answers from files they can open
- [ ] Agent shared with an Entra security group (Ops team), not "everyone"
- [ ] CreateTask requires explicit confirmation (instructions + tool description)

## Monitoring
- [ ] Transcripts in Dataverse, retention agreed with compliance
- [ ] Weekly: analytics (resolution, escalation), credits used, failed tool calls
- [ ] Monthly: run `eval/test-questions.csv` after every change
