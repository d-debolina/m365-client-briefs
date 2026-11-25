# Day 26 · CLEAR: Catalogue, Lock down, Establish one version, Approve AI work, Review

A consulting kit for a small professional-services firm that wants its AI use under control
**without anyone building anything**: find the AI tools in use, write a plain-English policy with a
human sign-off rule, get each key process down to one current version, and hand the IT lead a
prioritised list of folders to lock down before Copilot finds them.

| File | What it is |
|---|---|
| `discovery/staff-ai-survey.md` | 7-question anonymous survey (Microsoft Forms) |
| `discovery/ai-tools-register.csv` | Fictional register combining survey answers with admin signals |
| `discovery/copilot-test-prompts.md` | Six "what can you see?" prompts to run before and after each fix |
| `policy/ai-use-policy-template.md` | Two-page AI use policy, incl. the human sign-off rule and a client/insurer statement |
| `processes/process-template.md` | One-version-only process template (owner, status, replaces, AI use, sign-off) |
| `processes/example-client-onboarding.md` | Worked example, incl. how conflicting versions were resolved |
| `data/document-register.csv` | Five processes: copies found, master chosen, what happens to old copies |
| `data/folder-access-review.csv` | Fictional review of 12 folders: sensitivity, current access, target access |
| `data/lockdown-checklist.md` | Generated, prioritised checklist for the IT lead |
| `scripts/build_lockdown_checklist.py` | Scores the review (sensitivity × exposure, +2 if Copilot surfaced it) |
| `architecture.png` / `.svg` / `.dot` | Engagement diagram |

## Quick start
```bash
python scripts/build_lockdown_checklist.py data/folder-access-review.csv > data/lockdown-checklist.md
```
Nothing here connects to Microsoft 365. The firm's IT lead makes every change himself.

All names, firms and data are fictional.
