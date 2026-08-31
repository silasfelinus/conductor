import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import retry_dream_identity_collision_new_slug as fresh  # noqa: E402


def _proposal(slug="kelp-ink-transfer"):
    return {"slug": slug, "title": "The Deep Shift", "idea": "same authored content"}


def test_replace_source_slug_updates_frontmatter_and_proposal_data(monkeypatch):
    monkeypatch.setattr(
        fresh.repair.records,
        "_data_block",
        lambda text, key: _proposal("kelp-ink-transfer") if key == "proposal-data" else None,
    )
    text = "---\nslug: kelp-ink-transfer\ntitle: The Deep Shift\n---\n\n<!-- proposal-data\n{}\n-->\n"
    revised, old = fresh._replace_source_slug(text, "deep-shift-kelphold")
    assert old == "kelp-ink-transfer"
    assert "slug: deep-shift-kelphold" in revised
    payload = revised.split("<!-- proposal-data\n", 1)[1].split("\n-->", 1)[0]
    assert json.loads(payload)["slug"] == "deep-shift-kelphold"


def test_history_validator_allows_only_slug_change(monkeypatch):
    historical = _proposal("kelp-ink-transfer")
    built = {"records": {}}

    def data_block(text, key):
        return historical if key == "proposal-data" else built

    monkeypatch.setattr(fresh.repair.records, "_data_block", data_block)
    monkeypatch.setattr(fresh.repair, "art_by_role", lambda value: {})
    current = _proposal("deep-shift-kelphold")
    assert fresh._slug_tolerant_history_validator(current, "historical") is built

    current["idea"] = "changed creative content"
    with pytest.raises(ValueError, match="differs beyond"):
        fresh._slug_tolerant_history_validator(current, "historical")


def test_replacement_slugs_must_target_approved_bundle():
    request = {
        "bundles": ["projects/dream-cycle/backlog/a.md", "projects/dream-cycle/backlog/b.md"],
        "replacement_slugs": {"projects/dream-cycle/backlog/c.md": "new-slug"},
    }
    with pytest.raises(ValueError, match="unapproved bundle"):
        fresh._replacement_slugs(request)


def test_replacement_slugs_require_policy_clean_slug():
    request = {
        "bundles": ["projects/dream-cycle/backlog/a.md", "projects/dream-cycle/backlog/b.md"],
        "replacement_slugs": {"projects/dream-cycle/backlog/a.md": "Bad Slug"},
    }
    with pytest.raises(ValueError, match="invalid replacement slug"):
        fresh._replacement_slugs(request)
