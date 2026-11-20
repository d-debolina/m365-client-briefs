# LIFT wave 3: restructure a classic site with subsites into flat modern sites (ShareGate PowerShell, licensed).
# Pattern: one subsite → one new modern team/communication site, associated to a hub. Check cmdlet parameters against your ShareGate version.
Import-Module Sharegate
$src = Connect-Site -Url "https://contoso.sharepoint.com/sites/projects" -Browser
$map = Import-Csv ".\subsite-to-site-map.csv"   # columns: SubsiteUrl, TargetUrl
foreach ($m in $map) {
  $s = Connect-Site -Url $m.SubsiteUrl -UseCredentialsFrom $src
  $t = Connect-Site -Url $m.TargetUrl  -UseCredentialsFrom $src
  Get-List -Site $s | Where-Object { -not $_.Hidden } | ForEach-Object { Copy-List -List $_ -DestinationSite $t }   # keeps metadata, versions, permissions per ShareGate settings
}
