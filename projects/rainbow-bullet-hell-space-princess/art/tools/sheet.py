"""Download finished art-backlog renders and build a labelled contact sheet: python3 sheet.py out.png key=id ..."""

import importlib.util
import io
import sys
from pathlib import Path

from PIL import Image, ImageDraw

spec = importlib.util.spec_from_file_location(
    "op", "/home/user/conductor/scripts/export_rainbow_opening.py"
)
op = importlib.util.module_from_spec(spec)
spec.loader.exec_module(op)
cache = Path("/tmp/rainbow-art-work/backlog")
cache.mkdir(exist_ok=True)
out = sys.argv[1]
tiles = []
for arg in sys.argv[2:]:
    key, iid = arg.split("=")
    f = cache / f"{key}-{iid}.png"
    if not f.exists():
        Image.open(io.BytesIO(op.download(int(iid)))).convert("RGB").save(f)
    im = Image.open(f).convert("RGB")
    im.thumbnail((448, 300))
    tile = Image.new("RGB", (448, 320), "#222")
    tile.paste(im, ((448 - im.width) // 2, 20))
    ImageDraw.Draw(tile).text((6, 4), f"{key} {iid}", fill="#fff")
    tiles.append(tile)
cols = 3
rows = (len(tiles) + cols - 1) // cols
sheet = Image.new("RGB", (448 * cols, 320 * rows), "#000")
for i, t in enumerate(tiles):
    sheet.paste(t, ((i % cols) * 448, (i // cols) * 320))
sheet.save(out)
print(out, sheet.size)
