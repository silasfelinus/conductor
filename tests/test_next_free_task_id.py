from __future__ import annotations

import pytest

from scripts.next_free_task_id import NextTaskIdError, next_free_task_id, used_numeric_ids


def test_returns_lowest_gap_not_highest_plus_one() -> None:
    doc = {"tasks": [{"id": "t-001"}, {"id": "t-003"}, {"id": "t-065"}]}
    assert next_free_task_id(doc) == "t-002"


def test_ignores_noncanonical_historical_ids() -> None:
    doc = {"tasks": [{"id": "t-001"}, {"id": "t-003b"}, {"id": "launch-copy"}]}
    assert used_numeric_ids(doc) == {1}
    assert next_free_task_id(doc) == "t-002"


def test_duplicate_ids_only_occupy_one_slot() -> None:
    doc = {"tasks": [{"id": "t-001"}, {"id": "t-001"}, {"id": "t-002"}]}
    assert next_free_task_id(doc) == "t-003"


def test_errors_when_canonical_range_is_exhausted() -> None:
    doc = {"tasks": [{"id": f"t-{number:03d}"} for number in range(1, 1000)]}
    with pytest.raises(NextTaskIdError, match="no free canonical task id"):
        next_free_task_id(doc)
