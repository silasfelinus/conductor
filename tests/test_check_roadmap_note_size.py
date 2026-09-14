"""Tests for scripts/check_roadmap_note_size.py. No network, no real roadmaps."""

import textwrap

import scripts.check_roadmap_note_size as note_size


def write_roadmap(root, slug, content):
    project_dir = root / "projects" / slug
    project_dir.mkdir(parents=True, exist_ok=True)
    (project_dir / "roadmap.yaml").write_text(textwrap.dedent(content), encoding="utf-8")


def write_overrides(root, entries):
    lines = ["overrides:"]
    for slug, status in entries:
        lines.extend([f"  - slug: {slug}", f"    status: {status}"])
    (root / "project-overrides.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def test_note_size_bytes_handles_string_list_and_none():
    assert note_size.note_size_bytes(None) == 0
    assert note_size.note_size_bytes("abc") == 3
    assert note_size.note_size_bytes(["ab", "cd"]) == len("ab\ncd".encode("utf-8"))
    # non-ASCII should count encoded bytes, not characters
    assert note_size.note_size_bytes("café") == len("café".encode("utf-8")) == 5


def test_oversized_note_is_flagged(tmp_path):
    write_roadmap(
        tmp_path,
        "interface-vision",
        f"""\
        tasks:
          - id: t-104
            title: "Drive live front-end consistency"
            recurring: true
            note: "{"x" * 60_000}"
        """,
    )
    write_overrides(tmp_path, [("interface-vision", "active")])

    result = note_size.scan(
        projects_dir=tmp_path / "projects",
        overrides_path=tmp_path / "project-overrides.yaml",
        threshold_bytes=50_000,
    )

    assert len(result["findings"]) == 1
    finding = result["findings"][0]
    assert finding["project"] == "interface-vision"
    assert finding["task"] == "t-104"
    assert finding["recurring"] is True
    assert finding["note_bytes"] == 60_000


def test_note_under_threshold_is_not_flagged(tmp_path):
    write_roadmap(
        tmp_path,
        "coat-dance",
        """\
        tasks:
          - id: t-003
            title: "Small task"
            note: "short note"
        """,
    )
    write_overrides(tmp_path, [("coat-dance", "active")])

    result = note_size.scan(
        projects_dir=tmp_path / "projects",
        overrides_path=tmp_path / "project-overrides.yaml",
        threshold_bytes=50_000,
    )

    assert result["findings"] == []


def test_findings_sorted_largest_first(tmp_path):
    write_roadmap(
        tmp_path,
        "model-builder",
        f"""\
        tasks:
          - id: t-029
            title: "Bigger"
            note: "{"a" * 70_000}"
          - id: t-031
            title: "Smaller"
            note: "{"b" * 55_000}"
        """,
    )
    write_overrides(tmp_path, [("model-builder", "active")])

    result = note_size.scan(
        projects_dir=tmp_path / "projects",
        overrides_path=tmp_path / "project-overrides.yaml",
        threshold_bytes=50_000,
    )

    assert [f["task"] for f in result["findings"]] == ["t-029", "t-031"]


def test_custom_threshold_is_respected(tmp_path):
    write_roadmap(
        tmp_path,
        "storybook",
        f"""\
        tasks:
          - id: t-010
            title: "Mid-size"
            note: "{"c" * 60_000}"
        """,
    )
    write_overrides(tmp_path, [("storybook", "active")])

    result_default = note_size.scan(
        projects_dir=tmp_path / "projects",
        overrides_path=tmp_path / "project-overrides.yaml",
        threshold_bytes=50_000,
    )
    assert len(result_default["findings"]) == 1

    result_high = note_size.scan(
        projects_dir=tmp_path / "projects",
        overrides_path=tmp_path / "project-overrides.yaml",
        threshold_bytes=100_000,
    )
    assert result_high["findings"] == []


def test_paused_project_excluded_by_default(tmp_path):
    write_roadmap(
        tmp_path,
        "paused-project",
        f"""\
        tasks:
          - id: t-001
            title: "Stale big note"
            note: "{"z" * 60_000}"
        """,
    )
    write_overrides(tmp_path, [("paused-project", "paused")])

    result = note_size.scan(
        projects_dir=tmp_path / "projects",
        overrides_path=tmp_path / "project-overrides.yaml",
        threshold_bytes=50_000,
    )
    assert result["findings"] == []

    result_inactive = note_size.scan(
        projects_dir=tmp_path / "projects",
        overrides_path=tmp_path / "project-overrides.yaml",
        threshold_bytes=50_000,
        include_inactive=True,
    )
    assert len(result_inactive["findings"]) == 1


def test_unparseable_roadmap_is_reported_not_fatal(tmp_path):
    project_dir = tmp_path / "projects" / "broken-project"
    project_dir.mkdir(parents=True, exist_ok=True)
    (project_dir / "roadmap.yaml").write_text("tasks: [unbalanced", encoding="utf-8")
    write_overrides(tmp_path, [("broken-project", "active")])

    result = note_size.scan(
        projects_dir=tmp_path / "projects",
        overrides_path=tmp_path / "project-overrides.yaml",
    )

    assert len(result["findings"]) == 1
    assert result["findings"][0]["note_bytes"] is None
    assert "failed to parse" in result["findings"][0]["detail"]


def test_render_reports_clean_when_no_findings():
    text = note_size.render({"findings": [], "threshold_bytes": 50_000})
    assert "No oversized roadmap note" in text
    assert "50,000" in text


def test_render_names_project_task_and_size_and_archive_pattern():
    text = note_size.render(
        {
            "findings": [
                {
                    "project": "interface-vision",
                    "task": "t-104",
                    "title": "Drive live front-end consistency",
                    "recurring": True,
                    "note_bytes": 395_000,
                    "threshold_bytes": 50_000,
                    "detail": "note: field is 395,000 bytes (over the 50,000-byte threshold)",
                }
            ],
            "threshold_bytes": 50_000,
        }
    )
    assert "interface-vision/t-104" in text
    assert "[recurring]" in text
    assert "395,000 bytes" in text
    assert "T104-HISTORY.md" in text


# --------------------------------------------------------------------------- #
# conductor/t-158: the per-file and whole-payload checks. The per-note threshold
# above never saw the shape that actually refilled the payload three days after
# t-104 was archived -- many medium notes in one file, none individually large.


def test_file_findings_flags_a_large_roadmap_with_no_single_large_note(tmp_path):
    """The t-158 failure mode: 40 x 5KB notes trip nothing per-note, but the file
    is large and the payload is what actually has a ceiling."""
    tasks = "\n".join(
        f"- id: t-{i:03d}\n  status: done\n  title: x\n  note: {'y' * 5000}" for i in range(40)
    )
    write_roadmap(tmp_path, "bulky", f"tasks:\n{tasks}\n")
    write_overrides(tmp_path, [("bulky", "active")])

    notes = note_size.scan(
        projects_dir=tmp_path / "projects",
        overrides_path=tmp_path / "project-overrides.yaml",
        check_payload=False,
    )
    assert notes["findings"] == [], "no single note should exceed the per-note threshold"

    files = note_size.file_findings(
        projects_dir=tmp_path / "projects",
        overrides_path=tmp_path / "project-overrides.yaml",
        file_threshold_bytes=100_000,
    )
    assert [f["project"] for f in files] == ["bulky"]
    assert files[0]["file_bytes"] > 100_000


def test_file_findings_includes_inactive_projects_by_default(tmp_path):
    """roadmap_map() ships every roadmap regardless of project status, so a
    retired project's file counts against the ceiling exactly as much."""
    write_roadmap(tmp_path, "retired-but-big", f"tasks:\n- id: t-001\n  note: {'z' * 60000}\n")
    write_overrides(tmp_path, [("retired-but-big", "retired")])

    files = note_size.file_findings(
        projects_dir=tmp_path / "projects",
        overrides_path=tmp_path / "project-overrides.yaml",
        file_threshold_bytes=10_000,
    )
    assert [f["project"] for f in files] == ["retired-but-big"]


def test_payload_line_reports_headroom_and_warns_past_the_ratio():
    ok = note_size.render_payload_line(
        {
            "measured": True,
            "payload_bytes": 1_600_000,
            "limit_bytes": 4_000_000,
            "headroom_bytes": 2_400_000,
            "ratio": 0.4,
            "over_warn": False,
        }
    )
    assert "1,600,000 / 4,000,000" in ok
    assert "40.0%" in ok
    assert "headroom 2,400,000" in ok

    text = note_size.render(
        {
            "findings": [],
            "threshold_bytes": 50_000,
            "file_findings": [],
            "file_threshold_bytes": 150_000,
            "payload": {
                "measured": True,
                "payload_bytes": 3_900_000,
                "limit_bytes": 4_000_000,
                "headroom_bytes": 100_000,
                "ratio": 0.975,
                "over_warn": True,
            },
        }
    )
    assert "archive_done_task_notes.py" in text
    assert "4,000,134" in text, "the warning should name the time it actually broke"


def test_payload_line_degrades_gracefully_when_unmeasurable():
    assert "not measured" in note_size.render_payload_line({"measured": False})


def test_render_still_works_without_the_t158_keys():
    """render() is called by older callers with only the per-note keys."""
    text = note_size.render({"findings": [], "threshold_bytes": 50_000})
    assert "No oversized roadmap note" in text
