"""ruler-hooked/t-037: --list-lanes summary for build_ruler_hooked_art_queue.py."""
import sys

import pytest

import scripts.build_ruler_hooked_art_queue as bruq


def _run(monkeypatch, capsys, *argv):
    monkeypatch.setattr(sys, "argv", ["build_ruler_hooked_art_queue.py", *argv])
    code = bruq.main()
    return code, capsys.readouterr().out


def _rows(out):
    lines = [ln.split() for ln in out.splitlines()]
    return {r[0]: tuple(int(x) for x in r[1:]) for r in lines if len(r) == 4 and r[0] in bruq.LANES}


def test_lane_counts_splits_staged_and_unstaged():
    entries = [
        {"id": "a", "lane": "fish"},
        {"id": "b", "lane": "fish"},
        {"id": "c", "lane": "card"},
    ]
    rows = {lane: (s, u) for lane, s, u in bruq.lane_counts(entries, {"a", "c"})}
    assert rows["fish"] == (1, 1)
    assert rows["card"] == (1, 0)
    assert rows["layer"] == (0, 0)
    assert set(rows) == set(bruq.LANES)


def test_list_lanes_prints_every_lane_once_and_totals_add_up(monkeypatch, capsys):
    code, out = _run(monkeypatch, capsys, "--list-lanes")
    assert code == 0
    rows = _rows(out)
    assert set(rows) == set(bruq.LANES)
    for total, staged, unstaged in rows.values():
        assert staged + unstaged == total
    assert rows["layer"] == (0, 0, 0)


def test_list_lanes_never_writes(monkeypatch, capsys):
    def boom(*a, **k):
        raise AssertionError("--list-lanes must be read-only")

    monkeypatch.setattr(type(bruq.ART_PROMPTS), "write_text", boom)
    code, _ = _run(monkeypatch, capsys, "--list-lanes", "--write")
    assert code == 0


def test_list_lanes_rejects_lane(monkeypatch, capsys):
    with pytest.raises(SystemExit) as exc:
        _run(monkeypatch, capsys, "--list-lanes", "--lane", "fish")
    assert exc.value.code == 2


def test_list_lanes_layer_row_reflects_include_layers(monkeypatch, capsys):
    _, out = _run(monkeypatch, capsys, "--include-layers", "--list-lanes")
    total, staged, unstaged = _rows(out)["layer"]
    assert total > 0 and staged + unstaged == total
