# Prompting Copilot in the Power Automate designer (one change at a time)

Copilot in the designer works best with **clear, scoped instructions**: adding an action at a specific point, changing settings,
explaining a flow, simple one-line expressions, adding try/catch scopes. Feed the reviewed spec **step by step**, not all at once:

1. "Add a trigger: when a new email arrives in the shared mailbox invoices@contoso.example, only with attachments."
2. "After the trigger, add Filter array on the attachments to keep only names ending with .pdf."
3. "Add an Apply to each over the filtered array with concurrency 1."
4. "Inside the loop, add Get items from the list Invoice log filtered by InvoiceNumber and Supplier."
5. "Wrap everything after the trigger in a Scope named Try and add a Scope named Catch that runs if Try fails or times out."

After each step: open the action, check the inputs, and **test with the acceptance cases**. Write complex expressions yourself.
