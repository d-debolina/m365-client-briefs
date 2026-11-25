import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
from simulate_run import plan, exit_code, NOW
from datetime import timedelta

def row(name, hours_old, sha="A", locked="no", size=1000, sub=False, pc="PC1"):
    path = f"C:\\Fabrikam\\PM\\{'archive\\' if sub else ''}{name}"
    return {"pc": pc, "path": path, "name": name, "size_bytes": str(size),
            "modified": (NOW - timedelta(hours=hours_old)).isoformat(timespec="minutes"), "sha256": sha, "locked": locked}

def actions(rows, state=None):
    return {r["name"]: a.split(" ")[0] for r, a in plan(rows, state or {})}

def test_old_files_ignored():
    assert actions([row("old.csv", 80)]) == {}

def test_subfolders_ignored():
    assert actions([row("sub.csv", 1, sub=True)]) == {}

def test_unchanged_skipped_changed_uploaded():
    rows = [row("same.csv", 5, sha="X"), row("edited.csv", 5, sha="NEW")]
    state = {"PC1|C:\\Fabrikam\\PM\\same.csv": "X", "PC1|C:\\Fabrikam\\PM\\edited.csv": "OLD"}
    assert actions(rows, state) == {"same.csv": "UNCHANGED", "edited.csv": "UPLOAD"}

def test_same_file_name_on_two_pcs_goes_to_two_folders():
    res = plan([row("daysheet.csv", 1, pc="PC1"), row("daysheet.csv", 1, pc="PC2")], {})
    targets = {a.split("-> ")[1] for _, a in res}
    assert targets == {"PM/PC1/daysheet.csv", "PM/PC2/daysheet.csv"}

def test_large_file_uses_upload_session_in_320k_multiples():
    res = plan([row("big.zip", 1, size=14_500_000)], {})
    assert "upload session, 3 chunks" in res[0][1]          # 5 MiB chunks = 16 x 320 KiB

def test_locked_file_gives_exit_code_1():
    res = plan([row("busy.csv", 1, locked="yes"), row("ok.csv", 1)], {})
    assert exit_code(res) == 1
