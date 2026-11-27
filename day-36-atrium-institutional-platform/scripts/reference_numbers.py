"""ATRIUM correspondence numbering: OUT-CI-2027-00042 style references with no gaps or duplicates.

In SharePoint, each series (direction + entity + year) is ONE item in a hidden 'Counters' list. The flow that
issues a number reads the item, then updates it with an If-Match ETag. If someone else updated it first the
update fails with 412 and the flow retries. This module simulates exactly that so you can test the logic,
including 20 people pressing 'Issue number' at the same moment.
Run: python scripts/reference_numbers.py  -> writes out/correspondence-register.csv
"""
import csv, pathlib, random, threading, time

ROOT = pathlib.Path(__file__).resolve().parents[1]
PREFIX = {"Outgoing": "OUT", "Incoming": "IN", "Internal memo": "MEMO"}
ENTITY = {"Contoso Institute": "CI", "Contoso Services": "CS"}


class PreconditionFailed(Exception):
    """HTTP 412 from SharePoint: the ETag you sent is stale."""


class CountersList:
    """Stands in for the SharePoint 'Counters' list (one item per series, with an ETag)."""
    def __init__(self):
        self._items, self._lock = {}, threading.Lock()

    def get(self, key):
        with self._lock:
            value, etag = self._items.get(key, (0, 0))
            return value, etag

    def update(self, key, new_value, if_match):
        with self._lock:
            value, etag = self._items.get(key, (0, 0))
            if etag != if_match:
                raise PreconditionFailed(key)
            self._items[key] = (new_value, etag + 1)


def series_key(direction, entity, year):
    return f"{PREFIX[direction]}-{ENTITY[entity]}-{year}"


def issue_number(counters, direction, entity, year, max_retries=20, jitter=0.0):
    key = series_key(direction, entity, year)
    for attempt in range(max_retries):
        value, etag = counters.get(key)
        if jitter:
            time.sleep(random.random() * jitter)        # people are slow; flows are concurrent
        try:
            counters.update(key, value + 1, if_match=etag)
            return f"{key}-{value + 1:05d}"
        except PreconditionFailed:
            time.sleep(0.001 * (attempt + 1))           # back off, then read again
    raise RuntimeError(f"Couldn't get a number for {key} after {max_retries} tries")


def build_register(path=ROOT / "data/correspondence-drafts.csv", out=ROOT / "out/correspondence-register.csv"):
    counters = CountersList()
    with open(path, encoding="utf-8") as f:
        drafts = list(csv.DictReader(f))
    for d in drafts:
        d["reference"] = issue_number(counters, d["direction"], d["entity"], d["date"][:4])
        d["status"] = "Awaiting approval" if d["direction"] != "Incoming" else "Registered"
    out.parent.mkdir(exist_ok=True)
    with open(out, "w", newline="", encoding="utf-8-sig") as f:   # BOM so Excel shows Arabic correctly
        w = csv.DictWriter(f, fieldnames=["reference"] + [k for k in drafts[0] if k != "reference"])
        w.writeheader(); w.writerows(drafts)
    return drafts


if __name__ == "__main__":
    reg = build_register()
    for r in reg[:6]:
        print(r["reference"], "|", r["subject_en"], "|", r["subject_ar"])
    print(f"... {len(reg)} references written to out/correspondence-register.csv")
