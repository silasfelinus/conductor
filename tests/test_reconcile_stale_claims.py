from datetime import datetime, timedelta, timezone

import yaml

from scripts.reconcile_stale_claims import reconcile
from scripts.roadmap_claims import CLAIM_TTL_MINUTES


NOW = datetime(2026, 11, 21, 23, 56, tzinfo=timezone.utc)


def stamp(minutes_ago: int) -> str:
    return (NOW - timedelta(minutes=minutes_ago)).strftime("%Y-%m-%dT%H:%M:%SZ")


def setup_project(tmp_path, slug="kr-arcade", status="active", body=""):
    project_dir = tmp_path / "projects" / slug
    project_dir.mkdir(parents=True)
    path = project_dir / "roadmap.yaml"
    path.write_text("project: " + slug + "\ntasks:\n" + body, encoding="utf-8")
    overrides_path = tmp_path / "project-overrides.yaml"
    existing = yaml.safe_load(overrides_path.read_text()) if overrides_path.exists() else {}
    overrides = existing.get("overrides", [])
    overrides.append({"slug": slug, "status": status})
    overrides_path.write_text(yaml.safe_dump({"overrides": overrides}), encoding="utf-8")
    return path


def test_releases_expired_claim_but_preserves_task_notes_and_history(tmp_path):
    path = setup_project(
        tmp_path,
        body=f"""- id: t-076
  title: Ribbon Riders
  status: claimed
  owner: worker
  claimed_by: old-worker-session
  claimed_at: '{stamp(CLAIM_TTL_MINUTES + 1)}'
  updated: '{stamp(CLAIM_TTL_MINUTES + 1)}'
  note: >-
    Existing specification and implementation notes stay intact.
  passes: 2
""",
    )
    original = path.read_text()
    findings = reconcile(tmp_path, now=NOW)
    assert len(findings) == 1
    assert path.read_text() == original  # default is read-only

    reconcile(tmp_path, apply=True, now=NOW)
    updated = path.read_text()
    task = yaml.safe_load(updated)["tasks"][0]
    assert task["status"] == "ready"
    assert task["passes"] == 2
    assert task["note"] == "Existing specification and implementation notes stay intact."
    assert task["updated"] == "2026-11-21T23:56:00Z"
    assert "owner:" not in updated
    assert "claimed_by:" not in updated
    assert "claimed_at:" not in updated
    assert "Existing specification" in updated
    assert reconcile(tmp_path, apply=True, now=NOW) == []  # idempotent


def test_does_not_release_fresh_or_exact_boundary_claim(tmp_path):
    path = setup_project(
        tmp_path,
        body=f"""- id: t-001
  status: claimed
  claimed_at: '{stamp(1)}'
- id: t-002
  status: claimed
  claimed_at: '{stamp(CLAIM_TTL_MINUTES)}'
""",
    )
    original = path.read_text()
    assert reconcile(tmp_path, apply=True, now=NOW) == []
    assert path.read_text() == original


def test_stale_claim_with_unmet_dependency_returns_to_waiting(tmp_path):
    path = setup_project(
        tmp_path,
        body=f"""- id: t-001
  status: ready
- id: t-002
  status: claimed
  claimed_at: '{stamp(150)}'
  depends_on: t-001
""",
    )
    found = reconcile(tmp_path, apply=True, now=NOW)
    assert found[0]["status"] == "waiting"
    assert found[0]["blockers"] == ["t-001"]
    assert yaml.safe_load(path.read_text())["tasks"][1]["status"] == "waiting"


def test_clears_old_claims_without_timestamps_and_skips_inactive(tmp_path):
    active = setup_project(
        tmp_path,
        slug="kr-arcade",
        status="playtest",
        body="- id: t-001\n  status: claimed\n  owner: worker\n",
    )
    paused = setup_project(
        tmp_path,
        slug="archived-game",
        status="paused",
        body=f"- id: t-001\n  status: claimed\n  claimed_at: '{stamp(200)}'\n",
    )
    untouched = paused.read_text()
    results = reconcile(tmp_path, apply=True, now=NOW)
    assert [item["project"] for item in results] == ["kr-arcade"]
    assert yaml.safe_load(active.read_text())["tasks"][0]["status"] == "ready"
    assert paused.read_text() == untouched
