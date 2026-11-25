# DOCKET – Power Automate flows (standard connectors only)

## 1. New case → document set with the right permissions
Trigger: Power Apps button or *When an item is created* in a "Case intake" list.
1. **Create new document set** (SharePoint connector action) in *Case files*, name = Case ID, content type = Case.
2. Update the document set properties (client, practice, lead, retainer, restricted).
3. If **Restricted = Yes**, use *Send an HTTP request to SharePoint*:
   - `POST _api/web/lists/getbytitle('Case files')/items({id})/breakroleinheritance(copyRoleAssignments=false,clearSubscopes=true)`
   - `POST .../items({id})/roleassignments/addroleassignment(principalid={groupId},roledefid={editRoleId})` for the
     case team group and the partners group.
4. If **External access = Yes**, create folder `Client Share/<Practice>/<Case ID>` and send the lead a Teams message
   with a link to share it (people share; the flow never shares with outside addresses itself).
5. Add the case to the *Allocations* list with the lead's first estimate.

## 2. Retainer hours used
Trigger: recurrence, daily. Sum this month's time entries per retainer (from the time-recording export dropped into a
library as CSV), write *hours used*, and if hours used > 80% of included hours, post an adaptive card to the
relationship partner.

## 3. Guest access review
Trigger: recurrence, weekly. List folders in Client Share with guests whose case is **Closed** in Case files.
Send the lead an approval: *Remove guest access?* On approve, remove the role assignments on the folder.

## Notes
- "Send an HTTP request to SharePoint" is a **standard** connector action, so every flow here runs on Microsoft 365
  licences. Power BI needs Pro (or PPU) for anyone viewing the shared dashboard.
- Run the flows under a dedicated service account that's a site owner, not a partner's personal account.
