"""Shifting Desks packs must link each slot to the render the game shows.

projects/shifting-desks/encounters/link_art.py maps every pack slot to the path
kind_robots stationArt() requests and links it only when the latest art ledger
row for that path is delivered and was not sent back (t-015, 2026-10-20 PT).
"""

import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENC_DIR = ROOT / "projects" / "shifting-desks" / "encounters"

_spec = importlib.util.spec_from_file_location("shifting_desks_link_art", ENC_DIR / "link_art.py")
la = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(la)

_vspec = importlib.util.spec_from_file_location("shifting_desks_validate_pack_link", ENC_DIR / "validate_pack.py")
vp = importlib.util.module_from_spec(_vspec)
_vspec.loader.exec_module(vp)


def _pack(name="ORIENTATION-12.json"):
    return json.loads((ENC_DIR / name).read_text(encoding="utf-8"))


def _row(status="delivered", verdict="keep: on brief"):
    return {"status": status, "verdict": verdict, "key": "k", "_round": "ROUND-99.yaml"}


def test_committed_packs_agree_with_the_art_ledgers():
    assert la.main([]) == 0


def test_every_slot_maps_to_a_ledger_row():
    index = la.ledger_index()
    for name in la.PACKS:
        for label, _art, path in la.slots(_pack(name)):
            assert path in index, (name, label, path)


def test_slot_paths_follow_station_art():
    paths = {label: path for label, _art, path in la.slots(_pack("RECORDS-12.json"))}
    assert paths["department records"] == "/images/shifting-desks/departments/records.webp"
    assert paths["review the-form-that-requires-itself"] == (
        "/images/shifting-desks/cards/records/the-form-that-requires-itself.webp"
    )
    assert paths["window window-9-tuesday"] == "/images/shifting-desks/window/window-9-tuesday.webp"
    assert paths["applicant courier-from-four"] == "/images/shifting-desks/window/courier-from-four.webp"


def _index_for(pack, row):
    return {path: dict(row) for _label, _art, path in la.slots(pack)}


def test_write_links_accepted_renders_and_is_idempotent():
    pack = _pack()
    for _label, art, _path in la.slots(pack):
        art["status"], art["art_ref"] = "design-only", None
    index = _index_for(pack, _row())
    problems, linked = la.reconcile(pack, index, write=True)
    assert len(linked) == sum(1 for _ in la.slots(pack))
    for _label, art, path in la.slots(pack):
        assert (art["status"], art["art_ref"]) == ("verified-repository-art", path)
    once = copy.deepcopy(pack)
    assert la.reconcile(pack, index, write=False)[0] == []
    la.reconcile(pack, index, write=True)
    assert pack == once


def test_sent_back_or_pending_render_unlinks_the_slot():
    for row in (_row(verdict="redo: garbled lettering"), _row(status="requested", verdict=None), _row(status="delivered", verdict=None)):
        pack = _pack()
        for _label, art, path in la.slots(pack):
            art["status"], art["art_ref"] = "verified-repository-art", path
        index = _index_for(pack, row)
        problems, linked = la.reconcile(pack, index)
        assert linked == [] and problems and all("ledger says design-only" in p for p in problems)
        la.reconcile(pack, index, write=True)
        assert all(art["art_ref"] is None for _label, art, _path in la.slots(pack))


def test_missing_ledger_row_is_reported():
    pack = _pack()
    problems, _linked = la.reconcile(pack, {})
    assert problems and all("no art ledger row" in p for p in problems)


def test_later_round_supersedes_earlier(tmp_path):
    for n, status in ((2, "delivered"), (13, "requested")):
        (tmp_path / f"ROUND-{n}.yaml").write_text(
            "subjects:\n- key: x\n  target_path: kind_robots public/images/shifting-desks/cards/orientation/x.webp\n"
            f"  status: {status}\n  verdict: null\n",
            encoding="utf-8",
        )
    row = la.ledger_index(tmp_path)["/images/shifting-desks/cards/orientation/x.webp"]
    assert row["_round"] == "ROUND-13.yaml" and not la.accepted(row)


def test_validator_rejects_a_linked_slot_without_a_public_path(tmp_path):
    pack = _pack()
    pack["encounters"][0]["art"].update(status="verified-repository-art", art_ref="cards/orientation/x.png")
    path = tmp_path / "PACK.json"
    path.write_text(json.dumps(pack), encoding="utf-8")
    assert any("verified-repository-art needs art_ref" in e for e in vp.validate_pack(path))
