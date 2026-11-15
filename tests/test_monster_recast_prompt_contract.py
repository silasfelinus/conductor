"""Monster Recast studio prompts must clear the prompt contract's negation rules.

ArtJob 69344 (mr-012, "not human eyes") and the mr-021 enqueue ("no face around it")
were refused by kind_robots' prompt contract on 2026-11-14/15 PT. The studio submits
these source prompts plus the coloring-book suffixes, so check every combination with
the Python mirror of the negation rules. The server stays the authority for the other
rules (frame-noun, picture-noun): run scripts/check_art_prompts_live_contract.py-style
checks against kind_robots when editing these prompts.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import consume_coloring_book_color_art as coloring  # noqa: E402
import queue_monster_recast_art as monster_queue  # noqa: E402
from repair_negation_art_prompts import violations  # noqa: E402

REQUEST = ROOT / "projects/coloring-book/sets/monster-recast/art-modeler-request.yaml"


def _prompts() -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []

    def walk(node):
        if isinstance(node, dict):
            if isinstance(node.get("prompt"), str) and node.get("id"):
                found.append((str(node["id"]), node["prompt"]))
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(yaml.safe_load(REQUEST.read_text(encoding="utf-8")))
    return found


PROMPTS = _prompts()
SUFFIXES = {
    "color": coloring.COLOR_SUFFIX,
    "logo": coloring.LOGO_SUFFIX,
    "style": " " + monster_queue.STYLE_SUFFIX,
}


def test_request_has_prompts():
    assert len(PROMPTS) >= 30


@pytest.mark.parametrize("name,suffix", sorted(SUFFIXES.items()))
def test_suffix_alone_is_clean(name, suffix):
    assert violations(suffix, "krea2") == []
    assert not any(word in suffix for word in ("edges of the picture", "frame", "no readable"))


@pytest.mark.parametrize("item_id,prompt", PROMPTS, ids=[p[0] for p in PROMPTS])
def test_source_prompt_with_suffixes_is_clean(item_id, prompt):
    for suffix in SUFFIXES.values():
        assert violations(coloring.clean(prompt + suffix), "krea2") == [], item_id
