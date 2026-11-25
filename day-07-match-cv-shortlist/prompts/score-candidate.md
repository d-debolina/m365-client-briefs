# Prompt: Score one candidate against the vacancy (JSON output)

Inputs: {Job description}, {Candidate record as JSON}

Score the candidate from 0–100 against the MUST-HAVE criteria first, then nice-to-haves.
Return:
```json
{ "score": 0, "meets_all_must_haves": true, "strengths": ["..."], "gaps": ["..."], "one_line_reason": "..." }
```
Rules: do not infer skills that are not listed. Missing information counts as a gap, not a pass.
