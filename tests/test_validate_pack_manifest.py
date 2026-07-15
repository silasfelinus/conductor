from pathlib import Path

import pytest

import scripts.validate_pack_manifest as validate_pack_manifest


@pytest.fixture(autouse=True)
def _isolate_packs_dir(tmp_path, monkeypatch):
    packs_dir = tmp_path / "packs"
    packs_dir.mkdir()
    monkeypatch.setattr(validate_pack_manifest, "PACKS_DIR", packs_dir)
    return packs_dir


VALID_MANIFEST = """
schemaVersion: 1
id: starter-sampler
title: Starter Sampler
description: A tiny sample pack.
owner: silas
visibility: draft
price:
  hook: free
items:
  - id: sample-location
    type: location
    itemShape: dream
    draftPayload:
      title: The Lantern Archive
      description: A drifting library-ship.
      generationPrompt: Write a location description.
      artPrompt: A library-ship illustration.
"""


def write_manifest(dir_: Path, name: str, text: str) -> Path:
    path = dir_ / name
    path.write_text(text, encoding="utf-8")
    return path


def test_valid_manifest_passes(_isolate_packs_dir, capsys):
    write_manifest(_isolate_packs_dir, "starter-sampler.yaml", VALID_MANIFEST)

    assert validate_pack_manifest.main([]) == 0
    assert "OK: 1 pack manifest(s) valid" in capsys.readouterr().out


def test_real_example_starter_pack_passes():
    example = Path(__file__).resolve().parents[1] / "projects" / "packmaker" / "packs" / "example-starter-pack.yaml"
    errors = validate_pack_manifest.validate_manifest(example)
    assert errors == []


def test_missing_top_level_fields_fail(_isolate_packs_dir, capsys):
    write_manifest(
        _isolate_packs_dir,
        "broken.yaml",
        "schemaVersion: 1\nid: broken\nitems: []\n",
    )

    assert validate_pack_manifest.main([]) == 1
    err = capsys.readouterr().err
    assert "'title' must be a non-empty string" in err
    assert "'owner' must be a non-empty string" in err
    assert "'visibility' must be one of" in err
    assert "'price' must be a mapping" in err
    assert "'items' must be a non-empty list" in err


def test_unknown_schema_version_fails(_isolate_packs_dir, capsys):
    write_manifest(
        _isolate_packs_dir,
        "future.yaml",
        VALID_MANIFEST.replace("schemaVersion: 1", "schemaVersion: 2"),
    )

    assert validate_pack_manifest.main([]) == 1
    assert "'schemaVersion' must be one of" in capsys.readouterr().err


def test_item_missing_draft_payload_without_ref_id_fails(_isolate_packs_dir, capsys):
    manifest = VALID_MANIFEST.replace(
        "    draftPayload:\n      title: The Lantern Archive\n      description: A drifting library-ship.\n      generationPrompt: Write a location description.\n      artPrompt: A library-ship illustration.\n",
        "",
    )
    write_manifest(_isolate_packs_dir, "no-payload.yaml", manifest)

    assert validate_pack_manifest.main([]) == 1
    assert "'draftPayload' is required while 'refId' is unset" in capsys.readouterr().err


def test_item_with_ref_id_may_omit_draft_payload(_isolate_packs_dir, capsys):
    manifest = VALID_MANIFEST.replace(
        "    itemShape: dream\n",
        "    itemShape: dream\n    refId: 42\n",
    ).replace(
        "    draftPayload:\n      title: The Lantern Archive\n      description: A drifting library-ship.\n      generationPrompt: Write a location description.\n      artPrompt: A library-ship illustration.\n",
        "",
    )
    write_manifest(_isolate_packs_dir, "generated.yaml", manifest)

    assert validate_pack_manifest.main([]) == 0


def test_invalid_item_type_fails(_isolate_packs_dir, capsys):
    manifest = VALID_MANIFEST.replace("type: location", "type: vehicle")
    write_manifest(_isolate_packs_dir, "bad-type.yaml", manifest)

    assert validate_pack_manifest.main([]) == 1
    assert "'type' must be one of" in capsys.readouterr().err


def test_invalid_yaml_fails(_isolate_packs_dir, capsys):
    write_manifest(_isolate_packs_dir, "invalid.yaml", "id: [unterminated\n")

    assert validate_pack_manifest.main([]) == 1
    assert "invalid YAML" in capsys.readouterr().err


def test_no_manifests_found_fails(_isolate_packs_dir, capsys):
    assert validate_pack_manifest.main([]) == 1
    assert "No pack manifests found" in capsys.readouterr().err


def test_explicit_paths_override_default_dir(_isolate_packs_dir, tmp_path):
    # An explicit path outside PACKS_DIR should still be picked up, and the
    # (empty) default packs dir should not be consulted.
    outside = tmp_path / "elsewhere.yaml"
    outside.write_text(VALID_MANIFEST, encoding="utf-8")

    targets = validate_pack_manifest.resolve_targets([str(outside)])
    assert targets == [outside]
