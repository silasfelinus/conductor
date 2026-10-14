"""Historical approved-pitch intake is idempotent and never publishes releases."""
import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import approved_pitch_recovery as recovery  # noqa: E402
import daily_pitches as pitches  # noqa: E402
import intake  # noqa: E402


@pytest.fixture
def repo(tmp_path, monkeypatch):
    projects = tmp_path / "projects"
    daily = tmp_path / "pitches" / "daily"
    projects.mkdir()
    daily.mkdir(parents=True)
    (tmp_path / "repos.yaml").write_text("repos: []\n")
    (projects / "priority.yaml").write_text("projects:\n  - dream-cycle\n")
    (tmp_path / "project-overrides.yaml").write_text("overrides: []\n")
    (projects / "art-prompts.yaml").write_text("images: []\n")
    (tmp_path / "CONTROL.md").write_text("## Per-project direction\n")

    for module, key, value in [
        (recovery, "ROOT", tmp_path),
        (pitches, "ROOT", tmp_path),
        (pitches, "DAILY_DIR", daily),
        (intake, "REPO_ROOT", tmp_path),
        (intake, "TEMPLATE_DIR", projects / "_template"),
        (intake, "PROJECTS_DIR", projects),
        (intake, "REPOS_FILE", tmp_path / "repos.yaml"),
        (intake, "PRIORITY_FILE", projects / "priority.yaml"),
        (intake, "OVERRIDES_FILE", tmp_path / "project-overrides.yaml"),
        (intake, "ART_PROMPTS_FILE", projects / "art-prompts.yaml"),
        (intake, "CONTROL_FILE", tmp_path / "CONTROL.md"),
    ]:
        monkeypatch.setattr(module, key, value)
    return tmp_path


def pitch(repo, date="2026-10-12", slug="painted-palace", target="new"):
    row = {
        "slug": slug,
        "title": "Painted Palace",
        "hook": "Play a tactile game with a real moving avatar and meaningful stages.",
        "effort": "small",
        "art_plan": "Use existing sprites where licensed.",
        "first_slice": "Implement a moving avatar",
        "llm_at_runtime": "none",
        "target": target,
    }
    if date >= pitches.EXPANSION_START:
        row["expansion_kind"] = "level"
    docket = repo / "pitches" / "daily" / f"{date}.yaml"
    docket.write_text(yaml.safe_dump({"date": date, "pitches": [row]}))
    record = repo / "pitches" / f"{date}-{slug}.md"
    record.write_text(
        pitches.pitch_markdown(date, row).replace(
            "status: awaiting-silas", "status: approved"
        )
    )
    return row


def roadmap(repo, target):
    path = repo / "projects" / target / "roadmap.yaml"
    path.parent.mkdir(parents=True)
    path.write_text(
        f"project: {target}\nkind: software\n"
        "milestones:\n  - id: m1\n    title: Build\n    weight: 100\n"
        "    status: not-started\n"
        "tasks:\n  - id: t-001\n    milestone: m1\n    title: Original\n"
        "    status: done\n    stakes: reversible\n"
    )
    return path


def test_legacy_standalone_scaffold_becomes_real_actionable_tasks(repo):
    pitch(repo)
    rows = recovery.approved_legacy_rows()
    assert len(rows) == 1
    result = recovery.recover_one(rows[0])
    assert result.result == "queued"
    text = (repo / "projects" / "painted-palace" / "roadmap.yaml").read_text()
    data = yaml.safe_load(text)
    assert data["project"] == "painted-palace"
    assert len(data["tasks"]) >= 4
    assert any("/admin/" in task.get("note", "") for task in data["tasks"])
    assert any("phone/tablet/desktop" in task.get("note", "") for task in data["tasks"])
    assert any("human-gated" in task.get("note", "") for task in data["tasks"])
    assert "pitches/2026-10-12-painted-palace.md" in text
    assert recovery.recover_one(rows[0]).result == "already-linked"
    assert len(yaml.safe_load(
        (repo / "projects" / "painted-palace" / "roadmap.yaml").read_text()
    )["tasks"]) == len(data["tasks"])


def test_targeted_non_arcade_creates_one_task_without_new_project(repo):
    path = roadmap(repo, "kind-robots")
    pitch(repo, target="kind-robots")
    row = recovery.approved_legacy_rows()[0]
    assert recovery.recover_one(row).result == "queued"
    data = yaml.safe_load(path.read_text())
    assert len(data["tasks"]) == 2
    assert data["tasks"][-1]["source_pitch"].endswith("-painted-palace.md")
    assert recovery.recover_one(row).result == "already-linked"
    assert not (repo / "projects" / "painted-palace").exists()


def test_arcade_queue_inserts_once_ahead_of_first_catalog_queued(repo):
    path = repo / "projects" / "kr-arcade" / "games.yaml"
    path.parent.mkdir()
    path.write_text(
        "# keep this curator comment\ngames:\n"
        "  - slug: existing\n    status: shipped\n"
        "  - slug: first-queued\n    status: queued\n    source: catalog\n"
    )
    pitch(repo, slug="new-cabinet", target="kr-arcade")
    row = recovery.approved_legacy_rows()[0]
    assert recovery.recover_one(row).result == "queued"
    text = path.read_text()
    assert text.startswith("# keep this curator comment")
    assert text.index("slug: new-cabinet") < text.index("slug: first-queued")
    assert text.count("slug: new-cabinet") == 1
    assert recovery.recover_one(row).result == "already-linked"


def test_post_cutover_pitch_and_unapproved_are_not_recovered(repo):
    pitch(repo, date="2026-10-13", slug="today-expansion")
    assert recovery.approved_legacy_rows() == []
    pitch(repo)
    (repo / "pitches" / "2026-10-12-painted-palace.md").write_text(
        "status: awaiting-silas\n"
    )
    assert recovery.approved_legacy_rows() == []


def test_missing_existing_target_fails_without_auto_fabricating_project(repo):
    pitch(repo, target="missing-project")
    row = recovery.approved_legacy_rows()[0]
    with pytest.raises(ValueError, match="missing target"):
        recovery.recover_one(row)
    assert not (repo / "projects" / "missing-project").exists()


def test_existing_source_linked_first_slice_still_gets_missing_followups(repo):
    pitch(repo, slug="kind-sliding-tile-gallery")
    path = roadmap(repo, "kind-sliding-tile-gallery")
    path.write_text(
        path.read_text() +
        "  - id: t-003\n    milestone: m2\n"
        "    title: Ship one 3x3 daily puzzle\n"
        "    status: ready\n    stakes: reversible\n"
        "    note: Source pitches/2026-10-12-kind-sliding-tile-gallery.md\n"
    )
    row = recovery.approved_legacy_rows()[0]
    assert recovery.recover_one(row).result == "queued"
    tasks = yaml.safe_load(path.read_text())["tasks"]
    assert len(tasks) == 4
    assert any("admin-only interactive preview" in t["title"] for t in tasks)
    assert any("explicit Play promotion" in t["title"] for t in tasks)
    assert sum("playable or usable content slice" in t["title"] for t in tasks) == 0
    assert recovery.recover_one(row).result == "already-linked"
    assert len(yaml.safe_load(path.read_text())["tasks"]) == 4


def test_zero_indent_legacy_task_rows_get_new_unique_ids(repo):
    """Actual October backlog uses tasks: then - id at column zero."""
    pitch(repo, slug="older-game")
    path = roadmap(repo, "older-game")
    old = (
        "project: older-game\n"
        "kind: software\n"
        "milestones:\n"
        "- id: m1\n  title: Shape\n  weight: 30\n  status: not-started\n"
        "- id: m2\n  title: Build\n  weight: 40\n  status: not-started\n"
        "- id: m3\n  title: Polish\n  weight: 30\n  status: not-started\n"
        "tasks:\n"
        + "".join(
            f"- id: t-{number:03d}\n"
            "  milestone: m2\n"
            f"  title: Legacy task {number}\n"
            "  status: ready\n"
            for number in range(1, 9)
        )
        + "goal: preserve the existing tail metadata\n"
    )
    path.write_text(old)
    row = recovery.approved_legacy_rows()[0]
    assert recovery.recover_one(row).result == "queued"
    result = path.read_text()
    parsed = yaml.safe_load(result)
    assert [task["id"] for task in parsed["tasks"]] == [
        *(f"t-{number:03d}" for number in range(1, 9)),
        "t-009",
        "t-010",
        "t-011",
    ]
    assert parsed["goal"] == "preserve the existing tail metadata"
    assert result.count("goal: preserve the existing tail metadata") == 1
    assert recovery.recover_one(row).result == "already-linked"
    assert path.read_text() == result


def test_zero_indent_existing_project_target_preserves_following_section(repo):
    path = roadmap(repo, "kind-robots")
    path.write_text(
        "project: kind-robots\n"
        "milestones:\n- id: m1\n  title: Build\n  weight: 100\n"
        "  status: not-started\n"
        "tasks:\n- id: t-008\n  milestone: m1\n  title: Existing\n"
        "  status: ready\n"
        "summary: keep me unchanged\n"
    )
    pitch(repo, slug="new-feature", target="kind-robots")
    row = recovery.approved_legacy_rows()[0]
    assert recovery.recover_one(row).result == "queued"
    parsed = yaml.safe_load(path.read_text())
    assert parsed["summary"] == "keep me unchanged"
    assert [task["id"] for task in parsed["tasks"]] == ["t-008", "t-009"]
    assert recovery.recover_one(row).result == "already-linked"


def test_writer_never_persists_invalid_task_insertion(repo):
    path = roadmap(repo, "kind-robots")
    original = path.read_text()
    with pytest.raises(ValueError, match="expected number"):
        recovery._append_task_rows(
            original,
            "  - id: t-002\n    title: Not enough\n",
            2,
        )
    assert path.read_text() == original
