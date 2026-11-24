# ATLAS list schema: `Leadership_Calendar`

One SharePoint list. Low volume (about 50–100 items a year), so one list is plenty.

| Column (internal name) | Type | Required | Notes |
|---|---|---|---|
| `Title` | Single line of text | Yes | Activity title |
| `Category` | Choice (single) | Yes | 15 fixed values, see below. Also drives the colour |
| `StartDate` | Date only | Yes | |
| `EndDate` | Date only | Yes | List validation: `=[EndDate]>=[StartDate]` |
| `AllDay` | Yes/No | – | Default Yes |
| `StartTime` | Single line of text | – | `HH:mm`, only when AllDay = No |
| `EndTime` | Single line of text | – | `HH:mm`, only when AllDay = No |
| `Region` | Choice (single) | Yes | Group, North, South, East, West, Central |
| `Location` | Single line of text | – | |
| `Visibility` | Choice (single) | – | Leadership team, All managers, Everyone |
| `Description` | Multiple lines (plain text) | – | |
| `DocumentLink` | Hyperlink | – | Link to the folder or document |
| `MeetingLink` | Hyperlink | – | Teams meeting link |

**List validation formula** (List settings → Validation settings):

```
=[EndDate]>=[StartDate]
```

Message: `End date can't be before the start date.`

The app checks this too, but the list rule is the safety net for anyone editing the list directly.

## Categories and colours

Each category gets one built-in Power Apps colour. The app reads this mapping from a named formula (see `app/formulas.md`), so adding a category means one new Choice value + one new row in the named formula.

| Category | Colour |
|---|---|
| Leadership Team Meeting | `Color.Navy` |
| Business Review | `Color.Teal` |
| Long-Range Planning | `Color.DarkOliveGreen` |
| Budget Process | `Color.DarkGoldenRod` |
| Board Meeting | `Color.Maroon` |
| Executive Visit | `Color.SteelBlue` |
| Town Hall | `Color.MediumPurple` |
| Strategy Offsite | `Color.SeaGreen` |
| Quarterly Close | `Color.SlateGray` |
| Risk Committee | `Color.Crimson` |
| People Review | `Color.DarkOrange` |
| Customer Summit | `Color.RoyalBlue` |
| Partner Day | `Color.CadetBlue` |
| Audit | `Color.Sienna` |
| Holiday / Blackout | `Color.Silver` |

## Permissions

| Group | Permission on the list | Who |
|---|---|---|
| `ATLAS Viewers` (or the site Visitors group) | Read | Whole leadership team |
| `ATLAS Editors` | Contribute | Executive assistants / planners |

SharePoint enforces this on the server. The app only *hides* the edit buttons for people who can't save anyway (see `app/formulas.md`, "Who can edit?").
