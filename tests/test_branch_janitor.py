import scripts.branch_janitor as bj


def _classify(branches, merged=(), ages=None, force=(), stale_hours=12.0):
    merged_set = set(merged)
    ages = ages or {}
    return bj.classify(
        branches,
        is_merged_fn=lambda b: b in merged_set,
        age_fn=lambda b: ages.get(b, 0.0),
        force_set=set(force),
        stale_hours=stale_hours,
    )


def test_merged_branch_is_delete_candidate():
    plan = _classify(["claude/a"], merged=["claude/a"])
    assert plan[bj.MERGED] == ["claude/a"]
    assert plan[bj.STRANDED] == [] and plan[bj.ACTIVE] == []


def test_unmerged_recent_branch_left_active():
    plan = _classify(["claude/a"], ages={"claude/a": 1.0}, stale_hours=12.0)
    assert plan[bj.ACTIVE] == ["claude/a"]
    assert plan[bj.MERGED] == [] and plan[bj.STRANDED] == []


def test_unmerged_old_branch_reported_not_deleted():
    plan = _classify(["claude/a"], ages={"claude/a": 48.0}, stale_hours=12.0)
    assert plan[bj.STRANDED] == ["claude/a"]
    # stranded work is never in the auto-delete tiers
    assert "claude/a" not in plan[bj.MERGED] and "claude/a" not in plan[bj.FORCE]


def test_force_overrides_everything():
    # even a recent, unmerged branch is force-deleted when named explicitly
    plan = _classify(["claude/a"], ages={"claude/a": 0.5}, force=["claude/a"])
    assert plan[bj.FORCE] == ["claude/a"]
    assert plan[bj.ACTIVE] == []


def test_force_takes_precedence_over_merged():
    plan = _classify(["claude/a"], merged=["claude/a"], force=["claude/a"])
    assert plan[bj.FORCE] == ["claude/a"] and plan[bj.MERGED] == []


def test_mixed_set_partitions_cleanly():
    plan = _classify(
        ["claude/merged", "claude/old", "claude/new", "worker/forced"],
        merged=["claude/merged"],
        ages={"claude/old": 99.0, "claude/new": 2.0, "worker/forced": 99.0},
        force=["worker/forced"],
        stale_hours=12.0,
    )
    assert plan[bj.MERGED] == ["claude/merged"]
    assert plan[bj.STRANDED] == ["claude/old"]
    assert plan[bj.ACTIVE] == ["claude/new"]
    assert plan[bj.FORCE] == ["worker/forced"]


def test_delete_branch_dry_run_is_noop_success(monkeypatch):
    called = {"ran": False}

    def _boom(*a, **k):
        called["ran"] = True
        raise AssertionError("must not shell out in dry-run")

    monkeypatch.setattr(bj.subprocess, "run", _boom)
    assert bj.delete_branch("claude/whatever", dry_run=True) is True
    assert called["ran"] is False


def test_main_dry_run_json_reports_plan(monkeypatch, capsys):
    monkeypatch.setattr(bj, "refresh_remotes", lambda: None)
    monkeypatch.setattr(bj, "list_remote_branches", lambda prefixes: ["claude/gone", "claude/keep"])
    monkeypatch.setattr(bj, "is_merged", lambda b, base="origin/main": b == "claude/gone")
    monkeypatch.setattr(bj, "branch_age_hours", lambda b, now=None: 1.0)

    rc = bj.main(["--dry-run", "--json"])
    out = capsys.readouterr().out
    assert rc == 0
    assert '"deleted"' in out and "claude/gone" in out
    assert "claude/keep" in out  # left active


def test_force_delete_bypasses_prefix_filter(monkeypatch, capsys):
    # A branch outside claude/*|worker/* (e.g. reviewer/*) named via --force-delete
    # must still be picked up, not silently dropped by the prefix scan.
    monkeypatch.setattr(bj, "refresh_remotes", lambda: None)
    monkeypatch.setattr(bj, "list_remote_branches", lambda prefixes: ["claude/keep"])
    monkeypatch.setattr(
        bj, "list_all_remote_branches",
        lambda: ["claude/keep", "reviewer/stray-branch"],
    )
    monkeypatch.setattr(bj, "is_merged", lambda b, base="origin/main": False)
    monkeypatch.setattr(bj, "branch_age_hours", lambda b, now=None: 1.0)

    rc = bj.main(["--dry-run", "--json", "--force-delete", "reviewer/stray-branch"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "reviewer/stray-branch" in out
    assert '"deleted"' in out


def test_force_delete_ignores_nonexistent_branch_name(monkeypatch, capsys):
    # A --force-delete name that doesn't actually exist as a remote branch must not
    # be fabricated into the plan.
    monkeypatch.setattr(bj, "refresh_remotes", lambda: None)
    monkeypatch.setattr(bj, "list_remote_branches", lambda prefixes: ["claude/keep"])
    monkeypatch.setattr(bj, "list_all_remote_branches", lambda: ["claude/keep"])
    monkeypatch.setattr(bj, "is_merged", lambda b, base="origin/main": False)
    monkeypatch.setattr(bj, "branch_age_hours", lambda b, now=None: 1.0)

    rc = bj.main(["--dry-run", "--json", "--force-delete", "reviewer/does-not-exist"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "reviewer/does-not-exist" not in out


def test_default_prefixes_cover_closeout_and_conductor_branches():
    assert "close/" in bj.DEFAULT_PREFIXES
    assert "conductor/" in bj.DEFAULT_PREFIXES


def test_retirement_requires_exact_sha_and_no_open_pr():
    entries = {"close/old": "a" * 40, "close/moved": "b" * 40, "close/review": "c" * 40}
    heads = {"close/old": "a" * 40, "close/moved": "d" * 40, "close/review": "c" * 40}
    allowed, skipped = bj.eligible_retirements(
        entries, set(heads),
        head_fn=lambda branch: heads[branch],
        open_heads={"close/review"},
    )
    assert allowed == {"close/old"}
    assert skipped == {"close/moved": "branch head changed", "close/review": "open PR"}


def test_retirement_fails_closed_when_pr_api_unavailable():
    allowed, skipped = bj.eligible_retirements(
        {"close/old": "a" * 40}, {"close/old"},
        head_fn=lambda _: "a" * 40, open_heads=None,
    )
    assert allowed == set()
    assert skipped["close/old"] == "open PR lookup unavailable"


def test_retirement_manifest_rejects_unsafe_entries(tmp_path):
    import json
    import pytest
    f = tmp_path / "retirements.json"
    f.write_text(json.dumps({"version": 1, "retirements": {"main": "a" * 40}}))
    with pytest.raises(ValueError, match="Invalid branch retirement"):
        bj.read_retirements(f)


def test_delete_uses_exact_remote_head_lease(monkeypatch):
    calls = []
    monkeypatch.setattr(bj, "git", lambda *args: "a" * 40)
    class Result:
        returncode = 0
    monkeypatch.setattr(bj.subprocess, "run", lambda *a, **k: (calls.append(a), Result())[1])
    assert bj.delete_branch("close/old", False)
    argv = calls[0][0]
    assert "--force-with-lease=refs/heads/close/old:" + "a" * 40 in argv
