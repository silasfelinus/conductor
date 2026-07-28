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


class ColoringBookStudioEventTests(unittest.TestCase):
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
            "proposal_ids": ["mr-009"],
            "timeout": 600,
            "force": False,
            "requested_by": "kind-robots-coloring-studio",
            "task": "coloring-book/t-028",
        }
        payload.update(overrides)
        path = self.root / "event.yaml"
        path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
        return path

    def test_load_event_accepts_targeted_color_proposals(self) -> None:
        event = MODULE.load_event(
            self.write_event(proposal_ids=["mr-009", "mr-010"], force=True)
        )

        self.assertEqual(event.operation, "generate-color-proposals")
        self.assertEqual(event.book, "monster-recast")
        self.assertEqual(event.proposal_ids, ("mr-009", "mr-010"))
        self.assertIsNone(event.source_path)
        self.assertTrue(event.force)
        command = event.command(live=True)
        self.assertIn("consume_coloring_book_studio_request.py", command[1])
        self.assertIn("--force", command)
        self.assertEqual(command.count("--proposal-id"), 2)
        self.assertEqual(command[-1], "--live")

    def test_production_action_routes_to_management_consumer(self) -> None:
        event = MODULE.load_event(
            self.write_event(operation="generate-bw", force=True)
        )
        command = event.command(live=False)
        self.assertIn("manage_coloring_book_production.py", command[1])
        self.assertIn("generate-bw", command)
        self.assertIn("--force", command)

    def test_existing_asset_adoption_routes_to_dedicated_consumer(self) -> None:
        event = MODULE.load_event(
            self.write_event(
                operation="accept-color",
                source_path="projects/coloring-book/sets/monster-recast/approved/fly-beach-color.webp",
            )
        )
        self.assertEqual(event.source_path, "approved/fly-beach-color.webp")
        command = event.command(live=False)
        self.assertIn("adopt_coloring_book_asset.py", command[1])
        self.assertEqual(command.count("--proposal-id"), 1)
        self.assertIn("approved/fly-beach-color.webp", command)

    def test_accept_and_finalize_operations_are_valid(self) -> None:
        for operation in ("accept-color", "accept-bw", "finalize-pair"):
            with self.subTest(operation=operation):
                event = MODULE.load_event(self.write_event(operation=operation))
                self.assertEqual(event.operation, operation)
                self.assertNotIn("--force", event.command(live=False))

    def test_load_event_deduplicates_ids_without_reordering(self) -> None:
        event = MODULE.load_event(
            self.write_event(proposal_ids=["mr-010", "mr-009", "mr-010"])
        )
        self.assertEqual(event.proposal_ids, ("mr-010", "mr-009"))

    def test_load_event_rejects_cross_book_ids(self) -> None:
        with self.assertRaisesRegex(ValueError, "does not belong"):
            MODULE.load_event(
                self.write_event(book="kind-robots", proposal_ids=["mr-009"])
            )

    def test_force_is_restricted_to_generation_operations(self) -> None:
        with self.assertRaisesRegex(ValueError, "force is only supported"):
            MODULE.load_event(
                self.write_event(operation="accept-color", force=True)
            )

    def test_source_path_is_restricted_to_single_acceptance(self) -> None:
        cases = [
            (
                {"operation": "generate-bw", "source_path": "approved/pair.webp"},
                "supported only",
            ),
            (
                {
                    "operation": "accept-color",
                    "proposal_ids": ["mr-009", "mr-010"],
                    "source_path": "approved/pair.webp",
                },
                "exactly one proposal",
            ),
            (
                {
                    "operation": "accept-color",
                    "source_path": "../approved/pair.webp",
                },
                "safe image path",
            ),
            (
                {
                    "operation": "accept-bw",
                    "source_path": "projects/coloring-book/sets/kind-robots/approved/pair.webp",
                },
                "must belong",
            ),
        ]
        for overrides, message in cases:
            with self.subTest(overrides=overrides):
                with self.assertRaisesRegex(ValueError, message):
                    MODULE.load_event(self.write_event(**overrides))

    def test_load_event_rejects_unsafe_values(self) -> None:
        cases = [
            ("version", 2, "version must be 1"),
            ("operation", "shell", "operation must be one of"),
            ("book", "other", "book must be one of"),
            ("proposal_ids", [], "proposal_ids must be a non-empty list"),
            ("proposal_ids", ["mr-9"], "does not belong"),
            ("timeout", 29, "timeout must be between 30 and 900"),
            ("timeout", 901, "timeout must be between 30 and 900"),
            ("force", "yes", "force must be a boolean"),
        ]

        for field, value, message in cases:
            with self.subTest(field=field, value=value):
                with self.assertRaisesRegex(ValueError, message):
                    MODULE.load_event(self.write_event(**{field: value}))

    def test_load_event_rejects_unknown_fields(self) -> None:
        with self.assertRaisesRegex(ValueError, "unsupported event fields: command"):
            MODULE.load_event(self.write_event(command="rm -rf /"))


if __name__ == "__main__":
    unittest.main()
