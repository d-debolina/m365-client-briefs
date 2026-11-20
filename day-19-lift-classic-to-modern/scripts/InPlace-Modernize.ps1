# LIFT wave 1/2: in-place modernization of a classic team site (PnP PowerShell). Test on a copy first!
param([string]$SiteUrl, [string]$ClientId, [string]$Alias, [switch]$WhatIf)
Connect-PnPOnline -Url $SiteUrl -Interactive -ClientId $ClientId

# 1. Snapshot permissions BEFORE (evidence + rollback reference)
Get-PnPSiteGroup | Select-Object Title, @{n="Members";e={($_.Users | ForEach-Object LoginName) -join ";"}} |
  Export-Csv ".\perm-before-$Alias.csv" -NoTypeInformation

# 2. Connect the site to a new Microsoft 365 group ("groupify")
if (-not $WhatIf) { Add-PnPMicrosoft365GroupToSite -Url $SiteUrl -Alias $Alias -DisplayName $Alias -KeepOldHomePage }

# 3. Transform classic wiki/web part pages in SitePages into modern pages (draft, keep the source)
#    Microsoft's current guidance: assess with the Microsoft 365 Assessment tool, transform a representative wave, validate, then expand.
Get-PnPListItem -List "SitePages" -Fields "FileLeafRef" | ForEach-Object {
  $page = $_["FileLeafRef"]
  if ($page -ne "Home.aspx") { if (-not $WhatIf) { ConvertTo-PnPPage -Identity $page -Overwrite:$false -AddPageAcceptBanner } ; Write-Host "transformed: $page" }
}
Write-Host "Next: validate pages, then compare permissions with perm-before-$Alias.csv"
