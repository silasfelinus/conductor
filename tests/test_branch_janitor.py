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
