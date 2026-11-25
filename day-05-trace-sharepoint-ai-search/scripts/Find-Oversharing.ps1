# TRACE – pre-launch oversharing report (PnP.PowerShell 2.x). Fictional demo tenant only.
param([string]$SiteUrl, [string]$ClientId)
Connect-PnPOnline -Url $SiteUrl -Interactive -ClientId $ClientId
$report = @()
foreach ($list in Get-PnPList | Where-Object { $_.BaseTemplate -eq 101 -and -not $_.Hidden }) {
    $items = Get-PnPListItem -List $list -PageSize 500 -Fields "FileRef","HasUniqueRoleAssignments"
    foreach ($item in $items) {
        $links = Get-PnPFileSharingLink -Identity $item["FileRef"] -ErrorAction SilentlyContinue
        foreach ($l in $links) {
            if ($l.Link.Scope -in @("anonymous","organization")) {
                $report += [pscustomobject]@{ Library=$list.Title; File=$item["FileRef"]; Scope=$l.Link.Scope; Type=$l.Link.Type }
            }
        }
    }
}
$report | Export-Csv -Path ".\oversharing-report.csv" -NoTypeInformation
Write-Host "Found $($report.Count) broad sharing links"
