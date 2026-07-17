"""
Tests for scripts/git_plumbing.py's commit_file_on_ref -- specifically that it signs
the commit when the repo has commit.gpgsign configured (conductor/t-061).

commit-tree does NOT apply commit.gpgsign the way porcelain `git commit` does, so this
needs an explicit -S flag. Without it, every direct-to-ref commit claim_task.py makes
(one per task claim, across every project) lands unsigned/"Unverified" on GitHub even
when the caller's git config has signing fully set up.

Isolated from the host's real global/system git config (GIT_CONFIG_GLOBAL/SYSTEM point
at os.devnull) so these tests are deterministic regardless of whether the machine
running them has its own commit.gpgsign/user.signingkey already set -- this repo's own
CI sandbox does, which would otherwise make the "not configured" cases false-negative.
"""

import os
import shutil
import subprocess
from pathlib import Path

import pytest

import scripts.git_plumbing as gp


@pytest.fixture(autouse=True)
def isolated_git_config(monkeypatch):
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", os.devnull)
    monkeypatch.setenv("GIT_CONFIG_SYSTEM", os.devnull)


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)


def make_repo(tmp_path: Path, name: str) -> Path:
    """Bare 'origin' + a real clone, matching commit_file_on_ref's expected remote."""
    bare = tmp_path / f"{name}-bare"
    bare.mkdir()
    run(["git", "init", "-q", "--bare"], cwd=bare)

    clone = tmp_path / name
    clone.mkdir()
    run(["git", "init", "-q"], cwd=clone)
    run(["git", "config", "user.email", "test@example.com"], cwd=clone)
    run(["git", "config", "user.name", "Test"], cwd=clone)
    (clone / "seed.txt").write_text("seed\n", encoding="utf-8")
    run(["git", "add", "-A"], cwd=clone)
    run(["git", "commit", "-q", "-m", "init"], cwd=clone)
    run(["git", "remote", "add", "origin", str(bare)], cwd=clone)
    run(["git", "push", "-q", "origin", "HEAD:refs/heads/main"], cwd=clone)
    return clone


def configure_ssh_signing(repo: Path, tmp_path: Path) -> None:
    key_path = tmp_path / "signing_key"
    run(["ssh-keygen", "-t", "ed25519", "-N", "", "-f", str(key_path), "-q"], cwd=repo)
    run(["git", "config", "commit.gpgsign", "true"], cwd=repo)
    run(["git", "config", "gpg.format", "ssh"], cwd=repo)
    run(["git", "config", "user.signingkey", str(key_path) + ".pub"], cwd=repo)


def commit_at_ref(repo: Path, ref: str) -> str:
    result = subprocess.run(
        ["git", "cat-file", "commit", ref], cwd=repo, capture_output=True, text=True, check=True
    )
    return result.stdout


def test_gpgsign_enabled_false_when_config_absent(tmp_path):
    repo = make_repo(tmp_path, "repo-default")
    assert gp.gpgsign_enabled(repo) is False


def test_gpgsign_enabled_false_when_explicitly_false(tmp_path):
    repo = make_repo(tmp_path, "repo-explicit-false")
    run(["git", "config", "commit.gpgsign", "false"], cwd=repo)
    assert gp.gpgsign_enabled(repo) is False


def test_commits_unsigned_when_gpgsign_not_configured(tmp_path):
    repo = make_repo(tmp_path, "repo-unsigned")
    parent_sha = gp.resolve_ref(repo, "HEAD")

    ok = gp.commit_file_on_ref(repo, parent_sha, "refs/heads/main", "out.txt", "hello\n", "unsigned commit")
    assert ok is True

    run(["git", "fetch", "-q", "origin", "main"], cwd=repo)
    raw = commit_at_ref(repo, "origin/main")
    assert "gpgsig" not in raw


@pytest.mark.skipif(shutil.which("ssh-keygen") is None, reason="ssh-keygen not installed")
def test_commits_signed_when_gpgsign_configured(tmp_path):
    repo = make_repo(tmp_path, "repo-signed")
    configure_ssh_signing(repo, tmp_path)
    parent_sha = gp.resolve_ref(repo, "HEAD")

    assert gp.gpgsign_enabled(repo) is True

    ok = gp.commit_file_on_ref(repo, parent_sha, "refs/heads/main", "out.txt", "hello\n", "signed commit")
    assert ok is True

    run(["git", "fetch", "-q", "origin", "main"], cwd=repo)
    raw = commit_at_ref(repo, "origin/main")
    assert "gpgsig" in raw
    assert "SSH SIGNATURE" in raw
