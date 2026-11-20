# PARCEL flow outline (Power Automate cloud flow)

1. **Trigger:** When a new email arrives in a shared mailbox (V2), folder `Bookings`, *Include attachments: No*.
   Trigger condition: `@not(contains(triggerOutputs()?['body/subject'], 'Automatic reply'))`
2. **Html to text** → `EmailText` = subject + plain body
3. **Scope "Try"**
   1. **Run a prompt** → `extract-booking` (JSON output)
   2. **Condition:** `is_booking` is false → move email to `Not bookings`, terminate (Succeeded)
   3. **Condition:** `length(missing) > 0` → add to dead-letter list (reason = missing), Teams alert, terminate
   4. **Parse JSON** with the schema from `api-schema.json` (fails if the shape is wrong → Catch)
   5. **HTTP** POST `https://api.fabrikam-freight.example/v1/bookings`
      - Headers: `Content-Type: application/json`, `Idempotency-Key: @{triggerOutputs()?['body/internetMessageId']}`
      - Auth: API key from an environment variable (secret) / Azure Key Vault
      - **Retry policy:** Exponential, count 4, interval PT20S
   6. **Reply** to sender with the booking number from the API response; move email to `Done`
4. **Scope "Catch"** (run after Try *has failed* or *has timed out*)
   - Filter `result('Try')` for Failed → add row to **PARCEL dead-letter** list (message id, sender, error, flow run URL)
   - Post a Teams adaptive card to the Ops channel with a "Retry" link
5. **Idempotency:** the API (or a Lists lookup) rejects a second POST with the same Idempotency-Key, so retries never double-book.
