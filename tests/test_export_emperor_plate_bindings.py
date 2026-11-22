"""export_emperor_plate_bindings: only shipped keepers bind; rejects and missing files never do."""
from pathlib import Path

import yaml

from scripts.export_emperor_plate_bindings import collect, render


def _ledger(tmp: Path, subjects):
    (tmp / "art").mkdir(exist_ok=True)
    (tmp / "art" / "L.yaml").write_text(yaml.safe_dump({"subjects": subjects}))


def _ship(kr: Path, asset: str):
    path = kr / "public" / "emperor-of-dust" / f"{asset}.webp"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"RIFF....WEBP")


def test_bindings(tmp_path):
    kr = tmp_path / "kr"
    subjects = [
        {"asset": "chance-events/e-1/notice", "verdict": "keep"},
        {"asset": "chance-events/e-1/care", "verdict": "reject: human"},
        {"asset": "chance-events/e-2/notice", "verdict": "keep"},  # not shipped
        {"asset": "audiences/a-enter", "audience": "a", "variant": "entrance", "verdict": "keep"},
        {"asset": "audiences/a/opt", "audience": "a", "option": "opt", "verdict": "keep"},
        {"asset": "audiences/q-partial", "quest": "q-1", "variant": "partial", "verdict": "keep"},
        {"asset": "endings/long-night", "verdict": "keep"},
        {"asset": "endings/iron-peace"},  # no verdict: not curated
    ]
    _ledger(tmp_path, subjects)
    for s in subjects:
        _ship(kr, s["asset"]) if s["asset"] != "chance-events/e-2/notice" else None
    b = collect(tmp_path / "art", kr)
    assert b["chance"] == ["e-1/notice"]
    assert b["audience"] == {"a:opt": "a/opt", "a:scene": "a-enter"}
    assert b["quest"] == {"q-1:partial": "q-partial"}
    assert b["ending"] == ["long-night"]
    text = render(b)
    assert "export const CHANCE_PLATES" in text and "'a:scene': 'a-enter'," in text
