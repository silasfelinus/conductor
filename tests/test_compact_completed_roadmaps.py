"""Completion reconciliation is finite, lossless and approval-aware."""
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from compact_completed_roadmaps import reconcile_milestones


def test_only_fully_satisfied_finite_milestones_close():
    source = """project: demo
milestones:
  - id: m1
    status: in-progress # preserve comment
  - id: m2
    status: in-progress
  - id: m3
    status: in-progress
  - id: m4
    status: in-progress
tasks:
  - id: t-001
    milestone: m1
    status: done
  - id: t-002
    milestone: m1
    status: ready
    recurring: true
  - id: t-003
    milestone: m2
    status: waiting
  - id: t-004
    milestone: m3
    status: done
    gate_human: true
"""
    updated, closed = reconcile_milestones(source)
    assert closed == ["m1"]
    assert updated == source.replace("in-progress # preserve", "done # preserve")
    assert yaml.safe_load(updated)["tasks"] == yaml.safe_load(source)["tasks"]
    assert reconcile_milestones(updated) == (updated, [])


def test_cancelled_scope_is_not_automatically_complete():
    source = """milestones:
  - id: m1
    status: in-progress
tasks:
  - id: t-001
    milestone: m1
    status: cancelled
"""
    assert reconcile_milestones(source) == (source, [])
