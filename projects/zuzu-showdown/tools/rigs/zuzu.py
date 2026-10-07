"""Zuzu's rig (zuzu-showdown t-010).

Parts are cut from the reference build A7 (ArtImage 242193, mirrored to face right) until the t-010
parts sheet (art/T010-RIG-PARTS.yaml) lands; then each part's `art`, `polygon` and `pivot` move to the
cleaner sheet without touching the animations below. Coordinates are the source image's pixels
(832 x 1216); about 16 of them make one game pixel.
"""

from __future__ import annotations

import math

from PIL import ImageDraw

HEIGHT = 72
PALETTE_COLOURS = 16
REFERENCE = {"art": 242193, "mirror": True}

HIP_BACK = (350, 830)
HIP_FRONT = (480, 830)
NECK = (440, 390)
SHOULDER = (470, 560)

PARTS = {
    "hilt": {"art": 242193, "mirror": True, "z": 0, "pivot": NECK, "follows": ["body", "head"],
             "polygon": [(186, 38), (246, 34), (342, 352), (338, 384), (232, 388), (226, 352), (262, 346)]},
    "back_leg": {"art": 242193, "mirror": True, "z": 1, "pivot": HIP_BACK, "follows": [],
                 "polygon": [(286, 790), (430, 800), (440, 1060), (420, 1210), (260, 1210), (276, 1000)]},
    "front_leg": {"art": 242193, "mirror": True, "z": 2, "pivot": HIP_FRONT, "follows": [],
                  "polygon": [(400, 800), (570, 800), (600, 900), (568, 1050), (600, 1210), (380, 1210),
                              (410, 1060)]},
    "torso": {"art": 242193, "mirror": True, "z": 3, "pivot": HIP_FRONT, "follows": ["body"],
              "polygon": [(186, 352), (560, 360), (676, 560), (700, 800), (620, 920), (560, 930), (420, 840),
                          (290, 810), (186, 760), (150, 620)]},
    "head": {"art": 242193, "mirror": True, "z": 4, "pivot": NECK, "follows": ["body"],
             "polygon": [(286, 150), (600, 112), (790, 236), (780, 290), (590, 300), (560, 400), (300, 400),
                         (282, 300)]},
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


def stance(dy=0, head=0, front=14, back=-12, lean=4):
    """The fighting stance every grounded move starts from: legs apart, weight low."""
    return {"body": {"dy": 24 + dy, "angle": lean}, "head": {"dy": head}, "front_leg": {"angle": front},
            "back_leg": {"angle": back}}


ANIMATIONS = {
    "idle": {"fps": 8, "loop": True, "frames": [stance(0), stance(-8, -2), stance(-14, -4), stance(-6, -4)]},
    "walk_forward": {"fps": 10, "loop": True, "frames": [
        {"front_leg": {"angle": 20}, "back_leg": {"angle": -18}, "body": {"dy": 6}},
        {"front_leg": {"angle": 10}, "back_leg": {"angle": -8, "dy": -12}, "body": {"dy": 16}},
        {"front_leg": {"angle": -4}, "back_leg": {"angle": 6, "dy": -24}, "body": {"dy": 0}},
        {"front_leg": {"angle": -16}, "back_leg": {"angle": 16}, "body": {"dy": -12}},
        {"front_leg": {"angle": -20}, "back_leg": {"angle": 20}, "body": {"dy": 6}},
        {"front_leg": {"angle": -6, "dy": -24}, "back_leg": {"angle": 6}, "body": {"dy": 0}},
    ]},
    "crouch": {"fps": 12, "loop": False, "frames": [
        {"body": {"dy": 70, "angle": 6}, "front_leg": {"angle": 38, "dy": 30}, "back_leg": {"angle": -34, "dy": 30}},
        {"body": {"dy": 130, "angle": 8}, "front_leg": {"angle": 62, "dy": 60}, "back_leg": {"angle": -58, "dy": 60}},
    ]},
    "jump_up": {"fps": 12, "loop": False, "frames": [
        {"body": {"dy": 40}, "front_leg": {"angle": 30, "dy": 20}, "back_leg": {"angle": -30, "dy": 20}},
        {"body": {"dy": -10}, "front_leg": {"angle": 70, "dy": -60}, "back_leg": {"angle": 50, "dy": -50}},
        {"body": {"dy": -10, "angle": -6}, "front_leg": {"angle": 80, "dy": -80}, "back_leg": {"angle": 60, "dy": -70}},
    ]},
    "stand_hp": {"fps": 15, "loop": False, "frames": [
        {**stance(24), "body": {"dy": 48, "angle": -4}, "draw": [arm((330, 330), dy=48)]},
        {**stance(16), "body": {"dy": 40, "angle": 4}, "hide": ["hilt"], "draw": [arm((520, 300), 70, 40)]},
        {**stance(8), "body": {"dy": 32, "angle": 10}, "hide": ["hilt"], "draw": [arm((760, 520), 0, 32)]},
        {**stance(12), "body": {"dy": 36, "angle": 8}, "hide": ["hilt"], "draw": [arm((640, 640), -40, 36)]},
        {**stance(4), "body": {"dy": 28}, "draw": [arm((360, 360), dy=28)]},
    ]},
}

# P2's alternate colours (Street Fighter style): the rust poncho goes slate blue, the orange trim and
# neckerchief go teal, the straw kasa goes dark. Pairs of (P1 colour as drawn, P2 colour).
P2_SWAPS = [
    ((176, 128, 84), (92, 112, 148)),
    ((140, 98, 64), (64, 80, 112)),
    ((226, 128, 52), (52, 168, 160)),
    ((222, 196, 150), (150, 140, 120)),
]
