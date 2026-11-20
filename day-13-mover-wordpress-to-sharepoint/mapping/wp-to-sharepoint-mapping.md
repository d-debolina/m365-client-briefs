# WordPress → SharePoint mapping (MOVER)

| WordPress | SharePoint Online | Notes |
|---|---|---|
| Site | **Hub site** (Intranet home = communication site, set as home site) + associated department sites | One hub, flat structure, no subsites |
| Post (News, Events) | **News post** on the hub (or department site) | Rolls up automatically to the home site + Viva Connections |
| Page | **Site page** on the owning department's site | Use one of 4 page templates |
| Category | **Managed metadata column** `Topic` (term set *Intranet Topics*) | Drives Highlighted content / News web part filters |
| Tags | **Enterprise keywords** (or a second term set if curated) | Keep curated; WordPress tags are usually chaos |
| Author | Page author / Created by + `Content owner` person column | Owner ≠ author: who keeps it up to date |
| Media library | **Site Assets / Documents** library per site | Large PDFs → document library, link from page |
| Shortcodes / custom plugins | Native web parts (Quick links, Events, Forms, Embed) | No SPFx unless truly needed |
| Menus | **Hub navigation** (mega menu) + site navigation | Max 2 levels |
| Permalinks | `redirects.csv` → keep the old WP host up with 301s, or a small Azure Static Web App redirect map | Avoid 2,000 broken bookmarks |
| Comments | Page comments (on) for news; off for policies | |
| Revisions | Not migrated: only the current version | Keep a WP export archive for audit |

## Surfacing without duplication
One page lives in **one** place (the owning site). It appears elsewhere through:
- **News web part** filtered by `Topic` (e.g. Health & Safety news on the Facilities site *and* the home page)
- **Highlighted content** web part filtered by managed property (e.g. `owstaxIdTopic` contains "Policies")
- **Hub navigation** links, never copies.

## Four page templates
1. **Policy page**: title, owner + review date banner, summary, body, "Related policies" (Highlighted content by Topic)
2. **How-to page**: steps, Quick links, "Still stuck?" contact card
3. **Department landing**: hero, news (department filter), quick links, events, contacts
4. **News post**: banner image, body, related news (same Topic)
