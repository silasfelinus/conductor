"""Regression coverage for conductor/t-188's direct close_task handoff guard."""

import subprocess
from pathlib import Path

import pytest

import scripts.close_task as ct


def run(cmd: list[str], cwd: Path) -> str:
    return subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True).stdout


def make_repo(tmp_path: Path, *, committed_handoff: bool = False) -> Path:
    bare = tmp_path / "bare"
    clone = tmp_path / "clone"
    bare.mkdir()
    clone.mkdir()
    run(["git", "init", "-q", "--bare"], bare)
    run(["git", "init", "-q"], clone)
    run(["git", "config", "user.email", "test@example.com"], clone)
    run(["git", "config", "user.name", "Test"], clone)

    roadmap = clone / "projects" / "demo" / "roadmap.yaml"
    roadmap.parent.mkdir(parents=True)
    roadmap.write_text(
        "project: demo\nkind: software\ntasks:\n"
        "- id: t-001\n  title: Demo\n  status: review\n  owner: worker\n",
        encoding="utf-8",
    )
    if committed_handoff:
        handoff = clone / "projects" / "demo" / "docs" / "t-001-handoff.md"
        handoff.parent.mkdir(parents=True)
        handoff.write_text("# Handoff\n", encoding="utf-8")
    run(["git", "add", "-A"], clone)
    run(["git", "commit", "-q", "-m", "init"], clone)
    run(["git", "remote", "add", "origin", str(bare)], clone)
    run(["git", "push", "-q", "origin", "HEAD:refs/heads/main"], clone)
    return clone


def install_repo(monkeypatch, clone: Path) -> None:
    monkeypatch.setattr(ct, "ROOT", clone)
    monkeypatch.setattr(ct, "PROJECTS_DIR", clone / "projects")


def test_needs_human_refuses_missing_handoff(tmp_path, monkeypatch):
    clone = make_repo(tmp_path)
    install_repo(monkeypatch, clone)

    with pytest.raises(ct.CloseError, match="references missing handoff document"):
        ct.close(
            "demo",
            "t-001",
            "needs-human",
            "session-a",
            "close/demo-t-001-session-a",
            {},
            dry_run=False,
            append_note="Preserved at projects/demo/docs/t-001-handoff.md.",
        )

    run(["git", "fetch", "-q", "origin"], clone)
    assert "close/demo-t-001-session-a" not in run(["git", "branch", "-r"], clone)


def test_uncommitted_worktree_handoff_does_not_satisfy_guard(tmp_path, monkeypatch):
    clone = make_repo(tmp_path)
    install_repo(monkeypatch, clone)
    handoff = clone / "projects" / "demo" / "docs" / "t-001-handoff.md"
    handoff.parent.mkdir(parents=True)
    handoff.write_text("# Loose file only\n", encoding="utf-8")

    with pytest.raises(ct.CloseError, match="references missing handoff document"):
        ct.close(
            "demo",
            "t-001",
            "needs-human",
            "session-a",
            "close/demo-t-001-session-a",
            {},
            dry_run=False,
            append_note="Preserved at projects/demo/docs/t-001-handoff.md.",
        )


def test_committed_handoff_allows_needs_human_close(tmp_path, monkeypatch):
    clone = make_repo(tmp_path, committed_handoff=True)
    install_repo(monkeypatch, clone)

    ct.close(
        "demo",
        "t-001",
        "needs-human",
        "session-a",
        "close/demo-t-001-session-a",
        {},
        dry_run=False,
        append_note="Preserved at projects/demo/docs/t-001-handoff.md.",
    )

    run(["git", "fetch", "-q", "origin"], clone)
    assert "origin/close/demo-t-001-session-a" in run(["git", "branch", "-r"], clone)


def test_non_needs_human_transition_ignores_handoff_text(tmp_path, monkeypatch):
    clone = make_repo(tmp_path)
    install_repo(monkeypatch, clone)

    ct.close(
        "demo",
        "t-001",
        "done",
        "session-a",
        "close/demo-t-001-session-a",
        {},
        dry_run=False,
        append_note="Historical mention: projects/demo/docs/t-001-handoff.md.",
    )

    run(["git", "fetch", "-q", "origin"], clone)
    assert "origin/close/demo-t-001-session-a" in run(["git", "branch", "-r"], clone)
