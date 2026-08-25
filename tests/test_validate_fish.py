from pathlib import Path

import pytest

import scripts.validate_fish as validate_fish


@pytest.fixture
def _isolate_fish_dir(tmp_path, monkeypatch):
    fish_dir = tmp_path / "fish"
    fish_dir.mkdir()
    monkeypatch.setattr(validate_fish, "FISH_DIR", fish_dir)
    return fish_dir


VALID_COMMON_ENTRY = """
fish:
  - slug: test-goldfish-common
    name: "Test Goldfish"
    tier: COMMON
    stats:
      charm: UNCOMMON
      empathy: COMMON
      grace: COMMON
      luck: COMMON
      might: COMMON
      wits: COMMON
    diet_role: neutral
    school_role: school
    rivals: []
    size: 1
    evolves_to: test-goldfish-elder
    evolution_kind: growth
    field_note: >
      A test fish, dryly described.
    art_prompt: >
      A test silhouette prompt.
    games:
      - cthulhuquarium
"""

VALID_UNCOMMON_ENTRY = """
fish:
  - slug: test-goldfish-elder
    name: "Test Elder Goldfish"
    tier: UNCOMMON
    stats:
      charm: RARE
      empathy: UNCOMMON
      grace: UNCOMMON
      luck: UNCOMMON
      might: COMMON
      wits: UNCOMMON
    diet_role: neutral
    school_role: school
    rivals: []
    size: 2
    field_note: >
      An elder test fish.
    art_prompt: >
      A larger test silhouette prompt.
    games:
      - cthulhuquarium
"""


def write_fish_file(dir_: Path, name: str, text: str) -> Path:
    path = dir_ / name
    path.write_text(text, encoding="utf-8")
    return path


def test_valid_bible_passes(_isolate_fish_dir, capsys):
    write_fish_file(_isolate_fish_dir, "common.yaml", VALID_COMMON_ENTRY)
    write_fish_file(_isolate_fish_dir, "uncommon.yaml", VALID_UNCOMMON_ENTRY)

    assert validate_fish.main([]) == 0
    assert "2 species across 2 tier files" in capsys.readouterr().out


def test_real_bible_passes():
    entries, errors = validate_fish.load_all_fish()
    assert errors == []
    for filename, expected_tier, entry in entries:
        validate_fish.validate_entry(filename, expected_tier, entry, None, errors)
    validate_fish.validate_slug_uniqueness(entries, errors)
    validate_fish.validate_cross_references(entries, errors)
    assert errors == []
    assert len(entries) >= 20


def test_real_bible_satisfies_require_20():
    assert validate_fish.main(["--require-20"]) == 0


def test_tier_mismatch_with_filename_fails(_isolate_fish_dir, capsys):
    bad = VALID_UNCOMMON_ENTRY.replace("tier: UNCOMMON", "tier: RARE")
    write_fish_file(_isolate_fish_dir, "uncommon.yaml", bad)

    assert validate_fish.main([]) == 1
    err = capsys.readouterr().err
    assert "doesn't match its file" in err


def test_bad_slug_pattern_fails(_isolate_fish_dir, capsys):
    bad = VALID_UNCOMMON_ENTRY.replace("test-goldfish-elder", "Test Goldfish Elder", 1)
    write_fish_file(_isolate_fish_dir, "uncommon.yaml", bad)

    assert validate_fish.main([]) == 1
    assert "lowercase, hyphenated" in capsys.readouterr().err


def test_invalid_diet_role_fails(_isolate_fish_dir, capsys):
    bad = VALID_UNCOMMON_ENTRY.replace("diet_role: neutral", "diet_role: hungry")
    write_fish_file(_isolate_fish_dir, "uncommon.yaml", bad)

    assert validate_fish.main([]) == 1
    assert "`diet_role`" in capsys.readouterr().err


def test_invalid_school_role_fails(_isolate_fish_dir, capsys):
    bad = VALID_UNCOMMON_ENTRY.replace("school_role: school", "school_role: swarm")
    write_fish_file(_isolate_fish_dir, "uncommon.yaml", bad)

    assert validate_fish.main([]) == 1
    assert "school_role" in capsys.readouterr().err


def test_invalid_stat_value_fails(_isolate_fish_dir, capsys):
    bad = VALID_UNCOMMON_ENTRY.replace("charm: RARE", "charm: SUPER_RARE")
    write_fish_file(_isolate_fish_dir, "uncommon.yaml", bad)

    assert validate_fish.main([]) == 1
    assert "stats.charm" in capsys.readouterr().err


def test_duplicate_slug_across_files_fails(_isolate_fish_dir, capsys):
    write_fish_file(_isolate_fish_dir, "common.yaml", VALID_COMMON_ENTRY)
    dup = VALID_UNCOMMON_ENTRY.replace("test-goldfish-elder", "test-goldfish-common")
    write_fish_file(_isolate_fish_dir, "uncommon.yaml", dup)

    assert validate_fish.main([]) == 1
    assert "duplicate slug" in capsys.readouterr().err


def test_evolves_to_dangling_reference_fails(_isolate_fish_dir, capsys):
    write_fish_file(_isolate_fish_dir, "common.yaml", VALID_COMMON_ENTRY)
    # uncommon.yaml intentionally omitted -> evolves_to target doesn't exist

    assert validate_fish.main([]) == 1
    assert "doesn't exist in the bible" in capsys.readouterr().err


def test_evolution_kind_without_evolves_to_fails(_isolate_fish_dir, capsys):
    bad = VALID_UNCOMMON_ENTRY.replace(
        "size: 2\n", "size: 2\n    evolution_kind: growth\n"
    )
    write_fish_file(_isolate_fish_dir, "uncommon.yaml", bad)

    assert validate_fish.main([]) == 1
    assert "`evolution_kind` set without `evolves_to`" in capsys.readouterr().err


def test_evolves_to_without_evolution_kind_fails(_isolate_fish_dir, capsys):
    write_fish_file(_isolate_fish_dir, "common.yaml", VALID_COMMON_ENTRY)
    bad = VALID_UNCOMMON_ENTRY.replace(
        "size: 2\n", "size: 2\n    evolves_to: test-goldfish-ancient\n"
    )
    write_fish_file(_isolate_fish_dir, "uncommon.yaml", bad)
    write_fish_file(
        _isolate_fish_dir,
        "rare.yaml",
        VALID_UNCOMMON_ENTRY.replace("test-goldfish-elder", "test-goldfish-ancient")
        .replace("tier: UNCOMMON", "tier: RARE"),
    )

    assert validate_fish.main([]) == 1
    assert "`evolution_kind` must be one of" in capsys.readouterr().err


def test_dangling_rivals_reference_fails(_isolate_fish_dir, capsys):
    bad = VALID_UNCOMMON_ENTRY.replace("rivals: []", "rivals: [nonexistent-slug]")
    write_fish_file(_isolate_fish_dir, "uncommon.yaml", bad)

    assert validate_fish.main([]) == 1
    assert "doesn't exist in the bible" in capsys.readouterr().err


def test_self_rivalry_fails(_isolate_fish_dir, capsys):
    bad = VALID_UNCOMMON_ENTRY.replace("rivals: []", "rivals: [test-goldfish-elder]")
    write_fish_file(_isolate_fish_dir, "uncommon.yaml", bad)

    assert validate_fish.main([]) == 1
    assert "rivals` lists itself" in capsys.readouterr().err


def test_unknown_game_fails(_isolate_fish_dir, capsys):
    bad = VALID_UNCOMMON_ENTRY.replace("- cthulhuquarium", "- fortnite")
    write_fish_file(_isolate_fish_dir, "uncommon.yaml", bad)

    assert validate_fish.main([]) == 1
    assert "unknown consumer" in capsys.readouterr().err


def test_negative_size_fails(_isolate_fish_dir, capsys):
    bad = VALID_UNCOMMON_ENTRY.replace("size: 2", "size: -1")
    write_fish_file(_isolate_fish_dir, "uncommon.yaml", bad)

    assert validate_fish.main([]) == 1
    assert "`size` must be a positive integer" in capsys.readouterr().err


def test_bad_tier_filename_reported(_isolate_fish_dir, capsys):
    write_fish_file(_isolate_fish_dir, "unknown.yaml", VALID_COMMON_ENTRY)

    assert validate_fish.main([]) == 1
    assert "doesn't match a known tier" in capsys.readouterr().err


def test_too_few_species_warns_but_passes_without_flag(_isolate_fish_dir, capsys):
    write_fish_file(_isolate_fish_dir, "common.yaml", VALID_COMMON_ENTRY)
    write_fish_file(_isolate_fish_dir, "uncommon.yaml", VALID_UNCOMMON_ENTRY)

    assert validate_fish.main([]) == 0
    assert "fewer than the DESIGN-BRIEF" in capsys.readouterr().err


def test_too_few_species_fails_with_require_20(_isolate_fish_dir, capsys):
    write_fish_file(_isolate_fish_dir, "common.yaml", VALID_COMMON_ENTRY)
    write_fish_file(_isolate_fish_dir, "uncommon.yaml", VALID_UNCOMMON_ENTRY)

    assert validate_fish.main(["--require-20"]) == 1
    assert "fewer than the DESIGN-BRIEF" in capsys.readouterr().err
