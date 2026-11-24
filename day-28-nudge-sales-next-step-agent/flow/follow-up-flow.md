# NUDGE – daily follow-up cloud flow

A **Power Automate cloud flow** (standard connectors only), not an agent flow, so it runs on
the Power Automate rights in Microsoft 365 and doesn't use Copilot Credits.

**Trigger:** Recurrence – every day at 08:00, time zone of the sales team, weekdays only
(`Monday–Friday` in the advanced options).

1. **SharePoint – Get items** on *Commitments*
   - Filter query: `FollowUpDate eq '@{formatDateTime(utcNow(),'yyyy-MM-dd')}' and Status eq 'Open'`
   - Top count: 100 (indexed columns, see `lists/schema.md`)
2. **Apply to each** item (Settings → Concurrency control ON, degree 10, so cards wait in parallel)
   1. **SharePoint – Update item**: Status = `Asked` (so a re-run doesn't ask twice)
   2. **Microsoft Teams – Post adaptive card and wait for a response**
      - Post as: **Microsoft Copilot Studio agent** · Post in: **Chat with agent** · Agent: *NUDGE*
      - Recipient: `OwnerEmail`
      - Message: `flow/follow-up-card.json`
      - Update message: "Thanks! NUDGE saved your answer."
      - Advanced → *If the agent is not installed*: **Succeed with status code**
      - Action timeout (Settings): `P5D` – after 5 days without an answer the flow moves on
   3. **Condition** – did the card get an answer?
      - **Yes** → **SharePoint – Update item**: Outcome = `result – notes`; Status = `Done`
        (or `Open` with a new EventDate/FollowUpDate when *Postponed*)
      - **No / status 100** (agent not installed or timed out) → **Outlook – Send an email (V2)** to `OwnerEmail`
        with the same question and a link to the item; Status stays `Asked`
3. Optional: a second **Post message in a chat or channel** (as the agent) with a one-line summary of
   today's open follow-ups for the sales manager.

## Why not an event trigger on the agent?
Copilot Studio agents can have a **Recurrence** event trigger, but event triggers authenticate with the
*maker's* credentials, every payload is billed like a user message, and proactive Teams messages
still need a flow. A plain scheduled cloud flow is cheaper and easier to govern for a daily reminder.
