"""Shared sprite plumbing for the zuzu-showdown t-007 bake-off.

Every method ends the same way so the strips compare fairly: a transparent RGBA frame at game
resolution (Zuzu stands 72 px, the hitbox height in kind_robots utils/zuzuShowdown/fighters/zuzu.ts),
a shared indexed palette, and the same preview outputs (a PNG strip and an animated GIF scaled up
with nearest-neighbour so the pixels stay square).
"""

from __future__ import annotations

from collections import deque
from pathlib import Path

from PIL import Image, ImageFilter

GAME_HEIGHT = 72  # Zuzu's standing height in game pixels.
PREVIEW_SCALE = 4
FPS = {"idle": 8, "walk": 10, "hp": 15}


def key_background(image: Image.Image, tolerance: int = 38, min_pocket: int = 1500) -> Image.Image:
    """Make the plain off-white backdrop transparent by flood-filling from the border.

    Only pixels connected to the edge are removed, so white inside the figure (the eyes,
    the kasa's highlights) survives.
    """
    rgb = image.convert("RGB")
    width, height = rgb.size
    px = rgb.load()
    corners = [px[0, 0], px[width - 1, 0], px[0, height - 1], px[width - 1, height - 1]]
    bg = tuple(sorted(c[i] for c in corners)[1] for i in range(3))

    def near(c):
        return sum(abs(c[i] - bg[i]) for i in range(3)) <= tolerance * 3

    seen = bytearray(width * height)
    queue = deque()
    for x in range(width):
        queue.extend([(x, 0), (x, height - 1)])
    for y in range(height):
        queue.extend([(0, y), (width - 1, y)])
    while queue:
        x, y = queue.popleft()
        i = y * width + x
        if seen[i] or not near(px[x, y]):
            continue
        seen[i] = 1
        if x > 0:
            queue.append((x - 1, y))
        if x < width - 1:
            queue.append((x + 1, y))
        if y > 0:
            queue.append((x, y - 1))
        if y < height - 1:
            queue.append((x, y + 1))
    # Second pass: backdrop trapped inside the figure (between an arm and the face, under the kasa
    # brim) is not connected to the border. Remove any enclosed near-backdrop pocket of at least
    # `min_pocket` pixels; smaller ones are more likely a highlight than a hole.
    tight = tolerance * 2

    def backdrop(c):
        return sum(abs(c[i] - bg[i]) for i in range(3)) <= tight

    for start in range(width * height):
        if seen[start] or not backdrop(px[start % width, start // width]):
            continue
        pocket, stack = [], [start]
        seen[start] = 2
        while stack:
            i = stack.pop()
            pocket.append(i)
            x, y = i % width, i // width
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if 0 <= nx < width and 0 <= ny < height:
                    j = ny * width + nx
                    if not seen[j] and backdrop(px[nx, ny]):
                        seen[j] = 2
                        stack.append(j)
        keep = 1 if len(pocket) >= min_pocket else 3
        for i in pocket:
            seen[i] = keep
    out = rgb.convert("RGBA")
    alpha = Image.frombytes("L", (width, height), bytes(0 if s == 1 else 255 for s in seen))
    out.putalpha(alpha)
    return out


def crop_to_content(image: Image.Image) -> Image.Image:
    box = image.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox()
    return image.crop(box) if box else image


def to_game_size(image: Image.Image, figure_height: int, target: int = GAME_HEIGHT) -> Image.Image:
    """Scale so that `figure_height` source pixels become `target` game pixels.

    Each frame passes the same `figure_height` (the reference's standing height), so a crouch
    comes out shorter instead of being stretched back to 72.
    """
    scale = target / figure_height
    size = (max(1, round(image.width * scale)), max(1, round(image.height * scale)))
    # Flatten the illustration's hatching first (a mode filter about one game pixel wide), then
    # Lanczos down; alpha separately with a hard threshold so edges stay crisp. The t-007 variant
    # sheet compared box/Lanczos and with/without the pre-smooth: this was the least noisy.
    radius = max(3, round(1 / scale) | 1)
    colour = image.convert("RGB").filter(ImageFilter.ModeFilter(radius)).resize(size, Image.Resampling.LANCZOS)
    alpha = image.getchannel("A").resize(size, Image.Resampling.BOX).point(lambda a: 255 if a >= 128 else 0)
    colour = colour.convert("RGBA")
    colour.putalpha(alpha)
    return colour


def outer_outline(frame: Image.Image, colour=(28, 22, 30, 255)) -> Image.Image:
    """A one-pixel dark outline drawn just OUTSIDE the silhouette, so thin parts (the katana, the
    kasa brim) keep their pixels instead of being eaten by an inner outline."""
    width, height = frame.size
    out = Image.new("RGBA", (width + 2, height + 2), (0, 0, 0, 0))
    out.alpha_composite(frame, (1, 1))
    src = out.copy().load()
    dst = out.load()
    for y in range(height + 2):
        for x in range(width + 2):
            if src[x, y][3]:
                continue
            if any(0 <= x + dx < width + 2 and 0 <= y + dy < height + 2 and src[x + dx, y + dy][3]
                   for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                dst[x, y] = colour
    return out


def shared_palette(frames: list[Image.Image], colours: int = 24) -> Image.Image:
    """One palette for a whole fighter, built from all of its frames' opaque pixels."""
    opaque = []
    for frame in frames:
        rgb = frame.convert("RGB")
        alpha = frame.getchannel("A")
        opaque.extend(p for p, a in zip(rgb.getdata(), alpha.getdata()) if a)
    swatch = Image.new("RGB", (len(opaque), 1))
    swatch.putdata(opaque)
    return swatch.quantize(colours, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)


def quantize(frame: Image.Image, palette: Image.Image) -> Image.Image:
    alpha = frame.getchannel("A")
    indexed = frame.convert("RGB").quantize(palette=palette, dither=Image.Dither.NONE)
    out = indexed.convert("RGBA")
    out.putalpha(alpha)
    return out


def palette_size(frames: list[Image.Image]) -> int:
    colours = set()
    for frame in frames:
        colours.update(p[:3] for p in frame.getdata() if p[3])
    return len(colours)


def anchor_frames(frames: list[Image.Image], width: int | None = None, height: int | None = None) -> list[Image.Image]:
    """Pad frames onto one canvas with their feet on the bottom row, centred horizontally."""
    width = width or max(f.width for f in frames)
    height = height or max(f.height for f in frames)
    out = []
    for frame in frames:
        canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        canvas.alpha_composite(frame, ((width - frame.width) // 2, height - frame.height))
        out.append(canvas)
    return out


def write_previews(frames: list[Image.Image], out_dir: Path, name: str, fps: int,
                   backdrop=(36, 30, 46), scale: int = PREVIEW_SCALE) -> tuple[Path, Path]:
    """Write <name>-strip.png (frames side by side) and <name>.gif (looping), both scaled up."""
    out_dir.mkdir(parents=True, exist_ok=True)
    width, height = frames[0].size
    strip = Image.new("RGBA", (width * len(frames), height), backdrop + (255,))
    for i, frame in enumerate(frames):
        strip.alpha_composite(frame, (i * width, 0))
    strip = strip.resize((strip.width * scale, strip.height * scale), Image.Resampling.NEAREST)
    strip_path = out_dir / f"{name}-strip.png"
    strip.convert("RGB").save(strip_path)
    gif_frames = []
    for frame in frames:
        canvas = Image.new("RGBA", frame.size, backdrop + (255,))
        canvas.alpha_composite(frame)
        gif_frames.append(canvas.resize((width * scale, height * scale), Image.Resampling.NEAREST).convert("RGB"))
    gif_path = out_dir / f"{name}.gif"
    gif_frames[0].save(gif_path, save_all=True, append_images=gif_frames[1:], duration=round(1000 / fps),
                       loop=0, disposal=2)
    return strip_path, gif_path
