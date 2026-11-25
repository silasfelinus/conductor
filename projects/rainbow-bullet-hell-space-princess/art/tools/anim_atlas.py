"""Cut a reviewed WAN idle loop into an 8-cell horizontal atlas with the matte keyed out.

python atlas.py <name> <kind> <out.webp>: frames from <name>/all*.png (frame 0 is the exact source and is
dropped), the tail crossfaded into the head so the loop closes, 8 evenly spaced cells, each keyed with the
Gen-2 key_matte rules but uncropped, then all cropped to one union box so the creature never jitters, and
scaled so a cell's longer side matches the shipped still's.
"""

import glob
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

name, kind, out = sys.argv[1:4]
STILL = Image.open(
    f"/home/user/kind_robots/public/rainbow-princess-art/doodle/{kind if '/' in kind else 'enemies/' + kind}.webp"
)


def key(image, near=48.0, far=110.0):
    rgb = np.asarray(image.convert("RGB")).astype(np.float32)
    h, w, _ = rgb.shape
    ring = np.concatenate(
        [
            rgb[:6].reshape(-1, 3),
            rgb[-6:].reshape(-1, 3),
            rgb[:, :6].reshape(-1, 3),
            rgb[:, -6:].reshape(-1, 3),
        ]
    )
    matte = np.median(ring, axis=0)
    dist = np.sqrt(((rgb - matte) ** 2).sum(axis=2))
    hard = Image.fromarray(((dist < near) * 255).astype(np.uint8), "L")
    pad = Image.new("L", (w + 2, h + 2), 255)
    pad.paste(hard, (1, 1))
    ImageDraw.floodfill(pad, (0, 0), 128)
    background = np.asarray(pad)[1:-1, 1:-1] == 128
    band = (
        np.asarray(
            Image.fromarray((background * 255).astype(np.uint8), "L").filter(
                ImageFilter.MaxFilter(9)
            )
        )
        > 0
    )
    alpha = np.ones((h, w), np.float32)
    alpha[band] = np.clip((dist[band] - near) / (far - near), 0, 1)
    alpha[background] = 0
    alpha[dist < near * 0.6] = 0
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    spill = band & (g > np.maximum(r, b))
    rgb[..., 1] = np.where(spill, np.maximum(r, b), g)
    keyed = Image.fromarray(np.dstack([rgb, alpha * 255]).astype(np.uint8), "RGBA")
    keyed.putalpha(keyed.getchannel("A").filter(ImageFilter.MinFilter(3)))
    return keyed


def key2(image):
    """Key twice when the source still sat on its own flat matte inside the render's green pad (Krea's muted
    green, or a plate colour): the first key clears the pad, leaving the inner rectangle opaque; if that box's
    edge rows are still solid, key the rectangle again against its own border colour."""
    first = key(image)
    box = first.getbbox()
    if not box:
        return first
    # Look a few pixels in from the box: the first key leaves a soft ramp right at the rectangle's border.
    a = np.asarray(first.getchannel("A"))[box[1] + 8 : box[3] - 8, box[0] + 8 : box[2] - 8]
    if a.size == 0:
        return first
    edge = np.concatenate([a[:3].ravel(), a[-3:].ravel(), a[:, :3].ravel(), a[:, -3:].ravel()])
    if (edge > 200).mean() < 0.9:
        return first
    inner = key(image.crop((box[0] + 8, box[1] + 8, box[2] - 8, box[3] - 8)))
    out = Image.new("RGBA", image.size, (0, 0, 0, 0))
    out.paste(inner, (box[0] + 8, box[1] + 8))
    return out


frames = [Image.open(f).convert("RGB") for f in sorted(glob.glob(f"{name}/all*.png"))][
    1:
]
# Raw frames (no crossfade: a drifting creature ghosts when two positions blend), 8 evenly spaced.
picks = [frames[round(i * (len(frames) - 1) / 8)] for i in range(8)]
cells = [key2(p) for p in picks]


def despill(cell):
    # Green backdrop showing through a soft or see-through edge: pull green down to the brighter of red/blue.
    a = np.asarray(cell).astype(np.float32)
    soft = a[..., 3] < 250
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    a[..., 1] = np.where(soft & (g > np.maximum(r, b)), np.maximum(r, b), g)
    return Image.fromarray(a.astype(np.uint8), "RGBA")


cells = [despill(c) for c in cells]
# Idle motion stays in place: centre every cell on its own creature, then share one box.
crops = [c.crop(c.getbbox()) for c in cells]
w = max(c.width for c in crops)
h = max(c.height for c in crops)
cells = []
for c in crops:
    cell = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    cell.paste(c, ((w - c.width) // 2, (h - c.height) // 2))
    cells.append(cell)
scale = max(STILL.size) / max(cells[0].size)
size = (round(cells[0].width * scale), round(cells[0].height * scale))
cells = [c.resize(size, Image.LANCZOS) for c in cells]
atlas = Image.new("RGBA", (size[0] * 8, size[1]), (0, 0, 0, 0))
for i, c in enumerate(cells):
    atlas.paste(c, (i * size[0], 0))
atlas.save(out, "WEBP", quality=88, method=6)
# A preview on a dark ground for review.
prev = Image.new("RGBA", atlas.size, (24, 13, 56, 255))
prev.alpha_composite(atlas)
prev.convert("RGB").save(out.replace(".webp", "-preview.png"))
print(kind, "cell", size, "atlas", atlas.size, "still", STILL.size)
