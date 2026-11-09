import yaml

import scripts.sweep_art_ledgers as sweep

LANES = [{"key": "a", "engine": "zimage", "prompt": "prose"}, {"key": "b", "engine": "krea2", "prompt": "prose"}]


def _write(path, **data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False))
    return path


def test_only_opted_in_ledgers_are_found(tmp_path):
    subjects = [{"key": "s1", "prompt_prose": "x"}]
    on = _write(tmp_path / "projects/p/art/ON.yaml", auto_submit=True, lanes=LANES, subjects=subjects)
    _write(tmp_path / "projects/p/art/DRAFT.yaml", lanes=LANES, subjects=subjects)
    _write(tmp_path / "projects/p/art/STRING.yaml", auto_submit="true", lanes=LANES, subjects=subjects)
    _write(tmp_path / "projects/q/art/deep/ON2.yaml", auto_submit=True, lanes=LANES, subjects=subjects)
    _write(tmp_path / "projects/q/art/NOT-A-LEDGER.yaml", auto_submit=True, items=[1, 2])
    (tmp_path / "projects/q/art/BROKEN.yaml").write_text("auto_submit: [unclosed\n")

    found = sweep.find_ledgers(tmp_path)

    assert found == sorted([on, tmp_path / "projects/q/art/deep/ON2.yaml"])


def test_open_cells_respects_subject_lane_and_existing_jobs():
    data = {
        "lanes": LANES,
        "subjects": [
            {"key": "both-open"},
            {"key": "one-done", "jobs": {"a": 101}},
            {"key": "pinned-lane", "lane": "b"},
            {"key": "pinned-done", "lane": "a", "jobs": {"a": 7}},
        ],
    }
    assert sweep.open_cells(data) == 2 + 1 + 1 + 0


def test_dry_run_lists_without_token(tmp_path, monkeypatch, capsys):
    _write(tmp_path / "projects/p/art/ON.yaml", auto_submit=True, lanes=LANES, subjects=[{"key": "s1"}])
    monkeypatch.setattr(sweep, "ROOT", tmp_path)

    assert sweep.main([]) == 0
    assert "projects/p/art/ON.yaml: 2 open cell(s)" in capsys.readouterr().out


def test_live_sweep_survives_a_ledger_error_and_runs_high_priority_first(tmp_path, monkeypatch, capsys):
    # 2026-11-09: a read timeout in one ledger's status refresh aborted the whole
    # sweep, so later ledgers (Slime City's lizard round) were never submitted.
    import sys
    import types

    subjects = [{"key": "s1"}]
    low = _write(tmp_path / "projects/a/art/LOW.yaml", auto_submit=True, priority=1, lanes=LANES, subjects=subjects)
    broken = _write(tmp_path / "projects/b/art/BROKEN.yaml", auto_submit=True, priority=5, lanes=LANES, subjects=subjects)
    high = _write(tmp_path / "projects/z/art/HIGH.yaml", auto_submit=True, priority=620, lanes=LANES, subjects=subjects)
    calls = []

    def fake_main(argv):
        calls.append((argv[0], argv[1]))
        if argv[0] == str(broken) and argv[1] == "--status":
            raise TimeoutError("The read operation timed out")
        return 0

    monkeypatch.setitem(sys.modules, "enqueue_art_requests", types.SimpleNamespace(main=fake_main))
    monkeypatch.setattr(sweep, "ROOT", tmp_path)

    assert sweep.main(["--live"]) == 1
    out = capsys.readouterr().out
    assert "ERROR projects/b/art/BROKEN.yaml: TimeoutError" in out
    assert "swept 3 ledger(s), 1 with submission failures" in out
    assert [path for path, flag in calls if flag == "--live"] == [str(high), str(broken), str(low)]
    assert (str(low), "--status") in calls, "the sweep continues past a failing ledger"
