"""
Tests for build_dream_records.py's ATOMIC build guarantee (dream-cycle).

The builder creates one exact six-asset bundle over several REST calls. If an
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
        {"ok": True, "created": True, "id": 1, "delete_base": "/api/dreams"},
        {"ok": False, "created": False, "id": None, "delete_base": "/api/dreams"},
        {"ok": True, "created": False, "id": 5, "delete_base": "/api/rewards"},
        {"ok": True, "created": True, "id": 7, "delete_base": "/api/sheets"},
        {"ok": True, "created": True, "id": None, "delete_base": "/api/characters"},
    ]
    n = bdr.rollback_created(results)
    assert n == 2
    # newest-first
    assert deletes[0] == ("DELETE", f"{bdr.KR_BASE_URL}/api/sheets/7")
    assert deletes[1] == ("DELETE", f"{bdr.KR_BASE_URL}/api/dreams/1")


def test_conflict_adopts_one_exact_row_and_never_rolls_it_back(monkeypatch):
    identity = {
        "name": "The Exact Prize",
        "description": "A prize from the interrupted bundle.",
        "rewardType": "ITEM",
        "artPrompt": "a precise prize",
    }

    def fake_http(method, url, body=None, timeout=60):
        if method == "POST":
            return 409, {"success": False, "message": "Record already exists."}
        if method == "GET":
            return 200, {"success": True, "data": [{"id": 77, **identity}]}
        raise AssertionError(f"unexpected {method} {url}")

    monkeypatch.setattr(bdr, "http_json", fake_http)
    results = []
    record = bdr.kr_call(
        "POST", "/api/rewards", {**identity, "isPublic": True}, False, results,
        "Reward: The Exact Prize", conflict_identity=identity,
    )

    assert record == {"id": 77, **identity}
    assert results[0]["ok"] is True
    assert results[0]["adopted"] is True
    assert results[0]["created"] is False
    assert bdr.rollback_created(results) == 0


def test_conflict_with_different_content_remains_a_failure(monkeypatch):
    identity = {"title": "Same Name", "description": "intended"}

    def fake_http(method, url, body=None, timeout=60):
        if method == "POST":
            return 409, {"success": False, "message": "Already exists."}
        return 200, {"success": True, "data": [
            {"id": 88, "title": "Same Name", "description": "different"},
        ]}

    monkeypatch.setattr(bdr, "http_json", fake_http)
    results = []
    record = bdr.kr_call(
        "POST", "/api/scenarios", identity, False, results,
        "Scenario: Same Name", conflict_identity=identity,
    )

    assert record is None
    assert results[0]["ok"] is False
    assert results[0]["created"] is False


def test_idempotent_200_response_is_not_owned_by_this_attempt(monkeypatch):
    monkeypatch.setattr(
        bdr,
        "http_json",
        lambda method, url, body=None, timeout=60: (200, {"data": {"id": 91}}),
    )
    results = []
    assert bdr.kr_call(
        "POST", "/api/sheets/by-dream/12", {}, False, results, "existing sheet"
    ) == {"id": 91}
    assert results[0]["created"] is False
    assert bdr.rollback_created(results) == 0


def test_dream_relation_upsert_is_never_assumed_new(monkeypatch):
    monkeypatch.setattr(
        bdr,
        "http_json",
        lambda method, url, body=None, timeout=60: (201, {"data": {"id": 92}}),
    )
    results = []
    assert bdr.kr_call(
        "POST", "/api/dream-relations",
        {"fromDreamId": 1, "toDreamId": 2, "relationType": "CONTAINS"},
        False, results, "existing-or-new relation",
    ) == {"id": 92}
    assert results[0]["created"] is False
    assert bdr.rollback_created(results) == 0


# --------------------------------------------------------------------------- #
# End-to-end run_build with a scripted fake API
# --------------------------------------------------------------------------- #

PROPOSAL = {
    "title": "Test Dream", "slug": "test-dream",
    "idea": "A small self-consistent world for the atomic-build test.",
    "vibe": {"title": "Test Vibe", "line": "cozy wonder"},
    "locations": [
        {"title": "Place A", "known_for": "x", "local_rule": "y", "best_scene": "z", "art_direction": "amber"},
    ],
    "characters": [
        {"name": "Cee", "role_drive": "keeper", "carries": "keys", "complication": "none", "look": "old"},
    ],
    "rewards": [
        {"name": "Skill One", "reward_type": "SKILL", "rarity": "RARE", "grants": "g", "best_used_when": "w", "catch": "c"},
        {"name": "Item Two", "reward_type": "ITEM", "rarity": "LEGENDARY", "grants": "g", "best_used_when": "w", "catch": "c"},
    ],
    "scenarios": [
        {"title": "Scene One", "setup": "the cast, the place, the task."},
    ],
    "seed_facets": {
        "version": 2,
        "elements": {
            key: [{"id": index, "title": key}]
            for index, key in enumerate(sorted(bdr.REQUIRED_SEED_ASSETS), start=1)
        },
    },
}


def write_proposal_file(backlog: Path) -> Path:
    fm = ("---\nslug: test-dream\ntitle: Test Dream\ntype: dream\nstatus: outline\n"
          "narrator: 'no'\nproposal: true\nproposal_date: '2020-01-01'\nbuilt_pr: null\n---\n")
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
        self.created = []

    def __call__(self, method, url, body=None, timeout=60):
        if method == "DELETE":
            self.deletes.append(url)
            return 200, {"success": True}
        self.posts.append(url)
        if self.fail_after is not None and self.post_ok >= self.fail_after:
            return 503, {"success": False, "message": "Database connection was temporarily unavailable."}
        self.post_ok += 1
        self.next_id += 1
        self.created.append((url, body, self.next_id))
        return 201, {"data": {"id": self.next_id}}


class ScenarioConflictAPI(FakeAPI):
    """The interrupted run created the Scenario but lost its ledger commit."""

    def __init__(self):
        super().__init__()
        self.scenario_body = None

    def __call__(self, method, url, body=None, timeout=60):
        if method == "POST" and url.endswith("/api/scenarios"):
            self.posts.append(url)
            self.scenario_body = body
            return 409, {"message": "Scenario already exists with ID 1850."}
        if method == "GET" and url.endswith("/api/scenarios"):
            live = {"id": 1850, **self.scenario_body}
            live["intros"] = json.dumps(
                [self.scenario_body["intros"]], ensure_ascii=False
            )
            return 200, {"success": True, "data": [live]}
        return super().__call__(method, url, body, timeout)


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

    outcome = bdr.run_build("2020-01-01", dry_run=False)

    assert outcome["status"] == "built"
    assert outcome["art_requests"] == 6
    assert fake.deletes == []                       # nothing rolled back
    assert "<!-- built-data" in path.read_text()    # marked built
    assert "requests:" in art.read_text()


def test_retry_adopts_scenario_after_api_intro_normalization(env, monkeypatch):
    backlog, _ = env
    path = write_proposal_file(backlog)
    fake = ScenarioConflictAPI()
    monkeypatch.setattr(bdr, "http_json", fake)

    outcome = bdr.run_build("2020-01-01", dry_run=False)

    assert outcome["status"] == "built"
    assert fake.deletes == []
    built = bdr._data_block(path.read_text(encoding="utf-8"), "built-data")
    assert built["records"]["scenarios"][0]["id"] == 1850


def test_partial_failure_rolls_back_and_leaves_unbuilt(env, monkeypatch):
    backlog, art = env
    path = write_proposal_file(backlog)
    fake = FakeAPI(fail_after=5)                     # 5 rows land, then the DB "blips"
    monkeypatch.setattr(bdr, "http_json", fake)

    outcome = bdr.run_build("2020-01-01", dry_run=False)

    assert outcome["status"] == "failed"
    assert outcome["retry"] is True
    # Four owned rows are deleted. The fifth success is a DreamRelation upsert,
    # whose 201 response cannot distinguish new from pre-existing; deleting the
    # Dreams cascades a new edge without risking an adopted edge.
    assert len(fake.deletes) == 4
    assert "<!-- built-data" not in path.read_text() # NOT marked built
    assert art.read_text() == "requests:\n"          # no art queued for a failed build
    assert '"status": "retry"' in path.read_text()
    assert "Database connection was temporarily unavailable." in path.read_text()


def test_total_failure_rolls_back_nothing_and_leaves_unbuilt(env, monkeypatch):
    backlog, art = env
    path = write_proposal_file(backlog)
    fake = FakeAPI(fail_after=0)                     # every POST 503s from the start
    monkeypatch.setattr(bdr, "http_json", fake)

    outcome = bdr.run_build("2020-01-01", dry_run=False)

    assert outcome["status"] == "failed"
    assert fake.deletes == []                        # nothing was created, nothing to undo
    assert "<!-- built-data" not in path.read_text()

def test_real_entities_link_to_world_without_retired_genre_dream(env, monkeypatch):
    backlog, _ = env
    write_proposal_file(backlog)
    fake = FakeAPI(fail_after=None)
    monkeypatch.setattr(bdr, "http_json", fake)

    bdr.run_build("2020-01-01", dry_run=False)

    world_id = next(
        row_id for url, body, row_id in fake.created
        if url.endswith("/api/dreams") and body.get("dreamType") == "PITCH"
    )
    assert not any(
        url.endswith("/api/dreams") and body.get("dreamType") == "GENRE"
        for url, body, _ in fake.created
    )
    linked_paths = ("/api/characters", "/api/rewards", "/api/scenarios")
    linked_bodies = [
        body for url, body, _ in fake.created
        if any(url.endswith(path) for path in linked_paths)
    ]

    assert linked_bodies
    for body in linked_bodies:
        assert body["dreamIds"]
        assert world_id in body["dreamIds"]

    for url, body, _ in fake.created:
        if url.endswith("/api/rewards") or url.endswith("/api/scenarios"):
            assert "designer" not in body


def test_failed_proposal_stays_ahead_of_newer_unattempted_proposal(env, monkeypatch):
    backlog, _ = env
    failed = write_proposal_file(backlog)
    bdr.record_build_failure(
        failed,
        {"status": "retry", "attempted_at": "2026-08-02T10:00:00-07:00", "message": "DB down"},
        dry_run=False,
    )
    newer = backlog / "2020-01-02-newer.md"
    newer.write_text(
        failed.read_text(encoding="utf-8")
        .replace("slug: test-dream", "slug: newer")
        .replace("proposal_date: '2020-01-01'", "proposal_date: '2020-01-02'")
        .replace("<!-- build-attempt-data\n", "<!-- ignored-build-attempt-data\n"),
        encoding="utf-8",
    )

    selected, reason = bdr.eligible_proposal(None)

    assert reason == ""
    assert selected == failed


def test_missing_token_is_a_failed_retry_not_a_green_noop(env, monkeypatch):
    backlog, _ = env
    path = write_proposal_file(backlog)
    monkeypatch.setattr(bdr, "KR_API_TOKEN", "")

    outcome = bdr.run_build("2020-01-01", dry_run=False)

    assert outcome["status"] == "failed"
    assert outcome["proposal"] == path.name
    assert '"status": "retry"' in path.read_text(encoding="utf-8")


def test_unexpected_builder_exception_is_recorded_for_retry(env, monkeypatch):
    backlog, _ = env
    path = write_proposal_file(backlog)
    monkeypatch.setattr(
        bdr,
        "build_records",
        lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("socket vanished")),
    )

    outcome = bdr.run_build("2020-01-01", dry_run=False)

    assert outcome["status"] == "failed"
    assert "socket vanished" in outcome["message"]
    assert '"status": "retry"' in path.read_text(encoding="utf-8")
def test_missing_token_failure_pins_attempt_count_at_one(env, monkeypatch):
    backlog, _ = env
    path = write_proposal_file(backlog)
    monkeypatch.setattr(bdr, "KR_API_TOKEN", "")

    bdr.run_build("2020-01-01", dry_run=False)

    attempt = bdr._data_block(path.read_text(encoding="utf-8"), "build-attempt-data")
    assert attempt["attempt_count"] == 1


def test_persisting_retry_does_not_re_fail_the_sweep_exit_code(env, monkeypatch):
    """Kaizen from conductor/t-102/t-104 (2026-08-08): eligible_proposal() keeps a
    failed proposal pinned at the head of the line until it succeeds, so the exact
    same already-alerted failure would otherwise re-report `status: failed` (and
    fail hourly-conductor.yml's exit code) every single sweep forever. Only the
    FRESH failure should read as `failed`; once the proposal is already pinned at
    `status: retry` entering this attempt, a repeat of the same failure must report
    a distinct, non-`failed` status so the exit code stops re-alerting on a known,
    unresolved issue -- see t-105's audit of this repo's other backlog sidecars for
    the sibling fix in apply_daily_dream_facets.py this generalizes from.
    """
    backlog, _ = env
    path = write_proposal_file(backlog)
    monkeypatch.setattr(bdr, "KR_API_TOKEN", "")

    first = bdr.run_build("2020-01-01", dry_run=False)
    assert first["status"] == "failed"

    second = bdr.run_build("2020-01-01", dry_run=False)
    third = bdr.run_build("2020-01-01", dry_run=False)

    assert second["status"] == "retry-persisting"
    assert third["status"] == "retry-persisting"
    assert second["status"] != "failed"

    attempt = bdr._data_block(path.read_text(encoding="utf-8"), "build-attempt-data")
    assert attempt["attempt_count"] == 3


def test_persisting_retry_survives_a_different_failure_reason(env, monkeypatch):
    """The already-pinned check keys on `status: retry` in the ledger, not on the
    failure reason matching exactly -- a proposal stuck failing for reason A that
    then starts failing for reason B is still a known, already-alerted proposal,
    not a fresh incident."""
    backlog, _ = env
    path = write_proposal_file(backlog)
    bdr.record_build_failure(
        path,
        {"status": "retry", "attempted_at": "2026-08-02T10:00:00-07:00", "message": "DB down"},
        dry_run=False,
    )
    monkeypatch.setattr(
        bdr, "build_records",
        lambda *a, **k: (_ for _ in ()).throw(RuntimeError("a completely different failure")),
    )

    outcome = bdr.run_build("2020-01-01", dry_run=False)

    assert outcome["status"] == "retry-persisting"
    attempt = bdr._data_block(path.read_text(encoding="utf-8"), "build-attempt-data")
    assert attempt["attempt_count"] == 2
    assert "a completely different failure" in attempt["message"]


def test_legacy_multi_asset_proposal_is_not_eligible(env):
    backlog, _ = env
    path = write_proposal_file(backlog)
    text = path.read_text(encoding="utf-8")
    old = json.loads(json.dumps(PROPOSAL))
    old["characters"].append({"name": "Extra"})
    old["narrator"] = {"name": "Retired Host"}
    text = text.replace(json.dumps(PROPOSAL), json.dumps(old))
    path.write_text(text, encoding="utf-8")

    selected, reason = bdr.eligible_proposal("2020-01-01")

    assert selected is None
    assert "invalid canonical proposal" in reason
