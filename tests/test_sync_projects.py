"""The legacy sync_projects entrypoint must never write Project fields directly."""

from pathlib import Path

import scripts.sync_projects as legacy


def test_legacy_entrypoint_delegates_to_projection_sender(monkeypatch):
    calls = []
    monkeypatch.setattr(legacy, "projection_main", lambda: calls.append("projection") or 0)

    assert legacy.main() == 0
    assert calls == ["projection"]


def test_legacy_entrypoint_contains_no_project_mutation_path():
    source = Path(legacy.__file__).read_text(encoding="utf-8")

    assert "/api/projects" not in source
    assert "urllib.request" not in source
    assert "build_project_payload" not in source
    assert "liveUrl" not in source
    assert "channelKey" not in source
    assert "tabKey" not in source
    assert "repoUrl" not in source
    assert "sync_kind_robots_projection" in source
