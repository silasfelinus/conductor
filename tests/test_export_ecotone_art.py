from PIL import Image

from scripts import export_ecotone_art as exporter


def subject(asset, **art):
    return {"key": asset, "asset": asset, "art": {lane: {"status": status, "art_image_id": image_id}
                                                  for lane, (status, image_id) in art.items()}}


def test_exports_finished_renders_per_style_and_writes_the_manifest(tmp_path):
    subjects = [
        subject("cards/kn-5", zimage=("DONE", 11), krea2=("PENDING", None)),
        subject("outcomes/kn-5/pedal-failure", zimage=("DONE", 12), arthemy=("DONE", 13)),
    ]
    loaded = []

    def load(image_id):
        loaded.append(image_id)
        return Image.new("RGB", (100, 60), "yellow")

    assert exporter.export(subjects, tmp_path, load=load) == 3
    assert sorted(loaded) == [11, 12, 13]
    written = Image.open(tmp_path / "public/ecotone/styles/zimage/outcomes/kn-5/pedal-failure.webp")
    assert written.size == exporter.SIZE
    # A second run fetches nothing it already shipped.
    assert exporter.export(subjects, tmp_path, load=load) == 0

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
    exporter.export([item], tmp_path, load=lambda _id: Image.new("RGB", exporter.SIZE))
    item["withdrawn"] = {"novacomic": "same face as Kit"}
    assert exporter.export([item], tmp_path, load=lambda _id: 1 / 0) == 0
    assert not (tmp_path / "public/ecotone/styles/novacomic/endings/mara-sober-hope.webp").exists()
    assert exporter.write_manifest(tmp_path) == {}
    assert "> = {}" in (tmp_path / exporter.MANIFEST).read_text()
