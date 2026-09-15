"""Regression coverage for conductor/t-161 branch-tip safety."""

import subprocess
from pathlib import Path

import pytest

import scripts.close_task as ct


def git(cwd: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=cwd, check=True, capture_output=True, text=True
    ).stdout.strip()


def make_repo(tmp_path: Path, monkeypatch) -> Path:
    bare = tmp_path / "bare"
    clone = tmp_path / "clone"
    git(tmp_path, "init", "-q", "--bare", str(bare))
    git(tmp_path, "init", "-q", str(clone))
    git(clone, "config", "user.email", "test@example.com")
    git(clone, "config", "user.name", "Test")
    path = clone / "projects/demo/roadmap.yaml"
    path.parent.mkdir(parents=True)
    path.write_text(
        "project: demo\nkind: software\ntasks:\n- id: t-001\n  title: Demo\n  status: claimed\n  owner: worker\n",
        encoding="utf-8",
    )
    git(clone, "add", "-A")
    git(clone, "commit", "-q", "-m", "init")
    git(clone, "remote", "add", "origin", str(bare))
    git(clone, "push", "-q", "origin", "HEAD:refs/heads/main")
    monkeypatch.setattr(ct, "ROOT", clone)
    monkeypatch.setattr(ct, "PROJECTS_DIR", clone / "projects")
    return clone


def test_close_refuses_to_drop_unpushed_commit_on_named_local_branch(tmp_path, monkeypatch):
    repo = make_repo(tmp_path, monkeypatch)
    branch = "worker/demo-t-001"
    git(repo, "checkout", "-q", "-b", branch)
    git(repo, "push", "-q", "-u", "origin", branch)

    marker = repo / "implementation.txt"
    marker.write_text("must survive\n", encoding="utf-8")
    git(repo, "add", "implementation.txt")
    git(repo, "commit", "-q", "-m", "local implementation")
    local_tip = git(repo, "rev-parse", "HEAD")
    remote_tip = git(repo, "rev-parse", f"origin/{branch}")
    assert local_tip != remote_tip

    with pytest.raises(ct.CloseError, match="could omit local/unpushed commits"):
        ct.close("demo", "t-001", "review", "session-a", branch, {}, dry_run=False)

    # Refusal is non-destructive: neither local nor remote branch moved.
    assert git(repo, "rev-parse", "HEAD") == local_tip
    assert git(repo, "rev-parse", f"origin/{branch}") == remote_tip


def test_close_allows_named_local_branch_when_tip_matches_remote(tmp_path, monkeypatch):
    repo = make_repo(tmp_path, monkeypatch)
    branch = "worker/demo-t-001"
    git(repo, "checkout", "-q", "-b", branch)
    git(repo, "push", "-q", "-u", "origin", branch)

    ct.close("demo", "t-001", "review", "session-a", branch, {}, dry_run=False)
    git(repo, "fetch", "-q", "origin", branch)
    assert git(repo, "show", f"origin/{branch}:projects/demo/roadmap.yaml").find("status: review") >= 0
