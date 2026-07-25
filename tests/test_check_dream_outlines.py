"""
Tests for check_dream_outlines.py — the CI preflight that verifies each dream
backlog outline is buildable per specs/dream.md. Fixture outlines in both shapes
(seed + daily-proposal), plus each failure mode. No API calls.
"""

from pathlib import Path

import pytest

import scripts.check_dream_outlines as dc


SEED_OK = """\
---
slug: demo-dream
title: Demo Dream
type: dream
status: outline
narrator: yes
created: '2026-07-24'
---

## Creative seeds
- **Genres:** sports comedy + procedural
- **Occupation:** scorekeeper
- **Animal / species:** octopus
- **Fusion:** Eight-arm scorekeeping changes the tools and action, while the procedural genre turns disputed points into investigations that drive every scene.

## The idea
A specific underwater tournament where recordkeeping matters more than enchanted architecture.

## Location dream
**The Demo Arena** — LOCATION. An underwater venue built around eight-armed officials.

## Vibe / genre dream
**Comic Review** — GENRE. Competitive comedy with procedural mysteries.

## Characters (2-4)
- **Ada** — octopus scorekeeper; wants every point recorded fairly.
- **Bram** — rookie competitor; keeps inventing accidental rules.
- **The Hush** — a replay drone that only speaks in timestamps.

## Rewards (3-6)
- **Warm Token** (COMMON) — a small comfort you can keep.
- **Bright Key** (UNCOMMON) — opens one disputed locker.
- **The True Map** (LEGENDARY) — shows the play everyone missed.

## Scenarios (1-2)
- **Opening Match** — help Ada investigate a point that appeared before the game began.

## Narrator (if narrator: yes)
**Ada** as narrator bot: brisk, fair, dryly funny.
Expressions: NEUTRAL, PROUD, ANXIOUS, SURPRISED, THINKING; action SHOUTING.
Topics/threads: "Rules", "Replay Review".

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
created: '2026-07-24'
proposal: true
proposal_date: '2026-07-24'
---

## Creative seeds
- **Genres:** courtroom drama + biopunk
- **Occupation:** public defender
- **Animal / species:** mantis shrimp
- **Fusion:** Polarized vision becomes evidence, public defense structures the conflict, and living reef technology changes testimony during the hearing.

## The idea
Two connected places sharing a legal-biological conflict, a small cast, and a host.

## Vibe / genre dream
**Chromatic Appeal** — GENRE. Fast objections and biological evidence.

## Locations (2)
- **The Spectrum Court** — known for polarized-light testimony. Art: living coral courtroom.
- **The Evidence Reef** — known for memories that change form. Art: forensic biopunk reef.

## Characters (3)
- **One** — mantis-shrimp defender with a sensory conflict.
- **Two** — cuttlefish clerk translating testimony.
- **Three** — human investigator carrying disputed evidence.

## Rewards (2 — one skill, one item)
- **A Skill** (SKILL, RARE) — grants a useful sensory objection.
- **An Item** (ITEM, LEGENDARY) — a tangible precedent shell.

## Scenarios (1-2)
- **The Setup** — the cast, the court, and what the player must prove.

## Narrator
**The Clerk** as narrator bot: precise, skeptical, patient. Expressions: NEUTRAL plus
THINKING, SURPRISED. Topics: "Precedent", "Evidence".

## Notes from Silas
- (leave notes here)

## Build log
- proposed
"""

NARRATORLESS_OK = SEED_OK.replace("narrator: yes", "narrator: no").replace(
    """## Narrator (if narrator: yes)
**Ada** as narrator bot: brisk, fair, dryly funny.
Expressions: NEUTRAL, PROUD, ANXIOUS, SURPRISED, THINKING; action SHOUTING.
Topics/threads: "Rules", "Replay Review".""",
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


def test_seed_shape_ok(backlog):
    write(backlog, "seed.md", SEED_OK)
    assert dc.collect(backlog) == []


def test_daily_shape_ok(backlog):
    write(backlog, "daily.md", DAILY_OK)
    assert dc.collect(backlog) == []


def test_narratorless_ok(backlog):
    write(backlog, "narratorless.md", NARRATORLESS_OK)
    assert dc.collect(backlog) == []


def test_legacy_pre_contract_outline_is_grandfathered(backlog):
    legacy = SEED_OK.replace("created: '2026-07-24'", "created: '2026-07-23'")
    start = legacy.index("## Creative seeds")
    end = legacy.index("## The idea")
    legacy = legacy[:start] + legacy[end:]
    write(backlog, "legacy.md", legacy)
    assert dc.collect(backlog) == []


def test_non_dream_and_non_buildable_are_ignored(backlog):
    write(backlog, "coloring.md", SEED_OK.replace("type: dream", "type: coloring-book"))
    write(backlog, "built.md", SEED_OK.replace("status: outline", "status: built"))
    write(backlog, "parked.md", SEED_OK.replace("status: outline", "status: parked"))
    assert dc.collect(backlog) == []


def test_real_backlog_is_buildable():
    assert dc.collect(dc.DEFAULT_BACKLOG) == []


def test_missing_creative_seed_section(backlog):
    text = SEED_OK
    start = text.index("## Creative seeds")
    end = text.index("## The idea")
    text = text[:start] + text[end:]
    findings = dc.collect(write(backlog, "x.md", text).parent)
    assert "seed-missing" in kinds(findings)


def test_too_many_genre_seeds(backlog):
    text = SEED_OK.replace(
        "**Genres:** sports comedy + procedural",
        "**Genres:** sports comedy + procedural + mystery",
    )
    findings = dc.collect(write(backlog, "x.md", text).parent)
    assert "seed-genres" in kinds(findings)


def test_missing_species_seed(backlog):
    text = SEED_OK.replace("- **Animal / species:** octopus\n", "")
    findings = dc.collect(write(backlog, "x.md", text).parent)
    assert "seed-species" in kinds(findings)


def test_thin_fusion_seed(backlog):
    text = SEED_OK.replace(
        "Eight-arm scorekeeping changes the tools and action, while the procedural genre turns disputed points into investigations that drive every scene.",
        "They combine.",
    )
    findings = dc.collect(write(backlog, "x.md", text).parent)
    assert "seed-fusion" in kinds(findings)


def test_missing_vibe_section(backlog):
    text = SEED_OK.replace(
        "## Vibe / genre dream\n**Comic Review** — GENRE. Competitive comedy with procedural mysteries.\n\n",
        "",
    )
    write(backlog, "x.md", text)
    assert "missing-section" in kinds(dc.collect(backlog))


def test_too_few_characters(backlog):
    text = SEED_OK.replace(
        "- **Bram** — rookie competitor; keeps inventing accidental rules.\n", ""
    ).replace("- **The Hush** — a replay drone that only speaks in timestamps.\n", "")
    findings = dc.collect(write(backlog, "x.md", text).parent)
    assert "characters-count" in kinds(findings)


def test_rewards_no_rarity_spread(backlog):
    text = SEED_OK.replace("(UNCOMMON)", "(COMMON)").replace("(LEGENDARY)", "(COMMON)")
    findings = dc.collect(write(backlog, "x.md", text).parent)
    assert "rewards-rarity" in kinds(findings)


def test_narrator_yes_but_no_block(backlog):
    text = SEED_OK.replace(
        """**Ada** as narrator bot: brisk, fair, dryly funny.
Expressions: NEUTRAL, PROUD, ANXIOUS, SURPRISED, THINKING; action SHOUTING.
Topics/threads: "Rules", "Replay Review".""",
        "- (leave notes here)",
    )
    findings = dc.collect(write(backlog, "x.md", text).parent)
    assert "narrator-missing" in kinds(findings)


def test_empty_idea_section(backlog):
    text = SEED_OK.replace(
        "A specific underwater tournament where recordkeeping matters more than enchanted architecture.",
        "",
    )
    findings = dc.collect(write(backlog, "x.md", text).parent)
    assert "empty-section" in kinds(findings)


def test_too_many_scenarios(backlog):
    text = SEED_OK.replace(
        "- **Opening Match** — help Ada investigate a point that appeared before the game began.\n",
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
