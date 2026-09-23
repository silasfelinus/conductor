"""Tests for scripts/build_digest.py's project-overrides filtering.

Silas reported the daily digest email surfacing needs-human tasks and stale
100%-complete milestone summaries from projects already paused/retired/
finished in project-overrides.yaml (mermaids-of-venice, pinball-hero,
career-transition, ecosystem-map, global-ui, davinci, superkate-hairstyle-ai,
among others) -- build_digest.py never read project-overrides.yaml at all.
"""
import datetime
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


def test_animation_release_status_uses_latest_shipped_build(tmp_path):
    pitches = tmp_path / "PITCHES.yaml"
    pitches.write_text(textwrap.dedent("""\
        pitches:
          - id: older
            title: Older Effect
            builds:
              - version: 1
                released_at: '2026-09-20T12:00:00Z'
                pull_request: silasfelinus/kind_robots#100
          - id: newest-effect
            title: Newest Effect
            builds:
              - version: 1
                released_at: '2026-09-22T23:00:00Z'
                pull_request: silasfelinus/kind_robots#200
    """))

    now = datetime.datetime(2026, 9, 23, 8, 0, tzinfo=build_digest._TZ)
    status = build_digest.animation_release_status(now=now, pitches_path=str(pitches))

    assert status["state"] == "fresh"
    assert status["id"] == "newest-effect"
    assert status["title"] == "Newest Effect"
    assert status["try_url"].endswith(
        "/build/animation-manager?effect=newest-effect&preview=1"
    )
    assert status["pull_request"] == "silasfelinus/kind_robots#200"


def test_animation_release_status_reports_stale_daily_cadence(tmp_path):
    pitches = tmp_path / "PITCHES.yaml"
    pitches.write_text(textwrap.dedent("""\
        pitches:
          - id: latest
            title: Latest Effect
            builds:
              - version: 1
                released_at: '2026-09-20T12:00:00Z'
    """))

    now = datetime.datetime(2026, 9, 23, 8, 0, tzinfo=build_digest._TZ)
    status = build_digest.animation_release_status(now=now, pitches_path=str(pitches))

    assert status["state"] == "stale"
    assert status["id"] == "latest"
    assert status["age_hours"] > 24


def test_animation_manager_build_ledger_has_release_provenance():
    pitches = build_digest.yaml.safe_load(
        open(build_digest.ANIMATION_PITCHES_PATH, encoding="utf-8")
    )["pitches"]

    missing = []
    for pitch in pitches:
        for build in pitch.get("builds") or []:
            if not build.get("released_at"):
                missing.append(f"{pitch['id']} v{build.get('version', '?')}")

    assert missing == []


def write_animation_pitches(tmp_path, released_at="2026-09-23T15:00:00Z"):
    path = tmp_path / "projects" / "animation-manager" / "PITCHES.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(f"""\
        pitches:
          - id: candlelit-reliquary
            title: Candlelit Reliquary
            status: candidate
            builds:
              - version: 1
                status: candidate
                pull_request: silasfelinus/kind_robots#2962
                released_at: '{released_at}'
    """))
    return path


def test_animation_release_status_reports_fresh_latest_build(tmp_path):
    path = write_animation_pitches(tmp_path)
    now = build_digest.datetime.datetime(
        2026, 9, 23, 11, 0, tzinfo=build_digest._TZ
    )

    release = build_digest.animation_release_status(now=now, pitches_path=str(path))

    assert release["state"] == "fresh"
    assert release["id"] == "candlelit-reliquary"
    assert release["title"] == "Candlelit Reliquary"
    assert release["pull_request"] == "silasfelinus/kind_robots#2962"
    assert release["try_url"].endswith(
        "/build/animation-manager?effect=candlelit-reliquary&preview=1"
    )


def test_animation_release_status_makes_missed_daily_goal_visible(tmp_path):
    path = write_animation_pitches(tmp_path, released_at="2026-09-05T07:55:56Z")
    now = build_digest.datetime.datetime(
        2026, 9, 23, 11, 0, tzinfo=build_digest._TZ
    )

    release = build_digest.animation_release_status(now=now, pitches_path=str(path))

    assert release["state"] == "stale"
    assert release["age_hours"] > 24
    assert "Geode" not in release["title"]
