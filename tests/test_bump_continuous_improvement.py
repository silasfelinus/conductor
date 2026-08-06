import subprocess
import sys
from pathlib import Path

import yaml

import scripts.bump_continuous_improvement as bci

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "bump_continuous_improvement.py"

# Mirrors ai-art-academy/t-010's real shape: an inline comment on last_lane
# documenting the enum, a quoted timestamp, and a quoted owner/repo#N ref
# (which itself contains a literal `#` -- the exact character a naive
# trailing-comment scanner would misread as a YAML comment).
ROADMAP = """\
project: demo
kind: software
milestones:
- id: m1
  title: First milestone
  status: not-started
tasks:
- id: t-010
  milestone: m6
  title: Recurring task
  status: ready
  recurring: true
  note: |-
    Standing instructions here.
  continuous_improvement:
    last_lane: 4  # 1=front-end polish, 2=roadmap accuracy, 3=inspiration assets, 4=curriculum depth
    next_lane: 1
    last_run: '2026-08-06T11:32:00Z'
    last_pr: 'silasfelinus/conductor#1793'
  run_log: docs/run-log.md
  implementation_pr: null
- id: t-011
  milestone: m6
  title: Recurring task with no continuous_improvement mapping yet
  status: ready
  recurring: true
- id: t-012
  milestone: m6
  title: Recurring task with a partial mapping
  status: ready
  recurring: true
  continuous_improvement:
    last_lane: 1
"""


def parse_tasks(text: str) -> dict:
    data = yaml.safe_load(text)
    return {task["id"]: task for task in data["tasks"]}


def write_demo_repo(tmp_path: Path) -> Path:
    projects_dir = tmp_path / "projects" / "demo"
    projects_dir.mkdir(parents=True)
    roadmap = projects_dir / "roadmap.yaml"
    roadmap.write_text(ROADMAP)
    return roadmap


def run_cli(tmp_path: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )


def test_bumps_lane_and_derives_next_lane_with_wraparound(tmp_path: Path):
    roadmap = write_demo_repo(tmp_path)
    result = run_cli(
        tmp_path, "demo", "t-010", "--lane", "4", "--pr", "silasfelinus/conductor#1800", "--run", "2026-08-06T13:00:00Z"
    )
    assert result.returncode == 0, result.stderr
    task = parse_tasks(roadmap.read_text())["t-010"]
    ci = task["continuous_improvement"]
    assert ci["last_lane"] == 4
    assert ci["next_lane"] == 1  # wraps 4 -> 1
    assert ci["last_run"] == "2026-08-06T13:00:00Z"
    assert ci["last_pr"] == "silasfelinus/conductor#1800"


def test_mid_rotation_lane_advances_by_one(tmp_path: Path):
    roadmap = write_demo_repo(tmp_path)
    result = run_cli(tmp_path, "demo", "t-010", "--lane", "2", "--pr", "silasfelinus/conductor#1801")
    assert result.returncode == 0, result.stderr
    ci = parse_tasks(roadmap.read_text())["t-010"]["continuous_improvement"]
    assert ci["last_lane"] == 2
    assert ci["next_lane"] == 3


def test_preserves_inline_comment_on_last_lane(tmp_path: Path):
    roadmap = write_demo_repo(tmp_path)
    run_cli(tmp_path, "demo", "t-010", "--lane", "3", "--pr", "silasfelinus/conductor#1802")
    text = roadmap.read_text()
    assert "last_lane: 3  # 1=front-end polish, 2=roadmap accuracy, 3=inspiration assets, 4=curriculum depth" in text


def test_pr_ref_containing_hash_is_not_mistaken_for_a_comment(tmp_path: Path):
    # Regression: an earlier version of extract_trailing_comment() matched any
    # `#` in the line, including one inside the quoted last_pr value itself,
    # and appended a second bogus "comment" after the closing quote.
    roadmap = write_demo_repo(tmp_path)
    run_cli(tmp_path, "demo", "t-010", "--lane", "3", "--pr", "silasfelinus/conductor#9999")
    text = roadmap.read_text()
    assert "last_pr: 'silasfelinus/conductor#9999'\n" in text
    assert "#9999'#" not in text


def test_other_fields_and_tasks_are_untouched(tmp_path: Path):
    roadmap = write_demo_repo(tmp_path)
    before = parse_tasks(ROADMAP)
    run_cli(tmp_path, "demo", "t-010", "--lane", "1", "--pr", "silasfelinus/conductor#1803")
    after = parse_tasks(roadmap.read_text())
    assert after["t-010"]["note"] == before["t-010"]["note"]
    assert after["t-010"]["run_log"] == before["t-010"]["run_log"]
    assert after["t-011"] == before["t-011"]
    assert after["t-012"] == before["t-012"]


def test_missing_mapping_key_is_appended_not_an_error(tmp_path: Path):
    roadmap = write_demo_repo(tmp_path)
    result = run_cli(tmp_path, "demo", "t-012", "--lane", "2", "--pr", "silasfelinus/conductor#1804")
    assert result.returncode == 0, result.stderr
    ci = parse_tasks(roadmap.read_text())["t-012"]["continuous_improvement"]
    assert ci == {
        "last_lane": 2,
        "next_lane": 3,
        "last_run": ci["last_run"],  # timestamped by --run now, not asserted exactly
        "last_pr": "silasfelinus/conductor#1804",
    }


def test_task_with_no_mapping_fails_clearly(tmp_path: Path):
    write_demo_repo(tmp_path)
    result = run_cli(tmp_path, "demo", "t-011", "--lane", "1", "--pr", "silasfelinus/conductor#1805")
    assert result.returncode == 1
    assert "continuous_improvement" in result.stderr


def test_invalid_lane_number_rejected(tmp_path: Path):
    write_demo_repo(tmp_path)
    result = run_cli(tmp_path, "demo", "t-010", "--lane", "5", "--pr", "silasfelinus/conductor#1806")
    assert result.returncode == 1
    assert "--lane must be between 1 and 4" in result.stderr


def test_invalid_pr_ref_rejected(tmp_path: Path):
    write_demo_repo(tmp_path)
    result = run_cli(tmp_path, "demo", "t-010", "--lane", "1", "--pr", "not-a-valid-ref")
    assert result.returncode == 1
    assert "--pr must look like owner/repo#number" in result.stderr


def test_missing_task_fails_clearly(tmp_path: Path):
    write_demo_repo(tmp_path)
    result = run_cli(tmp_path, "demo", "t-999", "--lane", "1", "--pr", "silasfelinus/conductor#1807")
    assert result.returncode == 1
    assert "not found" in result.stderr


def test_cli_dry_run_prints_diff_without_writing(tmp_path: Path):
    roadmap = write_demo_repo(tmp_path)
    result = run_cli(tmp_path, "demo", "t-010", "--lane", "1", "--pr", "silasfelinus/conductor#1808", "--dry-run")
    assert result.returncode == 0, result.stderr
    assert "+    last_lane: 1" in result.stdout
    assert roadmap.read_text() == ROADMAP


def test_extract_trailing_comment_handles_quoted_and_plain_scalars():
    assert bci.extract_trailing_comment("4  # an enum comment") == "  # an enum comment"
    assert bci.extract_trailing_comment("'silasfelinus/conductor#1793'") == ""
    assert bci.extract_trailing_comment("'silasfelinus/conductor#1793'  # trailing note") == "  # trailing note"
    assert bci.extract_trailing_comment("3") == ""


def test_real_ai_art_academy_roadmap_roundtrip():
    # Exercise against the actual repo roadmap this tool exists to edit.
    path = Path(__file__).resolve().parent.parent / "projects" / "ai-art-academy" / "roadmap.yaml"
    real = path.read_text()
    out = bci.bump_continuous_improvement_text(real, "t-010", 3, "silasfelinus/conductor#1999", "2026-08-06T13:30:00Z")
    data = yaml.safe_load(out)
    t010 = next(t for t in data["tasks"] if t["id"] == "t-010")
    ci = t010["continuous_improvement"]
    assert ci["last_lane"] == 3
    assert ci["next_lane"] == 4
    assert ci["last_pr"] == "silasfelinus/conductor#1999"
    # Every other task in the real roadmap must parse unchanged.
    other_real = yaml.safe_load(real)
    other_ids = [t["id"] for t in other_real["tasks"] if t["id"] != "t-010"]
    after_ids = [t["id"] for t in data["tasks"] if t["id"] != "t-010"]
    assert after_ids == other_ids
