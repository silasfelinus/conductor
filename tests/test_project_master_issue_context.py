"""Conductor issue handoff stays discoverable without embedding giant briefs."""

from pathlib import Path
from urllib.parse import urlparse

import yaml


ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / "docs" / "agents" / "master-issues.yaml"
GUIDE = ROOT / "docs" / "agents" / "project-issue-context.md"

# These are actual, independently verified completion-roadmap issues.
VERIFIED_ROUTES = {
    "cthulhuquarium": "4140",
    "emperor-of-dust": "4142",
    "rainbow-bullet-hell-space-princess": "4146",
    "ruler-hooked": "4144",
    "weird-humboldt": "4145",
    "zuzu-gamebook": "4139",
    "zuzu-shifting-lands": "3917",
}


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_master_issue_directory_is_only_a_small_valid_url_index():
    source = DIRECTORY.read_text(encoding="utf-8")
    data = yaml.safe_load(source)
    issues = data["master_issues"]
    assert isinstance(issues, dict)
    assert len(source) < 4000, "keep issue context on GitHub, not in the prompt directory"
    assert len(issues) == len(set(issues.values())), "two projects cannot silently share a master issue"

    for slug, url in issues.items():
        assert (ROOT / "projects" / slug / "roadmap.yaml").is_file(), slug
        parsed = urlparse(url)
        assert parsed.scheme == "https" and parsed.netloc == "github.com", slug
        owner, repo, marker, number, *remainder = parsed.path.strip("/").split("/")
        assert owner and repo and marker == "issues" and number.isdecimal(), slug
        assert not remainder and not parsed.query and not parsed.fragment, slug

    for slug, number in VERIFIED_ROUTES.items():
        assert issues[slug] == f"https://github.com/silasfelinus/kind_robots/issues/{number}"


def test_all_agent_entrypoints_point_to_context_runbook():
    for entry in (
        "AGENTS.md",
        "CLAUDE.md",
        "prompts/hourly-worker.md",
        "docs/agents/roles/worker.md",
        "docs/agents/roles/reviewer.md",
    ):
        body = read(entry)
        assert "docs/agents/master-issues.yaml" in body, entry
        assert "docs/agents/project-issue-context.md" in body, entry


def test_shared_findings_do_not_override_source_of_truth_or_prematurely_close():
    body = GUIDE.read_text(encoding="utf-8")
    for guarantee in (
        "CONTROL.md",
        "Conductor task",
        "conductor:skip",
        "source_issue",
        "issuecomment-",
        "ArtJob",
        "Do not mark art complete",
        "final human creative verdict",
    ):
        assert guarantee in body
