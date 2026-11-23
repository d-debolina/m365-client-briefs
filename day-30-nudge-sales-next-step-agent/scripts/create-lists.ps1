# Creates the three NUDGE lists on a SharePoint site with PnP PowerShell.
# Requires PnP.PowerShell 2.x+ and your own Entra app registration (ClientId) for interactive login.
# Usage: ./create-lists.ps1 -SiteUrl https://<tenant>.sharepoint.com/sites/SalesNudge -ClientId <app-id>
param(
  [Parameter(Mandatory)] [string] $SiteUrl,
  [Parameter(Mandatory)] [string] $ClientId
)
Connect-PnPOnline -Url $SiteUrl -ClientId $ClientId -Interactive

function Add-List($name) {
  if (-not (Get-PnPList -Identity $name -ErrorAction SilentlyContinue)) { New-PnPList -Title $name -Template GenericList | Out-Null }
}

# Accounts
Add-List "Accounts"
Add-PnPField -List "Accounts" -DisplayName "AccountId" -InternalName "AccountId" -Type Text -AddToDefaultView | Out-Null
Add-PnPField -List "Accounts" -DisplayName "OwnerEmail" -InternalName "OwnerEmail" -Type Text -AddToDefaultView | Out-Null
Add-PnPField -List "Accounts" -DisplayName "Stage" -InternalName "Stage" -Type Choice -Choices "Prospect","Evaluation","First cases","Adopted","At risk" -AddToDefaultView | Out-Null
Add-PnPField -List "Accounts" -DisplayName "FocusProduct" -InternalName "FocusProduct" -Type Text | Out-Null
Add-PnPField -List "Accounts" -DisplayName "KeySurgeon" -InternalName "KeySurgeon" -Type Text | Out-Null
Add-PnPField -List "Accounts" -DisplayName "LastContact" -InternalName "LastContact" -Type DateTime -AddToDefaultView | Out-Null

# Commitments
Add-List "Commitments"
foreach ($f in "CommitmentId","AccountId","AccountName","OwnerEmail") {
  Add-PnPField -List "Commitments" -DisplayName $f -InternalName $f -Type Text -AddToDefaultView | Out-Null
}
Add-PnPField -List "Commitments" -DisplayName "Type" -InternalName "CommitmentType" -Type Choice -Choices "Proctorship","In-service training","Product evaluation","Value analysis meeting","Sample delivery","Follow-up call" -AddToDefaultView | Out-Null
Add-PnPField -List "Commitments" -DisplayName "EventDate" -InternalName "EventDate" -Type DateTime -AddToDefaultView | Out-Null
Add-PnPField -List "Commitments" -DisplayName "FollowUpDate" -InternalName "FollowUpDate" -Type DateTime -AddToDefaultView | Out-Null
Add-PnPField -List "Commitments" -DisplayName "FollowUpQuestion" -InternalName "FollowUpQuestion" -Type Note | Out-Null
Add-PnPField -List "Commitments" -DisplayName "Status" -InternalName "Status" -Type Choice -Choices "Open","Asked","Done","Cancelled" -AddToDefaultView | Out-Null
Add-PnPField -List "Commitments" -DisplayName "Outcome" -InternalName "Outcome" -Type Note | Out-Null
Add-PnPField -List "Commitments" -DisplayName "NextStep" -InternalName "NextStep" -Type Note | Out-Null
foreach ($f in "AccountId","OwnerEmail","FollowUpDate","Status") {
  Set-PnPField -List "Commitments" -Identity $f -Values @{ Indexed = $true } | Out-Null
}

# Activities
Add-List "Activities"
Add-PnPField -List "Activities" -DisplayName "AccountId" -InternalName "AccountId" -Type Text -AddToDefaultView | Out-Null
Add-PnPField -List "Activities" -DisplayName "Kind" -InternalName "Kind" -Type Choice -Choices "Call","Visit","Email","Case support","Lunch & learn" -AddToDefaultView | Out-Null
Add-PnPField -List "Activities" -DisplayName "ActivityDate" -InternalName "ActivityDate" -Type DateTime -AddToDefaultView | Out-Null
Add-PnPField -List "Activities" -DisplayName "OwnerEmail" -InternalName "OwnerEmail" -Type Text | Out-Null

Write-Host "NUDGE lists ready. Import data/*.csv with the list's 'Edit in grid view' paste, or PnP Add-PnPListItem."
