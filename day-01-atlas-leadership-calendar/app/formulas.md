# ATLAS canvas app: key Power Fx

Standard connectors only (SharePoint + Office 365 Users). No Dataverse, no premium connectors, no PCF.
Screen size 16:9, scale to fit off, so the layout can respond to Teams desktop, tablet and phone.

## 1. App.Formulas (named formulas)

```powerfx
// Category → colour. One row per Choice value in the list.
CategoryColours = Table(
    {Category: "Leadership Team Meeting", Colour: Color.Navy},
    {Category: "Business Review",        Colour: Color.Teal},
    {Category: "Long-Range Planning",    Colour: Color.DarkOliveGreen},
    {Category: "Budget Process",         Colour: Color.DarkGoldenRod},
    {Category: "Board Meeting",          Colour: Color.Maroon},
    {Category: "Executive Visit",        Colour: Color.SteelBlue},
    {Category: "Town Hall",              Colour: Color.MediumPurple},
    {Category: "Strategy Offsite",       Colour: Color.SeaGreen},
    {Category: "Quarterly Close",        Colour: Color.SlateGray},
    {Category: "Risk Committee",         Colour: Color.Crimson},
    {Category: "People Review",          Colour: Color.DarkOrange},
    {Category: "Customer Summit",        Colour: Color.RoyalBlue},
    {Category: "Partner Day",            Colour: Color.CadetBlue},
    {Category: "Audit",                  Colour: Color.Sienna},
    {Category: "Holiday / Blackout",     Colour: Color.Silver}
);

// Who can edit? Looked up in a tiny "ATLAS_Editors" list (one row per editor email).
IsEditor = !IsBlank(LookUp(ATLAS_Editors, Email = Lower(User().Email)));

MaxRowsPerCard = 4;
```

## 2. Main screen OnVisible

```powerfx
Set(varYear, Year(Today()));
ClearCollect(colSelCategories, {Category: ""}); Clear(colSelCategories);   // typed, empty = all categories
Set(varSelRegion, "All");
Select(btnLoadYear)                  // hidden button on the same screen; holds the load logic
```

`btnLoadYear.OnSelect` (a hidden button, also called after year navigation and after saving):

```powerfx
// Delegable: date comparisons are delegated to SharePoint.
ClearCollect(
    colYear,
    Filter(
        Leadership_Calendar,
        StartDate <= Date(varYear, 12, 31) && EndDate >= Date(varYear, 1, 1)
    )
);
Select(btnApplyFilters)
```

With ~100 items a year this stays far below the 500/2,000 data row limit, and every filter after this runs on `colYear` in memory.

## 3. Filtered view

`btnApplyFilters.OnSelect` (hidden button, called after loading and whenever a filter changes):

```powerfx
ClearCollect(
    FilteredYear,
    Filter(
        colYear,
        (IsEmpty(colSelCategories) || Category.Value in colSelCategories.Category) &&
        (varSelRegion = "All" || Region.Value = varSelRegion)
    )
)
```

Category filter = a gallery over `CategoryColours` (it doubles as the colour legend) with a checkbox per row:

- `OnCheck`: `Collect(colSelCategories, {Category: ThisItem.Category}); Select(btnApplyFilters)`
- `OnUncheck`: `RemoveIf(colSelCategories, Category = ThisItem.Category); Select(btnApplyFilters)`

Region filter = a dropdown with `["All","Group","North","South","East","West","Central"]`, `OnChange`: `Set(varSelRegion, Self.Selected.Value); Select(btnApplyFilters)`.

**Reset filters**: `Clear(colSelCategories); Set(varSelRegion, "All"); Reset(galCategoryFilter); Reset(ddRegion); Select(btnApplyFilters)`

## 4. Month grid (3 × 4)

`galMonths` (vertical gallery): `Items = Sequence(12)`, `WrapCount = 3`, `TemplateHeight = (Parent.Height - 24) / 4`.

Inside the template, a label for the month name: `Text(Date(varYear, ThisItem.Value, 1), "mmmm")`

Nested `galActivities.Items`:

```powerfx
With(
    { mStart: Date(varYear, ThisItem.Value, 1),
      mEnd:   DateAdd(Date(varYear, ThisItem.Value + 1, 1), -1, TimeUnit.Days) },
    FirstN(
        SortByColumns(Filter(FilteredYear, StartDate <= mEnd && EndDate >= mStart), "StartDate"),
        MaxRowsPerCard
    )
)
```

An activity that spans two months appears in both months.

Row content:

- Dot (circle): `Fill = LookUp(CategoryColours, Category = ThisItem.Category.Value, Colour)`
- Title: `ThisItem.Title`
- Date label:

```powerfx
If(
    ThisItem.StartDate = ThisItem.EndDate,
    Text(ThisItem.StartDate, "d mmm"),
    Month(ThisItem.StartDate) = Month(ThisItem.EndDate),
    Text(ThisItem.StartDate, "d") & "–" & Text(ThisItem.EndDate, "d mmm"),
    Text(ThisItem.StartDate, "d mmm") & " – " & Text(ThisItem.EndDate, "d mmm")
)
```

"+N more" label below the nested gallery:

```powerfx
// Text
With({ n: CountRows(Filter(FilteredYear,
        StartDate <= DateAdd(Date(varYear, ThisItem.Value + 1, 1), -1, TimeUnit.Days) &&
        EndDate   >= Date(varYear, ThisItem.Value, 1))) - MaxRowsPerCard },
     If(n > 0, "+" & n & " more", ""))
```

Selecting "+N more" sets `varMonthFilter` and opens the details panel as a list for that month.

## 5. Details panel (slides in from the right)

`galActivities.OnSelect`: `Set(varSelected, ThisItem); Set(varShowDetails, true)`

Panel container: `Visible = varShowDetails`, `X = Parent.Width - Self.Width`.

Time line: `If(varSelected.AllDay, "All day", varSelected.StartTime & "–" & varSelected.EndTime)`

Links: `Launch(varSelected.DocumentLink)` and `Launch(varSelected.MeetingLink)`.

Edit button: `Visible = IsEditor`, `OnSelect = EditForm(frmActivity); Set(varShowForm, true)`.

## 6. Create / edit form

Form `frmActivity`, `DataSource = Leadership_Calendar`, `Item = varSelected`.

- Time cards: `Visible = !tglAllDay.Value`
- Save button `DisplayMode`:

```powerfx
If(
    IsBlank(txtTitle.Value) || IsBlank(ddCategory.Selected) || IsBlank(dpStart.SelectedDate) ||
    IsBlank(dpEnd.SelectedDate) || IsBlank(ddRegion.Selected) || dpEnd.SelectedDate < dpStart.SelectedDate,
    DisplayMode.Disabled, DisplayMode.Edit
)
```

- Validation label under the end date: `If(dpEnd.SelectedDate < dpStart.SelectedDate, "End date can't be before the start date.", "")`
- Save: `SubmitForm(frmActivity)`; `OnSuccess`: `Select(btnLoadYear); Set(varShowForm, false); Notify("Saved", NotificationType.Success)`
- `OnFailure`: `Notify(frmActivity.Error, NotificationType.Error)` (shows the SharePoint permission error if a non-editor somehow gets there)

## 7. "New activity" button

`Visible = IsEditor`, `OnSelect = NewForm(frmActivity); Set(varShowForm, true)`

## 8. Year navigation

`‹` : `Set(varYear, varYear - 1); Select(btnLoadYear)` and `›` : `Set(varYear, varYear + 1); Select(btnLoadYear)`
