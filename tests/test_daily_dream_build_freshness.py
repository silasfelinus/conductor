"""Regression coverage for Daily Dream proposal freshness at build time."""

from __future__ import annotations

import datetime
import json
from pathlib import Path

import pytest

import scripts.run_daily_dream_build as runner


PROPOSAL = {
    "title": "Freshness Test",
    "slug": "freshness-test",
    "idea": "A visible rescue unfolds across a floating orchard during a storm.",
    "vibe": {
        "title": "Storm Orchard",
        "line": "bright fruit, hard wind, moving bridges",
        "art_direction": "floating citrus terraces under silver storm light",
    },
    "locations": [{
        "title": "Citrus Span",
        "known_for": "rope bridges between airborne orchard terraces",
        "local_rule": "every bridge is retied after lightning",
        "best_scene": "neighbors hauling a broken terrace back into formation",
        "art_direction": "wind-bent trees, wet rope, airborne stone terraces",
    }],
    "characters": [{
        "name": "Mara Sol",
        "role_drive": "rescue stranded orchard crews",
        "carries": "a coil of living rope",
        "complication": "the rope tightens when she lies",
        "look": "weathered flight coat, cropped dark hair, rope harness",
    }],
    "rewards": [
        {
            "name": "Bridge Seed",
            "reward_type": "ITEM",
            "rarity": "RARE",
            "grants": "grows one temporary rope bridge",
            "best_used_when": "a gap opens during the storm",
            "catch": "the bridge lasts only until the rain stops",
            "look": "thumb-sized amber seed wrapped in braided fiber",
        },
        {
            "name": "Windstep",
            "reward_type": "SKILL",
            "rarity": "UNCOMMON",
            "grants": "briefly balances a runner against a crosswind",
            "best_used_when": "crossing a swaying span",
            "catch": "cannot be used twice without touching solid ground",
            "look": "spiraling pressure ripples around boot soles",
        },
    ],
    "scenarios": [{
        "title": "Save Citrus Span",
        "setup": "Storm Orchard tears Citrus Span loose while Mara Sol races to reconnect it before the next lightning front.",
    }],
    "seed_facets": {
        "version": 2,
        "elements": {
            key: [{"id": index, "title": key}]
            for index, key in enumerate(sorted(runner.core.REQUIRED_SEED_ASSETS), start=1)
        },
    },
}


def _write_proposal(backlog: Path, day: datetime.date, slug: str, *, retry: bool = False) -> Path:
    payload = {**PROPOSAL, "slug": slug, "title": slug.replace("-", " ").title()}
    attempt = ""
    if retry:
        attempt = (
            "\n<!-- build-attempt-data\n"
            + json.dumps({"status": "retry", "message": "transient failure"})
            + "\n-->\n"
        )
    text = (
        "---\n"
        f"slug: {slug}\n"
        f"title: {payload['title']}\n"
        "type: dream\n"
        "status: outline\n"
        "proposal: true\n"
        f"proposal_date: '{day.isoformat()}'\n"
        "---\n\n"
        "## Notes from Silas\n- (leave notes here)\n\n"
        "## Build log\n- proposed\n\n"
        "<!-- proposal-data\n"
        + json.dumps(payload)
        + "\n-->\n"
        + attempt
    )
    path = backlog / f"{day.isoformat()}-{slug}.md"
    path.write_text(text, encoding="utf-8")
    return path


@pytest.fixture
def backlog(tmp_path, monkeypatch):
    root = tmp_path / "backlog"
    root.mkdir()
    monkeypatch.setattr(runner.core, "BACKLOG", root)
    monkeypatch.setattr(runner.creative_contract, "validate_path", lambda path: [])
    return root


def _today() -> datetime.date:
    return datetime.datetime.now(runner.core._TZ).date()


def test_automatic_selection_rejects_twelve_day_old_orphan(backlog):
    old = _write_proposal(backlog, _today() - datetime.timedelta(days=12), "old-orphan")

    path, reason = runner.eligible_proposal(None)

    assert path is None
    assert old.name in reason
    assert "stale proposal (12 days old)" in reason


def test_pinned_retry_can_be_older_than_freshness_window(backlog):
    old_retry = _write_proposal(
        backlog,
        _today() - datetime.timedelta(days=12),
        "old-retry",
        retry=True,
    )

    path, reason = runner.eligible_proposal(None)

    assert path == old_retry
    assert reason == ""


def test_recent_proposal_still_builds_automatically(backlog):
    recent = _write_proposal(backlog, _today() - datetime.timedelta(days=2), "recent")

    path, reason = runner.eligible_proposal(None)

    assert path == recent
    assert reason == ""


def test_explicit_date_bypasses_freshness_but_not_creative_contract(backlog, monkeypatch):
    day = _today() - datetime.timedelta(days=12)
    old = _write_proposal(backlog, day, "manual-old")

    path, reason = runner.eligible_proposal(day.isoformat())
    assert path == old
    assert reason == ""

    monkeypatch.setattr(
        runner.creative_contract,
        "validate_path",
        lambda path: ["story falls back into the overused bureaucracy/record-keeping motif"],
    )
    path, reason = runner.eligible_proposal(day.isoformat())
    assert path is None
    assert "creative contract failed at build time" in reason


def test_creative_contract_is_rechecked_for_fresh_candidates(backlog, monkeypatch):
    recent = _write_proposal(backlog, _today() - datetime.timedelta(days=1), "ledger-redux")
    monkeypatch.setattr(
        runner.creative_contract,
        "validate_path",
        lambda path: ["story falls back into the overused bureaucracy/record-keeping motif"],
    )

    path, reason = runner.eligible_proposal(None)

    assert path is None
    assert recent.name in reason
    assert "creative contract failed at build time" in reason
