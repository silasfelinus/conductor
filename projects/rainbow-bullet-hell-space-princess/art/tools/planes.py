"""Ship reviewed stage planes: python3 planes.py s01 s02 ... (run from kind_robots).

For each stage, encodes the kept Classic sky/far/mid and the Fever Dream sky/far/mid (where no doodle plane has
already shipped) from the art-backlog ledger, then registers them in RAINBOW_STAGE_PAINTINGS / RAINBOW_DOODLE_ART.
"""

import os
import re
import sys
from pathlib import Path

import yaml
from PIL import Image

CACHE = Path("/tmp/rainbow-art-work/backlog")
LEDGER = Path(
    "/home/user/conductor/projects/rainbow-bullet-hell-space-princess/art/ART-BACKLOG-2026-11-24.yaml"
)
ART = Path("public/rainbow-princess-art")
SIZE = {"sky": (960, 540), "far": (768, 439), "mid": (768, 439)}

subjects = {s["key"]: s for s in yaml.safe_load(LEDGER.read_text())["subjects"]}
doodle_src = Path("utils/arcade/games/rainbowDoodleArt.ts").read_text()


def kept(key):
    s = subjects.get(key)
    if not s or not str(s.get("verdict", "")).startswith("keep"):
        return None
    iid = s["art"]["krea2"]["art_image_id"]
    f = CACHE / f"{key}-{iid}.png"
    if not f.exists():
        import importlib.util
        import io

        spec = importlib.util.spec_from_file_location(
            "op", "/home/user/conductor/scripts/export_rainbow_opening.py"
        )
        op = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(op)
        Image.open(io.BytesIO(op.download(int(iid)))).convert("RGB").save(f)
    return f


def encode(src, dst, size, budget):
    im = Image.open(src).convert("RGB").resize(size, Image.LANCZOS)
    dst.parent.mkdir(parents=True, exist_ok=True)
    for q in (82, 76, 70, 64, 58, 52):
        im.save(dst, "WEBP", quality=q, method=6)
        if os.path.getsize(dst) < budget:
            return os.path.getsize(dst)
    raise SystemExit(f"{dst} over budget")


classic, doodle = [], []
for stage in sys.argv[1:]:
    for depth in ("sky", "far", "mid"):
        path = f"stages/{stage}-{depth}"
        c = kept(f"{stage}-{depth}-classic") or kept(f"{stage}-{depth}-classic-2")
        f = kept(f"{stage}-{depth}-fever") or kept(f"{stage}-{depth}-fever-2")
        already = f"'{path}'" in doodle_src
        if not c or not (f or already):
            print("skip", path, bool(c), bool(f), already)
            continue
        print(path, encode(c, ART / f"{path}.webp", SIZE[depth], 120_000))
        classic.append(path)
        if not already:
            print(
                "doodle",
                path,
                encode(f, ART / "doodle" / f"{path}.webp", SIZE[depth], 120_000),
            )
            doodle.append(path)

GA = Path("utils/arcade/games/rainbowGameArt.ts")
t = GA.read_text()
m = re.search(
    r"RAINBOW_STAGE_PAINTINGS: readonly string\[\] = \[(.*?)\]", t, flags=re.DOTALL
)
cur = re.findall(r"'([^']+)'", m.group(1))
allp = sorted(set(cur + classic))
t = t[: m.start(1)] + "".join(f"\n  '{p}'," for p in allp) + "\n" + t[m.end(1) :]
GA.write_text(t)

DA = Path("utils/arcade/games/rainbowDoodleArt.ts")
d = DA.read_text()
for p in doodle:
    if f"'{p}'" in d:
        continue
    last = [l for l in d.split("\n") if l.startswith("  'stages/")][-1] + "\n"
    d = d.replace(last, last + f"  '{p}',\n", 1)
# Keep the contiguous stages/ block sorted, as the list was.
lines = d.split("\n")
idx = [i for i, l in enumerate(lines) if l.startswith("  'stages/")]
block = sorted(lines[i] for i in idx)
for i, l in zip(idx, block):
    lines[i] = l
d = "\n".join(lines)
DA.write_text(d)
print("registered", len(classic), "classic and", len(doodle), "doodle planes")
