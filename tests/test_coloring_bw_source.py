"""generate-bw source modes: accepted color, one named version, or the page prompt."""

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


PRODUCTION = load("manage_coloring_book_production")
EVENTS = load("process_coloring_art_events")


class BwJobBodyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.set_root = Path(self.temp.name)
        for rel in ("approved/mr-001-color.webp", "generated/bw/mr-001-bw.webp"):
            path = self.set_root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"RIFF....WEBP")
        patcher = patch.object(PRODUCTION, "set_dir", lambda _book: self.set_root)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(self.temp.cleanup)

    def body(self, **kwargs):
        return PRODUCTION.bw_job_body(
            "monster-recast",
            "mr-001",
            kwargs.pop("queue_entry", {"prompt": "A mummy hosts a beach volleyball game."}),
            kwargs.pop("accepted", {"color": "approved/mr-001-color.webp", "bw": None}),
            **kwargs,
        )

    def test_default_converts_the_accepted_color_master(self) -> None:
        body, source = self.body(bw_source="color", source_path=None)
        self.assertEqual(body["engine"], "kontext")
        self.assertEqual(body["promptString"], PRODUCTION.BW_PROMPT)
        self.assertTrue(body["sourceImageBase64"].startswith("data:image/webp;base64,"))
        self.assertEqual(source, "approved/mr-001-color.webp")

    def test_default_still_requires_an_accepted_color(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "accepted color master first"):
            self.body(accepted={"color": None}, bw_source="color", source_path=None)

    def test_version_converts_a_selected_color_without_accepted_color(self) -> None:
        body, source = self.body(
            accepted={"color": None},
            bw_source="version",
            source_path="projects/coloring-book/sets/monster-recast/approved/mr-001-color.webp",
        )
        self.assertEqual(body["engine"], "kontext")
        self.assertEqual(body["promptString"], PRODUCTION.BW_PROMPT)
        self.assertEqual(source, "approved/mr-001-color.webp")

    def test_version_refines_a_selected_bw_file(self) -> None:
        body, source = self.body(
            bw_source="version", source_path="generated/bw/mr-001-bw.webp"
        )
        self.assertEqual(body["promptString"], PRODUCTION.BW_REFINE_PROMPT)
        self.assertEqual(source, "generated/bw/mr-001-bw.webp")

    def test_version_refuses_a_missing_or_unsafe_file(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "does not exist"):
            self.body(bw_source="version", source_path="approved/nope.webp")
        with self.assertRaisesRegex(RuntimeError, "Unsafe"):
            self.body(bw_source="version", source_path="../other/mr-001.webp")

    def test_prompt_renders_fresh_line_art_from_the_page_prompt(self) -> None:
        body, source = self.body(
            accepted={"color": None}, bw_source="prompt", source_path=None
        )
        self.assertIsNone(source)
        self.assertEqual(body["engine"], "krea2")
        self.assertNotIn("sourceImageBase64", body)
        self.assertTrue(body["promptString"].startswith("A mummy hosts a beach volleyball game."))
        self.assertIn("black-and-white coloring-book page", body["promptString"])
        self.assertIn("visible nipples", body["negativePrompt"])

    def test_prompt_mode_needs_a_prompt(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "no prompt"):
            self.body(queue_entry={}, bw_source="prompt", source_path=None)

    def test_is_bw_path(self) -> None:
        self.assertTrue(PRODUCTION.is_bw_path("generated/bw/mr-001-bw.webp"))
        self.assertTrue(PRODUCTION.is_bw_path("approved/mr-001-bw.png"))
        self.assertFalse(PRODUCTION.is_bw_path("approved/mr-001-color.webp"))
        self.assertFalse(PRODUCTION.is_bw_path("approved/rainbow-mr-001.webp"))


class BwSourceEventTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)

    def load(self, **overrides):
        payload = {
            "version": 1,
            "operation": "generate-bw",
            "book": "monster-recast",
            "proposal_ids": ["mr-009"],
            "timeout": 600,
            "force": True,
        }
        payload.update(overrides)
        path = Path(self.temp.name) / "event.yaml"
        path.write_text(yaml.safe_dump(payload), encoding="utf-8")
        return EVENTS.load_event(path)

    def test_version_source_routes_to_production_with_the_file(self) -> None:
        event = self.load(bw_source="version", source_path="approved/mr-009-color.webp")
        command = event.command(live=False)
        self.assertIn("manage_coloring_book_production.py", command[1])
        self.assertNotIn("adopt_coloring_book_asset.py", " ".join(command))
        self.assertEqual(command[command.index("--bw-source") + 1], "version")
        self.assertEqual(command[command.index("--source-path") + 1], "approved/mr-009-color.webp")
        self.assertIn("--force", command)

    def test_prompt_source_routes_without_a_file(self) -> None:
        command = self.load(bw_source="prompt").command(live=False)
        self.assertEqual(command[command.index("--bw-source") + 1], "prompt")
        self.assertNotIn("--source-path", command)

    def test_events_without_bw_source_keep_the_old_command(self) -> None:
        command = self.load().command(live=False)
        self.assertNotIn("--bw-source", command)

    def test_invalid_combinations_are_refused(self) -> None:
        cases = [
            ({"bw_source": "version"}, "requires a source_path"),
            ({"bw_source": "prompt", "source_path": "approved/a.webp"}, "supported only"),
            ({"bw_source": "sketch"}, "bw_source must be one of"),
            ({"operation": "accept-bw", "force": False, "bw_source": "prompt"}, "only for generate-bw"),
            ({"bw_source": "version", "source_path": "../a.webp"}, "safe image path"),
        ]
        for overrides, message in cases:
            with self.subTest(overrides=overrides):
                with self.assertRaisesRegex(ValueError, message):
                    self.load(**overrides)


if __name__ == "__main__":
    unittest.main()
