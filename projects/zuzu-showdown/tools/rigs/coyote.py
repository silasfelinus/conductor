"""The Coyote Vagrant's rig (zuzu-showdown t-010).

Parts are cut from his profile-right reference (ArtImage 242404, already facing right) until the t-010
parts sheet (art/T010-RIG-PARTS.yaml) lands; then each part's `art`, `polygon` and `pivot` move to the
cleaner sheet without touching the animations. Coordinates are the source image's pixels (832 x 1216);
about 11 of them make one game pixel at his 104 px height.

Post-croc (Silas, 2026-10-07): his right hand is gone and a knife is lashed to the bandaged stump. He
faces right, so that near arm is the stump arm, drawn in front of the coat; his left arm, with the
revolver he fires left-handed and badly, is on the far side and drawn behind it.
"""

from __future__ import annotations

import math

from PIL import ImageDraw

HEIGHT = 104
PALETTE_COLOURS = 16
REFERENCE = {"art": 242404}

NECK = (430, 300)
HIP_BACK = (300, 880)
HIP_FRONT = (460, 620)
SHOULDER_NEAR = (300, 340)
SHOULDER_FAR = (440, 340)

PARTS = {
    "back_leg": {"art": 242404, "z": 1, "pivot": HIP_BACK, "follows": [],
                 "polygon": [(226, 860), (372, 860), (352, 1000), (346, 1196), (210, 1196), (228, 1000)]},
    "front_leg": {"art": 242404, "z": 2, "pivot": HIP_FRONT, "follows": [],
                  "polygon": [(376, 560), (560, 600), (566, 800), (546, 900), (566, 960), (704, 1096), (694, 1166),
                              (496, 1166), (476, 1000), (436, 900), (376, 820)]},
    "torso": {"art": 242404, "z": 3, "pivot": HIP_FRONT, "follows": ["body"],
              "polygon": [(176, 256), (426, 250), (520, 316), (532, 560), (500, 560), (430, 600), (400, 820),
                          (382, 906), (196, 906), (168, 700), (186, 500)]},
    "head": {"art": 242404, "z": 4, "pivot": NECK, "follows": ["body"],
             "polygon": [(278, 56), (600, 36), (606, 214), (572, 252), (520, 284), (430, 304), (330, 326),
                         (288, 250)]},
}

INK = (20, 16, 14)
SLEEVE = (98, 117, 92)
SLEEVE_FAR = (52, 72, 46)
BANDAGE = (212, 203, 165)
FUR = (171, 153, 124)
STEEL = (196, 204, 214)
STEEL_EDGE = (246, 248, 250)
GUNMETAL = (58, 60, 66)
FLASH = (255, 236, 150)
FLASH_CORE = (255, 255, 236)
SAND = (214, 186, 128)


def _limb(d, start, end, width, colour):
    d.line([start, end], fill=INK, width=width + 16)
    d.line([start, end], fill=colour, width=width)


def stump_arm(canvas, offset, hand, knife=0, dy=0):
    """His right arm: the coat sleeve, the bandaged stump, the knife lashed to it pointing `knife`
    degrees (0 = straight ahead, positive = up)."""
    d = ImageDraw.Draw(canvas)
    s = (SHOULDER_NEAR[0] + offset[0], SHOULDER_NEAR[1] + offset[1] + dy)
    h = (hand[0] + offset[0], hand[1] + offset[1])
    _limb(d, s, h, 66, SLEEVE)
    d.ellipse([h[0] - 34, h[1] - 34, h[0] + 34, h[1] + 34], fill=INK)
    d.ellipse([h[0] - 26, h[1] - 26, h[0] + 26, h[1] + 26], fill=BANDAGE)
    a = math.radians(knife)
    ux, uy = math.cos(a), -math.sin(a)
    tip = (h[0] + ux * 300, h[1] + uy * 300)
    d.line([h, tip], fill=INK, width=30)
    d.line([h, tip], fill=STEEL, width=16)
    d.line([(h[0] - uy * 4, h[1] + ux * 4), (tip[0] - uy * 4, tip[1] + ux * 4)], fill=STEEL_EDGE, width=5)
    for k in (-14, 0, 14):  # the bandage wraps lashing the knife on
        cx, cy = h[0] + ux * (30 + k), h[1] + uy * (30 + k)
        d.line([(cx - uy * 24, cy + ux * 24), (cx + uy * 24, cy - ux * 24)], fill=BANDAGE, width=8)


def gun_arm(canvas, offset, hand, aim=0, flash=False, dy=0):
    """His left arm on the far side, holding the revolver, aimed `aim` degrees; `flash` fires it."""
    d = ImageDraw.Draw(canvas)
    s = (SHOULDER_FAR[0] + offset[0], SHOULDER_FAR[1] + offset[1] + dy)
    h = (hand[0] + offset[0], hand[1] + offset[1])
    _limb(d, s, h, 58, SLEEVE_FAR)
    d.ellipse([h[0] - 30, h[1] - 30, h[0] + 30, h[1] + 30], fill=INK)
    d.ellipse([h[0] - 22, h[1] - 22, h[0] + 22, h[1] + 22], fill=FUR)
    a = math.radians(aim)
    ux, uy = math.cos(a), -math.sin(a)
    muzzle = (h[0] + ux * 150, h[1] + uy * 150)
    d.line([h, muzzle], fill=INK, width=40)
    d.line([h, muzzle], fill=GUNMETAL, width=26)
    d.ellipse([h[0] + ux * 30 - 26, h[1] + uy * 30 - 26, h[0] + ux * 30 + 26, h[1] + uy * 30 + 26], fill=GUNMETAL,
              outline=INK, width=6)
    if flash:
        cx, cy = muzzle[0] + ux * 60, muzzle[1] + uy * 60
        for k in range(8):
            r = 110 if k % 2 == 0 else 55
            t = a + k * math.pi / 4
            d.line([(cx, cy), (cx + math.cos(t) * r, cy - math.sin(t) * r)], fill=FLASH, width=22)
        d.ellipse([cx - 40, cy - 40, cx + 40, cy + 40], fill=FLASH_CORE)


def sand(canvas, offset, origin, reach=1.0):
    """A thrown fistful of grit: a widening cone of grains."""
    d = ImageDraw.Draw(canvas)
    ox, oy = origin[0] + offset[0], origin[1] + offset[1]
    for i in range(36):
        t = (i * 37 % 100) / 100
        x = ox + 60 + t * 360 * reach
        y = oy - 40 + ((i * 53) % 90 - 45) * (0.4 + t * 1.6)
        r = 9 if i % 3 else 13
        d.ellipse([x - r, y - r, x + r, y + r], fill=SAND, outline=INK, width=3)


def stump(hand, knife=0, dy=0):
    return {"fn": "stump_arm", "args": {"hand": hand, "knife": knife, "dy": dy}}


def gun(hand, aim=0, flash=False, dy=0):
    return {"fn": "gun_arm", "args": {"hand": hand, "aim": aim, "flash": flash, "dy": dy}}


def slouch(dy=0, head=0, sway=0):
    return {"body": {"dy": dy, "angle": sway}, "head": {"dy": head}}


ANIMATIONS = {
    # A slouching, coughing sway rather than a guard: he fights like someone with nothing left to lose.
    "idle": {"fps": 7, "loop": True, "frames": [slouch(0), slouch(-6, -2, 1), slouch(-10, -4, 2), slouch(-6, -6, 1)]},
    "walk_forward": {"fps": 11, "loop": True, "frames": [
        {"front_leg": {"angle": 16}, "back_leg": {"angle": -14}, "body": {"dy": 6, "angle": 2}},
        {"front_leg": {"angle": 8}, "back_leg": {"angle": -6, "dy": -10}, "body": {"dy": 14, "angle": 2}},
        {"front_leg": {"angle": -4}, "back_leg": {"angle": 6, "dy": -20}, "body": {"dy": 0, "angle": 1}},
        {"front_leg": {"angle": -14}, "back_leg": {"angle": 14}, "body": {"dy": -10, "angle": 0}},
        {"front_leg": {"angle": -18}, "back_leg": {"angle": 16}, "body": {"dy": 6, "angle": 1}},
        {"front_leg": {"angle": -6, "dy": -20}, "back_leg": {"angle": 6}, "body": {"dy": 0, "angle": 2}},
    ]},
    # Each leg squashes about its hip by its own amount so both feet rise the same 160 px, then the
    # legs and body drop 160 px to put the feet back on the floor.
    "crouch": {"fps": 12, "loop": False, "frames": [
        {"body": {"dy": 80, "angle": 6}, "front_leg": {"sy": -0.15, "dy": 80}, "back_leg": {"sy": -0.25, "dy": 80}},
        {"body": {"dy": 160, "angle": 12}, "front_leg": {"sy": -0.29, "sx": 0.1, "dy": 160, "angle": 4},
         "back_leg": {"sy": -0.5, "sx": 0.1, "dy": 160, "angle": -4}},
    ]},
    "jump_up": {"fps": 12, "loop": False, "frames": [
        {"body": {"dy": 60}, "front_leg": {"sy": -0.11, "dy": 60}, "back_leg": {"sy": -0.19, "dy": 60}},
        # His front leg is cut long (from under the coat), so it barely rotates; the squash does the tuck.
        {"body": {"angle": -4}, "front_leg": {"sy": -0.32, "angle": 4}, "back_leg": {"sy": -0.45, "angle": 10}},
        {"body": {"angle": -8}, "front_leg": {"sy": -0.4, "angle": 6}, "back_leg": {"sy": -0.55, "angle": 18}},
    ]},
    "stand_hp": {"fps": 15, "loop": False, "frames": [
        {**slouch(10, 0, -4), "draw": [stump((250, 520), knife=30, dy=10)]},
        {**slouch(6, 0, 6), "front_leg": {"angle": 12}, "draw": [stump((560, 470), knife=4, dy=6)]},
        {**slouch(4, 0, 10), "front_leg": {"angle": 16}, "draw": [stump((700, 440), knife=0, dy=4)]},
        {**slouch(8, 0, 4), "draw": [stump((480, 500), knife=10, dy=8)]},
    ]},
    # Wild Shot: a left-handed draw, a shaky aim, the shot, the kick, the gun drifting down.
    "wild_shot": {"fps": 14, "loop": False, "frames": [
        {**slouch(4), "draw_behind": [gun((470, 640), aim=-60, dy=4)]},
        {**slouch(2, 0, -2), "draw_behind": [gun((640, 430), aim=4, dy=2)]},
        {**slouch(2, 0, -2), "draw_behind": [gun((660, 430), aim=2, flash=True, dy=2)]},
        {**slouch(0, -4, -6), "draw_behind": [gun((620, 380), aim=24, dy=0)]},
        {**slouch(4, 0, 0), "draw_behind": [gun((560, 520), aim=-20, dy=4)]},
    ]},
    # Pocket Sand: dig in the coat pocket, wind up, fling.
    "pocket_sand": {"fps": 14, "loop": False, "frames": [
        {**slouch(14, 0, 4), "draw": [stump((300, 640), knife=-70, dy=14)]},
        {**slouch(6, 0, -4), "draw": [stump((240, 420), knife=60, dy=6)]},
        {**slouch(4, 0, 8), "draw": [stump((600, 380), knife=10, dy=4),
                                     {"fn": "sand", "args": {"origin": (600, 380), "reach": 1.0}}]},
    ]},
}

# P2's alternate colours: the green riding coat turns maroon, everything else stays (the boots and hat
# are the same brown leather as P1, which keeps him readable as the same vagrant).
P2_RULES = [
    {"hue": (55, 125), "sat_min": 0.1, "shift": -115, "sat": 1.3},
]
