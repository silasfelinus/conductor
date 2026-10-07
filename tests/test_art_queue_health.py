from datetime import date

import scripts.art_queue_health as health

# Trimmed from Auto Art Generate run 701 (2026-10-07 04:05Z).
PROJECT_LOG = """\
  FAILED projects/images/kr-adventures-card.webp: enqueue failed: HTTP 422 Art prompt rejected by the prompt contract (1 violation):
  [text-exclusion-pile] no text names text on an engine whose negative prompt is inert.
  FAILED projects/images/comic-film-hero.webp: enqueue failed: HTTP 422 Art prompt rejected by the prompt contract (1 violation):
  [format-vocabulary] "comic panel" asks for a physical format.
LIVE: 24 entries via https://kindrobots.org

0/24 succeeded; 0 marked done in projects/art-generate.yaml.
"""

REQUESTS_LOG = """\
  FAILED to adopt projects/images/robot-sound-garden-icon.webp: ArtImage 242405 has no imageData and its imagePath fallback fetch failed: HTTP Error 404: Not Found
  FAILED public/images/channels/admin/zuzu-showdown.webp: job 34379 timed out after 300s (still queued/running)
  ADOPTED public/images/arcade/cabinet-hero.webp -> .media-direct/arcade/cabinet-hero.webp (ArtImage 242543)
0/4 generated; 0 marked done.
"""

REPAIR_LOG = """\
  ArtJob 100: legacy-sampler
Unhandled FAILED ArtJobs (1):
  ArtJob 34375: engine=COMFY; error=ArtJob validation failed before claim: [frame-noun] "rounded frame"
No failed Kind Robots ArtJobs need a known legacy repair.
"""


def test_parse_classifies_each_failure_kind():
    project = health.parse_log(PROJECT_LOG, "project-art")
    assert [(f["target"], f["kind"], f.get("rules")) for f in project] == [
        ("projects/images/kr-adventures-card.webp", "contract-rejected", ["text-exclusion-pile"]),
        ("projects/images/comic-film-hero.webp", "contract-rejected", ["format-vocabulary"]),
    ]

    requests = health.parse_log(REQUESTS_LOG, "requests")
    assert [(f["target"], f["kind"]) for f in requests] == [
        ("projects/images/robot-sound-garden-icon.webp", "adopt-failed"),
        ("public/images/channels/admin/zuzu-showdown.webp", "timeout"),
    ]

    repair = health.parse_log(REPAIR_LOG, "kr-failed-jobs")
    # The repairable ArtJob 100 above the header is not a failure.
    assert [(f["target"], f["kind"], f.get("rules")) for f in repair] == [
        ("ArtJob 34375", "kr-job-failed", ["frame-noun"]),
    ]


def test_merge_keeps_first_seen_and_skipped_sources():
    previous = health.merge([], {"requests": health.parse_log(REQUESTS_LOG, "requests")}, "2026-10-05")
    fresh = {"project-art": health.parse_log(PROJECT_LOG, "project-art")}
    merged = health.merge(previous, fresh, "2026-10-07")

    by_target = {e["target"]: e for e in merged}
    # requests had no log this run (step skipped): its entries survive unchanged.
    assert by_target["public/images/channels/admin/zuzu-showdown.webp"]["first_seen"] == "2026-10-05"
    assert by_target["projects/images/kr-adventures-card.webp"]["first_seen"] == "2026-10-07"

    # The same failures again keep their original date; a fixed one drops out.
    again = health.merge(merged, {"requests": health.parse_log(REQUESTS_LOG.splitlines()[0], "requests")}, "2026-10-09")
    targets = {e["target"]: e["first_seen"] for e in again}
    assert targets["projects/images/robot-sound-garden-icon.webp"] == "2026-10-05"
    assert "public/images/channels/admin/zuzu-showdown.webp" not in targets


def test_actionable_waits_out_transient_failures():
    entries = health.merge([], {
        "requests": health.parse_log(REQUESTS_LOG, "requests"),
        "project-art": health.parse_log(PROJECT_LOG, "project-art"),
    }, "2026-10-07")

    same_day = {e["target"] for e in health.actionable(entries, date(2026, 10, 7))}
    assert "public/images/channels/admin/zuzu-showdown.webp" not in same_day
    assert "projects/images/robot-sound-garden-icon.webp" in same_day
    assert "projects/images/kr-adventures-card.webp" in same_day

    later = {e["target"] for e in health.actionable(entries, date(2026, 10, 9))}
    assert "public/images/channels/admin/zuzu-showdown.webp" in later


def test_record_is_stable_and_check_exits_on_work(tmp_path, capsys):
    log = tmp_path / "project.log"
    log.write_text(PROJECT_LOG)
    out = tmp_path / "health.yaml"
    args = ["--out", str(out), "--today", "2026-10-07", "record", "--log", f"project-art={log}",
            "--log", f"requests={tmp_path / 'missing.log'}"]

    assert health.main(args) == 0
    first = out.read_text()
    assert health.main(args[:3] + ["2026-10-08"] + args[4:]) == 0
    assert out.read_text() == first  # same failures, next day: no churn commit

    assert health.main(["--out", str(out), "--today", "2026-10-08", "check"]) == 1
    assert "2 actionable art failure(s): 2 contract-rejected" in capsys.readouterr().out

    log.write_text("0/0 succeeded; 0 marked done.\n")
    health.main(args)
    assert health.load(out) == []
    assert health.main(["--out", str(out), "check"]) == 0


def test_checked_in_health_file_parses():
    assert isinstance(health.load(), list)
