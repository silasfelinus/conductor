"""Tests for scripts/reconcile_project_tombstones.py."""

from pathlib import Path

import pytest

import scripts.reconcile_project_tombstones as tombstones


def test_load_tombstones_requires_exact_unique_targets(tmp_path: Path):
    path = tmp_path / "project-tombstones.yaml"
    path.write_text(
        """version: 1
projects:
  - id: 2125
    slug: hidden-robots
  - id: 2126
    slug: robot-dress-up
""",
        encoding="utf-8",
    )

    assert tombstones.load_tombstones(path) == [
        {"id": 2125, "slug": "hidden-robots", "reason": None},
        {"id": 2126, "slug": "robot-dress-up", "reason": None},
    ]


def test_plan_actions_archives_only_exact_live_match():
    configured = [{"id": 2125, "slug": "hidden-robots", "reason": "accidental"}]
    live = [
        {
            "id": 2125,
            "slug": "hidden-robots",
            "conductorSlug": "hidden-robots",
            "isActive": True,
            "status": "ACTIVE",
        }
    ]

    assert tombstones.plan_actions(configured, live) == [
        {"id": 2125, "slug": "hidden-robots", "archive": True}
    ]


def test_plan_actions_is_idempotent_for_archived_row():
    configured = [{"id": 2125, "slug": "hidden-robots", "reason": "accidental"}]
    archived = [
        {
            "id": 2125,
            "slug": "hidden-robots",
            "conductorSlug": "hidden-robots",
            "isActive": False,
            "status": "ARCHIVED",
        }
    ]

    assert tombstones.plan_actions(configured, archived) == [
        {"id": 2125, "slug": "hidden-robots", "archive": False}
    ]


@pytest.mark.parametrize(
    "project",
    [
        {
            "id": 2125,
            "slug": "something-else",
            "conductorSlug": "hidden-robots",
            "isActive": True,
            "status": "ACTIVE",
        },
        {
            "id": 2125,
            "slug": "hidden-robots",
            "conductorSlug": "something-else",
            "isActive": True,
            "status": "ACTIVE",
        },
    ],
)
def test_plan_actions_refuses_identity_mismatch(project):
    configured = [{"id": 2125, "slug": "hidden-robots", "reason": "accidental"}]

    with pytest.raises(RuntimeError, match="refusing to archive"):
        tombstones.plan_actions(configured, [project])


def test_plan_actions_refuses_missing_target():
    configured = [{"id": 2125, "slug": "hidden-robots", "reason": "accidental"}]

    with pytest.raises(RuntimeError, match="was not found"):
        tombstones.plan_actions(configured, [])
