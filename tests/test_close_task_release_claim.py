"""close_task.py releases the claim when returning a task to ready, and prints a
PR body skeleton that satisfies check_pr_handoff_template."""

import yaml

import scripts.close_task as ct
from scripts.check_pr_handoff_template import missing_sections

ROADMAP = """\
tasks:
  - id: t-001
    title: "Umbrella"
    status: claimed
    owner: worker
    claimed_by: sess-1
    claimed_at: '2026-11-18T05:48:03Z'
    note: |-
      keep me
  - id: t-002
    title: "Other"
    status: claimed
    claimed_by: sess-2
    claimed_at: '2026-11-18T05:48:03Z'
"""


def _task(text, task_id):
    return next(t for t in yaml.safe_load(text)["tasks"] if t["id"] == task_id)


def test_ready_close_clears_claim_fields_only_on_target_task():
    after = ct.apply_close(ROADMAP, "t-001", "ready", {})
    t1, t2 = _task(after, "t-001"), _task(after, "t-002")
    assert t1["status"] == "ready"
    assert "claimed_by" not in t1 and "claimed_at" not in t1
    assert t1["note"] == "keep me" and t1["owner"] == "worker"
    assert t2["claimed_by"] == "sess-2"


def test_non_ready_close_keeps_claim_fields():
    after = ct.apply_close(ROADMAP, "t-001", "review", {})
    assert _task(after, "t-001")["claimed_by"] == "sess-1"


def test_explicit_set_claim_field_is_respected():
    after = ct.apply_close(ROADMAP, "t-001", "ready", {"claimed_by": "sess-9"})
    assert _task(after, "t-001")["claimed_by"] == "sess-9"


def test_unset_absent_field_is_noop():
    assert ct.unset_task_field_text(ROADMAP, "t-001", "missing_field") == ROADMAP


def test_handoff_skeleton_passes_handoff_check():
    body = ct.handoff_body_skeleton("demo", "t-001", "ready")
    assert missing_sections(body) == []
    assert "demo/t-001" in body
