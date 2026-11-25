"""Ship reviewed boss phase redraws in both looks: python3 bossship.py b02-phase2=<backlog png> ... (run anywhere).

Classic: key_matte (the Gen-2 exporter's border-sampled key) fitted to the shipped Classic sprite's longer edge.
Fever Dream: the same keyed art through export_rainbow_doodle_art.fever (saturation lift, white sticker outline),
fitted to the shipped doodle sprite's longer edge. Writes both webps into kind_robots and a side-by-side preview
over a checkerboard at /tmp/rainbow-art-work/<name>-ship-preview.png.
"""

import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, "/home/user/conductor/scripts")
from export_rainbow_doodle_art import QUALITY, fever, fit_edge  # noqa: E402
from export_rainbow_gen2_art import key_matte  # noqa: E402

ART = Path("/home/user/kind_robots/public/rainbow-princess-art")
WORK = Path("/tmp/rainbow-art-work")


def drop_specks(image, share=0.004):
    """Clear detached bits smaller than `share` of the sprite's opaque area. fever() gives every island its own
    sticker outline, so loose sparkles turn into outlined boxes; the Classic look keeps them."""
    import numpy as np
    from PIL import ImageDraw

    alpha = np.asarray(image.getchannel("A"))
    mask = Image.fromarray(((alpha > 20) * 255).astype(np.uint8), "L")
    total = int((alpha > 20).sum())
    out = np.asarray(image).copy()
    while True:
        seen = np.asarray(mask)
        ys, xs = np.nonzero(seen == 255)
        if not len(ys):
            break
        ImageDraw.floodfill(mask, (int(xs[0]), int(ys[0])), 128)
        comp = np.asarray(mask) == 128
        if comp.sum() < share * total:
            out[comp, 3] = 0
        mask.paste(64, mask=Image.fromarray((comp * 255).astype(np.uint8), "L"))
    cleared = Image.fromarray(out, "RGBA")
    box = cleared.getbbox()
    return cleared.crop(box) if box else cleared

for arg in sys.argv[1:]:
    name, src = arg.split("=")
    keyed = key_matte(Image.open(WORK / src if not src.startswith("/") else src))
    outs = {}
    for rel, look in ((f"bosses/{name}", "classic"), (f"doodle/bosses/{name}", "fever")):
        path = ART / f"{rel}.webp"
        edge = max(Image.open(path).size)
        image = fit_edge(fever(drop_specks(keyed)) if look == "fever" else keyed, edge)
        image.save(path, "WEBP", quality=QUALITY, method=6)
        outs[look] = image
        print(name, look, path.relative_to(ART.parent.parent), image.size, path.stat().st_size)
    w = sum(i.width for i in outs.values()) + 20
    h = max(i.height for i in outs.values())
    board = Image.new("RGBA", (w, h))
    for y in range(0, h, 16):
        for x in range(0, w, 16):
            board.paste((200, 200, 200, 255) if (x + y) // 16 % 2 else (255, 255, 255, 255), (x, y, x + 16, y + 16))
    x = 0
    for image in outs.values():
        board.alpha_composite(image, (x, 0))
        x += image.width + 20
    board.save(WORK / f"{name}-ship-preview.png")
