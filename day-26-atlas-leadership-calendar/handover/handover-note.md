# ATLAS – one-page handover note (template)

## How it works
- All activities live in the SharePoint list **Leadership_Calendar** on the leadership site.
- The **ATLAS** canvas app reads that list and runs as a tab in the *Leadership* Teams channel.
- The main screen shows the whole year: 12 month cards (3 × 4). Click an activity to see its details.
- Filters on the left: category (also the colour legend) and region. **Reset filters** clears both.

## Add a category
1. Open the list → **Category** column → **Edit** → add the new choice. Save.
2. Open the app in Power Apps Studio → **App** → **Formulas** → add one row to `CategoryColours`, for example
   `{Category: "Investor Day", Colour: Color.DarkCyan}`.
3. **Save** → **Publish**. The Teams tab picks up the new version on next load.

## Give someone edit rights
1. Add them to the SharePoint group **ATLAS Editors** (this is what actually allows saving).
2. Add their email (lower case) to the **ATLAS_Editors** list (this shows the *New* / *Edit* buttons in the app).
3. Remove them from both to take rights away.

## Good to know
- Licences: standard Microsoft 365 licences are enough (SharePoint + standard connectors only).
- Volume: built for about 100 activities a year. The app loads one year at a time.
- Out of scope for this version: day-by-day view, Planner/Outlook sync, notifications.
