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
    (repo / "projects/dream-cycle/daily-deliveries/2026-10-13.yaml").write_text(yaml.safe_dump(data))
    dd.materialize("2026-10-13", data)
    monkeypatch.setenv("PITCH_LINK_SECRET", "fixture-not-production")
    html = email.daily_deliveries_section(dd.payload("2026-10-13"))
    assert "Your five daily project upgrades" in html
    assert "SHIPPED" in html and "IN PROGRESS" in html
    assert html.count("Keep</a>") == 5
    assert html.count("Modify</a>") == 5
    assert html.count("Reject / request rollback</a>") == 5
    assert "actual PR-backed" in html  # supported delivery description
    assert "Daily Dream and project-catalog art remain independent" in html
    assert "No new Comfy ArtJob IDs" in html

    missing = email.daily_deliveries_section({"entries": [], "missing": True})
    assert "No five-entry verified" in missing


def test_digest_discloses_five_rows_from_one_pr(repo):
    data = docket(repo)
    for row in data["entries"]:
        row["pull_request"] = data["entries"][0]["pull_request"]
    (repo / "projects/dream-cycle/daily-deliveries/2026-10-13.yaml").write_text(
        yaml.safe_dump(data)
    )
    html = email.daily_deliveries_section(dd.payload("2026-10-13"))
    assert "5 entries came from 1 implementation PR(s)" in html
    assert "Grouped design changes are not independent productions" in html


def test_digest_asset_freshness_counts_real_jobs_separately_from_requests():
    digest = {
        "current_dream_output": {
            "built": True, "built_date": "2026-11-14",
            "assets": [
                {"lane": "dream", "art_job_id": 17, "art_status": "ready"},
                {"lane": "dream", "request_id": "card-only", "art_status": "queued"},
                {"lane": "zuzu", "art_job_id": 18, "art_status": "queued"},
            ],
        },
    }
    html = email.daily_asset_freshness_section(digest)
    assert "2/6 linked Dream records" in html
    assert "1/8 independent Zuzu records" in html
    assert "2/14 verified ArtJob IDs" in html
    assert "1/3 verified images" in html
    assert "queued request is not a delivered image" in html
    missing = email.daily_asset_freshness_section({
        "daily_dream_output_status": "No fresh bundle today."
    })
    assert "No fresh bundle today" in missing


def roadmap_docket(repo, date="2026-11-15"):
    """Five discrete scoped improvements can all share ONE existing roadmap."""
    data = docket(repo, date)
    tasks = []
    for index, row in enumerate(data["entries"]):
        task_id = f"t-{101 + index:03d}"
        row["roadmap_task"] = task_id
        tasks.append({
            "id": task_id,
            "title": f"Deliver the independent upgrade {index}",
            "status": "ready",
            "note": (
                f"daily-delivery:{date}/{row['slug']} | "
                f"PR: silasfelinus/kind_robots#{101 + index} | "
                "Shipped and checked against actual GitHub CI."
            ),
        })
    path = repo / "projects/zuzu-gamebook/roadmap.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump({
        "project": "zuzu-gamebook", "kind": "software", "tasks": tasks,
    }))
    return data, path


def test_new_daily_closeout_requires_five_distinct_existing_roadmap_tasks(repo):
    data, path = roadmap_docket(repo)
    assert dd.validate("2026-11-15", data) == []
    assert len(dd.materialize("2026-11-15", data)) == 5
    body = dd.record_path("2026-11-15", data["entries"][0]["slug"]).read_text()
    assert "Canonical roadmap: projects/zuzu-gamebook/roadmap.yaml task t-101" in body

    without_roadmap = copy.deepcopy(data)
    without_roadmap["entries"][0].pop("roadmap_task")
    assert "roadmap_task" in " ".join(dd.validate("2026-11-15", without_roadmap))

    fake_task = copy.deepcopy(data)
    fake_task["entries"][0]["roadmap_task"] = "t-999"
    assert "does not exist" in " ".join(dd.validate("2026-11-15", fake_task))

    duplicate = copy.deepcopy(data)
    duplicate["entries"][1]["roadmap_task"] = "t-101"
    assert "duplicate roadmap task" in " ".join(dd.validate("2026-11-15", duplicate))

    path.unlink()
    assert "canonical" in " ".join(dd.validate("2026-11-15", data))


def test_new_daily_roadmap_entry_must_record_its_exact_delivery_and_pr(repo):
    data, path = roadmap_docket(repo)
    roadmap = yaml.safe_load(path.read_text())
    roadmap["tasks"][0]["note"] = "A preexisting task without any new work."
    path.write_text(yaml.safe_dump(roadmap))
    assert "missing daily-delivery:2026-11-15/chapter-0" in " ".join(
        dd.validate("2026-11-15", data)
    )

    roadmap["tasks"][0]["note"] = (
        "daily-delivery:2026-11-15/chapter-0 | PR: kind_robots#999"
    )
    path.write_text(yaml.safe_dump(roadmap))
    assert "must cite delivery implementation PR" in " ".join(
        dd.validate("2026-11-15", data)
    )

    roadmap["tasks"][0]["note"] = (
        "daily-delivery:2026-11-15/chapter-0 | "
        "PR: https://github.com/silasfelinus/kind_robots/pull/101"
    )
    path.write_text(yaml.safe_dump(roadmap))
    assert dd.validate("2026-11-15", data) == []

    roadmap["project"] = "a-different-project"
    path.write_text(yaml.safe_dump(roadmap))
    assert "identity does not match" in " ".join(dd.validate("2026-11-15", data))


def test_existing_historical_daily_deliveries_keep_their_valid_contract(repo):
    historical = docket(repo, "2026-11-14")
    assert all("roadmap_task" not in row for row in historical["entries"])
    assert dd.validate("2026-11-14", historical) == []


def test_in_progress_delivery_also_has_a_canonical_roadmap_progress_note(repo):
    data, path = roadmap_docket(repo)
    row = data["entries"][0]
    row["status"] = "in-progress"
    row.pop("merge_sha")
    row.pop("checks")
    row["next_step"] = "Complete card metadata and rerun regression tests."
    assert dd.validate("2026-11-15", data) == []
    row.pop("roadmap_task")
    assert "roadmap_task" in " ".join(dd.validate("2026-11-15", data))


def test_daily_digest_links_canonical_roadmap_evidence(repo):
    data, _ = roadmap_docket(repo)
    dd.materialize("2026-11-15", data)
    html = email.daily_deliveries_section(dd.payload("2026-11-15"))
    assert "Canonical roadmap t-101" in html
    assert "projects/zuzu-gamebook/roadmap.yaml" in html
    assert html.count("Canonical roadmap t-") == 5
