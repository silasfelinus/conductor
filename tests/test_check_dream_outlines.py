"""
Tests for check_dream_outlines.py — the CI preflight that verifies each dream
backlog outline is buildable per specs/dream.md. Fixture outlines in both shapes
(seed + daily-proposal), plus each failure mode. No API calls.
"""

from pathlib import Path

import pytest

import scripts.check_dream_outlines as dc


# --------------------------------------------------------------------------- #
# Fixtures
# --------------------------------------------------------------------------- #

SEED_OK = """\
---
slug: demo-dream
title: Demo Dream
type: dream
status: outline
narrator: yes
---

## The idea
A cozy, specific little world with a tactile hook and a reason to linger here.

## Location dream
**The Demo Hall** — LOCATION. A warm, strange place rendered in amber light.

## Vibe / genre dream
**Demo Reverie** — GENRE. Gentle wonder, low stakes, deep feeling.

## Characters (2-4)
- **Ada** — the keeper; wants every visitor to leave lighter.
- **Bram** — the apprentice; keeps almost breaking things beautifully.
- **The Hush** — a presence that only speaks in weather.

## Rewards (3-6)
- **Warm Token** (COMMON) — a small comfort you can keep.
- **Bright Key** (UNCOMMON) — opens one door you were afraid of.
- **The True Map** (LEGENDARY) — shows the way you already knew.

## Scenarios (1-2)
- **Opening Night** — help Ada ready the hall before the first visitor.

## Narrator (if narrator: yes)
**Ada** as narrator bot: warm, unhurried, speaks in lamplight metaphors.
Expressions: NEUTRAL, LOVING, THINKING, SURPRISED, WINKING; action WHISPERING.
Topics/threads: "Hall Lore", "Ask Ada".

## Notes from Silas
- (leave notes here)

## Build log
- (agents append)
"""

DAILY_OK = """\
---
slug: daily-dream
title: Daily Dream
type: dream
status: outline
narrator: 'yes'
proposal: true
proposal_date: '2026-07-20'
---

## The idea
Two connected places sharing one mood, a small cast, and a host who ties it together.

## Vibe / genre dream
**Daily Reverie** — GENRE. Cozy wonder with an edge.

## Locations (2)
- **The First Place** — known for its warm strangeness. Art: amber light.
- **The Second Place** — known for its quiet machinery. Art: teal dusk.

## Characters (3)
- **One** — role and drive in a line.
- **Two** — role and drive in a line.
- **Three** — role and drive in a line.

## Rewards (2 — one skill, one item)
- **A Skill** (SKILL, RARE) — grants a useful ability.
- **An Item** (ITEM, LEGENDARY) — a tangible object that matters.

## Scenarios (1-2)
- **The Setup** — the cast, the place, and what the player does.

## Narrator
**The Host** as narrator bot: warm, wry, patient. Expressions: NEUTRAL plus LOVING,
THINKING. Topics: "Lore", "Advice".

## Notes from Silas
- (leave notes here)

## Build log
- proposed
"""

NARRATORLESS_OK = SEED_OK.replace("narrator: yes", "narrator: no").replace(
    """## Narrator (if narrator: yes)
**Ada** as narrator bot: warm, unhurried, speaks in lamplight metaphors.
Expressions: NEUTRAL, LOVING, THINKING, SURPRISED, WINKING; action WHISPERING.
Topics/threads: "Hall Lore", "Ask Ada".""",
    """## Narrator (if narrator: yes)
narrator: no — this dream stays narratorless on purpose.""",
)


@pytest.fixture
def backlog(tmp_path):
    d = tmp_path / "backlog"
    d.mkdir()
    return d


def write(backlog: Path, name: str, text: str) -> Path:
    p = backlog / name
    p.write_text(text, encoding="utf-8")
    return p


def kinds(findings):
    return {f.kind for f in findings}


# --------------------------------------------------------------------------- #
# Clean cases
# --------------------------------------------------------------------------- #

def test_seed_shape_ok(backlog):
    write(backlog, "seed.md", SEED_OK)
    assert dc.collect(backlog) == []


def test_daily_shape_ok(backlog):
    write(backlog, "daily.md", DAILY_OK)
    assert dc.collect(backlog) == []


def test_narratorless_ok(backlog):
    write(backlog, "narratorless.md", NARRATORLESS_OK)
    assert dc.collect(backlog) == []


def test_non_dream_and_non_buildable_are_ignored(backlog):
    write(backlog, "coloring.md", SEED_OK.replace("type: dream", "type: coloring-book"))
    write(backlog, "built.md", SEED_OK.replace("status: outline", "status: built"))
    write(backlog, "parked.md", SEED_OK.replace("status: outline", "status: parked"))
    assert dc.collect(backlog) == []


def test_real_backlog_is_buildable():
    """The committed dream outlines must all pass, so the CI guard stays green
    until a real outline actually regresses."""
    assert dc.collect(dc.DEFAULT_BACKLOG) == []


# --------------------------------------------------------------------------- #
# Failure modes
# --------------------------------------------------------------------------- #

def test_missing_vibe_section(backlog):
    text = SEED_OK.replace("## Vibe / genre dream\n**Demo Reverie** — GENRE. Gentle wonder, low stakes, deep feeling.\n\n", "")
    write(backlog, "x.md", text)
    assert "missing-section" in kinds(dc.collect(backlog))


def test_too_few_characters(backlog):
    text = SEED_OK.replace(
        "- **Bram** — the apprentice; keeps almost breaking things beautifully.\n", ""
    ).replace("- **The Hush** — a presence that only speaks in weather.\n", "")
    findings = dc.collect(write(backlog, "x.md", text).parent)
    assert "characters-count" in kinds(findings)


def test_rewards_no_rarity_spread(backlog):
    text = SEED_OK.replace("(COMMON)", "(COMMON)").replace("(UNCOMMON)", "(COMMON)").replace("(LEGENDARY)", "(COMMON)")
    findings = dc.collect(write(backlog, "x.md", text).parent)
    assert "rewards-rarity" in kinds(findings)


def test_narrator_yes_but_no_block(backlog):
    text = SEED_OK.replace(
        """**Ada** as narrator bot: warm, unhurried, speaks in lamplight metaphors.
Expressions: NEUTRAL, LOVING, THINKING, SURPRISED, WINKING; action WHISPERING.
Topics/threads: "Hall Lore", "Ask Ada".""",
        "- (leave notes here)",
    )
    findings = dc.collect(write(backlog, "x.md", text).parent)
    assert "narrator-missing" in kinds(findings)


def test_empty_idea_section(backlog):
    text = SEED_OK.replace(
        "A cozy, specific little world with a tactile hook and a reason to linger here.",
        "",
    )
    findings = dc.collect(write(backlog, "x.md", text).parent)
    assert "empty-section" in kinds(findings)


def test_too_many_scenarios(backlog):
    text = SEED_OK.replace(
        "- **Opening Night** — help Ada ready the hall before the first visitor.\n",
        "- **A** — one.\n- **B** — two.\n- **C** — three.\n- **D** — four.\n",
    )
    findings = dc.collect(write(backlog, "x.md", text).parent)
    assert "scenarios-count" in kinds(findings)


def test_main_exits_one_on_problem(backlog, monkeypatch):
    write(backlog, "x.md", SEED_OK.replace("## Vibe / genre dream", "## Removed"))
    monkeypatch.setattr("sys.argv", ["check_dream_outlines.py", "--backlog-dir", str(backlog)])
    assert dc.main() == 1


def test_main_exits_zero_when_clean(backlog, monkeypatch, capsys):
    write(backlog, "seed.md", SEED_OK)
    monkeypatch.setattr("sys.argv", ["check_dream_outlines.py", "--backlog-dir", str(backlog)])
    assert dc.main() == 0
    assert "buildable" in capsys.readouterr().out
