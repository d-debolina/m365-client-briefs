<#
  Run ONCE on an admin workstation (not on client PCs).
  Creates a 2-year certificate with a CNG (KSP) key, which HAUL needs for PS256/PSS signing,
  then exports:
    haul-<client>.cer  -> upload to the app registration (Certificates & secrets)
    haul-<client>.pfx  -> deploy to PCs with Install-HaulCertificate.ps1, then delete it
  One certificate (and ideally one app registration) per client organisation, so a stolen key
  only exposes that client's drop folder.
#>
param([Parameter(Mandatory)][string]$ClientCode, [Parameter(Mandatory)][securestring]$PfxPassword)

$cert = New-SelfSignedCertificate -Subject "CN=HAUL-$ClientCode" -CertStoreLocation 'Cert:\CurrentUser\My' `
    -KeyAlgorithm RSA -KeyLength 2048 -KeySpec Signature -KeyExportPolicy Exportable `
    -Provider 'Microsoft Software Key Storage Provider' -NotAfter (Get-Date).AddYears(2)

Export-Certificate    -Cert $cert -FilePath ".\haul-$ClientCode.cer" | Out-Null
Export-PfxCertificate -Cert $cert -FilePath ".\haul-$ClientCode.pfx" -Password $PfxPassword | Out-Null
Write-Output "Thumbprint: $($cert.Thumbprint)  (put this in haul.config.json)"
Write-Output "Expires:    $($cert.NotAfter.ToString('yyyy-MM-dd'))  (add a rotation reminder 30 days before)"
