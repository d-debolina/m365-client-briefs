# Prompt: draft outreach email (JSON output)

**Inputs:** `Prospect` (one row as JSON), `Offer` (offer sheet as JSON)

**Instructions**
Write a first-touch B2B email from the Sender to the prospect.
1. Max 110 words. Plain text. No emojis, no "I hope this email finds you well".
2. First sentence must reference something specific from Trigger or Notes. If both are empty, reference the Industry pain instead. NEVER invent facts about the company.
3. One proof point (from Offer.Proof), one clear CTA (Offer.CTA).
4. Language: follow Offer.Language rule.
5. Add a one-line opt-out: "If this isn't relevant, just reply 'no thanks' and I won't follow up."
6. If Consent is "Do not contact", return {"skip": true, "reason": "do not contact"}.

**JSON format**
```json
{"skip": false, "subject": "…", "body": "…", "language": "de", "personalisation_used": "Trigger", "risk_flags": []}
```
`risk_flags`: list anything a human must check (e.g. "trigger is vague", "claims a number").
