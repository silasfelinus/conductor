"""The Fever Dream art reviewer produces evidence, never auto-approves images."""

import pytest
import yaml
from PIL import Image

import scripts.review_rainbow_doodle_art as reviewer
from rainbow_doodle_fixture import (
    make_doodle_subject as _write_subject,
    write_doodle_ledger as _write_ledger,
)


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


def test_cli_lists_edge_risk_sprite_and_artimage_id(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(
        reviewer.exporter,
        "key_green",
        lambda image: image.convert("RGBA"),
    )
    subjects = [
        _write_subject(tmp_path, "ships/halo-fin", 263272, green=False),
        _write_subject(tmp_path, "ships/petal-wing", 263273),
    ]
    ledger = _write_ledger(tmp_path, subjects)
    manifest = reviewer.generate_review(
        tmp_path / "kind_robots",
        tmp_path / "review",
        tmp_path / "cache",
        offline=True,
        ledger=ledger,
    )
    assert [entry["edge_check"] for entry in manifest["assets"]] == [
        "edge-risk",
        "clear-border",
    ]
    monkeypatch.setattr(
        reviewer,
        "generate_review",
        lambda *_args, **_kwargs: manifest,
    )

    assert reviewer.main(["--offline"]) == 0
    output = capsys.readouterr().out
    assert "1 edge-risk sprite(s) need visual inspection:" in output
    assert "ships/halo-fin (ArtImage 263272)" in output
    assert "ships/petal-wing (ArtImage 263273)" not in output
    assert all(
        entry["verdict"] == "PENDING_VISUAL_INSPECTION"
        for entry in manifest["assets"]
    )
