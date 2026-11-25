# TALLY: create the list with PnP PowerShell, then import the CSV. Test site only.
param([string]$Url = "https://contoso.sharepoint.com/sites/migration", [string]$ClientId)
Connect-PnPOnline -Url $Url -Interactive -ClientId $ClientId
New-PnPList -Title "Migration validation" -Template GenericList -OnQuickLaunch
$l = "Migration validation"
Add-PnPField -List $l -DisplayName "Workload" -InternalName "Workload" -Type Text -AddToDefaultView
Add-PnPField -List $l -DisplayName "Wave" -InternalName "Wave" -Type Choice -Choices "Wave 1","Wave 2","Wave 3" -AddToDefaultView
Add-PnPField -List $l -DisplayName "Check" -InternalName "Check" -Type Text -AddToDefaultView
Add-PnPField -List $l -DisplayName "Owner" -InternalName "Owner" -Type User -AddToDefaultView
Add-PnPField -List $l -DisplayName "Status" -InternalName "Status" -Type Choice -Choices "Not started","In progress","Passed","Failed","Blocked","N/A" -AddToDefaultView
Add-PnPField -List $l -DisplayName "DueDate" -InternalName "DueDate" -Type DateTime -AddToDefaultView
Add-PnPField -List $l -DisplayName "Evidence" -InternalName "Evidence" -Type URL -AddToDefaultView
Add-PnPField -List $l -DisplayName "Severity" -InternalName "Severity" -Type Choice -Choices "Low","Medium","High"
Set-PnPField -List $l -Identity "Status" -Values @{CustomFormatter = (Get-Content ..\formatting\status-pill.json -Raw)}
Import-Csv ..\list\validation-items.csv | ForEach-Object {
  Add-PnPListItem -List $l -Values @{ Title=$_.ID; Workload=$_.Workload; Wave=$_.Wave; Check=$_.Check; Status=$_.Status; DueDate=$_.DueDate } | Out-Null
}
