"""Validate extracted JSON against api-schema.json, the same check the flow does before calling the API.
Usage: pip install jsonschema && python scripts/validate_and_post.py expected/
"""
import json, sys, pathlib
from jsonschema import Draft202012Validator, FormatChecker
root = pathlib.Path(__file__).resolve().parents[1]
v = Draft202012Validator(json.loads((root/"api-schema.json").read_text()), format_checker=FormatChecker())
folder = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else root/"expected")
for f in sorted(folder.glob("*.json")):
    data = json.loads(f.read_text())
    if "_expected" in data:
        print(f"{f.name}: → dead-letter list ({data['_expected']})"); continue
    errs = sorted(v.iter_errors(data), key=lambda e: e.path)
    print(f"{f.name}: " + ("valid → POST /bookings" if not errs else "INVALID → dead-letter: " + "; ".join(e.message for e in errs)))
