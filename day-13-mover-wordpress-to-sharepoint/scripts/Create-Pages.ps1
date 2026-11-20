# MOVER: create modern pages from page-manifest.csv with PnP PowerShell. Test on a dev site first!
# Requires: PnP.PowerShell 2.x+, an Entra app registration for PnP (Register-PnPEntraIDAppForInteractiveLogin)
param([string]$Tenant = "contoso", [string]$ClientId = "<your-pnp-app-id>", [string]$Manifest = "./page-manifest.csv")

$rows = Import-Csv $Manifest
foreach ($site in ($rows | Select-Object -ExpandProperty site -Unique)) {
    Connect-PnPOnline -Url "https://$Tenant.sharepoint.com/sites/$site" -Interactive -ClientId $ClientId
    foreach ($r in ($rows | Where-Object site -eq $site)) {
        $name = $r.pageName -replace ".aspx$",""
        if (Get-PnPPage -Identity $name -ErrorAction SilentlyContinue) { Write-Host "skip (exists): $name"; continue }  # idempotent re-runs
        $page = Add-PnPPage -Name $name -Title $r.title -LayoutType Article
        Add-PnPPageSection -Page $page -SectionTemplate OneColumn | Out-Null
        Add-PnPPageTextPart -Page $page -Text $r.html -Section 1 -Column 1 | Out-Null
        # Topic = managed metadata column on Site Pages (create it once per site, bound to the "Intranet Topics" term set)
        $item = Get-PnPListItem -List "SitePages" -Query "<View><Query><Where><Eq><FieldRef Name='FileLeafRef'/><Value Type='Text'>$($r.pageName)</Value></Eq></Where></Query></View>"
        Set-PnPListItem -List "SitePages" -Identity $item.Id -Values @{ "Topic" = "Intranet Topics|$($r.topic)" } | Out-Null
        if ($r.isNews -eq "True") { Set-PnPPage -Identity $name -PromoteAs NewsArticle | Out-Null }
        Set-PnPPage -Identity $name -Publish | Out-Null
        Write-Host "created: $site/$($r.pageName)"
    }
}
