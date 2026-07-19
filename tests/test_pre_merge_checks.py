"""
Tests for pre_merge_checks.py — the single-invocation wrapper that runs every
advisory pre-merge PR check (check_pr_kaizen.py + check_pr_file_overlap.py) in
one pass (conductor/t-070). No network calls.
"""

import json

import scripts.pre_merge_checks as pmc


def pr(**overrides):
    base = {
        "number": 900,
        "title": "newsfeed/t-008: something",
        "body": "conductor newsfeed/t-008",
        "files": ["components/newsfeed-feed.vue"],
    }
    base.update(overrides)
    return base


# --------------------------------------------------------------------------- #
# run_checks
# --------------------------------------------------------------------------- #

def test_run_checks_clean_pr_both_none():
    target = pr(title="newsfeed/t-008: a", body="### Kaizen suggestion\nnone", files=["a.vue"])
    results = pmc.run_checks(target, [])
    assert results["kaizen"] is None
    assert results["overlap"] == []


def test_run_checks_flags_missing_kaizen_section():
    target = pr(title="newsfeed/t-008: a", body="no section here", files=["a.vue"])
    results = pmc.run_checks(target, [])
    assert results["kaizen"] is not None
    assert "newsfeed/t-008" in results["kaizen"]


def test_run_checks_flags_file_overlap():
    target = pr(number=1, title="newsfeed/t-008: a", body="### Kaizen suggestion\nnone", files=["a.vue"])
    others = [pr(number=2, title="newsfeed/t-010: b", body="newsfeed/t-010", files=["a.vue"])]
    results = pmc.run_checks(target, others)
    assert results["kaizen"] is None
    assert len(results["overlap"]) == 1
    assert results["overlap"][0]["number"] == 2


def test_run_checks_flags_both_independently():
    target = pr(number=1, title="newsfeed/t-008: a", body="no section", files=["a.vue"])
    others = [pr(number=2, title="newsfeed/t-010: b", body="newsfeed/t-010", files=["a.vue"])]
    results = pmc.run_checks(target, others)
    assert results["kaizen"] is not None
    assert len(results["overlap"]) == 1


# --------------------------------------------------------------------------- #
# format_results
# --------------------------------------------------------------------------- #

def test_format_results_empty_when_clean():
    target = pr(body="### Kaizen suggestion\nnone", files=["a.vue"])
    results = {"kaizen": None, "overlap": []}
    assert pmc.format_results(target, results) == ""


def test_format_results_includes_both_sections():
    target = pr(number=1)
    results = {
        "kaizen": "WARNING: PR references task id(s) newsfeed/t-008 but has no ...",
        "overlap": [
            {"number": 2, "title": "newsfeed/t-010: b", "shared_projects": ["newsfeed"], "overlapping_files": ["b.ts"]}
        ],
    }
    text = pmc.format_results(target, results)
    assert "WARNING: PR references task id(s)" in text
    assert "#2" in text
    assert "b.ts" in text


# --------------------------------------------------------------------------- #
# main() CLI
# --------------------------------------------------------------------------- #

def _run_main(tmp_path, target, others, extra_args=None):
    target_path = tmp_path / "target.json"
    others_path = tmp_path / "others.json"
    target_path.write_text(json.dumps(target))
    others_path.write_text(json.dumps(others))

    import sys as _sys

    old_argv = _sys.argv
    try:
        _sys.argv = [
            "pre_merge_checks.py",
            "--target",
            str(target_path),
            "--others",
            str(others_path),
            *(extra_args or []),
        ]
        rc = pmc.main()
    finally:
        _sys.argv = old_argv
    return rc


def test_main_prints_nothing_for_clean_pr(tmp_path, capsys):
    target = pr(body="### Kaizen suggestion\nnone", files=["a.vue"])
    rc = _run_main(tmp_path, target, [])
    assert rc == 0
    captured = capsys.readouterr()
    assert captured.out == ""


def test_main_prints_both_warnings(tmp_path, capsys):
    target = pr(number=1, title="newsfeed/t-008: a", body="no section", files=["a.vue"])
    others = [pr(number=2, title="newsfeed/t-010: b", body="newsfeed/t-010", files=["a.vue"])]
    rc = _run_main(tmp_path, target, others)
    assert rc == 0
    captured = capsys.readouterr()
    assert "WARNING: PR references task id(s)" in captured.out
    assert "WARNING: PR #1 shares changed files" in captured.out


def test_main_json_output(tmp_path, capsys):
    target = pr(number=1, title="newsfeed/t-008: a", body="no section", files=["a.vue"])
    others = [pr(number=2, title="newsfeed/t-010: b", body="newsfeed/t-010", files=["a.vue"])]
    rc = _run_main(tmp_path, target, others, extra_args=["--json"])
    assert rc == 0
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data["target"] == 1
    assert data["kaizen"] is not None
    assert data["overlap"][0]["number"] == 2


def test_main_errors_on_non_array_others(tmp_path, capsys):
    target = pr()
    target_path = tmp_path / "target.json"
    others_path = tmp_path / "others.json"
    target_path.write_text(json.dumps(target))
    others_path.write_text(json.dumps({"not": "a list"}))

    import sys as _sys

    old_argv = _sys.argv
    try:
        _sys.argv = [
            "pre_merge_checks.py",
            "--target",
            str(target_path),
            "--others",
            str(others_path),
        ]
        rc = pmc.main()
    finally:
        _sys.argv = old_argv
    assert rc == 2
    captured = capsys.readouterr()
    assert "ERROR" in captured.err
