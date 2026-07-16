"""
Tests for check_scheduler_drift.py — the CI guard that diffs dream-cycle
coloring-book scheduler cards against their home sets. Fixture cards + fixture
home sets, no network, no real coloring-book files touched.
"""

from pathlib import Path

import pytest

import scripts.check_scheduler_drift as drift


# --------------------------------------------------------------------------- #
# Fixture builders
# --------------------------------------------------------------------------- #

def write_card(backlog: Path, name: str, frontmatter: str, body: str) -> Path:
    path = backlog / name
    path.write_text(f"---\n{frontmatter.strip()}\n---\n\n{body.strip()}\n", encoding="utf-8")
    return path


def write_home_set(root: Path, slug: str, *, readme: str = "", manifest: str = "") -> Path:
    home = root / "projects" / "coloring-book" / "sets" / slug
    home.mkdir(parents=True, exist_ok=True)
    if readme:
        (home / "README.md").write_text(readme, encoding="utf-8")
    if manifest:
        approved = home / "approved"
        approved.mkdir(exist_ok=True)
        (approved / "manifest.yaml").write_text(manifest, encoding="utf-8")
    return home


MANIFEST_3 = """\
set: demo-book
confirmed_approvals:
  - concept_id: d-001
    slug: alpha
    label: Alpha One
    status: approved-pair
    color: approved/alpha-color.webp
    bw: approved/alpha-bw.webp
  - concept_id: d-002
    slug: beta
    label: Beta Two
    status: approved-pair
    color: approved/beta-color.webp
    bw: approved/beta-bw.webp
  - concept_id: d-003
    slug: gamma
    label: Gamma Three
    status: approved-pair
    color: approved/gamma-color.webp
    bw: approved/gamma-bw.webp
"""

README_PG13_34 = """\
# Demo Book

content-rating: progressive teen horror, approximately PG-13

The pool is a **34-concept homage pool** plus six group-page seeds.
"""

CARD_FM = "slug: demo-book\ntitle: Demo Book\ntype: coloring-book\nstatus: approved\npriority: high\nhome_set: projects/coloring-book/sets/demo-book/"

CARD_BODY_IN_SYNC = """\
## The idea
Progressive teen horror, ~PG-13 (NOT all-ages). A 34-concept homage pool.

## Production state
Three approved master pairs already exist (Alpha One, Beta Two, Gamma Three).
"""


@pytest.fixture
def env(tmp_path):
    backlog = tmp_path / "backlog"
    backlog.mkdir()
    return tmp_path, backlog


def find(findings, kind):
    return [f for f in findings if f.kind == kind]


# --------------------------------------------------------------------------- #
# In-sync: no drift
# --------------------------------------------------------------------------- #

def test_in_sync_card_has_no_findings(env):
    root, backlog = env
    write_home_set(root, "demo-book", readme=README_PG13_34, manifest=MANIFEST_3)
    write_card(backlog, "demo-book.md", CARD_FM, CARD_BODY_IN_SYNC)
    assert drift.collect(backlog, root) == []


def test_main_exits_zero_when_clean(env, monkeypatch, capsys):
    root, backlog = env
    write_home_set(root, "demo-book", readme=README_PG13_34, manifest=MANIFEST_3)
    write_card(backlog, "demo-book.md", CARD_FM, CARD_BODY_IN_SYNC)
    monkeypatch.setattr("sys.argv",
                        ["check_scheduler_drift.py", "--backlog-dir", str(backlog),
                         "--repo-root", str(root)])
    assert drift.main() == 0
    assert "No drift" in capsys.readouterr().out


# --------------------------------------------------------------------------- #
# Each drift signal
# --------------------------------------------------------------------------- #

def test_new_approved_pair_not_named_in_card_is_flagged(env):
    root, backlog = env
    write_home_set(root, "demo-book", readme=README_PG13_34, manifest=MANIFEST_3)
    # card names only two of the three approved pairs, and states the wrong count
    body = """## Production state
Two approved master pairs exist (Alpha One, Beta Two). ~PG-13 (NOT all-ages).
A 34-concept pool.
"""
    write_card(backlog, "demo-book.md", CARD_FM, body)
    findings = drift.collect(backlog, root)
    assert find(findings, "approved-pair-names")
    assert "Gamma Three" in find(findings, "approved-pair-names")[0].detail
    assert find(findings, "approved-pair-count")  # 'Two' != 3


def test_rating_drift_is_flagged(env):
    root, backlog = env
    write_home_set(root, "demo-book", readme=README_PG13_34, manifest=MANIFEST_3)
    body = """## The idea
An all-ages coloring book. A 34-concept pool.

## Production state
Three approved master pairs exist (Alpha One, Beta Two, Gamma Three).
"""
    write_card(backlog, "demo-book.md", CARD_FM, body)
    findings = drift.collect(backlog, root)
    assert find(findings, "rating")


def test_concept_pool_drift_is_flagged(env):
    root, backlog = env
    write_home_set(root, "demo-book", readme=README_PG13_34, manifest=MANIFEST_3)
    body = """## The idea
~PG-13 (NOT all-ages). A 28-concept homage pool.

## Production state
Three approved master pairs exist (Alpha One, Beta Two, Gamma Three).
"""
    write_card(backlog, "demo-book.md", CARD_FM, body)
    findings = drift.collect(backlog, root)
    pool = find(findings, "concept-pool")
    assert pool and "28" in pool[0].detail and "34" in pool[0].detail


def test_main_exits_one_on_drift(env, monkeypatch):
    root, backlog = env
    write_home_set(root, "demo-book", readme=README_PG13_34, manifest=MANIFEST_3)
    write_card(backlog, "demo-book.md", CARD_FM,
               "An all-ages book. 34-concept pool.\nThree approved master pairs "
               "exist (Alpha One, Beta Two, Gamma Three).")
    monkeypatch.setattr("sys.argv",
                        ["check_scheduler_drift.py", "--backlog-dir", str(backlog),
                         "--repo-root", str(root)])
    assert drift.main() == 1


# --------------------------------------------------------------------------- #
# Structural / skip cases
# --------------------------------------------------------------------------- #

def test_active_card_with_missing_home_set_is_error(env):
    root, backlog = env
    write_card(backlog, "ghost.md",
               "slug: ghost\ntitle: Ghost\ntype: coloring-book\nstatus: approved\n"
               "home_set: projects/coloring-book/sets/ghost/",
               "A book. ~PG-13.")
    findings = drift.collect(backlog, root)
    hs = find(findings, "home-set-missing")
    assert hs and hs[0].severity == "error"


def test_parked_card_with_missing_home_set_is_soft_drift(env):
    root, backlog = env
    write_card(backlog, "parked.md",
               "slug: parked\ntitle: Parked\ntype: coloring-book\nstatus: parked\n"
               "home_set: projects/coloring-book/sets/parked/",
               "A future book.")
    findings = drift.collect(backlog, root)
    hs = find(findings, "home-set-missing")
    assert hs and hs[0].severity == "drift"


def test_parked_card_with_existing_seed_set_and_no_manifest_is_clean(env):
    """Mirrors hollywood-recast-2: parked, home set exists as a seed scaffold with
    no approvals yet and no rating/pool figures — nothing to drift against."""
    root, backlog = env
    write_home_set(root, "seed-book", readme="# Seed Book\n\nConcept seed only.\n")
    write_card(backlog, "seed.md",
               "slug: seed-book\ntitle: Seed Book\ntype: coloring-book\nstatus: parked\n"
               "home_set: projects/coloring-book/sets/seed-book/",
               "A parked concept seed. Not yet defined.")
    assert drift.collect(backlog, root) == []


def test_dream_cards_are_ignored(env):
    root, backlog = env
    write_card(backlog, "a-dream.md",
               "slug: a-dream\ntitle: A Dream\ntype: dream\nstatus: outline",
               "A dream, not a coloring book.")
    assert drift.collect(backlog, root) == []


def test_real_repo_backlog_is_in_sync():
    """The committed backlog + coloring-book sets must be drift-free, so the CI
    guard stays green until a real card actually drifts."""
    assert drift.collect(drift.DEFAULT_BACKLOG, drift.ROOT) == []
