"""Motion score for 8-cell horizontal RGBA idle atlases: python3 motion.py a.webp b.webp ... Mean deviation of each cell from the mean cell (premultiplied RGB and alpha) over the union alpha mask, x100. Shipped: angler 2.7 (the floor), picket 7.3, urchin 10.2."""
import sys
import numpy as np
from PIL import Image
for p in sys.argv[1:]:
    im = np.asarray(Image.open(p).convert("RGBA")).astype(np.float32) / 255
    h, w, _ = im.shape
    cw = w // 8
    cells = np.stack([im[:, i * cw:(i + 1) * cw] for i in range(8)])
    a = cells[..., 3]
    fg = a.max(axis=0) > 0.5
    prem = cells[..., :3] * a[..., None]
    full = np.concatenate([prem, a[..., None]], axis=-1)
    dev = np.abs(full - full.mean(axis=0)).mean(axis=-1)  # 8,h,w
    score = dev[:, fg].mean() * 100
    # adjacent change
    adj = np.abs(np.diff(full, axis=0)).mean(axis=-1)[:, fg].mean() * 100
    print(f"{p.split('/')[-1]:28} cell {cw}x{h} motion {score:5.2f} adjacent {adj:5.2f}")
