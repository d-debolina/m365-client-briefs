# ATLAS – follow the Teams theme (default, dark, high contrast)

Checked on Microsoft Learn, 25 Nov 2026.

- A canvas app added to Teams can read the user's Teams theme with `Param("theme")`. It returns
  `"default"`, `"dark"` or `"contrast"` ("Embed a canvas app as personal app in Teams" → Use context from Teams).
  The value comes in when the tab opens, so after someone switches their Teams theme the tab needs a reload.
- Teams mobile only has light and dark, so the phone layout only needs two token sets.
- Turn on **Settings → Updates → New → Modern controls and themes** and use modern controls (Fluent 2).
  Create a custom modern theme with seed colour `#5B5FC7` so buttons and inputs match Teams.
- Microsoft Learn doesn't describe switching `App.Theme` at runtime, so the modern theme stays the same.
  Dark and high contrast come from the token record below, which you put on screens, containers, labels
  and gallery rows. Check how each modern control you use looks in dark mode before publishing.

## 1. App.Formulas – one token record per theme

```powerfx
ThemeName = Coalesce(Param("theme"), "default");

T = Switch(ThemeName,
    "dark", {
        Bg: ColorValue("#1F1F1F"), Surface: ColorValue("#292929"), Border: ColorValue("#3D3D3D"),
        Text: ColorValue("#FFFFFF"), Muted: ColorValue("#ADADAD"), Link: ColorValue("#9EA2FF"),
        Brand: ColorValue("#5B5FC7"), OnBrand: Color.White, Selected: ColorValue("#3D3E66"),
        InputBorder: ColorValue("#5C5C5C"), Error: ColorValue("#FF8A94")
    },
    "contrast", {
        Bg: Color.Black, Surface: Color.Black, Border: Color.White,
        Text: Color.White, Muted: Color.White, Link: ColorValue("#FFFF00"),
        Brand: ColorValue("#FFFF00"), OnBrand: Color.Black, Selected: Color.Black,
        InputBorder: Color.White, Error: ColorValue("#FFFF00")
    },
    {   // default (light)
        Bg: ColorValue("#F5F5F5"), Surface: Color.White, Border: ColorValue("#E0E0E0"),
        Text: ColorValue("#242424"), Muted: ColorValue("#616161"), Link: ColorValue("#4F52B2"),
        Brand: ColorValue("#5B5FC7"), OnBrand: Color.White, Selected: ColorValue("#EBEBF8"),
        InputBorder: ColorValue("#D1D1D1"), Error: ColorValue("#B10E1C")
    }
);
```

Then use the tokens everywhere instead of fixed colours, for example:

| Control | Property | Formula |
|---|---|---|
| Screen | Fill | `T.Bg` |
| Month card container | Fill / BorderColor | `T.Surface` / `T.Border` |
| Labels | Color | `T.Text` (secondary text: `T.Muted`) |
| Selected activity row | TemplateFill | `If(ThisItem.ID = varSelected.ID, T.Selected, Color.Transparent)` |
| High contrast selection | BorderThickness | `If(ThemeName = "contrast" && ThisItem.ID = varSelected.ID, 2, 0)` |

## 2. Category colours that work on dark

The built-in colours from `../list/schema.md` (Navy, Maroon…) disappear on a dark background. Add a second
column to `CategoryColours` and pick by theme:

```powerfx
CategoryColours = Table(
    {Category: "Leadership Team Meeting", Colour: Color.Navy,           ColourDark: ColorValue("#8A8FFF")},
    {Category: "Business Review",         Colour: Color.Teal,           ColourDark: ColorValue("#2FB3B3")},
    {Category: "Long-Range Planning",     Colour: Color.DarkOliveGreen, ColourDark: ColorValue("#9BB36B")},
    {Category: "Budget Process",          Colour: Color.DarkGoldenRod,  ColourDark: ColorValue("#D9A520")},
    {Category: "Board Meeting",           Colour: Color.Maroon,         ColourDark: ColorValue("#E0607A")},
    {Category: "Executive Visit",         Colour: Color.SteelBlue,      ColourDark: ColorValue("#6FA8DC")},
    {Category: "Town Hall",               Colour: Color.MediumPurple,   ColourDark: ColorValue("#B39DF0")},
    {Category: "Strategy Offsite",        Colour: Color.SeaGreen,       ColourDark: ColorValue("#4FBF85")},
    {Category: "Quarterly Close",         Colour: Color.SlateGray,      ColourDark: ColorValue("#A3B1BF")},
    {Category: "Risk Committee",          Colour: Color.Crimson,        ColourDark: ColorValue("#FF5C7A")},
    {Category: "People Review",           Colour: Color.DarkOrange,     ColourDark: ColorValue("#FF9F40")},
    {Category: "Customer Summit",         Colour: Color.RoyalBlue,      ColourDark: ColorValue("#7F9CFF")},
    {Category: "Partner Day",             Colour: Color.CadetBlue,      ColourDark: ColorValue("#7FC4C7")},
    {Category: "Audit",                   Colour: Color.Sienna,         ColourDark: ColorValue("#D08A5E")},
    {Category: "Holiday / Blackout",      Colour: Color.Silver,         ColourDark: ColorValue("#8C8C8C")}
);

CategoryColour(cat: Text): Color =
    With({r: LookUp(CategoryColours, Category = cat)},
         If(ThemeName = "dark", r.ColourDark, r.Colour));
```

(`CategoryColour` is a user-defined function. If your environment doesn't support them yet, put the `With(...)`
straight into the dot's `Fill`.) In high contrast, give the dot `BorderColor: Color.White`, `BorderThickness: 1`,
and never rely on colour alone: the category name is always shown next to the dot in the details panel and the filter list.

## 3. Test without changing your own Teams theme

Add a hidden admin toggle (or a URL parameter while testing in the browser: `…&theme=dark`) so you can check
all three themes quickly. Microsoft's own Teams sample apps use the same trick.
