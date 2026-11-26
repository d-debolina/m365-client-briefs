import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
import switch_plan as sp

users, drives, links = sp.read("users.csv"), sp.read("shared-drives.csv"), sp.read("external-links.csv")
pilot, wave1, dest, repl = sp.plan(users, drives, links)


def test_pilot_is_one_user_and_not_in_wave1():
    assert len(pilot) == 1
    assert not set(pilot) & set(wave1)
    assert len(pilot) + len(wave1) == len(users)


def test_shared_drives_go_into_a_folder_not_the_library_root():
    for kind, source, target in dest:
        if kind == "shared":
            assert target.endswith("/Shared Documents/" + source)


def test_every_personal_drive_has_a_onedrive_destination():
    personal = [d for d in dest if d[0] == "personal"]
    assert len(personal) == len(users)
    assert all("-my.sharepoint.com/personal/" in d[2] for d in personal)


def test_every_client_link_gets_a_replacement_and_a_negative_test():
    assert len(repl) == len(links)
    assert all("access denied" in r[4] for r in repl)


def test_readiness_has_no_blockers_and_backup_estimate():
    lines, _ = sp.readiness(users, drives)
    assert not any(l.startswith("BLOCK") for l in lines)
    assert any("Microsoft 365 Backup" in l for l in lines)
