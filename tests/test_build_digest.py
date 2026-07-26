"""Tests for scripts/build_digest.py's project-overrides filtering.

Silas reported the daily digest email surfacing needs-human tasks and stale
100%-complete milestone summaries from projects already paused/retired/
finished in project-overrides.yaml (mermaids-of-venice, pinball-hero,
career-transition, ecosystem-map, global-ui, davinci, superkate-hairstyle-ai,
among others) -- build_digest.py never read project-overrides.yaml at all.
"""
import json
import textwrap

import scripts.build_digest as build_digest


def write_overrides(tmp_path, yaml_text):
    (tmp_path / "project-overrides.yaml").write_text(textwrap.dedent(yaml_text))


def write_roadmap(tmp_path, slug, status="ready"):
    proj_dir = tmp_path / "projects" / slug
    proj_dir.mkdir(parents=True)
    (proj_dir / "roadmap.yaml").write_text(textwrap.dedent(f"""\
        project: {slug}
        kind: software
        milestones: []
        tasks:
          - id: t-001
            title: Do the thing
            status: {status}
    """))


def test_load_inactive_project_slugs_skips_non_active(tmp_path, monkeypatch):
    write_overrides(tmp_path, """\
        overrides:
          - slug: mermaids-of-venice
            status: paused
          - slug: pinball-hero
            status: retired
          - slug: ecosystem-map
            status: finished
          - slug: kind-robots
            status: active
    """)
    monkeypatch.chdir(tmp_path)

    inactive = build_digest.load_inactive_project_slugs()

    assert inactive == {"mermaids-of-venice", "pinball-hero", "ecosystem-map"}
    assert "kind-robots" not in inactive


def test_load_inactive_project_slugs_missing_override_treated_as_active(tmp_path, monkeypatch):
    write_overrides(tmp_path, """\
        overrides:
          - slug: kind-robots
            status: active
    """)
    monkeypatch.chdir(tmp_path)

    inactive = build_digest.load_inactive_project_slugs()

    # a project not mentioned in overrides at all is never marked inactive
    assert "some-unlisted-project" not in inactive


def test_load_inactive_project_slugs_missing_file_returns_empty_set(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)  # no project-overrides.yaml written at all

    assert build_digest.load_inactive_project_slugs() == set()


def test_main_excludes_paused_and_finished_projects_from_digest(tmp_path, monkeypatch, capsys):
    write_overrides(tmp_path, """\
        overrides:
          - slug: mermaids-of-venice
            status: paused
          - slug: ecosystem-map
            status: finished
          - slug: kind-robots
            status: active
    """)
    write_roadmap(tmp_path, "mermaids-of-venice", status="needs-human")
    write_roadmap(tmp_path, "ecosystem-map", status="done")
    write_roadmap(tmp_path, "kind-robots", status="needs-human")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(build_digest, "git", lambda *a: "")
    monkeypatch.setattr(build_digest, "collect_proposals", lambda: (None, None))
    monkeypatch.setattr(build_digest, "art_highlights", lambda: [])
    monkeypatch.setattr(build_digest, "new_creations", lambda: [])
    monkeypatch.setattr(build_digest, "significant_activity", lambda since: [])
    monkeypatch.setattr(build_digest, "autonomous_work", lambda since: [])
    monkeypatch.setattr(build_digest, "scan_pitches", lambda: [])
    monkeypatch.setattr(build_digest, "scan_branches", lambda: [])
    monkeypatch.setattr("sys.argv", ["build_digest.py"])

    build_digest.main()

    payload = json.loads(capsys.readouterr().out)
    names = [p["name"] for p in payload["projects"]]

    assert names == ["kind-robots"]
    assert payload["all_needs_attention"] == [
        "kind-robots/t-001: Do the thing (needs-human)"
    ]
