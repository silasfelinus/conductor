"""Key the Fever Dream detour twins (rendered on flat magenta) to alpha at their Classic plane's size.

python3 altkey.py <key>=<png> ...  e.g. x1-mid=backlog/doodle-alt-x1-mid-280302.png
Append !bottom to keep the bottom strip of a render taller than its Classic band (no squash).
Extra flat colours to key (e.g. a floor the Classic plane leaves open) can follow as x1-far=path@R,G,B.
Writes <scratch>/altkeyed/<name>.png plus a preview over a checker.
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

S = Path("/tmp/rainbow-art-work")
KR = Path("/home/user/kind_robots/public/rainbow-princess-art")
# Key distances (near, far) per plane. x1-far needed (18, 45) on the old magenta matte; the green retakes key
# cleanly at the default.
TIGHT_MAGENTA = {"x1-far": (18, 45)}
TIGHT = {}
out = S / "altkeyed"
out.mkdir(exist_ok=True)


def key(rgb, colour, near, far):
    d = np.sqrt(((rgb - np.array(colour, np.float32)) ** 2).sum(axis=2))
    return np.clip((d - near) / (far - near), 0, 1)


for arg in sys.argv[1:]:
    name, rest = arg.split("=")
    fit = rest.endswith("!fit")
    rest = rest.removesuffix("!fit")
    bottom = rest.endswith("!bottom")
    rest = rest.removesuffix("!bottom")
    parts = rest.split("@")
    src = Image.open(S / parts[0]).convert("RGB")
    classic = Image.open(KR / f"alt/{name}.webp")
    rgb = np.asarray(src).astype(np.float32)
    top = rgb[:8].reshape(-1, 3)
    matte = np.median(top, axis=0)
    green = matte[1] > max(matte[0], matte[2])
    alpha = key(rgb, matte, *(TIGHT if green else TIGHT_MAGENTA).get(name, (40, 100)))
    for extra in parts[1:]:
        alpha = np.minimum(
            alpha, key(rgb, [float(v) for v in extra.split(",")], 30, 80)
        )
    # Pull matte spill from the semi-transparent fringe: green for a green matte, magenta otherwise.
    fringe = (alpha > 0) & (alpha < 1)
    g = rgb[..., 1]
    if green:
        rgb[..., 1] = np.where(fringe, np.minimum(g, np.maximum(rgb[..., 0], rgb[..., 2])), g)
    else:
        rgb[..., 0] = np.where(
            fringe, np.minimum(rgb[..., 0], np.maximum(g, rgb[..., 2] * 0.9)), rgb[..., 0]
        )
        rgb[..., 2] = np.where(
            fringe, np.minimum(rgb[..., 2], np.maximum(g, rgb[..., 0] * 0.9)), rgb[..., 2]
        )
    a = Image.fromarray((alpha * 255).astype(np.uint8), "L").filter(
        ImageFilter.MinFilter(3)
    )
    im = Image.fromarray(rgb.clip(0, 255).astype(np.uint8), "RGB")
    im.putalpha(a)
    if bottom:
        # The render is taller than the Classic band: keep the bottom strip at the Classic aspect, unsquashed.
        want = round(im.width * classic.height / classic.width)
        im = im.crop((0, max(0, im.height - want), im.width, im.height))
        # Shapes the crop cut flat along the top would show a hard line: fade the top rows.
        a = np.asarray(im.getchannel("A")).astype(np.float32)
        fade = max(4, want // 12)
        a[:fade] *= np.linspace(0, 1, fade, dtype=np.float32)[:, None]
        im.putalpha(Image.fromarray(a.astype(np.uint8), "L"))
    if fit:
        # The render left a margin of key colour at the sides: fill the Classic band edge to edge.
        im = im.crop(im.getchannel("A").point(lambda v: 255 if v > 64 else 0).getbbox())
    im = im.resize(classic.size, Image.LANCZOS)
    im.save(out / f"{name}.png")
    check = Image.new("RGB", im.size, "#30303a")
    for y in range(0, im.height, 24):
        for x in range(0, im.width, 24):
            if (x // 24 + y // 24) % 2:
                check.paste("#55556a", (x, y, x + 24, y + 24))
    check.paste(im, (0, 0), im)
    check.save(out / f"{name}-preview.png")
    op = np.asarray(im)[..., 3]
    h = op.shape[0]
    print(
        name,
        im.size,
        "opaque by band",
        [
            round(float((op[int(h * f) : int(h * (f + 0.1))] > 128).mean()), 2)
            for f in np.arange(0, 1, 0.1)
        ],
        "matte",
        matte.round(),
    )
