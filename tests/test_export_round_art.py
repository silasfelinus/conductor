import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import export_round_art as era


def subject(asset, status="DONE", image=7):
    return {"asset": asset, "art": {"lane": {"status": status, "art_image_id": image}}}


def test_plan_skips_unfinished_existing_and_unmatched(tmp_path):
    existing = tmp_path / "public" / "game" / "cast" / "a.webp"
    existing.parent.mkdir(parents=True)
    existing.write_bytes(b"x")
    subjects = [
        subject("cast/a"),
        subject("cast/b"),
        subject("cast/c", status="FAILED"),
        subject("props/d"),
    ]
    todo = era.plan(subjects, tmp_path, "game", only=r"^cast/")
    assert [dest.name for _s, _i, dest in todo] == ["b.webp"]
    forced = era.plan(subjects, tmp_path, "game", only=r"^cast/", force=True)
    assert [dest.name for _s, _i, dest in forced] == ["a.webp", "b.webp"]


def test_target_without_prefix_uses_asset_path(tmp_path):
    assert era.target(tmp_path, "", "game-of-captains/portraits/crew-pell") == (
        tmp_path / "public" / "game-of-captains" / "portraits" / "crew-pell.webp"
    )


def test_manifest_replaces_only_the_named_array(tmp_path):
    root = tmp_path / "public" / "eod" / "cast"
    for name in ("followers/F001/portrait/neutral", "followers/F021/portrait/neutral"):
        path = root / f"{name}.webp"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"x")
    ts = tmp_path / "castArt.ts"
    ts.write_text(
        "// header\nexport const CAST_ART: readonly string[] = [\n  'old',\n]\n\n"
        "export const castArtUrl = (asset: string) => asset\n"
    )
    entries = era.manifest_entries(tmp_path, "eod/cast")
    assert entries == ["followers/F001/portrait/neutral", "followers/F021/portrait/neutral"]
    era.write_manifest(ts, "CAST_ART", entries, "// unused")
    text = ts.read_text()
    assert "'old'" not in text and "'followers/F021/portrait/neutral'," in text
    assert text.startswith("// header") and "castArtUrl" in text


def test_manifest_writes_a_new_file(tmp_path):
    ts = tmp_path / "utils" / "artManifest.ts"
    era.write_manifest(ts, "WARP_ART", ["portraits/crew-pell"], "// generated")
    assert ts.read_text() == (
        "// generated\n\nexport const WARP_ART: readonly string[] = [\n  'portraits/crew-pell',\n]\n"
    )
