# Deploying HAUL through an RMM tool (generic steps)

1. **Once per client org:** run `New-HaulCertificate.ps1`, create the app registration, grant `write` on the
   drop library (`grant-permission.http`), fill in `haul.config.json`.
2. **Once per PC (RMM job, runs as SYSTEM):**
   - copy `Invoke-Haul.ps1` and `haul.config.json` to `C:\ProgramData\Haul\`
   - copy the PFX to a temp path and run `Install-HaulCertificate.ps1` with the password from a secret variable
   - restrict `C:\ProgramData\Haul\` to SYSTEM and Administrators
3. **Schedule (RMM job, runs as SYSTEM), e.g. hourly:**
   `powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\ProgramData\Haul\Invoke-Haul.ps1 -ConfigPath C:\ProgramData\Haul\haul.config.json`
4. **Pilot:** run with `-DryRun` on 2–3 PCs first, read the output, then switch it on.
5. **Alerting:** treat exit code 2 or 3 as "needs a human", 1 or 4 only when repeated.
6. **Certificate rotation:** upload the new `.cer` next to the old one, push the new PFX + thumbprint,
   then remove the old certificate from the app registration.
