# STAMP sample form: "Contoso Wellness – Programme Enrolment"

Create this in Microsoft Forms (work account). All names are fictional.

| # | Question | Type | Required | Notes |
|---|---|---|---|---|
| 1 | Full name | Text | Yes | |
| 2 | Email | Text | Yes | Restriction: email |
| 3 | Phone | Text | No | |
| 4 | Date of birth | Date | Yes | |
| 5 | Programme | Choice (single) | Yes | Foundations · Active Living · Mindful Workplace · Family Plus |
| 6 | Preferred start date | Date | Yes | |
| 7 | Sessions you can attend | Choice (multiple) | Yes | Weekday mornings · Weekday evenings · Weekends · Online only |
| 8 | Emergency contact name | Text | Yes | |
| 9 | Emergency contact phone | Text | Yes | |
| 10 | Anything we should know? | Long text | No | |
| 11 | I agree to the programme terms | Choice (single) | Yes | I agree |

Tip: keep question titles short. They become the dynamic-content names in Power Automate.

Multi-select answers (question 7) arrive in the flow as a JSON-style string such as
`["Weekday mornings","Online only"]`. The flow cleans that up before it goes into the PDF (see `flow/flow-steps.md`).
