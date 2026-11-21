# STAMP flow: one PDF per Microsoft Forms response (standard connectors only)

Route A below uses only **standard** connectors (Microsoft Forms, OneDrive for Business, SharePoint, Office 365 Outlook),
so it runs on the Power Automate rights included with most Microsoft 365 business and enterprise plans.
Route B (Word template) is at the end. It needs **premium**.

Checked on Microsoft Learn on 21 Nov 2026: Microsoft Forms and OneDrive for Business connectors are Standard tier;
Word Online (Business) is Premium in Power Automate.

## Before you start
- Run the flow as a **service account** (for example `svc-forms@contoso.com`). The temporary HTML file lives in that
  account's OneDrive, and the flow keeps working when a person leaves.
- Create a SharePoint library **Enrolments** with columns `Reference` (text), `Programme` (choice), `Participant` (text), `StartDate` (date).

## Route A: HTML → PDF with OneDrive "Convert file"

| # | Action | Settings |
|---|---|---|
| 1 | **Microsoft Forms – When a new response is submitted** | Form Id: your form. Group forms don't appear in the list: paste the part after `FormId=` from the form URL. |
| 2 | **Microsoft Forms – Get response details** | Form Id: same. Response Id: `Response Id` from step 1 |
| 3 | **Compose** `Reference` | `concat('ENR-', formatDateTime(utcNow(), 'yyyyMMdd'), '-', formatNumber(int(triggerOutputs()?['body/resourceData/responseId']), '0000'))` |
| 4 | **Compose** `Sessions` | `join(json(outputs('Get_response_details')?['body/<sessions-question-id>']), ', ')` (multi-select answers arrive as a JSON array in a string) |
| 5 | **Compose** `HTML` | Paste `templates/enrolment.html`. Replace each `{{Placeholder}}` with the matching answer, wrapped in the encode expression below |
| 6 | **OneDrive for Business – Create file** | Folder: `/STAMP-temp`. File name: `@{outputs('Reference')}.html`. Content: `outputs('HTML')` |
| 7 | **Delay** (optional) | 5–10 seconds. Microsoft's known-issues list suggests a delay between creating and converting if you see "Bad gateway" or "resource could not be found" |
| 8 | **OneDrive for Business – Convert file** | File: `Id` from step 6. Target type: `PDF` |
| 9 | **SharePoint – Create file** | Library: `Enrolments`. Name: `@{outputs('Reference')}.pdf`. Content: `body('Convert_file')` |
| 10 | **SharePoint – Update file properties** | Reference, Programme, Participant, StartDate from the response |
| 11 | **OneDrive for Business – Delete file** | File: `Id` from step 6 (clean up the temp HTML) |
| 12 | **Office 365 Outlook – Send an email (V2)** (optional) | To the enrolment team, attachment: the PDF (`body('Convert_file')`) |

### Encode every answer before it goes into HTML

People type `<`, `>` and `&` into forms. Unencoded, those break the layout (or inject markup). Use:

```
replace(replace(replace(coalesce(<answer>, '–'), '&', '&amp;'), '<', '&lt;'), '>', '&gt;')
```

### Dates

`formatDateTime(<date answer>, 'd MMM yyyy')`. Forms returns dates as `yyyy-MM-dd` text.

### Error handling

Put steps 3–11 in a **Scope** called `Try`. Add a second Scope `Catch` with *Configure run after → has failed / has timed out*,
and inside it send a Teams or email alert with the response id and `result('Try')`. Nobody should find out about a missing PDF from the participant.

## Route B: Word template (premium)

Use this when the client wants a pixel-perfect branded document (logo in the header, tables that repeat, page numbers).

1. In Word desktop, enable the **Developer** tab and add **Plain Text content controls** with unique titles (FullName, Programme…).
2. Save the .docx in SharePoint.
3. Flow: Forms trigger → Get response details → **Word Online (Business) – Populate a Microsoft Word template** →
   SharePoint Create file (.docx) → **Word Online (Business) – Convert Word Document to PDF** → SharePoint Create file (.pdf).

Limits to tell the client (Microsoft Learn, checked 21 Nov 2026): input files up to 10 MB; images in headers and rich text,
date picker and checkbox content controls aren't supported; the populate action can't be used when an MFA conditional-access
policy applies to the connection; conversion must finish in under 2 minutes; files labelled Confidential or Highly Confidential
aren't supported for conversion. The flow owner needs **Power Automate Premium**.

## Which route?

| Need | Route |
|---|---|
| Clean, readable PDF; no extra licence | A (HTML) |
| Exact brand template, logos, repeating tables | B (Word, premium) |
| Hundreds of responses a day | A or B, but watch connector throttling (OneDrive: 100 calls per connection per minute) |
