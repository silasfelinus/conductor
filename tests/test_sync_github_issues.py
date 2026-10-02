import yaml

import scripts.sync_github_issues as bridge

COL0_ROADMAP = """project: alpha
kind: software
milestones:
  - id: m1
    title: One
    status: in-progress
tasks:
- id: t-001
  title: "First"
  status: done
  note: |-
    keeps its
    block scalar

- id: t-003
  title: "Third"
  status: ready

goal: Keep alpha delightful.
"""

INDENTED_ROADMAP = """project: beta
kind: software
milestones:
  - id: m1
    title: One
    status: in-progress
tasks:
  - id: t-001
    title: First
    status: ready
"""


def _issue(number, title="Fix the thing", assoc="OWNER", labels=(), body="Details here."):
    return {
        "number": number,
        "title": title,
        "body": body,
        "author_association": assoc,
        "labels": [{"name": name} for name in labels],
        "html_url": f"https://github.com/o/r/issues/{number}",
        "user": {"login": "silas"},
        "created_at": "2026-09-12T11:09:15Z",
    }


def _fixture(tmp_path, monkeypatch, issues_by_repo, *, beta_status="active"):
    projects = tmp_path / "projects"
    for slug, text in (("alpha", COL0_ROADMAP), ("beta", INDENTED_ROADMAP)):
        (projects / slug).mkdir(parents=True)
        (projects / slug / "roadmap.yaml").write_text(text)
    (tmp_path / "repos.yaml").write_text(
        "repos:\n"
        "  - slug: alpha\n    repo: o/r\n"
        "  - slug: beta\n    repo: o/r\n"
        "  - slug: beta\n    repo: o/b\n"
    )
    (tmp_path / "project-overrides.yaml").write_text(
        f"overrides:\n  - slug: alpha\n    status: active\n  - slug: beta\n    status: {beta_status}\n"
    )
    monkeypatch.setattr(bridge, "PROJECTS_DIR", projects)
    monkeypatch.setattr(bridge, "REPOS_FILE", tmp_path / "repos.yaml")
    monkeypatch.setattr(bridge, "OVERRIDES_FILE", tmp_path / "project-overrides.yaml")
    monkeypatch.setattr(bridge, "fetch_open_issues", lambda repo, token: issues_by_repo.get(repo, []))
    return projects


def test_append_preserves_trailing_keys_and_block_scalars():
    entry = {"source": "o/r#7", "title": 'Quote "me": yes', "body": "line one\n\nline #3",
             "url": "u", "author": "silas", "created": "2026-09-12"}
    block = bridge.render_task(entry, "t-002", bridge.item_indent(COL0_ROADMAP), "2026-10-02")
    out = bridge.append_task_text(COL0_ROADMAP, block)
    doc = yaml.safe_load(out)
    assert doc["goal"] == "Keep alpha delightful."
    assert doc["tasks"][0]["note"] == "keeps its\nblock scalar"
    new = doc["tasks"][-1]
    assert new["id"] == "t-002" and new["status"] == "ready"
    assert new["source_issue"] == "o/r#7"
    assert new["title"] == 'Quote "me": yes'
    assert new["note"].endswith("line one\n\nline #3")
    assert out.startswith(COL0_ROADMAP.split("goal:")[0].rstrip("\n"))


def test_append_matches_indented_list_style():
    entry = {"source": "o/b#1", "title": "T", "body": "", "url": "u", "author": "a", "created": "d"}
    block = bridge.render_task(entry, "t-002", bridge.item_indent(INDENTED_ROADMAP), "2026-10-02")
    assert block.startswith("  - id: t-002")
    doc = yaml.safe_load(bridge.append_task_text(INDENTED_ROADMAP, block))
    assert [t["id"] for t in doc["tasks"]] == ["t-001", "t-002"]


def test_apply_imports_once_and_routes(tmp_path, monkeypatch):
    issues = {
        "o/r": [
            _issue(1),
            _issue(2, labels=["project:beta"]),
            _issue(3, labels=["conductor:skip"]),
            _issue(4, assoc="NONE", title="drive-by"),
            _issue(5, labels=["project:nope"]),
        ],
    }
    projects = _fixture(tmp_path, monkeypatch, issues)

    plan, roadmaps = bridge.build_plan(None, close_done=False)
    assert {e["source"]: e["project"] for e in plan.imports} == {
        "o/r#1": "alpha", "o/r#2": "beta", "o/r#5": "alpha"}
    assert [e["source"] for e in plan.untrusted] == ["o/r#4"]

    done = bridge.apply_imports(plan, roadmaps)
    alpha = yaml.safe_load((projects / "alpha" / "roadmap.yaml").read_text())
    # lowest free id fills the t-002 gap, then t-004
    assert {t["id"]: t.get("source_issue") for t in alpha["tasks"]} == {
        "t-001": None, "t-003": None, "t-002": "o/r#1", "t-004": "o/r#5"}
    assert len(done) == 3

    again, _ = bridge.build_plan(None, close_done=False)
    assert again.imports == []


def test_inactive_project_is_reported_not_imported(tmp_path, monkeypatch):
    _fixture(tmp_path, monkeypatch, {"o/b": [_issue(9)]}, beta_status="finished")
    plan, _ = bridge.build_plan(None, close_done=False)
    assert plan.imports == []
    assert [(e["source"], e["lifecycle"]) for e in plan.inactive] == [("o/b#9", "finished")]


def test_close_done_only_for_open_issue_with_done_task(tmp_path, monkeypatch):
    projects = _fixture(tmp_path, monkeypatch, {"o/r": [_issue(1), _issue(2)]})
    path = projects / "alpha" / "roadmap.yaml"
    path.write_text(path.read_text().replace(
        'title: "First"\n  status: done',
        'title: "First"\n  status: done\n  source_issue: "o/r#1"').replace(
        'title: "Third"\n  status: ready',
        'title: "Third"\n  status: ready\n  source_issue: "o/r#2"'))
    plan, _ = bridge.build_plan(None, close_done=True)
    assert plan.imports == []
    assert [(e["source"], e["task"]) for e in plan.close] == [("o/r#1", "t-001")]


def test_check_mode_exit_codes(tmp_path, monkeypatch):
    _fixture(tmp_path, monkeypatch, {})
    assert bridge.main([]) == 0
    _fixture_dir = tmp_path / "second"
    _fixture_dir.mkdir()
    _fixture(_fixture_dir, monkeypatch, {"o/r": [_issue(1)]})
    assert bridge.main(["--check"]) == 1


def test_long_body_is_truncated_with_link():
    entry = {"source": "o/r#1", "title": "T", "body": "x" * (bridge.BODY_LIMIT + 50),
             "url": "https://example/1", "author": "a", "created": "d"}
    note = bridge.task_note(entry)
    assert "truncated" in note and "https://example/1" in note
    assert len(note) < bridge.BODY_LIMIT + 600


def test_apply_then_comment_from_handoff(tmp_path, monkeypatch):
    _fixture(tmp_path, monkeypatch, {"o/r": [_issue(1)]})
    out = tmp_path / "imported.json"
    assert bridge.main(["--apply", "--imported-json", str(out)]) == 0
    calls = []
    monkeypatch.setattr(bridge, "gh", lambda method, path, token, body=None, params=None: calls.append((method, path, body)))
    monkeypatch.setenv("ISSUE_BRIDGE_TOKEN", "x")
    assert bridge.main(["--comment-from", str(out)]) == 0
    assert len(calls) == 1
    method, path, body = calls[0]
    assert (method, path) == ("POST", "repos/o/r/issues/1/comments")
    assert "alpha/t-002" in body["body"]
