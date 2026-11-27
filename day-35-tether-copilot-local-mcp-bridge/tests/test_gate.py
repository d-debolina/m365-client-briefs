import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
from tether_gate import Gate

AISHA, BEN, CHLOE, DEV = ("aisha.rahman@contoso.example", "ben.okafor@contoso.example",
                          "chloe.martin@contoso.example", "dev.patel@fabrikam-customer.example")


def test_reader_never_sees_write_tools():
    names = [t["name"] for t in Gate().list_tools(BEN)]
    assert "set_variable" not in names and "run_script" not in names


def test_reads_run_without_confirmation():
    assert Gate().call(AISHA, "search_files", {"workspace": "finance-exports", "query": "x"})["status"] == "allowed"


def test_write_needs_confirmation_then_runs():
    g = Gate(); args = {"workspace": "nightly-jobs", "name": "RETRY_LIMIT", "value": "5"}
    first = g.call(AISHA, "set_variable", args)
    assert first["status"] == "needs_confirmation"
    assert g.call(AISHA, "set_variable", args, confirm=first["confirm_code"])["status"] == "allowed"


def test_code_is_bound_to_user_and_arguments():
    g = Gate(); args = {"workspace": "nightly-jobs", "name": "RETRY_LIMIT", "value": "5"}
    code = g.call(AISHA, "set_variable", args)["confirm_code"]
    assert g.call(AISHA, "set_variable", {**args, "value": "9"}, confirm=code)["status"] == "denied"
    assert g.call(CHLOE, "set_variable", args, confirm=code)["status"] == "denied"


def test_code_expires():
    clock = [1_000_000]
    g = Gate(now=lambda: clock[0]); args = {"workspace": "nightly-jobs", "name": "A", "value": "1"}
    code = g.call(AISHA, "set_variable", args)["confirm_code"]
    clock[0] += 121
    assert g.call(AISHA, "set_variable", args, confirm=code)["status"] == "denied"


def test_customers_are_isolated():
    assert Gate().call(AISHA, "search_files", {"workspace": "orders", "query": "*"})["status"] == "denied"
    assert Gate().call(DEV, "search_files", {"workspace": "orders", "query": "*"})["status"] == "allowed"


def test_paths_and_scripts_are_fenced():
    g = Gate()
    assert g.call(AISHA, "get_file_info", {"workspace": "finance-exports", "path": "..\\..\\Windows\\win.ini"})["status"] == "denied"
    assert g.call(CHLOE, "run_script", {"workspace": "nightly-jobs", "script": "format-disk.ps1"})["status"] == "denied"
