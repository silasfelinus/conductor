"""
Tests for check_pr_merged_drift.py — the sweep that flags conductor tasks
stuck at claimed/review whose referenced cross-repo PR already merged
(conductor/t-071). Fixture roadmaps + mocked GitHub responses, no network,
no real project files touched.
"""

import io
import json
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
    for task in tasks:
        lines.append(f"  - id: {task['id']}")
        lines.append(f"    status: {task['status']}")
        lines.append(f"    title: \"{task['title']}\"")
        if task.get("note"):
            lines.append(f"    note: \"{task['note']}\"")
        if task.get("implementation_pr"):
            lines.append(f"    implementation_pr: \"{task['implementation_pr']}\"")
        if task.get("remaining_scope_task"):
            lines.append(f"    remaining_scope_task: \"{task['remaining_scope_task']}\"")
    (project_dir / "roadmap.yaml").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def write_overrides(root, entries):
    lines = ["overrides:"]
    for slug, status in entries:
        lines.extend([f"  - slug: {slug}", f"    status: {status}"])
    (root / "project-overrides.yaml").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


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
# parse_implementation_pr (conductor/t-099)
# --------------------------------------------------------------------------- #


def test_parse_implementation_pr_parses_owner_repo_number():
    assert dr.parse_implementation_pr("silasfelinus/kind_robots#1464") == (
        "silasfelinus/kind_robots",
        1464,
    )


def test_parse_implementation_pr_strips_surrounding_whitespace():
    assert dr.parse_implementation_pr("  silasfelinus/kind_robots#1464  ") == (
        "silasfelinus/kind_robots",
        1464,
    )


def test_parse_implementation_pr_returns_none_for_missing_field():
    assert dr.parse_implementation_pr(None) is None
    assert dr.parse_implementation_pr("") is None


def test_parse_implementation_pr_returns_none_for_malformed_value():
    assert dr.parse_implementation_pr("kind_robots PR #1464") is None
    assert dr.parse_implementation_pr("silasfelinus/kind_robots") is None
    assert dr.parse_implementation_pr("#1464") is None


# --------------------------------------------------------------------------- #
# scan
# --------------------------------------------------------------------------- #


def test_scan_only_picks_up_claimed_and_review_tasks(tmp_path):
    write_roadmap(
        tmp_path,
        "newsfeed",
        [
            {
                "id": "t-020",
                "status": "claimed",
                "title": "x",
                "note": "kind_robots PR #517",
            },
            {
                "id": "t-021",
                "status": "review",
                "title": "y",
                "note": "kind_robots PR #518",
            },
            {
                "id": "t-022",
                "status": "done",
                "title": "z",
                "note": "kind_robots PR #519",
            },
            {
                "id": "t-023",
                "status": "ready",
                "title": "w",
                "note": "kind_robots PR #520",
            },
        ],
    )
    result = dr.scan(tmp_path / "projects")
    pr_numbers = sorted(candidate["pr_number"] for candidate in result)
    assert pr_numbers == [517, 518]


def test_scan_skips_tasks_with_no_pr_reference(tmp_path):
    write_roadmap(
        tmp_path,
        "davinci",
        [{"id": "t-001", "status": "claimed", "title": "no reference here"}],
    )
    assert dr.scan(tmp_path / "projects") == []


def test_scan_skips_template_project(tmp_path):
    write_roadmap(
        tmp_path,
        "_template",
        [
            {
                "id": "t-001",
                "status": "claimed",
                "title": "x",
                "note": "kind_robots PR #1",
            }
        ],
    )
    assert dr.scan(tmp_path / "projects") == []


def test_scan_skips_paused_projects_by_default(tmp_path):
    write_roadmap(
        tmp_path,
        "mermaids-of-venice",
        [
            {
                "id": "t-001",
                "status": "review",
                "title": "x",
                "note": "kind_robots PR #517",
            }
        ],
    )
    write_overrides(tmp_path, [("mermaids-of-venice", "paused")])

    assert dr.scan(tmp_path / "projects") == []


def test_scan_can_include_paused_projects_explicitly(tmp_path):
    write_roadmap(
        tmp_path,
        "mermaids-of-venice",
        [
            {
                "id": "t-001",
                "status": "review",
                "title": "x",
                "note": "kind_robots PR #517",
            }
        ],
    )
    write_overrides(tmp_path, [("mermaids-of-venice", "paused")])

    result = dr.scan(tmp_path / "projects", include_inactive=True)
    assert len(result) == 1
    assert result[0]["project_status"] == "paused"


# --------------------------------------------------------------------------- #
# check (mocked GitHub API)
# --------------------------------------------------------------------------- #


def test_check_flags_merged_pr():
    candidates = [
        {
            "project": "newsfeed",
            "task_id": "t-020",
            "title": "x",
            "status": "claimed",
            "repo": "silasfelinus/kind_robots",
            "pr_number": 517,
        }
    ]
    body = b'{"merged": true, "merged_at": "2026-07-19T16:16:31Z", "title": "newsfeed/t-020"}'

    with patch("urllib.request.urlopen", return_value=FakeResponse(body)):
        findings, unresolved = dr.check(candidates, token=None)

    assert len(findings) == 1
    assert findings[0]["pr_merged_at"] == "2026-07-19T16:16:31Z"
    assert unresolved == []


def test_check_does_not_flag_open_pr():
    candidates = [
        {
            "project": "newsfeed",
            "task_id": "t-020",
            "title": "x",
            "status": "claimed",
            "repo": "silasfelinus/kind_robots",
            "pr_number": 517,
        }
    ]
    body = b'{"merged": false, "merged_at": null, "title": "newsfeed/t-020"}'

    with patch("urllib.request.urlopen", return_value=FakeResponse(body)):
        findings, unresolved = dr.check(candidates, token=None)

    assert findings == []
    assert unresolved == []


def test_check_reports_pr_lookup_failure_as_unresolved_not_clean():
    candidates = [
        {
            "project": "newsfeed",
            "task_id": "t-020",
            "title": "x",
            "status": "claimed",
            "repo": "silasfelinus/kind_robots",
            "pr_number": 404,
        }
    ]

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
    findings = [
        {
            "project": "newsfeed",
            "task_id": "t-020",
            "status": "claimed",
            "repo": "silasfelinus/kind_robots",
            "pr_number": 517,
            "pr_title": "newsfeed/t-020: fix",
            "pr_merged_at": "2026-07-19T16:16:31Z",
        }
    ]
    output = dr.render(findings, [], total=1)
    assert "newsfeed/t-020" in output
    assert "silasfelinus/kind_robots#517" in output


def test_render_flags_unresolved_instead_of_claiming_clean():
    unresolved = [
        {
            "project": "newsfeed",
            "task_id": "t-020",
            "title": "x",
            "status": "claimed",
            "repo": "silasfelinus/kind_robots",
            "pr_number": 404,
        }
    ]
    output = dr.render([], unresolved, total=1)
    assert "No drift found" not in output
    assert "could NOT be verified" in output
    assert "newsfeed/t-020" in output


def test_render_labels_weak_findings_as_unconfirmed():
    weak = [
        {
            "project": "interface-vision",
            "task_id": "t-081",
            "status": "claimed",
            "repo": "silasfelinus/kind_robots",
            "pr_number": 1391,
            "pr_title": "some other task's kaizen PR",
            "pr_merged_at": "2026-07-28T00:00:00Z",
        }
    ]
    output = dr.render([], [], total=1, weak=weak)
    assert "No drift found" not in output
    assert "weak evidence" in output
    assert "interface-vision/t-081" in output
    assert "silasfelinus/kind_robots#1391" in output


def test_render_reports_clean_state_with_no_weak_findings():
    assert "No drift found" in dr.render([], [], total=1, weak=[])


# --------------------------------------------------------------------------- #
# scan_in_progress_tasks
# --------------------------------------------------------------------------- #


def test_scan_in_progress_tasks_includes_tasks_with_no_pr_reference(tmp_path):
    write_roadmap(
        tmp_path,
        "davinci",
        [
            {"id": "t-001", "status": "claimed", "title": "no reference here"},
            {"id": "t-002", "status": "done", "title": "done, excluded"},
        ],
    )
    result = dr.scan_in_progress_tasks(tmp_path / "projects")
    assert [t["task_id"] for t in result] == ["t-001"]


# --------------------------------------------------------------------------- #
# gh_search_task_prs
# --------------------------------------------------------------------------- #


def test_gh_search_task_prs_parses_repository_url():
    body = json.dumps({
        "items": [
            {
                "number": 1464,
                "repository_url": "https://api.github.com/repos/silasfelinus/kind_robots",
            }
        ]
    }).encode()

    with patch("urllib.request.urlopen", return_value=FakeResponse(body)):
        results = dr.gh_search_task_prs(
            ["silasfelinus/kind_robots"], "interface-vision", "t-081", token=None
        )

    assert results == [{"repo": "silasfelinus/kind_robots", "number": 1464}]


def test_gh_search_task_prs_returns_none_on_api_failure():
    with patch("urllib.request.urlopen", side_effect=http_error(403)):
        results = dr.gh_search_task_prs(
            ["silasfelinus/kind_robots"], "interface-vision", "t-081", token=None
        )
    assert results is None


def test_gh_search_task_prs_skips_call_with_no_repos():
    with patch("urllib.request.urlopen") as mock_urlopen:
        results = dr.gh_search_task_prs([], "interface-vision", "t-081", token=None)
    assert results == []
    mock_urlopen.assert_not_called()


# --------------------------------------------------------------------------- #
# check_drift — the combined two-pass orchestration (conductor/t-098)
# --------------------------------------------------------------------------- #


def test_check_drift_prefers_task_id_search_over_note_reference(tmp_path):
    # interface-vision/t-081: note quotes kind_robots#1391 (the kaizen-filing
    # PR, merged, but NOT the implementation), while the real implementation
    # kind_robots#1464 is only discoverable via task-id search — never
    # mentioned in the note. The authoritative pass must find #1464 as the
    # high-confidence finding and NOT also report #1391 as a competing one.
    write_roadmap(
        tmp_path,
        "interface-vision",
        [
            {
                "id": "t-081",
                "status": "claimed",
                "title": "Facet create affordance",
                "note": "Filed from kind_robots PR #1391's kaizen suggestion.",
            }
        ],
    )

    search_body = json.dumps({
        "items": [
            {
                "number": 1464,
                "repository_url": "https://api.github.com/repos/silasfelinus/kind_robots",
            }
        ]
    }).encode()
    pr_1464_body = json.dumps({
        "merged": True,
        "merged_at": "2026-08-01T00:00:00Z",
        "title": "interface-vision/t-081: facet create affordance",
    }).encode()

    def fake_urlopen(req, timeout=10):
        url = req.full_url if hasattr(req, "full_url") else req
        if "search/issues" in url:
            return FakeResponse(search_body)
        return FakeResponse(pr_1464_body)

    with patch("urllib.request.urlopen", side_effect=fake_urlopen):
        result = dr.check_drift(tmp_path / "projects", token=None)

    assert len(result["high"]) == 1
    assert result["high"][0]["pr_number"] == 1464
    assert result["high"][0]["confidence"] == "high"
    assert result["weak"] == []
    assert result["unresolved"] == []


def test_check_drift_falls_back_to_note_reference_when_no_task_id_match(tmp_path):
    write_roadmap(
        tmp_path,
        "newsfeed",
        [
            {
                "id": "t-020",
                "status": "claimed",
                "title": "x",
                "note": "kind_robots PR #517",
            }
        ],
    )

    empty_search_body = json.dumps({"items": []}).encode()
    pr_517_body = json.dumps({
        "merged": True,
        "merged_at": "2026-07-19T16:16:31Z",
        "title": "newsfeed/t-020: fix",
    }).encode()

    def fake_urlopen(req, timeout=10):
        url = req.full_url if hasattr(req, "full_url") else req
        if "search/issues" in url:
            return FakeResponse(empty_search_body)
        return FakeResponse(pr_517_body)

    with patch("urllib.request.urlopen", side_effect=fake_urlopen):
        result = dr.check_drift(tmp_path / "projects", token=None)

    assert result["high"] == []
    assert len(result["weak"]) == 1
    assert result["weak"][0]["pr_number"] == 517
    assert result["weak"][0]["confidence"] == "low"
    assert result["unresolved"] == []


def test_check_drift_does_not_downgrade_to_weak_when_search_itself_failed(tmp_path):
    # If the authoritative search call errors out for a task, that task must
    # land in `unresolved` -- NOT silently fall back to a "weak" note-based
    # finding presented as if the authoritative pass came back clean/empty.
    write_roadmap(
        tmp_path,
        "newsfeed",
        [
            {
                "id": "t-020",
                "status": "claimed",
                "title": "x",
                "note": "kind_robots PR #517",
            }
        ],
    )

    def fake_urlopen(req, timeout=10):
        raise http_error(403)

    with patch("urllib.request.urlopen", side_effect=fake_urlopen):
        result = dr.check_drift(tmp_path / "projects", token=None)

    assert result["high"] == []
    assert result["weak"] == []
    assert len(result["unresolved"]) == 1
    assert result["unresolved"][0]["task_id"] == "t-020"


def test_check_drift_clean_when_no_evidence_either_way(tmp_path):
    write_roadmap(
        tmp_path,
        "davinci",
        [{"id": "t-001", "status": "claimed", "title": "in progress, no PR yet"}],
    )
    empty_search_body = json.dumps({"items": []}).encode()

    with patch("urllib.request.urlopen", return_value=FakeResponse(empty_search_body)):
        result = dr.check_drift(tmp_path / "projects", token=None)

    assert result == {
        "high": [],
        "weak": [],
        "unresolved": [],
        "remaining_scope_resolved": [],
    }


# --------------------------------------------------------------------------- #
# check_drift — implementation_pr field pass (conductor/t-099)
# --------------------------------------------------------------------------- #


def test_check_drift_field_present_confirms_without_search_call(tmp_path):
    # Field-present path: a task carrying implementation_pr is checked
    # directly against that PR and never triggers the title-search call at
    # all -- the field is stronger evidence, so pass 1 is skipped entirely.
    write_roadmap(
        tmp_path,
        "newsfeed",
        [
            {
                "id": "t-020",
                "status": "claimed",
                "title": "x",
                "implementation_pr": "silasfelinus/kind_robots#1464",
            }
        ],
    )

    pr_body = json.dumps({
        "merged": True,
        "merged_at": "2026-08-01T00:00:00Z",
        "title": "some unrelated PR title",
    }).encode()

    def fake_urlopen(req, timeout=10):
        url = req.full_url if hasattr(req, "full_url") else req
        assert "search/issues" not in url, "field-present task must not hit the search API"
        return FakeResponse(pr_body)

    with patch("urllib.request.urlopen", side_effect=fake_urlopen):
        result = dr.check_drift(tmp_path / "projects", token=None)

    assert len(result["high"]) == 1
    assert result["high"][0]["repo"] == "silasfelinus/kind_robots"
    assert result["high"][0]["pr_number"] == 1464
    assert result["high"][0]["confidence"] == "high"
    assert result["high"][0]["source"] == "implementation-pr-field"
    assert result["weak"] == []
    assert result["unresolved"] == []


def test_check_drift_field_absent_still_uses_title_search(tmp_path):
    # Field-absent path: a task with no implementation_pr field (the common
    # case for tasks closed before this field existed) is unaffected and
    # still goes through the title-search pass exactly as before.
    write_roadmap(
        tmp_path,
        "newsfeed",
        [{"id": "t-020", "status": "claimed", "title": "x"}],
    )

    search_body = json.dumps({
        "items": [
            {
                "number": 1464,
                "repository_url": "https://api.github.com/repos/silasfelinus/kind_robots",
            }
        ]
    }).encode()
    pr_body = json.dumps({
        "merged": True,
        "merged_at": "2026-08-01T00:00:00Z",
        "title": "newsfeed/t-020: fix",
    }).encode()

    def fake_urlopen(req, timeout=10):
        url = req.full_url if hasattr(req, "full_url") else req
        if "search/issues" in url:
            return FakeResponse(search_body)
        return FakeResponse(pr_body)

    with patch("urllib.request.urlopen", side_effect=fake_urlopen):
        result = dr.check_drift(tmp_path / "projects", token=None)

    assert len(result["high"]) == 1
    assert result["high"][0]["source"] == "task-id-search"
    assert result["high"][0]["pr_number"] == 1464


def test_check_drift_field_lookup_failure_is_unresolved_not_downgraded(tmp_path):
    # A task whose implementation_pr field is present but whose PR lookup
    # itself fails must land in `unresolved` -- not fall back to the
    # title-search or note-reference passes (which would risk reporting a
    # false "clean" or a downgraded "weak" result for evidence that was
    # never actually checked).
    write_roadmap(
        tmp_path,
        "newsfeed",
        [
            {
                "id": "t-020",
                "status": "claimed",
                "title": "x",
                "implementation_pr": "silasfelinus/kind_robots#404",
                "note": "kind_robots PR #517",
            }
        ],
    )

    def fake_urlopen(req, timeout=10):
        url = req.full_url if hasattr(req, "full_url") else req
        assert "search/issues" not in url, "a field-present task must not fall back to search"
        raise http_error(404)

    with patch("urllib.request.urlopen", side_effect=fake_urlopen):
        result = dr.check_drift(tmp_path / "projects", token=None)

    assert result["high"] == []
    assert result["weak"] == []
    assert len(result["unresolved"]) == 1
    assert result["unresolved"][0]["task_id"] == "t-020"


def test_check_drift_malformed_field_is_unresolved_not_search_fallback(tmp_path):
    # Review finding on PR #1737 (conductor/t-099): a task whose
    # implementation_pr field is PRESENT but malformed (doesn't parse into
    # owner/repo#number, e.g. missing the owner) must be treated differently
    # from a task where the field is simply absent. It must land in
    # `unresolved` directly -- it must NOT fall through to the title-search
    # pass (that would silently replace stronger, task-authored-but-corrupt
    # evidence with a weaker heuristic and could return a false "clean"),
    # and it must NOT be confused with a task-id-search or PR-lookup failure.
    write_roadmap(
        tmp_path,
        "newsfeed",
        [
            {
                "id": "t-020",
                "status": "claimed",
                "title": "x",
                "implementation_pr": "kind_robots PR #1464",
                "note": "kind_robots PR #517",
            }
        ],
    )

    def fake_urlopen(req, timeout=10):
        url = req.full_url if hasattr(req, "full_url") else req
        raise AssertionError(
            f"a malformed implementation_pr field must never trigger any API call, got {url!r}"
        )

    with patch("urllib.request.urlopen", side_effect=fake_urlopen):
        result = dr.check_drift(tmp_path / "projects", token=None)

    assert result["high"] == []
    assert result["weak"] == []
    assert len(result["unresolved"]) == 1
    unresolved = result["unresolved"][0]
    assert unresolved["task_id"] == "t-020"
    assert unresolved["implementation_pr"] == "kind_robots PR #1464"
    assert "repo" not in unresolved
    assert "pr_number" not in unresolved


def test_render_labels_malformed_implementation_pr_distinctly(tmp_path):
    unresolved = [
        {
            "project": "newsfeed",
            "task_id": "t-020",
            "title": "x",
            "status": "claimed",
            "implementation_pr": "kind_robots PR #1464",
        }
    ]
    output = dr.render([], unresolved, total=1)
    assert "malformed implementation_pr field" in output
    assert "kind_robots PR #1464" in output


def test_render_does_not_mislabel_absent_field_task_as_malformed(tmp_path):
    # A search-failed task's dict carries implementation_pr=None (the key
    # exists, just falsy) -- render() must key on truthiness, not mere key
    # presence, or every ordinary search failure would misreport as a
    # "malformed implementation_pr field: None".
    unresolved = [
        {
            "project": "newsfeed",
            "task_id": "t-020",
            "title": "x",
            "status": "claimed",
            "implementation_pr": None,
        }
    ]
    output = dr.render([], unresolved, total=1)
    assert "malformed implementation_pr field" not in output
    assert "task-id search" in output


# --------------------------------------------------------------------------- #
# resolve_remaining_scope_chain / remaining_scope_resolved (conductor/t-108)
# --------------------------------------------------------------------------- #


def test_resolve_remaining_scope_chain_returns_none_with_no_pointer(tmp_path):
    write_roadmap(
        tmp_path,
        "digital-storefront",
        [{"id": "t-038", "status": "review", "title": "umbrella"}],
    )
    assert (
        dr.resolve_remaining_scope_chain(
            "digital-storefront", "t-038", tmp_path / "projects"
        )
        is None
    )


def test_resolve_remaining_scope_chain_follows_single_hop_to_done(tmp_path):
    write_roadmap(
        tmp_path,
        "digital-storefront",
        [
            {
                "id": "t-038",
                "status": "review",
                "title": "umbrella",
                "remaining_scope_task": "t-004",
            },
            {"id": "t-004", "status": "done", "title": "the real remaining scope"},
        ],
    )
    result = dr.resolve_remaining_scope_chain(
        "digital-storefront", "t-038", tmp_path / "projects"
    )
    assert result == {"chain": ["t-004"], "terminal_status": "done"}


def test_resolve_remaining_scope_chain_follows_multi_hop_chain(tmp_path):
    write_roadmap(
        tmp_path,
        "digital-storefront",
        [
            {
                "id": "t-038",
                "status": "review",
                "title": "umbrella",
                "remaining_scope_task": "t-004",
            },
            {
                "id": "t-004",
                "status": "review",
                "title": "sub-umbrella",
                "remaining_scope_task": "t-009",
            },
            {"id": "t-009", "status": "done", "title": "actual remaining scope"},
        ],
    )
    result = dr.resolve_remaining_scope_chain(
        "digital-storefront", "t-038", tmp_path / "projects"
    )
    assert result == {"chain": ["t-004", "t-009"], "terminal_status": "done"}


def test_resolve_remaining_scope_chain_reports_terminal_not_done(tmp_path):
    write_roadmap(
        tmp_path,
        "digital-storefront",
        [
            {
                "id": "t-038",
                "status": "review",
                "title": "umbrella",
                "remaining_scope_task": "t-004",
            },
            {"id": "t-004", "status": "claimed", "title": "still in progress"},
        ],
    )
    result = dr.resolve_remaining_scope_chain(
        "digital-storefront", "t-038", tmp_path / "projects"
    )
    assert result == {"chain": ["t-004"], "terminal_status": "claimed"}


def test_resolve_remaining_scope_chain_reports_missing_pointer(tmp_path):
    write_roadmap(
        tmp_path,
        "digital-storefront",
        [
            {
                "id": "t-038",
                "status": "review",
                "title": "umbrella",
                "remaining_scope_task": "t-999",
            }
        ],
    )
    result = dr.resolve_remaining_scope_chain(
        "digital-storefront", "t-038", tmp_path / "projects"
    )
    assert result == {"chain": ["t-999"], "terminal_status": None, "missing": "t-999"}


def test_resolve_remaining_scope_chain_reports_cycle(tmp_path):
    write_roadmap(
        tmp_path,
        "digital-storefront",
        [
            {
                "id": "t-038",
                "status": "review",
                "title": "umbrella",
                "remaining_scope_task": "t-004",
            },
            {
                "id": "t-004",
                "status": "review",
                "title": "loops back",
                "remaining_scope_task": "t-038",
            },
        ],
    )
    result = dr.resolve_remaining_scope_chain(
        "digital-storefront", "t-038", tmp_path / "projects"
    )
    assert result["cycle"] is True


def test_check_drift_flags_remaining_scope_resolved_without_network(tmp_path):
    # The umbrella task itself has no implementation_pr and no note-quoted PR
    # reference at all -- the title-search API call still runs (and, per this
    # fake, comes back empty), but remaining_scope_resolved must still surface
    # this task as likely-ready-to-close from roadmap data alone.
    write_roadmap(
        tmp_path,
        "digital-storefront",
        [
            {
                "id": "t-038",
                "status": "review",
                "title": "umbrella",
                "remaining_scope_task": "t-004",
            },
            {"id": "t-004", "status": "done", "title": "the real remaining scope"},
        ],
    )
    empty_search_body = json.dumps({"items": []}).encode()

    with patch("urllib.request.urlopen", return_value=FakeResponse(empty_search_body)):
        result = dr.check_drift(tmp_path / "projects", token=None)

    assert result["high"] == []
    assert result["weak"] == []
    assert result["unresolved"] == []
    assert len(result["remaining_scope_resolved"]) == 1
    resolved = result["remaining_scope_resolved"][0]
    assert resolved["project"] == "digital-storefront"
    assert resolved["task_id"] == "t-038"
    assert resolved["chain"] == ["t-004"]
    assert resolved["terminal_status"] == "done"


def test_check_drift_omits_remaining_scope_not_yet_done(tmp_path):
    write_roadmap(
        tmp_path,
        "digital-storefront",
        [
            {
                "id": "t-038",
                "status": "review",
                "title": "umbrella",
                "remaining_scope_task": "t-004",
            },
            {"id": "t-004", "status": "claimed", "title": "still in progress"},
        ],
    )
    empty_search_body = json.dumps({"items": []}).encode()

    with patch("urllib.request.urlopen", return_value=FakeResponse(empty_search_body)):
        result = dr.check_drift(tmp_path / "projects", token=None)

    assert result["remaining_scope_resolved"] == []


def test_render_flags_remaining_scope_resolved():
    resolved = [
        {
            "project": "digital-storefront",
            "task_id": "t-038",
            "status": "review",
            "chain": ["t-004"],
            "terminal_status": "done",
        }
    ]
    output = dr.render([], [], total=1, remaining_scope_resolved=resolved)
    assert "No drift found" not in output
    assert "likely ready to close" in output
    assert "digital-storefront/t-038" in output
    assert "t-004" in output


def test_render_clean_requires_no_remaining_scope_resolved():
    resolved = [
        {
            "project": "digital-storefront",
            "task_id": "t-038",
            "status": "review",
            "chain": ["t-004"],
            "terminal_status": "done",
        }
    ]
    output = dr.render([], [], total=1, weak=[], remaining_scope_resolved=resolved)
    assert "No drift found" not in output
