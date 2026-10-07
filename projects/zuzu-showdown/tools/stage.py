"""zuzu-showdown t-009: stage layers from house-lane art.

A stage is a config module in tools/stages/<slug>.py: which ArtImage each parallax layer comes from, how
it is cropped and placed, how fast it scrolls, the pieces cut out of it to animate (the bell, the banner),
the anchors the game's moving parts hang off (the lantern's smoke, the water, the arch board), and the procedural
floor. This script writes, per style:

    OUT/<slug>-<layer>-<style>.png       each layer (pixel: indexed, a palette per layer; HD: 4x, smooth)
    OUT/<slug>-<cutout>-<style>.png      each cutout, its hole in the layer filled
    OUT/<slug>-<style>.json              the manifest kind_robots' stages.ts reads
    OUT/preview/<slug>-<style>.png       the stage composed at camera left, centre and right

Geometry is in game pixels on the 480x270 view (the floor line at y 238). A layer that scrolls at `factor`
must be 480 + 2 * 144 * factor wide to cover the view at both camera limits (sim STAGE_HALF_WIDTH 384,
so the camera travels +-144), and it sits centred: x = (480 - width) / 2.

    python projects/zuzu-showdown/tools/stage.py SLUG SOURCE_DIR OUT_DIR

SOURCE_DIR holds the source art as <art_image_id>.png. A layer may set `crop` (source pixels) and
`mirror: true` (the crop followed by its mirror image); boxes and anchors are given in the uncropped
source, and a point past the crop's right edge lands in the mirrored half.
"""

from __future__ import annotations

import importlib
import json
import random
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sprite_common as sc

VIEW = (480, 270)
FLOOR_Y = 238
CAMERA_TRAVEL = 144
HD = sc.HD_SCALE


def span(factor: float) -> int:
    """The width a layer scrolling at `factor` needs to cover the view at both camera limits."""
    return VIEW[0] + int(np.ceil(2 * CAMERA_TRAVEL * factor)) + 2


def load(source_dir: Path, spec: dict) -> Image.Image:
    image = Image.open(source_dir / f"{spec['art']}.png").convert("RGB")
    if spec.get("crop"):
        image = image.crop(spec["crop"])
    if spec.get("mirror"):
        # The crop and its mirror image side by side: closes a scene cut short (the pond without the cow).
        doubled = Image.new("RGB", (image.width * 2, image.height))
        doubled.paste(image, (0, 0))
        doubled.paste(image.transpose(Image.Transpose.FLIP_LEFT_RIGHT), (image.width, 0))
        image = doubled
    spec["_box"] = (0, 0, image.width, image.height)
    if spec.get("kind") == "keyed":
        image = sc.key_background(image)
        box = image.getchannel("A").getbbox() or (0, 0, image.width, image.height)
        spec["_box"] = box
        image = image.crop(box)
    return image.convert("RGBA")


def place(image: Image.Image, spec: dict) -> tuple[Image.Image, float, int, int]:
    """Scale a layer's source to game size and size its canvas: returns the layer at HD (4x game), the
    source-to-game scale, and its game-pixel width and top."""
    width = span(spec["factor"])
    if spec["kind"] == "full":
        # Cover the layer's box, then crop to it (centred, or `focus_x` of the way across).
        height = spec["height"]
        scale = max(width / image.width, height / image.height)
        size = (round(image.width * scale * HD), round(image.height * scale * HD))
        big = image.resize(size, Image.Resampling.LANCZOS)
        left = round((size[0] - width * HD) * spec.get("focus_x", 0.5))
        top = round((size[1] - height * HD) * spec.get("focus_y", 0.5))
        big = big.crop((left, top, left + width * HD, top + height * HD))
        spec["_left"], spec["_top"] = left / HD, top / HD
        return big, scale, width, spec.get("top", 0)
    # Keyed art keeps its shape: scaled to its height, its content's bottom on `bottom`, centred.
    height = spec["height"]
    scale = height / image.height
    content_w = round(image.width * scale)
    width = max(width, content_w)
    canvas = Image.new("RGBA", (width * HD, height * HD), (0, 0, 0, 0))
    scaled = image.resize((content_w * HD, height * HD), Image.Resampling.LANCZOS)
    offset = round((width - content_w) * spec.get("focus_x", 0.5))
    canvas.alpha_composite(scaled, (offset * HD, 0))
    # Remember where the source landed so boxes in source pixels map onto the layer.
    spec["_offset"] = offset
    return canvas, scale, width, spec["bottom"] - height


def floor_layer(spec: dict, seed: int) -> Image.Image:
    """The street: a dirt band in the stage's ground colours, rutted and pebbled, drawn at game size."""
    width, height = span(spec["factor"]), VIEW[1] - spec["top"]
    rng = random.Random(seed)
    colours = [tuple(c) for c in spec["colours"]]  # dark to light
    img = Image.new("RGBA", (width, height), colours[1] + (255,))
    px = img.load()
    for y in range(height):
        for x in range(width):
            band = 1 + (1 if rng.random() < 0.18 else 0) - (1 if rng.random() < 0.12 else 0)
            px[x, y] = colours[max(0, min(len(colours) - 1, band))] + (255,)
    # The lip where the street meets the backdrop, then two wheel ruts.
    for x in range(width):
        px[x, 0] = colours[0] + (255,)
        if rng.random() < 0.7:
            px[x, 1] = colours[0] + (255,)
    for rut in spec.get("ruts", []):
        for x in range(width):
            y = rut + (1 if (x // 37) % 2 else 0)
            if 0 <= y < height:
                px[x, y] = colours[0] + (255,)
    for _ in range(width // 6):
        x, y = rng.randrange(width), rng.randrange(3, height)
        px[x, y] = colours[-1] + (255,)
    return img


def to_pixel(hd: Image.Image) -> Image.Image:
    size = (hd.width // HD, hd.height // HD)
    colour = hd.convert("RGB").filter(ImageFilter.ModeFilter(3)).resize(size, Image.Resampling.LANCZOS)
    alpha = hd.getchannel("A").resize(size, Image.Resampling.BOX).point(lambda a: 255 if a >= 128 else 0)
    out = colour.convert("RGBA")
    out.putalpha(alpha)
    return out


def layer_palette(images: list[Image.Image], colours: int) -> Image.Image:
    """One palette for a layer and its cutouts, from their opaque pixels. Octree, not the fighters' median
    cut: median cut spends the colours on the sky's broad gradient and drops the small bright sun."""
    opaque = np.concatenate(
        [np.asarray(image.convert("RGBA"))[..., :3][np.asarray(image.getchannel("A")) > 0] for image in images]
    )
    swatch = Image.fromarray(opaque.reshape(1, -1, 3).astype(np.uint8), "RGB")
    return swatch.quantize(colours, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE)


def fill_hole(layer: Image.Image, box: tuple[int, int, int, int]) -> None:
    """Fill a cut-out's hole with the median colour around it, so the static layer doesn't show a
    second bell behind the swinging one; transparent pixels stay transparent."""
    x0, y0, x1, y1 = box
    arr = np.asarray(layer).copy()
    ring = []
    for x in range(max(0, x0 - 1), min(layer.width, x1 + 1)):
        for y in (y0 - 1, y1):
            if 0 <= y < layer.height and arr[y, x, 3]:
                ring.append(arr[y, x, :3])
    for y in range(max(0, y0), min(layer.height, y1)):
        for x in (x0 - 1, x1):
            if 0 <= x < layer.width and arr[y, x, 3]:
                ring.append(arr[y, x, :3])
    colour = np.median(np.array(ring), axis=0).astype(np.uint8) if ring else np.array([40, 30, 24], np.uint8)
    region = arr[y0:y1, x0:x1]
    mask = region[..., 3] > 0
    region[mask, :3] = colour
    arr[y0:y1, x0:x1] = region
    layer.paste(Image.fromarray(arr, "RGBA"))


def main(slug: str, source_dir: str, out_dir: str) -> None:
    cfg = importlib.import_module(f"stages.{slug.replace('-', '_')}")
    src, out = Path(source_dir), Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "preview").mkdir(exist_ok=True)

    layers_hd: dict[str, Image.Image] = {}
    meta: dict[str, dict] = {}
    for spec in cfg.LAYERS:
        name = spec["name"]
        if spec["kind"] == "floor":
            pixel = floor_layer(spec, cfg.SEED)
            layers_hd[name] = pixel.resize((pixel.width * HD, pixel.height * HD), Image.Resampling.NEAREST)
            meta[name] = {"factor": spec["factor"], "w": pixel.width, "h": pixel.height,
                          "x": (VIEW[0] - pixel.width) // 2, "y": spec["top"], "scale": None, "offset": 0}
            continue
        hd, scale, width, top = place(load(src, spec), spec)
        layers_hd[name] = hd
        meta[name] = {"factor": spec["factor"], "w": width, "h": hd.height // HD,
                      "x": (VIEW[0] - width) // 2, "y": top, "scale": scale, "offset": spec.get("_offset", 0),
                      "crop": spec.get("crop")}

    def to_layer(name: str, point) -> tuple[int, int]:
        """A source-pixel point (in the uncropped ArtImage) as layer game pixels."""
        m = meta[name]
        spec = next(s for s in cfg.LAYERS if s["name"] == name)
        x, y = point
        if spec.get("crop"):
            x, y = x - spec["crop"][0], y - spec["crop"][1]
        if spec["kind"] == "keyed":
            x, y = x - spec["_box"][0], y - spec["_box"][1]
            return round(x * m["scale"]) + m["offset"], round(y * m["scale"])
        # A full layer was cropped after scaling; undo that crop.
        return (round(x * m["scale"] - spec["_left"]), round(y * m["scale"] - spec["_top"]))

    # Cut the animated pieces out at HD, fill their holes.
    cutouts_hd: dict[str, Image.Image] = {}
    cut_meta = []
    for name, spec in getattr(cfg, "CUTOUTS", {}).items():
        layer = spec["layer"]
        x0, y0 = to_layer(layer, spec["box"][:2])
        x1, y1 = to_layer(layer, spec["box"][2:])
        box_hd = (x0 * HD, y0 * HD, x1 * HD, y1 * HD)
        cutouts_hd[name] = layers_hd[layer].crop(box_hd)
        fill_hole(layers_hd[layer], box_hd)
        cut_meta.append({"name": name, "layer": layer, "x": x0, "y": y0, "w": x1 - x0, "h": y1 - y0})
    anchors = {}
    for name, spec in getattr(cfg, "ANCHORS", {}).items():
        x, y = to_layer(spec["layer"], spec["at"][:2])
        anchor = {"layer": spec["layer"], "x": x, "y": y}
        if len(spec["at"]) == 4:
            x1, y1 = to_layer(spec["layer"], spec["at"][2:])
            anchor.update({"w": x1 - x, "h": y1 - y})
        anchors[name] = anchor

    # Pixel style: every layer and cutout at game size.
    pixel_layers = {n: to_pixel(im) for n, im in layers_hd.items()}
    pixel_cuts = {n: to_pixel(im) for n, im in cutouts_hd.items()}
    # Each layer gets its own palette (its cutouts share it): with one palette for the stage the sky took
    # the colours and the pond's water went missing.
    for name in pixel_layers:
        cuts = [c["name"] for c in cut_meta if c["layer"] == name]
        palette = layer_palette([pixel_layers[name]] + [pixel_cuts[c] for c in cuts], cfg.PALETTE_COLOURS)
        pixel_layers[name] = sc.quantize(pixel_layers[name], palette)
        for c in cuts:
            pixel_cuts[c] = sc.quantize(pixel_cuts[c], palette)

    from rig import save_atlas  # the exact indexed PNG writer
    for style, layers, cuts, scale in (("pixel", pixel_layers, pixel_cuts, 1), ("hd", layers_hd, cutouts_hd, HD)):
        manifest = {"stage": slug, "style": style, "scale": scale, "layers": [], "cutouts": [], "anchors": anchors}
        for spec in cfg.LAYERS:
            name = spec["name"]
            file = f"{slug}-{name}-{style}.png"
            save_atlas(layers[name], out / file, style == "pixel")
            m = meta[name]
            manifest["layers"].append({"name": name, "file": file, "factor": m["factor"], "x": m["x"], "y": m["y"],
                                       "w": m["w"], "h": m["h"]})
        for cut in cut_meta:
            file = f"{slug}-{cut['name']}-{style}.png"
            save_atlas(cuts[cut["name"]], out / file, style == "pixel")
            manifest["cutouts"].append({**cut, "file": file})
        (out / f"{slug}-{style}.json").write_text(json.dumps(manifest, indent=1) + "\n")
        preview(manifest, layers, cuts, scale, out / "preview" / f"{slug}-{style}.png")
    print(json.dumps({"stage": slug, "layers": {n: [meta[n]["w"], meta[n]["h"]] for n in meta},
                      "cutouts": [c["name"] for c in cut_meta], "anchors": list(anchors),
                      "pixel_colours": sc.palette_size(list(pixel_layers.values()))}))


def preview(manifest: dict, layers: dict, cuts: dict, scale: int, path: Path) -> None:
    """The stage at camera left, centre and right, stacked, with the floor line marked."""
    shots = []
    for cam in (-CAMERA_TRAVEL, 0, CAMERA_TRAVEL):
        view = Image.new("RGBA", (VIEW[0] * scale, VIEW[1] * scale), (0, 0, 0, 255))
        for layer in manifest["layers"]:
            x = round(layer["x"] - cam * layer["factor"])
            view.alpha_composite(layers[layer["name"]], (x * scale, layer["y"] * scale))
            for cut in manifest["cutouts"]:
                if cut["layer"] == layer["name"]:
                    view.alpha_composite(cuts[cut["name"]], ((x + cut["x"]) * scale, (layer["y"] + cut["y"]) * scale))
        shots.append(view)
    sheet = Image.new("RGBA", (VIEW[0] * scale, VIEW[1] * scale * 3 + 8 * scale), (255, 0, 0, 255))
    for i, shot in enumerate(shots):
        sheet.alpha_composite(shot, (0, i * (VIEW[1] + 4) * scale))
    sheet.convert("RGB").save(path)


if __name__ == "__main__":
    main(*sys.argv[1:4])
