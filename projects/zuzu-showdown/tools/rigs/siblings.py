"""The Siblings' rig (zuzu-showdown t-011): the sister, who fights.

Parts are cut from the t-011 parts sheet's fighting stance (ArtImage 243456: a low, scrappy stance facing
right, both arms flung out clear of her dress, claws out, teeth bared), with scale from her standing
reference (242140), so she keeps her true 84 px. Coordinates are the source image's pixels (832 x 1216);
about 13 make one game pixel.

Her toddler brother is not in this rig: he is a separate puppet layer with no hurtbox (fighters.yaml
children_rules), drawn by the game beside her from his own poses. So her specials here are her side of
each move: turning to shield him, ducking under a strike, the snap and the scramble.

Moves are timed with `timed` (as in rigs/abbess.py): at 20 fps each drawn frame covers three sim frames,
so a move's active frames always show its strike pose.
"""

from __future__ import annotations

HEIGHT = 84
PALETTE_COLOURS = 18
REFERENCE = {"art": 242140}  # scale only
STANCE = 243456

NECK = (445, 362)
SHOULDER_NEAR = (500, 474)
SHOULDER_FAR = (390, 420)
HIP_BACK = (300, 880)
HIP_FRONT = (600, 800)
TAIL_ROOT = (275, 800)
# The fighter's spot on the ground in the source art: midway between her feet.
ANCHOR = (420, 1134)

PARTS = {
    "far_arm": {"art": STANCE, "z": 0, "pivot": SHOULDER_FAR, "follows": ["body"],
                "polygon": [(404, 398), (384, 452), (330, 482), (252, 502), (226, 500), (198, 472), (140, 456),
                            (84, 462), (66, 410), (94, 346), (152, 344), (202, 342), (212, 408), (240, 428),
                            (300, 418), (352, 394)]},
    "tail": {"art": STANCE, "z": 1, "pivot": TAIL_ROOT, "follows": ["body"],
             "polygon": [(36, 700), (132, 626), (142, 698), (240, 758), (284, 798), (262, 862), (180, 884),
                         (88, 862), (36, 800)]},
    "back_leg": {"art": STANCE, "z": 2, "pivot": HIP_BACK, "follows": [],
                 "polygon": [(236, 888), (334, 900), (302, 962), (222, 1040), (196, 1080), (204, 1118),
                             (182, 1136), (94, 1138), (98, 1098), (140, 1048), (180, 980), (218, 920)]},
    "front_leg": {"art": STANCE, "z": 3, "pivot": HIP_FRONT, "follows": [],
                  "polygon": [(556, 818), (652, 798), (668, 880), (662, 1000), (682, 1058), (762, 1078),
                              (776, 1104), (740, 1116), (618, 1112), (618, 1060), (608, 980), (588, 900)]},
    "torso": {"art": STANCE, "z": 4, "pivot": HIP_FRONT, "follows": ["body"],
              "polygon": [(350, 388), (402, 378), (460, 368), (502, 418), (512, 478), (502, 560), (502, 600),
                          (522, 680), (592, 750), (664, 800), (602, 832), (562, 882), (482, 922), (400, 952),
                          (298, 942), (248, 902), (258, 800), (278, 700), (318, 620), (348, 560), (344, 470)]},
    "head": {"art": STANCE, "z": 5, "pivot": NECK, "follows": ["body"],
             "polygon": [(264, 58), (302, 58), (352, 128), (420, 228), (472, 218), (532, 248), (552, 298),
                         (602, 350), (582, 372), (542, 392), (472, 372), (432, 382), (402, 372), (380, 332),
                         (330, 292), (290, 242), (268, 160)]},
    "near_arm": {"art": STANCE, "z": 6, "pivot": SHOULDER_NEAR, "follows": ["body"],
                 "polygon": [(488, 448), (520, 468), (560, 518), (610, 498), (658, 468), (668, 400), (700, 378),
                             (742, 376), (782, 408), (776, 470), (722, 492), (662, 522), (612, 562), (572, 582),
                             (540, 582), (510, 542), (488, 500)]},
}

MEASURING = False  # set by rig.py while it measures reach


def merged(base: dict, more: dict) -> dict:
    out = {key: dict(value) if isinstance(value, dict) else value for key, value in base.items()}
    for key, value in more.items():
        out[key] = {**out.get(key, {}), **value} if isinstance(value, dict) else value
    return out


def stance(dy=0, tilt=0, arm=0, **more):
    """The fighting stance is the source art itself: the body dropped `dy`, the head tilted, the near
    arm turned, plus `more` per part."""
    return merged({"body": {"dy": dy}, "head": {"angle": tilt}, "near_arm": {"angle": arm}}, more)


CROUCH_DY = 170


def crouched(**more):
    """Low to the ground: the body drops onto legs squashed about the hips, feet planted."""
    return merged({"body": {"dy": CROUCH_DY, "angle": 6}, "front_leg": {"sy": -0.4, "sx": 0.1, "dy": CROUCH_DY},
                   "back_leg": {"sy": -0.4, "sx": 0.1, "dy": CROUCH_DY}, "near_arm": {"angle": -14},
                   "far_arm": {"angle": -10}, "head": {"angle": 4}}, more)


def tucked(**more):
    """The top of the leap: legs tucked up, ears and tail streaming."""
    return merged({"body": {"angle": -8}, "front_leg": {"sy": -0.45, "angle": 30, "dy": -60},
                   "back_leg": {"sy": -0.45, "angle": -20, "dy": -60}, "tail": {"angle": -16},
                   "head": {"angle": -8}, "near_arm": {"angle": 16}}, more)


def fall(angle, pivot=(140, 1134)):
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


STRIKES = {
    # Standing LP: a quick claw swipe with the near paw.
    "stand_lp": ("near_arm", timed(4, 2, 6, stance(4, arm=10), stance(2, arm=-12, near_arm={"dx": 16, "dy": -40}),
                                   stance(2, arm=-6), stance(0))),
    # Standing HP: the two-handed shove, both arms driven forward.
    "stand_hp": ("near_arm", timed(8, 3, 16, stance(10, arm=20, far_arm={"angle": 30}),
                                   stance(4, arm=-20, body={"angle": 8, "dx": 20}, near_arm={"dx": 90, "sx": 0.2},
                                          far_arm={"angle": -150, "dx": 60}),
                                   stance(6, arm=-10, far_arm={"angle": -40}), stance(0))),
    # Standing LK: a fast scrappy kick.
    "stand_lk": ("front_leg", timed(5, 3, 8, stance(4, front_leg={"angle": 16}),
                                    stance(2, body={"angle": -6}, front_leg={"angle": 52, "dy": -20, "dx": 20}),
                                    stance(4, front_leg={"angle": 20}), stance(0))),
    "stand_hk": ("front_leg", timed(10, 4, 18, stance(8, front_leg={"angle": 24}),
                                    stance(-4, body={"angle": -12, "dx": -10},
                                           front_leg={"angle": 84, "dy": -60, "dx": 40, "sy": 0.1}, arm=24),
                                    stance(4, front_leg={"angle": 36, "dy": -10}), stance(0))),
    "crouch_lp": ("near_arm", timed(4, 2, 6, crouched(near_arm={"angle": -10}),
                                    crouched(near_arm={"angle": -30, "dx": 16}), crouched(near_arm={"angle": -16}))),
    "crouch_lk": ("front_leg", timed(5, 3, 8, crouched(front_leg={"sy": -0.4, "sx": 0.1, "dy": CROUCH_DY, "angle": 26}),
                                     crouched(front_leg={"sy": -0.05, "sx": 0, "dy": CROUCH_DY + 70, "angle": 82, "dx": 30}),
                                     crouched(front_leg={"sy": -0.4, "sx": 0.1, "dy": CROUCH_DY, "angle": 26}))),
    # Crouching HP: the anti-air, both paws clawing straight up.
    "crouch_hp": ("near_arm", timed(7, 4, 16, crouched(near_arm={"angle": 20}),
                                    [crouched(near_arm={"angle": 50, "dy": -60, "dx": 20}),
                                     crouched(near_arm={"angle": 76, "dy": -170, "dx": 20})],
                                    crouched(near_arm={"angle": 20}))),
    # Crouching HK: a low sweeping scratch along the floor.
    "crouch_hk": ("front_leg", timed(9, 4, 20, crouched(),
                                     crouched(body={"dy": 230, "angle": 10}, back_leg={"sy": -0.55, "sx": 0.12, "dy": 230},
                                              front_leg={"sy": 0.15, "sx": 0, "dy": 280, "dx": 90, "angle": 86}),
                                     crouched(front_leg={"sy": -0.3, "dy": CROUCH_DY, "angle": 40}))),
    "jump_lp": ("near_arm", timed(4, 6, 4, tucked(), tucked(near_arm={"angle": -70, "dy": 160}), tucked())),
    "jump_hp": ("near_arm", timed(7, 5, 6, tucked(near_arm={"angle": 40}),
                                  tucked(near_arm={"angle": -55, "dy": 170, "dx": 40, "sx": 0.2}, far_arm={"angle": -60}),
                                  tucked(near_arm={"angle": -20}))),
    "jump_lk": ("front_leg", timed(4, 8, 4, tucked(), tucked(front_leg={"sy": -0.05, "angle": 16, "dy": -20}), tucked())),
    "jump_hk": ("front_leg", timed(7, 5, 6, tucked(body={"angle": -10}),
                                   tucked(body={"angle": -12}, front_leg={"sy": 0.1, "angle": 50, "dx": 40, "dy": 30},
                                          back_leg={"sy": -0.5, "angle": -24}),
                                   tucked())),
    # Bared Teeth: the leaping snap upward, jaws first (the anti-air special).
    "bared_teeth": ("head", timed(5, 8, 24, crouched(head={"angle": -10}),
                                  [stance(-60, -24, 40, body={"angle": -10, "dx": 160}, head={"dy": -60, "dx": 60},
                                          front_leg={"angle": 20, "dy": -40}, back_leg={"angle": -14, "dy": -40}),
                                   stance(-140, -30, 50, body={"angle": -14, "dx": 160}, head={"dy": -110, "dx": 60},
                                          front_leg={"angle": 24, "dy": -110}, back_leg={"angle": -18, "dy": -110})],
                                  stance(-40, -10, 20, front_leg={"dy": -30}, back_leg={"dy": -30}), stance(0))),
    # Scramble: a low skid, then the scrappy two-hit claw at the end of it.
    "scramble": ("near_arm", timed(8, 12, 18, crouched(),
                                   crouched(body={"dy": 240, "angle": 14}, near_arm={"angle": -40, "dx": 150, "dy": 240, "sx": 0.15},
                                            front_leg={"sy": -0.1, "dy": 240, "angle": 70},
                                            back_leg={"sy": -0.55, "dy": 240}),
                                   crouched())),
}

ANIMATIONS = {
    # Idle: tense and watchful, ears twitching, the tail low.
    "idle": {"fps": 7, "loop": True, "frames": [stance(0), stance(-6, 2, 3, tail={"angle": 3}),
                                                stance(-10, 3, 4, tail={"angle": 5}, far_arm={"angle": 2}),
                                                stance(-4, 1, 2, tail={"angle": 2})]},
    # Walking: quick light steps.
    "walk_forward": {"fps": 12, "loop": True, "frames": [
        stance(4, front_leg={"angle": 10}, back_leg={"angle": -8}, tail={"angle": 4}),
        stance(0, front_leg={"angle": 4}, back_leg={"angle": -2, "dy": -16}, tail={"angle": 0}),
        stance(4, front_leg={"angle": -6}, back_leg={"angle": 6}, tail={"angle": -4}),
        stance(0, front_leg={"angle": -2, "dy": -16}, back_leg={"angle": 2}, tail={"angle": 0}),
    ]},
    "walk_back": {"fps": 10, "loop": True, "frames": [
        stance(2, front_leg={"angle": -6}, back_leg={"angle": 8}),
        stance(0, front_leg={"angle": 0, "dy": -14}, back_leg={"angle": 2}),
        stance(2, front_leg={"angle": 6}, back_leg={"angle": -6}),
        stance(0, front_leg={"angle": 2}, back_leg={"angle": 0, "dy": -14}),
    ]},
    "crouch": {"fps": 12, "loop": False, "frames": [
        merged(crouched(), {"body": {"dy": 85}, "front_leg": {"sy": -0.2, "dy": 85}, "back_leg": {"sy": -0.2, "dy": 85}}),
        crouched(),
    ]},
    "jump_up": {"fps": 12, "loop": False, "frames": [
        merged(crouched(), {"body": {"dy": 70}, "front_leg": {"sy": -0.18, "dy": 70}, "back_leg": {"sy": -0.18, "dy": 70}}),
        tucked(body={"angle": -4}),
        tucked(),
    ]},
    "land": {"fps": 20, "loop": False, "frames": [
        merged(crouched(), {"body": {"dy": 85}, "front_leg": {"sy": -0.2, "dy": 85}, "back_leg": {"sy": -0.2, "dy": 85}}),
    ]},
    "block_high": {"fps": 12, "loop": False, "frames": [stance(10, -6, 70, body={"angle": -4}, far_arm={"angle": -30}),
                                                        stance(12, -8, 76, body={"angle": -5}, far_arm={"angle": -34})]},
    "block_low": {"fps": 12, "loop": False, "frames": [crouched(near_arm={"angle": -50}, far_arm={"angle": -40})]},
    "hit_high": {"fps": 14, "loop": False, "frames": [
        stance(8, -16, 30, body={"dx": -30, "angle": -14}, head={"dx": -34}),
        stance(6, -10, 20, body={"dx": -20, "angle": -9}, head={"dx": -22}),
        stance(2, -4, 6, body={"dx": -8, "angle": -3}, head={"dx": -8}),
    ]},
    "hit_low": {"fps": 14, "loop": False, "frames": [
        stance(50, 12, -30, body={"angle": 18}, head={"dy": 20, "dx": 26}),
        stance(34, 8, -18, body={"angle": 12}, head={"dy": 12, "dx": 16}),
        stance(12, 2, -6, body={"angle": 4}),
    ]},
    # Knockdown: she sits down hard and is up again (never a harmed pose: children_rules).
    "knockdown": {"fps": 12, "loop": False, "frames": [
        {**fall(18), "near_arm": {"angle": 30}},
        {**fall(44), "near_arm": {"angle": 40}},
        {**fall(70), "near_arm": {"angle": 30}},
        {**fall(84), "near_arm": {"angle": 20}},
    ]},
    # KO is never death (children_rules): down on one knee, gathering herself to scoop him up and run; the
    # game plays the flight.
    "ko": {"fps": 8, "loop": False, "frames": [
        crouched(head={"angle": 10}, near_arm={"angle": -40}),
        crouched(body={"dy": CROUCH_DY + 30, "angle": 12}, head={"angle": 14}, near_arm={"angle": -60}),
    ]},
    "wakeup": {"fps": 12, "loop": False, "frames": [
        {**fall(60), "near_arm": {"angle": 20}},
        {**fall(30), "near_arm": {"angle": -20}},
        crouched(),
        stance(10),
    ]},
    "dodge_forward": {"fps": 13, "loop": False, "frames": [
        crouched(),
        {**crouched(), "whole": {"angle": -90, "pivot": (420, 860), "dy": -70}},
        {**crouched(), "whole": {"angle": -180, "pivot": (420, 860), "dy": -120}},
        {**crouched(), "whole": {"angle": -270, "pivot": (420, 860), "dy": -70}},
        crouched(),
    ]},
    "dodge_back": {"fps": 12, "loop": False, "frames": [
        stance(8, -4, 20, body={"dx": -20, "angle": -6}),
        stance(10, -8, 34, body={"dx": -70, "angle": -14}, back_leg={"angle": -10}),
        stance(10, -8, 34, body={"dx": -70, "angle": -14}, back_leg={"angle": -10}),
        stance(6, -2, 10, body={"dx": -20, "angle": -4}),
    ]},
    "throw": {"fps": 15, "loop": False, "frames": [stance(8, arm=-20, body={"angle": 6}),
                                                   stance(8, arm=-30, body={"angle": 8}, near_arm={"dx": 20})]},
    "throw_hold": {"fps": 8, "loop": False, "frames": [
        stance(10, arm=-30, body={"angle": 6}, near_arm={"dx": 20}),
        stance(20, arm=60, body={"angle": -12}, far_arm={"angle": 30}),
        stance(24, arm=-50, body={"angle": 10}),
        stance(10, arm=-10, body={"angle": 4}),
    ]},
    "throw_whiff": {"fps": 10, "loop": False, "frames": [
        stance(10, arm=-40, body={"angle": 10, "dx": 20}, near_arm={"dx": 24}),
        stance(14, 6, -30, body={"angle": 12, "dx": 24}),
        stance(6),
    ]},
    "thrown": {"fps": 15, "loop": False, "frames": [
        stance(-10, 14, 50, body={"dx": 20, "angle": 10}, front_leg={"angle": 10}, back_leg={"angle": -10}),
        stance(-30, 18, 60, body={"dx": 30, "angle": 16}, front_leg={"angle": 16, "dy": -20},
               back_leg={"angle": -14, "dy": -20}),
    ]},
    # Apple Toss: she braces and pushes him up to lob it (the game draws him and the apple).
    "apple_toss": {"fps": 20, "loop": False, "frames": timed(
        16, 1, 18, stance(8, -4, 40, far_arm={"angle": 30}), stance(4, -6, 50, far_arm={"angle": 50}),
        stance(6, -2, 20), stance(0))},
    # Big Ears: the ears twitch, she drops under the strike, and answers with a low scratch.
    "big_ears": {"fps": 20, "loop": False, "frames": timed(
        30, 1, 20, crouched(head={"angle": -12}), crouched(body={"dy": 230}, near_arm={"angle": -40, "dx": 20, "dy": 120}),
        crouched(), stance(10))},
    # Shield Him: she turns her back and wraps around her brother.
    "shield_him": {"fps": 20, "loop": False, "frames": timed(
        6, 1, 30, crouched(near_arm={"angle": 60}, far_arm={"angle": 60}),
        crouched(near_arm={"angle": 80, "dx": -60}, far_arm={"angle": 70}, head={"angle": 20}),
        crouched(near_arm={"angle": 80, "dx": -60}, far_arm={"angle": 70}, head={"angle": 20}), stance(10))},
    # Rain of Apples: she braces with him on her shoulders while he hurls them.
    "rain_of_apples": {"fps": 20, "loop": False, "frames": timed(
        12, 24, 24, stance(10, -6, 70, far_arm={"angle": 40}), stance(14, -8, 80, far_arm={"angle": 50}),
        stance(8, -4, 40), stance(0))},
    # Lone Survivor: the lunge (the hit lands off-screen; the game plays the cutaway).
    "lone_survivor": {"fps": 20, "loop": False, "frames": timed(
        2, 2, 54, stance(10, -4, -10, near_arm={"dx": 20}),
        stance(6, -8, -30, body={"dx": 60, "angle": 14}, near_arm={"dx": 40}, far_arm={"angle": -120, "dx": 60}),
        stance(8, 6, -40), stance(0))},
    # Taunt: the toddler blows a raspberry; she quickly covers his mouth (her paw reaches back).
    "taunt": {"fps": 6, "loop": False, "frames": [stance(0), stance(4, 10, 0, far_arm={"angle": -40}),
                                                  stance(6, 12, 0, far_arm={"angle": -50}), stance(0)]},
    # Victory: sinks to her knees and hugs her brother hard (the game draws him in her arms).
    "victory": {"fps": 5, "loop": False, "frames": [stance(10), crouched(near_arm={"angle": -60}, far_arm={"angle": -70}),
                                                    crouched(near_arm={"angle": -70, "dx": -30}, far_arm={"angle": -80})]},
    # Victory (the other): he holds up an apple; she takes it, almost smiles.
    "victory_button": {"fps": 5, "loop": False, "frames": [stance(0), stance(4, 8, -40), stance(4, 6, -10, near_arm={"dy": -20}),
                                                          stance(2, 2, 10)]},
    # Perfect: she stands still and watches (he waves bye-bye).
    "perfect": {"fps": 4, "loop": False, "frames": [stance(0), stance(-4, -2, -10), stance(-4, -2, -10)]},
    # Intro: she pushes him back behind her and bares her teeth.
    "intro": {"fps": 4, "loop": False, "frames": [stance(4, 6, 10, far_arm={"angle": -30}),
                                                 stance(2, 4, 0, far_arm={"angle": -40}), stance(0, -6, -10), stance(0)]},
}

for _name, (_layer, _frames) in STRIKES.items():
    ANIMATIONS[_name] = {"fps": 20, "loop": False, "strike": [_layer], "frames": _frames}

# P2's alternate colours: her sandy fur warms to a red fox's rust (the grey dress and bandages keep their
# colour: too little saturation to match).
P2_RULES = [
    {"hue": (18, 44), "sat_min": 0.3, "val_min": 0.35, "shift": -14, "sat": 1.35},
]
