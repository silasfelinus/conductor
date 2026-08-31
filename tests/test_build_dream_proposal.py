import copy
from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

import scripts.build_dream_proposal as bdp


def fallback_catalog():
    return {
        key: [bdp._fallback(key)[i] for i in range(len(rows))]
        for key, rows in bdp.FALLBACK_FACETS.items()
    }


def test_target_date_is_pacific_calendar_date():
    instant = datetime(2026, 8, 1, 1, 30, tzinfo=ZoneInfo("UTC"))
    assert bdp._target_date(instant) == "2026-07-31"


def test_facet_seed_plan_is_deterministic_and_connected():
    first = bdp.facet_seed_plan(
        "2026-07-31", catalog=fallback_catalog()
    )
    second = bdp.facet_seed_plan(
        "2026-07-31", catalog=fallback_catalog()
    )
    assert first == second
    assert len(first["umbrella"]["genres"]) == 2
    assert first["umbrella"]["creature"] in first["elements"]["location"]
    assert first["umbrella"]["creature"] in first["elements"]["character"]
    assert first["shared"]["material"] in first["elements"]["location"]
    assert first["shared"]["material"] in first["elements"]["reward_item"]
    assert first["extra_genres"]["scenario"] in first["elements"]["scenario"]
    assert (
        len(
            {
                facet["slug"]
                for facet in first["extra_genres"].values()
            }
        )
        == 5
    )


def test_sample_enforces_exact_six_asset_contract():
    assert bdp.validate_proposal(bdp.SAMPLE_PROPOSAL) == []
    assert len(bdp.SAMPLE_PROPOSAL["locations"]) == 1
    assert len(bdp.SAMPLE_PROPOSAL["characters"]) == 1
    assert len(bdp.SAMPLE_PROPOSAL["rewards"]) == 2
    assert len(bdp.SAMPLE_PROPOSAL["scenarios"]) == 1
    assert sorted(
        row["reward_type"] for row in bdp.SAMPLE_PROPOSAL["rewards"]
    ) == ["ITEM", "SKILL"]
    assert "narrator" not in bdp.SAMPLE_PROPOSAL


def test_normalize_uppercases_reward_types_before_rendering():
    proposal = copy.deepcopy(bdp.SAMPLE_PROPOSAL)
    proposal["rewards"][0]["reward_type"] = "item"
    proposal["rewards"][1]["reward_type"] = "skill"

    normalized = bdp.normalize(proposal)

    assert [
        reward["reward_type"] for reward in normalized["rewards"]
    ] == ["ITEM", "SKILL"]
    assert "## Reward item (1)" in bdp.render_markdown(
        normalized, "2026-07-31"
    )


def test_validator_rejects_detached_scenario_and_wrong_counts():
    proposal = copy.deepcopy(bdp.SAMPLE_PROPOSAL)
    proposal["locations"].append(
        copy.deepcopy(proposal["locations"][0])
    )
    proposal["scenarios"][0][
        "setup"
    ] = "A completely unrelated event occurs elsewhere."
    problems = bdp.validate_proposal(proposal)
    assert "locations must be a list of exactly 1" in problems
    assert any(
        "scenario setup must name the vibe" in problem
        for problem in problems
    )
    assert any(
        "scenario setup must name the location" in problem
        for problem in problems
    )
    assert any(
        "scenario setup must name the character" in problem
        for problem in problems
    )


def test_markdown_prints_seed_facets_and_six_sections():
    rendered = bdp.render_markdown(
        bdp.SAMPLE_PROPOSAL, "2026-07-31"
    )
    assert "## Seed Facets" in rendered
    assert "## Dream vibe (1)" in rendered
    assert "## Dream location (1)" in rendered
    assert "## Character (1)" in rendered
    assert "## Reward item (1)" in rendered
    assert "## Reward skill (1)" in rendered
    assert "## Scenario (1, authored last)" in rendered
    assert '"seed_facets"' in rendered


def test_write_proposal_rechecks_remote_before_writing(
    tmp_path, monkeypatch
):
    monkeypatch.setattr(bdp, "BACKLOG", tmp_path)
    monkeypatch.setattr(bdp, "fetch_main", lambda quiet=True: True)
    monkeypatch.setattr(
        bdp, "remote_proposal_for", lambda date: "already-there.md"
    )
    assert (
        bdp.write_proposal(
            copy.deepcopy(bdp.SAMPLE_PROPOSAL),
            date="2026-07-31",
        )
        is None
    )
    assert list(tmp_path.iterdir()) == []


def test_write_proposal_normalizes_duplicate_slug(tmp_path, monkeypatch):
    monkeypatch.setattr(bdp, "BACKLOG", tmp_path)
    existing = tmp_path / "2026-07-30-prism-appeal.md"
    existing.write_text(
        "---\nslug: prism-appeal\nproposal: true\n"
        "proposal_date: '2026-07-30'\n---\n",
        encoding="utf-8",
    )
    proposal = copy.deepcopy(bdp.SAMPLE_PROPOSAL)
    path = bdp.write_proposal(
        proposal, date="2026-07-31", fetch=False
    )
    assert path is not None
    assert path.name == "2026-07-31-prism-appeal-2.md"


def test_invalid_proposal_raises_before_file_write(
    tmp_path, monkeypatch
):
    monkeypatch.setattr(bdp, "BACKLOG", tmp_path)
    bad = copy.deepcopy(bdp.SAMPLE_PROPOSAL)
    bad["rewards"] = bad["rewards"][:1]
    with pytest.raises(
        ValueError, match="rewards must be a list of exactly 2"
    ):
        bdp.write_proposal(
            bad, date="2026-07-31", fetch=False
        )


def test_check_cli_reports_docket_depth_not_a_calendar_hit(
    tmp_path, monkeypatch, capsys
):
    # Authoring pauses while the buffer is deep, so "no proposal dated today" is
    # expected and must not read as a failure. An empty docket is the real alarm.
    monkeypatch.setattr(bdp, "BACKLOG", tmp_path)

    assert bdp.main(["--check", "--date", "2026-07-31"]) == 1
    assert "docket is EMPTY" in capsys.readouterr().out

    (tmp_path / "2026-07-31-existing.md").write_text(
        "---\nslug: existing\nproposal: true\n"
        "proposal_date: '2026-07-31'\n---\n",
        encoding="utf-8",
    )
    assert bdp.main(["--check", "--date", "2026-07-31"]) == 0
    out = capsys.readouterr().out
    assert "docket holds 1 unbuilt proposal(s) (2026-07-31)" in out
    assert f"Below the {bdp.TARGET_BUFFER_DAYS}-day buffer" in out


def test_check_cli_is_quiet_once_the_buffer_is_full(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(bdp, "BACKLOG", tmp_path)
    for day in range(1, bdp.TARGET_BUFFER_DAYS + 1):
        (tmp_path / f"2026-07-0{day}-entry.md").write_text(
            f"---\nslug: entry{day}\nproposal: true\n"
            f"proposal_date: '2026-07-0{day}'\n---\n",
            encoding="utf-8",
        )

    assert bdp.main(["--check"]) == 0
    out = capsys.readouterr().out
    assert f"docket holds {bdp.TARGET_BUFFER_DAYS} unbuilt proposal(s)" in out
    assert "Below the" not in out


def test_check_cli_fetches_before_reading_the_docket(tmp_path, monkeypatch):
    monkeypatch.setattr(bdp, "BACKLOG", tmp_path)
    calls = []
    monkeypatch.setattr(bdp, "fetch_main", lambda quiet=True: calls.append("fetch") or True)
    (tmp_path / "2026-07-31-existing.md").write_text(
        "---\nslug: existing\nproposal: true\n"
        "proposal_date: '2026-07-31'\n---\n",
        encoding="utf-8",
    )

    assert bdp.main(["--check", "--fetch"]) == 0
    assert calls == ["fetch"]


def test_dry_run_renders_without_writing(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(bdp, "BACKLOG", tmp_path)

    assert (
        bdp.main(
            ["--sample", "--dry-run", "--date", "2026-07-31"]
        )
        == 0
    )
    output = capsys.readouterr()
    assert "## Dream vibe (1)" in output.out
    assert "# would write:" in output.err
    assert list(tmp_path.iterdir()) == []

def _docket_file(backlog, name, *, proposal=True, built=False, day=None):
    day = day or name[:10]
    text = (
        "---\n"
        f"slug: {name[11:-3]}\n"
        "title: Docket Entry\n"
        "type: dream\n"
        "status: outline\n"
        f"proposal: {'true' if proposal else 'false'}\n"
        f"proposal_date: '{day}'\n"
        "---\n\n## Build log\n- proposed\n\n"
        "<!-- proposal-data\n{}\n-->\n"
    )
    if built:
        text += "\n<!-- built-data\n{}\n-->\n"
    (backlog / name).write_text(text, encoding="utf-8")


def test_unbuilt_backlog_is_the_build_docket_oldest_first(tmp_path, monkeypatch):
    backlog = tmp_path / "backlog"
    backlog.mkdir()
    monkeypatch.setattr(bdp, "BACKLOG", backlog)
    _docket_file(backlog, "2026-08-31-newer.md")
    _docket_file(backlog, "2026-08-29-older.md")
    _docket_file(backlog, "2026-08-20-already-built.md", built=True)
    _docket_file(backlog, "2026-07-15-legacy-outline.md", proposal=False)

    assert bdp.unbuilt_backlog() == ["2026-08-29", "2026-08-31"]


def test_unbuilt_backlog_excludes_the_template_and_readme(tmp_path, monkeypatch):
    # _template-proposal.md carries `proposal: true` and a 2026-01-01 placeholder
    # date. Counting it inflates the docket by one and stops authoring a day early.
    backlog = tmp_path / "backlog"
    backlog.mkdir()
    monkeypatch.setattr(bdp, "BACKLOG", backlog)
    _docket_file(backlog, "2026-08-31-real.md")
    _docket_file(backlog, "_template-proposal.md", day="2026-01-01")
    (backlog / "README.md").write_text("---\nproposal: true\n---\n", encoding="utf-8")

    assert bdp.unbuilt_backlog() == ["2026-08-31"]
