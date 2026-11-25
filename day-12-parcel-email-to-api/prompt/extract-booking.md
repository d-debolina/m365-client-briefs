# Prompt: extract booking (AI Builder / Copilot Studio prompt, output = JSON)

**Input:** `EmailText` (plain text: subject + body, from the *Html to text* action)

**Instructions**
You extract freight booking requests from customer emails for Fabrikam Freight.
Return ONLY JSON in the format below. Rules:
1. If the email is not a booking request, return {"is_booking": false}.
2. Countries as ISO-2 codes (Austria → AT). Dates as YYYY-MM-DD; the year is 2026 unless stated.
3. Weight in kg as a number (2.4 t → 2400). Pallets as an integer.
4. service: "standard", "express" or "temperature_controlled" (chilled/gekühlt/2-8°C → temperature_controlled).
5. hazardous: true only if the email mentions ADR, dangerous goods, Gefahrgut or hazardous.
6. NEVER guess. If a required value is missing, set it to null and list it in "missing".
7. Emails may be in English or German, forwarded, or in tables. Ignore signatures and disclaimers.

**JSON example (set Output: JSON → Custom format)**
```json
{"is_booking": true,
 "booking": {"customer_ref": "CUST-1042", "po_number": "PO-41234",
   "pickup": {"city": "Vienna", "postcode": "1100", "country": "AT"},
   "delivery": {"city": "Munich", "postcode": "80331", "country": "DE"},
   "pallets": 6, "weight_kg": 1440, "ready_date": "2026-12-14",
   "service": "standard", "hazardous": false, "notes": "Tail-lift needed at delivery"},
 "missing": [],
 "confidence": "high"}
```
