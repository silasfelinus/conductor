"""Storm Crow's rig (zuzu-showdown t-012).

Parts are cut from the t-012 parts sheet's fighting stance (ArtImage 244343: a wide lunge facing right, the
hooked blade raised in his right hand, his left hand at his hip, the great black wings half spread from his
back, the rifle slung behind). Scale comes from the stance itself, so he stands his kit's 100 px.
Coordinates are the source image's pixels (832 x 1216); about 11 make one game pixel.

His LP is the wing buffet: the near wing sweeps forward off his back. His HP is the hooked blade. In the
air the wing beats (Take Wing, the hover); the lightning, the flock and the rifle's shot are the game's.

Moves are timed with `timed`: at 20 fps each drawn frame covers three sim frames, so a move's active
frames always show its strike pose (sprites.ts pickSprite: index = (frame - 1) * fps / 60).
"""

from __future__ import annotations

HEIGHT = 100
PALETTE_COLOURS = 20
STANCE = 244343
REFERENCE = {"art": STANCE}  # scale only

NECK = (440, 400)
SHOULDER = (540, 490)
WING_ROOT = (320, 440)
HIP_BACK = (290, 900)
HIP_FRONT = (560, 880)
# The fighter's spot on the ground in the source art: midway between his feet.
ANCHOR = (400, 1150)

PARTS = {
    "wing": {"art": STANCE, "z": 0, "pivot": WING_ROOT, "follows": ["body"],
             "polygon": [(40, 36), (104, 36), (200, 116), (262, 156), (312, 248), (342, 338), (352, 380),
                         (332, 424), (292, 472), (252, 524), (200, 524), (160, 424), (138, 330), (98, 252),
                         (58, 172), (38, 100)]},
    "back_leg": {"art": STANCE, "z": 1, "pivot": HIP_BACK, "follows": [],
                 "polygon": [(150, 880), (330, 880), (322, 940), (252, 1000), (212, 1060), (172, 1130),
                             (172, 1164), (78, 1164), (88, 1110), (118, 1060), (150, 960)]},
    "front_leg": {"art": STANCE, "z": 2, "pivot": HIP_FRONT, "follows": [],
                  "polygon": [(480, 858), (642, 858), (652, 950), (642, 1040), (632, 1090), (722, 1108),
                              (722, 1144), (548, 1144), (548, 1060), (540, 980), (500, 920)]},
    "torso": {"art": STANCE, "z": 3, "pivot": HIP_FRONT, "follows": ["body"],
              "polygon": [(340, 378), (420, 378), (480, 418), (540, 438), (562, 480), (562, 560), (600, 620),
                          (622, 700), (652, 820), (642, 882), (560, 902), (470, 922), (440, 954), (400, 922),
                          (330, 922), (250, 962), (160, 962), (58, 968), (140, 880), (230, 800), (240, 700),
                          (206, 692), (200, 636), (240, 620), (250, 560), (240, 500), (300, 420)]},
    "head": {"art": STANCE, "z": 4, "pivot": NECK, "follows": ["body"],
             "polygon": [(358, 280), (378, 238), (440, 222), (522, 228), (562, 278), (596, 350), (560, 362),
                         (500, 372), (480, 420), (430, 432), (380, 402), (350, 350)]},
    "blade_arm": {"art": STANCE, "z": 5, "pivot": SHOULDER, "follows": ["body"],
                  "polygon": [(530, 470), (590, 480), (640, 490), (670, 450), (680, 420), (700, 400),
                              (700, 320), (640, 280), (600, 280), (600, 258), (660, 226), (730, 238), (764, 290),
                              (762, 420), (754, 480), (732, 520), (720, 594), (684, 594), (680, 560), (660, 602),
                              (620, 614), (570, 604), (540, 566)]},
}

MEASURING = False  # set by rig.py while it measures reach


def merged(base: dict, more: dict) -> dict:
    out = {key: dict(value) if isinstance(value, dict) else value for key, value in base.items()}
    for key, value in more.items():
        out[key] = {**out.get(key, {}), **value} if isinstance(value, dict) else value
    return out


def stance(dy=0, tilt=0, blade=0, wing=0, **more):
    """The fighting stance is the source art itself: the body dropped `dy`, the head tilted, the blade
    arm and the wing turned, plus `more` per part."""
    return merged({"body": {"dy": dy}, "head": {"angle": tilt}, "blade_arm": {"angle": blade},
                   "wing": {"angle": wing}}, more)


CROUCH_DY = 160


def crouched(**more):
    """Down low: the body drops onto legs squashed about the hips, the wing folded, the blade ready."""
    return merged({"body": {"dy": CROUCH_DY, "angle": 6}, "front_leg": {"sy": -0.42, "sx": 0.12, "dy": CROUCH_DY},
                   "back_leg": {"sy": -0.42, "sx": 0.12, "dy": CROUCH_DY}, "blade_arm": {"angle": -8},
                   "wing": {"angle": 10}}, more)


def tucked(**more):
    """The top of the jump: knees drawn up, the wing raised for the beat."""
    return merged({"body": {"angle": -6}, "front_leg": {"sy": -0.5, "angle": 24, "dy": -50},
                   "back_leg": {"sy": -0.5, "angle": -14, "dy": -50}, "blade_arm": {"angle": 16},
                   "wing": {"angle": 16}}, more)


def flying(beat=0, **more):
    """Aloft: legs dangling, the wing beating (`beat` from -40, down, to 20, up)."""
    return merged({"body": {"angle": -4}, "front_leg": {"angle": 8, "dy": -20}, "back_leg": {"angle": -6, "dy": -20},
                   "wing": {"angle": beat}, "blade_arm": {"angle": 6}}, more)


def fall(angle, pivot=(120, 1150)):
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


# The wing buffet: the wing (raised behind him in the stance) swung clockwise, forward and down past his
# shoulder, its trailing feathers leading; he leans in.
BUFFET = -120
# The blade: the stance holds it raised; it slashes clockwise, down and through.
SLASH = -70


def buffet(extra=0, dx=0, dy=0):
    return {"wing": {"angle": BUFFET + extra, "dx": dx, "dy": dy}}


STRIKES = {
    # Standing LP: the wing buffet, a quick sweep forward.
    "stand_lp": timed(4, 2, 6, stance(4, wing=-40), merged(stance(2, body={"angle": 4, "dx": 20}), buffet(0, 160, 40)),
                      stance(4, wing=-60), stance(0)),
    # Standing HP: the hooked blade, a long downward slash.
    "stand_hp": timed(8, 3, 16, stance(6, blade=30, body={"angle": -4}),
                      stance(6, blade=SLASH, body={"angle": 8, "dx": 30}, blade_arm={"dx": 40}),
                      stance(8, blade=-100), stance(2)),
    # Standing LK: a quick talon kick.
    "stand_lk": timed(5, 3, 8, stance(4, front_leg={"angle": 20}),
                      stance(2, body={"angle": -6}, front_leg={"angle": 64, "dy": -30, "dx": 30}),
                      stance(4, front_leg={"angle": 24}), stance(0)),
    # Standing HK: a high stamping kick, leaning back behind it.
    "stand_hk": timed(10, 4, 18, stance(8, front_leg={"angle": 30}),
                      stance(-4, body={"angle": -10, "dx": -10}, front_leg={"angle": 84, "dy": -30, "dx": 30}),
                      stance(4, front_leg={"angle": 40, "dy": -20}), stance(0)),
    "crouch_lp": timed(4, 2, 6, crouched(wing={"angle": -30}),
                       crouched(wing={"angle": BUFFET + 10, "dx": 170, "dy": 120}), crouched(wing={"angle": -40})),
    # Crouching LK: a talon poke along the floor.
    "crouch_lk": timed(5, 3, 8, crouched(front_leg={"sy": -0.42, "sx": 0.12, "dy": CROUCH_DY, "angle": 30}),
                       crouched(front_leg={"sy": 0.0, "sx": 0, "dy": CROUCH_DY, "angle": 74, "dx": 40}),
                       crouched(front_leg={"sy": -0.42, "sx": 0.12, "dy": CROUCH_DY, "angle": 30})),
    # Crouching HP: the anti-air, the hook swung up overhead.
    "crouch_hp": timed(7, 4, 16, crouched(blade_arm={"angle": -20}),
                       [crouched(blade_arm={"angle": 20, "dy": -40}), crouched(blade_arm={"angle": 40, "dy": -120})],
                       crouched(blade_arm={"angle": 0})),
    # Crouching HK: the sweep, low along the floor.
    "crouch_hk": timed(9, 4, 20, crouched(),
                       crouched(body={"dy": 200, "angle": 10}, back_leg={"sy": -0.6, "sx": 0.12, "dy": 200},
                                front_leg={"sy": 0.15, "sx": 0, "dy": 200, "dx": 10, "angle": 88}),
                       crouched(front_leg={"sy": -0.3, "dy": CROUCH_DY, "angle": 40})),
    "jump_lp": timed(4, 6, 4, tucked(), tucked(wing={"angle": BUFFET - 30, "dx": 160, "dy": 200}), tucked()),
    # Jumping HP: the hook raked down.
    "jump_hp": timed(7, 5, 6, tucked(blade_arm={"angle": 40}),
                     tucked(blade_arm={"angle": -110, "dy": 120, "dx": 40}), tucked(blade_arm={"angle": -40})),
    "jump_lk": timed(4, 8, 4, tucked(), tucked(front_leg={"sy": -0.05, "angle": 44, "dy": 10, "dx": 20}), tucked()),
    "jump_hk": timed(7, 5, 6, tucked(body={"angle": -10}),
                     tucked(body={"angle": -12}, front_leg={"sy": 0.1, "angle": 50, "dx": 60, "dy": 30},
                            back_leg={"sy": -0.5, "angle": -20}),
                     tucked()),
}

BEAT = [flying(-40), flying(-10), flying(20), flying(-10)]

ANIMATIONS = {
    # Idle: a cocky sway, the wing ruffling, the blade bobbing.
    "idle": {"fps": 6, "loop": True, "frames": [stance(0), stance(-6, 2, 3, 3), stance(-8, 3, 4, 5),
                                                stance(-4, 1, 2, 2)]},
    "walk_forward": {"fps": 9, "loop": True, "frames": [
        stance(6, 2, 4, 4, front_leg={"angle": 14}, back_leg={"angle": -8}),
        stance(0, 0, 2, 0, front_leg={"angle": 4}, back_leg={"angle": 0, "dy": -16}),
        stance(6, -2, -2, -4, front_leg={"angle": -10}, back_leg={"angle": 10}),
        stance(0, 0, 0, 2, front_leg={"angle": -2, "dy": -16}, back_leg={"angle": 2}),
    ]},
    "walk_back": {"fps": 8, "loop": True, "frames": [
        stance(4, front_leg={"angle": -8}, back_leg={"angle": 12}),
        stance(0, front_leg={"angle": 0, "dy": -14}, back_leg={"angle": 2}),
        stance(4, front_leg={"angle": 8}, back_leg={"angle": -8}),
        stance(0, front_leg={"angle": 2}, back_leg={"angle": 0, "dy": -14}),
    ]},
    "crouch": {"fps": 12, "loop": False, "frames": [
        merged(crouched(), {"body": {"dy": 80}, "front_leg": {"sy": -0.21, "dy": 80}, "back_leg": {"sy": -0.21, "dy": 80}}),
        crouched(),
    ]},
    "jump_up": {"fps": 12, "loop": False, "frames": [
        merged(crouched(), {"body": {"dy": 70}, "front_leg": {"sy": -0.18, "dy": 70}, "back_leg": {"sy": -0.18, "dy": 70}}),
        tucked(wing={"angle": -30}),
        tucked(),
    ]},
    "land": {"fps": 20, "loop": False, "frames": [
        merged(crouched(), {"body": {"dy": 80}, "front_leg": {"sy": -0.21, "dy": 80}, "back_leg": {"sy": -0.21, "dy": 80}}),
    ]},
    "block_high": {"fps": 12, "loop": False, "frames": [stance(8, -4, 40, -60, body={"angle": -4}),
                                                        stance(10, -6, 46, -70, body={"angle": -5})]},
    "block_low": {"fps": 12, "loop": False, "frames": [crouched(blade_arm={"angle": -50}, wing={"angle": -40})]},
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
        {**fall(20), "body": {"angle": -6}, "blade_arm": {"angle": 30}},
        {**fall(48), "blade_arm": {"angle": 40}, "wing": {"angle": 20}},
        {**fall(76), "blade_arm": {"angle": 30}, "wing": {"angle": 30}},
        {**fall(90), "blade_arm": {"angle": 20}, "wing": {"angle": 30}},
    ]},
    # KO (fighters.yaml): he spins down and lands in a heap.
    "ko": {"fps": 8, "loop": False, "frames": [
        {**stance(-6, -14, 20, 30), **fall(20)},
        {**stance(0, -10, 30, 40), **fall(50)},
        {**stance(0, -6, 40, 40), **fall(80)},
        {**stance(0, -4, 40, 40), **fall(90)},
    ]},
    "wakeup": {"fps": 12, "loop": False, "frames": [
        {**fall(70), "blade_arm": {"angle": 20}},
        {**fall(40), "blade_arm": {"angle": -20}},
        crouched(),
        stance(10),
    ]},
    "dodge_forward": {"fps": 13, "loop": False, "frames": [
        crouched(),
        {**crouched(), "whole": {"angle": -90, "pivot": (400, 880), "dy": -60}},
        {**crouched(), "whole": {"angle": -180, "pivot": (400, 880), "dy": -110}},
        {**crouched(), "whole": {"angle": -270, "pivot": (400, 880), "dy": -60}},
        crouched(),
    ]},
    "dodge_back": {"fps": 12, "loop": False, "frames": [
        stance(8, -4, 20, -20, body={"dx": -20, "angle": -6}),
        stance(10, -8, 34, -40, body={"dx": -60, "angle": -12}, back_leg={"angle": -8}),
        stance(10, -8, 34, -40, body={"dx": -60, "angle": -12}, back_leg={"angle": -8}),
        stance(6, -2, 10, -10, body={"dx": -20, "angle": -4}),
    ]},
    "throw": {"fps": 15, "loop": False, "frames": [stance(8, blade=-40, body={"angle": 6}),
                                                   stance(8, blade=-60, body={"angle": 8}, blade_arm={"dx": 30})]},
    "throw_hold": {"fps": 8, "loop": False, "frames": [
        stance(10, blade=-60, body={"angle": 6}, blade_arm={"dx": 30}),
        stance(20, blade=40, wing=-40, body={"angle": -12}),
        stance(24, blade=-80, wing=10, body={"angle": 10}),
        stance(10, blade=-10, body={"angle": 4}),
    ]},
    "throw_whiff": {"fps": 10, "loop": False, "frames": [
        stance(10, blade=-60, body={"angle": 10, "dx": 20}, blade_arm={"dx": 30}),
        stance(14, 6, -50, body={"angle": 12, "dx": 24}),
        stance(6),
    ]},
    "thrown": {"fps": 15, "loop": False, "frames": [
        stance(-10, 14, 50, 30, body={"dx": 20, "angle": 10}, front_leg={"angle": 10}, back_leg={"angle": -10}),
        stance(-30, 18, 60, 40, body={"dx": 30, "angle": 16}, front_leg={"angle": 16, "dy": -20},
               back_leg={"angle": -14, "dy": -20}),
    ]},
    # Murder Dive: from the air, a steep dive, talons first.
    "murder_dive": {"fps": 20, "loop": False, "frames": timed(
        6, 22, 10, tucked(wing={"angle": 30}),
        {**tucked(wing={"angle": -50}, front_leg={"angle": 50, "dy": 20, "dx": 30}), "whole": {"angle": -24,
                                                                                         "pivot": (400, 700)}},
        tucked(), flying(-10))},
    # Hook and Reel: the blade thrown out on its cord, then hauled back (the game draws the cord).
    "hook_and_reel": {"fps": 20, "loop": False, "frames": timed(
        14, 4, 24, stance(6, blade=50, body={"angle": -6}),
        stance(2, blade=-50, body={"angle": 8, "dx": 30}, blade_arm={"dx": 60}),
        stance(-2, -6, 40, body={"angle": -10, "dx": -30}), stance(0))},
    # Take Wing: one great beat and he is aloft.
    "take_wing": {"fps": 20, "loop": False, "frames": [crouched(wing={"angle": 30}), flying(-40), flying(-10)]},
    # Thunderhead: he raises the hook to the storm (the game draws the cloud and the bolt).
    "thunderhead": {"fps": 20, "loop": False, "frames": timed(
        30, 6, 24, stance(-4, -10, 40, 10, body={"angle": -6}), stance(-6, -14, 60, 20, body={"angle": -8}),
        stance(-2, -6, 30, 6), stance(0))},
    "thunderhead_air": {"fps": 20, "loop": False, "frames": timed(
        10, 6, 16, flying(-20, blade_arm={"angle": 40}), flying(10, blade_arm={"angle": 60}),
        flying(-10, blade_arm={"angle": 30}))},
    # Rifle Crack: he swings the rifle round and fires (the shot is the game's).
    "rifle_crack": {"fps": 20, "loop": False, "frames": timed(
        24, 1, 26, stance(6, blade=-40, wing=-20, body={"angle": -4}),
        stance(4, blade=-30, wing=-20, body={"angle": -8, "dx": -20}),
        stance(4, blade=-20, body={"angle": -4}), stance(0))},
    # Wheel of Wings: he spins with the wings out, a whirl of feathers.
    "wheel_of_wings": {"fps": 20, "loop": False, "frames": timed(
        6, 30, 26, stance(4, wing=-40),
        [stance(0, wing=-120), stance(0, wing=-200, body={"angle": 6}), stance(0, wing=-280),
         stance(0, wing=-360, body={"angle": -6})],
        stance(4, wing=-20), stance(0))},
    # The Murder: he screams, and the whole flock pours across (the game draws the flock).
    "the_murder": {"fps": 20, "loop": False, "frames": timed(
        2, 36, 50, stance(-4, -16, 40, 20, body={"angle": -8}),
        [stance(-8, -22, 60, 30, body={"angle": -10}), stance(-6, -20, 56, 26, body={"angle": -9})],
        stance(0, -6, 20, 6), stance(0))},
    # Taunt (fighters.yaml): spreads his wings wide and caws at the sky.
    "taunt": {"fps": 8, "loop": False, "frames": [stance(0, -10, 10, 20), stance(-4, -20, 20, 30),
                                                  stance(-4, -22, 20, 34), stance(0, -6, 4, 6)]},
    # Victory: perches with the rifle across his knees, preening.
    "victory": {"fps": 5, "loop": False, "frames": [crouched(), crouched(head={"angle": 16}),
                                                    crouched(head={"angle": 22}, wing={"angle": 20})]},
    # Victory (the other): bows with a theatrical sweep of the wing.
    "victory_button": {"fps": 5, "loop": False, "frames": [stance(0, 0, -20, -40), stance(10, 14, -40, -80,
                                                                                       body={"angle": 10}),
                                                          stance(14, 18, -50, -100, body={"angle": 14})]},
    # Perfect: he doesn't land. Hovers, laughs, and flies off into the storm.
    "perfect": {"fps": 6, "loop": True, "frames": BEAT},
    # Intro: drops out of the storm, folds his wings, and shakes off the rain.
    "intro": {"fps": 6, "loop": False, "frames": [flying(-30), flying(10), crouched(wing={"angle": 20}),
                                                 stance(-4, 4, 0, 6), stance(0, -4, 0, -6), stance(0)]},
}

for _name, _frames in STRIKES.items():
    if _name.endswith("_lp"):
        _strike = "wing"
    elif _name.endswith("_hp"):
        _strike = "blade_arm"
    else:
        _strike = "front_leg"
    ANIMATIONS[_name] = {"fps": 20, "loop": False, "strike": [_strike], "frames": _frames}

# P2's alternate colours: the black feathers stay black (value too low to recolour), so P2 turns the grey
# coat a dusty brown and the red sash a deep blue.
P2_RULES = [
    {"hue": (180, 230), "sat_min": 0.08, "val_min": 0.25, "shift": -170, "sat": 1.6},
    {"hue": (350, 360), "sat_min": 0.35, "val_min": 0.3, "shift": -130, "sat": 1.0},
    {"hue": (0, 16), "sat_min": 0.35, "val_min": 0.3, "shift": 220, "sat": 1.0},
]
