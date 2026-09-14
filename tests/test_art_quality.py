"""Regression fixture for art_quality.py's calibrated thresholds (BW_*,
COLOR_MIN_*, TINT_*), pinned against the real monster-recast/approved/ corpus
(coloring-book/t-046, kaizen from t-045).

t-045's tint-concentration check went through two discarded signal designs
before landing on the one now in production, and both discards were only
caught because someone thought to test against the real
monster-recast/approved/ corpus by hand -- art_quality.py had no automated
test file at all, only the pure-synthetic `--selftest` CLI check (see that
function's own docstring for the synthetic-only coverage this file adds to).

This pins each real file's pixel statistics as a frozen fixture rather than
loading images at test time, because the suite's main CI job
(`pytest-suite` in .github/workflows/ci.yml) runs `pytest tests/` without
installing Pillow -- art_quality.py's own module docstring says the scoring
math is "pure Python over pixel statistics so it is testable without PIL or
any real image", and this file relies on exactly that property to stay
collectible there. `_pinned_stats()` reconstructs an `art_quality.Stats`
instance that reports the frozen aggregate values without needing any
per-pixel data.

Fixture values were captured once via:
    python3 -c "
    from scripts import art_quality as aq
    from pathlib import Path
    ok, reasons, info = aq.assess_file(Path('<file>'), '<variant>')
    print(info)
    "
against the actual files checked into this repo (Pillow 12.3.0). If
art_quality.py's sampling math changes, or a fixture file is replaced with a
new render, re-derive these numbers from the real file rather than
hand-editing them -- `test_live_*_match_frozen_fixtures` below does exactly
that recomputation automatically whenever Pillow is installed, and fails
loudly if a checked-in image has drifted from what this file expects.

Real corpus checked: every approved/*-bw.webp master (17, BW_* thresholds),
every approved/*-color.webp master (10, COLOR_MIN_*/TINT_* thresholds), and
the two known-bad rejects those color thresholds exist to catch. Testing the
bw set against real data surfaced a genuine miscalibration this file also
fixes: BW_MIN_WHITE_FRACTION was 0.30, which would have rejected 4 of the 17
real approved bw masters (dense/heavily-shaded line art, still genuinely
black-and-white) -- see art_quality.py's own comment on that constant for
the corrected value and margin.
"""

from __future__ import annotations

from pathlib import Path

import pytest

import scripts.art_quality as aq

REPO_ROOT = Path(__file__).resolve().parents[1]
APPROVED_DIR = (
    REPO_ROOT / "projects" / "coloring-book" / "sets" / "monster-recast" / "approved"
)

# Every approved/*-bw.webp master in the Monster Recast corpus (17 files,
# 2026-09-14). Each must PASS the bw line-art gate (BW_MAX_MEAN_SATURATION,
# BW_MAX_COLORFUL_FRACTION, BW_MIN_WHITE_FRACTION).
APPROVED_BW_MASTERS = {
    "alien-king-bw.webp": dict(mean_saturation=0.0006, colorful_fraction=0.0, white_fraction=0.2153, luma_std=0.2103),
    "carpet-unraveled-bw.webp": dict(mean_saturation=0.0004, colorful_fraction=0.0, white_fraction=0.4586, luma_std=0.1733),
    "draculina-bw.webp": dict(mean_saturation=0.0024, colorful_fraction=0.0029, white_fraction=0.2478, luma_std=0.3245),
    "fly-beach-bw.webp": dict(mean_saturation=0.0003, colorful_fraction=0.0, white_fraction=0.6448, luma_std=0.1077),
    "frieda-krueger-bw.webp": dict(mean_saturation=0.0002, colorful_fraction=0.0, white_fraction=0.5563, luma_std=0.1834),
    "gothic-schoolgirl-bw.webp": dict(mean_saturation=0.0004, colorful_fraction=0.0, white_fraction=0.4497, luma_std=0.0899),
    "hush-darling-bw.webp": dict(mean_saturation=0.0011, colorful_fraction=0.0010, white_fraction=0.4198, luma_std=0.3322),
    "masked-bath-bw.webp": dict(mean_saturation=0.0002, colorful_fraction=0.0, white_fraction=0.6314, luma_std=0.1978),
    "masked-countess-bw.webp": dict(mean_saturation=0.0004, colorful_fraction=0.0, white_fraction=0.4061, luma_std=0.1199),
    "masking-up-bw.webp": dict(mean_saturation=0.0011, colorful_fraction=0.0007, white_fraction=0.1633, luma_std=0.2511),
    "moon-torn-bw.webp": dict(mean_saturation=0.0004, colorful_fraction=0.0, white_fraction=0.4641, luma_std=0.2097),
    "perfect-woman-bw.webp": dict(mean_saturation=0.0015, colorful_fraction=0.0006, white_fraction=0.1876, luma_std=0.2202),
    "pound-foolish-bw.webp": dict(mean_saturation=0.0010, colorful_fraction=0.0007, white_fraction=0.4054, luma_std=0.2820),
    "prom-king-bw.webp": dict(mean_saturation=0.0004, colorful_fraction=0.0, white_fraction=0.3508, luma_std=0.1148),
    "screwhead-bw.webp": dict(mean_saturation=0.0006, colorful_fraction=0.0002, white_fraction=0.3780, luma_std=0.2045),
    "tv-boy-bw.webp": dict(mean_saturation=0.0004, colorful_fraction=0.0001, white_fraction=0.5646, luma_std=0.1594),
    "victorian-barber-bw.webp": dict(mean_saturation=0.0004, colorful_fraction=0.0, white_fraction=0.4027, luma_std=0.1232),
}

# Every approved/*-color.webp master in the Monster Recast corpus (10 files,
# 2026-09-14). Each must PASS the color gate: real color, not a single-hue
# tint/wash.
APPROVED_COLOR_MASTERS = {
    "fly-beach-color.webp": dict(
        mean_saturation=0.4914, colorful_fraction=0.9517, luma_std=0.2064,
        tint_concentration=0.7154,
    ),
    "freida-krueger-color.webp": dict(
        mean_saturation=0.5577, colorful_fraction=0.8702, luma_std=0.1809,
        tint_concentration=None,
    ),
    "gothic-schoolgirl-color.webp": dict(
        mean_saturation=0.3414, colorful_fraction=0.6701, luma_std=0.1884,
        tint_concentration=0.5277,
    ),
    "masked-countess-color.webp": dict(
        mean_saturation=0.4997, colorful_fraction=0.8602, luma_std=0.1498,
        tint_concentration=0.8688,
    ),
    "masking-up-color.webp": dict(
        mean_saturation=0.4372, colorful_fraction=0.8713, luma_std=0.1209,
        tint_concentration=0.0755,
    ),
    "perfect-woman-color.webp": dict(
        mean_saturation=0.4240, colorful_fraction=0.9133, luma_std=0.1493,
        tint_concentration=0.2376,
    ),
    "prom-king-color.webp": dict(
        mean_saturation=0.3760, colorful_fraction=0.6335, luma_std=0.1508,
        tint_concentration=0.7132,
    ),
    "tricycle-doll-color.webp": dict(
        mean_saturation=0.5975, colorful_fraction=0.9199, luma_std=0.1437,
        tint_concentration=0.7189,
    ),
    "tv-boy-color.webp": dict(
        mean_saturation=0.4229, colorful_fraction=0.8262, luma_std=0.1717,
        tint_concentration=0.7822,
    ),
    "victorian-barber-color.webp": dict(
        mean_saturation=0.4284, colorful_fraction=0.8700, luma_std=0.1821,
        tint_concentration=0.3728,
    ),
}

# The known-bad examples the tint-concentration check exists to catch
# (coloring-book/t-045's own docstring names both by id). Both still live in
# the repo as real rejected color-stage renders and both must FAIL the color
# gate specifically on the tint/wash check.
KNOWN_BAD_DIR_MR = (
    REPO_ROOT / "projects" / "coloring-book" / "sets" / "monster-recast"
    / "generated" / "color-proposals-v1"
)
KNOWN_BAD_DIR_HWR = (
    REPO_ROOT / "projects" / "coloring-book" / "sets" / "hollywood-recast"
    / "generated" / "color-proposals-v1"
)
KNOWN_BAD = {
    "mr-025-little-miss-omen.webp": dict(
        path=KNOWN_BAD_DIR_MR / "mr-025-little-miss-omen.webp",
        mean_saturation=0.2812, colorful_fraction=0.3496, luma_std=0.3826,
        tint_concentration=0.9889,
    ),
    "hwr-021-the-silent-mechanic.webp": dict(
        path=KNOWN_BAD_DIR_HWR / "hwr-021-the-silent-mechanic.webp",
        mean_saturation=0.2878, colorful_fraction=0.6124, luma_std=0.2989,
        tint_concentration=0.9458,
    ),
}


def _pinned_stats(mean_saturation: float, colorful_fraction: float,
                   luma_std: float, white_fraction: float = 0.0) -> aq.Stats:
    """Build an `art_quality.Stats` that reports the given aggregate values
    without any real pixel data -- `assess()` only reads `Stats`'s aggregate
    properties for the checks this file exercises, all of which divide by
    `count`, so a single synthetic "pixel" whose running sums equal the
    target values reproduces the real measurement exactly."""
    s = aq.Stats()
    s.count = 1
    s._sat_sum = mean_saturation
    s._colorful = colorful_fraction
    s._white = white_fraction
    s._luma_sum = 0.0
    s._luma_sq_sum = luma_std * luma_std  # var = luma_std**2 when mean == 0
    return s


def test_approved_bw_masters_pass_the_line_art_gate():
    for name, fx in APPROVED_BW_MASTERS.items():
        stats = _pinned_stats(
            fx["mean_saturation"], fx["colorful_fraction"], fx["luma_std"],
            white_fraction=fx["white_fraction"],
        )
        ok, reasons = aq.assess(stats, "bw")
        assert ok, f"{name} should pass the bw gate but was rejected: {reasons}"


def test_approved_color_masters_pass_the_color_gate():
    for name, fx in APPROVED_COLOR_MASTERS.items():
        stats = _pinned_stats(fx["mean_saturation"], fx["colorful_fraction"], fx["luma_std"])
        ok, reasons = aq.assess(stats, "color", tint_concentration=fx["tint_concentration"])
        assert ok, f"{name} should pass the color gate but was rejected: {reasons}"


def test_known_bad_examples_are_rejected_as_tint_wash():
    for name, fx in KNOWN_BAD.items():
        stats = _pinned_stats(fx["mean_saturation"], fx["colorful_fraction"], fx["luma_std"])
        ok, reasons = aq.assess(stats, "color", tint_concentration=fx["tint_concentration"])
        assert not ok, f"{name} should be REJECTED by the color gate"
        assert any("tint" in r or "wash" in r for r in reasons), (
            f"{name} expected a single-hue tint/wash rejection, got: {reasons}"
        )


def test_masked_countess_stays_the_closest_real_color_pass():
    """masked-countess-color.webp is the color corpus's tightest real margin
    call (tint_concentration=0.8688 against a 0.90 reject threshold, per
    art_quality.py's own calibration comment) -- pin it on its own so a
    threshold nudge that would flip this specific file shows up as an
    obvious, named failure rather than getting lost in the loop above."""
    fx = APPROVED_COLOR_MASTERS["masked-countess-color.webp"]
    assert fx["tint_concentration"] < aq.TINT_MAX_HUE_CONCENTRATION
    stats = _pinned_stats(fx["mean_saturation"], fx["colorful_fraction"], fx["luma_std"])
    ok, reasons = aq.assess(stats, "color", tint_concentration=fx["tint_concentration"])
    assert ok, f"masked-countess-color.webp should still pass: {reasons}"


def test_masking_up_bw_stays_the_closest_real_bw_pass():
    """masking-up-bw.webp is the bw corpus's tightest real margin call
    (white_fraction=0.1633 against the calibrated BW_MIN_WHITE_FRACTION
    floor) -- pin it on its own for the same reason as the color case above."""
    fx = APPROVED_BW_MASTERS["masking-up-bw.webp"]
    assert fx["white_fraction"] > aq.BW_MIN_WHITE_FRACTION
    stats = _pinned_stats(
        fx["mean_saturation"], fx["colorful_fraction"], fx["luma_std"],
        white_fraction=fx["white_fraction"],
    )
    ok, reasons = aq.assess(stats, "bw")
    assert ok, f"masking-up-bw.webp should still pass: {reasons}"


@pytest.mark.parametrize("name,fx", list(APPROVED_BW_MASTERS.items()))
def test_live_approved_bw_masters_match_frozen_fixture(name, fx):
    """When Pillow is installed, re-load the real checked-in file and confirm
    it still measures close to the frozen fixture above and still passes the
    live gate. Skipped (not failed) without Pillow -- the CI job that runs
    the full suite does not install it; `coloring-render-contract.yml` and a
    provisioned dev sandbox do, and this is where drift in the real image
    (a re-render, a bad overwrite) would actually be caught."""
    pytest.importorskip("PIL")
    path = APPROVED_DIR / name
    if not path.exists():
        pytest.skip(f"{path} not present in this checkout")
    ok, reasons, info = aq.assess_file(path, "bw")
    assert ok is True, f"{name} regressed on the live bw gate: {reasons}"
    assert info["mean_saturation"] == pytest.approx(fx["mean_saturation"], abs=0.01)
    assert info["colorful_fraction"] == pytest.approx(fx["colorful_fraction"], abs=0.01)
    assert info["white_fraction"] == pytest.approx(fx["white_fraction"], abs=0.01)


@pytest.mark.parametrize("name,fx", list(APPROVED_COLOR_MASTERS.items()))
def test_live_approved_color_masters_match_frozen_fixture(name, fx):
    pytest.importorskip("PIL")
    path = APPROVED_DIR / name
    if not path.exists():
        pytest.skip(f"{path} not present in this checkout")
    ok, reasons, info = aq.assess_file(path, "color")
    assert ok is True, f"{name} regressed on the live color gate: {reasons}"
    assert info["mean_saturation"] == pytest.approx(fx["mean_saturation"], abs=0.01)
    assert info["colorful_fraction"] == pytest.approx(fx["colorful_fraction"], abs=0.01)
    if fx["tint_concentration"] is None:
        assert info["tint_concentration"] is None
    else:
        assert info["tint_concentration"] == pytest.approx(fx["tint_concentration"], abs=0.01)


@pytest.mark.parametrize("name,fx", list(KNOWN_BAD.items()))
def test_live_known_bad_examples_match_frozen_fixture(name, fx):
    """Same live cross-check as above, for the known-bad rejects."""
    pytest.importorskip("PIL")
    path = fx["path"]
    if not path.exists():
        pytest.skip(f"{path} not present in this checkout")
    ok, reasons, info = aq.assess_file(path, "color")
    assert ok is False, f"{name} unexpectedly passes the live color gate now: {info}"
    assert any("tint" in r or "wash" in r for r in reasons), (
        f"{name} rejected for a different reason than expected: {reasons}"
    )
    assert info["mean_saturation"] == pytest.approx(fx["mean_saturation"], abs=0.01)
    assert info["tint_concentration"] == pytest.approx(fx["tint_concentration"], abs=0.01)
