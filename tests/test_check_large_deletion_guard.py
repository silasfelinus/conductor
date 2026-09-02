"""
Tests for scripts/check_large_deletion_guard.py.

Splits into (1) pure threshold-logic tests against evaluate_deletion(), no git
involved, and (2) one integration test against a real throwaway git repo
modeling the exact conductor/t-143 shape (a large art-prompts.yaml-style
file, most of it deleted in one commit) to exercise the actual
numstat/base_line_count git plumbing, not just the pure logic.
"""

import subprocess
from pathlib import Path

import scripts.check_large_deletion_guard as guard


def run(cmd: list[str], cwd: Path) -> str:
    result = subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)
    return result.stdout


# --- pure threshold logic -----------------------------------------------


def test_small_deletion_is_not_flagged():
    assert guard.evaluate_deletion("projects/x/roadmap.yaml", 1000, 10, 5) is None


def test_no_deletion_is_not_flagged():
    assert guard.evaluate_deletion("projects/x/roadmap.yaml", 1000, 0, 200) is None


def test_absolute_threshold_flags_regardless_of_base_size():
    finding = guard.evaluate_deletion("projects/art-prompts.yaml", 20000, 600, 3)
    assert finding is not None
    assert finding["removed_lines"] == 600
    assert finding["base_lines"] == 20000


def test_percentage_threshold_flags_large_fraction_of_a_big_file():
    # 25% of a 1000-line file removed, well under the absolute threshold.
    finding = guard.evaluate_deletion("projects/x/roadmap.yaml", 1000, 250, 10)
    assert finding is not None
    assert finding["removed_pct"] == 25.0


def test_percentage_threshold_excludes_small_base_files():
    # 70% of a 10-line file removed -- exactly the kind of noisy swing on a
    # brand-new small roadmap the MIN_BASE_LINES_FOR_PCT floor exists to skip.
    assert guard.evaluate_deletion("projects/new/roadmap.yaml", 10, 7, 0) is None


def test_new_file_with_zero_base_lines_is_not_flagged():
    # A file that didn't exist at base (base_line_count == 0) can't have
    # "deleted" a fraction of itself.
    assert guard.evaluate_deletion("projects/new/roadmap.yaml", 0, 0, 50) is None


# --- real-git integration -------------------------------------------------


def make_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    run(["git", "init", "-q"], cwd=repo)
    run(["git", "config", "user.email", "test@example.com"], cwd=repo)
    run(["git", "config", "user.name", "Test"], cwd=repo)
    return repo


def write(repo: Path, rel: str, content: str) -> None:
    path = repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def commit(repo: Path, message: str) -> str:
    run(["git", "add", "-A"], cwd=repo)
    run(["git", "commit", "-q", "-m", message], cwd=repo)
    return run(["git", "rev-parse", "HEAD"], cwd=repo).strip()


def test_scan_flags_a_large_art_prompts_deletion(tmp_path):
    repo = make_repo(tmp_path)

    # Base: art-prompts.yaml with 600 append-only request rows.
    rows = "\n".join(f"- id: req-{i}\n  status: pending" for i in range(600))
    write(repo, "projects/art-prompts.yaml", rows + "\n")
    base_sha = commit(repo, "seed art-prompts")

    # Head: the t-143 incident shape -- almost everything wiped, one row left.
    write(repo, "projects/art-prompts.yaml", "- id: req-0\n  status: pending\n")
    head_sha = commit(repo, "accidental wipe")

    result = guard.scan(base_sha, head_sha, cwd=repo)

    assert result["findings"], "expected the near-total wipe to be flagged"
    finding = result["findings"][0]
    assert finding["path"] == "projects/art-prompts.yaml"
    assert finding["removed_lines"] >= guard.ABS_LINE_THRESHOLD


def test_scan_is_clean_for_a_normal_append(tmp_path):
    repo = make_repo(tmp_path)

    rows = "\n".join(f"- id: req-{i}\n  status: pending" for i in range(600))
    write(repo, "projects/art-prompts.yaml", rows + "\n")
    base_sha = commit(repo, "seed art-prompts")

    # Head: append a few new rows, nothing removed.
    write(repo, "projects/art-prompts.yaml", rows + "\n- id: req-600\n  status: pending\n")
    head_sha = commit(repo, "append one row")

    result = guard.scan(base_sha, head_sha, cwd=repo)

    assert result["findings"] == []


def test_scan_ignores_files_outside_the_watch_list(tmp_path):
    repo = make_repo(tmp_path)

    rows = "\n".join(f"line {i}" for i in range(600))
    write(repo, "projects/some-project/notes.md", rows + "\n")
    base_sha = commit(repo, "seed notes")

    write(repo, "projects/some-project/notes.md", "line 0\n")
    head_sha = commit(repo, "wipe notes")

    result = guard.scan(base_sha, head_sha, cwd=repo)

    # notes.md is not a roadmap.yaml or art-prompts.yaml -- out of scope for
    # this guard even though the deletion shape is identical.
    assert result["findings"] == []


def test_scan_flags_a_roadmap_yaml_deletion(tmp_path):
    repo = make_repo(tmp_path)

    tasks = "\n".join(f"  - id: t-{i}\n    status: done" for i in range(100))
    write(repo, "projects/demo/roadmap.yaml", f"tasks:\n{tasks}\n")
    base_sha = commit(repo, "seed roadmap")

    write(repo, "projects/demo/roadmap.yaml", "tasks:\n  - id: t-0\n    status: done\n")
    head_sha = commit(repo, "drop most tasks")

    result = guard.scan(base_sha, head_sha, cwd=repo)

    assert len(result["findings"]) == 1
    assert result["findings"][0]["path"] == "projects/demo/roadmap.yaml"


def test_render_reports_clean_when_no_findings():
    result = {"base": "main", "head": "HEAD", "findings": []}
    assert "No large deletions" in guard.render(result)


def test_render_mentions_path_and_percentage():
    result = {
        "base": "main",
        "head": "HEAD",
        "findings": [
            {
                "path": "projects/art-prompts.yaml",
                "base_lines": 20000,
                "added_lines": 3,
                "removed_lines": 11000,
                "removed_pct": 55.0,
            }
        ],
    }
    rendered = guard.render(result)
    assert "projects/art-prompts.yaml" in rendered
    assert "55.0%" in rendered


def test_target_paths_includes_art_prompts_and_every_roadmap(tmp_path):
    write(tmp_path, "projects/art-prompts.yaml", "- id: req-0\n")
    write(tmp_path, "projects/alpha/roadmap.yaml", "tasks: []\n")
    write(tmp_path, "projects/beta/roadmap.yaml", "tasks: []\n")

    paths = guard.target_paths(tmp_path)

    assert "projects/art-prompts.yaml" in paths
    assert "projects/alpha/roadmap.yaml" in paths
    assert "projects/beta/roadmap.yaml" in paths
