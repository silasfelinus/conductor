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


BACK_FOOT = (120, 1168)
FRONT_FOOT = (700, 1168)


def fall(angle, pivot=BACK_FOOT):
    """The whole figure toppling about a foot: positive angles tip him over backwards (head to his
    rear) about the back foot; negative angles about the front foot pitch him forwards."""
    return {"whole": {"angle": angle, "pivot": pivot}}


def stance(dy=0, head=0, arm=0):
    """The fighting stance is the source art itself, so a stance frame is just small offsets."""
    return {"body": {"dy": dy}, "head": {"dy": head}, "lead_arm": {"angle": arm}}


CROUCH_DY = 131


def crouched(**more):
    """The crouch's held frame (legs squashed about the hips, body dropped onto them), plus `more`."""
    pose = {"body": {"dy": CROUCH_DY, "angle": 6}, "front_leg": {"sy": -0.35, "sx": 0.12, "dy": CROUCH_DY},
            "back_leg": {"sy": -0.35, "sx": 0.12, "dy": CROUCH_DY}, "lead_arm": {"angle": -16}}
    for key, value in more.items():
        pose[key] = {**pose.get(key, {}), **value} if isinstance(value, dict) else value
    return pose


def tucked(**more):
    """The top of the jump: legs tucked up under the poncho, plus `more`."""
    pose = {"body": {"angle": -8}, "front_leg": {"sy": -0.5, "angle": 24}, "back_leg": {"sy": -0.48, "angle": -2},
            "lead_arm": {"angle": 30}}
    for key, value in more.items():
        pose[key] = {**pose.get(key, {}), **value} if isinstance(value, dict) else value
    return pose


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
    "walk_back": {"fps": 9, "loop": True, "frames": [
        {"front_leg": {"angle": -4}, "back_leg": {"angle": 6}, "body": {"dy": 4}},
        {"front_leg": {"angle": -2}, "back_leg": {"angle": 2, "dy": -12}, "body": {"dy": 10}},
        {"front_leg": {"angle": 4}, "back_leg": {"angle": -4}, "body": {"dy": 2}},
        {"front_leg": {"angle": 6, "dy": -12}, "back_leg": {"angle": -6}, "body": {"dy": 6}},
    ]},
    # Blocks: the lead forearm comes up across his face (high), or he drops into the crouch (low).
    "block_high": {"fps": 12, "loop": False, "frames": [
        {**stance(8), "body": {"dy": 8, "angle": -4}, "lead_arm": {"angle": 64}},
        {**stance(12), "body": {"dy": 12, "angle": -5}, "lead_arm": {"angle": 70}},
    ]},
    "block_low": {"fps": 12, "loop": False, "frames": [
        {"body": {"dy": 131, "angle": 6}, "front_leg": {"sy": -0.35, "sx": 0.12, "dy": 131},
         "back_leg": {"sy": -0.35, "sx": 0.12, "dy": 131}, "lead_arm": {"angle": -34}},
    ]},
    "hit_high": {"fps": 14, "loop": False, "frames": [
        {"body": {"dy": 8, "dx": -30, "angle": -14}, "head": {"angle": -18, "dx": -40}, "lead_arm": {"angle": 30}},
        {"body": {"dy": 6, "dx": -20, "angle": -9}, "head": {"angle": -11, "dx": -24}, "lead_arm": {"angle": 18}},
        {"body": {"dy": 2, "dx": -8, "angle": -3}, "head": {"angle": -4, "dx": -8}},
    ]},
    "hit_low": {"fps": 14, "loop": False, "frames": [
        {"body": {"dy": 50, "angle": 20}, "head": {"dy": 20, "dx": 30, "angle": 12}, "lead_arm": {"angle": -30}},
        {"body": {"dy": 34, "angle": 13}, "head": {"dy": 12, "dx": 18, "angle": 6}, "lead_arm": {"angle": -18}},
        {"body": {"dy": 12, "angle": 4}},
    ]},
    "knockdown": {"fps": 12, "loop": False, "frames": [
        {**fall(20), "body": {"angle": -6}, "lead_arm": {"angle": 30}},
        {**fall(48), "lead_arm": {"angle": 40}},
        {**fall(76), "lead_arm": {"angle": 30}},
        {**fall(90), "lead_arm": {"angle": 20}},
    ]},
    # KO (fighters.yaml): drops to one knee, then pitches forward.
    "ko": {"fps": 8, "loop": False, "frames": [
        {"body": {"dy": 131, "angle": 10}, "front_leg": {"sy": -0.35, "sx": 0.12, "dy": 131},
         "back_leg": {"sy": -0.5, "dy": 131, "angle": -30}, "head": {"dy": 10, "angle": 10}, "lead_arm": {"angle": -50}},
        {**fall(-40, FRONT_FOOT), "body": {"dy": 131, "angle": 10}, "front_leg": {"sy": -0.35, "dy": 131},
         "back_leg": {"sy": -0.5, "dy": 131, "angle": -30}, "lead_arm": {"angle": -60}},
        {**fall(-86, FRONT_FOOT), "body": {"dy": 131, "angle": 10}, "front_leg": {"sy": -0.35, "dy": 131},
         "back_leg": {"sy": -0.5, "dy": 131, "angle": -30}, "lead_arm": {"angle": -70}},
    ]},
    # Taunt (fighters.yaml): slowly sets his kasa straight with one finger. Doesn't look at you.
    "taunt": {"fps": 6, "loop": False, "frames": [
        {**stance(0, 0, 40)},
        {**stance(-4, -2, 84), "head": {"angle": -4}},
        {**stance(-4, -2, 88), "head": {"angle": 0}},
        {**stance(0, 0, 40)},
    ]},
    # Victory: the kasa off to the fallen, a bow.
    "victory": {"fps": 6, "loop": False, "frames": [
        {**stance(0, 0, 60)},
        {**stance(10, 12, 84), "head": {"angle": 12, "dy": 12}},
        {**stance(16, 18, 90), "head": {"angle": 16, "dy": 18}},
    ]},
    # Iai Flash: the quick-draw dash cut, a deep lunge with the blade straight out.
    "iai_flash": {"fps": 18, "loop": False, "frames": [
        {**stance(20), "hide": ["lead_arm"], "draw": [arm((600, 330), dy=20)]},
        {**stance(10), "body": {"dy": 10, "angle": 10}, "front_leg": {"angle": 14}, "hide": ["lead_arm", "hilt"],
         "draw": [arm((880, 500), -2, 10)]},
        {**stance(10), "body": {"dy": 10, "angle": 12}, "front_leg": {"angle": 16}, "hide": ["lead_arm", "hilt"],
         "draw": [arm((900, 520), -6, 10)]},
        {**stance(6), "hide": ["lead_arm"], "draw": [arm((610, 340), dy=6)]},
    ]},
    # Falling Leaf: the rising cut, legs tucked, blade sweeping up overhead.
    "falling_leaf": {"fps": 16, "loop": False, "frames": [
        {**stance(30), "hide": ["lead_arm"], "draw": [arm((620, 420), dy=30)]},
        {"body": {"angle": -6}, "front_leg": {"sy": -0.3, "angle": 14}, "back_leg": {"sy": -0.3},
         "hide": ["lead_arm", "hilt"], "draw": [arm((720, 300), 60)]},
        {"body": {"angle": -10}, "front_leg": {"sy": -0.45, "angle": 22}, "back_leg": {"sy": -0.42},
         "hide": ["lead_arm", "hilt"], "draw": [arm((680, 160), 96)]},
    ]},
    # Descending Cut: in the air, the blade swung down and forward.
    "descending_cut": {"fps": 16, "loop": False, "frames": [
        {"body": {"angle": -6}, "front_leg": {"sy": -0.4, "angle": 20}, "back_leg": {"sy": -0.36},
         "hide": ["lead_arm", "hilt"], "draw": [arm((700, 260), 70)]},
        {"body": {"angle": 8}, "front_leg": {"sy": -0.4, "angle": 24}, "back_leg": {"sy": -0.36},
         "hide": ["lead_arm", "hilt"], "draw": [arm((820, 620), -40)]},
    ]},
    # Poncho Veil: the parry stance, crouched behind the poncho, the lead arm tucked away.
    "poncho_veil": {"fps": 10, "loop": False, "frames": [
        {"body": {"dy": 50, "angle": 6}, "front_leg": {"sy": -0.13, "dy": 50}, "back_leg": {"sy": -0.13, "dy": 50},
         "head": {"dy": 20, "angle": 8}, "hide": ["lead_arm"]},
    ]},
    # Kasa Toss: a sidearm throw (the game draws the kasa itself in flight).
    "kasa_toss": {"fps": 14, "loop": False, "frames": [
        {**stance(10), "lead_arm": {"angle": 70}},
        {**stance(6), "body": {"dy": 6, "angle": 6}, "lead_arm": {"angle": 20}},
        {**stance(4), "body": {"dy": 4, "angle": 8}, "lead_arm": {"angle": -10}},
    ]},
    # The normals (frame counts from fighters/placeholders.ts and zuzu.ts: an animation spans the move's
    # startup + active + recovery at its fps, clamping on its last frame if the move runs longer).
    # Standing LP: a short jab with the lead fist, the blade left sheathed.
    "stand_lp": {"fps": 15, "loop": False, "frames": [
        {**stance(6), "body": {"dy": 6, "angle": 3}, "lead_arm": {"sx": 0.1, "angle": -4}},
        {**stance(4), "body": {"dy": 4, "angle": 6}, "lead_arm": {"sx": 0.35, "angle": -8}},
        {**stance(4), "body": {"dy": 4, "angle": 3}, "lead_arm": {"sx": 0.1, "angle": -2}},
    ]},
    # Standing LK: a snap kick off the front foot.
    "stand_lk": {"fps": 15, "loop": False, "frames": [
        {**stance(4), "body": {"dy": 4, "angle": -3}, "front_leg": {"angle": 22, "dy": -10}},
        {**stance(4), "body": {"dy": 4, "angle": -8}, "front_leg": {"angle": 58, "dy": -24}},
        {**stance(4), "body": {"dy": 4, "angle": -7}, "front_leg": {"angle": 52, "dy": -20}},
        {**stance(4), "body": {"dy": 4, "angle": -2}, "front_leg": {"angle": 16, "dy": -6}},
    ]},
    # Standing HK: a roundhouse, the chamber, the leg swinging up to his own head height, the return.
    "stand_hk": {"fps": 12, "loop": False, "frames": [
        {**stance(10), "body": {"dy": 10, "angle": 6}, "front_leg": {"angle": -10}},
        {**stance(0), "body": {"dy": 0, "angle": -10}, "front_leg": {"angle": 40, "dy": -30}},
        {**stance(0), "body": {"dy": -10, "angle": -16}, "front_leg": {"angle": 84, "dy": -50},
         "back_leg": {"angle": -6}, "lead_arm": {"angle": 30}},
        {**stance(0), "body": {"dy": -10, "angle": -16}, "front_leg": {"angle": 88, "dy": -50},
         "back_leg": {"angle": -6}, "lead_arm": {"angle": 34}},
        {**stance(4), "body": {"dy": 4, "angle": -8}, "front_leg": {"angle": 40, "dy": -20}},
        {**stance(8)},
    ]},
    "crouch_lp": {"fps": 15, "loop": False, "frames": [
        crouched(lead_arm={"angle": -18, "sx": 0.1}),
        crouched(lead_arm={"angle": -20, "sx": 0.35}),
        crouched(lead_arm={"angle": -18, "sx": 0.1}),
    ]},
    # Crouching LK: a low toe-poke at the shins.
    "crouch_lk": {"fps": 15, "loop": False, "frames": [
        crouched(front_leg={"sy": -0.35, "sx": 0.12, "dy": CROUCH_DY, "angle": 24}),
        crouched(front_leg={"sy": -0.35, "sx": 0.12, "dy": CROUCH_DY, "angle": 52}),
        crouched(front_leg={"sy": -0.35, "sx": 0.12, "dy": CROUCH_DY, "angle": 48}),
        crouched(front_leg={"sy": -0.35, "sx": 0.12, "dy": CROUCH_DY, "angle": 20}),
    ]},
    # Crouching HP: the anti-air, drawing from the crouch straight up overhead.
    "crouch_hp": {"fps": 13, "loop": False, "frames": [
        crouched(hide=["lead_arm"], draw=[arm((600, 330 + CROUCH_DY), dy=CROUCH_DY)]),
        crouched(hide=["lead_arm", "hilt"], draw=[arm((780, 560), 40, CROUCH_DY)]),
        crouched(hide=["lead_arm", "hilt"], draw=[arm((740, 420), 80, CROUCH_DY)]),
        crouched(hide=["lead_arm", "hilt"], draw=[arm((720, 400), 96, CROUCH_DY)]),
        crouched(hide=["lead_arm", "hilt"], draw=[arm((800, 600), 20, CROUCH_DY)]),
        crouched(hide=["lead_arm"], draw=[arm((610, 340 + CROUCH_DY), dy=CROUCH_DY)]),
    ]},
    # Crouching HK: the sweep, dropping to the floor and swinging the front leg out full length along it.
    "crouch_hk": {"fps": 12, "loop": False, "frames": [
        crouched(),
        crouched(body={"dy": 230, "angle": 12}, back_leg={"sy": -0.58, "sx": 0.15, "dy": 230},
                 front_leg={"sy": -0.15, "sx": 0, "dy": 230, "angle": 50}, lead_arm={"angle": -30}),
        crouched(body={"dy": 260, "angle": 14}, back_leg={"sy": -0.62, "sx": 0.15, "dy": 260},
                 front_leg={"sy": 0, "sx": 0, "dy": 260, "angle": 84}, lead_arm={"angle": -34}),
        crouched(body={"dy": 260, "angle": 14}, back_leg={"sy": -0.62, "sx": 0.15, "dy": 260},
                 front_leg={"sy": 0, "sx": 0, "dy": 260, "angle": 86}, lead_arm={"angle": -34}),
        crouched(body={"dy": 200, "angle": 10}, back_leg={"sy": -0.52, "sx": 0.15, "dy": 200},
                 front_leg={"sy": -0.2, "dy": 200, "angle": 44}, lead_arm={"angle": -24}),
        crouched(),
    ]},
    "jump_lp": {"fps": 15, "loop": False, "frames": [
        tucked(lead_arm={"angle": 0, "sx": 0.12}),
        tucked(lead_arm={"angle": -14, "sx": 0.35}),
        tucked(lead_arm={"angle": -6, "sx": 0.14}),
    ]},
    # Jumping HP: a downward slash in the air.
    "jump_hp": {"fps": 12, "loop": False, "frames": [
        tucked(hide=["lead_arm", "hilt"], draw=[arm((700, 260), 70)]),
        tucked(body={"angle": 4}, hide=["lead_arm", "hilt"], draw=[arm((860, 520), -10)]),
        tucked(body={"angle": 8}, hide=["lead_arm", "hilt"], draw=[arm((800, 640), -46)]),
        tucked(hide=["lead_arm"], draw=[arm((610, 340))]),
    ]},
    # Jumping LK: the flying kick, the front leg shot straight out and down.
    "jump_lk": {"fps": 12, "loop": False, "frames": [
        tucked(),
        tucked(body={"angle": 8}, front_leg={"sy": 0.05, "angle": 56}, back_leg={"sy": -0.5, "angle": -12}),
        tucked(body={"angle": 8}, front_leg={"sy": 0.05, "angle": 58}, back_leg={"sy": -0.5, "angle": -12}),
        tucked(body={"angle": 4}, front_leg={"sy": -0.2, "angle": 40}),
    ]},
    # Jumping HK: a bigger flying kick, leaning back behind a straight leg.
    "jump_hk": {"fps": 12, "loop": False, "frames": [
        tucked(body={"angle": -12}, front_leg={"sy": -0.5, "angle": 10}),
        tucked(body={"angle": -16}, front_leg={"sy": 0.12, "angle": 80}, back_leg={"sy": -0.5, "angle": -20},
               lead_arm={"angle": 50}),
        tucked(body={"angle": -16}, front_leg={"sy": 0.12, "angle": 84}, back_leg={"sy": -0.5, "angle": -20},
               lead_arm={"angle": 52}),
        tucked(body={"angle": -10}, front_leg={"sy": -0.3, "angle": 40}),
    ]},
    # Landing: the first frame of the crouch, absorbing the drop (the sim holds it 3 frames).
    "land": {"fps": 20, "loop": False, "frames": [
        {"body": {"dy": 66, "angle": 3}, "front_leg": {"sy": -0.18, "sx": 0.06, "dy": 66},
         "back_leg": {"sy": -0.18, "sx": 0.06, "dy": 66}, "lead_arm": {"angle": -8}},
    ]},
    # Dodges: a forward roll through the opponent (22 frames; the sim moves him), a lean-back sidestep (18).
    "dodge_forward": {"fps": 13, "loop": False, "frames": [
        crouched(),
        {**crouched(), "whole": {"angle": -90, "pivot": (420, 860), "dy": -60}},
        {**crouched(), "whole": {"angle": -180, "pivot": (420, 860), "dy": -110}},
        {**crouched(), "whole": {"angle": -270, "pivot": (420, 860), "dy": -60}},
        crouched(),
    ]},
    "dodge_back": {"fps": 12, "loop": False, "frames": [
        {**stance(8), "body": {"dy": 8, "dx": -20, "angle": -6}, "head": {"dx": -24}, "lead_arm": {"angle": 20}},
        {**stance(10), "body": {"dy": 10, "dx": -60, "angle": -12}, "head": {"dx": -70, "angle": -6},
         "back_leg": {"angle": -8}, "lead_arm": {"angle": 34}},
        {**stance(10), "body": {"dy": 10, "dx": -60, "angle": -12}, "head": {"dx": -70, "angle": -6},
         "back_leg": {"angle": -8}, "lead_arm": {"angle": 34}},
        {**stance(6), "body": {"dy": 6, "dx": -20, "angle": -4}, "head": {"dx": -24}},
    ]},
    # Wake-up (20 frames): up off his back, through the crouch, into the stance.
    "wakeup": {"fps": 12, "loop": False, "frames": [
        {**fall(70), "lead_arm": {"angle": 20}},
        {**fall(40), "lead_arm": {"angle": -20}},
        crouched(),
        stance(10),
    ]},
    # Throws: the lead hand grabs the collar (5 frames), then he flips them over his hip (30 frames);
    # a whiffed grab overreaches and stumbles (20 frames).
    "throw": {"fps": 15, "loop": False, "frames": [
        {**stance(10), "body": {"dy": 10, "angle": 8}, "lead_arm": {"sx": 0.2, "angle": 6}},
        {**stance(10), "body": {"dy": 10, "angle": 10}, "lead_arm": {"sx": 0.35, "angle": 10}},
    ]},
    "throw_hold": {"fps": 8, "loop": False, "frames": [
        {**stance(10), "body": {"dy": 10, "angle": 6}, "lead_arm": {"sx": 0.3, "angle": 14}},
        {**stance(20), "body": {"dy": 20, "angle": -14}, "lead_arm": {"angle": 76}, "front_leg": {"angle": -6}},
        {**stance(24), "body": {"dy": 24, "angle": 10}, "lead_arm": {"sx": 0.2, "angle": -30}},
        {**stance(10), "body": {"dy": 10, "angle": 4}},
    ]},
    "throw_whiff": {"fps": 10, "loop": False, "frames": [
        {**stance(10), "body": {"dy": 10, "angle": 12, "dx": 20}, "lead_arm": {"sx": 0.45, "angle": 4}},
        {**stance(14), "body": {"dy": 14, "angle": 14, "dx": 24}, "head": {"angle": 6}, "lead_arm": {"sx": 0.35}},
        stance(6),
    ]},
    # Thrown: caught by the collar before the toss lands him (then the knockdown plays).
    "thrown": {"fps": 15, "loop": False, "frames": [
        {"body": {"dy": -10, "dx": 20, "angle": 10}, "head": {"angle": 14, "dx": 30}, "lead_arm": {"angle": 50},
         "front_leg": {"angle": 10}, "back_leg": {"angle": -10}},
        {"body": {"dy": -30, "dx": 30, "angle": 16}, "head": {"angle": 18, "dx": 40}, "lead_arm": {"angle": 60},
         "front_leg": {"angle": 16, "dy": -20}, "back_leg": {"angle": -14, "dy": -20}},
    ]},
    # Thousand-Mile Step (Lv1, 42 frames): a hand to the hilt, the low dash straight through them with the
    # blade out (the sim carries him past, so he ends with his back to them), then the slow sheathe.
    "thousand_mile_step": {"fps": 10, "loop": False, "frames": [
        {**stance(20), "hide": ["lead_arm"], "draw": [arm((600, 330), dy=20)]},
        {**stance(30), "body": {"dy": 30, "angle": 14}, "front_leg": {"angle": 20}, "back_leg": {"angle": -14},
         "hide": ["lead_arm", "hilt"], "draw": [arm((900, 560), -8, 30)]},
        {**stance(30), "body": {"dy": 30, "angle": 14}, "front_leg": {"angle": 22}, "back_leg": {"angle": -16},
         "hide": ["lead_arm", "hilt"], "draw": [arm((920, 580), -10, 30)]},
        {**stance(24), "body": {"dy": 24, "angle": 10}, "front_leg": {"angle": 14}, "back_leg": {"angle": -10},
         "hide": ["lead_arm", "hilt"], "draw": [arm((900, 560), -10, 24)]},
        {**stance(12), "hide": ["lead_arm", "hilt"], "draw": [arm((720, 300), 72, 12)]},
        {**stance(6), "hide": ["lead_arm"], "draw": [arm((610, 340), dy=6)]},
        stance(0),
    ]},
    # Hat to the Dead (Lv3 Showdown, 55 frames): the cut happens in the black; when the lights come up he
    # is already sheathing, and lifts the kasa off his head to the fallen.
    "hat_to_the_dead": {"fps": 6, "loop": False, "frames": [
        {**stance(6), "hide": ["lead_arm"], "draw": [arm((610, 340), dy=6)]},
        {**stance(0, 0, 60)},
        {**stance(0, 0, 84), "head": {"angle": -4}},
        {**stance(10, 12, 84), "head": {"angle": 12, "dy": 12}},
        {**stance(16, 18, 90), "head": {"angle": 16, "dy": 18}},
    ]},
    # Intro (the 90-frame round intro, fighters.yaml): steps up out of the heat shimmer, thumb resting
    # on the scabbard mouth over his shoulder, and settles into the stance.
    "intro": {"fps": 4, "loop": False, "frames": [
        {**stance(-14, -4), "body": {"dy": -14, "angle": -3}, "hide": ["lead_arm"], "draw": [arm((600, 330), dy=-14)]},
        {**stance(-6, -2), "hide": ["lead_arm"], "draw": [arm((600, 330), dy=-6)]},
        {**stance(0), "hide": ["lead_arm"], "draw": [arm((600, 330))]},
        stance(0),
    ]},
    # Perfect (fighters.yaml): never drew. Brushes the dust off his poncho and is done.
    "perfect": {"fps": 6, "loop": False, "frames": [
        {**stance(0, 0, -40)},
        {**stance(4, 4, -64), "head": {"angle": 6, "dy": 4}},
        {**stance(4, 4, -40), "head": {"angle": 6, "dy": 4}},
        {**stance(4, 4, -66), "head": {"angle": 6, "dy": 4}},
        {**stance(0, -2, 10), "head": {"angle": -4}},
    ]},
}

# P2's alternate colours (Street Fighter style): the rust poncho and the orange trim turn slate blue.
# The trousers share the poncho's hue but are darker, so the value floor keeps them brown.
P2_RULES = [
    {"hue": (15, 40), "sat_min": 0.3, "val_min": 0.45, "shift": 190, "sat": 0.85},
]
