"""Regression fixtures for Ruler Hooked cross-repository card-art coverage."""

from pathlib import Path

import yaml

from scripts.check_ruler_hooked_card_art_coverage import (
    card_art_contract,
    request_coverage,
    validate,
)


def test_card_id_scanner_excludes_choice_and_deck_ids():
    source = """
  decks: [
    {
      id: 'kingdom-core',
      cards: [
        {
          id: 'river-vote',
          title: 'The River',
          art: 'card-river-vote',
          choices: [
            {
              id: 'approve',
              text: 'Yes',
            },
          ],
        },
      ],
    },
  ],
  endings: [
    { outcomeKey: 'the-end' },
  ],
"""
    ids, errors = card_art_contract(source)
    assert ids == {"river-vote"}
    assert errors == []


def test_missing_request_is_actionable():
    errors = request_coverage({"river-vote"}, {"requests": []})
    assert errors == ["river-vote: missing art request ruler-hooked-card-river-vote"]


def test_matching_pending_request_passes():
    requests = {
        "requests": [
            {
                "id": "ruler-hooked-card-river-vote",
                "status": "pending",
                "target_repo": "silasfelinus/kind_robots",
                "image_path": "public/images/ruler-hooked/card-river-vote.webp",
            }
        ]
    }
    assert request_coverage({"river-vote"}, requests) == []


def test_wrong_destination_and_duplicate_are_reported():
    row = {
        "id": "ruler-hooked-card-river-vote",
        "target_repo": "somewhere/else",
        "image_path": "public/images/ruler-hooked/wrong.webp",
    }
    errors = request_coverage({"river-vote"}, {"requests": [row, row]})
    assert any("duplicate" in error for error in errors)
    assert any("expected image_path" in error for error in errors)
    assert any("target_repo" in error for error in errors)


def test_art_key_mismatch_is_reported():
    ids, errors = card_art_contract(
        "          id: 'riverside',\n"
        "          title: 'Riverside',\n"
        "          art: 'card-elsewhere',\n"
        "          choices: [\n"
    )
    assert ids == {"riverside"}
    assert errors == ["riverside: art key must be card-riverside"]


def test_full_validator_with_synthetic_files(tmp_path: Path):
    content = tmp_path / "content.ts"
    queue = tmp_path / "art-prompts.yaml"
    content.write_text(
        "          id: 'new-quest',\n"
        "          art: 'card-new-quest',\n"
        "          choices: [\n",
        encoding="utf-8",
    )
    queue.write_text(
        yaml.safe_dump(
            {
                "requests": [
                    {
                        "id": "ruler-hooked-card-new-quest",
                        "image_path": "public/images/ruler-hooked/card-new-quest.webp",
                        "target_repo": "silasfelinus/kind_robots",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    assert validate(content, queue) == (1, [])
    queue.write_text("requests: []\n", encoding="utf-8")
    assert "missing art request" in validate(content, queue)[1][0]
