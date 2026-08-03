"""Contract tests for Daily Dream proposals and legacy idea inventory."""

import json
from pathlib import Path

import pytest

import scripts.check_dream_outlines as dc


IDEA_OK = """\
---
slug: loose-idea
title: Loose Idea
type: dream
status: outline
priority: normal
proposal: false
created: '2026-08-02'
---

## The idea
A municipal glacier inspector discovers the ice has begun filing appeals.

## Notes from Silas
- (leave notes here)

## Build log
- idea inventory only
"""

PROPOSAL = {
    "title": "Daily Dream",
    "slug": "daily-dream",
    "idea": "One coherent test world.",
    "vibe": {"title": "Test Vibe", "line": "A precise umbrella premise."},
    "locations": [{"title": "One Place"}],
    "characters": [{"name": "One Person"}],
    "rewards": [
        {"name": "One Item", "reward_type": "ITEM", "rarity": "RARE"},
        {"name": "One Skill", "reward_type": "SKILL", "rarity": "UNCOMMON"},
    ],
    "scenarios": [{"title": "One Scenario"}],
    "seed_facets": {
        "version": 2,
        "elements": {
            key: [{"id": index, "title": key}]
            for index, key in enumerate(sorted(dc.REQUIRED_FACET_KEYS), start=1)
        },
    },
}


def proposal_text(data=None, **frontmatter):
    fields = {
        "slug": "daily-dream",
        "title": "Daily Dream",
        "type": "dream",
        "status": "outline",
        "priority": "normal",
        "proposal": True,
        "proposal_date": "2026-08-02",
        "narrator": "no",
    }
    fields.update(frontmatter)
    fm = "\n".join(f"{key}: {json.dumps(value) if isinstance(value, bool) else value}" for key, value in fields.items())
    payload = PROPOSAL if data is None else data
    return (
        f"---\n{fm}\n---\n\n## The idea\nA world.\n\n"
        "## Notes from Silas\n- (leave notes here)\n\n## Build log\n- proposed\n\n"
        f"<!-- proposal-data\n{json.dumps(payload)}\n-->\n"
    )


@pytest.fixture
def backlog(tmp_path):
    path = tmp_path / "backlog"
    path.mkdir()
    return path


def write_file(backlog: Path, name: str, text: str) -> Path:
    path = backlog / name
    path.write_text(text, encoding="utf-8")
    return path


def kinds(findings):
    return {finding.kind for finding in findings}


def test_canonical_proposal_is_clean(backlog):
    write_file(backlog, "proposal.md", proposal_text())
    assert dc.collect(backlog) == []


def test_legacy_idea_inventory_is_clean(backlog):
    write_file(backlog, "idea.md", IDEA_OK)
    assert dc.collect(backlog) == []


def test_non_dream_and_inactive_proposals_are_ignored(backlog):
    write_file(backlog, "coloring.md", IDEA_OK.replace("type: dream", "type: coloring-book"))
    write_file(backlog, "built.md", proposal_text(status="built"))
    write_file(backlog, "parked.md", proposal_text(status="parked"))
    assert dc.collect(backlog) == []


def test_old_multi_asset_proposal_is_rejected(backlog):
    old = json.loads(json.dumps(PROPOSAL))
    old["locations"].append({"title": "Second Place"})
    old["characters"].extend([{"name": "Two"}, {"name": "Three"}])
    old["narrator"] = {"name": "Old Host"}
    write_file(backlog, "old.md", proposal_text(old, narrator="yes"))
    findings = dc.collect(backlog)
    assert "proposal-contract" in kinds(findings)
    assert "proposal-narrator" in kinds(findings)


def test_missing_proposal_data_is_rejected(backlog):
    write_file(backlog, "bad.md", proposal_text().split("<!-- proposal-data", 1)[0])
    assert "proposal-contract" in kinds(dc.collect(backlog))


def test_reward_types_must_be_item_and_skill(backlog):
    bad = json.loads(json.dumps(PROPOSAL))
    bad["rewards"][1]["reward_type"] = "ITEM"
    write_file(backlog, "bad.md", proposal_text(bad))
    assert "proposal-contract" in kinds(dc.collect(backlog))


def test_legacy_idea_cannot_be_building(backlog):
    write_file(backlog, "bad.md", IDEA_OK.replace("status: outline", "status: building"))
    assert "legacy-building" in kinds(dc.collect(backlog))


def test_legacy_idea_needs_content_and_notes(backlog):
    text = IDEA_OK.replace("A municipal glacier inspector discovers the ice has begun filing appeals.", "")
    text = text.replace("## Notes from Silas\n- (leave notes here)\n\n", "")
    write_file(backlog, "bad.md", text)
    found = kinds(dc.collect(backlog))
    assert {"idea-missing", "notes-missing"}.issubset(found)


def test_real_backlog_is_clean():
    assert dc.collect(dc.DEFAULT_BACKLOG) == []


def test_main_exit_codes(backlog, monkeypatch, capsys):
    write_file(backlog, "idea.md", IDEA_OK)
    monkeypatch.setattr("sys.argv", ["check_dream_outlines.py", "--backlog-dir", str(backlog)])
    assert dc.main() == 0
    assert "contracts are clean" in capsys.readouterr().out

    write_file(backlog, "bad.md", IDEA_OK.replace("status: outline", "status: building"))
    assert dc.main() == 1
