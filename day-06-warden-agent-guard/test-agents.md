# Three deliberately risky test agents (build in a DEV environment only)
1. **Open Door** – knowledge-only FAQ bot, authentication set to *No authentication* (triggers R01).
2. **Busy Bee** – HR agent with a Dataverse `update_record` tool using *maker-provided credentials* (R03).
3. **Night Shift** – autonomous agent, email trigger, can send emails (R04). Use it to demo the guard blocking an external recipient.
