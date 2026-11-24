# PROBE · Hardening checklist

Checked against Microsoft Learn in November 2026. Salesforce items: confirm with the client's Salesforce admin.

## Identity (the one that matters most)
- [ ] Every Salesforce tool on the agent uses **User authentication**, not *Agent author authentication*.
      With author authentication the tool runs with the maker's connection, so users can get data they can't see themselves.
- [ ] Power Platform admin center → environment → **control maker-provided credentials**: allow end-user credentials only.
      Warning: this switches every tool in the environment to end-user sign-in immediately. Tell users first.
- [ ] Connected agents: their tools also use User authentication. Not sharing a connected agent doesn't protect its data.
- [ ] Agent-level authentication is on (don't turn it off while tools need user credentials).
- [ ] Salesforce connected app (*Microsoft Power Platform*): **Admin approved users are pre-authorized**, assigned
      through a permission set, so only agent users can connect. Agree the refresh token and session policies.
- [ ] No integration user / admin connection anywhere in the agent, its flows or its connection references.

## Salesforce permissions (the agent can't be safer than this)
- [ ] Org-wide defaults for the agent's objects are Private (or the client knows why not).
- [ ] Field-level security hides PHI fields from roles that shouldn't see them.
- [ ] *View All* / *Modify All* / *View All Data* only on the profiles that really need it.

## The agent itself
- [ ] Tools select only the fields the scenario needs (no "all fields").
- [ ] Instructions: never paste raw IDs or bulk lists; refuse raw queries; say "I can't access that" rather than guess.
- [ ] No Salesforce exports uploaded as **knowledge files** (static knowledge ignores Salesforce sharing).
- [ ] Generative answers from the web are off for this agent.
- [ ] Instructions are a convenience, not a control: the controls are identity + Salesforce permissions.

## Data at rest and logging
- [ ] Transcripts: decide with compliance whether to save them to Dataverse at all; if yes, set retention
      (default 30 days in the transcript table; Copilot Studio also keeps session data up to 28 days).
- [ ] Only named people have the **Bot Transcript Viewer** role; turn off maker transcript download if not needed.
- [ ] Sensitive topic variables marked **Sensitive data** so they stay out of transcripts and logs.
- [ ] Microsoft Purview audit: saved search for the agent's Copilot interactions; check `JailbreakDetected` / XPIA flags.
- [ ] Salesforce side: API / login logging (Event Monitoring if licensed) to match "who asked for what".

## Compliance notes
- [ ] Copilot Studio is covered by Microsoft's HIPAA Business Associate Agreement; confirm the client's BAA is in place.
- [ ] Web search queries aren't covered by the BAA, so keep web grounding off.
- [ ] Final statement says *technical assessment*, never "HIPAA compliant".
