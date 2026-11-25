# Day 32 · HAUL – Hash-checked, App-only, Unattended, Logged

Upload recently changed files from many remote Windows PCs to one SharePoint Online library, run unattended by
an RMM tool, **without a single password in the script**. HAUL uses an Entra app registration with a certificate,
gives that app `write` on one library only (`Lists.SelectedOperations.Selected`), skips files it already uploaded
(SHA-256 state file), copes with locked files, throttling and lost connections, and returns exit codes an RMM
dashboard can alert on.

> All PCs, folders, tenants and IDs here are fictional. Test in a developer or trial tenant first.

## What's inside
| Path | What it is |
|---|---|
| `scripts/Invoke-Haul.ps1` | The upload script (Windows PowerShell 5.1+, no modules needed) |
| `scripts/New-HaulCertificate.ps1` | Creates the certificate (CNG key, 2 years) and exports `.cer` + `.pfx` |
| `scripts/Install-HaulCertificate.ps1` | RMM job: imports the PFX into `LocalMachine\My` as non-exportable, deletes the PFX |
| `config/haul.config.sample.json` | Settings: tenant, app, thumbprint, drive ID, folders, state and log paths |
| `docs/grant-permission.http` | Graph calls to grant the app `write` on one library and create the top folder |
| `docs/rmm-deployment.md` | Generic deployment and certificate-rotation steps for any RMM tool |
| `docs/exit-codes.md`, `docs/troubleshooting.md` | What each exit code and log line means |
| `sample/pm-folder-snapshot.csv` | 25 fictional files on 4 PCs (incl. a locked file and a sub-folder file) |
| `sample/state-before.json`, `sample/haul-sample.log` | State from the previous run and an example log |
| `scripts/simulate_run.py`, `tests/` | Python simulation of the selection rules + 6 tests |
| `architecture.*` | Diagram (PNG / SVG / editable DOT) |

## How to use
1. `python scripts/simulate_run.py` shows what HAUL would upload from each PC; `python -m pytest tests` checks the rules.
2. Follow `docs/grant-permission.http` to create the app registration and the least-privilege grant.
3. Run `New-HaulCertificate.ps1`, upload the `.cer`, fill in `haul.config.json`.
4. On one test PC: `Invoke-Haul.ps1 -ConfigPath ... -DryRun`, then without `-DryRun`.
5. Roll out through your RMM tool (`docs/rmm-deployment.md`).

> The PowerShell scripts are written for Windows PowerShell 5.1 on Windows 10/11 and Server 2016+.
> Always test on a lab PC before deploying to client machines.
