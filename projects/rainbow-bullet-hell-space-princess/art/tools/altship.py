"""Ship keyed Fever Dream detour twins: python3 altship.py x1-sky=backlog/...png x1-mid x1-near (run from kind_robots).

A name with =path is an opaque sky (resized to its Classic size); a bare name is taken from altkeyed/<name>.png.
Registers doodle `alt/<name>` in RAINBOW_DOODLE_ART (kept sorted).
"""

import os
import re
import sys
from pathlib import Path

from PIL import Image

S = Path("/tmp/rainbow-art-work")
ART = Path("public/rainbow-princess-art")
names = []
for arg in sys.argv[1:]:
    name, _, src = arg.partition("=")
    classic = Image.open(ART / f"alt/{name}.webp")
    if src:
        im = Image.open(S / src).convert("RGB")
        # Trim a near-white border the render painted around the sky.
        import numpy as np

        a = np.asarray(im).min(axis=2) > 235
        rows = [i for i in range(a.shape[0]) if a[i].mean() < 0.5]
        cols = [j for j in range(a.shape[1]) if a[:, j].mean() < 0.5]
        im = im.crop((cols[0] + 2, rows[0] + 2, cols[-1] - 1, rows[-1] - 1)).resize(
            classic.size, Image.LANCZOS
        )
    else:
        im = Image.open(S / "altkeyed" / f"{name}.png").convert("RGBA")
        assert im.size == classic.size, (name, im.size, classic.size)
    dst = ART / "doodle/alt" / f"{name}.webp"
    dst.parent.mkdir(parents=True, exist_ok=True)
    for q in (82, 76, 70, 64, 58):
        im.save(dst, "WEBP", quality=q, method=6)
        if os.path.getsize(dst) < 120_000:
            break
    else:
        raise SystemExit(f"{dst} over budget")
    print(name, im.size, im.mode, os.path.getsize(dst))
    names.append(f"alt/{name}")

DA = Path("utils/arcade/games/rainbowDoodleArt.ts")
body = DA.read_text()
marker = "export const RAINBOW_DOODLE_ART"
head = body.split(marker)[0]
entries = sorted(
    dict.fromkeys(re.findall(r"^  '([^']+)',$", body, re.MULTILINE) + names)
)
DA.write_text(
    head
    + marker
    + ": readonly string[] = [\n"
    + "".join(f"  '{e}',\n" for e in entries)
    + "]\n"
)
print("registered", names)
