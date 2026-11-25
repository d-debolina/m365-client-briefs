# NUDGE – SharePoint lists (the "CRM-lite")

One SharePoint site, three lists. Create them with `scripts/create-lists.ps1` or by hand.
Every column is a simple type, so the Copilot Studio SharePoint connector tools and the
cloud flow can read and write them without extra work.

## Accounts
| Column | Type | Notes |
|---|---|---|
| Title | Single line | Account name (e.g. *Contoso General Hospital*) |
| AccountId | Single line, indexed | `ACC-001` |
| OwnerEmail | Single line | Rep who owns the account (used for item-level filtering in tools) |
| Stage | Choice | Prospect · Evaluation · First cases · Adopted · At risk |
| FocusProduct | Single line | |
| KeySurgeon | Single line | Fictional names only in the demo |
| LastContact | Date | Updated by the agent after each logged activity |

## Commitments  ← the heart of NUDGE
| Column | Type | Notes |
|---|---|---|
| Title | Single line | Short description |
| CommitmentId | Single line, indexed | `CMT-0001` |
| AccountId | Single line, indexed | |
| AccountName | Single line | Copied in so the card can show it without a second lookup |
| OwnerEmail | Single line, indexed | Who gets the follow-up |
| Type (internal name `CommitmentType`) | Choice | Proctorship · In-service training · Product evaluation · Value analysis meeting · Sample delivery · Follow-up call |
| EventDate | Date | When the thing happens |
| FollowUpDate | Date, indexed | When NUDGE asks how it went (default: EventDate + 1 working day) |
| FollowUpQuestion | Multiple lines (plain) | The question the card shows |
| Status | Choice | Open · Asked · Done · Cancelled |
| Outcome | Multiple lines (plain) | Filled from the rep's card answer |
| NextStep | Multiple lines (plain) | Suggested by the agent, confirmed by the rep |

## Activities
| Column | Type | Notes |
|---|---|---|
| Title | Single line | Summary |
| AccountId | Single line, indexed | |
| Kind | Choice | Call · Visit · Email · Case support · Lunch & learn |
| ActivityDate | Date | |
| OwnerEmail | Single line | |

> Index `FollowUpDate`, `Status` and `OwnerEmail` on Commitments. The daily flow filters on them,
> and lists over 5,000 items need indexed columns for filtered queries.
