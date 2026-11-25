# Day 20 · PITCH: Personalised, Inspected, Tailored, Checked, Human-sent

AI-drafted B2B outreach from an Excel list: Power Automate + a prompt with JSON output, drafts in Outlook, a human sends.

| File | What it is |
|---|---|
| `data/prospects.xlsx` | 30 fictional prospects (table `Prospects`) + `Offer` sheet |
| `prompt/draft-outreach.md` | Prompt with rules, opt-out, DNC handling and JSON format |
| `flow/flow-outline.md` | Flow design: list rows → prompt → Outlook draft → update row → Teams summary |
| `eval/review-checklist.csv` | What a human checks before sending |
