import json
import sys

import pytest
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
    assert [dest.name for _s, _i, dest in todo] == ["a.webp", "b.webp"]
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
        path.write_bytes(b"RIFF" + b"\x10\x00\x00\x00" + b"WEBP" + b"VP8 " + b"\x00" * 8)
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


def test_rejected_renders_never_ship_and_strict_mode_requires_keep(tmp_path):
    kept = subject("quests/keeper")
    kept["verdict"] = "keep: on model"
    rejected = subject("quests/rejected")
    rejected["verdict"] = "reject: human rider"
    unreviewed = subject("quests/unreviewed")
    subjects = [kept, rejected, unreviewed]

    ordinary = era.plan(subjects, tmp_path, "emperor-of-dust")
    assert [dest.name for _subject, _id, dest in ordinary] == [
        "keeper.webp", "unreviewed.webp"
    ]
    strict = era.plan(
        subjects, tmp_path, "emperor-of-dust", require_keep=True
    )
    assert [dest.name for _subject, _id, dest in strict] == ["keeper.webp"]



def test_curator_lane_acceptance_allows_strict_export_without_text_verdict(tmp_path):
    rendered = subject("ship/pocket-room", status="ACCEPTED", image=277778)
    unreviewed = subject("ship/other", status="DONE", image=277779)

    assert era.finished(rendered) == 277778
    assert era.plan([rendered, unreviewed], tmp_path, "game-of-captains",
                    require_keep=True) == [
        (rendered, 277778, tmp_path / "public/game-of-captains/ship/pocket-room.webp"),
    ]
    report = era.audit([rendered, unreviewed], tmp_path, "game-of-captains",
                       require_keep=True)
    assert report["counts"] == {"curation-needed": 1, "export-ready": 1}


def test_curator_lane_reject_blocks_export_even_with_stale_keep_verdict(tmp_path):
    rejected = subject("ship/bad-anatomy", status="REJECTED", image=277780)
    rejected["verdict"] = "keep: outdated verdict from earlier attempt"
    untouched = subject("ship/unreviewed", status="DONE", image=277781)

    assert era.finished(rejected) is None
    for strict in (False, True):
        assert rejected not in [
            item for item, _image, _dest in era.plan(
                [rejected, untouched], tmp_path, "game-of-captains",
                require_keep=strict,
            )
        ]
    report = era.audit([rejected, untouched], tmp_path, "game-of-captains",
                       require_keep=True)
    assert report["counts"] == {"curation-needed": 1, "rejected": 1}

def test_sheet_generates_review_without_export_or_token(tmp_path, monkeypatch):
    import export_crystal_street_art as crystal

    ledger = tmp_path / "round.yaml"
    ledger.write_text(
        "subjects:\n"
        "- asset: quests/keeper\n"
        "  art: {lane: {status: DONE, art_image_id: 270430}}\n"
        "- asset: rooms/skip\n"
        "  art: {lane: {status: DONE, art_image_id: 270431}}\n"
    )
    called = []

    def capture(subjects, out, thumb):
        called.append(([subject["asset"] for subject in subjects], out, thumb))

    monkeypatch.setattr(crystal, "contact_sheet", capture)
    result = era.main([
        str(ledger), "--kind-robots", str(tmp_path),
        "--only", "^quests/", "--sheet", str(tmp_path / "review.jpg"),
    ])
    assert result == 0
    assert called == [(
        ["quests/keeper"], str(tmp_path / "review.jpg"), (220, 145)
    )]
    assert not (tmp_path / "public").exists()


def test_valid_webp_is_not_reexported_without_force(tmp_path):
    image = tmp_path / "public" / "game" / "cast" / "a.webp"
    image.parent.mkdir(parents=True)
    image.write_bytes(b"RIFF" + b"\x10\x00\x00\x00" + b"WEBP" + b"VP8 " + b"\x00" * 8)
    assert era.is_valid_webp(image)
    assert era.plan([subject("cast/a")], tmp_path, "game") == []
    assert len(era.plan([subject("cast/a")], tmp_path, "game", force=True)) == 1


def test_audit_distinguishes_exported_corrupt_rejected_pending_and_review(tmp_path):
    root = tmp_path / "public" / "emperor-of-dust" / "endings"
    root.mkdir(parents=True)
    (root / "ready.webp").write_bytes(
        b"RIFF" + b"\x10\x00\x00\x00" + b"WEBP" + b"VP8 " + b"\x00" * 8
    )
    (root / "broken.webp").write_bytes(b"not an image")
    ready = subject("endings/ready", image=270430)
    ready["verdict"] = "keep: on model"
    broken = subject("endings/broken", image=270431)
    broken["verdict"] = "keep: valid scene"
    missing = subject("endings/missing", image=270432)
    missing["verdict"] = "keep"
    unreviewed = subject("endings/unreviewed", image=270433)
    rejected = subject("endings/rejected", image=270434)
    rejected["verdict"] = "reject: off model"
    pending = subject("endings/pending", status="FAILED", image=0)
    report = era.audit(
        [ready, broken, missing, unreviewed, rejected, pending],
        tmp_path, "emperor-of-dust", require_keep=True,
    )
    assert report["counts"] == {
        "corrupt": 1,
        "curation-needed": 1,
        "export-ready": 1,
        "rejected": 1,
        "render-pending": 1,
        "shipped": 1,
    }
    assert report["total"] == 6
    assert report["rows"][0]["art_image_id"] == 270430
    assert report["rows"][0]["path"].endswith("endings/ready.webp")


def test_audit_flags_competing_render_ids_for_same_unshipped_asset(tmp_path):
    old = subject("endings/iron-peace", image=270432)
    new = subject("endings/iron-peace", image=270531)
    assert era.audit([old, new], tmp_path, "emperor-of-dust")["counts"] == {
        "collision": 2
    }
    old["verdict"] = "reject: wrong scene"
    new["verdict"] = "keep: verified"
    assert era.audit([old, new], tmp_path, "emperor-of-dust")["counts"] == {
        "export-ready": 1,
        "rejected": 1,
    }


@pytest.mark.parametrize("asset", ["../escape", "portraits/../../escape", r"faces\\bad"])
def test_export_rejects_path_traversal_or_windows_separators(tmp_path, asset):
    with pytest.raises(ValueError, match="Unsafe art asset"):
        era.target(tmp_path, "emperor-of-dust", asset)


def test_offline_audit_cli_never_fetches_render_bytes(tmp_path, capsys):
    ledger = tmp_path / "round.yaml"
    ledger.write_text(
        "subjects:\n"
        "- asset: endings/open-roads\n"
        "  key: eod-ending-open-roads\n"
        "  jobs: {arthemy-house: 68221}\n"
        "  art: {arthemy-house: {status: DONE, art_image_id: 270431}}\n"
    )
    assert era.main([
        str(ledger), "--kind-robots", str(tmp_path),
        "--prefix", "emperor-of-dust", "--audit",
    ]) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["counts"] == {"export-ready": 1}
    assert report["rows"][0]["art_job_ids"] == [68221]
    assert report["rows"][0]["art_image_id"] == 270431


def test_plan_fails_closed_on_concurrent_conflicting_render_ids(tmp_path):
    a = subject("endings/bell-restored", image=270430)
    b = subject("endings/bell-restored", image=270531)
    with pytest.raises(ValueError, match="Competing DONE renders"):
        era.plan([a, b], tmp_path, "emperor-of-dust")
    assert len(era.plan([a, dict(a)], tmp_path, "emperor-of-dust")) == 1


def test_manifest_excludes_corrupted_files(tmp_path):
    root = tmp_path / "public" / "emperor-of-dust" / "endings"
    root.mkdir(parents=True)
    (root / "missing.webp").write_bytes(b"corrupt")
    (root / "valid.webp").write_bytes(
        b"RIFF" + b"\x10\x00\x00\x00" + b"WEBP" + b"VP8 " + b"\x00" * 8
    )
    assert era.manifest_entries(tmp_path, "emperor-of-dust/endings") == ["valid"]
