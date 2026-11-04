"""Coloring Book Studio render settings: engine, checkpoint and LoRA per page.

Silas, 2026-11-04 PT: "I should be able to ... change the checkpoint or select a
coloring book lora."
"""

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import coloring_render_settings as settings  # noqa: E402
import dream_sdxl_checkpoint_art as sdxl  # noqa: E402


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


EVENTS = _load("process_coloring_art_events")


class NormalizeTests(unittest.TestCase):
    def test_defaults_to_krea2_and_clears_everything_else(self) -> None:
        self.assertEqual(
            settings.normalize({}),
            {"engine": "krea2", "checkpoint": None, "lora": None, "lora_strength": None},
        )

    def test_sdxl_requires_a_checkpoint(self) -> None:
        with self.assertRaises(ValueError):
            settings.normalize({"engine": "sdxl-checkpoint"})
        result = settings.normalize({
            "engine": "sdxl-checkpoint",
            "checkpoint": "Illustrious/arthemyWesternArt_v30.safetensors",
            "lora": "coloring/line-art.safetensors",
            "lora_strength": "0.8",
        })
        self.assertEqual(result["checkpoint"], "Illustrious/arthemyWesternArt_v30.safetensors")
        self.assertEqual(result["lora_strength"], 0.8)

    def test_checkpoint_is_dropped_for_non_checkpoint_engines(self) -> None:
        result = settings.normalize({"engine": "krea2", "checkpoint": "x.safetensors"})
        self.assertIsNone(result["checkpoint"])

    def test_rejects_unsafe_names_unknown_fields_and_bad_strength(self) -> None:
        for raw in (
            {"engine": "a1111"},
            {"engine": "krea2", "lora": "../../etc/passwd.safetensors"},
            {"engine": "krea2", "lora": "/abs/path.safetensors"},
            {"engine": "krea2", "lora": "notes.txt"},
            {"engine": "krea2", "lora": "ok.safetensors", "lora_strength": 5},
            {"engine": "krea2", "steps": 99},
        ):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                settings.normalize(raw)

    def test_apply_sets_and_clears_queue_fields(self) -> None:
        source = {"id": "mr-001", "engine": "krea2", "lora": "old.safetensors", "lora_strength": 1.0}
        changed = settings.apply(source, settings.normalize({
            "engine": "sdxl-checkpoint", "checkpoint": "Illustrious/a.safetensors",
        }))
        self.assertTrue(changed)
        self.assertEqual(source, {
            "id": "mr-001", "engine": "sdxl-checkpoint", "checkpoint": "Illustrious/a.safetensors",
        })
        self.assertFalse(settings.apply(source, settings.normalize({
            "engine": "sdxl-checkpoint", "checkpoint": "Illustrious/a.safetensors",
        })))


class EventTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "event.yaml"

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write(self, **extra: object) -> Path:
        payload = {
            "version": 1,
            "operation": "generate-color-proposals",
            "book": "hollywood-recast",
            "proposal_ids": ["hwr-007"],
            "timeout": 600,
            "force": True,
        }
        payload.update(extra)
        self.path.write_text(yaml.safe_dump(payload), encoding="utf-8")
        return self.path

    def test_render_settings_reach_the_studio_consumer(self) -> None:
        event = EVENTS.load_event(self.write(render_settings={
            "engine": "sdxl-checkpoint",
            "checkpoint": "Illustrious/arthemyWesternArt_v30.safetensors",
            "lora": None,
            "lora_strength": None,
        }))
        command = event.command(live=True)
        flag = command.index("--render-settings")
        self.assertEqual(json.loads(command[flag + 1])["engine"], "sdxl-checkpoint")

    def test_render_settings_only_on_color_generation(self) -> None:
        with self.assertRaises(ValueError):
            EVENTS.load_event(self.write(
                operation="generate-bw", render_settings={"engine": "krea2"},
            ))

    def test_events_without_settings_are_unchanged(self) -> None:
        command = EVENTS.load_event(self.write()).command(live=False)
        self.assertNotIn("--render-settings", command)


class FakeCore:
    @staticmethod
    def _load_resource_index():
        return {
            "CHECKPOINT": {"arthemywesternart_v30.safetensors": "Illustrious/arthemyWesternArt_v30.safetensors"},
            "LORA": {},
        }

    @staticmethod
    def parse_size(size):
        width, height = str(size or "1024x1536").split("x")
        return int(width), int(height)

    @staticmethod
    def resolve_seed(seed):
        return 1234 if seed is None else int(seed)


class NamedCheckpointJobTests(unittest.TestCase):
    def test_builds_sdxl_graph_with_lora_and_portrait_bucket(self) -> None:
        job = sdxl.make_named_checkpoint_job({
            "project": "coloring-book",
            "engine": "sdxl-checkpoint",
            "checkpoint": "arthemyWesternArt_v30.safetensors",
            "lora": "coloring/line-art.safetensors",
            "lora_strength": 0.7,
            "prompt": "A jolly bearded Scotsman over a subway grate.",
            "size": "1024x1536",
        }, FakeCore)
        payload = job["payload"]
        graph = payload["workflow"]
        self.assertEqual(graph["1"]["inputs"]["ckpt_name"], "Illustrious/arthemyWesternArt_v30.safetensors")
        self.assertEqual(graph["9"]["class_type"], "LoraLoader")
        self.assertEqual(graph["9"]["inputs"]["lora_name"], "coloring/line-art.safetensors")
        self.assertEqual(graph["5"]["inputs"]["model"], ["9", 0])
        self.assertEqual(graph["8"]["inputs"]["clip"], ["9", 1])
        self.assertEqual((payload["width"], payload["height"]), (832, 1216))
        self.assertTrue(payload["promptString"].startswith(sdxl.ILLUSTRIOUS_PREFIX))
        self.assertEqual(job["resolvedSeed"], 1234)

    def test_without_lora_the_checkpoint_feeds_the_sampler(self) -> None:
        job = sdxl.make_named_checkpoint_job({
            "checkpoint": "Illustrious/arthemyWesternArt_v30.safetensors",
            "prompt": "page",
        }, FakeCore)
        graph = job["payload"]["workflow"]
        self.assertNotIn("9", graph)
        self.assertEqual(graph["5"]["inputs"]["model"], ["1", 0])


if __name__ == "__main__":
    unittest.main()
