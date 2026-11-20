# Custom sensitive information types (fictional Contoso examples)

## 1. Contoso Employee ID
- Pattern: `\bCTS-EMP-\d{5}\b`
- Supporting keywords (within 300 chars): employee, staff no, personnel, Mitarbeiter
- Confidence: High = pattern + keyword · Medium = pattern only
- Test strings: `CTS-EMP-04211` ✅ · `CTS-EMP-4211` ❌ (4 digits) · `ctS-EMP-04211` ❌ (case)

## 2. Project codenames (keyword dictionary)
`ORCHID, KESTREL, BLUEFIN, SALTMARSH, NORTHSTAR` (case-insensitive, whole words)

## 3. Exact Data Match: Customer master
- Schema: `customer_name` (searchable), `account_number` (searchable), `email`, `city`
- Rule: account_number **and** customer_name within 300 characters → High confidence
- Source table: `edm-customer-master-sample.csv` (fictional; in real life the file is hashed by the EDM upload agent and never leaves your network in plain text)
