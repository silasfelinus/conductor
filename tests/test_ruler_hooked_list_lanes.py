"""ruler-hooked/t-037: --list-lanes summary for build_ruler_hooked_art_queue.py."""
import sys

import pytest

import scripts.build_ruler_hooked_art_queue as bruq


FAKE = {
    "concept": ["c1", "c2"],
    "alt": [],
    "ruler": ["r1"],
    "fish": ["f1", "f2", "f3"],
    "reward": [],
    "ending": ["e1"],
    "card": ["k1"],
}
STAGED = ["c1", "f2", "k1"]


def _entries(lane, ids):
    return [{"id": i, "lane": lane, "size": "1x1"} for i in ids]


@pytest.fixture(autouse=True)
def hermetic(monkeypatch, tmp_path):
    """CI has no kind_robots checkout, so stub every source of entries."""
    monkeypatch.setattr(bruq, "find_content_bundle", lambda: tmp_path / "content.ts")
    monkeypatch.setattr(bruq, "read_cast", lambda ts: None)
    monkeypatch.setattr(bruq, "read_regions", lambda ts: None)
    monkeypatch.setattr(bruq, "alt_vista_entries", lambda: [])
    monkeypatch.setattr(bruq, "concept_entries", lambda cast: _entries("concept", FAKE["concept"]))
    monkeypatch.setattr(bruq, "ruler_entries", lambda: _entries("ruler", FAKE["ruler"]))
    monkeypatch.setattr(bruq, "fish_entries", lambda: _entries("fish", FAKE["fish"]))
    monkeypatch.setattr(bruq, "reward_entries", lambda ts: [])
    monkeypatch.setattr(bruq, "ending_entries", lambda ts: _entries("ending", FAKE["ending"]))
    monkeypatch.setattr(bruq, "card_entries", lambda ts: _entries("card", FAKE["card"]))
    monkeypatch.setattr(bruq, "layer_entries", lambda regions: _entries("layer", ["l1", "l2"]))
    monkeypatch.setattr(bruq, "assert_contract", lambda entries: None)
    monkeypatch.setattr(bruq, "staged_ids", lambda text: set(STAGED))
    art = tmp_path / "art-prompts.yaml"
    art.write_text("stub\n", encoding="utf-8")
    monkeypatch.setattr(bruq, "ART_PROMPTS", art)


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
    assert rows["fish"] == (3, 1, 2)  # f2 staged; f1, f3 not
    assert rows["card"] == (1, 1, 0)


def test_list_lanes_never_writes(monkeypatch, capsys):
    def boom(*a, **k):
        raise AssertionError("--list-lanes must be read-only")

    path = bruq.ART_PROMPTS
    before = path.read_text(encoding="utf-8")
    with monkeypatch.context() as m:
        m.setattr(type(path), "write_text", boom)
        code, _ = _run(m, capsys, "--list-lanes", "--write")
    assert code == 0
    assert path.read_text(encoding="utf-8") == before


def test_list_lanes_rejects_lane(monkeypatch, capsys):
    with pytest.raises(SystemExit) as exc:
        _run(monkeypatch, capsys, "--list-lanes", "--lane", "fish")
    assert exc.value.code == 2


def test_list_lanes_layer_row_reflects_include_layers(monkeypatch, capsys):
    _, out = _run(monkeypatch, capsys, "--include-layers", "--list-lanes")
    assert _rows(out)["layer"] == (2, 0, 2)
