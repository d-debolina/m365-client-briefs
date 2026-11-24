# CREW · Dataverse schema (core tables)

The real brief has about 25 tables. These 11 carry the demo; the rest (rates, certifications, site diaries…)
follow the same patterns. Prefix `crew_`, solution **CREW**, publisher prefix `crew`.

| Table | Ownership | Key columns | Notes |
|---|---|---|---|
| `crew_project` | User/Team | name, businessunit, startweek, endweek, **planlocked** (Yes/No), **unlockeduntil** (date/time) | Owned by the yard's Entra group team |
| `crew_task` | User/Team | projectid, title, **startdate**, **durationworkdays**, enddate (set by plug-in), assignedcrew | Look-ahead tasks. Guarded by `LockGuard` |
| `crew_crewmember` | Organization | name, skilllevel (choice: Foreman/Journeyman/Apprentice), hoursperweek, businessunit | Org-owned reference data |
| `crew_assignment` | User/Team | crewmemberid, projectid, weekstart, hours | What the Resource Board drags around |
| `crew_demand` | User/Team | projectid, weekstart, kind (Skill/Equipment), skilllevel or equipmenttype, hours/units, **scenarioid** | Empty scenario = the live plan |
| `crew_scenario` | User | name, basedon, createdby | What-if copies of demand |
| `crew_leave` | User/Team | crewmemberid, weekstart, hoursoff | Reduces supply |
| `crew_equipmenttype` | Organization | name, ownedunits, rentalperweek | Anything above owned units = rental |
| `crew_weeklycapacity` | Organization | weekstart, skilllevel, scenarioid, demand, supply, gap | Written by the planning engine; alternate key (weekstart, skilllevel, scenarioid) |
| `crew_holiday` | Organization | date, name | Used by `WorkdayMath` |
| `crew_importstaging` | User | source (Excel/SharePoint), payload (JSON), status, errors | Row validation before rows reach real tables |

## Security model
- Two business units (**North yard**, **South yard**). Each has an **Entra group team** linked to a Microsoft 365
  security group (`SG-CREW-North-Planners`, `SG-CREW-South-Planners`) with the *CREW Planner* role at
  business-unit depth. Join the group in Entra, get access in Dataverse. No per-user role assignments.
- *CREW Viewer* role (read at organisation depth) for site managers who only look at the boards.
- **Access team template** on `crew_project` (*Project collaborators*: read + write) for the odd foreman from the other yard.
- Field security profile on `crew_crewmember.hourlyrate` (if you add it): only payroll sees it.
- Plug-ins enforce the lock for everyone, including people with write access. Security roles decide *who* may
  write; plug-ins decide *when* a write is allowed.
