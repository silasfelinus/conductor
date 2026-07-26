"""
Tests for scripts/append_ledger_entry.py against real (throwaway, local-only) git
repos -- no network access, no real origin. Exercises the actual retry-on-race plumbing
(conductor/t-085), not just the pure text-building logic, since the race handling is the
part this task exists to add.
"""

import subprocess
from pathlib import Path

import pytest
import yaml

import scripts.append_ledger_entry as ale


def run(cmd: list[str], cwd: Path) -> None:
    subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)


def show(repo: Path, ref: str, path: str) -> str:
    result = subprocess.run(
        ["git", "show", f"{ref}:{path}"], cwd=repo, check=True, capture_output=True, text=True
    )
    return result.stdout


TALKBACK_SEED = """\
# TALKBACK.md — demo

Append-only log.

## 2026-07-01 | Reviewer -> Worker | demo/t-001 | pattern
type: pattern

**Subject:** first entry.
"""

LEARNING_SEED = """\
records:
- date: '2026-07-01'
  project: demo
  task: t-001
  kind: software
  stakes: reversible
  passes: 0
  outcome: done
  failure_category: null
  lesson: >
    first lesson.
"""

EMPTY_LEARNING_SEED = "records: []\n"


@pytest.fixture
def demo_repo(tmp_path):
    bare = tmp_path / "bare"
    clone = tmp_path / "clone"
    bare.mkdir()
    clone.mkdir()

    run(["git", "init", "-q", "--bare"], cwd=bare)
    run(["git", "init", "-q"], cwd=clone)
    run(["git", "config", "user.email", "test@example.com"], cwd=clone)
    run(["git", "config", "user.name", "Test"], cwd=clone)

    (clone / "TALKBACK.md").write_text(TALKBACK_SEED, encoding="utf-8")
    (clone / "LEARNING.yaml").write_text(LEARNING_SEED, encoding="utf-8")

    run(["git", "add", "-A"], cwd=clone)
    run(["git", "commit", "-q", "-m", "init"], cwd=clone)
    run(["git", "remote", "add", "origin", str(bare)], cwd=clone)
    run(["git", "push", "-q", "origin", "HEAD:refs/heads/main"], cwd=clone)
    return clone


def test_append_talkback_entry_pushes_to_origin_main(demo_repo):
    entry = "## 2026-07-26 | Worker -> Reviewer | demo/t-002 | pattern\ntype: pattern\n\n**Subject:** second entry.\n"

    ale.append_talkback_entry(demo_repo, "TALKBACK.md", entry, "talkback: demo/t-002")

    run(["git", "fetch", "-q", "origin", "main"], cwd=demo_repo)
    text = show(demo_repo, "origin/main", "TALKBACK.md")
    assert "first entry." in text
    assert "second entry." in text
    # exactly one blank line between the two headings, no clobbering of prior bytes
    assert "\n\n## 2026-07-26 | Worker -> Reviewer | demo/t-002" in text


def test_append_talkback_rejects_entry_without_heading(demo_repo):
    with pytest.raises(ValueError):
        ale.append_talkback_entry(demo_repo, "TALKBACK.md", "not a heading\n", "talkback: bad")


def test_append_does_not_touch_callers_branch_or_worktree(demo_repo):
    before_branch = subprocess.run(
        ["git", "branch", "--show-current"], cwd=demo_repo, capture_output=True, text=True
    ).stdout

    ale.append_talkback_entry(
        demo_repo, "TALKBACK.md", "## 2026-07-26 | Worker -> Reviewer | demo/t-002 | pattern\n", "talkback: t-002"
    )

    after_branch = subprocess.run(
        ["git", "branch", "--show-current"], cwd=demo_repo, capture_output=True, text=True
    ).stdout
    status = subprocess.run(
        ["git", "status", "--short"], cwd=demo_repo, capture_output=True, text=True
    ).stdout

    assert before_branch == after_branch
    assert status.strip() == ""


def test_append_learning_record_appends_without_touching_prior_record(demo_repo):
    record = {
        "date": "2026-07-26",
        "project": "demo",
        "task": "t-002",
        "kind": "software",
        "stakes": "reversible",
        "passes": 0,
        "outcome": "done",
        "failure_category": None,
        "lesson": "second lesson.",
    }

    ale.append_learning_record(demo_repo, record, "learning: demo/t-002")

    run(["git", "fetch", "-q", "origin", "main"], cwd=demo_repo)
    text = show(demo_repo, "origin/main", "LEARNING.yaml")
    doc = yaml.safe_load(text)
    assert len(doc["records"]) == 2
    assert doc["records"][0]["task"] == "t-001"
    assert doc["records"][1]["task"] == "t-002"
    assert "first lesson." in text  # prior record's exact bytes untouched


def test_append_learning_record_handles_empty_ledger(tmp_path):
    bare = tmp_path / "bare"
    clone = tmp_path / "clone"
    bare.mkdir()
    clone.mkdir()
    run(["git", "init", "-q", "--bare"], cwd=bare)
    run(["git", "init", "-q"], cwd=clone)
    run(["git", "config", "user.email", "test@example.com"], cwd=clone)
    run(["git", "config", "user.name", "Test"], cwd=clone)
    (clone / "LEARNING.yaml").write_text(EMPTY_LEARNING_SEED, encoding="utf-8")
    run(["git", "add", "-A"], cwd=clone)
    run(["git", "commit", "-q", "-m", "init"], cwd=clone)
    run(["git", "remote", "add", "origin", str(bare)], cwd=clone)
    run(["git", "push", "-q", "origin", "HEAD:refs/heads/main"], cwd=clone)

    record = {"date": "2026-07-26", "project": "demo", "task": "t-001", "lesson": "first."}
    ale.append_learning_record(clone, record, "learning: demo/t-001")

    run(["git", "fetch", "-q", "origin", "main"], cwd=clone)
    doc = yaml.safe_load(show(clone, "origin/main", "LEARNING.yaml"))
    assert len(doc["records"]) == 1
    assert doc["records"][0]["task"] == "t-001"


def test_concurrent_appends_both_land_via_retry(demo_repo, tmp_path):
    """Regression coverage for the exact race conductor/t-085 exists to close: two
    sessions append to the same file in the same window. The second call's push races
    against the first (simulated here by advancing origin/main out from under it between
    its read and its push) and must retry onto the new tip instead of clobbering or
    losing the first entry."""
    second_clone = tmp_path / "clone2"
    run(["git", "clone", "-q", str(tmp_path / "bare"), str(second_clone)], cwd=tmp_path)
    run(["git", "config", "user.email", "test2@example.com"], cwd=second_clone)
    run(["git", "config", "user.name", "Test2"], cwd=second_clone)

    original_commit = ale.commit_file_on_ref
    call_count = {"n": 0}

    def land_session_a_directly() -> None:
        """Commits session A's entry using the *unpatched* plumbing, on a separate
        clone, so it never re-enters (and re-counts against) the patched function
        below -- this call must look like an entirely different, concurrent process."""
        run(["git", "clone", "-q", str(tmp_path / "bare"), str(tmp_path / "clone-a")], cwd=tmp_path)
        clone_a = tmp_path / "clone-a"
        run(["git", "config", "user.email", "testA@example.com"], cwd=clone_a)
        run(["git", "config", "user.name", "TestA"], cwd=clone_a)
        parent_sha = ale.resolve_ref(clone_a, "origin/main")
        before = ale.read_file_at_ref(clone_a, "origin/main", "TALKBACK.md")
        after = ale.build_talkback_append(
            before, "## 2026-07-26 | Worker -> Reviewer | demo/t-A | pattern\n**Subject:** session A.\n"
        )
        assert original_commit(clone_a, parent_sha, "refs/heads/main", "TALKBACK.md", after, "talkback: demo/t-A")

    def racing_commit_file_on_ref(root, parent_sha, ref, path, content, message):
        call_count["n"] += 1
        if call_count["n"] == 1:
            # Land session A's append first, out from under session B's in-flight call.
            land_session_a_directly()
        return original_commit(root, parent_sha, ref, path, content, message)

    ale.commit_file_on_ref = racing_commit_file_on_ref
    try:
        ale.append_talkback_entry(
            second_clone,
            "TALKBACK.md",
            "## 2026-07-26 | Worker -> Reviewer | demo/t-B | pattern\n**Subject:** session B.\n",
            "talkback: demo/t-B",
        )
    finally:
        ale.commit_file_on_ref = original_commit

    assert call_count["n"] == 2  # first push raced (non-fast-forward), second succeeded

    run(["git", "fetch", "-q", "origin", "main"], cwd=demo_repo)
    text = show(demo_repo, "origin/main", "TALKBACK.md")
    assert "session A." in text
    assert "session B." in text
