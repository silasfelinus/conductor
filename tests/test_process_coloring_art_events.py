import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "process_coloring_art_events.py"
SPEC = importlib.util.spec_from_file_location("process_coloring_art_events", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class ColoringArtEventTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_event(self, **overrides: object) -> Path:
        payload: dict[str, object] = {
            "version": 1,
            "operation": "generate-color-proposals",
            "book": "monster-recast",
            "limit": 18,
            "timeout": 300,
            "task": "coloring-book/t-022",
        }
        payload.update(overrides)
        path = self.root / "event.yaml"
        path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
        return path

    def test_load_event_accepts_bounded_batch(self) -> None:
        event = MODULE.load_event(self.write_event())

        self.assertEqual(event.book, "monster-recast")
        self.assertEqual(event.limit, 18)
        self.assertEqual(event.timeout, 300)
        self.assertEqual(
            event.command(live=False)[-6:],
            ["--book", "monster-recast", "--limit", "18", "--timeout", "300"],
        )
        self.assertEqual(event.command(live=True)[-1], "--live")

    def test_load_event_accepts_attempt_metadata(self) -> None:
        event = MODULE.load_event(
            self.write_event(
                attempt_count=3,
                last_attempt_at="2026-07-18T07:14:50+00:00",
            )
        )

        self.assertEqual(event.book, "monster-recast")

    def test_load_event_rejects_unsafe_values(self) -> None:
        cases = [
            ("version", 2, "version must be 1"),
            ("operation", "shell", "operation must be generate-color-proposals"),
            ("book", "other", "book must be one of"),
            ("limit", 0, "limit must be between 1 and 18"),
            ("limit", 19, "limit must be between 1 and 18"),
            ("limit", "18", "limit must be an integer"),
            ("timeout", 29, "timeout must be between 30 and 900"),
            ("timeout", 901, "timeout must be between 30 and 900"),
            ("attempt_count", -1, "attempt_count must be at least 0"),
            ("attempt_count", "1", "attempt_count must be an integer"),
            ("last_attempt_at", 1, "last_attempt_at must be an ISO-8601 string"),
        ]

        for field, value, message in cases:
            with self.subTest(field=field, value=value):
                with self.assertRaisesRegex(ValueError, message):
                    MODULE.load_event(self.write_event(**{field: value}))

    def test_load_event_rejects_unknown_fields(self) -> None:
        with self.assertRaisesRegex(ValueError, "unsupported event fields: command"):
            MODULE.load_event(self.write_event(command="rm -rf /"))

    def test_record_attempt_increments_and_timestamps_event(self) -> None:
        path = self.write_event(attempt_count=2)

        MODULE.record_attempt(path)

        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        self.assertEqual(payload["attempt_count"], 3)
        self.assertRegex(payload["last_attempt_at"], r"^\d{4}-\d{2}-\d{2}T")


if __name__ == "__main__":
    unittest.main()
