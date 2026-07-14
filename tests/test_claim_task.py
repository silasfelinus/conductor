"""
Integration tests for claim_task.py against real (throwaway, local-only) git repos --
no network access, no real origin. Exercises the actual git plumbing (scratch-index
commit + push), not just the pure YAML-editing logic, since that's the part most
likely to silently break (see conductor/t-040).
"""

import subprocess
from pathlib import Path

import pytest
import yaml

import scripts.claim_task as ct


def run(cmd: list[str], cwd: Path) -> None:
    subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)


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


READY_ROADMAP = """\
project: demo
kind: software
tasks:
- id: t-001
  title: Demo task
  status: ready
  owner: null
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
    clone = make_remote_and_clone(tmp_path, READY_ROADMAP)
    monkeypatch.setattr(ct, "ROOT", clone)
    monkeypatch.setattr(ct, "PROJECTS_DIR", clone / "projects")
    return clone


def test_claim_pushes_status_claimed_to_origin_main(demo_repo):
    ct.claim("demo", "t-001", "reviewer", "session-a", dry_run=False)

    run(["git", "fetch", "-q", "origin", "main"], cwd=demo_repo)
    result = subprocess.run(
        ["git", "show", "origin/main:projects/demo/roadmap.yaml"],
        cwd=demo_repo,
        check=True,
        capture_output=True,
        text=True,
    )
    doc = yaml.safe_load(result.stdout)
    task = doc["tasks"][0]
    assert task["status"] == "claimed"
    assert task["owner"] == "reviewer"
    assert task["claimed_by"] == "session-a"
    assert task["claimed_at"]


def test_claim_does_not_touch_callers_branch_or_worktree(demo_repo):
    before_branch = subprocess.run(
        ["git", "branch", "--show-current"], cwd=demo_repo, capture_output=True, text=True
    ).stdout

    ct.claim("demo", "t-001", "reviewer", "session-a", dry_run=False)

    after_branch = subprocess.run(
        ["git", "branch", "--show-current"], cwd=demo_repo, capture_output=True, text=True
    ).stdout
    status = subprocess.run(
        ["git", "status", "--short"], cwd=demo_repo, capture_output=True, text=True
    ).stdout

    assert before_branch == after_branch
    assert status.strip() == ""


def test_dry_run_claims_nothing(demo_repo):
    ct.claim("demo", "t-001", "reviewer", "session-a", dry_run=True)

    run(["git", "fetch", "-q", "origin", "main"], cwd=demo_repo)
    result = subprocess.run(
        ["git", "log", "--oneline", "origin/main"], cwd=demo_repo, capture_output=True, text=True
    )
    assert result.stdout.count("\n") == 1  # only the initial "init" commit


def test_already_claimed_task_raises_claim_error(tmp_path, monkeypatch):
    clone = make_remote_and_clone(tmp_path, DONE_ROADMAP)
    monkeypatch.setattr(ct, "ROOT", clone)
    monkeypatch.setattr(ct, "PROJECTS_DIR", clone / "projects")

    with pytest.raises(ct.ClaimError) as excinfo:
        ct.claim("demo", "t-001", "reviewer", "session-a", dry_run=False)
    assert excinfo.value.code == 3
    assert "ALREADY_CLAIMED" in str(excinfo.value)


def test_second_session_cannot_claim_after_first_lands(demo_repo):
    ct.claim("demo", "t-001", "worker", "session-a", dry_run=False)

    with pytest.raises(ct.ClaimError) as excinfo:
        ct.claim("demo", "t-001", "reviewer", "session-b", dry_run=False)
    assert excinfo.value.code == 3
