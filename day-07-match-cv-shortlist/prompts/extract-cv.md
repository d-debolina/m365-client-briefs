# Prompt: Extract CV (AI Builder / Copilot Studio prompt, JSON output)

Input: {CV document}

Instructions:
Extract the candidate's details from the CV. Use only information written in the CV. If a field is missing, return null.
Return JSON exactly in this shape:

```json
{
  "full_name": "string",
  "current_role": "string",
  "years_experience": 0,
  "location": "string",
  "skills": ["string"],
  "languages": ["string"],
  "education": "string",
  "summary": "one sentence, max 30 words"
}
```
