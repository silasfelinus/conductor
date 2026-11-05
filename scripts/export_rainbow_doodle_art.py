#!/usr/bin/env python3
"""Export Rainbow Space Princess's Fever Dream look into kind_robots.

WHY THIS EXISTS. t-036's doodle set (art/DOODLE-SET-1.yaml, 93 Kontext/Krea 2 cells) restyles every shipped
asset into the 1980s neon airbrush school-folder look, but the renders need work before the game can use
them (DOODLE-SET-2.yaml and later sets re-render what the review held back). Sprites come back on a #00ff00 matte at 3-4x the shipped size. Some cells crop the creature, and a few
break CAST-QA. art/DOODLE-SET-1-REVIEW.yaml records a decision for each asset, and this script applies them:

  keep   the render is keyed, trimmed, fitted and written to public/rainbow-princess-art/doodle/<path>.webp
  fever  the CLASSIC sprite is written there instead, with a saturation lift, a white sticker outline and a
         hot-pink rim. Hue never changes, so every pilot keeps her colour.
  hold   nothing is written, and the game falls back to the classic picture

Then it rewrites utils/arcade/games/rainbowDoodleArt.ts, the list the game resolves Fever Dream paths
against. A path missing from the list always falls back to the classic file, so a partial set is safe.

Usage:
    python scripts/export_rainbow_doodle_art.py --kind-robots ../kind_robots [--cache DIR] [--dry-run]

Environment: KR_API_TOKEN, KR_BASE_URL (only to download renders not already in --cache).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

PROJECT = Path(__file__).resolve().parent.parent / "projects/rainbow-bullet-hell-space-princess"
LEDGERS = sorted(
    (p for p in (PROJECT / "art").glob("DOODLE-SET-*.yaml") if re.fullmatch(r"DOODLE-SET-\d+\.yaml", p.name)),
    key=lambda p: int(re.findall(r"\d+", p.name)[0]),
)
REVIEW = PROJECT / "art/DOODLE-SET-1-REVIEW.yaml"
ART = "rainbow-princess-art"
MANIFEST = "utils/arcade/games/rainbowDoodleArt.ts"

# Output box per folder: sprites keep about 1.5x the classic edge so they stay crisp on HiDPI screens without
# growing the download much; pictures keep the classic size (cut-ins 1.5x).
SPRITE_EDGE = {"ships": 288, "enemies": 192, "guardian": 320, "bosses": 400, "pickups": 128}
PICTURE_BOX = {
    "comms": (256, 256),
    "cutins": (540, 186),
    "stages": (640, 366),
    "portraits": (576, 842),
    "hero-pearl-palace": (1344, 768),
    "key-art": (1024, 585),
}
PINK_RIM = (255, 79, 195, 255)
QUALITY = 80


def decision(value):
    """('keep'|'fever'|'hold', reason)."""
    if isinstance(value, str):
        return value, ""
    (kind, reason), = value.items()
    return kind, reason


def classic_assets(kind_robots: Path):
    """Every shipped classic asset as a path relative to the art root (no extension), portraits included."""
    root = kind_robots / "public" / ART
    out = sorted(
        str(p.relative_to(root).with_suffix(""))
        for p in root.rglob("*.webp")
        if p.relative_to(root).parts[0] != "doodle"
    )
    portraits = kind_robots / "public/rainbow-princess-portraits"
    out += sorted(f"portraits/{p.stem}" for p in portraits.glob("*.webp"))
    return out


def classic_file(kind_robots: Path, rel: str) -> Path:
    if rel.startswith("portraits/"):
        return kind_robots / "public/rainbow-princess-portraits" / (rel.split("/", 1)[1] + ".webp")
    return kind_robots / "public" / ART / (rel + ".webp")


def review_key(rel: str) -> str:
    """The review entry that decides this asset: bosses by boss, foreground strips as one group."""
    if rel.startswith("bosses/"):
        return rel.split("-phase")[0]
    if rel.startswith("stages/") and rel.endswith("-fore"):
        return "stages/fore"
    return rel


def key_green(image):
    """Key the #00ff00 matte to alpha, pull green spill out of the edges, erode the fringe, trim."""
    import numpy as np
    from PIL import Image, ImageFilter

    a = np.asarray(image.convert("RGB")).astype(np.float32)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    greenness = g - np.maximum(r, b)
    alpha = np.clip(1 - (greenness - 40) / 100, 0, 1)
    a[..., 1] = np.where(greenness > 0, np.maximum(r, b), g)
    out = Image.fromarray(np.dstack([a, alpha * 255]).astype(np.uint8), "RGBA")
    out.putalpha(out.getchannel("A").filter(ImageFilter.MinFilter(3)))
    box = out.getbbox()
    return out.crop(box) if box else out


def fit_edge(image, edge):
    from PIL import Image

    scale = edge / max(image.size)
    if scale >= 1:
        return image
    return image.resize((round(image.width * scale), round(image.height * scale)), Image.LANCZOS)


def cover(image, size):
    """Scale to cover the box, then centre-crop to it."""
    from PIL import ImageOps, Image

    return ImageOps.fit(image, size, Image.LANCZOS)


def paint_out(image, box, pad=24):
    """Replace a small area (baked lettering on a smooth sky) with a heavy blur of its surroundings."""
    from PIL import Image, ImageDraw, ImageFilter

    x0, y0, x1, y1 = box
    area = (max(0, x0 - pad), max(0, y0 - pad), min(image.width, x1 + pad), min(image.height, y1 + pad))
    patch = image.crop(area).filter(ImageFilter.GaussianBlur(28))
    mask = Image.new("L", patch.size, 0)
    ImageDraw.Draw(mask).rectangle((x0 - area[0], y0 - area[1], x1 - area[0], y1 - area[1]), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(pad / 2))
    image = image.copy()
    image.paste(patch, area[:2], mask)
    return image


def trim_frame(image, inset):
    from PIL import Image

    w, h = image.size
    return image.crop((inset, inset, w - inset, h - inset)).resize((w, h), Image.LANCZOS)


def fever(image, outline=None):
    """The classic sprite in fever colours: saturation lift, white sticker outline, hot-pink rim."""
    from PIL import Image, ImageEnhance, ImageFilter

    image = image.convert("RGBA")
    edge = max(image.size)
    width = outline or max(2, round(edge * 0.022))
    pad = width * 2 + 2
    canvas = Image.new("RGBA", (image.width + pad * 2, image.height + pad * 2), (0, 0, 0, 0))
    rgb = ImageEnhance.Contrast(ImageEnhance.Color(image).enhance(1.45)).enhance(1.08)
    sprite = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    sprite.paste(rgb, (pad, pad), image)
    alpha = sprite.getchannel("A").point(lambda v: 255 if v > 96 else 0)
    # Open the mask first, so glitter specks a few pixels wide stay loose sparkles, not outlined boxes.
    alpha = alpha.filter(ImageFilter.MinFilter(5)).filter(ImageFilter.MaxFilter(5))
    size = width * 2 + 1
    white = alpha.filter(ImageFilter.MaxFilter(size))
    pink = white.filter(ImageFilter.MaxFilter(max(3, (width // 2) * 2 + 1)))
    canvas.paste(Image.new("RGBA", canvas.size, PINK_RIM), (0, 0), pink)
    canvas.paste(Image.new("RGBA", canvas.size, (255, 255, 255, 255)), (0, 0), white)
    canvas.alpha_composite(sprite)
    box = canvas.getbbox()
    return canvas.crop(box) if box else canvas


def finished_id(subject):
    for art in (subject.get("art") or {}).values():
        if (art or {}).get("status") == "DONE" and art.get("art_image_id"):
            return art["art_image_id"]
    return None


def render_path(subjects, rel, cache: Path):
    """The cached render for this asset, downloading it on first use. When a later set re-renders an
    asset (DOODLE-SET-2's fixes), its finished render wins; the review decides whether it ships."""
    asset = f"{ART}/doodle/{rel}"
    done = [(s, finished_id(s)) for s in subjects if s.get("asset") == asset and finished_id(s)]
    if not done:
        return None
    _subject, image_id = done[-1]
    path = cache / f"{rel}-{image_id}.png"
    if not path.exists():
        from export_shifting_lands_cards import load_image

        path.parent.mkdir(parents=True, exist_ok=True)
        load_image(image_id).save(path)
    return path


def doodle_image(rel, src: Path):
    from PIL import Image

    image = Image.open(src)
    folder = rel.split("/")[0]
    if folder in ("ships", "enemies", "bosses", "pickups"):
        edge = SPRITE_EDGE["guardian" if "/guardian-" in rel else folder]
        return fit_edge(key_green(image), edge)
    image = image.convert("RGB")
    if rel == "stages/s04-card":
        image = paint_out(image, (1080, 16, 1344, 124))
    if rel == "stages/s05-card":
        image = trim_frame(image, 14)
    return cover(image, PICTURE_BOX.get(folder, PICTURE_BOX.get(rel)))


def fever_image(rel, src: Path):
    from PIL import Image

    image = Image.open(src)
    if rel.endswith("-fore"):
        # Foreground strips tile seamlessly, so the outline must not reach the left or right edge: treat a
        # wider canvas and crop back to the original width.
        strip = fever(image, outline=2)
        left = (strip.width - image.width) // 2
        return strip.crop((left, 0, left + image.width, strip.height))
    return fever(image)


def write_manifest(kind_robots: Path, entries):
    lines = [
        "// Written by conductor scripts/export_rainbow_doodle_art.py from art/DOODLE-SET-1-REVIEW.yaml: every",
        "// Fever Dream picture shipped under public/rainbow-princess-art/doodle/<entry>.webp. A path missing",
        "// here falls back to the classic picture. Re-run the export; do not edit by hand.",
        "",
        "export const RAINBOW_DOODLE_ART: readonly string[] = [",
        *[f"  '{e}'," for e in entries],
        "]",
        "",
    ]
    (kind_robots / MANIFEST).write_text("\n".join(lines))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--kind-robots", default="../kind_robots")
    parser.add_argument("--cache", default=".cache/rainbow-doodle", help="where raw renders are kept")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    kind_robots = Path(args.kind_robots)
    cache = Path(args.cache)
    subjects = [s for ledger in LEDGERS for s in yaml.safe_load(ledger.read_text())["subjects"]]
    decisions = yaml.safe_load(REVIEW.read_text())["decisions"]

    out_root = kind_robots / "public" / ART / "doodle"
    written, missing = [], []
    for rel in classic_assets(kind_robots):
        key = review_key(rel)
        if key not in decisions:
            missing.append(rel)
            continue
        kind, _reason = decision(decisions[key])
        if kind == "hold":
            continue
        if kind == "keep":
            src = render_path(subjects, rel, cache)
            if src is None:
                missing.append(rel)
                continue
            make = doodle_image
        else:
            src, make = classic_file(kind_robots, rel), fever_image
        dest = out_root / (rel + ".webp")
        print(f"{kind:5} {rel}")
        if not args.dry_run:
            dest.parent.mkdir(parents=True, exist_ok=True)
            make(rel, src).save(dest, "WEBP", quality=QUALITY, method=6)
        written.append(rel)
    # The key art has no classic twin; it is Fever Dream's own Pilots-tab backdrop.
    if decision(decisions.get("key-art", "hold"))[0] == "keep":
        src = render_path(subjects, "key-art", cache)
        print(f"keep  key-art")
        if not args.dry_run:
            doodle_image("key-art", src).save(out_root / "key-art.webp", "WEBP", quality=QUALITY, method=6)
        written.append("key-art")
    if missing:
        print(f"no decision or render for: {', '.join(missing)}", file=sys.stderr)
        return 1
    if not args.dry_run:
        write_manifest(kind_robots, sorted(written))
    print(f"{len(written)} Fever Dream pictures", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
