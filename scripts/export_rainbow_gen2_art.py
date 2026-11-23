#!/usr/bin/env python3
"""Export the reviewed Gen-2 alternate-Act renders into the Rainbow cabinet (t-059).

WHY THIS EXISTS. The X1-X4 ledgers (GEN2-KELP-NEBULA-X1, GEN2-CORAL-COMET-X2, GEN2-ALT-GUARDIANS-1,
MIRROR-SHOAL-X4) hold DONE renders that never shipped: the Pearl Warden drew the Bulwark, the
Bellkeeper drew the Mirror Eel and the Herder and Shoal Koi fell back to a scaled scout. A DONE
ledger row is not delivery. SHIP below is the 2026-11-22 PT visual review: each keeper is keyed off
its #00ff00 matte with the Fever Dream exporter's key_green, trimmed, fitted and written to the
runtime path the cabinet resolves (``public/rainbow-princess-art/<path>.webp``). HOLD records what
the review kept out and why, so a later pass starts from the reason rather than a re-review.

Usage:
    python scripts/export_rainbow_gen2_art.py --kind-robots ../kind_robots [--cache DIR] [--dry-run]

Environment: KR_API_TOKEN, KR_BASE_URL (only to download renders not already in --cache).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

from export_rainbow_doodle_art import QUALITY, finished_id, fit_edge  # noqa: E402

ART = Path(__file__).resolve().parent.parent / "projects/rainbow-bullet-hell-space-princess/art"
LEDGERS = (
    "GEN2-KELP-NEBULA-X1.yaml",
    "GEN2-CORAL-COMET-X2.yaml",
    "GEN2-ALT-GUARDIANS-1.yaml",
    "MIRROR-SHOAL-X4.yaml",
)
GUARDIAN_EDGE = 256  # matches the shipped main-Act guardians (verifyRainbowGameArt: < 48 KB)
PICKUP_EDGE = 96  # matches the shipped pickups (verifyRainbowGameArt: < 16 KB)

# ledger subject key -> (runtime path under rainbow-princess-art, longest edge)
SHIP = {
    "rb2-kelp-warden-idle": ("enemies/guardian-kelp-warden", GUARDIAN_EDGE),
    "rb2-comet-herder-guardian": ("enemies/guardian-comet-herder", GUARDIAN_EDGE),
    "rb2-pearl-warden-guardian": ("enemies/guardian-pearl-warden", GUARDIAN_EDGE),
    "rb2-drowned-bellkeeper-guardian": ("enemies/guardian-bellkeeper", GUARDIAN_EDGE),
    "x4-shoal-koi-idle": ("enemies/guardian-shoal-koi", GUARDIAN_EDGE),
    "rb2-coral-choir-rescue-pod": ("pickups/coral-choir-pod", PICKUP_EDGE),
    "rb2-comet-cadet-rescue-pod": ("pickups/comet-cadet-pod", PICKUP_EDGE),
    "rb2-lighthouse-lamp-pickup": ("pickups/lighthouse-lamp", PICKUP_EDGE),
}

HOLD = {
    "rb2-kelp-warden-sweep": "identity drift: a slimmer hull and new tail, reads as a different creature from idle",
    "rb2-kelp-warden-hurt": "identity drift: darker armoured fish with dorsal spines, not the idle Kelp Warden",
    "x4-shoal-koi-telegraph": "pose frame; needs a runtime pose-swap hook before it can ship",
    "x4-shoal-koi-hurt": "pose frame; needs a runtime pose-swap hook before it can ship",
    "rb2-lashing-kelp-frond": "hazard art; X1 frond has no sprite hook yet",
    "rb2-comet-coral-asteroid": "hazard art; X2 asteroid has no sprite hook yet",
    "x4-mirror-shoal-card": "X4 plane set ships together with a stage-plane hook",
    "x4-shoal-far-nebula": "flat grey band across the lower third needs a crop decision",
    "x4-shoal-mid-shards": "X4 plane set ships together with a stage-plane hook",
    "x4-shoal-near-prisms": "X4 plane set ships together with a stage-plane hook",
    "x4-shoal-foreground": "X4 plane set ships together with a stage-plane hook",
}


def key_matte(image, near=48.0, far=110.0):
    """Key a soft studio matte of any tint to alpha.

    Krea 2 paints its "pure green" request as a muted, slightly uneven green (about rgb(60-120,
    170-205, 80-125)), which key_green's #00ff00 threshold leaves opaque. Sample the matte from the
    frame border, then key only background *connected to the border*: greens inside the creature
    survive. Alpha ramps from ``near`` to ``far`` colour distance across a 4 px edge band, green
    spill is pulled out of that band, and the fringe is eroded before trimming.
    """
    import numpy as np
    from PIL import Image, ImageDraw, ImageFilter

    rgb = np.asarray(image.convert("RGB")).astype(np.float32)
    h, w, _ = rgb.shape
    ring = np.concatenate([rgb[:6].reshape(-1, 3), rgb[-6:].reshape(-1, 3),
                           rgb[:, :6].reshape(-1, 3), rgb[:, -6:].reshape(-1, 3)])
    matte = np.median(ring, axis=0)
    dist = np.sqrt(((rgb - matte) ** 2).sum(axis=2))
    # Hard background mask, then keep only the part a flood from the border reaches.
    hard = Image.fromarray(((dist < near) * 255).astype(np.uint8), "L")
    pad = Image.new("L", (w + 2, h + 2), 255)
    pad.paste(hard, (1, 1))
    ImageDraw.floodfill(pad, (0, 0), 128)
    background = np.asarray(pad)[1:-1, 1:-1] == 128
    band = Image.fromarray((background * 255).astype(np.uint8), "L").filter(ImageFilter.MaxFilter(9))
    band = np.asarray(band) > 0
    alpha = np.ones((h, w), np.float32)
    alpha[band] = np.clip((dist[band] - near) / (far - near), 0, 1)
    alpha[background] = 0
    # Matte enclosed by the creature (between claws or tentacles) is not border-connected; key only
    # the pixels that are a near-exact match for the sampled matte, which creature greens are not.
    alpha[dist < near * 0.6] = 0
    # A render that cropped a fin or tail against the frame would show a hard straight edge: fade it.
    fade = 24
    ramp = np.linspace(0, 1, fade, dtype=np.float32)
    if (alpha[:, -1] > 0).mean() > 0.02:
        alpha[:, -fade:] *= ramp[::-1]
    if (alpha[:, 0] > 0).mean() > 0.02:
        alpha[:, :fade] *= ramp
    if (alpha[-1] > 0).mean() > 0.02:
        alpha[-fade:] *= ramp[::-1, None]
    if (alpha[0] > 0).mean() > 0.02:
        alpha[:fade] *= ramp[:, None]
    # Despill the soft edge: no channel greener than the brighter of red and blue.
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    spill = band & (g > np.maximum(r, b))
    rgb[..., 1] = np.where(spill, np.maximum(r, b), g)
    out = Image.fromarray(np.dstack([rgb, alpha * 255]).astype(np.uint8), "RGBA")
    out.putalpha(out.getchannel("A").filter(ImageFilter.MinFilter(3)))
    box = out.getbbox()
    return out.crop(box) if box else out


def subjects():
    for name in LEDGERS:
        for subject in yaml.safe_load((ART / name).read_text())["subjects"]:
            yield subject


def render(subject, cache: Path) -> Path:
    image_id = finished_id(subject)
    path = cache / f"{subject['key']}-{image_id}.png"
    if not path.exists():
        from export_shifting_lands_cards import load_image

        cache.mkdir(parents=True, exist_ok=True)
        load_image(image_id).save(path)
    return path


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--kind-robots", default="../kind_robots")
    parser.add_argument("--cache", default=".cache/rainbow-gen2")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    from PIL import Image

    out_root = Path(args.kind_robots) / "public/rainbow-princess-art"
    cache = Path(args.cache)
    seen = set()
    for subject in subjects():
        key = subject["key"]
        seen.add(key)
        if key in HOLD:
            print(f"hold  {key}: {HOLD[key]}")
            continue
        if key not in SHIP:
            print(f"skip  {key}: not reviewed", file=sys.stderr)
            continue
        if not finished_id(subject):
            print(f"wait  {key}: no DONE render", file=sys.stderr)
            continue
        rel, edge = SHIP[key]
        dest = out_root / f"{rel}.webp"
        if args.dry_run:
            print(f"ship  {key} -> {dest}")
            continue
        sprite = fit_edge(key_matte(Image.open(render(subject, cache))), edge)
        dest.parent.mkdir(parents=True, exist_ok=True)
        sprite.save(dest, "WEBP", quality=QUALITY, method=6)
        print(f"ship  {key} -> {dest} {sprite.size} {dest.stat().st_size} B")
    missing = (set(SHIP) | set(HOLD)) - seen
    if missing:
        print(f"unknown ledger keys: {sorted(missing)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
