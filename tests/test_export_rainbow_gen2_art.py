"""t-059: the Gen-2 exporter keys Krea's muted matte and covers every Gen-2 ledger subject."""

import sys
from pathlib import Path

import numpy as np
import pytest
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import export_rainbow_gen2_art as gen2  # noqa: E402

MATTE = (96, 182, 102)  # the muted "pure green" Krea 2 actually paints


def creature(touch_right=False):
    """A pink disc on a noisy muted-green matte, with a pocket of matte enclosed by a pink ring."""
    rng = np.random.default_rng(7)
    a = np.empty((200, 300, 3), np.float32)
    a[:] = MATTE
    a += rng.normal(0, 4, a.shape)
    yy, xx = np.mgrid[:200, :300]
    disc = (xx - 120) ** 2 + (yy - 100) ** 2 < 60 ** 2
    a[disc] = (240, 120, 190)
    pocket = (xx - 120) ** 2 + (yy - 100) ** 2 < 12 ** 2
    a[pocket] = MATTE  # enclosed matte: must still key
    teal = (xx - 150) ** 2 + (yy - 100) ** 2 < 8 ** 2
    a[teal] = (60, 200, 170)  # a creature's own teal/green: must survive
    if touch_right:
        a[90:110, 180:] = (240, 120, 190)  # a tail cropped by the frame
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")


def test_key_matte_clears_border_and_enclosed_matte_but_keeps_creature_greens():
    out = gen2.key_matte(creature())
    alpha = np.asarray(out.getchannel("A"))
    assert out.size[0] < 140 and out.size[1] < 140, "trimmed to the creature"
    h, w = alpha.shape
    assert alpha[h // 2, w // 2] == 0, "enclosed matte pocket is keyed"
    assert alpha[h // 2, w // 2 + 30] == 255, "the creature's own teal survives"
    assert alpha[h // 2, w // 2 - 40] == 255, "the creature body is opaque"
    rgba = np.asarray(out)
    edge = rgba[(alpha > 0) & (alpha < 255)]
    assert (edge[:, 1] <= np.maximum(edge[:, 0], edge[:, 2]) + 1).all(), "no green spill on the soft edge"


def test_key_matte_fades_a_tail_the_render_cropped():
    out = gen2.key_matte(creature(touch_right=True))
    alpha = np.asarray(out.getchannel("A"))
    assert alpha[:, -1].max() < 40, "the cropped edge fades instead of cutting hard"


def test_every_gen2_ledger_subject_is_reviewed():
    keys = {s["key"] for s in gen2.subjects()}
    assert set(gen2.SHIP) | set(gen2.HOLD) == keys
    assert not set(gen2.SHIP) & set(gen2.HOLD)


@pytest.mark.parametrize("key", sorted(gen2.SHIP))
def test_shipped_paths_match_the_cabinet_folders(key):
    rel, edge = gen2.SHIP[key]
    assert rel.split("/")[0] in {"enemies", "pickups"}
    assert edge in {gen2.GUARDIAN_EDGE, gen2.PICKUP_EDGE}
