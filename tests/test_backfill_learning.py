import textwrap
from pathlib import Path

import yaml

import scripts.backfill_learning as bl
import scripts.build_learning_summary as bls

REPO_ROOT = Path(__file__).resolve().parent.parent
REAL_LEDGER = REPO_ROOT / "LEARNING.yaml"

VALID_KINDS = {"software", "content", "proposal"}
VALID_STAKES = {"reversible", "outward-facing", "irreversible"}
VALID_FAILURE = {"transient", "actionable", "quality", "scope"}
RECORD_FIELDS = ["date", "project", "task", "kind", "stakes", "passes", "outcome",
                 "failure_category", "lesson"]


# --------------------------------------------------------------------------- #
# Fixtures
# --------------------------------------------------------------------------- #

def write_roadmap(projects_dir: Path, slug: str, kind: str, tasks: list[dict]) -> None:
    (projects_dir / slug).mkdir(parents=True, exist_ok=True)
    doc = {"project": slug, "kind": kind, "tasks": tasks}
    (projects_dir / slug / "roadmap.yaml").write_text(yaml.safe_dump(doc, sort_keys=False))


def task(id, status="done", **kw):
    base = {"id": id, "status": status, "passes": 0, "stakes": "reversible",
            "updated": "2026-07-12T00:00:00Z", "note": f"Did {id}. And more."}
    base.update(kw)
    return base


def seed_ledger(root: Path, records: list[dict]) -> None:
    (root / "LEARNING.yaml").write_text(yaml.safe_dump({"records": records}, sort_keys=False))


def count_records(root: Path) -> int:
    data = yaml.safe_load((root / "LEARNING.yaml").read_text()) or {}
    return len(data.get("records") or [])


# --------------------------------------------------------------------------- #
# Pure helpers
# --------------------------------------------------------------------------- #

def test_apply_backfill_prefix_idempotent():
    once = bl.apply_backfill_prefix("watch the deploy")
    twice = bl.apply_backfill_prefix(once)
    assert once == twice == "backfilled: watch the deploy"


def test_first_sentence_not_cut_at_abbreviation():
    text = "Run the audit (e.g. jsonNestedFilters) then commit. Second sentence."
    assert bl.first_sentence(text) == "Run the audit (e.g. jsonNestedFilters) then commit."


def test_first_sentence_empty():
    assert bl.first_sentence("") == ""
    assert bl.first_sentence("   ") == ""


def test_talkback_outcome_mapping():
    assert bl.talkback_outcome("closed (hourly burst-mode pick)") == "done"
    assert bl.talkback_outcome("merged (PR #304)") == "done"
    assert bl.talkback_outcome("blocked on token") == "blocked"
    assert bl.talkback_outcome("security-flag") is None
    assert bl.talkback_outcome("pattern") is None


def test_split_talkback_entries_two_formats():
    text = textwrap.dedent(
        """\
        ## 2026-06-30 | Reviewer → Worker | system | pattern
        **Subject:** a system-level note not tied to a task.

        ## 2026-07-16 | Reviewer → Silas | conductor/t-050 | closed (hourly cycle)
        **Decision:** done.
        **What to improve:** guard the index access next time.

        ## 2026-07-16 | Reviewer → Silas | kind-robots/t-022 | security-flag (reconfirmation)
        **Decision:** still open.
        """
    )
    entries = bl.split_talkback_entries(text)
    # only the terminal, task-scoped entry survives
    assert len(entries) == 1
    e = entries[0]
    assert (e["project"], e["task"], e["outcome"]) == ("conductor", "t-050", "done")


def test_talkback_index_prefers_improve_field():
    text = (
        "## 2026-07-16 | Reviewer → Silas | demo/t-001 | closed\n"
        "**Decision:** done.\n"
        "**What to improve:** claim before starting the review.\n"
    )
    idx = bl.talkback_index(text)
    assert idx[("demo", "t-001", "done")]["lesson"] == "claim before starting the review."


# --------------------------------------------------------------------------- #
# Candidate assembly
# --------------------------------------------------------------------------- #

def test_recency_window_excludes_old_and_curated_bypasses(tmp_path, monkeypatch):
    projects = tmp_path / "projects"
    write_roadmap(projects, "demo", "software", [
        task("t-001", updated="2026-07-05T00:00:00Z"),   # old → excluded by window
        task("t-002", updated="2026-07-14T00:00:00Z"),   # recent → included
        task("t-050", status="ready"),                   # not closed → skipped
    ])
    # curated entry pointing at the old task → must bypass the window
    monkeypatch.setattr(bl, "CURATED", {
        ("demo", "t-001", "done"): {"failure_category": "quality", "lesson": "curated wisdom"},
    })
    cands = bl.build_candidates(projects, "", since="2026-07-10", sources="roadmap")
    got = {(c.task, c.source) for c in cands}
    assert ("t-002", "roadmap") in got
    assert ("t-001", "curated") in got            # curated bypassed the cutoff
    assert not any(c.task == "t-050" for c in cands)  # non-closed excluded


def test_candidate_fields_and_enums_conform(tmp_path):
    projects = tmp_path / "projects"
    write_roadmap(projects, "demo", "content", [
        task("t-002", stakes="outward-facing", passes=2, updated="2026-07-14T00:00:00Z"),
    ])
    cands = bl.build_candidates(projects, "", since="2026-07-10", sources="roadmap")
    assert len(cands) == 1
    c = cands[0]
    assert c.kind in VALID_KINDS and c.kind == "content"
    assert c.stakes in VALID_STAKES and c.stakes == "outward-facing"
    assert isinstance(c.passes, int) and c.passes == 2
    assert c.outcome == "done"
    assert c.failure_category is None
    assert c.lesson.startswith("backfilled: ")


def test_invalid_kind_stakes_fall_back(tmp_path):
    projects = tmp_path / "projects"
    write_roadmap(projects, "demo", "nonsense-kind", [
        task("t-002", stakes="whatever", updated="2026-07-14T00:00:00Z"),
    ])
    c = bl.build_candidates(projects, "", since="2026-07-10", sources="roadmap")[0]
    assert c.kind == "software"      # invalid roadmap kind → default
    assert c.stakes == "reversible"  # invalid task stakes → default


# --------------------------------------------------------------------------- #
# Append path — dedup + idempotency (headline)
# --------------------------------------------------------------------------- #

def test_backfill_is_idempotent(tmp_path, monkeypatch):
    monkeypatch.setattr(bl.pte, "ROOT", tmp_path)
    seed_ledger(tmp_path, [])
    projects = tmp_path / "projects"
    write_roadmap(projects, "demo", "software", [
        task("t-001", updated="2026-07-14T00:00:00Z"),
        task("t-002", status="blocked", updated="2026-07-14T00:00:00Z"),
    ])
    cands = bl.build_candidates(projects, "", since="2026-07-10", sources="roadmap")

    appended, skipped = bl.run_backfill(cands, dry_run=False)
    assert appended == 2 and skipped == 0
    after_first = count_records(tmp_path)
    assert after_first == 2

    appended2, skipped2 = bl.run_backfill(cands, dry_run=False)
    assert appended2 == 0 and skipped2 == 2          # zero new on re-run
    assert count_records(tmp_path) == after_first     # ledger unchanged


def test_dedup_against_existing_record(tmp_path, monkeypatch):
    monkeypatch.setattr(bl.pte, "ROOT", tmp_path)
    seed_ledger(tmp_path, [{
        "date": "2026-07-11", "project": "demo", "task": "t-002", "kind": "software",
        "stakes": "reversible", "passes": 0, "outcome": "done",
        "failure_category": None, "lesson": "already here",
    }])
    projects = tmp_path / "projects"
    write_roadmap(projects, "demo", "software", [task("t-002", updated="2026-07-14T00:00:00Z")])
    cands = bl.build_candidates(projects, "", since="2026-07-10", sources="roadmap")
    appended, skipped = bl.run_backfill(cands, dry_run=False)
    assert appended == 0 and skipped == 1
    assert count_records(tmp_path) == 1


def test_dry_run_writes_nothing(tmp_path, monkeypatch):
    monkeypatch.setattr(bl.pte, "ROOT", tmp_path)
    seed_ledger(tmp_path, [])
    before = (tmp_path / "LEARNING.yaml").read_text()
    projects = tmp_path / "projects"
    write_roadmap(projects, "demo", "software", [task("t-001", updated="2026-07-14T00:00:00Z")])
    cands = bl.build_candidates(projects, "", since="2026-07-10", sources="roadmap")
    appended, skipped = bl.run_backfill(cands, dry_run=True)
    assert appended == 1
    assert (tmp_path / "LEARNING.yaml").read_text() == before  # byte-identical


def test_appended_records_conform_and_prefixed(tmp_path, monkeypatch):
    monkeypatch.setattr(bl.pte, "ROOT", tmp_path)
    seed_ledger(tmp_path, [])
    projects = tmp_path / "projects"
    write_roadmap(projects, "demo", "software", [task("t-001", updated="2026-07-14T00:00:00Z")])
    cands = bl.build_candidates(projects, "", since="2026-07-10", sources="roadmap")
    bl.run_backfill(cands, dry_run=False)

    records = yaml.safe_load((tmp_path / "LEARNING.yaml").read_text())["records"]
    assert len(records) == 1
    r = records[0]
    assert list(r.keys()) == RECORD_FIELDS               # exact field set + order
    assert r["failure_category"] is None                 # real YAML null, not "null"
    assert r["lesson"].startswith("backfilled: ")


# --------------------------------------------------------------------------- #
# Consumer still parses; real ledger stays schema-conformant
# --------------------------------------------------------------------------- #

def test_consumer_parses_after_backfill(tmp_path, monkeypatch):
    monkeypatch.setattr(bl.pte, "ROOT", tmp_path)
    seed_ledger(tmp_path, [])
    projects = tmp_path / "projects"
    write_roadmap(projects, "demo", "software", [task("t-001", updated="2026-07-14T00:00:00Z")])
    bl.run_backfill(bl.build_candidates(projects, "", since="2026-07-10", sources="roadmap"),
                    dry_run=False)
    records = bls.load_records(tmp_path / "LEARNING.yaml")
    report = bls.build_report(records)
    assert "backfilled: " in report
    assert "Recent lessons" in report


def test_committed_ledger_schema_conformance():
    """Every record in the real committed ledger (existing + backfilled) conforms."""
    records = yaml.safe_load(REAL_LEDGER.read_text())["records"]
    for r in records:
        assert set(RECORD_FIELDS).issubset(r.keys()), r
        assert r["kind"] in VALID_KINDS, r
        assert r["stakes"] in VALID_STAKES, r
        assert r["outcome"] in {"done", "blocked", "cancelled"}, r
        assert r["failure_category"] in VALID_FAILURE or r["failure_category"] is None, r
        assert isinstance(r["passes"], int), r
        assert isinstance(r["date"], (str,)) or hasattr(r["date"], "isoformat"), r
