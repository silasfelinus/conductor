"""The Hyena Matriarch's rig (zuzu-showdown t-013).

Parts are cut from the t-013 parts sheet's fighting stance (ArtImage 244362: feet planted wide facing
right, her left arm flung back with the claws open, the iron chain looping from that wrist across her
legs to her right fist, which holds the meat hook up). Scale comes from the stance itself, so she stands
her kit's 104 px. Coordinates are the source image's pixels (832 x 1216); about 11 make one game pixel.

Her LP is the backhand: the open back arm swings over and through. Her HP is the chain-wrapped fist,
the front arm with the hook. The chain's long loop across her legs stays with the body; the stretch of
it in her fists moves with her arms. The long chain moves (Hook Lash, Chain Gang) are drawn by the game.

Moves are timed with `timed`: at 20 fps each drawn frame covers three sim frames, so a move's active
frames always show its strike pose (sprites.ts pickSprite: index = (frame - 1) * fps / 60).
"""

from __future__ import annotations

HEIGHT = 104
PALETTE_COLOURS = 20
STANCE = 244362
REFERENCE = {"art": STANCE}  # scale only

NECK = (420, 320)
FRONT_SHOULDER = (520, 470)
BACK_SHOULDER = (300, 330)
HIP_BACK = (270, 870)
HIP_FRONT = (560, 870)
TAIL_ROOT = (235, 730)
# The fighter's spot on the ground in the source art: midway between her feet.
ANCHOR = (405, 1160)

PARTS = {
    "tail": {"art": STANCE, "z": 0, "pivot": TAIL_ROOT, "follows": ["body"],
             "polygon": [(250, 686), (196, 700), (120, 712), (66, 748), (44, 830), (110, 806), (176, 800),
                         (230, 786), (262, 740)]},
    "back_arm": {"art": STANCE, "z": 5, "pivot": BACK_SHOULDER, "follows": ["body"],
                 "polygon": [(334, 296), (290, 284), (244, 298), (220, 336), (190, 352), (150, 318), (110, 300),
                             (62, 316), (44, 384), (76, 436), (86, 480), (120, 540), (150, 520), (128, 470),
                             (150, 500), (200, 528), (246, 520), (254, 478), (296, 466), (326, 420), (344, 360)]},
    "back_leg": {"art": STANCE, "z": 2, "pivot": HIP_BACK, "follows": [],
                 "polygon": [(166, 858), (306, 862), (318, 902), (282, 960), (236, 1056), (252, 1112),
                             (244, 1186), (36, 1186), (52, 1130), (108, 1078), (138, 964), (150, 900)]},
    "front_leg": {"art": STANCE, "z": 3, "pivot": HIP_FRONT, "follows": [],
                  "polygon": [(500, 862), (636, 850), (652, 900), (622, 962), (640, 1060), (704, 1092),
                              (776, 1138), (744, 1164), (556, 1156), (538, 1100), (528, 1000), (508, 940)]},
    "torso": {"art": STANCE, "z": 4, "pivot": HIP_FRONT, "follows": ["body"],
              # The chain's loop runs from her back wrist down across her legs and up to her front fist.
              "polygon": [(244, 300), (330, 288), (384, 312), (432, 332), (476, 342), (514, 384), (552, 432),
                          (548, 480), (516, 562), (506, 604), (546, 664), (604, 700), (676, 690), (716, 626),
                          (748, 628), (726, 706), (654, 748), (602, 764), (606, 780), (634, 846), (566, 884),
                          (500, 900), (456, 966), (396, 966), (388, 902), (318, 884), (248, 882), (186, 864),
                          (178, 820), (220, 706), (176, 684), (118, 604), (96, 542), (142, 538), (172, 600),
                          (230, 656), (252, 600), (292, 560), (320, 482), (284, 420)]},
    "head": {"art": STANCE, "z": 6, "pivot": NECK, "follows": ["body"],
             "polygon": [(246, 186), (262, 124), (316, 88), (396, 36), (506, 38), (604, 108), (590, 196),
                         (566, 246), (534, 300), (474, 302), (432, 334), (382, 314), (330, 302), (262, 272),
                         (238, 232)]},
    "chain_arm": {"art": STANCE, "z": 7, "pivot": FRONT_SHOULDER, "follows": ["body"],
                  "polygon": [(498, 458), (540, 466), (592, 478), (660, 488), (700, 450), (708, 428), (762, 426),
                              (802, 458), (802, 522), (782, 602), (742, 628), (700, 622), (662, 602), (600, 598),
                              (558, 562), (518, 552), (498, 520)]},
}

MEASURING = False  # set by rig.py while it measures reach


def merged(base: dict, more: dict) -> dict:
    out = {key: dict(value) if isinstance(value, dict) else value for key, value in base.items()}
    for key, value in more.items():
        out[key] = {**out.get(key, {}), **value} if isinstance(value, dict) else value
    return out


def stance(dy=0, tilt=0, chain=0, back=0, **more):
    """The fighting stance is the source art itself: the body dropped `dy`, the head tilted, the chain
    arm and the back arm turned, plus `more` per part."""
    return merged({"body": {"dy": dy}, "head": {"angle": tilt}, "chain_arm": {"angle": chain},
                   "back_arm": {"angle": back}}, more)


CROUCH_DY = 170


def crouched(**more):
    """Down low: the body drops onto legs squashed about the hips, feet planted, the hook held ready."""
    return merged({"body": {"dy": CROUCH_DY, "angle": 6}, "front_leg": {"sy": -0.42, "sx": 0.12, "dy": CROUCH_DY},
                   "back_leg": {"sy": -0.42, "sx": 0.12, "dy": CROUCH_DY}, "chain_arm": {"angle": -8},
                   "back_arm": {"angle": -20}}, more)


def tucked(**more):
    """The top of the jump: knees drawn up, the tail flying."""
    return merged({"body": {"angle": -6}, "front_leg": {"sy": -0.5, "angle": 24, "dy": -50},
                   "back_leg": {"sy": -0.5, "angle": -14, "dy": -50}, "tail": {"angle": -16},
                   "chain_arm": {"angle": 16}, "back_arm": {"angle": -20}}, more)


def fall(angle, pivot=(120, 1170)):
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


# The backhand: the back arm (flung back in the stance) swings down past her hip and up through to
# point at the opponent, the open claws leading; she steps into it (`dx`).
BACKHAND = 158
# The chain fist: the front arm (held forward and a little up in the stance) punched level and out.
PUNCH = -18


def backhand(extra=0, dx=0, dy=0):
    return {"back_arm": {"angle": BACKHAND + extra, "dx": dx, "dy": dy}}


STRIKES = {
    # Standing LP: the backhand, swung over and through at chest height.
    "stand_lp": timed(4, 2, 6, stance(6, back=-60), stance(4, **backhand(10, 190, 90), body={"angle": 4, "dx": 30}),
                      stance(4, back=-100), stance(0)),
    # Standing HP: the chain-wrapped fist, a straight heavy punch.
    "stand_hp": timed(8, 3, 16, stance(8, chain=30, body={"angle": -4}),
                      stance(6, chain=PUNCH, body={"angle": 6, "dx": 30}, chain_arm={"dx": 110}),
                      stance(8, chain=-30), stance(2)),
    # Standing LK: a quick boot to the shin.
    "stand_lk": timed(5, 3, 8, stance(4, front_leg={"angle": 20}),
                      stance(2, body={"angle": -6}, front_leg={"angle": 64, "dy": -30, "dx": 30}),
                      stance(4, front_leg={"angle": 24}), stance(0)),
    # Standing HK: a stamping front kick, leaning back behind it.
    "stand_hk": timed(10, 4, 18, stance(8, front_leg={"angle": 30}),
                      stance(-4, body={"angle": -10, "dx": -10}, front_leg={"angle": 84, "dy": -30, "dx": 30}),
                      stance(4, front_leg={"angle": 40, "dy": -20}), stance(0)),
    "crouch_lp": timed(4, 2, 6, crouched(back_arm={"angle": -60}),
                       crouched(back_arm={"angle": BACKHAND + 8, "dx": 200, "dy": CROUCH_DY}),
                       crouched(back_arm={"angle": -80})),
    # Crouching LK: a boot poke along the floor.
    "crouch_lk": timed(5, 3, 8, crouched(front_leg={"sy": -0.42, "sx": 0.12, "dy": CROUCH_DY, "angle": 30}),
                       crouched(front_leg={"sy": 0.0, "sx": 0, "dy": CROUCH_DY, "angle": 74, "dx": 40}),
                       crouched(front_leg={"sy": -0.42, "sx": 0.12, "dy": CROUCH_DY, "angle": 30})),
    # Crouching HP: the anti-air, the chain fist driven up.
    "crouch_hp": timed(7, 4, 16, crouched(chain_arm={"angle": 0}),
                       [crouched(chain_arm={"angle": 40, "dy": -60}),
                        crouched(chain_arm={"angle": 70, "dy": -230, "dx": -30})],
                       crouched(chain_arm={"angle": 10})),
    # Crouching HK: the sweep, low along the floor.
    "crouch_hk": timed(9, 4, 20, crouched(),
                       crouched(body={"dy": 210, "angle": 10}, back_leg={"sy": -0.6, "sx": 0.12, "dy": 210},
                                front_leg={"sy": 0.15, "sx": 0, "dy": 210, "dx": 10, "angle": 88}),
                       crouched(front_leg={"sy": -0.3, "dy": CROUCH_DY, "angle": 40})),
    "jump_lp": timed(4, 6, 4, tucked(), tucked(back_arm={"angle": BACKHAND - 34, "dx": 160, "dy": 180}), tucked()),
    # Jumping HP: the chain fist hammered down.
    "jump_hp": timed(7, 5, 6, tucked(chain_arm={"angle": 50}),
                     tucked(chain_arm={"angle": -60, "dy": 200, "dx": 90}), tucked(chain_arm={"angle": -30})),
    "jump_lk": timed(4, 8, 4, tucked(), tucked(front_leg={"sy": -0.05, "angle": 44, "dy": 10, "dx": 20}), tucked()),
    "jump_hk": timed(7, 5, 6, tucked(body={"angle": -10}),
                     tucked(body={"angle": -12}, front_leg={"sy": 0.1, "angle": 50, "dx": 60, "dy": 30},
                            back_leg={"sy": -0.5, "angle": -20}),
                     tucked()),
}

LAUGH = [stance(-6, -14, 10, -30, body={"angle": -6}), stance(-2, -8, 6, -20, body={"angle": -3}),
         stance(-8, -16, 12, -34, body={"angle": -7}), stance(-2, -8, 6, -20, body={"angle": -3})]

ANIMATIONS = {
    # Idle: a rolling, hungry sway, the hook bobbing, the tail twitching.
    "idle": {"fps": 6, "loop": True, "frames": [stance(0), stance(-6, 2, 4, 3, tail={"angle": 4}),
                                                stance(-8, 3, 6, 4, tail={"angle": 7}),
                                                stance(-4, 1, 2, 2, tail={"angle": 3})]},
    # Walking: a loping, shoulder-rolling stride.
    "walk_forward": {"fps": 9, "loop": True, "frames": [
        stance(6, 2, 6, -6, front_leg={"angle": 14}, back_leg={"angle": -8}, tail={"angle": 5}),
        stance(0, 0, 2, 0, front_leg={"angle": 4}, back_leg={"angle": 0, "dy": -16}, tail={"angle": 0}),
        stance(6, -2, -4, 6, front_leg={"angle": -10}, back_leg={"angle": 10}, tail={"angle": -4}),
        stance(0, 0, 0, 2, front_leg={"angle": -2, "dy": -16}, back_leg={"angle": 2}, tail={"angle": 0}),
    ]},
    "walk_back": {"fps": 8, "loop": True, "frames": [
        stance(4, front_leg={"angle": -8}, back_leg={"angle": 12}),
        stance(0, front_leg={"angle": 0, "dy": -14}, back_leg={"angle": 2}),
        stance(4, front_leg={"angle": 8}, back_leg={"angle": -8}),
        stance(0, front_leg={"angle": 2}, back_leg={"angle": 0, "dy": -14}),
    ]},
    "crouch": {"fps": 12, "loop": False, "frames": [
        merged(crouched(), {"body": {"dy": 85}, "front_leg": {"sy": -0.21, "dy": 85}, "back_leg": {"sy": -0.21, "dy": 85}}),
        crouched(),
    ]},
    "jump_up": {"fps": 12, "loop": False, "frames": [
        merged(crouched(), {"body": {"dy": 70}, "front_leg": {"sy": -0.18, "dy": 70}, "back_leg": {"sy": -0.18, "dy": 70}}),
        tucked(body={"angle": -3}),
        tucked(),
    ]},
    "land": {"fps": 20, "loop": False, "frames": [
        merged(crouched(), {"body": {"dy": 85}, "front_leg": {"sy": -0.21, "dy": 85}, "back_leg": {"sy": -0.21, "dy": 85}}),
    ]},
    # Blocks: the chain fist up across her face (high), or down into the crouch (low).
    "block_high": {"fps": 12, "loop": False, "frames": [stance(8, -4, 50, -40, body={"angle": -4}),
                                                        stance(10, -6, 56, -44, body={"angle": -5})]},
    "block_low": {"fps": 12, "loop": False, "frames": [crouched(chain_arm={"angle": -50})]},
    "hit_high": {"fps": 14, "loop": False, "frames": [
        stance(8, -16, 30, 20, body={"dx": -30, "angle": -12}, head={"dx": -30}),
        stance(6, -10, 20, 12, body={"dx": -18, "angle": -8}, head={"dx": -18}),
        stance(2, -4, 6, 4, body={"dx": -6, "angle": -3}, head={"dx": -6}),
    ]},
    "hit_low": {"fps": 14, "loop": False, "frames": [
        stance(50, 10, -30, -20, body={"angle": 16}, head={"dy": 16, "dx": 24}),
        stance(34, 6, -18, -12, body={"angle": 10}, head={"dy": 10, "dx": 14}),
        stance(12, 2, -6, -4, body={"angle": 4}),
    ]},
    "knockdown": {"fps": 12, "loop": False, "frames": [
        {**fall(20), "body": {"angle": -6}, "chain_arm": {"angle": 30}},
        {**fall(48), "chain_arm": {"angle": 40}},
        {**fall(76), "chain_arm": {"angle": 30}},
        {**fall(90), "chain_arm": {"angle": 20}},
    ]},
    # KO (fighters.yaml): she topples backward with one last hiccuping giggle.
    "ko": {"fps": 8, "loop": False, "frames": [
        {**stance(-6, -14, 20, -30), **fall(16)},
        {**stance(0, -10, 30, -20), **fall(44)},
        {**stance(0, -6, 40, -10), **fall(76)},
        {**stance(0, -4, 40, -10), **fall(90)},
    ]},
    "wakeup": {"fps": 12, "loop": False, "frames": [
        {**fall(70), "chain_arm": {"angle": 20}},
        {**fall(40), "chain_arm": {"angle": -20}},
        crouched(),
        stance(10),
    ]},
    "dodge_forward": {"fps": 13, "loop": False, "frames": [
        crouched(),
        {**crouched(), "whole": {"angle": -90, "pivot": (400, 900), "dy": -60}},
        {**crouched(), "whole": {"angle": -180, "pivot": (400, 900), "dy": -110}},
        {**crouched(), "whole": {"angle": -270, "pivot": (400, 900), "dy": -60}},
        crouched(),
    ]},
    "dodge_back": {"fps": 12, "loop": False, "frames": [
        stance(8, -4, 20, -10, body={"dx": -20, "angle": -6}),
        stance(10, -8, 34, -20, body={"dx": -60, "angle": -12}, back_leg={"angle": -8}),
        stance(10, -8, 34, -20, body={"dx": -60, "angle": -12}, back_leg={"angle": -8}),
        stance(6, -2, 10, -6, body={"dx": -20, "angle": -4}),
    ]},
    # Throws: the chain fist takes the collar, then she slings them past her.
    "throw": {"fps": 15, "loop": False, "frames": [stance(8, chain=-30, body={"angle": 6}),
                                                   stance(8, chain=-40, body={"angle": 8}, chain_arm={"dx": 40})]},
    "throw_hold": {"fps": 8, "loop": False, "frames": [
        stance(10, chain=-40, body={"angle": 6}, chain_arm={"dx": 40}),
        stance(20, chain=60, body={"angle": -12}),
        stance(24, chain=-60, body={"angle": 10}),
        stance(10, chain=-10, body={"angle": 4}),
    ]},
    "throw_whiff": {"fps": 10, "loop": False, "frames": [
        stance(10, chain=-50, body={"angle": 10, "dx": 20}, chain_arm={"dx": 40}),
        stance(14, 6, -40, body={"angle": 12, "dx": 24}),
        stance(6),
    ]},
    "thrown": {"fps": 15, "loop": False, "frames": [
        stance(-10, 14, 50, 20, body={"dx": 20, "angle": 10}, front_leg={"angle": 10}, back_leg={"angle": -10}),
        stance(-30, 18, 60, 30, body={"dx": 30, "angle": 16}, front_leg={"angle": 16, "dy": -20},
               back_leg={"angle": -14, "dy": -20}),
    ]},
    # Hook Lash: the hook thrown out from the fist (the game draws the chain in flight).
    "hook_lash": {"fps": 20, "loop": False, "frames": timed(
        12, 4, 22, stance(6, chain=50, body={"angle": -6}), stance(2, chain=-24, body={"angle": 8, "dx": 30},
                                                                    chain_arm={"dx": 70}),
        stance(4, chain=-10), stance(0))},
    # Drag: she hauls the hooked opponent in, leaning back.
    "drag": {"fps": 20, "loop": False, "frames": timed(
        3, 3, 18, stance(4, chain=-20, chain_arm={"dx": 50}), stance(-2, -6, 40, -20, body={"angle": -12, "dx": -30}),
        stance(2, chain=20, body={"angle": -6}), stance(0))},
    # Cackle: head thrown back, laughing (open the whole time).
    "cackle": {"fps": 12, "loop": True, "frames": LAUGH},
    # Scavenger's Rush: a low lope that ends in a snapping bite.
    "scavengers_rush": {"fps": 20, "loop": False, "frames": timed(
        6, 18, 16, crouched(body={"dy": 120, "angle": 14}),
        [crouched(body={"dy": 110, "angle": 18, "dx": 30}, head={"angle": -10, "dx": 40, "dy": 60}),
         crouched(body={"dy": 120, "angle": 20, "dx": 50}, head={"angle": -20, "dx": 70, "dy": 70},
                  front_leg={"angle": 20})],
        crouched(), stance(6))},
    # Bone Crusher: she grabs, bites the shoulder and shakes.
    "bone_crusher": {"fps": 20, "loop": False, "frames": timed(
        5, 2, 30, stance(6, chain=-30, back=-120, body={"angle": 8}),
        stance(10, 10, -40, -150, body={"angle": 14, "dx": 40}, head={"dx": 40, "dy": 40}),
        stance(14, 14, -40, -150, body={"angle": 18, "dx": 50}, head={"dx": 50, "dy": 50, "angle": 10}),
        stance(4))},
    # Chain Gang: the chain whirled overhead, then smashed down (the game draws the whirling chain).
    "chain_gang": {"fps": 20, "loop": False, "frames": timed(
        8, 30, 30, stance(0, -6, 80, -20, body={"angle": -6}),
        [stance(-4, -8, 120, -20), stance(-4, -8, 160, -20), stance(-4, -8, 100, -20), stance(-4, -8, 140, -20)],
        stance(10, 6, -70, -10, body={"angle": 12}), stance(0))},
    # Last Laugh: she steps in with the hook, and the laughing stops.
    "last_laugh": {"fps": 20, "loop": False, "frames": timed(
        2, 36, 50, LAUGH[0], [*LAUGH, *LAUGH, stance(4, 0, 40, -20)],
        stance(6, chain=PUNCH, body={"angle": 8, "dx": 40}, chain_arm={"dx": 60}), stance(0))},
    # Taunt (fighters.yaml): she cackles and slaps her knee.
    "taunt": {"fps": 8, "loop": False, "frames": [*LAUGH, stance(10, -10, 10, -60, body={"angle": 6})]},
    # Victory: hangs the loser's hat on her trophy rack (the hook raised high).
    "victory": {"fps": 5, "loop": False, "frames": [stance(0, 0, 30), stance(-4, -6, 70), stance(-6, -8, 80)]},
    # Victory (the other): laughs so hard she has to sit down, wiping her eyes.
    "victory_button": {"fps": 6, "loop": False, "frames": [*LAUGH, crouched(back_arm={"angle": -120}),
                                                          crouched(back_arm={"angle": -130}, head={"angle": -12})]},
    # Perfect: she doesn't laugh. Just stares.
    "perfect": {"fps": 4, "loop": False, "frames": [stance(0), stance(2, 6), stance(2, 8), stance(2, 8)]},
    # Intro: drags the chain in a long slow scrape, then grins.
    "intro": {"fps": 4, "loop": False, "frames": [stance(4, 4, -60, 10), stance(2, 2, -40, 6), stance(0, -4, -10),
                                                 stance(-4, -10, 10)]},
}

for _name, _frames in STRIKES.items():
    if _name.endswith("_lp"):
        _strike = "back_arm"
    elif _name.endswith("_hp"):
        _strike = "chain_arm"
    else:
        _strike = "front_leg"
    ANIMATIONS[_name] = {"fps": 20, "loop": False, "strike": [_strike], "frames": _frames}

# P2's alternate colours: the black leather stays black (value too low to recolour), so P2 turns her
# sandy spotted fur a cold grey and the tan apron a dull green.
P2_RULES = [
    {"hue": (18, 48), "sat_min": 0.2, "val_min": 0.3, "shift": 120, "sat": 0.45},
]
