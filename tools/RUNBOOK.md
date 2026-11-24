# Daily run: runbook

This runbook is for the scheduled task that runs every morning (Europe/Berlin) for Debolina's
**"Real client brief → build"** Medium series. Every run follows it from top to bottom.

## 0. Setup

1. Attach this repo with push access (`add_repo` owner `d-debolina`, repo `m365-client-briefs`, access `push`).
   Clone it, then run `git config user.name "Debolina Das Gupta"` and
   `git config user.email "maildebolinahere@gmail.com"`.
   Push with `git -c push.negotiate=true push origin main`. Check the push with `git ls-remote origin main`.
2. Find today's date in Europe/Berlin. Work in Berlin dates throughout.
3. Load the Notion and Upwork tools you need with ToolSearch (one call).

## 1. Notion map

| Thing | ID |
|---|---|
| Upwork hub page (has the screenshot rules + series notes) | `41ea884d2f2281719d71ddd84b5acd24` |
| Upwork Job Briefs database | `41ea884d2f2281c591f3d914e16fd234` |
| Data source (use for queries / new rows) | `collection://41ea884d-2f22-81c8-9958-000b2606b984` |
| Daily run log page | `41ea884d2f228121b7ecef23bbc202bf` |
| Model draft to copy the structure from (Day 1, QUOTA) | `41ea884d2f22819a8bf3ec4f80f57070` |

Key properties: `Job title` (title), `Job link`, `Day` (number), `Planned date` (date),
`Blog status` (Idea / Outline ready / Building demo / Drafting / Published), `Blog potential`
(⭐ Flagship / Good post / Quick tip), `App name`, `Blog title`, `Area`, `Tech`, `Fit with my CV`,
`Hiring status`, `Published link`, plus job metadata (`Budget`, `Client`, `Proposals`, `Posted`,
`Experience`, `Duration`, `Job type`). Always fetch the data source schema first and use the exact option names.

## 2. Hard rules (never break)

- **Upwork is read-only.** Never apply, never send proposals or messages, never use Connects,
  never save, boost or edit anything. Use the search and read tools only.
- **Notion:** never delete or trash pages or rows. Only add rows, add content and update properties.
  Never change a row whose `Blog status` is `Published` (apart from reading it).
- **Privacy in public drafts:** never name the client, their country, company, budget or spend.
  Describe them generically ("a growing logistics company"). The client details stay only in the
  private brief part of the page.
- **Employer:** Debolina's employer and past employers are mentioned **only generically**
  ("an international organisation"). Never name IAEA, WCO or internal systems, and never give internal numbers.
- **Data:** all sample data is fictional (Contoso / Fabrikam style). No real people, emails or tenant IDs.
- Never commit secrets. Never touch other repos.
- If a step fails twice, skip it, carry on, and report it in the log.

## 3. Step A: re-plan the publishing schedule (do this first)

Cadence: **two posts a week, on Tuesday and Thursday**. No posts from **24 December to 1 January** inclusive.

Blog status meanings:
- **Drafting** = Claude's AI draft, not yet rewritten by Debolina.
- **Rewriting** = Debolina is rewriting it in her own voice. **Never edit the page content of a Rewriting
  post** (only properties such as Day and Planned date). If its Day number changes, don't rename anything
  inside the page; add a log item asking her to update the "Day N" mentions herself.
- **Published** = live on Medium. Never touch it.

Rewriting-first rule: if the post in either of the next 2 slots is still `Drafting` and a `Rewriting`
post exists further back, move the Rewriting post forward into that slot and add a friendly nudge to the
log ("Day N is due on <date> and is still an AI draft — please start rewriting it").

Draft wording must stay time-neutral: no "this week", "yesterday", "tomorrow", "next week" or weekday
names, so a post still reads correctly after it moves.

1. Query every row that has a `Day`.
2. **Published** rows (`Blog status` = Published) are fixed: never change their Day, date or content.
   If a Published row has no `Published link`, add a "please add the Medium link" item to the log.
3. **Late** rows are unpublished rows whose `Planned date` is before today. Today's post is not late yet,
   because she may publish later in the day.
4. Build the new order for every unpublished row with a Day:
   - Slots are Tuesdays and Thursdays starting from **today** (or the next Tue/Thu if today isn't one),
     skipping the holiday window.
   - Keep the current order by default. Only change it when there's a good reason, and log the reason:
     a) a row is still `Idea` or `Outline ready` (not drafted) and a drafted row is behind it → move the drafted row forward;
     b) two posts with the same main `Area` would run back to back → swap with the next different one;
     c) Flagship and Strong-fit posts go earlier.
   - Day numbers follow the order: the first unpublished post gets (highest published Day + 1), and so on.
5. Apply the changes:
   - Update `Day` and `Planned date` on each row that changed.
   - If a drafted row (status Drafting, never Rewriting) had its Day number changed, also update `Blog title`, the "# ✍️ Medium draft – Day N" heading,
     the public "### Day N:" title, any "Day N" mentions in the draft text and the "What's next" teaser
     (it must name the post that is now next). In the repo, `git mv day-NN-slug day-MM-slug`
     (two-digit numbers), then fix the links in the Notion page and in `README.md`.
     Rename carefully, one folder at a time, so no two folders share a number.
6. Only touch posts whose order actually changed. If nothing changed, say "Schedule unchanged" in the log.

## 4. Step B: scan Upwork for new niche jobs

1. Call `upwork__get_tool_help` once, then `upwork__find_jobs` (search mode). Pause about 6 seconds
   between calls (the rate limit is roughly 12 per minute).
2. Search terms (one search each): `Copilot Studio`, `Microsoft 365 Copilot`, `Power Automate`, `Power Apps`,
   `Dataverse`, `SharePoint Online`, `SharePoint intranet`, `SPFx`, `Microsoft Purview`, `Power Pages`,
   `Microsoft Graph API`, `Azure OpenAI SharePoint`.
3. Keep jobs posted in the **last 3 days** that are in Debolina's niche: Microsoft 365, SharePoint,
   Power Platform, Copilot / Copilot Studio agents, Azure integration, Purview / governance,
   Dataverse / Dynamics. Skip jobs that are:
   - already in the database (match on `Job link` or the job id in the URL),
   - pure data entry, very low budget (under $15/hr or under $100 fixed),
   - off-niche (WordPress-only, generic VA work), or
   - **not a project**: roles, retainers or staffing posts (fractional / part-time architect,
     administrator, "expert on retainer", ongoing consultant) with no concrete deliverable to build.
     This list feeds the blog series; it is not used to apply for jobs.
4. For each job you keep, open it with the get/detail tool and capture as much as possible: full description,
   requirements, skills, budget, job type, duration, experience level, proposals, client info (country,
   verified, spend, rating, reviews), and posted date.
5. Add one row per job, with `Blog status` = `Idea` and no Day yet. Set the tags:
   - `Area` and `Tech` (existing options only),
   - `Fit with my CV`: Strong / Partial / Stretch. Her CV: 14+ years; Azure, M365, SharePoint,
     Power Platform, Copilot Studio agents rollout, AI / digital transformation, solution architecture,
     Azure DevOps, Power BI, ITIL, PRINCE2,
   - `Blog potential`: Flagship / Good post / Quick tip,
   - `Hiring status` = Open, or Someone hired if the job already has a hire (hired jobs are still fine briefs for the blog).

   Page body, in the same section order as the other briefs: **Client request** (in your own words),
   **Requirements (must have)**, **Signals**, **Proposed solution**, **Build steps**, **Blog outline**.
6. **Pick the best 1–2 new jobs** for a full draft (blog potential first, then fit with her CV).
   Give each one a Day at the **end** of the current schedule (next free Tue/Thu slot) and draft it (Step C).
   The rest stay as `Idea` rows, with no Day, for later.

## 5. Step C: write full drafts

Draft these posts:
- (a) the 1–2 jobs picked in Step B, and
- (b) a **safety net**: any post planned in the **next 5 Tue/Thu slots** that is still `Idea` or `Outline ready`.

Cap the run at **3 new drafts** in total. If more are due, log them as "still to draft".

For each draft:

1. **Research first.** Use Microsoft Learn (search, then fetch) to check that every feature, API, limit,
   preview status and licence you mention is current. Use web search for prices. Note the date you checked.
   Things change fast, so don't trust memory, and write down anything in preview.
2. **Fun app name:** an acronym that spells a word (like QUOTA, TRACE, HIRE, MATCH, SPRINKLE, WARDEN, SCOUT).
   Set `App name` to "ACRONYM – Expansion" and `Blog title` to "Day N: <catchy title>".
3. **Repo folder** `day-NN-<acronym-lowercase>-<short-slug>/`:
   - fictional sample data (CSV, JSON, .docx or markdown as needed, made with Python),
   - any small code or scripts the post uses (keep them short and working),
   - a `README.md` that says what's inside and how to use it,
   - `architecture.dot`, `architecture.png` and `architecture.svg`. Draw the diagram by importing and
     reusing the styling helpers in `tools/diagrams.py` (same palette, clusters and colour key).
     Look at the PNG to make sure it's readable.
   - Add a row to the table in the root `README.md`.
   - Commit with the message "Day NN <ACRONYM>: sample data and architecture" and push.
4. **Notion page:** append the draft below the brief, matching the Day 1 model page exactly
   (fetch it once to copy its structure, tone and formatting):
   - `---` then `# ✍️ Medium draft – Day N: ACRONYM`
   - `## 🔒 Private notes (not for Medium)`, containing:
     - **How this post helps you** (career / proposal value, reuse)
     - **Sample data** (repo path + link)
     - **Research notes** (what was checked on Microsoft Learn and the date, preview flags, gotchas)
     - **Licences & costs (private)** (what to re-check before publishing)
     - **Screenshot plan** (numbered shots + GIFs; follow the 8 screenshot rules on the Upwork hub page,
       e.g. blur tenant URLs, emails and GUIDs)
   - `---` then the public post:
     - `### Day N: <title>` and an italic subtitle
     - a warm intro in Debolina's voice (friendly, "Hello everyone", ☕, short sentences, links back to
       earlier Days where it helps)
     - the anonymised brief as a quote
     - "#### What we're building"
     - numbered "#### Step N" sections with **[Screenshot N: …]** placeholders and 💡 tips
     - "#### 🗺️ Architecture": the image `https://raw.githubusercontent.com/d-debolina/m365-client-briefs/main/<folder>/architecture.png`,
       an italic one-paragraph explanation, and a note that the editable diagram is in the repo
     - "#### 💳 Licences & costs": **What you need** (bullets: licence, price, why), a worked
       **Example** for a realistic small team, **Build the demo for $0**, and the italic price
       caveat ("US list prices as of <Month YYYY> … check before you quote"). Use bullets, not tables
       (Medium has no tables), and escape dollar signs as `\$` in Notion.
     - "#### 🏛️ Architect's view" (trade-offs, security, cost, preview warnings)
     - "#### What's next" (tease the next Day's post from the schedule) plus a follow/clap call to action
     - credits line
   - Set `Blog status` = `Drafting`.
5. Wrap code and identifiers in backticks so Notion doesn't auto-link them.
6. Length: about the same as the Day 1–7 drafts. Even Quick-tip jobs get a complete post, just a shorter build.

## 6. Step D: log and notify

1. Prepend (insert at the top of the content, below the intro and divider) a dated entry on the
   **Daily run log** page:

   ```
   ## <Weekday D Month YYYY>
   **Schedule:** <unchanged | what moved and why> · next up: Day N <ACRONYM> on <date>
   **Late / needs you:** <late posts, missing Published links, failures, or "Nothing">
   **New Upwork jobs:** <n> added (<titles, short>) · drafted: <ACRONYMs or none>
   **Drafts written today:** <Day N ACRONYM – link to Notion page> …
   **Repo:** <commit hash(es) or "no changes">
   ```
2. Finish with a 2–3 line plain-text summary as the final message. Mention what's publishing today and
   anything that needs her. This is what the phone notification shows.
