<#
.SYNOPSIS
  Creates the ATLAS Leadership_Calendar list (+ ATLAS_Editors list) and imports the fictional sample activities.
.EXAMPLE
  ./Create-AtlasList.ps1 -SiteUrl https://contoso.sharepoint.com/sites/leadership-dev -ClientId <your-entra-app-id>
.EXAMPLE
  # PROD site for the ALM pipeline: same lists, no sample data
  ./Create-AtlasList.ps1 -SiteUrl https://contoso.sharepoint.com/sites/leadership -ClientId <your-entra-app-id> -SkipSampleData
.NOTES
  Requires PnP.PowerShell 2.x+ and your own Entra app registration (PnP no longer ships a shared app).
  Use a developer tenant. All sample data is fictional.
#>
param(
  [Parameter(Mandatory)] [string] $SiteUrl,
  [Parameter(Mandatory)] [string] $ClientId,
  [string] $CsvPath = (Join-Path $PSScriptRoot "..\list\sample-activities.csv"),
  [switch] $SkipSampleData
)

Connect-PnPOnline -Url $SiteUrl -ClientId $ClientId -Interactive

$list = "Leadership_Calendar"
New-PnPList -Title $list -Template GenericList -OnQuickLaunch | Out-Null

$categories = @("Leadership Team Meeting","Business Review","Long-Range Planning","Budget Process","Board Meeting",
  "Executive Visit","Town Hall","Strategy Offsite","Quarterly Close","Risk Committee","People Review",
  "Customer Summit","Partner Day","Audit","Holiday / Blackout")

Add-PnPField -List $list -DisplayName "Category"  -InternalName "Category"  -Type Choice -Choices $categories -Required -AddToDefaultView
Add-PnPField -List $list -DisplayName "StartDate" -InternalName "StartDate" -Type DateTime -Required -AddToDefaultView
Add-PnPField -List $list -DisplayName "EndDate"   -InternalName "EndDate"   -Type DateTime -Required -AddToDefaultView
Set-PnPField -List $list -Identity "StartDate" -Values @{ DisplayFormat = 0 }   # date only
Set-PnPField -List $list -Identity "EndDate"   -Values @{ DisplayFormat = 0 }
Add-PnPField -List $list -DisplayName "AllDay"    -InternalName "AllDay"    -Type Boolean
Add-PnPField -List $list -DisplayName "StartTime" -InternalName "StartTime" -Type Text
Add-PnPField -List $list -DisplayName "EndTime"   -InternalName "EndTime"   -Type Text
Add-PnPField -List $list -DisplayName "Region"    -InternalName "Region"    -Type Choice -Choices @("Group","North","South","East","West","Central") -Required -AddToDefaultView
Add-PnPField -List $list -DisplayName "Location"  -InternalName "Location"  -Type Text
Add-PnPField -List $list -DisplayName "Visibility" -InternalName "Visibility" -Type Choice -Choices @("Leadership team","All managers","Everyone")
Add-PnPField -List $list -DisplayName "Description" -InternalName "Description" -Type Note
Add-PnPField -List $list -DisplayName "DocumentLink" -InternalName "DocumentLink" -Type URL
Add-PnPField -List $list -DisplayName "MeetingLink"  -InternalName "MeetingLink"  -Type URL

# List validation: end date can't be before start date
$l = Get-PnPList -Identity $list
$l.ValidationFormula = "=[EndDate]>=[StartDate]"
$l.ValidationMessage = "End date can't be before the start date."
$l.Update(); Invoke-PnPQuery

# Editors list used by the app to show/hide edit buttons
New-PnPList -Title "ATLAS_Editors" -Template GenericList | Out-Null
Add-PnPField -List "ATLAS_Editors" -DisplayName "Email" -InternalName "Email" -Type Text -AddToDefaultView

# Import sample data (skip for PROD)
if (-not $SkipSampleData) { Import-Csv $CsvPath | ForEach-Object {
  $values = @{
    Title = $_.Title; Category = $_.Category; StartDate = $_.StartDate; EndDate = $_.EndDate
    AllDay = ($_.AllDay -eq "Yes"); StartTime = $_.StartTime; EndTime = $_.EndTime
    Region = $_.Region; Location = $_.Location; Visibility = $_.Visibility; Description = $_.Description
  }
  if ($_.DocumentLink) { $values.DocumentLink = "$($_.DocumentLink), Documents" }
  if ($_.MeetingLink)  { $values.MeetingLink  = "$($_.MeetingLink), Join meeting" }
  Add-PnPListItem -List $list -Values $values | Out-Null
} }

# List IDs: paste these into alm/deployment-settings/prod.json when this is the PROD site
Write-Host "Site URL:                $SiteUrl"
Write-Host "Leadership_Calendar ID:  $((Get-PnPList -Identity $list).Id)"
Write-Host "ATLAS_Editors ID:        $((Get-PnPList -Identity 'ATLAS_Editors').Id)"
Write-Host "Done. Now break inheritance on the list: Read for viewers, Contribute for 'ATLAS Editors'."
