"""
Tests for build_dream_records.py's ATOMIC build guarantee (dream-cycle).

The builder creates ~12 kind_robots rows per proposal over ~27 REST calls. If an
intermittent DB 503 hits mid-sequence, a partial build must NOT be marked `built`
(it would ship an incomplete dream that never retries) — instead every row created
this run is rolled back so the next sweep retries clean. These tests drive run_build
with a scripted fake http_json (no network) and assert that contract.
"""

import json
from pathlib import Path

import pytest

import scripts.build_dream_records as bdr


# --------------------------------------------------------------------------- #
# Pure helpers
# --------------------------------------------------------------------------- #

def test_delete_base_maps_sheets_to_collection():
    assert bdr._delete_base("/api/sheets/by-dream/42") == "/api/sheets"
    assert bdr._delete_base("/api/dreams") == "/api/dreams"
    assert bdr._delete_base("/api/dream-relations") == "/api/dream-relations"


def test_rollback_created_deletes_ok_rows_newest_first(monkeypatch):
    deletes = []
    monkeypatch.setattr(bdr, "http_json",
                        lambda m, url, body=None, timeout=60: (deletes.append((m, url)) or (200, {})))
    results = [
        {"ok": True, "id": 1, "delete_base": "/api/dreams"},
        {"ok": False, "id": None, "delete_base": "/api/dreams"},   # skipped (failed)
        {"ok": True, "id": 7, "delete_base": "/api/sheets"},
        {"ok": True, "id": None, "delete_base": "/api/characters"},  # skipped (no id)
    ]
    n = bdr.rollback_created(results)
    assert n == 2
    # newest-first
    assert deletes[0] == ("DELETE", f"{bdr.KR_BASE_URL}/api/sheets/7")
    assert deletes[1] == ("DELETE", f"{bdr.KR_BASE_URL}/api/dreams/1")


# --------------------------------------------------------------------------- #
# End-to-end run_build with a scripted fake API
# --------------------------------------------------------------------------- #

PROPOSAL = {
    "title": "Test Dream", "slug": "test-dream",
    "idea": "A small self-consistent world for the atomic-build test.",
    "vibe": {"title": "Test Vibe", "line": "cozy wonder"},
    "locations": [
        {"title": "Place A", "known_for": "x", "local_rule": "y", "best_scene": "z", "art_direction": "amber"},
        {"title": "Place B", "known_for": "x", "local_rule": "y", "best_scene": "z", "art_direction": "teal"},
    ],
    "characters": [
        {"name": "Cee", "role_drive": "keeper", "carries": "keys", "complication": "none", "look": "old"},
        {"name": "Dee", "role_drive": "apprentice", "carries": "wire", "complication": "none", "look": "young"},
        {"name": "Eee", "role_drive": "presence", "carries": "fog", "complication": "none", "look": "dim"},
    ],
    "rewards": [
        {"name": "Skill One", "reward_type": "SKILL", "rarity": "RARE", "grants": "g", "best_used_when": "w", "catch": "c"},
        {"name": "Item Two", "reward_type": "ITEM", "rarity": "LEGENDARY", "grants": "g", "best_used_when": "w", "catch": "c"},
    ],
    "scenarios": [
        {"title": "Scene One", "setup": "the cast, the place, the task."},
    ],
    "narrator": {
        "name": "Cee", "voice": "warm", "personality": "wry", "appears_as": "portrait",
        "best_for": "prompts", "expressions": "NEUTRAL, LOVING", "topics": ["Lore"],
    },
}


def write_proposal_file(backlog: Path) -> Path:
    fm = ("---\nslug: test-dream\ntitle: Test Dream\ntype: dream\nstatus: outline\n"
          "narrator: 'yes'\nproposal: true\nproposal_date: '2020-01-01'\nbuilt_pr: null\n---\n")
    body = ("\n## The idea\nA world.\n\n## Notes from Silas\n- (leave notes here)\n\n"
            f"## Build log\n- proposed\n\n<!-- proposal-data\n{json.dumps(PROPOSAL)}\n-->\n")
    p = backlog / "2020-01-01-test-dream.md"
    p.write_text(fm + body, encoding="utf-8")
    return p


class FakeAPI:
    """Scripted http_json: POSTs succeed (returning incrementing ids) until
    `fail_after` of them have succeeded, then return 503. DELETEs always 200."""

    def __init__(self, fail_after=None):
        self.fail_after = fail_after
        self.post_ok = 0
        self.next_id = 1000
        self.deletes = []
        self.posts = []

    def __call__(self, method, url, body=None, timeout=60):
        if method == "DELETE":
            self.deletes.append(url)
            return 200, {"success": True}
        self.posts.append(url)
        if self.fail_after is not None and self.post_ok >= self.fail_after:
            return 503, {"success": False, "message": "Database connection was temporarily unavailable."}
        self.post_ok += 1
        self.next_id += 1
        return 201, {"data": {"id": self.next_id}}


@pytest.fixture
def env(tmp_path, monkeypatch):
    backlog = tmp_path / "backlog"
    backlog.mkdir()
    art = tmp_path / "art-prompts.yaml"
    art.write_text("requests:\n", encoding="utf-8")
    monkeypatch.setattr(bdr, "BACKLOG", backlog)
    monkeypatch.setattr(bdr, "ART_PROMPTS", art)
    monkeypatch.setattr(bdr, "KR_API_TOKEN", "test-token")
    return backlog, art


def test_full_success_marks_built_and_never_rolls_back(env, monkeypatch):
    backlog, art = env
    path = write_proposal_file(backlog)
    fake = FakeAPI(fail_after=None)
    monkeypatch.setattr(bdr, "http_json", fake)

    bdr.run_build("2020-01-01", dry_run=False)

    assert fake.deletes == []                       # nothing rolled back
    assert "<!-- built-data" in path.read_text()    # marked built
    assert "requests:" in art.read_text()


def test_partial_failure_rolls_back_and_leaves_unbuilt(env, monkeypatch):
    backlog, art = env
    path = write_proposal_file(backlog)
    fake = FakeAPI(fail_after=5)                     # 5 rows land, then the DB "blips"
    monkeypatch.setattr(bdr, "http_json", fake)

    bdr.run_build("2020-01-01", dry_run=False)

    assert len(fake.deletes) == 5                    # exactly the created rows undone
    assert "<!-- built-data" not in path.read_text() # NOT marked built
    assert art.read_text() == "requests:\n"          # no art queued for a failed build


def test_total_failure_rolls_back_nothing_and_leaves_unbuilt(env, monkeypatch):
    backlog, art = env
    path = write_proposal_file(backlog)
    fake = FakeAPI(fail_after=0)                     # every POST 503s from the start
    monkeypatch.setattr(bdr, "http_json", fake)

    bdr.run_build("2020-01-01", dry_run=False)

    assert fake.deletes == []                        # nothing was created, nothing to undo
    assert "<!-- built-data" not in path.read_text()
