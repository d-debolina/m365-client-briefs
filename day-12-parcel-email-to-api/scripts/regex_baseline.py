"""Why regex isn't enough: a 'classic' Power Automate-style extraction (split/regex) scored against expected JSON.
Usage: python scripts/regex_baseline.py
"""
import re, json, pathlib
root = pathlib.Path(__file__).resolve().parents[1]
ok = total = 0
for f in sorted((root/"emails").glob("email-*.txt")):
    exp = json.loads((root/"expected"/(f.stem+".json")).read_text())
    if "_expected" in exp: continue
    t = f.read_text(); total += 1
    got = {"customer_ref": (m.group(0) if (m := re.search(r"CUST-\d{4}", t)) else None),
           "pallets": int(m.group(1)) if (m := re.search(r"\|\s*Pallets\s*\|\s*(\d+)", t)) else None,
           "weight_kg": float(m.group(1).replace(",", "")) if (m := re.search(r"Gross weight\s*\|\s*([\d,]+)", t)) else None}
    good = all(got[k] == exp[k] for k in got)
    ok += good
    print(f"{f.name}: {'OK  ' if good else 'FAIL'} {got}")
print(f"\nRegex baseline: {ok}/{total} emails fully correct on just 3 fields. It only works for the table format.")
