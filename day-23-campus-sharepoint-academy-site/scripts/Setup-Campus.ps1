# CAMPUS: libraries, metadata and permissions with PnP PowerShell (test site first)
param([string]$Url = "https://contoso.sharepoint.com/sites/academy", [string]$ClientId)
Connect-PnPOnline -Url $Url -Interactive -ClientId $ClientId
foreach ($lib in "Course Materials","Trainer Drafts") { New-PnPList -Title $lib -Template DocumentLibrary -OnQuickLaunch -ErrorAction SilentlyContinue }
$cols = @(
  @{N="Course";T="Choice";C=@("Digital Skills 2027")},
  @{N="Module";T="Choice";C=@("Microsoft 365 basics","Teams for meetings","SharePoint for site owners","Power Automate 101","Copilot prompting","Security awareness")},
  @{N="AssetType";T="Choice";C=@("Slide deck","Handout","Video","Exercise file","Quiz","Recording")},
  @{N="Level";T="Choice";C=@("Beginner","Intermediate","Advanced")},
  @{N="ReviewBy";T="DateTime"})
foreach ($lib in "Course Materials","Trainer Drafts") { foreach ($c in $cols) {
  if ($c.T -eq "Choice") { Add-PnPField -List $lib -DisplayName $c.N -InternalName $c.N -Type Choice -Choices $c.C -AddToDefaultView -ErrorAction SilentlyContinue }
  else { Add-PnPField -List $lib -DisplayName $c.N -InternalName $c.N -Type $c.T -AddToDefaultView -ErrorAction SilentlyContinue } } }
# Trainer Drafts: unique permissions, trainers only
Set-PnPList -Identity "Trainer Drafts" -BreakRoleInheritance -CopyRoleAssignments:$false
Set-PnPListPermission -Identity "Trainer Drafts" -Group "Academy Owners" -AddRole "Full Control"
Set-PnPListPermission -Identity "Trainer Drafts" -User "sg-academy-trainers@contoso.example" -AddRole "Edit"
# Permissions report for the quarterly review
Get-PnPSiteGroup | Select Title, @{n="Members";e={($_.Users | % LoginName) -join ";"}} | Export-Csv .\campus-permissions.csv -NoTypeInformation
