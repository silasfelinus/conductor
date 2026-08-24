"""Tests for scripts/check_project_scaffold_drift.py. No network, no real roadmaps."""

import scripts.check_project_scaffold_drift as drift


def write_roadmap(root, slug):
    project_dir = root / "projects" / slug
    project_dir.mkdir(parents=True, exist_ok=True)
    (project_dir / "roadmap.yaml").write_text("tasks: []\n", encoding="utf-8")


def write_overrides(root, entries):
    lines = ["overrides:"]
    for slug, status in entries:
        lines.extend([f"  - slug: {slug}", f"    status: {status}"])
    (root / "project-overrides.yaml").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def test_forward_drift_when_conductor_slug_has_no_roadmap(tmp_path):
    write_overrides(tmp_path, [("cthulhuquarium", "active")])
    # No projects/cthulhuquarium/roadmap.yaml written -- the scaffold never landed.
    kr_projects = [
        {"id": 2113, "title": "cthuluquarium", "slug": "cthuluquarium", "conductorSlug": "cthuluquarium"}
    ]

    result = drift.scan(
        kr_projects,
        projects_dir=tmp_path / "projects",
        overrides_path=tmp_path / "project-overrides.yaml",
    )

    assert len(result["forward"]) == 1
    assert result["forward"][0]["conductor_slug"] == "cthuluquarium"
    assert result["forward"][0]["kr_project_id"] == 2113


def test_no_forward_drift_when_roadmap_exists(tmp_path):
    write_roadmap(tmp_path, "cthulhuquarium")
    write_overrides(tmp_path, [("cthulhuquarium", "active")])
    kr_projects = [
        {"id": 2113, "title": "Cthulhuquarium", "slug": "cthulhuquarium", "conductorSlug": "cthulhuquarium"}
    ]

    result = drift.scan(
        kr_projects,
        projects_dir=tmp_path / "projects",
        overrides_path=tmp_path / "project-overrides.yaml",
    )

    assert result["forward"] == []
    assert result["reverse"] == []


def test_reverse_orphan_when_conductor_project_has_no_kr_row(tmp_path):
    write_roadmap(tmp_path, "orphan-project")
    write_overrides(tmp_path, [("orphan-project", "active")])

    result = drift.scan(
        [],
        projects_dir=tmp_path / "projects",
        overrides_path=tmp_path / "project-overrides.yaml",
    )

    assert result["forward"] == []
    assert len(result["reverse"]) == 1
    assert result["reverse"][0]["conductor_slug"] == "orphan-project"


def test_inactive_projects_excluded_by_default(tmp_path):
    # No local roadmap written at all -- would be forward drift if this project
    # were active, but it's marked retired, so the default (inactive-excluded)
    # scan must stay quiet about it.
    write_overrides(tmp_path, [("retired-project", "retired")])
    kr_projects = [
        {"id": 1, "title": "Retired", "slug": "retired-project", "conductorSlug": "retired-project"}
    ]

    result = drift.scan(
        kr_projects,
        projects_dir=tmp_path / "projects",
        overrides_path=tmp_path / "project-overrides.yaml",
    )

    # Neither direction should surface a retired project by default.
    assert result["forward"] == []
    assert result["reverse"] == []


def test_inactive_projects_included_with_flag(tmp_path):
    write_roadmap(tmp_path, "retired-project")
    write_overrides(tmp_path, [("retired-project", "retired")])
    kr_projects = [
        {"id": 1, "title": "Retired", "slug": "retired-project-typo", "conductorSlug": "retired-project-typo"}
    ]

    result = drift.scan(
        kr_projects,
        projects_dir=tmp_path / "projects",
        overrides_path=tmp_path / "project-overrides.yaml",
        include_inactive=True,
    )

    assert len(result["forward"]) == 1
    assert len(result["reverse"]) == 1


def test_blank_conductor_slug_is_ignored(tmp_path):
    write_overrides(tmp_path, [])
    kr_projects = [{"id": 5, "title": "No link yet", "slug": "unlinked", "conductorSlug": None}]

    result = drift.scan(
        kr_projects,
        projects_dir=tmp_path / "projects",
        overrides_path=tmp_path / "project-overrides.yaml",
    )

    assert result["forward"] == []
    assert result["reverse"] == []


def test_render_clean_when_no_findings():
    text = drift.render({"forward": [], "reverse": []})
    assert "No project-scaffold drift found" in text


def test_render_reports_forward_and_reverse():
    text = drift.render(
        {
            "forward": [
                {
                    "conductor_slug": "cthuluquarium",
                    "kr_project_id": 2113,
                    "kr_title": "cthuluquarium",
                    "kr_slug": "cthuluquarium",
                }
            ],
            "reverse": [{"conductor_slug": "orphan-project", "project_status": "active"}],
        }
    )
    assert "FORWARD drift (1)" in text
    assert "cthuluquarium" in text
    assert "REVERSE orphans (1" in text
    assert "orphan-project" in text
