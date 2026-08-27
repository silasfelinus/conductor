"""Regression test for conductor/t-044 (2026-08-27): every entry
build_cthulhuquarium_art_queue.py writes must resolve OUTSIDE projects/process/,
the staging directory consume_art_queue_core.py renders into before
distribute_images.py ever runs.

The bug: image_path was `projects/process/cthulhuquarium-{name}.webp` -- the
exact staging path consume_art_queue_core.py's save_result()/staged_filename()
lands the rendered file at. distribute_images.py's resolve_abs_path() then
returned that same path, so dest.resolve() == src.resolve() for every one of
the batch's 138 entries: not a real destination, just the file matching
itself, which distribute_images.py can only recognize as a bogus
self-referential match and park in projects/process/unmatched/ -- never
delivered anywhere real (PR #2962). No test caught this before it cost a full
render cycle; this is that test.
"""
import yaml

import scripts.build_cthulhuquarium_art_queue as builder
from scripts.distribute_images import PROCESS_DIR, resolve_abs_path


def _rendered_entries():
    """Render the queue with one synthetic fish (no bible checkout needed in
    this sandbox) plus the script's real hard-coded non-fish assets -- the
    same `render()` call main() uses, so this exercises the actual code path.
    """
    text = builder.render(
        [("test-species", "a test species, hand-coloured lithograph plate")],
        builder.NON_FISH,
    )
    doc = yaml.safe_load(text)
    return doc["batch"]["entries"]


def test_no_entry_resolves_into_the_staging_directory():
    entries = _rendered_entries()
    assert entries, "render() produced no entries -- test is not exercising anything"

    process_dir = PROCESS_DIR.resolve()
    for entry in entries:
        dest = resolve_abs_path(entry["image_path"], entry.get("target_repo")).resolve()
        assert dest.parent != process_dir, (
            f"{entry['image_path']} resolves directly inside the staging "
            f"directory ({PROCESS_DIR}) that consume_art_queue_core.py stages "
            f"rendered files into. distribute_images.py's resolve_abs_path() "
            f"would then return the exact same path as the staged file, so it "
            f"can only ever be recognized as a bogus self-referential match "
            f"and parked in projects/process/unmatched/, never delivered "
            f"anywhere real (conductor/t-044)."
        )


def test_every_entry_names_a_real_destination_under_the_project():
    """Narrower than the staging check above: also pins the actual convention
    (projects/cthulhuquarium/art/) so a future edit that moves entries
    somewhere new has to update this test deliberately, not by accident.
    """
    for entry in _rendered_entries():
        assert entry["image_path"].startswith("projects/cthulhuquarium/art/"), entry
