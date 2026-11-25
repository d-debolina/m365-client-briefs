# SHELF: tenant settings used in the post (SharePoint Online Management Shell). Review before running!
Connect-SPOService -Url https://contoso-admin.sharepoint.com

# 1. Push people to "Add shortcut to My files" instead of the Sync button (existing syncs keep working)
Set-SPOTenant -HideSyncButtonOnTeamSite $true

# 2. Keep a sensitive site out of org-wide search and Copilot while its permissions are reviewed
#    (Restricted Content Discovery: needs SharePoint Advanced Management or a Copilot licence)
Set-SPOSite -Identity https://contoso.sharepoint.com/sites/HR -RestrictContentOrgWideSearch $true

# 3. Check the setting
Get-SPOSite -Identity https://contoso.sharepoint.com/sites/HR | Select Url, RestrictContentOrgWideSearch
