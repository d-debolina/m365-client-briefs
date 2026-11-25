# HAUL exit codes (map these to alerts in the RMM tool)

| Code | Meaning | What to do |
|---|---|---|
| 0 | Success, or nothing new to upload | Nothing |
| 1 | Some files failed (locked, or upload error); the rest uploaded | Usually self-heals on the next run. Alert if it repeats 3 times |
| 2 | Authentication failed (wrong client ID, cert not registered, consent removed) | Check the app registration and the sign-in logs for the service principal |
| 3 | Config or certificate problem (missing setting, cert not in LocalMachine\My, no private key) | Re-run Install-HaulCertificate.ps1 / fix haul.config.json |
| 4 | No network or Microsoft 365 unreachable | Ignore single occurrences; alert if the PC is offline for days |
| 5 | Another HAUL run is still in progress | Lengthen the schedule interval |
