# QUOTA Estimate Builder – canvas app build notes

A tablet canvas app (1366 × 768) on the same five Dataverse tables as the model-driven Sales Hub Lite.
Three screens: pick an opportunity → build the lines → review and save. Nothing is written to Dataverse
until the person presses **Save as draft** (the same rule the QUOTA agent follows).

Names below use the display names from `../schema.md`. Let IntelliSense correct table, column and choice names
to whatever your environment shows (for example `'Status (Estimates)'.Draft`).

## Look
- Font: Inter if available in your theme, otherwise Segoe UI. Background `#F3F5F8`, cards `#FFFFFF` with a 1 px `#D8DEE4` border and radius 14.
- Accent `#0F6CBD` (buttons, selected row, active step). Muted text `#57606A`.
- Complexity pills: Low `#E3F4E8` / `#1A6B33`, Medium `#FFF1D6` / `#7A4300`, High `#FBE3E4` / `#9B1C22`.
- Buttons at least 44 px high. Use modern controls where possible.

## App
**App.Formulas** (named formulas, recalculate automatically)
```
fxSubtotal = Sum(colLines, Price * Qty);
fxMultiplier = Coalesce(varRule.Multiplier, 1);
fxTotal = Round(fxSubtotal * fxMultiplier, 0);
```
**App.OnStart**
```
Set(varStage, "All"); Set(varCat, "All"); Set(varSaved, false); Clear(colLines)
```

## Screen 1 – scrOpportunities
| Control | Property | Formula |
|---|---|---|
| `txtSearch` | – | text input, hint "Search account, scope or OPP number" |
| Stage chips (All / Qualify / Propose / Develop) | OnSelect | `Set(varStage, "Qualify")` (one per chip) |
| | Fill | `If(varStage = "Qualify", RGBA(230,240,250,1), Color.White)` |
| `galOpps` (vertical) | Items | `Filter(Opportunities, (varStage = "All" \|\| Text(Stage) = varStage) && (IsBlank(txtSearch.Text) \|\| StartsWith(Account, txtSearch.Text) \|\| StartsWith('Opportunity ID', txtSearch.Text)))` |
| | OnSelect | `Set(varOpp, ThisItem)` |
| | TemplateFill | `If(ThisItem.'Opportunity ID' = varOpp.'Opportunity ID', RGBA(230,240,250,1), Color.White)` |
| Complexity pill | Text / Fill | `Text(ThisItem.Complexity)` / `Switch(Text(ThisItem.Complexity), "Low", ColorValue("#E3F4E8"), "Medium", ColorValue("#FFF1D6"), ColorValue("#FBE3E4"))` |
| Detail card | Visible | `!IsBlank(varOpp)` |
| Pricing rule label | Text | `"× " & Text(LookUp('Pricing rules', Complexity = Text(varOpp.Complexity)).Multiplier, "0.00")` |
| `btnBuild` | OnSelect | `Set(varRule, LookUp('Pricing rules', Complexity = Text(varOpp.Complexity))); Clear(colLines); Set(varSaved, false); Navigate(scrBuilder, ScreenTransition.Cover)` |
| `btnAskQuota` | Visible | `false` until the agent is published, then `Launch()` its Teams / Copilot link |

`StartsWith` is delegable to Dataverse; `in` (contains) may not be, so stick to `StartsWith` for search.

## Screen 2 – scrBuilder
| Control | Property | Formula |
|---|---|---|
| Category chips | OnSelect | `Set(varCat, "Build")` etc. |
| `galPrice` | Items | `Filter('Price list items', varCat = "All" \|\| Text(Category) = varCat)` |
| `btnAdd` (+) | OnSelect | see below |
| `galLines` | Items | `colLines` |
| Qty + | OnSelect | `Patch(colLines, ThisItem, {Qty: ThisItem.Qty + 1})` |
| Qty − | OnSelect | `If(ThisItem.Qty > 1, Patch(colLines, ThisItem, {Qty: ThisItem.Qty - 1}), Remove(colLines, ThisItem))` |
| Remove | OnSelect | `Remove(colLines, ThisItem)` |
| Line total | Text | `Text(ThisItem.Price * ThisItem.Qty, "€#,##0")` |
| Subtotal / Total | Text | `Text(fxSubtotal, "€#,##0")` / `Text(fxTotal, "€#,##0")` |
| Extra hypercare | Text | `"+" & varRule.'Extra hypercare weeks' & " weeks"` |
| `btnReview` | DisplayMode | `If(CountRows(colLines) = 0, DisplayMode.Disabled, DisplayMode.Edit)` |
| | OnSelect | `Navigate(scrReview, ScreenTransition.Cover)` |

`btnAdd.OnSelect`
```
With({existing: LookUp(colLines, Code = ThisItem.'Product code')},
  If(IsBlank(existing),
    Collect(colLines, {Code: ThisItem.'Product code', Item: ThisItem, Name: ThisItem.Name,
                       Unit: ThisItem.Unit, Price: ThisItem.'Unit price', Qty: 1}),
    Patch(colLines, existing, {Qty: existing.Qty + 1})))
```

## Screen 3 – scrReview
| Control | Property | Formula |
|---|---|---|
| Lines list | Items | `colLines` |
| Confirm card / Saved card | Visible | `!varSaved` / `varSaved` |
| `btnSave` | OnSelect | see below |
| `btnBack` | OnSelect | `Navigate(scrBuilder)` |
| Saved card button | OnSelect | `Set(varOpp, Blank()); Clear(colLines); Navigate(scrOpportunities)` |

`btnSave.OnSelect`
```
IfError(
  Set(varEst, Patch(Estimates, Defaults(Estimates), {
      Opportunity: varOpp, Status: 'Status (Estimates)'.Draft,
      Subtotal: fxSubtotal, Multiplier: fxMultiplier }));
  ForAll(colLines As L,
      Patch('Estimate lines', Defaults('Estimate lines'), {
          'Line name': L.Name, Estimate: varEst, 'Price list item': L.Item,
          Quantity: L.Qty, 'Line total': L.Price * L.Qty }));
  Set(varSaved, true);
  Notify("Saved " & varEst.'Estimate number', NotificationType.Success),
  Notify("Couldn't save: " & FirstError.Message, NotificationType.Error))
```

## Security
The app uses each person's own Dataverse permissions, so the **Sales rep** role (create and read own
estimates) and **Sales manager** role (read all) from `../schema.md` apply here too. Share the app with a
security group and check that a rep only sees their own estimates.

## Licensing
Canvas apps on Dataverse need **Power Apps Premium** for each user (the same as the model-driven app).
Building it in a trial or developer environment costs nothing.
