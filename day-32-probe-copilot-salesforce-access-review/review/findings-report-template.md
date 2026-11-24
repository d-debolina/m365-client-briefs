# PROBE · Findings report (template)

**Agent:** <name> · **Environment:** <dev/test/prod> · **Salesforce org:** <sandbox> · **Review dates:** <from–to>

## Severity scale
| Severity | Meaning | Example |
|---|---|---|
| Critical | A user can read regulated data they're not allowed to see | Tool uses the agent author's (admin) connection |
| High | Regulated data is stored or shown outside the agreed controls | Restricted field in the answer; transcripts kept longer than agreed |
| Medium | A control exists but can be bypassed or isn't monitored | No audit search saved; maker credentials still allowed in the environment |
| Low | Hygiene | Tool descriptions too broad; no test users documented |

## Findings
| ID | Severity | Finding | Evidence (test ID) | Fix | Status |
|---|---|---|---|---|---|
| F-01 | Critical | `Get referrals` tool runs with *Agent author authentication* (integration user) | T-07: rep received East referrals | Switch tool to *User authentication*; turn off maker-provided credentials for the environment | Fixed, retested |
| F-02 | High | Diagnosis notes field readable by sales reps through the agent | T-10 | Remove FLS on the field from the Sales Rep profile/permission set; drop the field from the tool's select list | Fixed, retested |
| F-03 | Medium | Transcripts saved to Dataverse with default retention; 4 makers can download them | T-16 | Agree retention with compliance; bulk-delete job; restrict Bot Transcript Viewer role | Open – decision needed |

## What is now enforced
- Every request to Salesforce runs as the signed-in user (OAuth per user, no shared connection).
- Salesforce object, field and record-level security applies to every tool call (verified with 9 users × 20 tests).

## Still open / recommended next steps
- <e.g. Salesforce Event Monitoring for API events; DLP for Copilot; quarterly retest after agent changes>

*This is a technical assessment, not a legal or compliance certification.*
