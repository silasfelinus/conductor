"""
Tests for check_pr_merged_drift.py — the sweep that flags conductor tasks
stuck at claimed/review whose referenced cross-repo PR already merged
(conductor/t-071). Fixture roadmaps + mocked GitHub responses, no network,
no real project files touched.
"""

import io
import urllib.error
from unittest.mock import patch

import scripts.check_pr_merged_drift as dr


class FakeResponse:
    def __init__(self, data):
        self._data = data

    def read(self):
        return self._data

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


def http_error(code, body=b""):
    return urllib.error.HTTPError("http://x", code, "err", {}, io.BytesIO(body))


def write_roadmap(root, slug, tasks):
    project_dir = root / "projects" / slug
    project_dir.mkdir(parents=True, exist_ok=True)
    lines = ["tasks:"]
    for t in tasks:
        lines.append(f"  - id: {t['id']}")
        lines.append(f"    status: {t['status']}")
        lines.append(f"    title: \"{t['title']}\"")
        if t.get("note"):
            lines.append(f"    note: \"{t['note']}\"")
    (project_dir / "roadmap.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------- #
# find_pr_refs
# --------------------------------------------------------------------------- #

def test_find_pr_refs_matches_known_repo_alias():
    text = "Kaizen from newsfeed/t-020 (kind_robots PR #517, merged)."
    assert dr.find_pr_refs(text) == [("silasfelinus/kind_robots", 517)]


def test_find_pr_refs_dedupes_repeated_reference():
    text = "kind_robots PR #517 landed. See kind_robots PR #517 for detail."
    assert dr.find_pr_refs(text) == [("silasfelinus/kind_robots", 517)]


def test_find_pr_refs_ignores_bare_pr_number():
    text = "Fixed by PR #503, root cause still open."
    assert dr.find_pr_refs(text) == []


def test_find_pr_refs_ignores_unknown_repo_prefix():
    text = "humboldt-scoop PR #12 shipped it."
    assert dr.find_pr_refs(text) == []


def test_find_pr_refs_multiple_repos():
    text = "conductor PR #40 filed the kaizen; kind_robots PR #517 fixed it."
    assert dr.find_pr_refs(text) == [
        ("silasfelinus/conductor", 40),
        ("silasfelinus/kind_robots", 517),
    ]


# --------------------------------------------------------------------------- #
# scan
# --------------------------------------------------------------------------- #

def test_scan_only_picks_up_claimed_and_review_tasks(tmp_path):
    write_roadmap(tmp_path, "newsfeed", [
        {"id": "t-020", "status": "claimed", "title": "x", "note": "kind_robots PR #517"},
        {"id": "t-021", "status": "review", "title": "y", "note": "kind_robots PR #518"},
        {"id": "t-022", "status": "done", "title": "z", "note": "kind_robots PR #519"},
        {"id": "t-023", "status": "ready", "title": "w", "note": "kind_robots PR #520"},
    ])
    result = dr.scan(tmp_path / "projects")
    pr_numbers = sorted(c["pr_number"] for c in result)
    assert pr_numbers == [517, 518]


def test_scan_skips_tasks_with_no_pr_reference(tmp_path):
    write_roadmap(tmp_path, "davinci", [
        {"id": "t-001", "status": "claimed", "title": "no reference here"},
    ])
    assert dr.scan(tmp_path / "projects") == []


def test_scan_skips_template_project(tmp_path):
    write_roadmap(tmp_path, "_template", [
        {"id": "t-001", "status": "claimed", "title": "x", "note": "kind_robots PR #1"},
    ])
    assert dr.scan(tmp_path / "projects") == []


# --------------------------------------------------------------------------- #
# check (mocked GitHub API)
# --------------------------------------------------------------------------- #

def test_check_flags_merged_pr():
    candidates = [{
        "project": "newsfeed", "task_id": "t-020", "title": "x", "status": "claimed",
        "repo": "silasfelinus/kind_robots", "pr_number": 517,
    }]
    body = b'{"merged": true, "merged_at": "2026-07-19T16:16:31Z", "title": "newsfeed/t-020"}'

    with patch("urllib.request.urlopen", return_value=FakeResponse(body)):
        findings, unresolved = dr.check(candidates, token=None)

    assert len(findings) == 1
    assert findings[0]["pr_merged_at"] == "2026-07-19T16:16:31Z"
    assert unresolved == []


def test_check_does_not_flag_open_pr():
    candidates = [{
        "project": "newsfeed", "task_id": "t-020", "title": "x", "status": "claimed",
        "repo": "silasfelinus/kind_robots", "pr_number": 517,
    }]
    body = b'{"merged": false, "merged_at": null, "title": "newsfeed/t-020"}'

    with patch("urllib.request.urlopen", return_value=FakeResponse(body)):
        findings, unresolved = dr.check(candidates, token=None)

    assert findings == []
    assert unresolved == []


def test_check_reports_pr_lookup_failure_as_unresolved_not_clean():
    candidates = [{
        "project": "newsfeed", "task_id": "t-020", "title": "x", "status": "claimed",
        "repo": "silasfelinus/kind_robots", "pr_number": 404,
    }]

    with patch("urllib.request.urlopen", side_effect=http_error(404)):
        findings, unresolved = dr.check(candidates, token=None)

    assert findings == []
    assert unresolved == candidates


# --------------------------------------------------------------------------- #
# render
# --------------------------------------------------------------------------- #

def test_render_reports_clean_state():
    assert "No drift found" in dr.render([], [], total=1)


def test_render_lists_each_finding():
    findings = [{
        "project": "newsfeed", "task_id": "t-020", "status": "claimed",
        "repo": "silasfelinus/kind_robots", "pr_number": 517,
        "pr_title": "newsfeed/t-020: fix", "pr_merged_at": "2026-07-19T16:16:31Z",
    }]
    out = dr.render(findings, [], total=1)
    assert "newsfeed/t-020" in out
    assert "silasfelinus/kind_robots#517" in out


def test_render_flags_unresolved_instead_of_claiming_clean():
    unresolved = [{
        "project": "newsfeed", "task_id": "t-020", "title": "x", "status": "claimed",
        "repo": "silasfelinus/kind_robots", "pr_number": 404,
    }]
    out = dr.render([], unresolved, total=1)
    assert "No drift found" not in out
    assert "could NOT be verified" in out
    assert "newsfeed/t-020" in out
