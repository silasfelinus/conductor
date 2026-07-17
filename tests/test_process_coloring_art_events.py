from pathlib import Path

import pytest
import yaml

from scripts import process_coloring_art_events as events


def write_event(tmp_path: Path, **overrides: object) -> Path:
    payload: dict[str, object] = {
        "version": 1,
        "operation": "generate-color-proposals",
        "book": "monster-recast",
        "limit": 18,
        "timeout": 300,
        "task": "coloring-book/t-022",
    }
    payload.update(overrides)
    path = tmp_path / "event.yaml"
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
    return path


def test_load_event_accepts_bounded_batch(tmp_path: Path) -> None:
    event = events.load_event(write_event(tmp_path))

    assert event.book == "monster-recast"
    assert event.limit == 18
    assert event.timeout == 300
    assert event.command(live=False)[-6:] == [
        "--book",
        "monster-recast",
        "--limit",
        "18",
        "--timeout",
        "300",
    ]
    assert event.command(live=True)[-1] == "--live"


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("version", 2, "version must be 1"),
        ("operation", "shell", "operation must be generate-color-proposals"),
        ("book", "other", "book must be one of"),
        ("limit", 0, "limit must be between 1 and 18"),
        ("limit", 19, "limit must be between 1 and 18"),
        ("limit", "18", "limit must be an integer"),
        ("timeout", 29, "timeout must be between 30 and 900"),
        ("timeout", 901, "timeout must be between 30 and 900"),
    ],
)
def test_load_event_rejects_unsafe_values(
    tmp_path: Path,
    field: str,
    value: object,
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        events.load_event(write_event(tmp_path, **{field: value}))


def test_load_event_rejects_unknown_fields(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="unsupported event fields: command"):
        events.load_event(write_event(tmp_path, command="rm -rf /"))
