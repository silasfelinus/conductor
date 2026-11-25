"""Tests for scripts/check_workflow_yaml.py (memory-dungeon/t-071)."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import check_workflow_yaml as cwy

GOOD = "name: ok\non: push\njobs:\n  a:\n    runs-on: ubuntu-latest\n    steps: []\n"


def test_repo_workflows_all_parse():
    assert cwy.main([]) == 0


def test_seeded_bad_file_fails(tmp_path, capsys):
    (tmp_path / "good.yml").write_text(GOOD)
    # The t-070 shape: a mis-indented key makes the whole file unparseable.
    (tmp_path / "ci.yml").write_text(
        "name: ci\njobs:\n  a:\n    steps:\n   - run: x\n  bad: [\n"
    )
    assert cwy.main(["--dir", str(tmp_path)]) == 1
    err = capsys.readouterr().err
    assert "ci.yml: does not parse" in err
    assert "good.yml" not in err


def test_non_mapping_and_missing_jobs_fail(tmp_path):
    (tmp_path / "list.yml").write_text("- just\n- a list\n")
    (tmp_path / "nojobs.yaml").write_text("name: x\non: push\n")
    problems = cwy.workflow_problems(tmp_path)
    assert any("list.yml: root is not a mapping" in p for p in problems)
    assert any("nojobs.yaml: has no `jobs` mapping" in p for p in problems)


def test_empty_dir_fails(tmp_path):
    assert cwy.main(["--dir", str(tmp_path)]) == 1


def test_good_dir_passes(tmp_path):
    (tmp_path / "good.yml").write_text(GOOD)
    assert cwy.main(["--dir", str(tmp_path)]) == 0
