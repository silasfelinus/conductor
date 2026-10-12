"""Cutover contract: fourteen authored, validated, safely preflighted assets."""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_daily_dream_v3_contract import example_v3  # noqa: E402
import build_dream_proposal as proposal_writer  # noqa: E402
import build_dream_records as records  # noqa: E402
import daily_dream_v3_authoring as authoring  # noqa: E402
import daily_dream_v3_contract as v3  # noqa: E402
import author_dream_proposal as author  # noqa: E402
import consume_art_queue_core as art_core  # noqa: E402
import run_daily_dream_build as build_selector  # noqa: E402


def _catalog():
    return {
        taxonomy: proposal_writer._fallback(taxonomy)
        for taxonomy in proposal_writer.FALLBACK_FACETS
    }


def test_old_day_retains_six_slots_and_new_day_gets_fourteen_independent_facets():
    catalog = _catalog()
    old = proposal_writer.build_brief("2026-10-12", catalog=catalog)
    new = proposal_writer.build_brief("2026-10-13", catalog=catalog)
    repeat = proposal_writer.build_brief("2026-10-13", catalog=catalog)
    assert "bundle_version" not in old
    assert old["seed_facets"]["version"] == 2
    assert len(old["seed_facets"]["elements"]) == 6
    assert new["bundle_version"] == 3
    assert new == repeat
    assert new["seed_facets"]["version"] == 3
    assert set(new["seed_facets"]["elements"]) == set(v3.FACET_SLOTS)
    original_ids = {
        str(row.get("slug") or row.get("id")).casefold()
        for slot in v3.DREAM_SLOTS for row in new["seed_facets"]["elements"][slot]
    }
    for slot in v3.ZUZU_SLOTS:
        assert new["seed_facets"]["elements"][slot]
        assert all(
            str(row.get("slug") or row.get("id")).casefold() not in original_ids
            for row in new["seed_facets"]["elements"][slot]
        )
    assert new["required_counts"]["zuzu_scenarios"] == 2


def test_author_includes_full_v3_system_instructions_and_provenance(monkeypatch):
    p = example_v3()
    brief = {
        "bundle_version": 3, "proposal_date": "2026-10-13",
        "seed_facets": copy.deepcopy(p["seed_facets"]), "instructions": [],
    }
    monkeypatch.setattr(author.dreams, "build_brief", lambda day: copy.deepcopy(brief))
    monkeypatch.setattr(author, "recent_name_history", lambda day: {})
    monkeypatch.setattr(author, "recent_premise_history", lambda day: [])
    monkeypatch.setattr(author, "story_diversity_complaints", lambda *a: [])
    monkeypatch.setattr(author, "name_diversity_complaints", lambda *a: [])
    monkeypatch.setattr(author.dreams, "normalize", lambda p, avoid: p)
    monkeypatch.setattr(author.dreams, "existing_slugs", lambda: set())
    monkeypatch.setattr(author.dreams, "validate_proposal", lambda p: v3.validate_v3(p))
    seen = {}

    def fake_model(prompt, system, key):
        seen["prompt"] = prompt
        seen["system"] = system
        return json.dumps(p)

    monkeypatch.setattr(author, "call_claude", fake_model)
    out = author.author("2026-10-13", "fake-key", verbose=False)
    assert out["bundle_version"] == 3
    assert v3.validate_v3(out) == []
    assert "FOURTEEN ASSETS TOTAL" in seen["system"]
    assert "eight" in seen["system"].lower() or "EIGHT" in seen["system"]
    assert "zuzu_scenario_1" in seen["prompt"]
    assert [r["project_target"] for r in out["zuzu_assets"]["locations"]] == [
        "zuzu-gamebook", "emperor-of-dust"
    ]


def test_v3_draft_has_all_extra_sections_and_preserves_notes_heading():
    rendered = proposal_writer.render_markdown(example_v3(), "2026-10-13")
    assert "Eight additional Zuzu-world creations" in rendered
    assert "### Zuzu Locations (2)" in rendered
    assert "### Zuzu Scenarios (2)" in rendered
    assert "Choice Give sanctuary" in rendered
    assert rendered.index("Eight additional Zuzu-world creations") < rendered.index("## Notes from Silas")
    assert "<!-- proposal-data" in rendered


def test_future_six_asset_buffer_stays_preserved_but_does_not_block_v3_authoring(tmp_path, monkeypatch):
    backlog = tmp_path / "backlog"
    backlog.mkdir()
    path = backlog / "2026-10-13-old-dream.md"
    old = example_v3()
    old.pop("bundle_version")
    old.pop("zuzu_assets")
    old["seed_facets"]["version"] = 2
    path.write_text(
        "---\nproposal: true\nproposal_date: '2026-10-13'\nstatus: outline\n---\n"
        "<!-- proposal-data\n" + json.dumps(old) + "\n-->\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(proposal_writer, "BACKLOG", backlog)
    monkeypatch.setattr(proposal_writer, "_files", lambda: [path])
    monkeypatch.setattr(proposal_writer, "validate_proposal", lambda *_: [])
    assert proposal_writer.proposal_exists_for("2026-10-13") is False
    assert proposal_writer.unbuilt_backlog() == []
    assert proposal_writer.stale_unbuilt_backlog() == ["2026-10-13"]
    assert "proposal-data" in path.read_text()  # no destructive migration


def test_v3_rejects_hidden_per_row_relations_before_builder_write(monkeypatch):
    p = example_v3()
    p["zuzu_assets"]["characters"][0]["world_dream_id"] = 456
    error = " ".join(v3.validate_v3(p))
    assert "must not link" in error
    called = []

    def fake_http(*args, **kwargs):
        called.append(args)
        raise AssertionError("no write allowed")

    monkeypatch.setattr(records, "http_json", fake_http)
    with pytest.raises(ValueError, match="before any writes"):
        records.build_records(p, p["slug"], "2026-10-13", dry_run=False)
    assert called == []


def test_unregistered_zuzu_checkpoint_blocks_before_creating_db_rows(tmp_path, monkeypatch):
    backlog = tmp_path / "backlog"
    backlog.mkdir()
    art = tmp_path / "art.yaml"
    art.write_text("requests:\n", encoding="utf-8")
    p = example_v3()
    path = backlog / "2026-10-13-zuzu.md"
    path.write_text(
        "---\nproposal: true\nproposal_date: '2026-10-13'\nslug: zuzu\n"
        "status: outline\n---\n"
        "<!-- proposal-data\n" + json.dumps(p) + "\n-->\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(records, "BACKLOG", backlog)
    monkeypatch.setattr(records, "ART_PROMPTS", art)
    monkeypatch.setattr(records, "KR_API_TOKEN", "test-token")
    monkeypatch.setattr(art_core, "_load_resource_index", lambda: {"CHECKPOINT": {}})
    writes = []
    monkeypatch.setattr(records, "http_json", lambda *a, **kw: writes.append(a))
    outcome = records.run_build("2026-10-13", dry_run=False)
    assert outcome["status"] == "failed"
    assert "BEFORE DB writes" in outcome["message"]
    assert writes == []
    assert "build-attempt-data" in path.read_text()
    assert "built-data" not in path.read_text()
    assert art.read_text() == "requests:\n"


def test_post_cutover_selector_skips_legacy_candidate_without_deleting_it(tmp_path, monkeypatch):
    p = example_v3()
    old = copy.deepcopy(p)
    old.pop("bundle_version")
    old.pop("zuzu_assets")
    old["seed_facets"]["version"] = 2
    docs = []
    for key, payload in (("legacy", old), ("current", p)):
        f = tmp_path / (key + ".md")
        f.write_text(
            "---\nproposal: true\nproposal_date: '2026-10-13'\nstatus: outline\n---\n"
            "<!-- proposal-data\n" + json.dumps(payload) + "\n-->\n",
            encoding="utf-8",
        )
        docs.append((f, {"status": "outline", "proposal_date": "2026-10-13"}, f.read_text()))
    monkeypatch.setattr(records, "find_proposals", lambda: docs)
    monkeypatch.setattr(build_selector.creative_contract, "validate_path", lambda *_: [])
    selected, reason = build_selector.eligible_proposal("2026-10-13")
    assert selected == docs[1][0]
    assert docs[0][0].exists()
