import copy
import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import daily_project_deliveries as dd
import build_digest_email_v2_impl as email


@pytest.fixture
def repo(tmp_path, monkeypatch):
    (tmp_path / "projects/dream-cycle/daily-deliveries").mkdir(parents=True)
    (tmp_path / "pitches").mkdir()
    (tmp_path / "project-overrides.yaml").write_text(yaml.safe_dump({
        "overrides": [
            {"slug": "zuzu-gamebook", "status": "active"},
            {"slug": "paused-project", "status": "paused"},
        ]
    }))
    monkeypatch.setattr(dd, "ROOT", tmp_path)
    monkeypatch.setattr(dd, "DIR", tmp_path / "projects/dream-cycle/daily-deliveries")
    return tmp_path


def example(n):
    return {
        "slug": f"chapter-{n}",
        "title": f"Chapter {n} implemented",
        "target": "zuzu-gamebook",
        "kind": "encounter",
        "summary": "Added a playable branching encounter with consequences and inventory decisions.",
        "verification": "Completed gamebook route tests with actual passing checks.",
        "status": "shipped",
        "pull_request": f"https://github.com/silasfelinus/kind_robots/pull/{100+n}",
        "checks_url": f"https://github.com/silasfelinus/kind_robots/actions/runs/{100+n}",
        "checks": "passed",
        "merge_sha": "a" * 40,
        "art": {"status": "not-required"},
    }


def docket(repo, date="2026-10-13"):
    data = {"date": date, "entries": [example(i) for i in range(5)]}
    (repo / "projects/dream-cycle/daily-deliveries" / f"{date}.yaml").write_text(
        yaml.safe_dump(data)
    )
    return data


def test_exactly_five_shipped_evidenced_changes_and_review_records(repo):
    data = docket(repo)
    assert dd.validate("2026-10-13", data) == []
    assert len(dd.materialize("2026-10-13", data)) == 5
    assert dd.materialize("2026-10-13", data) == []
    assert dd.payload("2026-10-13")["entries"][0]["decision"] == "pending"
    assert dd.main  # module executable
    body = dd.record_path("2026-10-13", "chapter-0").read_text()
    assert "delivery-status: shipped" in body
    assert "request a scoped" in body
    assert dd.validate("2026-10-12", data)


def test_must_be_implemented_not_just_pitched(repo):
    data = docket(repo)
    data["entries"][0].pop("pull_request")
    data["entries"][1].pop("checks_url")
    data["entries"][2]["checks"] = "pending"
    data["entries"][3]["status"] = "in-progress"
    data["entries"][3].pop("next_step", None)
    data["entries"][4]["target"] = "paused-project"
    errors = " ".join(dd.validate("2026-10-13", data))
    for word in ("implementation PR", "Actions", "passing CI", "next_step", "active project"):
        assert word in errors


def test_partial_progress_cannot_masquerade_as_shipped(repo):
    data = docket(repo)
    row = data["entries"][0]
    row["status"] = "in-progress"
    row.pop("checks")
    row.pop("merge_sha")
    row["next_step"] = "Finish the new character art and rerun integration checks."
    row["art"] = {"status": "queued", "job_ids": [4032]}
    assert dd.validate("2026-10-13", data) == []
    row["art"] = {"status": "delivered"}
    assert "final asset URL" in " ".join(dd.validate("2026-10-13", data))


def test_rejection_or_modifications_become_agent_work(repo):
    data = docket(repo)
    dd.materialize("2026-10-13", data)
    reject = dd.record_path("2026-10-13", "chapter-0")
    reject.write_text(reject.read_text().replace("status: awaiting-silas", "status: rejected"))
    modify = dd.record_path("2026-10-13", "chapter-1")
    modify.write_text(modify.read_text().replace("status: awaiting-silas", "status: approved")
                      + "\n## Silas's modifications\nMake the combat less random.\n")
    feedback = dd.feedback()
    assert len(feedback) == 2
    assert "rollback PR" in feedback[0]
    assert "Make the combat less random." in feedback[1]
    assert dd.payload("2026-10-13")["entries"][0]["decision"] == "rejected"


def test_email_explicitly_distinguishes_shipped_and_progress(repo, monkeypatch):
    data = docket(repo)
    data["entries"][1].update(status="in-progress",
                              next_step="Complete the second screen and finish all pending tests.")
    dd.materialize("2026-10-13", data)
    monkeypatch.setenv("PITCH_LINK_SECRET", "fixture-not-production")
    html = email.daily_deliveries_section(dd.payload("2026-10-13"))
    assert "Your five daily project upgrades" in html
    assert "SHIPPED" in html and "IN PROGRESS" in html
    assert html.count("Keep</a>") == 5
    assert html.count("Modify</a>") == 5
    assert html.count("Reject / request rollback</a>") == 5
    assert "actual PR-backed" in html  # supported delivery description
    missing = email.daily_deliveries_section({"entries": [], "missing": True})
    assert "No five-entry verified" in missing
