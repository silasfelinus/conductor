"""Art delivery, curation and supersession are separate evidence gates."""
from __future__ import annotations

import yaml

from scripts.shifting_desks_art_readiness import classify, inventory, markdown

PREFIX = "kind_robots public/images/shifting-desks/"


def row(name, *, status="delivered", verdict="keep: matches prompt", check="HEAD 200", **extra):
    return {
        "key": name,
        "target_path": PREFIX + "cards/" + name + ".webp",
        "status": status,
        "verdict": verdict,
        "delivery_check": check,
        "request_id": "shifting-desks-" + name,
        **extra,
    }


def round_file(tmp_path, number, subjects):
    path = tmp_path / f"ROUND-{number}.yaml"
    path.write_text(yaml.safe_dump({"subjects": subjects}), encoding="utf-8")
    return path


def test_delivery_is_not_editorial_keep():
    assert classify(row("a", verdict=None)) == "unreviewed"
    assert classify(row("a", verdict="redo: missing visual gag")) == "redo"
    assert classify(row("a", status="requested", verdict="keep: stale")) == "not_delivered"
    assert classify(row("a", check=None)) == "missing_provenance"
    assert classify(row("a")) == "accepted"


def test_new_round_supersedes_old_approval_without_faking_completion(tmp_path):
    round_file(tmp_path, 2, [row("robot")])
    round_file(tmp_path, 15, [row("robot", status="requested", verdict=None)])
    report = inventory(tmp_path)
    assert report["targets"] == 1
    assert report["counts"] == {"not_delivered": 1}
    assert report["blocked"][0]["round"] == 15
    assert not report["ready"]
    assert "ROUND-15" in markdown(report)
    round_file(tmp_path, 15, [row("robot", verdict=None, art_job_id=123, art_image_id=456)])
    report = inventory(tmp_path)
    assert report["counts"] == {"unreviewed": 1}
    assert not report["ready"]
    round_file(tmp_path, 15, [row("robot")])
    assert inventory(tmp_path)["ready"]


def test_classic_and_western_have_separate_acceptance(tmp_path):
    round_file(tmp_path, 2, [row("a")])
    western = row("a", verdict=None)
    western["target_path"] = PREFIX + "styles/western-cartoon/cards/a.webp"
    round_file(tmp_path, 18, [western])
    report = inventory(tmp_path)
    assert report["targets"] == 2
    assert report["styles"]["classic"]["accepted"] == 1
    assert report["styles"]["western-cartoon"]["unreviewed"] == 1
    assert not report["ready"]


def test_duplicate_and_invalid_targets_are_fatal_even_if_all_other_rows_kept(tmp_path):
    round_file(tmp_path, 2, [row("a"), row("a"), {"key": "bad", "target_path": "/wrong"}])
    report = inventory(tmp_path)
    assert not report["ready"]
    assert len(report["errors"]) == 2
    assert "duplicate target" in "\n".join(report["errors"])
    assert "invalid target path" in "\n".join(report["errors"])


def test_repo_inventory_has_real_render_ledgers():
    report = inventory()
    assert report["targets"] >= 300
    assert 18 in report["rounds"]
    assert "classic" in report["styles"]
    assert "western-cartoon" in report["styles"]
    # This is a guard against accidental blanket approvals: an unreviewed
    # delivered Western render must not be counted as an accepted painting.
    assert report["styles"]["western-cartoon"]["accepted"] <= report["styles"]["western-cartoon"]["total"]
