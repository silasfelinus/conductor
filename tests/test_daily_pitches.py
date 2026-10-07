import copy
import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import build_digest_email_v2_impl as email_v2  # noqa: E402
import daily_pitches as dp  # noqa: E402
import pitch_links  # noqa: E402


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
    return tmp_path


def write(repo, date, pitches):
    (repo / "pitches" / "daily" / f"{date}.yaml").write_text(yaml.safe_dump({"date": date, "pitches": pitches}))


GOOD = [make_pitch(f"idea-{n}") for n in range(5)]


def errors_for(date="2026-10-02"):
    return dp.validate(date, dp.load_docket(date))


def ready(repo, date="2026-10-02", pitches=GOOD):
    write(repo, date, pitches)
    assert dp.cmd_materialize(date) == 0


def test_valid_docket_must_be_materialized(repo):
    write(repo, "2026-10-02", GOOD)
    assert dp.cmd_check("2026-10-02") == 1  # valid, but pitch files not written yet
    assert dp.cmd_materialize("2026-10-02") == 0
    assert dp.cmd_check("2026-10-02") == 0


def test_missing_docket_flags(repo):
    assert dp.cmd_check("2026-10-02") == 1


def test_needs_exactly_five(repo):
    write(repo, "2026-10-02", GOOD[:4])
    assert errors_for()


def test_needs_zero_llm_majority(repo):
    write(repo, "2026-10-02", [make_pitch(f"idea-{n}", llm="required" if n < 3 else "none") for n in range(5)])
    assert any("llm_at_runtime: none" in e for e in errors_for())


def test_slug_collisions_rejected_before_materializing(repo):
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


def test_materialized_pitch_uses_canonical_template_and_never_overwrites(repo):
    ready(repo)
    path = repo / "pitches" / "2026-10-02-idea-0.md"
    text = path.read_text()
    assert text.startswith("# Pitch: Idea-0\ndate: 2026-10-02\nproject-target: new\nstatus: awaiting-silas\n")
    assert "## The idea" in text and "## Rough effort\nsmall" in text
    path.write_text(text.replace("awaiting-silas", "approved"))
    assert dp.materialize("2026-10-02") == []
    assert dp.read_status(path) == "approved"


def test_decide_updates_the_pitch_file_and_payload(repo, capsys):
    ready(repo)
    assert dp.cmd_decide("2026-10-02-idea-0", "approved") == 0
    assert dp.cmd_decide("2026-10-02-idea-1", "rejected") == 0
    assert dp.cmd_decide("nope", "approved") == 2
    assert dp.cmd_decide("2026-10-02-idea-2", "maybe") == 2
    decisions = {p["slug"]: p["decision"] for p in dp.payload("2026-10-02")["pitches"]}
    assert decisions["idea-0"] == "approved" and decisions["idea-1"] == "rejected" and decisions["idea-2"] == "pending"
    capsys.readouterr()
    assert dp.cmd_check("2026-10-02") == 0
    assert "3 undecided today" in capsys.readouterr().out


def test_approved_pitch_that_became_a_project_stays_valid(repo):
    ready(repo)
    dp.cmd_decide("2026-10-02-idea-0", "approved")
    (repo / "projects" / "idea-0").mkdir()
    assert dp.cmd_check("2026-10-02") == 0


def test_approved_list_excludes_projects(repo, capsys):
    ready(repo)
    dp.cmd_decide("2026-10-02-idea-0", "approved")
    dp.cmd_decide("2026-10-02-idea-1", "approved")
    (repo / "projects" / "idea-0").mkdir()
    capsys.readouterr()
    dp.cmd_approved()
    out = capsys.readouterr().out
    assert "idea-1" in out and "idea-0 " not in out.replace("2026-10-02-idea-0", "")


def test_approved_list_shows_approve_with_changes_notes(repo, capsys):
    ready(repo)
    dp.cmd_decide("2026-10-02-idea-1", "approved")
    path = dp.pitch_file("2026-10-02", "idea-1")
    path.write_text(path.read_text() + "\n## Silas's modifications\nMake it smaller\nand free.\n")
    capsys.readouterr()
    dp.cmd_approved()
    assert "APPROVED WITH CHANGES" in capsys.readouterr().out
    assert dp.modifications(path) == "Make it smaller and free."
    assert dp.modifications(dp.pitch_file("2026-10-02", "idea-2")) == ""


def test_payload_carries_over_undecided_from_earlier_days(repo):
    ready(repo, "2026-10-01", [make_pitch(f"old-{n}") for n in range(5)])
    dp.cmd_decide("2026-10-01-old-0", "rejected")
    ready(repo, "2026-10-02")
    payload = dp.payload("2026-10-02")
    assert [p["slug"] for p in payload["pitches"]] == [f"idea-{n}" for n in range(5)]
    assert sorted(p["slug"] for p in payload["carried_over"]) == [f"old-{n}" for n in range(1, 5)]


def test_brief_lists_taken_slugs(repo, capsys):
    ready(repo)
    dp.cmd_brief()
    out = capsys.readouterr().out
    assert "existing-project" in out and "idea-0" in out


def test_email_section_has_signed_buttons_and_hides_them_once_decided(repo, monkeypatch):
    ready(repo)
    dp.cmd_decide("2026-10-02-idea-0", "approved")
    monkeypatch.setenv("PITCH_LINK_SECRET", "s3cret")
    html = email_v2.daily_pitches_section(dp.payload("2026-10-02"))
    assert html.count("Approve</a>") == 4 and html.count("Pass</a>") == 4  # the decided one has no buttons
    assert html.count("Approve with changes</a>") == 4
    # every button opens the single inbox page, preselecting that pitch's choice
    assert "/api/conductor/pitch-inbox?" in html and "pitch-decision" not in html
    assert "pick=2026-10-02-idea-1%3Aapprove&amp;" in html or "pick=2026-10-02-idea-1%3Aapprove\"" in html
    assert "pick=2026-10-02-idea-1%3Aapprove-changes" in html
    assert html.count("Decide all 4 on one page") == 1
    assert "[approved]" in html


def test_email_section_falls_back_to_project_page_without_a_secret(repo, monkeypatch):
    ready(repo)
    monkeypatch.delenv("PITCH_LINK_SECRET", raising=False)
    html = email_v2.daily_pitches_section(dp.payload("2026-10-02"))
    assert "pitch-decision" not in html
    assert html.count("Decide on the project page") == 5
    assert "kindrobots.org/conductor" in html


def test_email_section_empty_without_a_docket():
    assert email_v2.daily_pitches_section(None) == ""
    assert pitch_links  # imported for the shared fixture module path


def test_decide_records_a_pitch_with_no_status_line(repo):
    # 2026-08-11-retire-wonderlab.md had a bold "**Status:**" line, so approving it never stuck.
    (repo / "pitches" / "2026-08-11-hand-written.md").write_text("# Hand written\n**Status:** approved\n\nBody.\n")
    (repo / "pitches" / "2026-08-12-targeted.md").write_text("# T\nproject-target: kind-robots\n\nBody.\n")
    assert dp.cmd_decide("2026-08-11-hand-written", "approved") == 0
    assert dp.cmd_decide("2026-08-12-targeted", "rejected") == 0
    assert dp.read_status(repo / "pitches" / "2026-08-11-hand-written.md") == "approved"
    targeted = (repo / "pitches" / "2026-08-12-targeted.md").read_text()
    assert targeted.startswith("# T\nproject-target: kind-robots\nstatus: rejected\n")


def arcade_repo(repo):
    arcade = repo / "projects" / "kr-arcade"
    arcade.mkdir(parents=True)
    (arcade / "games.yaml").write_text(yaml.safe_dump({"games": [{"slug": "battery-maze", "status": "queued"}]}))
    return arcade


def test_arcade_pitch_targets_the_arcade_and_skips_intake(repo, capsys):
    arcade_repo(repo)
    pitches = copy.deepcopy(GOOD)
    pitches[0]["target"] = "kr-arcade"
    ready(repo, pitches=pitches)
    assert "project-target: kr-arcade" in (repo / "pitches" / "2026-10-02-idea-0.md").read_text()
    dp.cmd_decide("2026-10-02-idea-0", "approved")
    capsys.readouterr()
    dp.cmd_approved()
    out = capsys.readouterr().out
    assert "projects/kr-arcade/games.yaml" in out and "intake.py idea-0" not in out


def test_arcade_pitch_drops_off_approved_once_queued(repo, capsys):
    arcade = arcade_repo(repo)
    pitches = copy.deepcopy(GOOD)
    pitches[0]["target"] = "kr-arcade"
    ready(repo, pitches=pitches)
    dp.cmd_decide("2026-10-02-idea-0", "approved")
    (arcade / "games.yaml").write_text(yaml.safe_dump({"games": [{"slug": "idea-0", "status": "queued"}]}))
    capsys.readouterr()
    dp.cmd_approved()
    assert "idea-0" not in capsys.readouterr().out


def test_unknown_target_and_too_many_targets_rejected(repo):
    arcade_repo(repo)
    pitches = copy.deepcopy(GOOD)
    pitches[0]["target"] = "no-such-project"
    for p in pitches[1:4]:
        p["target"] = "kr-arcade"
    write(repo, "2026-10-02", pitches)
    errs = " ".join(errors_for())
    assert "not an existing project" in errs and "at most 2" in errs


def test_queued_arcade_game_slug_cannot_be_pitched_again(repo):
    arcade_repo(repo)
    pitches = copy.deepcopy(GOOD)
    pitches[0]["slug"] = "battery-maze"
    write(repo, "2026-10-02", pitches)
    assert any("already exists" in e for e in errors_for())


def test_approved_intake_command_carries_the_hook_as_desc(repo, capsys):
    # The hook becomes the project's art subject; a boilerplate --goal did not.
    ready(repo)
    dp.cmd_decide("2026-10-02-idea-1", "approved")
    capsys.readouterr()
    dp.cmd_approved()
    out = capsys.readouterr().out
    assert "--desc 'A complete idea that explains what it is" in out
