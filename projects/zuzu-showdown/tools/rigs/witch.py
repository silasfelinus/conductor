"""The Swamp Witch's rig (zuzu-showdown t-028).

Parts are cut from the t-028 parts sheet's stance (ArtImage 244663: she rises on her coil facing the
viewer, turned a little to her left, both gnarled hands raised and dripping, bottles and bone charms
hanging from the moss shawl). She is drawn facing the viewer rather than side-on, which suits her: the
avatar does not turn to face anyone. The moving parts are the hood and head, her near hand (LP, the slap),
her raised far hand (HP, the clawed lash) and the coil (the kicks are the coil lashing out); the shawl
and its charms stay with the body. Her bigger shapes are whole poses from the same sheet: sunk into her
coil (crouch, 244667), rising (244668), half sunk into the mud (Sink, 244669) and melted into a puddle
waving her white rag (244670, the KO). Scale comes from the stance, so she stands her kit's 120 px. The
tentacles from the mud, the leech and the Door are the game's to draw.

Moves are timed with `timed`: at 20 fps each drawn frame covers three sim frames, so a move's active
frames always show its strike pose (sprites.ts pickSprite: index = (frame - 1) * fps / 60).
"""

from __future__ import annotations

HEIGHT = 120
PALETTE_COLOURS = 22
STANCE = 244663
CROUCH, RISE, SUNK, PUDDLE = 244667, 244668, 244669, 244670
REFERENCE = {"art": STANCE, "crop": (0, 0, 832, 1150)}  # scale only, above the cast shadow

NECK = (450, 400)
NEAR_SHOULDER = (560, 470)
FAR_SHOULDER = (290, 450)
COIL_ROOT = (420, 880)
# The fighter's spot on the ground: under the middle of her coil.
ANCHOR = (400, 1146)


def whole(art, ground, polygon, z):
    """A whole-figure pose, placed so its own spot on the ground lands on ANCHOR."""
    return {"art": art, "z": z, "pivot": ground, "follows": ["pose"], "polygon": polygon,
            "base": {"dx": ANCHOR[0] - ground[0], "dy": ANCHOR[1] - ground[1]}}


PARTS = {
    "coil": {"art": STANCE, "z": 0, "pivot": COIL_ROOT, "follows": [],
             "polygon": [(110, 900), (240, 850), (420, 860), (600, 850), (690, 920), (690, 1100), (600, 1150),
                         (420, 1166), (220, 1150), (100, 1110)]},
    "far_arm": {"art": STANCE, "z": 1, "pivot": FAR_SHOULDER, "follows": ["body"],
                "polygon": [(118, 196), (204, 192), (266, 246), (262, 330), (244, 398), (290, 430), (300, 480),
                            (252, 524), (196, 522), (186, 470), (150, 330), (118, 282)]},
    "torso": {"art": STANCE, "z": 2, "pivot": COIL_ROOT, "follows": ["body"],
              "polygon": [(250, 380), (420, 360), (560, 380), (620, 470), (640, 560), (690, 640), (700, 860),
                          (620, 900), (420, 920), (230, 900), (170, 860), (140, 640), (140, 540), (200, 520),
                          (250, 470)]},
    "near_arm": {"art": STANCE, "z": 3, "pivot": NEAR_SHOULDER, "follows": ["body"],
                 "polygon": [(540, 440), (620, 466), (660, 430), (690, 398), (742, 368), (792, 380), (792, 470),
                             (762, 520), (732, 640), (700, 684), (680, 562), (640, 562), (560, 562), (540, 520)]},
    "head": {"art": STANCE, "z": 4, "pivot": NECK, "follows": ["body"],
             "polygon": [(250, 260), (300, 160), (380, 90), (450, 54), (540, 90), (600, 120), (640, 160),
                         (620, 210), (560, 210), (530, 260), (540, 340), (520, 400), (450, 420), (380, 400),
                         (300, 380), (260, 330)]},
    "crouch_pose": whole(CROUCH, (420, 1125), [(20, 60), (820, 60), (820, 1146), (20, 1146)], 5),
    "rise_pose": whole(RISE, (420, 1120), [(100, 50), (800, 50), (800, 1150), (100, 1150)], 6),
    "sunk_pose": whole(SUNK, (470, 1130), [(30, 60), (810, 60), (810, 1152), (30, 1152)], 7),
    "puddle_pose": whole(PUDDLE, (470, 1130), [(10, 50), (820, 50), (820, 1154), (10, 1154)], 8),
}

STANCE_PARTS = ["coil", "far_arm", "torso", "near_arm", "head"]
POSES = ["crouch_pose", "rise_pose", "sunk_pose", "puddle_pose"]

MEASURING = False  # set by rig.py while it measures reach


def merged(base: dict, more: dict) -> dict:
    out = {key: dict(value) if isinstance(value, dict) else value for key, value in base.items()}
    for key, value in more.items():
        out[key] = {**out.get(key, {}), **value} if isinstance(value, dict) else value
    return out


def stance(dy=0, tilt=0, near=0, far=0, **more):
    """The stance's parts posed: the body sunk `dy`, the head tilted, the near (slap) and far (lash) arms
    turned, plus `more` per part. The whole poses are hidden."""
    return merged({"body": {"dy": dy}, "head": {"angle": tilt}, "near_arm": {"angle": near},
                   "far_arm": {"angle": far}, "hide": POSES}, more)


def posed(name, angle=0, dx=0, dy=0, sy=0, **more):
    """One whole pose shown alone (`crouch`, `rise`, `sunk`, `puddle`), about its ground spot."""
    out = {"pose": {"angle": angle, "dx": dx, "dy": dy, "sy": sy},
           "hide": STANCE_PARTS + [p for p in POSES if p != f"{name}_pose"]}
    return merged(out, more)


CROUCH_DY = 220


def crouched(**more):
    """Sunk low into her coil on the stance parts (for crouching attacks): the coil squashed."""
    # The coil squashes about its root, which lifts its underside; it is set back down on the ground.
    return merged(stance(), merged({"body": {"dy": CROUCH_DY}, "coil": {"sy": -0.3, "sx": 0.08, "dy": 86}}, more))


def risen(**more):
    """Rising into the air on the stance parts (for jumping attacks): the coil drawn up."""
    return merged(stance(), merged({"body": {"angle": -4}, "coil": {"sy": -0.35, "dy": -80}}, more))


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


# The near (slap) hand, raised beside her in the stance, swung clockwise down and forward; the far
# hand, raised on the other side, swung over the top and through (the lash).
SLAP = -50
LASH = -150


def coil_lash(dx, dy=0, sx=0.35, angle=0):
    """The coil lashing out low along the ground: stretched toward the opponent."""
    return {"coil": {"sx": sx, "dx": dx, "dy": dy, "angle": angle}}


STRIKES = {
    "stand_lp": timed(4, 2, 6, stance(4, near=20), stance(2, near=SLAP, near_arm={"dx": 60}), stance(2, near=-10),
                      stance(0)),
    "stand_hp": timed(8, 3, 16, stance(-4, -6, far=30), stance(6, 8, far=LASH, far_arm={"dx": 260, "dy": 30},
                                                               body={"dx": 20}),
                      stance(4, far=-40), stance(0)),
    "stand_lk": timed(5, 3, 8, stance(4), merged(stance(6), coil_lash(90, 0, 0.3)), stance(2), stance(0)),
    "stand_hk": timed(10, 4, 18, stance(4), merged(stance(10), coil_lash(150, -20, 0.5, 6)), stance(4), stance(0)),
    "crouch_lp": timed(4, 2, 6, crouched(), crouched(near_arm={"angle": SLAP - 10, "dx": 60}), crouched()),
    "crouch_lk": timed(5, 3, 8, crouched(), merged(crouched(), coil_lash(100, 86, 0.35)), crouched()),
    "crouch_hp": timed(7, 4, 16, crouched(), [crouched(far_arm={"angle": -40, "dx": 120, "dy": -40}),
                                              crouched(far_arm={"angle": -60, "dx": 200, "dy": -80})], crouched()),
    "crouch_hk": timed(9, 4, 20, crouched(), merged(crouched(), coil_lash(170, 90, 0.6)), crouched()),
    "jump_lp": timed(4, 6, 4, risen(), risen(near_arm={"angle": SLAP - 30, "dx": 60, "dy": 120}), risen()),
    "jump_hp": timed(7, 5, 6, risen(), risen(far_arm={"angle": LASH - 20, "dx": 260, "dy": 200}), risen()),
    "jump_lk": timed(4, 8, 4, risen(), merged(risen(), coil_lash(80, -40, 0.3, 14)), risen()),
    "jump_hk": timed(7, 5, 6, risen(), merged(risen(), coil_lash(130, -40, 0.5, 18)), risen()),
}

ANIMATIONS = {
    # Idle: she sways on her coil, the hands curling, the charms swinging.
    "idle": {"fps": 5, "loop": True, "frames": [stance(0), stance(-6, 2, 4, -4, coil={"sx": 0.02}),
                                                stance(-10, 3, 6, -6, coil={"sx": 0.03}), stance(-4, 1, 2, -2)]},
    # Walking: a slow glide on the coil.
    "walk_forward": {"fps": 6, "loop": True, "frames": [
        stance(0, 2, coil={"sx": 0.04, "dx": 6}), stance(-6, 0, coil={"sx": 0.02}),
        stance(0, -2, coil={"sx": -0.02, "dx": -6}), stance(-6, 0, coil={"sx": 0.0})]},
    "walk_back": {"fps": 6, "loop": True, "frames": [
        stance(0, -2, coil={"sx": -0.02, "dx": -6}), stance(-6, 0), stance(0, 2, coil={"sx": 0.04, "dx": 6}),
        stance(-6, 0)]},
    "crouch": {"fps": 12, "loop": False, "frames": [stance(60), posed("crouch", sy=-0.18)]},
    "jump_up": {"fps": 12, "loop": False, "frames": [posed("crouch", sy=-0.18), posed("rise"), posed("rise", -4)]},
    "land": {"fps": 20, "loop": False, "frames": [posed("crouch", sy=-0.18)]},
    "block_high": {"fps": 12, "loop": False, "frames": [stance(8, -6, 40, 30), stance(10, -8, 46, 34)]},
    "block_low": {"fps": 12, "loop": False, "frames": [posed("crouch", sy=-0.18)]},
    "hit_high": {"fps": 14, "loop": False, "frames": [
        stance(8, -14, 30, 20, body={"dx": -30, "angle": -8}), stance(6, -8, 20, 12, body={"dx": -18, "angle": -5}),
        stance(2, -3, 6, 4, body={"dx": -6, "angle": -2})]},
    "hit_low": {"fps": 14, "loop": False, "frames": [
        stance(60, 10, -20, -20, body={"angle": 8}), stance(40, 6, -12, -12, body={"angle": 5}), stance(14, 2)]},
    "knockdown": {"fps": 12, "loop": False, "frames": [stance(20, -10, 30, 30, body={"angle": -10}), posed("sunk"),
                                                       posed("puddle")]},
    # KO (fighters.yaml): she melts into a puddle with a long bubbling croak, one tentacle waving a white rag.
    "ko": {"fps": 6, "loop": False, "frames": [stance(30, 10, -20, -20), posed("sunk"), posed("puddle", sy=-0.05),
                                               posed("puddle")]},
    "wakeup": {"fps": 10, "loop": False, "frames": [posed("puddle"), posed("sunk"), stance(20)]},
    "dodge_forward": {"fps": 13, "loop": False, "frames": [posed("sunk"), posed("sunk", dx=40, dy=40),
                                                           posed("sunk", dx=80, dy=40), posed("sunk", dx=40),
                                                           stance(10)]},
    "dodge_back": {"fps": 12, "loop": False, "frames": [
        stance(8, -4, 10, 10, body={"dx": -30}), stance(10, -6, 14, 14, body={"dx": -70}),
        stance(10, -6, 14, 14, body={"dx": -70}), stance(4, -2, 4, 4, body={"dx": -20})]},
    "throw": {"fps": 15, "loop": False, "frames": [stance(6, 6, SLAP, near_arm={"dx": 40}),
                                                   merged(stance(4, 8, SLAP, near_arm={"dx": 60}), coil_lash(60))]},
    "throw_hold": {"fps": 8, "loop": False, "frames": [merged(stance(4, 8, SLAP, near_arm={"dx": 60}), coil_lash(60)),
                                                       stance(0, -10, 30, 30), stance(0, 10, -60, -60), stance(4)]},
    "throw_whiff": {"fps": 10, "loop": False, "frames": [stance(4, 8, SLAP, near_arm={"dx": 70}), stance(6, 4),
                                                         stance(2)]},
    "thrown": {"fps": 15, "loop": False, "frames": [stance(-10, 14, 30, 30, body={"dx": 20, "angle": 8}),
                                                    stance(-30, 18, 40, 40, body={"dx": 30, "angle": 14})]},
    # Bog Grasp: she lowers a hand toward the mud where the tentacle rises (the game draws it).
    "bog_grasp": {"fps": 20, "loop": False, "frames": timed(
        16, 6, 24, stance(8, 6, -60, 10), stance(14, 10, -80, 10), stance(6, 4, -40), stance(0))},
    # Leech Hex: she flicks the glob from her near hand (the game draws it in flight).
    "leech_hex": {"fps": 20, "loop": False, "frames": timed(
        18, 1, 26, stance(-4, -6, 40), stance(4, 6, SLAP, near_arm={"dx": 50}), stance(2, near=-10), stance(0))},
    # Sink: she melts into the mud and surfaces under them.
    "sink": {"fps": 12, "loop": False, "frames": [posed("sunk"), posed("sunk", dy=80), posed("sunk", dy=160),
                                                  posed("sunk", dy=160), posed("sunk", dy=80), posed("sunk"),
                                                  stance(20)]},
    # Coil Snare: the coil lunges and wraps them.
    "coil_snare": {"fps": 20, "loop": False, "frames": timed(
        6, 2, 32, stance(6), merged(stance(10, 6, SLAP, near_arm={"dx": 40}), coil_lash(80)), stance(4), stance(0))},
    # Bargain: she holds out the little bottle, patiently.
    "bargain": {"fps": 12, "loop": False, "frames": [stance(0, 6, SLAP + 10, near_arm={"dx": 40}),
                                                     stance(0, 8, SLAP + 10, near_arm={"dx": 50}),
                                                     stance(0, 8, SLAP + 10, near_arm={"dx": 50}), stance(0)]},
    # Drowning Pool: both hands raised as the tentacles rise in a line (the game draws them).
    "drowning_pool": {"fps": 20, "loop": False, "frames": timed(
        8, 30, 30, stance(-6, -10, 30, -20), [stance(-10, -14, 50, -40), stance(-8, -12, 40, -30)], stance(4),
        stance(0))},
    # The Door Below: she points down at their feet, and the mud opens (the game draws the Door).
    "the_door_below": {"fps": 20, "loop": False, "frames": timed(
        6, 4, 50, stance(-6, -12, 40, -40), stance(10, 14, -90, 20), stance(6, 6, -60), stance(0))},
    # Taunt: she rattles her bottle charms and croaks, "Bargain?"
    "taunt": {"fps": 8, "loop": False, "frames": [stance(0, 6, -10), stance(2, 10, -20, body={"angle": 4}),
                                                  stance(2, 6, -10, body={"angle": -4}), stance(0)]},
    # Victory: corks a little bottle with something glowing inside and tucks it away.
    "victory": {"fps": 5, "loop": False, "frames": [stance(0, 4, SLAP + 10, near_arm={"dx": 40}), stance(2, 8, -20),
                                                    stance(2, 6, 10)]},
    # Victory (the other): sinks back into the mud, waving, until only her eyes remain.
    "victory_button": {"fps": 4, "loop": False, "frames": [stance(0, 0, 20, -20), posed("sunk"),
                                                          posed("sunk", dy=60)]},
    # Perfect: she doesn't speak. Just holds out a bottle, patiently.
    "perfect": {"fps": 2, "loop": False, "frames": [stance(0, 6, SLAP + 10, near_arm={"dx": 40}),
                                                   stance(0, 8, SLAP + 10, near_arm={"dx": 50}),
                                                   stance(0, 8, SLAP + 10, near_arm={"dx": 50}),
                                                   stance(0, 8, SLAP + 10, near_arm={"dx": 50})]},
    # Intro: she rises out of a puddle that wasn't there, wringing out her hair.
    "intro": {"fps": 4, "loop": False, "frames": [posed("sunk", dy=160), posed("sunk", dy=80), posed("sunk"),
                                                 stance(0)]},
}

for _name, _frames in STRIKES.items():
    if _name.endswith("_lp"):
        _strike = "near_arm"
    elif _name.endswith("_hp"):
        _strike = "far_arm"
    else:
        _strike = "coil"
    ANIMATIONS[_name] = {"fps": 20, "loop": False, "strike": [_strike], "frames": _frames}

# P2's alternate colours: her moss shawl turns a drowned grey-blue and the violet coil a deep sea green.
P2_RULES = [
    {"hue": (60, 110), "sat_min": 0.2, "val_min": 0.15, "shift": 120, "sat": 0.7},
    {"hue": (260, 320), "sat_min": 0.15, "val_min": 0.1, "shift": -120, "sat": 1.0},
]
