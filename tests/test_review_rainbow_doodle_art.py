"""The Fever Dream art reviewer produces evidence, never auto-approves images."""

from pathlib import Path

import pytest
import yaml
from PIL import Image

import scripts.review_rainbow_doodle_art as reviewer


def _write_subject(root, rel, image_id, *, status="DONE", green=True):
    root = Path(root)
    if rel.startswith("portraits/"):
        classic = root / "kind_robots/public/rainbow-princess-portraits" / (
            rel.split("/", 1)[1] + ".webp"
        )
    else:
        classic = root / "kind_robots/public/rainbow-princess-art" / f"{rel}.webp"
    classic.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGBA", (64, 48), (120, 50, 200, 255)).save(classic, "WEBP")

    cached = root / "cache" / f"{rel}-{image_id}.png"
    cached.parent.mkdir(parents=True, exist_ok=True)
    matte = (0, 255, 0) if green else (200, 20, 60)
    render = Image.new("RGB", (64, 48), matte)
    for x in range(16, 48):
        for y in range(10, 38):
            render.putpixel((x, y), (180, 50, 200))
    render.save(cached)

    return {
        "asset": f"rainbow-princess-art/doodle/{rel}",
        "jobs": {"kontext": image_id - 200000},
        "art": {"kontext": {"status": status, "art_image_id": image_id}},
    }


def _write_ledger(root, subjects):
    ledger = Path(root) / "DOODLE-SET-2.yaml"
    ledger.write_text(yaml.safe_dump({"subjects": subjects}))
    return ledger


def test_matte_check_flags_a_cropped_non_green_edge():
    green = Image.new("RGB", (64, 48), (0, 255, 0))
    assert reviewer.clear_green_border(green)
    for x in range(64):
        green.putpixel((x, 0), (255, 0, 30))
    assert not reviewer.clear_green_border(green)


def test_review_builds_private_comparisons_and_pending_verdicts(tmp_path, monkeypatch):
    monkeypatch.setattr(
        reviewer.exporter,
        "key_green",
        lambda image: image.convert("RGBA"),
    )
    subjects = [
        _write_subject(tmp_path, "ships/halo-fin", 263272),
        _write_subject(tmp_path, "portraits/p3-solenne", 263269),
    ]
    ledger = _write_ledger(tmp_path, subjects)
    out = tmp_path / "review"
    manifest = reviewer.generate_review(
        tmp_path / "kind_robots",
        out,
        tmp_path / "cache",
        offline=True,
        ledger=ledger,
    )

    assert len(manifest["assets"]) == 2
    assert manifest["sheets"] == ["cast.webp", "ships.webp"]
    assert all(item["verdict"] == "PENDING_VISUAL_INSPECTION" for item in manifest["assets"])
    assert manifest["assets"][0]["edge_check"] == "clear-border"
    assert manifest["assets"][1]["edge_check"] == "not-a-sprite"
    assert (out / "ships.webp").is_file()
    assert (out / "cast.webp").is_file()
    assert yaml.safe_load((out / "visual-review.yaml").read_text())["status"] == (
        "PENDING_VISUAL_INSPECTION"
    )


def test_review_refuses_unfinished_images_before_creating_a_sheet(tmp_path):
    subject = _write_subject(
        tmp_path, "ships/halo-fin", 263272, status="RUNNING"
    )
    ledger = _write_ledger(tmp_path, [subject])
    out = tmp_path / "review"

    with pytest.raises(RuntimeError, match="not DONE"):
        reviewer.generate_review(
            tmp_path / "kind_robots",
            out,
            tmp_path / "cache",
            offline=True,
            ledger=ledger,
        )
    assert not out.exists()


def test_review_offline_fails_closed_for_uncached_art(tmp_path):
    subject = _write_subject(tmp_path, "ships/halo-fin", 263272)
    ledger = _write_ledger(tmp_path, [subject])
    (tmp_path / "cache/ships/halo-fin-263272.png").unlink()
    out = tmp_path / "review"

    with pytest.raises(FileNotFoundError, match="missing cached ArtImage"):
        reviewer.generate_review(
            tmp_path / "kind_robots",
            out,
            tmp_path / "cache",
            offline=True,
            ledger=ledger,
        )
    assert not out.exists()
