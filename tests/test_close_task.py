"""
Integration tests for close_task.py against real (throwaway, local-only) git repos --
no network access, no real origin. Exercises the actual git plumbing (scratch-index
commit + push to a fresh branch), not just the pure YAML-editing logic, since that's
the part most likely to silently break (see conductor/t-040, t-091).
"""

import subprocess
from pathlib import Path

import pytest
import yaml

import scripts.close_task as ct


def run(cmd: list[str], cwd: Path) -> str:
    result = subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)
    return result.stdout


def make_remote_and_clone(tmp_path: Path, roadmap_text: str) -> Path:
    """Sets up bare + clone repos with one project's roadmap.yaml, and returns the
    clone's path with origin/main already pushed."""
    bare = tmp_path / "bare"
    clone = tmp_path / "clone"
    bare.mkdir()
    clone.mkdir()

    run(["git", "init", "-q", "--bare"], cwd=bare)
    run(["git", "init", "-q"], cwd=clone)
    run(["git", "config", "user.email", "test@example.com"], cwd=clone)
    run(["git", "config", "user.name", "Test"], cwd=clone)

    roadmap_path = clone / "projects" / "demo" / "roadmap.yaml"
    roadmap_path.parent.mkdir(parents=True)
    roadmap_path.write_text(roadmap_text, encoding="utf-8")

    run(["git", "add", "-A"], cwd=clone)
    run(["git", "commit", "-q", "-m", "init"], cwd=clone)
    run(["git", "remote", "add", "origin", str(bare)], cwd=clone)
    run(["git", "push", "-q", "origin", "HEAD:refs/heads/main"], cwd=clone)
    return clone


REVIEW_ROADMAP = """\
project: demo
kind: software
tasks:
- id: t-001
  title: Demo task
  status: review
  owner: worker
  claimed_by: session-a
  claimed_at: '2026-07-28T20:00:00Z'
"""

DONE_ROADMAP = """\
project: demo
kind: software
tasks:
- id: t-001
  title: Demo task
  status: done
  owner: worker
"""


@pytest.fixture
def demo_repo(tmp_path, monkeypatch):
    clone = make_remote_and_clone(tmp_path, REVIEW_ROADMAP)
    monkeypatch.setattr(ct, "ROOT", clone)
    monkeypatch.setattr(ct, "PROJECTS_DIR", clone / "projects")
    return clone


def test_close_pushes_status_to_a_new_branch_not_main(demo_repo):
    ct.close("demo", "t-001", "done", "session-b", "close/demo-t-001-session-b", {}, dry_run=False)

    run(["git", "fetch", "-q", "origin"], cwd=demo_repo)

    # main is untouched -- the whole point is no direct push to main.
    main_doc = yaml.safe_load(
        run(["git", "show", "origin/main:projects/demo/roadmap.yaml"], cwd=demo_repo)
    )
    assert main_doc["tasks"][0]["status"] == "review"

    branch_doc = yaml.safe_load(
        run(
            ["git", "show", "origin/close/demo-t-001-session-b:projects/demo/roadmap.yaml"],
            cwd=demo_repo,
        )
    )
    task = branch_doc["tasks"][0]
    assert task["status"] == "done"
    assert task["updated"]


def test_close_does_not_touch_callers_branch_or_worktree(demo_repo):
    before_branch = run(["git", "branch", "--show-current"], cwd=demo_repo)

    ct.close("demo", "t-001", "done", "session-b", None, {}, dry_run=False)

    after_branch = run(["git", "branch", "--show-current"], cwd=demo_repo)
    status = run(["git", "status", "--short"], cwd=demo_repo)

    assert before_branch == after_branch
    assert status.strip() == ""


def test_default_branch_name_is_derived_from_session(demo_repo):
    ct.close("demo", "t-001", "done", "session-b", None, {}, dry_run=False)

    branches = run(["git", "branch", "-r"], cwd=demo_repo)
    assert "origin/close/demo-t-001-session-b" in branches


def test_dry_run_pushes_nothing(demo_repo):
    ct.close("demo", "t-001", "done", "session-b", "close/demo-t-001-session-b", {}, dry_run=True)

    run(["git", "fetch", "-q", "origin"], cwd=demo_repo)
    branches = run(["git", "branch", "-r"], cwd=demo_repo)
    assert "origin/close/demo-t-001-session-b" not in branches


def test_already_at_target_status_refuses_without_force(tmp_path, monkeypatch):
    clone = make_remote_and_clone(tmp_path, DONE_ROADMAP)
    monkeypatch.setattr(ct, "ROOT", clone)
    monkeypatch.setattr(ct, "PROJECTS_DIR", clone / "projects")

    with pytest.raises(ct.CloseError) as excinfo:
        ct.close("demo", "t-001", "done", "session-b", None, {}, dry_run=False)
    assert excinfo.value.code == 1
    assert "already status" in str(excinfo.value)


def test_force_allows_reclosing_same_status_to_set_extra_fields(tmp_path, monkeypatch):
    clone = make_remote_and_clone(tmp_path, DONE_ROADMAP)
    monkeypatch.setattr(ct, "ROOT", clone)
    monkeypatch.setattr(ct, "PROJECTS_DIR", clone / "projects")

    ct.close(
        "demo",
        "t-001",
        "done",
        "session-b",
        "close/demo-t-001-session-b",
        {"owner": "null"},
        dry_run=False,
        force=True,
    )

    run(["git", "fetch", "-q", "origin"], cwd=clone)
    doc = yaml.safe_load(
        run(
            ["git", "show", "origin/close/demo-t-001-session-b:projects/demo/roadmap.yaml"],
            cwd=clone,
        )
    )
    assert doc["tasks"][0]["owner"] is None


def test_missing_task_raises_close_error(demo_repo):
    with pytest.raises(ct.CloseError) as excinfo:
        ct.close("demo", "t-999", "done", "session-b", None, {}, dry_run=False)
    assert excinfo.value.code == 1
    assert "not found" in str(excinfo.value)


def test_extra_set_fields_are_applied_alongside_status(demo_repo):
    ct.close(
        "demo",
        "t-001",
        "needs-human",
        "session-b",
        "close/demo-t-001-session-b",
        {"soft_gate": "true"},
        dry_run=False,
    )

    run(["git", "fetch", "-q", "origin"], cwd=demo_repo)
    doc = yaml.safe_load(
        run(
            ["git", "show", "origin/close/demo-t-001-session-b:projects/demo/roadmap.yaml"],
            cwd=demo_repo,
        )
    )
    task = doc["tasks"][0]
    assert task["status"] == "needs-human"
    assert task["soft_gate"] is True


TWO_TASK_ROADMAP = """\
project: demo
kind: software
tasks:
- id: t-001
  title: Demo task one
  status: review
  owner: worker
- id: t-002
  title: Demo task two
  status: review
  owner: worker
"""


def test_reusing_a_branch_name_retries_on_top_of_its_new_tip(tmp_path, monkeypatch):
    """A session bundling several task close-outs into one PR calls close_task.py
    once per task against the SAME branch. The second call must build on top of
    the first call's commit (the branch's actual tip), not on the stale
    origin/main it started from, so both edits land together -- mirroring
    claim_task.py's non-fast-forward retry behavior."""
    clone = make_remote_and_clone(tmp_path, TWO_TASK_ROADMAP)
    monkeypatch.setattr(ct, "ROOT", clone)
    monkeypatch.setattr(ct, "PROJECTS_DIR", clone / "projects")

    ct.close("demo", "t-001", "done", "session-b", "close/shared-branch", {"note": "first"}, dry_run=False)
    ct.close("demo", "t-002", "done", "session-b", "close/shared-branch", {}, dry_run=False)

    run(["git", "fetch", "-q", "origin"], cwd=clone)
    doc = yaml.safe_load(
        run(["git", "show", "origin/close/shared-branch:projects/demo/roadmap.yaml"], cwd=clone)
    )
    tasks = {t["id"]: t for t in doc["tasks"]}
    assert tasks["t-001"]["status"] == "done"
    assert tasks["t-001"]["note"] == "first"
    assert tasks["t-002"]["status"] == "done"
