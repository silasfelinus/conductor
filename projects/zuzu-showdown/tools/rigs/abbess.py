"""The Abbess's rig (zuzu-showdown t-011).

Parts are cut from the t-011 parts sheet's fighting stance (ArtImage 243448: a wide stance facing
right, the ritual dagger raised in her right paw, the rosary hanging from her left). Scale comes from
her standing reference (242521), so the stance keeps her true 96 px height. Coordinates are the source
image's pixels (832 x 1216); about 10 make one game pixel.

Her habit hides her legs to the shins, so the legs are only what shows below the hem (black stockings,
otter feet): kicks swing them out from under it. The rosary arm stays part of the habit; the dagger arm
moves on its own, and does the slashes, the thrown Benediction and the rosary jab (LP, the pommel
forward). Her tentacles and portals are drawn by the game (render.ts drawSummons), not here.

Moves are timed with `timed`: at 20 fps each drawn frame covers three sim frames, so a move's active
frames always show its strike pose (sprites.ts pickSprite: index = (frame - 1) * fps / 60).
"""

from __future__ import annotations


HEIGHT = 96
PALETTE_COLOURS = 18
REFERENCE = {"art": 242521}  # scale only
STANCE = 243448

NECK = (450, 372)
SHOULDER = (525, 482)
HIP_BACK = (230, 900)
HIP_FRONT = (560, 880)
TAIL_ROOT = (195, 905)
# The fighter's spot on the ground in the source art: midway between her feet.
ANCHOR = (370, 1080)

PARTS = {
    "tail": {"art": STANCE, "z": 0, "pivot": TAIL_ROOT, "follows": ["body"],
             "polygon": [(28, 826), (100, 846), (205, 880), (212, 952), (150, 944), (70, 908), (36, 872)]},
    "back_leg": {"art": STANCE, "z": 1, "pivot": HIP_BACK, "follows": [],
                 "polygon": [(140, 930), (268, 920), (250, 990), (190, 1040), (170, 1090), (50, 1092), (64, 1040),
                             (104, 990)]},
    "front_leg": {"art": STANCE, "z": 2, "pivot": HIP_FRONT, "follows": [],
                  "polygon": [(500, 900), (648, 870), (646, 990), (700, 1040), (706, 1064), (534, 1068), (528, 1000),
                              (512, 950)]},
    "torso": {"art": STANCE, "z": 3, "pivot": HIP_FRONT, "follows": ["body"],
              "polygon": [(148, 478), (212, 398), (330, 392), (452, 376), (500, 410), (536, 470), (540, 600),
                          (560, 640), (604, 780), (632, 832), (604, 884), (520, 912), (500, 964), (300, 974),
                          (196, 944), (168, 900), (160, 842), (198, 800), (238, 700), (250, 600), (168, 560)]},
    "head": {"art": STANCE, "z": 4, "pivot": NECK, "follows": ["body"],
             "polygon": [(210, 394), (248, 320), (298, 230), (338, 160), (400, 126), (470, 122), (526, 148),
                         (562, 196), (622, 246), (652, 298), (602, 348), (540, 336), (490, 348), (456, 374),
                         (400, 382), (330, 396), (262, 408)]},
    "dagger_arm": {"art": STANCE, "z": 5, "pivot": SHOULDER, "follows": ["body"],
                   "polygon": [(498, 440), (546, 478), (600, 504), (648, 500), (658, 452), (700, 444), (786, 228),
                               (810, 234), (746, 488), (734, 512), (730, 560), (702, 582), (666, 600), (560, 606),
                               (530, 592), (504, 540)]},
}

MEASURING = False  # set by rig.py while it measures reach


def merged(base: dict, more: dict) -> dict:
    out = {key: dict(value) if isinstance(value, dict) else value for key, value in base.items()}
    for key, value in more.items():
        out[key] = {**out.get(key, {}), **value} if isinstance(value, dict) else value
    return out


def stance(dy=0, tilt=0, arm=0, **more):
    """The fighting stance is the source art itself: the body dropped `dy`, the head tilted, the dagger
    arm turned, plus `more` per part."""
    return merged({"body": {"dy": dy}, "head": {"angle": tilt}, "dagger_arm": {"angle": arm}}, more)


CROUCH_DY = 150


def crouched(**more):
    """Down under the habit: the body drops onto legs squashed about the hips, feet planted."""
    return merged({"body": {"dy": CROUCH_DY, "angle": 4}, "front_leg": {"sy": -0.45, "sx": 0.1, "dy": CROUCH_DY},
                   "back_leg": {"sy": -0.45, "sx": 0.1, "dy": CROUCH_DY}, "dagger_arm": {"angle": -10}}, more)


def tucked(**more):
    """The top of the jump: feet drawn up under the habit, the habit and tail flying."""
    return merged({"body": {"angle": -6}, "front_leg": {"sy": -0.55, "angle": 20, "dy": -40},
                   "back_leg": {"sy": -0.55, "angle": -10, "dy": -40}, "tail": {"angle": -14},
                   "dagger_arm": {"angle": 20}}, more)


def fall(angle, pivot=(120, 1080)):
    """The whole figure toppling about a foot (positive: over backwards about the back foot)."""
    return {"whole": {"angle": angle, "pivot": pivot}}


def timed(startup, active, recovery, windup, strike, recover, settle=None, fps=20):
    """Frames for a move at `fps`: each drawn frame covers 60/fps sim frames, and any that overlaps the
    active frames [startup, startup + active) shows `strike` (or, given a list, its poses in turn, the
    last held); earlier ones `windup`, later ones `recover` then (for the last) `settle`."""
    step = 60 // fps
    total = startup + active - 1 + recovery
    strikes = strike if isinstance(strike, list) else [strike]
    frames = []
    first_active, last_active = startup, startup + active - 1
    i = 0
    struck = 0
    while i * step + 1 <= total:
        lo, hi = i * step + 1, i * step + step
        if hi >= first_active and lo <= last_active:
            frames.append(strikes[min(struck, len(strikes) - 1)])
            struck += 1
        elif hi < first_active:
            frames.append(windup)
        else:
            frames.append(recover)
        i += 1
    if settle is not None and frames and frames[-1] is recover:
        frames[-1] = settle
    return frames


# Arm angles (degrees, counter-clockwise; the stance holds the blade up and forward at 0).
FORWARD = -42    # the blade level, pointing at the opponent
OVERHEAD = 50    # raised high behind her head
DOWN = -100      # swung down and through


def slash(stage):
    return {"dagger_arm": {"angle": stage}}


STRIKES = {
    # Standing LP: the rosary jab, a short punch with the fist leading and the blade tipped back.
    "stand_lp": timed(4, 2, 6, stance(6, arm=20), stance(4, arm=40, dagger_arm={"dx": 60, "dy": 30}),
                      stance(4, arm=-14), stance(0)),
    # Standing HP: the dagger slash, from high to level across her chest.
    "stand_hp": timed(8, 3, 16, stance(8, arm=30), stance(6, arm=FORWARD, body={"angle": 4}, dagger_arm={"dx": 20}),
                      stance(8, arm=-70), stance(2)),
    # Standing LK: a quick kick from under the hem.
    "stand_lk": timed(5, 3, 8, stance(4, front_leg={"angle": 20}),
                      stance(2, body={"angle": -6}, front_leg={"angle": 60, "dy": -30, "dx": 30}),
                      stance(4, front_leg={"angle": 24}), stance(0)),
    # Standing HK: a high swinging kick, the habit hitched up.
    "stand_hk": timed(10, 4, 18, stance(8, front_leg={"angle": 24}),
                      stance(-6, body={"angle": -12}, front_leg={"angle": 92, "dy": -110, "dx": 70, "sy": 0.25},
                             arm=20),
                      stance(4, front_leg={"angle": 40, "dy": -20}), stance(0)),
    "crouch_lp": timed(4, 2, 6, crouched(dagger_arm={"angle": 20}),
                       crouched(dagger_arm={"angle": 40, "dx": 60, "dy": 30}), crouched(dagger_arm={"angle": 10})),
    # Crouching LK: a toe poke along the floor.
    "crouch_lk": timed(5, 3, 8, crouched(front_leg={"sy": -0.45, "sx": 0.1, "dy": CROUCH_DY, "angle": 30}),
                       crouched(front_leg={"sy": 0.0, "sx": 0, "dy": CROUCH_DY, "angle": 70, "dx": 40}),
                       crouched(front_leg={"sy": -0.45, "sx": 0.1, "dy": CROUCH_DY, "angle": 30})),
    # Crouching HP: the anti-air, the blade thrust straight up.
    "crouch_hp": timed(7, 4, 16, crouched(dagger_arm={"angle": 10}), [crouched(dagger_arm={"angle": 40, "dy": -80, "dx": -10}),
                        crouched(dagger_arm={"angle": 68, "dy": -170, "dx": -40})],
                       crouched(dagger_arm={"angle": 10})),
    # Crouching HK: the sweep, low along the floor.
    "crouch_hk": timed(9, 4, 20, crouched(),
                       crouched(body={"dy": 210, "angle": 8}, back_leg={"sy": -0.6, "sx": 0.12, "dy": 210},
                                front_leg={"sy": 0.15, "sx": 0, "dy": 210, "dx": 90, "angle": 82}),
                       crouched(front_leg={"sy": -0.3, "dy": CROUCH_DY, "angle": 40})),
    "jump_lp": timed(4, 6, 4, tucked(), tucked(dagger_arm={"angle": -96, "dx": -40, "dy": 150}), tucked()),
    # Jumping HP: a downward stab.
    "jump_hp": timed(7, 5, 6, tucked(dagger_arm={"angle": 40}), tucked(dagger_arm={"angle": -100, "dy": 190, "dx": 60}),
                     tucked(dagger_arm={"angle": -40})),
    "jump_lk": timed(4, 8, 4, tucked(), tucked(front_leg={"sy": -0.05, "angle": 14, "dy": -10}), tucked()),
    "jump_hk": timed(7, 5, 6, tucked(body={"angle": -10}),
                     tucked(body={"angle": -12}, front_leg={"sy": 0.15, "angle": 54, "dx": 60, "dy": -20},
                            back_leg={"sy": -0.5, "angle": -20}),
                     tucked()),
}

ANIMATIONS = {
    # Idle: she breathes, the blade bobbing a little, the tail stirring.
    "idle": {"fps": 6, "loop": True, "frames": [stance(0), stance(-6, 1, 2, tail={"angle": 3}),
                                                stance(-8, 2, 3, tail={"angle": 5}), stance(-4, 1, 1, tail={"angle": 2})]},
    # Walking: a slow glide, the habit swaying, the feet shuffling under the hem.
    "walk_forward": {"fps": 8, "loop": True, "frames": [
        stance(4, front_leg={"angle": 6}, back_leg={"angle": -4}, tail={"angle": 4}),
        stance(0, front_leg={"angle": 2}, back_leg={"angle": 0, "dy": -10}, tail={"angle": 0}),
        stance(4, front_leg={"angle": -4}, back_leg={"angle": 4}, tail={"angle": -3}),
        stance(0, front_leg={"angle": -2, "dy": -10}, back_leg={"angle": 2}, tail={"angle": 0}),
    ]},
    "walk_back": {"fps": 7, "loop": True, "frames": [
        stance(2, front_leg={"angle": -4}, back_leg={"angle": 6}),
        stance(0, front_leg={"angle": 0, "dy": -10}, back_leg={"angle": 2}),
        stance(2, front_leg={"angle": 4}, back_leg={"angle": -4}),
        stance(0, front_leg={"angle": 2}, back_leg={"angle": 0, "dy": -10}),
    ]},
    "crouch": {"fps": 12, "loop": False, "frames": [
        merged(crouched(), {"body": {"dy": 75}, "front_leg": {"sy": -0.22, "dy": 75}, "back_leg": {"sy": -0.22, "dy": 75}}),
        crouched(),
    ]},
    "jump_up": {"fps": 12, "loop": False, "frames": [
        merged(crouched(), {"body": {"dy": 60}, "front_leg": {"sy": -0.18, "dy": 60}, "back_leg": {"sy": -0.18, "dy": 60}}),
        tucked(body={"angle": -3}),
        tucked(),
    ]},
    "land": {"fps": 20, "loop": False, "frames": [
        merged(crouched(), {"body": {"dy": 75}, "front_leg": {"sy": -0.22, "dy": 75}, "back_leg": {"sy": -0.22, "dy": 75}}),
    ]},
    # Blocks: the blade brought across her face (high), or down into the crouch (low).
    "block_high": {"fps": 12, "loop": False, "frames": [stance(8, -4, 40, body={"angle": -4}),
                                                        stance(10, -5, 46, body={"angle": -5})]},
    "block_low": {"fps": 12, "loop": False, "frames": [crouched(dagger_arm={"angle": -60})]},
    "hit_high": {"fps": 14, "loop": False, "frames": [
        stance(8, -16, 30, body={"dx": -30, "angle": -12}, head={"dx": -30}),
        stance(6, -10, 20, body={"dx": -18, "angle": -8}, head={"dx": -18}),
        stance(2, -4, 6, body={"dx": -6, "angle": -3}, head={"dx": -6}),
    ]},
    "hit_low": {"fps": 14, "loop": False, "frames": [
        stance(50, 10, -30, body={"angle": 16}, head={"dy": 16, "dx": 24}),
        stance(34, 6, -18, body={"angle": 10}, head={"dy": 10, "dx": 14}),
        stance(12, 2, -6, body={"angle": 4}),
    ]},
    "knockdown": {"fps": 12, "loop": False, "frames": [
        {**fall(20), "body": {"angle": -6}, "dagger_arm": {"angle": 30}},
        {**fall(48), "dagger_arm": {"angle": 40}},
        {**fall(76), "dagger_arm": {"angle": 30}},
        {**fall(90), "dagger_arm": {"angle": 20}},
    ]},
    # KO (fighters.yaml): she collapses forward onto her face, the dagger skittering away.
    "ko": {"fps": 8, "loop": False, "frames": [
        {**crouched(dagger_arm={"angle": -60}), **fall(-30, (640, 1066))},
        {**crouched(dagger_arm={"angle": -80}), **fall(-64, (640, 1066))},
        {**crouched(), **fall(-88, (640, 1066)), "hide": ["dagger_arm"]},
    ]},
    "wakeup": {"fps": 12, "loop": False, "frames": [
        {**fall(70), "dagger_arm": {"angle": 20}},
        {**fall(40), "dagger_arm": {"angle": -20}},
        crouched(),
        stance(10),
    ]},
    "dodge_forward": {"fps": 13, "loop": False, "frames": [
        crouched(),
        {**crouched(), "whole": {"angle": -90, "pivot": (380, 860), "dy": -60}},
        {**crouched(), "whole": {"angle": -180, "pivot": (380, 860), "dy": -110}},
        {**crouched(), "whole": {"angle": -270, "pivot": (380, 860), "dy": -60}},
        crouched(),
    ]},
    "dodge_back": {"fps": 12, "loop": False, "frames": [
        stance(8, -4, 20, body={"dx": -20, "angle": -6}),
        stance(10, -8, 34, body={"dx": -60, "angle": -12}, back_leg={"angle": -8}),
        stance(10, -8, 34, body={"dx": -60, "angle": -12}, back_leg={"angle": -8}),
        stance(6, -2, 10, body={"dx": -20, "angle": -4}),
    ]},
    # Throws: the free hand takes the collar (5 frames), then she pitches them past her (30 frames).
    "throw": {"fps": 15, "loop": False, "frames": [stance(8, arm=-30, body={"angle": 6}),
                                                   stance(8, arm=-40, body={"angle": 8}, dagger_arm={"dx": 20})]},
    "throw_hold": {"fps": 8, "loop": False, "frames": [
        stance(10, arm=-40, body={"angle": 6}, dagger_arm={"dx": 20}),
        stance(20, arm=60, body={"angle": -12}),
        stance(24, arm=-60, body={"angle": 10}),
        stance(10, arm=-10, body={"angle": 4}),
    ]},
    "throw_whiff": {"fps": 10, "loop": False, "frames": [
        stance(10, arm=-50, body={"angle": 10, "dx": 20}, dagger_arm={"dx": 30}),
        stance(14, 6, -40, body={"angle": 12, "dx": 24}),
        stance(6),
    ]},
    "thrown": {"fps": 15, "loop": False, "frames": [
        stance(-10, 14, 50, body={"dx": 20, "angle": 10}, front_leg={"angle": 10}, back_leg={"angle": -10}),
        stance(-30, 18, 60, body={"dx": 30, "angle": 16}, front_leg={"angle": 16, "dy": -20},
               back_leg={"angle": -14, "dy": -20}),
    ]},
    # Benediction: a dagger drawn back over her shoulder and flung (the game draws it in flight from
    # frame 14); she keeps her own blade, so the thrown one comes from her sleeve.
    "benediction": {"fps": 20, "loop": False, "frames": timed(
        14, 1, 22, stance(6, arm=OVERHEAD, body={"angle": -6}), stance(2, arm=-60, body={"angle": 8}, dagger_arm={"dx": 30}),
        stance(4, arm=-40, body={"angle": 4}), stance(0))},
    # Reaching Tentacle: she lowers her paw toward the floor where it will rise, smiling.
    "reaching_tentacle": {"fps": 20, "loop": False, "frames": timed(
        24, 10, 26, stance(6, 6, -60, body={"angle": 6}), stance(10, 8, -80, body={"angle": 8}),
        stance(6, 4, -50), stance(0))},
    # The Thin Place: she steps back into the portal, and out again.
    "the_thin_place": {"fps": 20, "loop": False, "frames": timed(
        12, 1, 24, stance(4, -6, 30, body={"angle": -8, "dx": -20}), stance(4, -6, 30, body={"angle": -8}),
        stance(2, arm=10), stance(0))},
    # Last Rites: she reaches and takes them (the altar slab and the book are the game's to draw).
    "last_rites": {"fps": 20, "loop": False, "frames": timed(
        6, 3, 30, stance(6, arm=-30, body={"angle": 8}), stance(4, arm=-40, body={"angle": 10}, dagger_arm={"dx": 30}),
        stance(14, arm=OVERHEAD, body={"angle": -4}), stance(4, arm=-60, body={"angle": 10}))},
    # Vespers: head bowed, blade lowered, while the bell tolls.
    "vespers": {"fps": 20, "loop": False, "frames": timed(
        18, 1, 26, stance(6, 10, -70), stance(8, 14, -80), stance(6, 10, -70), stance(0))},
    # The Choir: arms raised to the singing.
    "the_choir": {"fps": 20, "loop": False, "frames": timed(
        20, 8, 36, stance(-4, -6, OVERHEAD, body={"angle": -4}), stance(-6, -8, OVERHEAD + 10, body={"angle": -6}),
        stance(-2, -4, 30), stance(0))},
    # Open the Door: she steps aside for what comes through, still smiling.
    "open_the_door": {"fps": 20, "loop": False, "frames": timed(
        2, 2, 54, stance(4, 4, -60), stance(6, 6, -70, body={"dx": -30, "angle": -4}),
        stance(6, 6, -70, body={"dx": -30, "angle": -4}), stance(0))},
    # Taunt (fighters.yaml): holds out the stew, smiling.
    "taunt": {"fps": 6, "loop": False, "frames": [stance(0, 0, -30), stance(2, 4, -46, dagger_arm={"dx": 24}),
                                                  stance(2, 6, -46, dagger_arm={"dx": 24}), stance(0, 0, -20)]},
    # Victory: hands folded in prayer, eyes open and cold (the blade lowered).
    "victory": {"fps": 5, "loop": False, "frames": [stance(0, 0, -40), stance(4, 6, -80), stance(6, 8, -90)]},
    # Victory (the other): wipes the dagger on her sleeve and tucks it away, humming.
    "victory_button": {"fps": 5, "loop": False, "frames": [stance(0, 0, 20), stance(2, 4, -20, dagger_arm={"dx": -40}),
                                                          stance(4, 6, -60), stance(4, 8, -100)]},
    # Perfect: lights a single candle and blows it out (the head dips to it).
    "perfect": {"fps": 5, "loop": False, "frames": [stance(0, 0, -30), stance(6, 14, -50), stance(6, 16, -50),
                                                   stance(0, 4, -20)]},
    # Intro: walks in with her hands folded, smiling.
    "intro": {"fps": 4, "loop": False, "frames": [stance(-8, 4, -90), stance(-4, 4, -80), stance(0, 2, -50),
                                                 stance(0)]},
}

for _name, _frames in STRIKES.items():
    _strike = "dagger_arm" if _name.endswith(("_lp", "_hp")) else "front_leg"
    ANIMATIONS[_name] = {"fps": 20, "loop": False, "strike": [_strike], "frames": _frames}

# P2's alternate colours: the black habit stays black (value too low to recolour), so P2 turns her warm
# brown fur a cool grey-brown and the gold rosary silver.
P2_RULES = [
    {"hue": (18, 48), "sat_min": 0.25, "val_min": 0.25, "shift": 190, "sat": 0.35},
]
