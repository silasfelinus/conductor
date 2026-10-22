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
