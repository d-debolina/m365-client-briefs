# CREW · ALM: Dev → Test → Prod

Checked against Microsoft Learn, November 2026.

## Solutions
| Solution | Contains | Why separate |
|---|---|---|
| `CREW_Core` | tables, choices, security roles, team template, environment variable definitions | changes rarely, deploy first |
| `CREW_Logic` | plug-in assembly + steps, custom API `crew_RecalculateDemand`, cloud flows, connection references | deploys often |
| `CREW_App` | model-driven app, custom pages, PCF board control, site map | UI only |

One publisher (`crew`). Always **managed** in Test and Prod. Never customise Prod directly.

## Environment variables (definitions in `CREW_Core`, values per environment)
| Name | Dev | Test | Prod |
|---|---|---|---|
| `crew_PlanningEngineUrl` | dev Function URL | test Function URL | prod Function URL |
| `crew_ProjectsChannelId` | test channel | test channel | live channel |
| `crew_MaxHoursPerWeek` | 60 | 60 | 60 |
| `crew_ImportLibraryUrl` | dev site | test site | prod site |

Leave the **current value out of the solution** (remove it before export) so each environment keeps its own.

## Pipeline (Power Platform pipelines)
1. Host: a dedicated production environment with the *Power Platform Pipelines* app (or the platform host).
2. Stages: **Dev (developer env) → Test → Prod**. Add **delegated deployment** with a service principal for Prod,
   plus a pre-deployment approval.
3. **Target environments (Test, Prod) must be managed environments.** Microsoft started enforcing this in
   October 2026: 30-day grace period, one 30-day extension, then deployments to unmanaged targets are blocked.
4. Managed environments come with a licensing rule: from **February 2027** users without a qualifying licence
   can't open apps in a managed environment. CREW users need Power Apps Premium anyway, so check that
   licences are assigned before you flip the switch.

## Plug-in versioning
Bump the assembly version on every significant change. The solution update might not notice that a managed
assembly changed if its fully qualified name doesn't change.
