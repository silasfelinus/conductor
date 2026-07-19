"""
Tests for check_pr_file_overlap.py — the advisory same-project open-PR file-overlap
check (conductor newsfeed/t-016). No network calls.
"""

import scripts.check_pr_file_overlap as cpo


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
# find_projects
# --------------------------------------------------------------------------- #

def test_find_projects_extracts_slug_from_title():
    assert cpo.find_projects("newsfeed/t-008: fix thing") == ["newsfeed"]


def test_find_projects_dedupes_and_preserves_order():
    text = "newsfeed/t-008 and later newsfeed/t-010, also ai-art-academy/t-019"
    assert cpo.find_projects(text) == ["newsfeed", "ai-art-academy"]


def test_find_projects_empty_when_no_task_id():
    assert cpo.find_projects("just a regular PR title") == []


# --------------------------------------------------------------------------- #
# find_overlaps
# --------------------------------------------------------------------------- #

def test_overlap_flagged_for_same_project_shared_file():
    target = pr(number=1, title="newsfeed/t-008: a", files=["a.vue", "b.ts"])
    others = [pr(number=2, title="newsfeed/t-010: b", files=["b.ts", "c.ts"])]
    result = cpo.find_overlaps(target, others)
    assert len(result) == 1
    assert result[0]["number"] == 2
    assert result[0]["overlapping_files"] == ["b.ts"]
    assert result[0]["shared_projects"] == ["newsfeed"]


def test_no_overlap_when_different_project():
    target = pr(number=1, title="newsfeed/t-008: a", files=["a.vue"])
    others = [pr(number=2, title="davinci/t-011: b", body="davinci/t-011", files=["a.vue"])]
    assert cpo.find_overlaps(target, others) == []


def test_no_overlap_when_files_disjoint():
    target = pr(number=1, title="newsfeed/t-008: a", files=["a.vue"])
    others = [pr(number=2, title="newsfeed/t-010: b", files=["c.ts"])]
    assert cpo.find_overlaps(target, others) == []


def test_target_pr_excluded_from_its_own_others_list():
    target = pr(number=1, title="newsfeed/t-008: a", files=["a.vue"])
    others = [pr(number=1, title="newsfeed/t-008: a", files=["a.vue"])]
    assert cpo.find_overlaps(target, others) == []


def test_no_task_id_in_target_yields_no_overlaps():
    target = pr(number=1, title="misc fix", body="", files=["a.vue"])
    others = [pr(number=2, title="newsfeed/t-010: b", files=["a.vue"])]
    assert cpo.find_overlaps(target, others) == []


def test_target_with_no_files_yields_no_overlaps():
    target = pr(number=1, title="newsfeed/t-008: a", files=[])
    others = [pr(number=2, title="newsfeed/t-010: b", files=["a.vue"])]
    assert cpo.find_overlaps(target, others) == []


def test_multiple_overlapping_prs_all_reported():
    target = pr(number=1, title="newsfeed/t-008: a", files=["a.vue", "b.ts"])
    others = [
        pr(number=2, title="newsfeed/t-010: b", files=["b.ts"]),
        pr(number=3, title="newsfeed/t-012: c", files=["a.vue"]),
    ]
    result = cpo.find_overlaps(target, others)
    assert {r["number"] for r in result} == {2, 3}


# --------------------------------------------------------------------------- #
# format_warning
# --------------------------------------------------------------------------- #

def test_format_warning_mentions_pr_number_and_files():
    target = pr(number=1)
    overlaps = [
        {"number": 2, "title": "newsfeed/t-010: b", "shared_projects": ["newsfeed"], "overlapping_files": ["b.ts"]}
    ]
    msg = cpo.format_warning(target, overlaps)
    assert "#1" in msg
    assert "#2" in msg
    assert "b.ts" in msg


# --------------------------------------------------------------------------- #
# main() CLI
# --------------------------------------------------------------------------- #

def test_main_prints_nothing_for_clean_pr(tmp_path, capsys):
    target_path = tmp_path / "target.json"
    others_path = tmp_path / "others.json"
    target_path.write_text('{"number": 1, "title": "newsfeed/t-008: a", "body": "", "files": ["a.vue"]}')
    others_path.write_text("[]")
    import sys as _sys

    old_argv = _sys.argv
    try:
        _sys.argv = ["check_pr_file_overlap.py", "--target", str(target_path), "--others", str(others_path)]
        rc = cpo.main()
    finally:
        _sys.argv = old_argv
    assert rc == 0
    captured = capsys.readouterr()
    assert captured.out == ""


def test_main_prints_warning_for_overlapping_pr(tmp_path, capsys):
    target_path = tmp_path / "target.json"
    others_path = tmp_path / "others.json"
    target_path.write_text('{"number": 1, "title": "newsfeed/t-008: a", "body": "", "files": ["a.vue"]}')
    others_path.write_text('[{"number": 2, "title": "newsfeed/t-010: b", "body": "", "files": ["a.vue"]}]')
    import sys as _sys

    old_argv = _sys.argv
    try:
        _sys.argv = ["check_pr_file_overlap.py", "--target", str(target_path), "--others", str(others_path)]
        rc = cpo.main()
    finally:
        _sys.argv = old_argv
    assert rc == 0
    captured = capsys.readouterr()
    assert "WARNING" in captured.out
    assert "a.vue" in captured.out


def test_main_json_output(tmp_path, capsys):
    target_path = tmp_path / "target.json"
    others_path = tmp_path / "others.json"
    target_path.write_text('{"number": 1, "title": "newsfeed/t-008: a", "body": "", "files": ["a.vue"]}')
    others_path.write_text('[{"number": 2, "title": "newsfeed/t-010: b", "body": "", "files": ["a.vue"]}]')
    import json as _json
    import sys as _sys

    old_argv = _sys.argv
    try:
        _sys.argv = [
            "check_pr_file_overlap.py",
            "--target",
            str(target_path),
            "--others",
            str(others_path),
            "--json",
        ]
        rc = cpo.main()
    finally:
        _sys.argv = old_argv
    assert rc == 0
    captured = capsys.readouterr()
    data = _json.loads(captured.out)
    assert data["target"] == 1
    assert data["overlaps"][0]["number"] == 2
