"""Tests for the one-way Conductor -> Kind Robots projection builder."""

import json
import urllib.error
from pathlib import Path
from unittest import mock

import pytest

import scripts.sync_kind_robots_projection as projection


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_build_snapshot_preserves_complete_coordination_inputs(tmp_path, monkeypatch):
    write(
        tmp_path / "project-overrides.yaml",
        "overrides:\n"
        "  - slug: active-project\n"
        "    status: active\n"
        "  - slug: paused-project\n"
        "    status: paused\n",
    )
    write(
        tmp_path / "projects" / "active-project" / "roadmap.yaml",
        "project: Active Project\ntasks: []\n",
    )
    write(
        tmp_path / "projects" / "paused-project" / "roadmap.yaml",
        "project: Paused Project\ntasks: []\n",
    )
    write(
        tmp_path / "projects" / "_template" / "roadmap.yaml",
        "project: Template\ntasks: []\n",
    )
    write(
        tmp_path / "pitches" / "2026-08-03-projection.md",
        "# Pitch: Projection\nstatus: awaiting-silas\n",
    )
    image = tmp_path / "projects" / "images" / "active-project-card.webp"
    image.parent.mkdir(parents=True, exist_ok=True)
    image.write_bytes(b"card-image")

    monkeypatch.setattr(projection, "ROOT", tmp_path)
    monkeypatch.setattr(projection, "source_commit_sha", lambda: "a" * 40)

    snapshot = projection.build_snapshot()

    assert snapshot["sourceRepo"] == "silasfelinus/conductor"
    assert snapshot["sourceRef"] == "main"
    assert snapshot["sourceCommitSha"] == "a" * 40
    assert set(snapshot["roadmaps"]) == {"active-project", "paused-project"}
    assert "paused-project" in snapshot["registryYaml"]
    assert set(snapshot["pitches"]) == {"2026-08-03-projection.md"}
    assert len(snapshot["imageVersions"][image.name]) == 64


def test_encoded_snapshot_is_compact_valid_json():
    snapshot = {
        "version": 1,
        "sourceRepo": "silasfelinus/conductor",
        "sourceRef": "main",
        "sourceCommitSha": "b" * 40,
        "generatedAt": "2026-08-03T11:30:00Z",
        "registryYaml": "overrides: []\n",
        "roadmaps": {},
        "pitches": {},
        "imageVersions": {},
    }

    encoded = projection.encoded_snapshot(snapshot)

    assert b"\n" not in encoded
    assert json.loads(encoded) == snapshot


def test_encoded_snapshot_rejects_oversized_payload(monkeypatch):
    monkeypatch.setattr(projection, "MAX_PAYLOAD_BYTES", 20)

    with pytest.raises(RuntimeError, match="projection payload"):
        projection.encoded_snapshot({"payload": "larger than twenty bytes"})


def test_repository_snapshot_fits_transport_limit():
    payload = projection.encoded_snapshot(projection.build_snapshot())

    assert len(payload) < projection.MAX_PAYLOAD_BYTES


def test_post_snapshot_retries_transient_connection_errors(monkeypatch):
    """A TLS/connection-level failure (e.g. the observed ssl.SSLEOFError on the
    self-hosted Kind Robots endpoint) should be retried, not fail immediately."""
    attempts = {"n": 0}

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

        def read(self):
            return b'{"success": true, "data": {"ok": true}}'

    def flaky_urlopen(request, timeout=60):
        attempts["n"] += 1
        if attempts["n"] < projection.SYNC_RETRY_ATTEMPTS:
            raise urllib.error.URLError("EOF occurred in violation of protocol")
        return FakeResponse()

    monkeypatch.setattr(projection.urllib.request, "urlopen", flaky_urlopen)
    monkeypatch.setattr(projection.time, "sleep", lambda _seconds: None)

    result = projection.post_snapshot("https://example.com", "token", b"{}")

    assert attempts["n"] == projection.SYNC_RETRY_ATTEMPTS
    assert result["data"] == {"ok": True}


def test_post_snapshot_gives_up_after_exhausting_retries(monkeypatch):
    def always_fails(request, timeout=60):
        raise urllib.error.URLError("EOF occurred in violation of protocol")

    monkeypatch.setattr(projection.urllib.request, "urlopen", always_fails)
    monkeypatch.setattr(projection.time, "sleep", lambda _seconds: None)

    with pytest.raises(RuntimeError, match="Kind Robots sync failed after"):
        projection.post_snapshot("https://example.com", "token", b"{}")


def test_post_snapshot_does_not_retry_http_errors(monkeypatch):
    """A real rejection (bad auth, validation) should fail fast, not retry."""
    attempts = {"n": 0}

    def rejecting_urlopen(request, timeout=60):
        attempts["n"] += 1
        raise urllib.error.HTTPError(
            "https://example.com/api/conductor/sync",
            401,
            "Unauthorized",
            hdrs=None,
            fp=mock.mock_open(read_data=b'{"error": "bad token"}')(),
        )

    monkeypatch.setattr(projection.urllib.request, "urlopen", rejecting_urlopen)

    with pytest.raises(RuntimeError, match="HTTP 401"):
        projection.post_snapshot("https://example.com", "token", b"{}")

    assert attempts["n"] == 1


def test_agent_entrypoints_name_the_authority_contract():
    source_contract = (projection.ROOT / "SOURCE_OF_TRUTH.md").read_text(
        encoding="utf-8"
    )
    reconciliation = (
        projection.ROOT / "docs" / "state-reconciliation.md"
    ).read_text(encoding="utf-8")
    connector = (
        projection.ROOT / "docs" / "github-connector-worker.md"
    ).read_text(encoding="utf-8")
    claude_hook = (
        projection.ROOT / ".claude" / "hooks" / "session-start.sh"
    ).read_text(encoding="utf-8")

    assert "Conductor is the canonical coordination ledger" in source_contract
    assert "SOURCE_OF_TRUTH.md" in reconciliation
    assert "SOURCE_OF_TRUTH.md" in connector
    assert "SOURCE_OF_TRUTH.md" in claude_hook
    assert 'overrides.get("overrides", [])' in claude_hook
    assert "if proj not in active_projects" in claude_hook


def test_production_api_hosts_never_fall_back_to_retired_vercel(monkeypatch):
    """Old environment overrides must fail before any outbound network request."""
    from scripts import check_project_scaffold_drift, complete_todo, fetch_todos

    assert projection.DEFAULT_API_BASE == "https://kindrobots.org"
    assert check_project_scaffold_drift.API_URL == (
        "https://kindrobots.org/api/conductor/project-parity"
    )
    assert fetch_todos.API_URL == "https://kindrobots.org/api/todos"
    assert complete_todo.API_BASE == "https://kindrobots.org/api/todos"

    def should_not_contact_network(*args, **kwargs):
        pytest.fail("attempted an outbound request to a retired host")

    monkeypatch.setattr(projection.urllib.request, "urlopen", should_not_contact_network)
    for old_url in ("https://kind-robots.vercel.app", "https://kindrobots.vercel.app"):
        with pytest.raises(ValueError, match="retired Vercel"):
            projection.post_snapshot(old_url, "token", b"{}")


def test_operational_scripts_and_workflows_have_no_retired_vercel_urls():
    """Fail CI if an old hardcoded endpoint sneaks back into a scheduled job."""
    roots = (projection.ROOT / "scripts", projection.ROOT / ".github" / "workflows")
    obsolete_host = "kind-robots" + ".vercel.app"
    matches = []
    for root in roots:
        for path in root.rglob("*"):
            if path.is_file() and path.suffix in {".py", ".sh", ".yml", ".yaml", ".js", ".ts", ".ps1"}:
                if obsolete_host in path.read_text(encoding="utf-8", errors="replace"):
                    matches.append(str(path.relative_to(projection.ROOT)))
    assert not matches, f"Retired Vercel endpoint in runnable files: {matches}"
