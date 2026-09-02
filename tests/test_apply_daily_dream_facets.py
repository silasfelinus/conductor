import json
from pathlib import Path

import scripts.apply_daily_dream_facets as assign


def write_bundle(path: Path):
    facets = {key: [{"id": index + 10, "title": key, "slug": key, "taxonomy": "GENRE"}]
              for index, key in enumerate(("vibe", "location", "character", "reward_item", "reward_skill", "scenario"))}
    proposal = {"seed_facets": {"version": 2, "elements": facets}}
    built = {"records": {"world": {"id": 1}, "locations": [{"id": 3}], "characters": [{"id": 4}], "rewards": [{"id": 5, "reward_type": "ITEM"}, {"id": 6, "reward_type": "SKILL"}], "scenarios": [{"id": 7}]}}
    path.write_text("---\nproposal: true\n---\n\n" f"<!-- proposal-data\n{json.dumps(proposal)}\n-->\n\n" f"<!-- built-data\n{json.dumps(built)}\n-->\n", encoding="utf-8")


def _attaching_put(calls):
    """A stand-in for a Facet PUT that actually attaches what it was given.

    It echoes the requested Facets back as rows, which is what every working
    endpoint does (dreams, scenarios, rewards, art images all return the
    resolved catalog). The previous stub returned ``data: []`` and the tests
    asserted "complete" against it -- so they were encoding, and protecting, the
    exact bug this suite should have caught: PUT /api/characters/:id/facets
    ignored ``facetKeys``, attached nothing, and answered success. All 36 built
    bundles recorded ``status: "complete"`` with a Character carrying no Facets.
    """

    def fake_put(endpoint, payload, token, dry_run=False):
        calls.append((endpoint, payload))
        keys = payload.get("facetKeys") or []
        ids = payload.get("facetIds") or []
        rows = [{"id": index + 10, "slug": key} for index, key in enumerate(keys)]
        rows += [{"id": facet_id} for facet_id in ids]
        return {"success": True, "data": rows}

    return fake_put


def test_sidecar_applies_world_and_five_dependent_records(tmp_path, monkeypatch):
    path = tmp_path / "bundle.md"; write_bundle(path); calls = []
    monkeypatch.setattr(assign, "_put", _attaching_put(calls))
    changed, status, was_already_partial = assign.apply_file(path, "token")
    assert changed is True and status == "complete" and was_already_partial is False
    assert [endpoint for endpoint, _ in calls] == ["/api/dreams/1/facets", "/api/dreams/3/facets", "/api/characters/4/facets", "/api/rewards/5/facets", "/api/rewards/6/facets", "/api/scenarios/7/facets"]
    assert all(not payload["facetIds"] for _, payload in calls)
    assert [payload["facetKeys"] for _, payload in calls] == [
        ["vibe"], ["location"], ["character"], ["reward_item"],
        ["reward_skill"], ["scenario"],
    ]
    built = assign._json_comment(assign.BUILT_RE, path.read_text(encoding="utf-8"))
    assert built["facet_assignments"]["status"] == "complete"
    assert len(built["facet_assignments"]["targets"]) == 6


def test_sidecar_is_idempotent_after_complete_assignment(tmp_path, monkeypatch):
    path = tmp_path / "bundle.md"; write_bundle(path)
    monkeypatch.setattr(assign, "_put", _attaching_put([]))
    assert assign.apply_file(path, "token") == (True, "complete", False)
    assert assign.apply_file(path, "token") == (False, "already complete", False)


def test_a_target_that_attaches_nothing_is_partial_not_complete(tmp_path, monkeypatch):
    """A 200 with an empty catalog is a failure, not an application.

    This is the regression that went unnoticed for 36 bundles. The Character
    endpoint accepted a slug-only body, attached nothing, cleared what was
    there, and returned success -- and because the sidecar only checked that the
    request had not raised, it wrote ``status: "complete"`` with ``errors: []``.
    The digest then reported "Record Facets: complete" over an empty Character
    every single day.
    """
    path = tmp_path / "bundle.md"
    write_bundle(path)

    def fake_put(endpoint, payload, token, dry_run=False):
        if "/characters/" in endpoint:
            return {"success": True, "data": []}
        keys = payload.get("facetKeys") or []
        return {"success": True, "data": [{"id": i + 10} for i, _ in enumerate(keys)]}

    monkeypatch.setattr(assign, "_put", fake_put)
    changed, status, _ = assign.apply_file(path, "token")

    assert changed is True
    assert status == "partial"

    built = assign._json_comment(assign.BUILT_RE, path.read_text(encoding="utf-8"))
    assignments = built["facet_assignments"]
    assert len(assignments["targets"]) == 5  # the Character is not counted applied
    assert any("characters/4/facets" in error for error in assignments["errors"])
    assert all(target["facet_ids"] for target in assignments["targets"])


def test_dry_run_still_trusts_the_request_it_never_sent(tmp_path, monkeypatch):
    """--dry-run has no response to verify, so it must not report failure."""
    path = tmp_path / "bundle.md"
    write_bundle(path)
    monkeypatch.setattr(
        assign, "_put",
        lambda *args, **kwargs: {"success": True, "data": [], "dry_run": True},
    )
    changed, status, _ = assign.apply_file(path, "token", dry_run=True)
    assert changed is True and status == "complete"


def test_main_fails_only_on_a_freshly_partial_proposal(tmp_path, monkeypatch):
    # A proposal that was ALREADY partial before this run (same seed_version,
    # unresolved) must not re-fail the exit code every run forever -- see
    # conductor/t-104's 2026-08-08 hourly-conductor incident, where exactly
    # this pattern kept the scheduled workflow red for 2+ days on one stuck
    # proposal while genuinely new proposals kept succeeding underneath it.
    # main() short-circuits to 0 immediately when KR_API_TOKEN is absent (a
    # deliberate non-blocking-degradation path, unrelated to what this test
    # is checking) -- set one so the real partial_new/partial_persisting
    # logic under test actually runs, matching a real CI environment that
    # HAS the secret configured.
    monkeypatch.setenv("KR_API_TOKEN", "fake-token")
    stale_partial = tmp_path / "stale.md"
    fresh = tmp_path / "fresh.md"

    def fake_apply_file(path, token, dry_run=False, force=False):
        if path == stale_partial:
            return True, "partial", True  # already partial before this run
        return True, "complete", False

    monkeypatch.setattr(assign, "apply_file", fake_apply_file)
    exit_code = assign.main(["--file", str(stale_partial), "--file", str(fresh)])
    assert exit_code == 0


def test_main_fails_on_a_newly_partial_proposal(tmp_path, monkeypatch):
    monkeypatch.setenv("KR_API_TOKEN", "fake-token")
    newly_broken = tmp_path / "newly-broken.md"

    def fake_apply_file(path, token, dry_run=False, force=False):
        return True, "partial", False  # first time this proposal has gone partial

    monkeypatch.setattr(assign, "apply_file", fake_apply_file)
    exit_code = assign.main(["--file", str(newly_broken)])
    assert exit_code == 1


def test_non_facet_seeded_proposal_returns_a_three_tuple(tmp_path):
    # Regression test: apply_file's first early-return branch (a proposal with
    # no seed_facets at all -- every pre-Facet-seeding backlog entry, e.g. the
    # 2026-07-14..07-21 files) used to return a 2-tuple while every other
    # branch returns 3, so main()'s `did_change, status, was_already_partial =
    # apply_file(...)` raised ValueError: not enough values to unpack on the
    # very first legacy file in the sorted backlog glob. This broke every
    # hourly-conductor.yml run from 2026-08-08T09:38Z onward (conductor/t-104's
    # own fix commit introduced it while fixing a different failure streak).
    path = tmp_path / "legacy.md"
    path.write_text("---\nproposal: true\n---\n\nno structured data here\n", encoding="utf-8")
    result = assign.apply_file(path, "token")
    assert result == (False, "not a built Facet-seeded proposal", False)


def test_stale_recipe_id_expands_to_live_canonical_facet_keys():
    selection = assign._facet_selection([
        {
            "id": 1674,
            "slug": "kaiju-from-the-kaiju-s-perspective",
            "title": "Kaiju (from the kaiju's perspective)",
        },
        {"id": 807, "slug": "solarpunk", "title": "Solarpunk"},
    ])

    assert selection == {
        "facetIds": [],
        "facetKeys": ["kaiju", "monster-perspective", "solarpunk"],
    }
