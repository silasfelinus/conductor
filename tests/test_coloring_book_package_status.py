import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "coloring_book_package_status.py"
SPEC = importlib.util.spec_from_file_location("coloring_book_package_status", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class ColoringBookPackageStatusTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.original_root = MODULE.ROOT
        MODULE.ROOT = self.root

    def tearDown(self) -> None:
        MODULE.ROOT = self.original_root
        self.temp.cleanup()

    def write_yaml(self, relative: str, data: object) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            yaml.safe_dump(data, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )
        return path

    def touch(self, relative: str) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"image")

    def base_config(self) -> dict:
        return {
            "schema_version": 1,
            "project": "coloring-book",
            "requirements": {
                "interior_slots": 2,
                "print_interior_variant": "bw",
            },
            "books": [
                {
                    "order": 1,
                    "slug": "kind-robots",
                    "title": "Kind Robots",
                    "ledger_path": "projects/coloring-book/sets/kind-robots/proposals.yaml",
                    "cover_queue_path": "projects/coloring-book/cover-art-jobs.yaml",
                    "layout": {field: None for field in MODULE.LAYOUT_FIELDS},
                    "exports": {
                        "ordered_interior_manifest": "projects/coloring-book/packages/kind-robots/interiors.yaml",
                        "interior_pdf": None,
                        "cover_wrap_pdf": None,
                        "source_archive": None,
                    },
                }
            ],
        }

    def complete_ledger(self) -> dict:
        return {
            "proposals": [
                {
                    "slot": 1,
                    "id": "kr-001",
                    "title": "One",
                    "prompt": {"text": "Prompt one", "ref": None},
                    "final": {
                        "color": "approved/kr-001-color.webp",
                        "bw": "approved/kr-001-bw.webp",
                    },
                },
                {
                    "slot": 2,
                    "id": "kr-002",
                    "title": "Two",
                    "prompt": {"text": None, "ref": "prompt-source.yaml#kr-002"},
                    "final": {
                        "color": "approved/kr-002-color.webp",
                        "bw": "approved/kr-002-bw.webp",
                    },
                },
            ]
        }

    def cover_queue(self, status: str = "final", final_path: str | None = "approved/cover.webp") -> dict:
        return {
            "covers": [
                {
                    "book_slug": "kind-robots",
                    "status": status,
                    "final_path": final_path,
                }
            ]
        }

    def prepare_complete_sources(self) -> None:
        self.write_yaml(
            "projects/coloring-book/sets/kind-robots/proposals.yaml",
            self.complete_ledger(),
        )
        self.write_yaml(
            "projects/coloring-book/cover-art-jobs.yaml",
            self.cover_queue(),
        )
        for name in (
            "kr-001-color.webp",
            "kr-001-bw.webp",
            "kr-002-color.webp",
            "kr-002-bw.webp",
            "cover.webp",
        ):
            self.touch(f"projects/coloring-book/sets/kind-robots/approved/{name}")

    def test_complete_sources_without_layout_are_layout_needed(self) -> None:
        self.prepare_complete_sources()
        config = self.write_yaml("config.yaml", self.base_config())

        status = MODULE.build_status(config)
        book = status["books"][0]

        self.assertTrue(book["source_ready"])
        self.assertFalse(book["layout_ready"])
        self.assertFalse(book["exports_ready"])
        self.assertEqual(book["status"], "layout-needed")
        self.assertEqual(book["final_pair_count"], 2)
        self.assertEqual(len(book["missing_layout_fields"]), len(MODULE.LAYOUT_FIELDS))
        manifest = yaml.safe_load(
            (self.root / "projects/coloring-book/packages/kind-robots/interiors.yaml").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual([row["id"] for row in manifest["interiors"]], ["kr-001", "kr-002"])
        self.assertEqual(manifest["cover_source"], "approved/cover.webp")

    def test_complete_layout_without_exports_is_exports_needed(self) -> None:
        self.prepare_complete_sources()
        config_data = self.base_config()
        config_data["books"][0]["layout"] = {
            "trim_width_inches": 8,
            "trim_height_inches": 12,
            "bleed_inches": 0.125,
            "binding": "perfect-bound",
            "paper": "white-uncoated",
            "interior_color_mode": "grayscale",
            "cover_color_mode": "cmyk",
            "printer_template": "printer-template-v1.pdf",
            "page_count_includes_blanks": True,
            "inside_cover_printing": False,
            "barcode_area_reserved": True,
        }
        config = self.write_yaml("config.yaml", config_data)

        book = MODULE.build_status(config)["books"][0]

        self.assertTrue(book["source_ready"])
        self.assertTrue(book["layout_ready"])
        self.assertFalse(book["exports_ready"])
        self.assertEqual(book["status"], "exports-needed")

    def test_complete_sources_layout_and_exports_are_package_ready(self) -> None:
        self.prepare_complete_sources()
        config_data = self.base_config()
        config_data["books"][0]["layout"] = {
            "trim_width_inches": 8,
            "trim_height_inches": 12,
            "bleed_inches": 0.125,
            "binding": "perfect-bound",
            "paper": "white-uncoated",
            "interior_color_mode": "grayscale",
            "cover_color_mode": "cmyk",
            "printer_template": "printer-template-v1.pdf",
            "page_count_includes_blanks": True,
            "inside_cover_printing": False,
            "barcode_area_reserved": True,
        }
        exports = config_data["books"][0]["exports"]
        exports.update(
            {
                "interior_pdf": "projects/coloring-book/packages/kind-robots/interior.pdf",
                "cover_wrap_pdf": "projects/coloring-book/packages/kind-robots/cover-wrap.pdf",
                "source_archive": "projects/coloring-book/packages/kind-robots/source.zip",
            }
        )
        for relative in (
            exports["interior_pdf"],
            exports["cover_wrap_pdf"],
            exports["source_archive"],
        ):
            self.touch(relative)
        config = self.write_yaml("config.yaml", config_data)

        book = MODULE.build_status(config)["books"][0]

        self.assertTrue(book["package_ready"])
        self.assertEqual(book["status"], "package-ready")
        self.assertEqual(book["missing_export_fields"], [])

    def test_missing_slot_file_and_cover_remain_source_production(self) -> None:
        ledger = self.complete_ledger()
        ledger["proposals"] = [ledger["proposals"][0]]
        self.write_yaml(
            "projects/coloring-book/sets/kind-robots/proposals.yaml",
            ledger,
        )
        self.write_yaml(
            "projects/coloring-book/cover-art-jobs.yaml",
            self.cover_queue(status="approved", final_path=None),
        )
        self.touch("projects/coloring-book/sets/kind-robots/approved/kr-001-color.webp")
        config = self.write_yaml("config.yaml", self.base_config())

        book = MODULE.build_status(config)["books"][0]

        self.assertFalse(book["source_ready"])
        self.assertEqual(book["status"], "source-production")
        self.assertEqual(book["source_issues"]["missing_slots"], [2])
        self.assertEqual(book["source_issues"]["missing_bw_files"], ["kr-001"])
        self.assertTrue(book["source_issues"]["cover_not_final"])


if __name__ == "__main__":
    unittest.main()
