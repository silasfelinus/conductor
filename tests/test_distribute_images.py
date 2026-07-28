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


def test_kind_robots_target_retained_not_pruned(tmp_path, monkeypatch):
    """A kind_robots-targeted request must never be copied into a local
    checkout or pruned from art-prompts.yaml, even when a kind_robots checkout
    happens to exist locally — public/images/** is git-ignored there and
    delivery goes through the relay's direct media path, not git. Copying it
    in used to look like delivery and silently drop the pending-request
    record with no trace of the file ever needing real delivery (conductor
    ai-art-academy/t-010, 2026-07-27)."""
    process_dir = tmp_path / "conductor" / "projects" / "process"
    process_dir.mkdir(parents=True)
    src = process_dir / "test-style.webp"
    src.write_bytes(b"fake-image-bytes")

    art_prompts = tmp_path / "conductor" / "projects" / "art-prompts.yaml"
    art_prompts.write_text(
        "images: []\n"
        "requests:\n"
        "- id: kind-robots-academy-style-preview-test-style\n"
        "  source: ai-art-academy-style-preview\n"
        "  status: done\n"
        "  target_repo: silasfelinus/kind_robots\n"
        "  image_path: public/images/academy/styles/test-style.webp\n"
        "  variant: image\n"
        "  size: 256x256\n"
        "  label: 'Academy style preview: Test Style'\n"
        "  prompt: 'a test style preview prompt'\n"
    )

    kr = tmp_path / "kind_robots"
    (kr / "public" / "images").mkdir(parents=True)

    monkeypatch.setattr(di, "REPO_ROOT", tmp_path / "conductor")
    monkeypatch.setattr(di, "PROCESS_DIR", process_dir)
    monkeypatch.setattr(di, "UNMATCHED_DIR", process_dir / "unmatched")
    monkeypatch.setattr(di, "ART_GENERATE_FILE", tmp_path / "conductor" / "projects" / "art-generate.yaml")
    monkeypatch.setattr(di, "ART_PROMPTS_FILE", art_prompts)
    monkeypatch.setattr(di, "KIND_ROBOTS_ROOT", kr)
    monkeypatch.setattr(di, "DRY_RUN", False)

    di.distribute()

    # File stays put -- never copied into the kind_robots checkout.
    assert src.exists()
    assert not (kr / "public" / "images" / "academy" / "styles" / "test-style.webp").exists()

    # The request record survives untouched -- distribute() must not prune it.
    assert "kind-robots-academy-style-preview-test-style" in art_prompts.read_text()


def test_record_project_art_provenance_writes_manifest(tmp_path, monkeypatch):
    manifest_path = tmp_path / "conductor" / "projects" / "images" / "manifest.json"
    monkeypatch.setattr(di, "REPO_ROOT", tmp_path / "conductor")
    monkeypatch.setattr(di, "PROJECT_ART_MANIFEST", manifest_path)
    monkeypatch.setattr(di, "DRY_RUN", False)

    match = {
        "image_path": "projects/images/coat-dance-icon.webp",
        "target_repo": "silasfelinus/conductor",
        "slug": "coat-dance",
        "variant": "icon",
        "prompt": "a friendly coat mid-dance, studio lighting",
        "model": None,
        "source": "art-prompts.yaml:images",
    }
    di.record_project_art_provenance("coat-dance-icon.webp", match, {"coat-dance"})

    manifest = json.loads(manifest_path.read_text())
    entry = manifest["coat-dance-icon.webp"]
    assert entry["slug"] == "coat-dance"
    assert entry["variant"] == "icon"
    assert entry["prompt"] == "a friendly coat mid-dance, studio lighting"
    assert entry["source"] == "art-prompts.yaml:images"
    assert "landed_at" in entry

    # A second, unrelated file merges into the existing manifest rather than
    # clobbering it.
    other_match = {
        "image_path": "projects/images/wishmaster-hero.webp",
        "target_repo": "silasfelinus/conductor",
        "slug": "wishmaster",
        "variant": "hero",
        "prompt": "a genie lamp granting a small wish",
        "model": None,
        "source": "art-generate.yaml:batch",
    }
    di.record_project_art_provenance("wishmaster-hero.webp", other_match, {"coat-dance", "wishmaster"})
    manifest = json.loads(manifest_path.read_text())
    assert set(manifest) == {"coat-dance-icon.webp", "wishmaster-hero.webp"}


def test_record_project_art_provenance_skips_non_conductor_and_non_project_art(tmp_path, monkeypatch):
    manifest_path = tmp_path / "conductor" / "projects" / "images" / "manifest.json"
    monkeypatch.setattr(di, "REPO_ROOT", tmp_path / "conductor")
    monkeypatch.setattr(di, "PROJECT_ART_MANIFEST", manifest_path)
    monkeypatch.setattr(di, "DRY_RUN", False)

    # kind_robots-targeted inspiration: not project icon/card/hero art.
    di.record_project_art_provenance(
        "flower-inspiration-1.webp",
        {"image_path": "public/images/flower/flower-inspiration-1.webp", "target_repo": "silasfelinus/kind_robots"},
        {"flower"},
    )
    # conductor-targeted but not under projects/images/ (e.g. a project inspiration mirror).
    di.record_project_art_provenance(
        "coat-dance-inspiration-1.webp",
        {"image_path": "projects/coat-dance/inspirations/coat-dance-inspiration-1.webp", "target_repo": "silasfelinus/conductor"},
        {"coat-dance"},
    )

    assert not manifest_path.exists()


def test_write_gallery_manifest_nested(tmp_path, monkeypatch):
    kr = make_images_tree(tmp_path)
    monkeypatch.setattr(di, "KIND_ROBOTS_ROOT", kr)

    di.write_gallery_manifest("dreams/coat-dance")
    manifest = json.loads(
        (kr / "public" / "images" / "dreams" / "coat-dance" / "gallery.json").read_text()
    )
    # write_gallery_manifest emits FULL filenames (with extension), not stems —
    # see the function docstring: the kind_robots reader appends .webp to any
    # bare stem, so entries must carry their real extension. (conductor #260)
    assert manifest == ["coat-dance-hero-1.webp"]
