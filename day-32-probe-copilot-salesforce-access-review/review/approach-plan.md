# PROBE · Approach plan (send this before you touch anything)

A one-page plan the client signs off before the review starts. Fictional example; adapt the names.

## Goal
Prove that the Copilot Studio agent (used through Microsoft 365 Copilot) returns only the Salesforce records and
fields each signed-in user is allowed to see, find where regulated data could leak outside those controls,
fix the gaps, and leave evidence.

## Scope
- In: the agent, its tools and knowledge, the Salesforce connection(s), the Salesforce connected app policies,
  the Power Platform environment settings, transcripts, audit logging.
- Out: a rebuild, Salesforce data model changes, legal sign-off on HIPAA (the summary is technical, not legal).

## Week 1 (read-only)
1. **Inventory:** list every tool, connector, flow and knowledge source on the agent. For each tool, record the
   authentication setting (*User authentication* or *Agent author authentication*) and which identity the
   connection uses.
2. **Salesforce side:** export profiles, permission sets, role hierarchy, org-wide defaults and sharing rules for
   the objects the agent touches; check the connected app OAuth policies (permitted users, refresh token policy).
3. **Environment side:** data policies (connector rules), *maker-provided credentials* setting, transcript
   settings and retention, who has the Bot Transcript Viewer role, Purview audit enabled.
4. **Test users:** agree 6–9 Salesforce test users across roles (rep, manager, compliance, one with no access)
   in a **sandbox org** with fictional or masked data.

## Week 2 (test, fix, retest)
5. Run the test matrix (`tests/test_matrix.csv`) for every test user. Record what came back.
6. Score the results with `scripts/check_results.py`; any LEAK is a finding.
7. Fix in this order: identity (user auth on every tool), Salesforce permissions, agent instructions and
   tool descriptions, transcript/logging settings.
8. Rerun the full matrix. Write the findings report and the final summary.

## What I need from you in week 1
- Copilot Studio environment maker access to the agent's environment (read-only is fine to start).
- A Salesforce admin for two short sessions, and a sandbox with test users.
- The Power Platform admin to change environment settings when we agree a fix.
- A named person who approves changes in production.
