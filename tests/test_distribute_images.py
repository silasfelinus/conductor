import json
from pathlib import Path

import scripts.distribute_images as di


def make_images_tree(tmp_path: Path) -> Path:
    """Fake kind_robots checkout with flat, nested, and legacy collections."""
    images = tmp_path / "kind_robots" / "public" / "images"
    # flat collection
    (images / "flower").mkdir(parents=True)
    (images / "flower" / "flower-inspiration-1.webp").write_bytes(b"x")
    # nested collection: dreams/coat-dance
    (images / "dreams" / "coat-dance").mkdir(parents=True)
    (images / "dreams" / "coat-dance" / "coat-dance-hero-1.webp").write_bytes(b"x")
    # legacy artcollections entry, shadowed by the flat folder above
    (images / "artcollections" / "flower").mkdir(parents=True)
    (images / "artcollections" / "flower" / "flower-inspiration-1.webp").write_bytes(b"x")
    # legacy-only entry
    (images / "artcollections" / "oldies").mkdir(parents=True)
    (images / "artcollections" / "oldies" / "oldies-inspiration-1.webp").write_bytes(b"x")
    return tmp_path / "kind_robots"


def test_slug_folder_rel_prefers_nested_then_flat(tmp_path, monkeypatch):
    kr = make_images_tree(tmp_path)
    monkeypatch.setattr(di, "KIND_ROBOTS_ROOT", kr)

    assert di.slug_folder_rel("coat-dance") == "dreams/coat-dance"
    assert di.slug_folder_rel("flower") == "flower"
    # unknown slug starts a new flat folder
    assert di.slug_folder_rel("brand-new") == "brand-new"


def test_next_numbered_path_iterates_within_owning_folder(tmp_path, monkeypatch):
    kr = make_images_tree(tmp_path)
    monkeypatch.setattr(di, "KIND_ROBOTS_ROOT", kr)

    # nested folder already holds hero-1 -> next hero is hero-2, same folder
    assert (
        di.next_numbered_path("coat-dance", "hero", ".webp")
        == "public/images/dreams/coat-dance/coat-dance-hero-2.webp"
    )
    # flat folder, new utility starts at 1
    assert (
        di.next_numbered_path("flower", "icon", ".webp")
        == "public/images/flower/flower-icon-1.webp"
    )
    # back-compat wrapper still speaks inspiration
    assert (
        di.next_inspiration_path("flower", ".webp")
        == "public/images/flower/flower-inspiration-2.webp"
    )


def test_slug_and_utility_from_dest_filename():
    slugs = {"flower", "coat-dance"}
    assert di.slug_and_utility_from_dest_filename("flower-icon.webp", slugs) == (
        "flower",
        "icon",
    )
    assert di.slug_and_utility_from_dest_filename(
        "coat-dance-inspiration-3.webp", slugs
    ) == ("coat-dance", "inspiration")
    assert di.slug_and_utility_from_dest_filename("coat-dance-hero-2.webp", slugs) == (
        "coat-dance",
        "hero",
    )
    # unknown shape preserves as inspiration
    assert di.slug_and_utility_from_dest_filename("mystery.webp", slugs) == (
        "mystery",
        "inspiration",
    )


def test_write_collections_index_precedence(tmp_path, monkeypatch):
    kr = make_images_tree(tmp_path)
    monkeypatch.setattr(di, "KIND_ROBOTS_ROOT", kr)

    di.write_collections_index()
    index = json.loads((kr / "public" / "images" / "collections.json").read_text())

    assert index["coat-dance"] == "dreams/coat-dance"  # nested wins
    assert index["flower"] == "flower"  # flat beats artcollections
    assert index["oldies"] == "artcollections/oldies"  # legacy-only fallback
    # context dirs with no direct images are not collections themselves
    assert "dreams" not in index


def test_write_gallery_manifest_nested(tmp_path, monkeypatch):
    kr = make_images_tree(tmp_path)
    monkeypatch.setattr(di, "KIND_ROBOTS_ROOT", kr)

    di.write_gallery_manifest("dreams/coat-dance")
    manifest = json.loads(
        (kr / "public" / "images" / "dreams" / "coat-dance" / "gallery.json").read_text()
    )
    assert manifest == ["coat-dance-hero-1"]
