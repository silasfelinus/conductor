"""Ship reviewed idle atlases into kind_robots: python3 idleship.py enemies/angler=t030/angler-idle.webp ... (run from kind_robots).

Copies each atlas to public/rainbow-princess-art/doodle/anim/<name>-idle.webp (under 200 KB) and registers
`<path>: 8` in RAINBOW_IDLE_ATLASES (kept sorted).
"""

import os
import re
import shutil
import sys
from pathlib import Path

S = Path("/tmp/rainbow-art-work")
ART = Path("public/rainbow-princess-art/doodle/anim")
GA = Path("utils/arcade/games/rainbowGameArt.ts")

added = {}
for arg in sys.argv[1:]:
    key, src = arg.split("=")
    name = key.split("/")[1]
    dst = ART / f"{name}-idle.webp"
    shutil.copy(S / src, dst)
    size = os.path.getsize(dst)
    assert size < 200_000, (dst, size)
    added[key] = 8
    print(key, dst, size)

t = GA.read_text()
m = re.search(
    r"RAINBOW_IDLE_ATLASES: Readonly<Record<string, number>> = \{(.*?)\}",
    t,
    flags=re.DOTALL,
)
cur = dict(re.findall(r"'([^']+)': (\d+)", m.group(1)))
cur.update({k: str(v) for k, v in added.items()})
body = "".join(f"\n  '{k}': {v}," for k, v in sorted(cur.items()))
t = t[: m.start(1)] + (body + "\n" if body else "") + t[m.end(1) :]
GA.write_text(t)
print("registered", sorted(cur))
