"""zuzu-showdown t-007, method C: hand-authored indexed pixel maps.

Every pixel below was typed by hand against the reference build (A7, ArtImage 242193, facing right),
one character per pixel, in a fixed 18-colour palette. Like a pixel artist working in layers, the
body above the waist is drawn once and each frame adds its own hand-drawn layer: the legs for the
walk, the sword arm (and the slash smear) for the standing HP. The idle breathes by moving the
upper body one pixel, the oldest trick in the sprite book.

    python projects/zuzu-showdown/tools/method_c_pixels.py OUT_DIR
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sprite_common as sc

PALETTE = {
    ".": None,
    "k": (28, 22, 30),  # ink
    "g": (138, 150, 163),  # fur
    "G": (92, 100, 114),  # fur shadow
    "l": (208, 214, 222),  # fur light, ear tuft
    "n": (16, 14, 18),  # nose
    "r": (168, 74, 44),  # eye
    "s": (226, 196, 140),  # straw
    "S": (176, 140, 92),  # straw shadow
    "o": (238, 132, 44),  # orange band, neckerchief
    "O": (186, 88, 28),  # orange shadow
    "p": (188, 144, 100),  # poncho
    "P": (134, 96, 62),  # poncho shadow
    "z": (236, 206, 160),  # zigzag trim
    "t": (112, 72, 46),  # trousers
    "T": (74, 46, 32),  # trousers shadow
    "h": (44, 34, 32),  # hilt wrap
    "y": (222, 200, 150),  # hilt diamonds, end cap
    "m": (190, 200, 212),  # steel
    "M": (248, 250, 252),  # steel edge, smear
}
WIDTH, HEIGHT = 80, 76
# Where the figure sits on the frame (the slash needs room in front).
X0 = 4

# Rows 0-49: hilt, kasa, head, neckerchief and poncho. The hand rests on the belly.
UPPER = """




...................kkkkkkk
.................kksssssssk
...............kkssssssssssk
..............kssssSssssssssk
.............kssssSSsssssssssk
...........kooooooooooooooooook
.........kkoOOOOOOOOOOOOOOOOOOok
........kssssssssssssssssssssssskkkk
.......ksSSSSssssssssssssssssssssssssskkk
........kkkkSSSSSSSSSSSSSSSSSSSSSSSSSkkk.kk.k
......kgglkkkkkkkkkkkkkkkkkkkkkkkkkk
.....kgllllgkgggggggggggggggk
.....kglllgkgggggggggGGGgggggk
.....kgllllgggggggggkkkrgggggk
.....kgglllgggggggggggkkgggggkkk
......kgllgggggggggggggggggggknnk
......kggggggggggggggggggggggnnnnk
.......kGggggggggggggggggggggnnnnk
.......kGGgggggggggggggggggggknnk
........kGGgggggggggglllllgggggk
.........kGGGgggggggglkkkllgggk
..........kkoooooooooooooooooook
.........kooooooOOOoooooooooooook
........kpooooOOOOOOOoooooooooooook
.......kppppOOOOOOOOOOOOOOOOOOOOppk
......kpppppppppppppppppppppppppppppk
.....kPpppppppppppppppppppppppppppppk
.....kPPppppppppppppppppppppppppppppk
....kPPPpppppppppppppppppppppppppppppk
....kPPPppppppgggkppppppppppppppppppppk
...kPPPPpppppgggggkppppppppppppppppppppk
...kPPPPppppggggggkpppppppppppppppppppppk
...kPPPPPpppgggggkppppppppppppppppppppppk
..kPPPPPPppggggggkppppppppppppppppppppppk
..kPPzPPPzPggggkPzpppzpppzpppzpppzppppppk
..kPzPzPzPzgggkzPzpzpzpzpzpzpzpzpzpzpzppk
..kzPPPzPPPzglgkzPPPzpppzpppzpppzpppzpppk
..kPPPPPPPPPkllgkPPPPpppppppppppppppppppk
...kPPPPPPPPPkllkPPPPPppppppppppppppppppk
...kOOOOOkPPPPPkkPPPPPPpppppppppppppppppk
....kOOOOkPPPPPPPPPPPPPPPPpppppppppppppk
.....kkkkkkPPPPPPPPPPPPPPPPPPPppppppppk
...........kkkPPPPPPPPPPPPPPPPPPPPPPkk
..............kkkkPPPPPPPPPPPPPPPkkk
..................kkkkkkkkkkkkkkk
"""

# The katana's hilt over his right shoulder, drawn behind the kasa (columns from X0 + 4).
HILT = """
kkk
kyyk
.kyyk
.khhk
..kyhk
..khyk
...kyhk
...khyk
....kyhk
....khyk
.....kyhk
.....khyk
......khhk
......kkk
"""

# Rows 46-75: legs. One map per walk frame; IDLE_LEGS is the planted fighting stance.
IDLE_LEGS = """
..........kttttTTk.....kTTttttk
.........kttttttTTk...kTTttttttk
.........ktttttttTTk.kTTtttttttk
.........ktttttttTTTkTTTtttttttk
........kttttttttTTTkTTTttttttttk
........kttttttttTTkkkTTtttttttttk
........ktttttttTTk...kTTttttttttk
........ktttttttTTk....kTTtttttttk
........kttttttTTk.....kTTttttttk
.........ktttttTk.......kTtttttk
.........kTTTTTTk.......kTTTTTTk
..........kgggGk.........kggggGk
..........kgggGk.........kggggGk
.........kggggGGk.......kgggggGGk
........kgggggggGkk....kgggggggGGkk
.......kkkkkkkkkkkk....kkkkkkkkkkkkk
"""

WALK_LEGS = [
    # 1: contact, front heel landing, back toe pushing
    """
..........ktttttTk.....kTTttttk
.........kttttttTTk...kTTtttttk
........kttttttTTk.....kTTtttttk
.......ktttttttTk.......kTTtttttk
......kttttttTTk.........kTTtttttk
......kttttttTk...........kTttttttk
.....ktttttTTk.............kTTttttk
.....kttttTTk...............kTTtttk
....kttttTTk.................kTttttk
....kTTTTTk...................kTTTTk
...kgggGk......................kggGk
...kgggGk......................kgggGk
..kgggGk.......................kggggGk
.kggggk.........................kgggggGk
.kkkkk...........................kkkkkkkk
""",
    # 2: down, weight on the front foot
    """
..........ktttttTk....kTTttttk
.........kttttttTTk..kTTtttttk
.........ktttttTTk....kTTttttk
........kttttttTk......kTTtttk
........ktttttTk........kTttttk
.......kttttttk.........kTTtttk
.......ktttttTk..........kTtttk
......ktttttTk...........kTTttk
......kttttTk.............kTttk
.....kTTTTTk..............kTTTk
.....kggGGk...............kgggk
....kgggGk................kgggk
....kggGk................kggggGk
...kkgGk................kgggggggk
...kkkk.................kkkkkkkkk
""",
    # 3: passing, back leg swinging through
    """
..............kttttTTttttk
.............kttttttTTtttk
.............kttttttTTtttk
.............kttttttTTttk
............ktttttttTTttk
............kttttttTTtttk
...........ktttttttTTtttk
...........ktttttkkTTtttk
..........kttttk.kTTttttk
..........kTTTTk.kTTTTTTk
..........kgggGk..kgggGk
..........kggGGk..kgggGk
...........kggk..kggggGk
...........kkk..kgggggggk
................kkkkkkkkk
""",
    # 4: up, rising on the standing leg, the free foot lifted and reaching forward
    """
..............kttttTTttttk
.............kttttttTTttttk
.............kttttttTTtttttk
............ktttttttTTtttttk
............kttttttkkTTtttttk
...........kttttttk..kTTttttk
...........kttttttk...kTTtttk
..........kttttttk....kTTTTTk
..........kttttTk.....kgggGk
..........kTTTTk.....kggggGk
..........kgggGk....kgggggGk
..........kgggGk....kkkkkkkk
..........kggggGk
..........kgggggGk
..........kkkkkkkk
""",
    # 5: contact on the other leg (mirror of 1's legs, swapped shading)
    """
..........kTTttttk.....ktttttTk
.........kTTtttttk...kttttttTTk
........kTTtttttk.....kttttttTTk
.......kTTtttttk.......kttttttTk
......kTTtttttk.........kttttttTk
......kTttttttk..........kttttttTk
.....kTTttttk.............kttttttk
.....kTTtttk...............kttttTk
....kTttttk.................kttttTk
....kTTTTk...................kTTTTTk
...kggGk......................kgggGk
...kgggGk.....................kgggGk
..kggggGk.....................kggggGk
.kgggggGk......................kgggggGk
.kkkkkkk........................kkkkkkkk
""",
    # 6: passing on the other leg
    """
..............kttttTTttttk
.............ktttTTttttttk
.............ktttTTtttttk
.............kttTTttttttk
............kttTTtttttttk
............ktttTTttttttk
...........ktttTTtttttttk
...........ktttTTkktttttk
..........kttttTTk.kttttk
..........kTTTTTTk.kTTTTk
...........kgggGk..kgggGk
...........kgggGk..kggGGk
...........kggggGk..kggk
...........kgggggggk.kkk
...........kkkkkkkkk
""",
]

# The standing HP, frame by frame: extra rows of offset to crouch, the hand/sword layer drawn on
# top (row, column, map), and whether the hilt still shows on his back.
HP = [
    # 1: crouch and grip the hilt over the shoulder
    {"dy": 2, "sheathed": True, "layer": (4, 6, """
...kk
..kggk
.kgggk
.kgggGk
..kgggk
...kgggk
....kgggk
.....kgggk
......kgGk
.......kk
""")},
    # 2: the draw, blade flashing up and out
    {"dy": 1, "sheathed": False, "layer": (0, 26, """
..................MM
.................Mmk
................Mmk
...............Mmk
..............Mmk
.............Mmk
............Mmk
...........Mmk
..........Mmk
.........kyk
........khhk
.......khhk
......khyk
.....kggk
....kgggk
...kgggk
..kgggk
.kgggk
kgggk
""")},
    # 3: the cut, blade straight out at chest height, with a smear behind it
    {"dy": 0, "sheathed": False, "layer": (30, 24, """
............................MM
.....................MMMMMMMMMMMMMM
...........MMMMMMMMMMMMMMMMM....
kkkkkkk.kkkk...........
kgggggggkhhyhhkkmmmmmmmmmmmmmmmmmmmmmmmMk
kgggggggkhyhhykmmmmmmmmmmmmmmmmmmmmmmmMMk
kkkkkkk.kkkk.kkkkkkkkkkkkkkkkkkkkkkkkkkk
""")},
    # 4: follow-through, blade swept low
    {"dy": 1, "sheathed": False, "layer": (24, 20, """
kkkkkk
kgggggk
.kggggkk
..kgggkhk
...kkkhyhk
.....khyhk
......kkkmk
.........kmmk
..........kmmk
...........kmmk
............kmmk
.............kmmk
..............kmMk
...............kMk
................kk
""")},
    # 5: re-sheathe, hand back at the hilt
    {"dy": 0, "sheathed": True, "layer": (5, 7, """
..kk
.kggk
.kgggk
..kgggk
...kgggk
....kgggk
.....kgGk
......kk
""")},
]


def parse(block: str) -> list[str]:
    """One string per row; blank rows count (the body starts four rows down, under the hilt)."""
    return block.split("\n")[1:-1]


def paint(image: Image.Image, rows: list[str], x: int, y: int) -> None:
    px = image.load()
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            colour = PALETTE[ch]
            if colour is None:
                continue
            xx, yy = x + i, y + j
            if 0 <= xx < image.width and 0 <= yy < image.height:
                px[xx, yy] = colour + (255,)


LEGS_Y = 47


def frame(upper_dy=0, legs=IDLE_LEGS, sheathed=True, layer=None, crouch=0) -> Image.Image:
    image = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    if sheathed:
        paint(image, parse(HILT), X0 + 4, upper_dy + crouch)
    paint(image, parse(legs), X0, LEGS_Y + crouch)
    paint(image, parse(UPPER), X0, upper_dy + crouch)
    if layer:
        row, col, block = layer
        paint(image, parse(block), X0 + col, row + crouch)
    return image


def animations() -> dict[str, list[Image.Image]]:
    return {
        "idle": [frame(0), frame(1), frame(1), frame(0)],
        "walk": [frame(0 if i % 3 != 1 else 1, legs) for i, legs in enumerate(WALK_LEGS)],
        "hp": [frame(0, sheathed=f["sheathed"], layer=f["layer"], crouch=f["dy"]) for f in HP],
    }


def main(out_dir: str) -> None:
    out = Path(out_dir)
    every = []
    meta = {"method": "C hand pixel maps", "frames": {}, "hand_typed_pixels": 0}
    for name, frames in animations().items():
        sc.write_previews(frames, out, f"c-{name}", sc.FPS[name])
        meta["frames"][name] = len(frames)
        every.extend(frames)
    blocks = [UPPER, HILT, IDLE_LEGS, *WALK_LEGS, *(f["layer"][2] for f in HP)]
    meta["hand_typed_pixels"] = sum(ch != "." for b in blocks for ch in b if ch != "\n")
    meta["palette_colours"] = sc.palette_size(every)
    meta["frame_size"] = [WIDTH, HEIGHT]
    (out / "c-meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta))


if __name__ == "__main__":
    main(sys.argv[1])
