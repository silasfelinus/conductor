"""read_regions must parse the t-054 regions manifest: decay ramps declare their
states as `driver: { ramp: [...] }` and a `pins` list follows the inner map.
Before the fix the layer lane exited with "no regions manifest found", so its
52 rows could not be checked or restaged."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import build_ruler_hooked_art_queue as builder  # noqa: E402

CONTENT = """export const BUNDLE = {
  contentVersion: 'test',

  regions: {
    regions: {
      sky: {
        z: 0,
        driver: { slider: 'joy', ramp: ['choked', 'overcast', 'open'] },
        times: ['day', 'night'],
      },
      far_shore: {
        z: 1,
        states: ['pristine', 'farmed'],
        times: ['day'],
      },
    },
    pins: [
      {
        id: 'tyranny',
        states: { far_shore: 'gallows' },
      },
    ],
  },
}
"""


def test_reads_ramps_and_tolerates_pins(tmp_path: Path) -> None:
    content = tmp_path / "content.ts"
    content.write_text(CONTENT, encoding="utf-8")
    regions = builder.read_regions(content)
    assert regions["sky"]["states"][:3] == ["choked", "overcast", "open"]
    assert regions["sky"]["times"] == ["day", "night"]
    assert regions["far_shore"]["states"][:2] == ["pristine", "farmed"]
