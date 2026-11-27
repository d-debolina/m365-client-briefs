import sys, pathlib, threading
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
import reference_numbers as rn
import build_plan


def test_format_and_sequence():
    c = rn.CountersList()
    assert rn.issue_number(c, "Outgoing", "Contoso Institute", "2027") == "OUT-CI-2027-00001"
    assert rn.issue_number(c, "Outgoing", "Contoso Institute", "2027") == "OUT-CI-2027-00002"


def test_series_are_separate_per_entity_direction_and_year():
    c = rn.CountersList()
    rn.issue_number(c, "Outgoing", "Contoso Institute", "2027")
    assert rn.issue_number(c, "Outgoing", "Contoso Services", "2027").endswith("00001")
    assert rn.issue_number(c, "Incoming", "Contoso Institute", "2027").endswith("00001")
    assert rn.issue_number(c, "Outgoing", "Contoso Institute", "2028").endswith("00001")


def test_twenty_people_at_once_get_unique_gapless_numbers():
    c, got = rn.CountersList(), []
    def worker():
        got.append(rn.issue_number(c, "Outgoing", "Contoso Institute", "2027", max_retries=200, jitter=0.002))
    ts = [threading.Thread(target=worker) for _ in range(20)]
    [t.start() for t in ts]; [t.join() for t in ts]
    nums = sorted(int(x[-5:]) for x in got)
    assert nums == list(range(1, 21))


def test_register_has_unique_references():
    reg = rn.build_register()
    refs = [r["reference"] for r in reg]
    assert len(refs) == len(set(refs)) == 30


def test_ai_assistant_comes_last():
    by = build_plan.plan()
    assert max(by) == 5 and [m["module"] for m in by[5]] == ["AI assistant"]
