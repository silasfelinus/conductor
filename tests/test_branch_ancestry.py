"""Tests for scripts/branch_ancestry.py's classify_relationship (conductor/t-163)."""

import subprocess
from pathlib import Path

import pytest

import scripts.branch_ancestry as ba
import scripts.git_plumbing as gp


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)


def make_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    run(["git", "init", "-q"], cwd=repo)
    run(["git", "config", "user.email", "test@example.com"], cwd=repo)
    run(["git", "config", "user.name", "Test"], cwd=repo)
    (repo / "file.txt").write_text("base\n", encoding="utf-8")
    run(["git", "add", "-A"], cwd=repo)
    run(["git", "commit", "-q", "-m", "base"], cwd=repo)
    return repo


def commit(repo: Path, message: str) -> str:
    (repo / "file.txt").write_text(f"{message}\n", encoding="utf-8")
    run(["git", "add", "-A"], cwd=repo)
    run(["git", "commit", "-q", "-m", message], cwd=repo)
    return run(["git", "rev-parse", "HEAD"], cwd=repo).stdout.strip()


def test_equal_when_same_commit(tmp_path):
    repo = make_repo(tmp_path)
    sha = run(["git", "rev-parse", "HEAD"], cwd=repo).stdout.strip()
    assert ba.classify_relationship(repo, sha, "HEAD") == "equal"


def test_ahead_when_a_has_extra_commits(tmp_path):
    repo = make_repo(tmp_path)
    base = run(["git", "rev-parse", "HEAD"], cwd=repo).stdout.strip()
    ahead = commit(repo, "extra")
    assert ba.classify_relationship(repo, ahead, base) == "ahead"


def test_behind_when_b_has_extra_commits(tmp_path):
    repo = make_repo(tmp_path)
    base = run(["git", "rev-parse", "HEAD"], cwd=repo).stdout.strip()
    ahead = commit(repo, "extra")
    assert ba.classify_relationship(repo, base, ahead) == "behind"


def test_diverged_when_neither_is_an_ancestor(tmp_path):
    repo = make_repo(tmp_path)
    base = run(["git", "rev-parse", "HEAD"], cwd=repo).stdout.strip()
    run(["git", "checkout", "-q", "-b", "left"], cwd=repo)
    left = commit(repo, "left-only")
    run(["git", "checkout", "-q", "-b", "right", base], cwd=repo)
    right = commit(repo, "right-only")
    assert ba.classify_relationship(repo, left, right) == "diverged"
    assert ba.classify_relationship(repo, right, left) == "diverged"


def test_raises_git_error_on_unresolvable_ref(tmp_path):
    repo = make_repo(tmp_path)
    with pytest.raises(gp.GitError):
        ba.classify_relationship(repo, "refs/heads/does-not-exist", "HEAD")
