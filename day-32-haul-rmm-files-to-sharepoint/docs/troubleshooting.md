# Troubleshooting

| Symptom in the log | Likely cause | Fix |
|---|---|---|
| `Certificate not found in LocalMachine\My` | PFX installed in CurrentUser, or wrong thumbprint | Re-run Install-HaulCertificate.ps1 as SYSTEM; check the thumbprint |
| `Method not supported` / PSS error during signing | Key created with the old CSP provider, which can't do PSS | Recreate the cert with `-Provider 'Microsoft Software Key Storage Provider'` |
| `AADSTS700027` | Certificate not uploaded to the app registration, or expired | Upload the .cer; check dates |
| HTTP 403 on upload | App has no `write` grant on the library, or consent missing | Repeat step 3 of grant-permission.http |
| HTTP 409 when creating the PC folder | Another run created it first | Harmless, HAUL ignores it |
| `LOCKED, will retry next run` | The PM software has the file open exclusively | Harmless; uploads on a later run |
| HTTP 429 / 503 with waits | SharePoint throttling | HAUL honours Retry-After; spread schedules across PCs |
