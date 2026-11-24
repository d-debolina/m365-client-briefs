<#
  Run through the RMM tool as SYSTEM, once per PC (or when rotating the certificate).
  Imports the PFX into LocalMachine\My with a NON-exportable private key, then deletes the PFX.
  Pass the password from the RMM tool's secure/secret variable, never hard-code it.
#>
param([Parameter(Mandatory)][string]$PfxPath, [Parameter(Mandatory)][string]$PfxPasswordPlain)

$ErrorActionPreference = 'Stop'
$pw = ConvertTo-SecureString $PfxPasswordPlain -AsPlainText -Force
$cert = Import-PfxCertificate -FilePath $PfxPath -CertStoreLocation 'Cert:\LocalMachine\My' -Password $pw   # non-exportable by default
Remove-Item -LiteralPath $PfxPath -Force
Write-Output "Installed $($cert.Thumbprint), expires $($cert.NotAfter.ToString('yyyy-MM-dd'))"
exit 0
