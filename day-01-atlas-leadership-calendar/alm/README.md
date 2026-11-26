# ATLAS · dev → prod pipeline (GitHub Actions + Power Platform CLI)

Moves the ATLAS canvas app from a **DEV** environment to a **PROD** environment as a managed solution,
with the source kept in this repo and a manual approval before anything reaches production.

```
 DEV environment (Dataverse)          GitHub                              PROD environment (Dataverse)
 ATLAS solution, unmanaged   ──export──▶  alm/solution/src  ──build──▶  managed .zip  ──approve──▶  ATLAS solution, managed
 points at the DEV SharePoint site      (pull request)        (artifact)                      points at the PROD site
                                                                                              (via prod.json)
```

| File | What it does |
|---|---|
| `.github/workflows/atlas-export.yml` (repo root) | Run by hand. Exports the solution from DEV, unpacks it into `alm/solution/src/` and opens a pull request |
| `.github/workflows/atlas-deploy.yml` (repo root) | On merge to `main` (or by hand). Packs a **managed** solution, waits for your approval, imports it into PROD with `prod.json` |
| `deployment-settings/prod.json` | PROD values for the environment variables (SharePoint site URL and list IDs) |
| `deployment-settings/template.generated.json` | Written by every export: lists every environment variable and connection reference the solution really has |
| `solution/src/` | The unpacked solution (filled in by the first export) |

## Why not Power Platform pipelines?

Pipelines are the built-in option, but every pipeline **target** must be a managed environment
(enforced since October 2026), and from **February 2027** every user who opens an app in a managed
environment needs a premium licence. That breaks the "standard licences only" brief.
GitHub Actions with the Power Platform CLI deploys to an ordinary environment instead, so leadership
users keep running ATLAS on Microsoft 365 licences.

*(Checked on Microsoft Learn, 25 Nov 2026.)*

## What you need

| Piece | For the demo | For a real client |
|---|---|---|
| Tenant | Microsoft 365 trial tenant where you are Global admin | Client tenant, with a Power Platform admin |
| DEV environment | **Trial** environment with Dataverse (start a Power Apps trial on your admin user; lasts 30 days) | Sandbox environment with Dataverse |
| PROD environment | **Default** environment, with Dataverse added (uses the default environment's included capacity) | Production environment with Dataverse (needs 1 GB free database capacity) |
| SharePoint | Two sites: `…/sites/leadership-dev` (sample data) and `…/sites/leadership` (empty) | Same pattern |
| GitHub | This repo, Actions enabled | Client's repo or yours |

Both environments must have Dataverse: solutions and the CLI only work there. ATLAS still stores its
data in SharePoint, and users don't need a Dataverse or premium licence to run it.

> ⚠️ Microsoft says the default environment shouldn't hold production workloads (no backup guarantees).
> It's fine for the demo. For a client, use a production environment and plan the 1 GB capacity.

## One-time setup (about 45 minutes)

### 1. SharePoint sites and lists

```powershell
# DEV: lists + 41 sample activities
./scripts/Create-AtlasList.ps1 -SiteUrl https://<tenant>.sharepoint.com/sites/leadership-dev -ClientId <pnp-app-id>
# PROD: same lists, no sample data. Note the two list IDs it prints.
./scripts/Create-AtlasList.ps1 -SiteUrl https://<tenant>.sharepoint.com/sites/leadership -ClientId <pnp-app-id> -SkipSampleData
```

### 2. Build the app inside a solution in DEV

1. In DEV, create a publisher (prefix **`atlas`**) and a solution **ATLAS Leadership Calendar**
   (unique name **`ATLASLeadershipCalendar`**, the workflows use this name).
2. In the solution, add three environment variables, type **Data source**, connector SharePoint:
   `atlas_SiteUrl` (parameter: Site), `atlas_CalendarList` and `atlas_EditorsList` (parameter: List).
   Point them at the DEV site.
3. Create the canvas app **from inside the solution**. When you add the SharePoint data source,
   open the **Advanced** tab and pick the environment variables, so the app never hard-codes the DEV site.
4. Build ATLAS (formulas in `../app/formulas.md`), save, publish.

### 3. Service principal and application users

```powershell
pac auth create --environment <DEV environment URL>
pac admin create-service-principal --environment <DEV environment ID> --name "ATLAS GitHub deploy"
```

It prints the tenant ID, application ID and client secret (keep the secret safe). Then add the same
app as an **application user** with **System Administrator** in PROD:
Power Platform admin center → Environments → PROD → Settings → Users + permissions → Application users → New app user.

### 4. GitHub settings

Settings → Secrets and variables → Actions:

| Kind | Name | Value |
|---|---|---|
| Variable | `ATLAS_TENANT_ID` | Tenant ID |
| Variable | `ATLAS_CLIENT_ID` | Application ID |
| Variable | `ATLAS_DEV_URL` | `https://<dev-org>.crm4.dynamics.com` |
| Secret | `ATLAS_CLIENT_SECRET` | Client secret |

Settings → Environments → **New environment** `atlas-prod`:
- add variable `ATLAS_PROD_URL` = PROD environment URL,
- tick **Required reviewers** and add yourself.

Settings → Actions → General → tick **Allow GitHub Actions to create and approve pull requests**
(the export workflow opens a PR).

### 5. PROD values

Fill in `deployment-settings/prod.json` with the PROD site URL and the two list IDs from step 1.
The deploy workflow refuses to run while any value is still empty or a `<placeholder>`.

## Day-to-day loop

1. Change the app in DEV, save and publish.
2. Actions → **ATLAS · export from dev** → Run. Review the PR (you can see which files changed) and merge.
3. The merge starts **ATLAS · deploy to prod**. Approve it when GitHub asks.
4. First deployment only: in PROD, **share** the app with the leadership group, then **Publish to Teams**
   from PROD (not DEV), so the Teams tab opens the production app. Later deployments update the same app and tab.

## Gotchas

- **Who owns the app in PROD?** Solution components are owned by the identity that imported them,
  here the service principal. Share the app (and add yourself as co-owner) after the first import.
- **Connection references:** canvas apps connect to SharePoint as the signed-in user. If
  `template.generated.json` ever lists a connection reference (for example after you add a flow),
  create that connection in PROD and add its ID to `prod.json`.
- **Version numbers:** the deploy job sets the revision number to the GitHub run number, so PROD always
  gets a higher version and upgrades cleanly.
- **The `.msapp` stays binary** in `solution/src/CanvasApps/`. You'll see that it changed, not what changed.
  The app's formulas are documented in `../app/formulas.md`.
- **Trial environment expiry:** the DEV trial expires after 30 days. Your source is safe in the repo;
  to carry on, import the unmanaged solution into a new DEV environment.
- **Secret rotation:** the client secret from `create-service-principal` expires. Put the expiry date in your calendar.
- **Next step for security:** swap the client secret for GitHub OIDC (`pac auth create --githubFederated`)
  so no secret is stored at all.

## Not tested yet

These workflows were written against the Microsoft Learn docs for PAC CLI (checked 25 Nov 2026) and
haven't run against a live tenant. Check on the first run:
`pac solution list` output with the service principal, `--stage-and-upgrade` on the second deployment,
and that the SharePoint data-source variables accept list IDs from `prod.json`.
