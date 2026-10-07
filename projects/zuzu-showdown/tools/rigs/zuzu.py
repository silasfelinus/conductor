"""Zuzu's rig (zuzu-showdown t-010).

Parts are cut from the t-010 parts sheet's fighting stance (ArtImage 242762: a wide, low stance facing
right, lead arm out, the off hand on his hip), so every pose starts from a real stance instead of the
standing reference. Scale still comes from the standing build A7 (242193), so the crouched stance keeps
his true size. Coordinates are the source image's pixels (832 x 1216); about 16 make one game pixel.
"""

from __future__ import annotations

import math

from PIL import ImageDraw

HEIGHT = 72
PALETTE_COLOURS = 16
REFERENCE = {"art": 242193, "mirror": True}  # scale only

HIP_BACK = (260, 790)
HIP_FRONT = (470, 790)
NECK = (420, 380)
SHOULDER = (610, 530)
STANCE = 242762

# The fighter's spot on the ground in the source art: midway between his planted feet.
ANCHOR = (420, 1168)

PARTS = {
    "hilt": {"art": STANCE, "z": 0, "pivot": NECK, "follows": ["body", "head"],
             "polygon": [(648, 44), (714, 60), (604, 336), (612, 362), (520, 374), (528, 330), (570, 318)]},
    "back_leg": {"art": STANCE, "z": 1, "pivot": HIP_BACK, "follows": [],
                 "polygon": [(160, 756), (334, 756), (304, 900), (244, 1020), (196, 1100), (184, 1168),
                             (56, 1168), (68, 1100), (128, 1000), (138, 880)]},
    "front_leg": {"art": STANCE, "z": 2, "pivot": HIP_FRONT, "follows": [],
                  "polygon": [(396, 756), (564, 756), (684, 880), (684, 1000), (644, 1100), (764, 1146),
                              (744, 1168), (576, 1168), (588, 1060), (556, 980), (466, 900)]},
    "torso": {"art": STANCE, "z": 3, "pivot": HIP_FRONT, "follows": ["body"],
              "polygon": [(36, 460), (160, 366), (500, 356), (626, 482), (654, 622), (566, 700), (544, 802),
                          (430, 862), (250, 802), (200, 722), (140, 642), (48, 562)]},
    "lead_arm": {"art": STANCE, "z": 4, "pivot": SHOULDER, "follows": ["body"],
                 "polygon": [(616, 516), (700, 466), (770, 436), (816, 456), (804, 524), (744, 564), (694, 624),
                             (628, 626)]},
    "head": {"art": STANCE, "z": 5, "pivot": NECK, "follows": ["body"],
             "polygon": [(228, 168), (500, 156), (722, 248), (704, 282), (562, 292), (560, 402), (480, 422),
                         (258, 382), (228, 300)]},
}

FUR = (138, 150, 163)
FUR_DARK = (70, 76, 88)
STEEL = (196, 204, 214)
STEEL_EDGE = (246, 248, 250)
INK = (24, 20, 26)
WRAP = (60, 44, 36)


def sword_arm(canvas, offset, hand, sword=None, dy=0):
    """The drawing arm (and, once drawn, the katana): the reference has no free arm, so it is drawn."""
    d = ImageDraw.Draw(canvas)
    s = (SHOULDER[0] + offset[0], SHOULDER[1] + offset[1] + dy)
    h = (hand[0] + offset[0], hand[1] + offset[1])
    d.line([s, h], fill=INK, width=74)
    d.line([s, h], fill=FUR, width=58)
    d.ellipse([h[0] - 40, h[1] - 40, h[0] + 40, h[1] + 40], fill=INK)
    d.ellipse([h[0] - 32, h[1] - 32, h[0] + 32, h[1] + 32], fill=FUR_DARK)
    if sword is None:
        return
    a = math.radians(sword)
    ux, uy = math.cos(a), -math.sin(a)
    grip = [(h[0] - ux * 150, h[1] - uy * 150), (h[0] + ux * 40, h[1] + uy * 40)]
    d.line(grip, fill=INK, width=44)
    d.line(grip, fill=WRAP, width=30)
    gx, gy = h[0] + ux * 50, h[1] + uy * 50
    d.line([(gx - uy * 46, gy + ux * 46), (gx + uy * 46, gy - ux * 46)], fill=INK, width=26)
    tip = (h[0] + ux * 640, h[1] + uy * 640)
    d.line([(gx, gy), tip], fill=INK, width=30)
    d.line([(gx, gy), tip], fill=STEEL, width=18)
    d.line([(gx - uy * 5, gy + ux * 5), (tip[0] - uy * 5, tip[1] + ux * 5)], fill=STEEL_EDGE, width=6)


def arm(hand, sword=None, dy=0):
    return {"fn": "sword_arm", "args": {"hand": hand, "sword": sword, "dy": dy}}


def stance(dy=0, head=0, arm=0):
    """The fighting stance is the source art itself, so a stance frame is just small offsets."""
    return {"body": {"dy": dy}, "head": {"dy": head}, "lead_arm": {"angle": arm}}


ANIMATIONS = {
    "idle": {"fps": 8, "loop": True, "frames": [stance(0), stance(-8, -2, 2), stance(-12, -4, 4), stance(-6, -4, 2)]},
    # A low shuffle: the stance is already wide, so the legs swing a little and the body bobs.
    "walk_forward": {"fps": 10, "loop": True, "frames": [
        {"front_leg": {"angle": 8}, "back_leg": {"angle": -6}, "body": {"dy": 6}},
        {"front_leg": {"angle": 4}, "back_leg": {"angle": -2, "dy": -10}, "body": {"dy": 14}, "lead_arm": {"angle": 3}},
        {"front_leg": {"angle": -2}, "back_leg": {"angle": 4, "dy": -18}, "body": {"dy": 4}, "lead_arm": {"angle": 5}},
        {"front_leg": {"angle": -8}, "back_leg": {"angle": 8}, "body": {"dy": -8}, "lead_arm": {"angle": 3}},
        {"front_leg": {"angle": -10, "dy": -12}, "back_leg": {"angle": 6}, "body": {"dy": 4}},
        {"front_leg": {"angle": -4, "dy": -18}, "back_leg": {"angle": 2}, "body": {"dy": 8}, "lead_arm": {"angle": -2}},
    ]},
    # Legs squash about the hips and drop by the same amount (375 px of leg), so the feet stay planted.
    "crouch": {"fps": 12, "loop": False, "frames": [
        {"body": {"dy": 66, "angle": 3}, "front_leg": {"sy": -0.18, "sx": 0.06, "dy": 66},
         "back_leg": {"sy": -0.18, "sx": 0.06, "dy": 66}, "lead_arm": {"angle": -8}},
        {"body": {"dy": 131, "angle": 6}, "front_leg": {"sy": -0.35, "sx": 0.12, "dy": 131},
         "back_leg": {"sy": -0.35, "sx": 0.12, "dy": 131}, "lead_arm": {"angle": -16}},
    ]},
    # In the air the engine moves him; the sprite tucks the legs up under the poncho.
    "jump_up": {"fps": 12, "loop": False, "frames": [
        {"body": {"dy": 50}, "front_leg": {"sy": -0.13, "dy": 50}, "back_leg": {"sy": -0.13, "dy": 50}},
        {"body": {"angle": -4}, "front_leg": {"sy": -0.4, "angle": 16}, "back_leg": {"sy": -0.4, "angle": -6},
         "lead_arm": {"angle": 20}},
        {"body": {"angle": -8}, "front_leg": {"sy": -0.5, "angle": 24}, "back_leg": {"sy": -0.48, "angle": -2},
         "lead_arm": {"angle": 30}},
    ]},
    # Standing HP, the draw-cut: the lead arm reaches back to the hilt over his shoulder, draws, cuts
    # straight out at chest height, follows through, and re-sheathes.
    "stand_hp": {"fps": 15, "loop": False, "frames": [
        {**stance(16), "hide": ["lead_arm"], "draw": [arm((600, 330), dy=16)]},
        {**stance(10), "hide": ["lead_arm", "hilt"], "draw": [arm((700, 270), 70, 10)]},
        {**stance(4), "body": {"dy": 4, "angle": 6}, "hide": ["lead_arm", "hilt"], "draw": [arm((830, 500), 0, 4)]},
        {**stance(8), "body": {"dy": 8, "angle": 4}, "hide": ["lead_arm", "hilt"], "draw": [arm((760, 620), -40, 8)]},
        {**stance(4), "hide": ["lead_arm"], "draw": [arm((610, 340), dy=4)]},
    ]},
}

# P2's alternate colours (Street Fighter style): the rust poncho and the orange trim turn slate blue.
# The trousers share the poncho's hue but are darker, so the value floor keeps them brown.
P2_RULES = [
    {"hue": (15, 40), "sat_min": 0.3, "val_min": 0.45, "shift": 190, "sat": 0.85},
]
