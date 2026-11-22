# Day 28 · STAMP: Submit, Template, Assemble, Make PDF

Every Microsoft Forms enrolment becomes its own PDF in SharePoint, automatically. Standard connectors route (HTML → OneDrive Convert file) plus a premium Word-template route.

| File | What it is |
|---|---|
| `forms/enrolment-form.md` | The 11-question sample form to recreate in Microsoft Forms |
| `templates/enrolment.html` | The HTML template with `{{Placeholders}}` (inline CSS) |
| `flow/flow-steps.md` | Step-by-step flow, expressions, error handling, and the premium Word route |
| `samples/form-responses.csv` | 20 fictional responses |
| `samples/ENR-*.html` | 3 rendered previews: open in a browser to check the layout |
| `scripts/make_samples.py` | Regenerates the responses and previews (HTML-encodes every answer, like the flow) |
| `architecture.png` / `.svg` / `.dot` | Architecture diagram |

## Quick start
1. Create the form from `forms/enrolment-form.md` in a developer tenant.
2. Run `python scripts/make_samples.py` and open a preview to tune the template.
3. Build the flow from `flow/flow-steps.md` (Route A first).

All names and data are fictional.
