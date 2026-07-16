"""
Tests for build_dream_proposal.py.

Two layers:
  * pure validation/normalization of an agent-authored proposal (no git), and
  * the concurrent-session double-proposal guard (dream-cycle/t-014), exercised
    against real (throwaway, local-only) git repos -- a bare "origin" plus a
    clone -- so the actual origin/main-fresh recheck runs, not a mock. Modeled on
    tests/test_claim_task.py; no network, no real GitHub.
"""

import copy
import json
import subprocess
from pathlib import Path

import pytest

import scripts.build_dream_proposal as bdp


# --------------------------------------------------------------------------- #
# Pure validation / normalization
# --------------------------------------------------------------------------- #

def test_sample_proposal_validates_clean():
    assert bdp.validate_proposal(bdp.SAMPLE_PROPOSAL) == []


def test_validate_flags_wrong_counts_and_missing_fields():
    bad = copy.deepcopy(bdp.SAMPLE_PROPOSAL)
    bad["characters"] = bad["characters"][:2]      # needs exactly 3
    bad["locations"][0].pop("art_direction")       # missing required field
    problems = bdp.validate_proposal(bad)
    assert any("characters must be a list of exactly 3" in p for p in problems)
    assert any("locations[0] missing art_direction" in p for p in problems)


def test_validate_rejects_non_skill_item_reward_type():
    bad = copy.deepcopy(bdp.SAMPLE_PROPOSAL)
    bad["rewards"][0]["reward_type"] = "CURRENCY"
    problems = bdp.validate_proposal(bad)
    assert any("reward_type values must be SKILL or ITEM" in p for p in problems)


def test_normalize_forces_one_skill_one_item():
    p = copy.deepcopy(bdp.SAMPLE_PROPOSAL)
    p["rewards"][0]["reward_type"] = "SKILL"
    p["rewards"][1]["reward_type"] = "SKILL"      # two of a kind -> repaired
    out = bdp.normalize(json.loads(json.dumps(p)), avoid=set())
    types = sorted(r["reward_type"] for r in out["rewards"])
    assert types == ["ITEM", "SKILL"]


def test_normalize_deduplicates_slug_against_avoid_set():
    p = copy.deepcopy(bdp.SAMPLE_PROPOSAL)
    p["slug"] = "kelpwick-lantern-post"
    out = bdp.normalize(json.loads(json.dumps(p)), avoid={"kelpwick-lantern-post"})
    assert out["slug"] == "kelpwick-lantern-post-2"


# --------------------------------------------------------------------------- #
# Git-backed concurrent-session guard (dream-cycle/t-014)
# --------------------------------------------------------------------------- #

def run(cmd, cwd):
    subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)


def make_remote_and_clone(tmp_path, backlog_files):
    """Bare 'origin' + clone with projects/dream-cycle/backlog/ seeded with
    `backlog_files` (name -> text), pushed to origin/main. Returns the clone path."""
    bare = tmp_path / "bare"
    clone = tmp_path / "clone"
    bare.mkdir()
    clone.mkdir()

    run(["git", "init", "-q", "--bare"], cwd=bare)
    run(["git", "init", "-q"], cwd=clone)
    run(["git", "config", "user.email", "test@example.com"], cwd=clone)
    run(["git", "config", "user.name", "Test"], cwd=clone)

    backlog = clone / "projects" / "dream-cycle" / "backlog"
    backlog.mkdir(parents=True)
    (backlog / "README.md").write_text("# backlog\n", encoding="utf-8")
    for name, text in backlog_files.items():
        (backlog / name).write_text(text, encoding="utf-8")

    run(["git", "add", "-A"], cwd=clone)
    run(["git", "commit", "-q", "-m", "init"], cwd=clone)
    run(["git", "remote", "add", "origin", str(bare)], cwd=clone)
    run(["git", "push", "-q", "origin", "HEAD:refs/heads/main"], cwd=clone)
    return clone


def proposal_file_text(slug, date):
    """A minimal but well-formed committed proposal file for a given date/slug."""
    return f"""---
slug: {slug}
title: {slug.replace('-', ' ').title()}
type: dream
status: outline
priority: normal
narrator: 'yes'
created: '{date}'
proposal: true
proposal_date: '{date}'
built_pr: null
---

## The idea
A committed proposal already on origin/main for {date}.
"""


def valid_proposal(slug, title):
    p = copy.deepcopy(bdp.SAMPLE_PROPOSAL)
    p["slug"] = slug
    p["title"] = title
    return p


@pytest.fixture
def repo_factory(tmp_path, monkeypatch):
    """Builds an origin+clone repo and points the module's ROOT/BACKLOG/SHIPPED at
    the clone so both the local-tree checks and the git recheck use it."""
    def _make(backlog_files):
        clone = make_remote_and_clone(tmp_path, backlog_files)
        monkeypatch.setattr(bdp, "ROOT", clone)
        monkeypatch.setattr(bdp, "BACKLOG", clone / "projects" / "dream-cycle" / "backlog")
        monkeypatch.setattr(bdp, "SHIPPED", clone / "projects" / "dream-cycle" / "SHIPPED.md")
        return clone
    return _make


DATE = "2026-07-20"


def test_remote_proposal_for_detects_same_date_different_slug(repo_factory):
    clone = repo_factory({f"{DATE}-moth-orchard.md": proposal_file_text("moth-orchard", DATE)})
    # fetch origin/main so the remote ref exists in the clone
    bdp.fetch_main()
    assert bdp.remote_proposal_for(DATE) == f"{DATE}-moth-orchard.md"
    assert bdp.remote_proposal_for("2026-07-21") is None


def test_write_refused_when_origin_has_same_date_proposal(repo_factory):
    """THE race: origin/main already has a same-date/different-slug proposal that is
    NOT yet in this session's working tree. The write must abort."""
    clone = repo_factory({f"{DATE}-moth-orchard.md": proposal_file_text("moth-orchard", DATE)})
    # Simulate a fresh session whose working tree has NOT pulled that file yet:
    # remove it locally but leave it on origin/main.
    (clone / "projects" / "dream-cycle" / "backlog" / f"{DATE}-moth-orchard.md").unlink()

    written = bdp.write_proposal(valid_proposal("moth-hour-mechanics", "Moth Hour"),
                                 date=DATE)
    assert written is None
    # nothing new written locally
    existing = list((clone / "projects" / "dream-cycle" / "backlog").glob(f"{DATE}-*.md"))
    assert existing == []


def test_write_proceeds_when_no_conflict(repo_factory):
    clone = repo_factory({})
    written = bdp.write_proposal(valid_proposal("comet-market", "Comet Market"), date=DATE)
    assert written is not None
    assert written.exists()
    assert written.name == f"{DATE}-comet-market.md"


def test_local_same_date_guard_still_blocks(repo_factory):
    clone = repo_factory({f"{DATE}-already-here.md": proposal_file_text("already-here", DATE)})
    written = bdp.write_proposal(valid_proposal("second-one", "Second One"), date=DATE)
    assert written is None


def test_offline_degrades_to_local_only(repo_factory, monkeypatch):
    """No reachable origin (fetch_main False) -> the write still proceeds off the
    local-only check rather than blocking the run."""
    clone = repo_factory({})
    monkeypatch.setattr(bdp, "fetch_main", lambda quiet=True: False)
    written = bdp.write_proposal(valid_proposal("lantern-fair", "Lantern Fair"), date=DATE)
    assert written is not None and written.exists()


def test_no_fetch_skips_remote_check(repo_factory):
    """--no-fetch (fetch=False) writes even if origin/main has a same-date proposal
    the local tree hasn't pulled -- the escape hatch for offline/local authoring."""
    clone = repo_factory({f"{DATE}-moth-orchard.md": proposal_file_text("moth-orchard", DATE)})
    (clone / "projects" / "dream-cycle" / "backlog" / f"{DATE}-moth-orchard.md").unlink()
    written = bdp.write_proposal(valid_proposal("moth-hour-mechanics", "Moth Hour"),
                                 date=DATE, fetch=False)
    assert written is not None and written.exists()
