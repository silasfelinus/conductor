#!/usr/bin/env python3
"""
art_quality.py — objective quality gate for generated art.

Two jobs:

1. **Guard** the automated pipeline: reject a render that structurally cannot be
   what was asked for — a "bw" coloring page that came back in full color, a
   "color" master that came back essentially monochrome (coloring-book/t-044),
   spatially-uncorrelated noise/static (coloring-book/t-039), a blank/degenerate
   frame, or the wrong aspect ratio. Called from consume_monster_recast_art.py
   before a variant is marked done, so failures stay pending instead of
   silently polluting the set (the mr-010/mr-013 bug).

2. **Curate**: score a folder of candidates so an agent can shortlist the ones
   worth promoting toward `approved/`. This is the objective first layer of the
   "let the AI approximate Silas's hand-picking" goal — it enforces the
   mechanical floor (is this a valid line-art page? not blank? right shape?).
   Aesthetic/subject-match judgement (does it *look* like the character, is the
   camp landing) is a vision-model pass layered on top — see `describe_gate()`.

The scoring math is pure Python over pixel statistics so it is testable without
PIL or any real image (`--selftest`). Pixel extraction uses PIL when available
(the same optional dep the live pipeline already needs to write webp); if PIL is
missing, image-file assessment is skipped with a clear warning rather than
crashing.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable, Optional

# Thresholds, tuned to the monster-recast approved/ set (line art is near-white
# with black ink; color masters are richly saturated). Conservative on purpose:
# the guard should only reject the clearly-wrong, never a borderline keeper.
BW_MAX_MEAN_SATURATION = 0.10      # line art is essentially greyscale
BW_MAX_COLORFUL_FRACTION = 0.04    # allow a few stray tinted pixels
BW_MIN_WHITE_FRACTION = 0.30       # a coloring page is mostly open white
COLORFUL_PIXEL_SATURATION = 0.20   # a pixel counts as "colorful" past this
BLANK_WHITE_FRACTION = 0.985       # near-all-white == blank
DEGENERATE_MAX_LUMA_STD = 0.02     # near-zero contrast == flat/dead frame
SAMPLE_EDGE = 160                  # downsample longest edge before sampling
NOISE_MIN_HF_RATIO = 0.55          # spatially-uncorrelated static, any variant
# A genuine color-stage master in this pipeline runs 0.20-0.60 mean_saturation
# and 0.43-0.95 colorful_fraction against the approved/ set (see
# coloring-book/t-044). An intermittent color-engine defect instead produces a
# structurally valid, non-blank, non-noise render with real contrast but almost
# no color at all — mr-006 (2026-09-07), mr-008 (2026-09-07 and again
# 2026-09-14), and mr-025 (2026-09-09) all measured mean_saturation ~0.01-0.02,
# colorful_fraction ~0.01-0.02, and silently passed the "color" gate as-is
# (only the blank/degenerate/noise/aspect checks applied to non-bw variants).
# Thresholds are set with wide margin below every observed legitimate color
# master so a real, if muted, illustration is never falsely rejected.
COLOR_MIN_MEAN_SATURATION = 0.06
COLOR_MIN_COLORFUL_FRACTION = 0.05


class Stats:
    """Aggregate pixel statistics, computed in one pass over (r,g,b) tuples."""

    def __init__(self) -> None:
        self.count = 0
        self._sat_sum = 0.0
        self._colorful = 0
        self._white = 0
        self._luma_sum = 0.0
        self._luma_sq_sum = 0.0

    def add(self, r: int, g: int, b: int) -> None:
        rf, gf, bf = r / 255.0, g / 255.0, b / 255.0
        mx = max(rf, gf, bf)
        mn = min(rf, gf, bf)
        sat = 0.0 if mx == 0 else (mx - mn) / mx
        luma = 0.2126 * rf + 0.7152 * gf + 0.0722 * bf
        self.count += 1
        self._sat_sum += sat
        if sat >= COLORFUL_PIXEL_SATURATION:
            self._colorful += 1
        if luma >= 0.90 and sat <= 0.06:
            self._white += 1
        self._luma_sum += luma
        self._luma_sq_sum += luma * luma

    @property
    def mean_saturation(self) -> float:
        return 0.0 if not self.count else self._sat_sum / self.count

    @property
    def colorful_fraction(self) -> float:
        return 0.0 if not self.count else self._colorful / self.count

    @property
    def white_fraction(self) -> float:
        return 0.0 if not self.count else self._white / self.count

    @property
    def luma_std(self) -> float:
        if not self.count:
            return 0.0
        mean = self._luma_sum / self.count
        var = max(0.0, self._luma_sq_sum / self.count - mean * mean)
        return var ** 0.5

    def as_dict(self) -> dict:
        return {
            "pixels": self.count,
            "mean_saturation": round(self.mean_saturation, 4),
            "colorful_fraction": round(self.colorful_fraction, 4),
            "white_fraction": round(self.white_fraction, 4),
            "luma_std": round(self.luma_std, 4),
        }


def stats_from_pixels(pixels: Iterable[tuple[int, int, int]]) -> Stats:
    s = Stats()
    for px in pixels:
        s.add(px[0], px[1], px[2])
    return s


def hf_energy_ratio(pixels: list[tuple[int, int, int]], width: int) -> float:
    """Ratio of adjacent-pixel luma variance to total luma variance, in
    [0, row-major] order over a `width`-wide image.

    Real imagery — line art, flat color, gradients, painted detail — has
    strong positive correlation between neighboring pixels: a pixel's luma is
    a good predictor of the one next to it, so the mean squared horizontal
    difference is small relative to the image's overall luma variance.
    Spatially-uncorrelated static has none of that structure: each pixel is
    effectively independent of its neighbor, so for iid values
    Var(X - Y) == 2*Var(X), making this ratio approach 1.0. A ratio near or
    above 1.0 means the frame has no discernible spatial structure at all —
    exactly the Kontext-corruption noise signature `coloring-book/t-039`
    found slipping past every saturation/white-fraction check, since static
    can be arbitrarily saturated and busy while still being pure garbage.

    Returns 0.0 (i.e. "not noise") when there isn't enough signal to judge —
    too few rows, or near-zero variance (a blank/flat frame, already caught
    by `is_blank_or_degenerate`).
    """
    n = len(pixels)
    if width <= 1 or n < width * 2:
        return 0.0
    lumas = [0.2126 * r / 255.0 + 0.7152 * g / 255.0 + 0.0722 * b / 255.0
              for r, g, b in pixels]
    mean = sum(lumas) / n
    variance = sum((l - mean) ** 2 for l in lumas) / n
    if variance <= 1e-9:
        return 0.0
    diff_sq_sum = 0.0
    diff_count = 0
    for row_start in range(0, n - width + 1, width):
        row = lumas[row_start:row_start + width]
        for i in range(len(row) - 1):
            d = row[i + 1] - row[i]
            diff_sq_sum += d * d
            diff_count += 1
    if diff_count == 0:
        return 0.0
    return (diff_sq_sum / diff_count) / (2.0 * variance)


def is_blank_or_degenerate(stats: Stats) -> bool:
    """Blank page or a flat/dead frame with no real content."""
    if stats.count == 0:
        return True
    if stats.white_fraction >= BLANK_WHITE_FRACTION:
        return True
    return stats.luma_std <= DEGENERATE_MAX_LUMA_STD


def is_line_art(stats: Stats) -> bool:
    """Structurally a black-on-white coloring page: near-greyscale, few colorful
    pixels, and plenty of open white to color into."""
    return (
        stats.mean_saturation <= BW_MAX_MEAN_SATURATION
        and stats.colorful_fraction <= BW_MAX_COLORFUL_FRACTION
        and stats.white_fraction >= BW_MIN_WHITE_FRACTION
    )


def assess(stats: Stats, variant: str, size: Optional[tuple[int, int]] = None,
           expect_portrait: bool = True,
           hf_ratio: Optional[float] = None) -> tuple[bool, list[str]]:
    """Return (ok, reasons). `reasons` explains every failure; empty on pass.

    variant: 'bw' enforces line-art; anything else ('color') only enforces the
    not-blank / not-degenerate floor. Aspect is checked when size is provided.
    `hf_ratio` (from `hf_energy_ratio`) is optional — callers that only have
    aggregate Stats with no pixel positions (e.g. the pure self-test blocks)
    simply skip the noise/static check by leaving it None.
    """
    reasons: list[str] = []

    if is_blank_or_degenerate(stats):
        reasons.append(
            f"blank/degenerate frame (white={stats.white_fraction:.2f}, "
            f"contrast_std={stats.luma_std:.3f})"
        )

    if hf_ratio is not None and hf_ratio >= NOISE_MIN_HF_RATIO:
        reasons.append(
            "spatially-uncorrelated noise/static — no discernible image "
            f"structure (hf_ratio={hf_ratio:.2f}); this can pass the "
            "saturation/white-fraction checks for either variant while "
            "being pure garbage (coloring-book/t-039)"
        )

    if variant == "bw" and not is_line_art(stats):
        reasons.append(
            "not black-and-white line art — came back colored/shaded "
            f"(mean_saturation={stats.mean_saturation:.2f}, "
            f"colorful_fraction={stats.colorful_fraction:.2f}, "
            f"white_fraction={stats.white_fraction:.2f})"
        )

    if (
        variant != "bw"
        and stats.mean_saturation < COLOR_MIN_MEAN_SATURATION
        and stats.colorful_fraction < COLOR_MIN_COLORFUL_FRACTION
    ):
        reasons.append(
            "rendered essentially monochrome/desaturated for a color-stage "
            f"master (mean_saturation={stats.mean_saturation:.3f}, "
            f"colorful_fraction={stats.colorful_fraction:.3f}) — intermittent "
            "color-engine defect, coloring-book/t-044"
        )

    if size and expect_portrait:
        w, h = size
        if w > 0 and h > 0 and h < w:
            reasons.append(f"landscape output {w}x{h} where portrait was expected")

    return (not reasons), reasons


# ---------------------------------------------------------------------------
# PIL-backed image loading (optional dependency)
# ---------------------------------------------------------------------------

_pil_missing_warned = False


def load_stats(path: Path) -> Optional[tuple[Stats, tuple[int, int], float]]:
    """Sample an image file into Stats + (width, height) + hf_ratio (see
    `hf_energy_ratio`). Returns None if PIL is unavailable (caller decides
    whether that's fatal)."""
    global _pil_missing_warned
    try:
        from PIL import Image
    except ImportError:
        if not _pil_missing_warned:
            _pil_missing_warned = True
            print(
                "art_quality.py: Pillow is not installed in this environment — "
                "image guards will be skipped for every file until it's added "
                "(pip3 install Pillow).",
                file=sys.stderr,
            )
        return None
    with Image.open(path) as im:
        size = im.size
        im = im.convert("RGB")
        longest = max(im.size)
        if longest > SAMPLE_EDGE:
            scale = SAMPLE_EDGE / longest
            im = im.resize((max(1, int(im.width * scale)),
                            max(1, int(im.height * scale))))
        sampled_pixels = list(im.getdata())
        stats = stats_from_pixels(sampled_pixels)
        hf_ratio = hf_energy_ratio(sampled_pixels, im.width)
    return stats, size, hf_ratio


def assess_file(path: Path, variant: str) -> tuple[Optional[bool], list[str], dict]:
    """(ok, reasons, stats_dict). ok is None when PIL is unavailable."""
    loaded = load_stats(path)
    if loaded is None:
        return None, ["PIL unavailable — image guard skipped"], {}
    stats, size, hf_ratio = loaded
    ok, reasons = assess(stats, variant, size=size, hf_ratio=hf_ratio)
    info = stats.as_dict()
    info["size"] = f"{size[0]}x{size[1]}"
    info["hf_ratio"] = round(hf_ratio, 4)
    return ok, reasons, info


def describe_gate() -> str:
    return (
        "Objective gate only: validates that a render is structurally what was "
        "asked for (bw==line art, color==actually has color, not blank, not "
        "spatially-uncorrelated noise, portrait). It does NOT judge likeness, "
        "camp, or composition — that is a vision-model pass layered on top "
        "before anything is promoted to approved/."
    )


# ---------------------------------------------------------------------------
# CLI: audit a folder, or self-test the pure logic without PIL/images
# ---------------------------------------------------------------------------

def _variant_from_path(path: Path) -> str:
    parts = {p.lower() for p in path.parts}
    if "bw" in parts or path.stem.endswith("-bw"):
        return "bw"
    return "color"


def _audit(folder: Path) -> int:
    images = sorted(
        p for p in folder.rglob("*")
        if p.suffix.lower() in (".webp", ".png", ".jpg", ".jpeg")
    )
    if not images:
        print(f"No images under {folder}")
        return 0
    any_pil = False
    fails = 0
    for path in images:
        variant = _variant_from_path(path)
        ok, reasons, info = assess_file(path, variant)
        if ok is None:
            print(f"  SKIP  {path.relative_to(folder)} ({reasons[0]})")
            continue
        any_pil = True
        mark = "PASS " if ok else "FAIL "
        if not ok:
            fails += 1
        detail = info.get("size", "") + (f"  {'; '.join(reasons)}" if reasons else "")
        print(f"  {mark}[{variant:5}] {path.relative_to(folder)}  {detail}")
    if not any_pil:
        print("\nPIL not installed — install Pillow to audit real image files.")
        return 0
    print(f"\n{len(images)} image(s); {fails} failed the objective gate.")
    print(describe_gate())
    return 1 if fails else 0


def _selftest() -> int:
    """Verify the pure classifier on synthetic pixel sets — no PIL, no files."""
    def block(color, n=1000):
        return [color] * n

    # 1. Clean line art: mostly white with ~20% black ink lines.
    line_art = stats_from_pixels(block((255, 255, 255), 800) + block((10, 10, 10), 200))
    # 2. A color master (rich saturated illustration).
    color_master = stats_from_pixels(
        block((200, 30, 40), 350) + block((30, 120, 200), 350) + block((240, 200, 40), 300)
    )
    # 3. The bug: a "bw" slot that came back as a saturated color image.
    color_in_bw = color_master
    # 4. Blank page.
    blank = stats_from_pixels(block((255, 255, 255), 1000))

    checks = []
    ok, _ = assess(line_art, "bw"); checks.append(("line_art passes bw gate", ok is True))
    ok, _ = assess(color_master, "color"); checks.append(("color_master passes color gate", ok is True))
    ok, r = assess(color_in_bw, "bw"); checks.append(("color-in-bw is REJECTED", ok is False and any("line art" in x for x in r)))
    ok, r = assess(blank, "color"); checks.append(("blank is REJECTED", ok is False and any("blank" in x for x in r)))
    ok, r = assess(line_art, "color", size=(1024, 700)); checks.append(("landscape flagged when portrait expected", any("landscape" in x for x in r)))
    checks.append(("is_line_art(line_art)", is_line_art(line_art) is True))
    checks.append(("not is_line_art(color)", is_line_art(color_master) is False))

    # 5. Spatially-uncorrelated static (coloring-book/t-039): saturated and
    #    busy per-pixel, so it clears every existing check for the "color"
    #    variant, but adjacent pixels carry no information about each other.
    #    Deterministic checkerboard alternation is enough to prove the math —
    #    real noise just makes the failure mode less visually obvious, not
    #    less spatially uncorrelated.
    noise_width = 40
    noise_pixels = [
        (220, 40, 200) if (i % noise_width + i // noise_width) % 2 == 0 else (30, 210, 60)
        for i in range(noise_width * 40)
    ]
    noise_stats = stats_from_pixels(noise_pixels)
    noise_hf = hf_energy_ratio(noise_pixels, noise_width)
    checks.append(("noise/static hf_ratio is high", noise_hf >= NOISE_MIN_HF_RATIO))
    ok, r = assess(noise_stats, "color", hf_ratio=noise_hf)
    checks.append(("noise/static is REJECTED for color variant", ok is False and any("noise/static" in x for x in r)))

    # A real, structured illustration (smooth horizontal gradient — strong
    # pixel-to-pixel correlation) must NOT trip the same check.
    grad_width = 40
    grad_pixels = [
        (int(255 * ((i % grad_width) / (grad_width - 1))), 60, 160)
        for i in range(grad_width * 40)
    ]
    grad_stats = stats_from_pixels(grad_pixels)
    grad_hf = hf_energy_ratio(grad_pixels, grad_width)
    checks.append(("smooth gradient hf_ratio stays low", grad_hf < NOISE_MIN_HF_RATIO))
    ok, r = assess(grad_stats, "color", hf_ratio=grad_hf)
    checks.append(("smooth gradient is NOT rejected as noise", ok is True))

    # 6. Intermittent color-engine defect (coloring-book/t-044): a structurally
    #    valid, non-blank render with real contrast but almost no color at all —
    #    mostly near-grey pixels with a little luma variation, nothing close to
    #    a real color master's saturation. Must be REJECTED for "color" but
    #    still cleanly PASS "bw" (a near-greyscale image is exactly what a bw
    #    variant wants).
    desaturated = stats_from_pixels(
        block((235, 233, 230), 600) + block((90, 88, 86), 300) + block((150, 149, 147), 100)
    )
    ok, r = assess(desaturated, "color")
    checks.append(("near-monochrome color-stage render is REJECTED", ok is False and any("monochrome" in x for x in r)))
    ok, _ = assess(desaturated, "bw")
    checks.append(("same near-monochrome pixels still pass the bw gate", ok is True))
    # A real, muted-but-genuine color master (well above threshold, still far
    # below the approved/ set's typical saturation) must not be caught by this.
    ok, r = assess(color_master, "color")
    checks.append(("real color_master is NOT rejected as desaturated", ok is True))

    failed = 0
    for name, passed in checks:
        print(f"  {'ok  ' if passed else 'FAIL'} {name}")
        if not passed:
            failed += 1
    print(f"\n{len(checks) - failed}/{len(checks)} self-test checks passed.")
    return 1 if failed else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", help="folder of images to audit")
    parser.add_argument("--selftest", action="store_true", help="run pure-logic self-test (no PIL needed)")
    args = parser.parse_args()

    if args.selftest:
        return _selftest()
    if not args.path:
        parser.print_help()
        return 0
    return _audit(Path(args.path))


if __name__ == "__main__":
    raise SystemExit(main())
