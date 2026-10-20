from scripts import export_ecotone_art as exporter


def subject(asset, **art):
    return {"key": asset, "asset": asset, "art": {lane: {"status": status, "art_image_id": image_id}
                                                  for lane, (status, image_id) in art.items()}}


def fake_write(log):
    def write(image_id, path):
        log.append(image_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"webp")
    return write


def test_exports_finished_renders_per_style_and_writes_the_manifest(tmp_path):
    subjects = [
        subject("cards/kn-5", zimage=("DONE", 11), krea2=("PENDING", None)),
        subject("outcomes/kn-5/pedal-failure", zimage=("DONE", 12), arthemy=("DONE", 13)),
    ]
    fetched = []
    assert exporter.export(subjects, tmp_path, write=fake_write(fetched)) == 3
    assert sorted(fetched) == [11, 12, 13]
    assert (tmp_path / "public/ecotone/styles/zimage/outcomes/kn-5/pedal-failure.webp").exists()
    # A second run fetches nothing it already shipped.
    assert exporter.export(subjects, tmp_path, write=fake_write(fetched)) == 0

    styles = exporter.write_manifest(tmp_path)
    assert styles == {
        "arthemy": ["outcomes/kn-5/pedal-failure"],
        "zimage": ["cards/kn-5", "outcomes/kn-5/pedal-failure"],
    }
    manifest = (tmp_path / exporter.MANIFEST).read_text()
    assert "  zimage: [\n    'cards/kn-5',\n    'outcomes/kn-5/pedal-failure',\n  ]," in manifest
    assert "Do not edit by hand" in manifest


def test_withdrawn_render_is_removed_and_never_refetched(tmp_path):
    item = subject("endings/mara-sober-hope", novacomic=("DONE", 21))
    exporter.export([item], tmp_path, write=fake_write([]))
    item["withdrawn"] = {"novacomic": "same face as Kit"}
    refetched = []
    assert exporter.export([item], tmp_path, write=fake_write(refetched)) == 0
    assert refetched == []
    assert not (tmp_path / "public/ecotone/styles/novacomic/endings/mara-sober-hope.webp").exists()
    assert exporter.write_manifest(tmp_path) == {}
    assert "> = {}" in (tmp_path / exporter.MANIFEST).read_text()
