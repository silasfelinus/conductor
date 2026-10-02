import copy
import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import daily_pitches as dp  # noqa: E402


def make_pitch(slug, llm="none"):
    return {
        "slug": slug, "title": slug.title(), "llm_at_runtime": llm, "effort": "small",
        "hook": "A complete idea that explains what it is and how someone would play with it today.",
        "art_plan": "plan", "first_slice": "slice",
    }


@pytest.fixture
def repo(tmp_path, monkeypatch):
    (tmp_path / "projects" / "existing-project").mkdir(parents=True)
    (tmp_path / "pitches" / "daily").mkdir(parents=True)
    (tmp_path / "pitches" / "2026-01-01-old-pitch.md").write_text("# x\n")
    monkeypatch.setattr(dp, "ROOT", tmp_path)
    monkeypatch.setattr(dp, "DAILY_DIR", tmp_path / "pitches" / "daily")
    monkeypatch.setattr(dp, "DECISIONS_PATH", tmp_path / "pitches" / "daily" / "decisions.yaml")
    return tmp_path


def write(repo, date, pitches):
    (repo / "pitches" / "daily" / f"{date}.yaml").write_text(yaml.safe_dump({"date": date, "pitches": pitches}))


GOOD = [make_pitch(f"idea-{n}") for n in range(5)]


def errors_for(date="2026-10-02"):
    return dp.validate(date, dp.load_docket(date))


def test_valid_docket_passes(repo):
    write(repo, "2026-10-02", GOOD)
    assert dp.cmd_check("2026-10-02") == 0


def test_missing_docket_flags(repo):
    assert dp.cmd_check("2026-10-02") == 1


def test_needs_exactly_five(repo):
    write(repo, "2026-10-02", GOOD[:4])
    assert errors_for()


def test_needs_zero_llm_majority(repo):
    write(repo, "2026-10-02", [make_pitch(f"idea-{n}", llm="required" if n < 3 else "none") for n in range(5)])
    assert any("llm_at_runtime: none" in e for e in errors_for())


def test_slug_collisions_rejected(repo):
    pitches = copy.deepcopy(GOOD)
    pitches[0]["slug"] = "existing-project"
    pitches[1]["slug"] = "old-pitch"
    write(repo, "2026-10-02", pitches)
    assert sum("already exists" in e for e in errors_for()) == 2


def test_earlier_day_slug_rejected(repo):
    write(repo, "2026-10-01", GOOD)
    write(repo, "2026-10-02", GOOD)
    assert any("earlier day" in e for e in errors_for())


def test_short_hook_rejected(repo):
    pitches = copy.deepcopy(GOOD)
    pitches[0]["hook"] = "Too short."
    write(repo, "2026-10-02", pitches)
    assert any("hook" in e for e in errors_for())


def test_decide_and_payload(repo, capsys):
    write(repo, "2026-10-02", GOOD)
    assert dp.cmd_decide("idea-0", "approved", "yes") == 0
    assert dp.cmd_decide("nope", "approved", "") == 2
    assert dp.cmd_decide("idea-1", "maybe", "") == 2
    decisions = {p["slug"]: p["decision"] for p in dp.payload("2026-10-02")["pitches"]}
    assert decisions["idea-0"] == "approved" and decisions["idea-1"] == "pending"
    capsys.readouterr()
    assert dp.cmd_check("2026-10-02") == 0
    assert "4 undecided" in capsys.readouterr().out


def test_approved_pitch_scaffolded_as_project_stays_valid(repo):
    write(repo, "2026-10-02", GOOD)
    dp.cmd_decide("idea-0", "approved", "")
    (repo / "projects" / "idea-0").mkdir()
    assert dp.cmd_check("2026-10-02") == 0
