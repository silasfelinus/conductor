"""Old Komodo's rig (zuzu-showdown t-013).

Kontext drew him facing left, so every source is mirrored (`mirror`). Coordinates below are written in
the original images' pixels (832 x 1216) and mirrored by `m()`. The fighting stance (ArtImage 244654: a
wide stride on his hind legs, the gnarled staff raised in his near claw, the far claw on his belly, the
tail sweeping behind) gives the moving parts: the staff arm (LP staff jab, HP overhead smash), the head,
the near leg (the kicks), the far leg and the tail. His heavier shapes are whole poses from the same sheet:
crouched low (244660), leaping (244661) and slumped into the sand (244662, Sand Burrow and the KO).
Scale comes from the stance (cropped above the cast shadow), so he stands his kit's 120 px. The sand and
the venom are the game's to draw.

Moves are timed with `timed`: at 20 fps each drawn frame covers three sim frames, so a move's active
frames always show its strike pose (sprites.ts pickSprite: index = (frame - 1) * fps / 60).
"""

from __future__ import annotations

HEIGHT = 120
PALETTE_COLOURS = 20
STANCE = 244654
CROUCH, LEAP, SLUMPED = 244660, 244661, 244662
WIDTH_PX = 832


def m(points):
    """Original-image points to the mirrored image the rig cuts from."""
    if isinstance(points, tuple):
        return (WIDTH_PX - 1 - points[0], points[1])
    return [(WIDTH_PX - 1 - x, y) for x, y in points]


# Scale only, cropped above the cast shadow under his feet.
REFERENCE = {"art": STANCE, "mirror": True, "crop": (0, 0, 832, 1044)}

NECK = m((440, 430))
SHOULDER = m((395, 450))
HIP_FRONT = m((390, 790))
HIP_BACK = m((470, 810))
TAIL_ROOT = m((560, 780))
# The fighter's spot on the ground: midway between his feet.
ANCHOR = m((350, 1050))


def whole(art, ground, polygon, z):
    """A whole-figure pose (already in mirrored pixels), placed so its spot on the ground lands on ANCHOR."""
    return {"art": art, "mirror": True, "z": z, "pivot": ground, "follows": ["pose"], "polygon": polygon,
            "base": {"dx": ANCHOR[0] - ground[0], "dy": ANCHOR[1] - ground[1]}}


PARTS = {
    "tail": {"art": STANCE, "mirror": True, "z": 0, "pivot": TAIL_ROOT, "follows": ["body"],
             "polygon": m([(480, 700), (560, 740), (700, 740), (760, 690), (790, 560), (790, 436), (832, 436),
                           (832, 600), (812, 762), (722, 822), (560, 834), (480, 802)])},
    "back_leg": {"art": STANCE, "mirror": True, "z": 1, "pivot": HIP_BACK, "follows": [],
                 "polygon": m([(400, 796), (520, 796), (560, 858), (642, 908), (662, 950), (642, 998), (528, 998),
                               (556, 960), (518, 940), (450, 902), (410, 924), (400, 860)])},
    "torso": {"art": STANCE, "mirror": True, "z": 2, "pivot": HIP_FRONT, "follows": ["body"],
              "polygon": m([(300, 400), (400, 428), (500, 438), (582, 498), (614, 600), (582, 652), (562, 722),
                            (562, 792), (480, 804), (400, 804), (330, 762), (248, 742), (226, 680), (238, 600),
                            (310, 500)])},
    "front_leg": {"art": STANCE, "mirror": True, "z": 3, "pivot": HIP_FRONT, "follows": [],
                  "polygon": m([(220, 736), (330, 726), (482, 758), (472, 832), (380, 842), (300, 862), (252, 962),
                                (212, 1022), (192, 1058), (28, 1058), (38, 1028), (118, 1008), (168, 950),
                                (200, 850)])},
    "head": {"art": STANCE, "mirror": True, "z": 4, "pivot": NECK, "follows": ["body"],
             "polygon": m([(290, 298), (330, 282), (420, 286), (482, 318), (502, 380), (482, 430), (430, 442),
                           (390, 422), (300, 392), (248, 396), (252, 338), (284, 328)])},
    "staff_arm": {"art": STANCE, "mirror": True, "z": 5, "pivot": SHOULDER, "follows": ["body"],
                  "polygon": m([(168, 146), (398, 146), (398, 262), (332, 298), (302, 330), (312, 400), (402, 428),
                                (412, 502), (330, 512), (270, 472), (236, 452), (206, 492), (166, 488), (198, 400),
                                (194, 320)])},
    # Whole poses, in mirrored pixels: hidden unless a frame shows them.
    "crouch_pose": whole(CROUCH, (400, 1040), [(20, 300), (812, 300), (812, 1034), (20, 1034)], 6),
    "leap_pose": whole(LEAP, (500, 900), [(20, 120), (820, 120), (820, 950), (20, 950)], 7),
    "slumped_pose": whole(SLUMPED, (600, 900), [(130, 400), (830, 400), (830, 990), (130, 990)], 8),
}

STANCE_PARTS = ["tail", "back_leg", "torso", "front_leg", "head", "staff_arm"]
POSES = ["crouch_pose", "leap_pose", "slumped_pose"]

MEASURING = False  # set by rig.py while it measures reach


def merged(base: dict, more: dict) -> dict:
    out = {key: dict(value) if isinstance(value, dict) else value for key, value in base.items()}
    for key, value in more.items():
        out[key] = {**out.get(key, {}), **value} if isinstance(value, dict) else value
    return out


def stance(dy=0, tilt=0, staff=0, **more):
    """The stance's parts posed: the body dropped `dy`, the head tilted, the staff arm turned, plus `more`
    per part. The whole poses are hidden."""
    return merged({"body": {"dy": dy}, "head": {"angle": tilt}, "staff_arm": {"angle": staff}, "hide": POSES},
                  more)


def posed(name, angle=0, dx=0, dy=0, **more):
    """One whole pose shown alone (`crouch`, `leap`, `slumped`), turned about its ground spot."""
    out = {"pose": {"angle": angle, "dx": dx, "dy": dy},
           "hide": STANCE_PARTS + [p for p in POSES if p != f"{name}_pose"]}
    return merged(out, more)


CROUCH_DY = 160


def crouched(**more):
    """Down low on the stance parts (for crouching attacks): the body drops onto squashed legs."""
    return merged(stance(), merged({"body": {"dy": CROUCH_DY, "angle": 6},
                                    "front_leg": {"sy": -0.4, "sx": 0.1, "dy": CROUCH_DY},
                                    "back_leg": {"sy": -0.4, "sx": 0.1, "dy": CROUCH_DY},
                                    "staff_arm": {"angle": -10}}, more))


def tucked(**more):
    """In the air on the stance parts (for jumping attacks): legs drawn up."""
    return merged(stance(), merged({"body": {"angle": -6}, "front_leg": {"sy": -0.45, "angle": 24, "dy": -60},
                                    "back_leg": {"sy": -0.45, "angle": -14, "dy": -60}, "tail": {"angle": -14}},
                                   more))


def fall(angle, pivot=(120, 1050)):
    """The whole figure toppling (positive: over backwards)."""
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


# The staff (raised up and back in the stance) swung clockwise: level for the jab, down for the smash.
JAB = -62
SMASH = -110

STRIKES = {
    # Standing LP: the staff jab, the butt driven forward.
    "stand_lp": timed(4, 2, 6, stance(4, staff=-20), stance(2, staff=JAB, staff_arm={"dx": 70}),
                      stance(4, staff=-30), stance(0)),
    # Standing HP: the overhead staff smash (slow, armored).
    "stand_hp": timed(11, 3, 16, stance(-6, -6, 20, body={"angle": -6}),
                      stance(10, 8, SMASH - 10, body={"angle": 12, "dx": 80}, staff_arm={"dx": 40}),
                      stance(10, staff=-90), stance(2)),
    "stand_lk": timed(5, 3, 8, stance(4, front_leg={"angle": -16}),
                      stance(2, body={"angle": -6}, front_leg={"angle": 30, "dy": -40, "dx": 40}),
                      stance(4, front_leg={"angle": 6}), stance(0)),
    "stand_hk": timed(13, 4, 18, stance(8, front_leg={"angle": -10}),
                      stance(-4, body={"angle": -10, "dx": -10}, front_leg={"angle": 54, "dy": -60, "dx": 50}),
                      stance(4, front_leg={"angle": 14, "dy": -20}), stance(0)),
    "crouch_lp": timed(4, 2, 6, crouched(staff_arm={"angle": -30}),
                       crouched(staff_arm={"angle": JAB, "dx": 70, "dy": CROUCH_DY}), crouched()),
    "crouch_lk": timed(5, 3, 8, crouched(front_leg={"sy": -0.4, "sx": 0.1, "dy": CROUCH_DY, "angle": 10}),
                       crouched(front_leg={"sy": 0.0, "sx": 0, "dy": CROUCH_DY + 20, "angle": 40, "dx": 60}),
                       crouched()),
    # Crouching HP: the staff swung straight up.
    "crouch_hp": timed(10, 4, 16, crouched(staff_arm={"angle": 0}),
                       [crouched(staff_arm={"angle": 14, "dy": 80}), crouched(staff_arm={"angle": 24, "dy": 20})],
                       crouched()),
    "crouch_hk": timed(12, 4, 20, crouched(),
                       crouched(body={"dy": 200, "angle": 10}, front_leg={"sy": 0.1, "sx": 0, "dy": 220, "dx": 30,
                                                                         "angle": 50}),
                       crouched()),
    "jump_lp": timed(4, 6, 4, tucked(), tucked(staff_arm={"angle": JAB - 20, "dx": 70, "dy": 80}), tucked()),
    "jump_hp": timed(10, 5, 6, tucked(staff_arm={"angle": 20}), tucked(staff_arm={"angle": SMASH - 20, "dy": 140,
                                                                                  "dx": 60}),
                     tucked()),
    "jump_lk": timed(4, 8, 4, tucked(), tucked(front_leg={"sy": 0.0, "angle": 40, "dy": 0, "dx": 30}), tucked()),
    "jump_hk": timed(10, 5, 6, tucked(body={"angle": -10}),
                     tucked(body={"angle": -12}, front_leg={"sy": 0.1, "angle": 54, "dx": 50, "dy": 20}), tucked()),
}

ANIMATIONS = {
    "idle": {"fps": 4, "loop": True, "frames": [stance(0), stance(-4, 2, 2, tail={"angle": 3}),
                                                stance(-6, 3, 3, tail={"angle": 5}), stance(-2, 1, 1)]},
    "walk_forward": {"fps": 5, "loop": True, "frames": [
        stance(6, 2, 4, front_leg={"angle": 10}, back_leg={"angle": -8}, tail={"angle": 4}),
        stance(0, 0, 2, front_leg={"angle": 2}, back_leg={"angle": 0, "dy": -16}),
        stance(6, -2, -2, front_leg={"angle": -10}, back_leg={"angle": 10}, tail={"angle": -4}),
        stance(0, 0, 0, front_leg={"angle": -2, "dy": -16}, back_leg={"angle": 2}),
    ]},
    "walk_back": {"fps": 5, "loop": True, "frames": [
        stance(4, front_leg={"angle": -8}, back_leg={"angle": 10}), stance(0, front_leg={"angle": 0, "dy": -14}),
        stance(4, front_leg={"angle": 8}, back_leg={"angle": -8}), stance(0, back_leg={"angle": 0, "dy": -14}),
    ]},
    "crouch": {"fps": 12, "loop": False, "frames": [stance(30), posed("crouch")]},
    "jump_up": {"fps": 12, "loop": False, "frames": [posed("crouch"), posed("leap"), posed("leap", -6)]},
    "land": {"fps": 20, "loop": False, "frames": [posed("crouch")]},
    "block_high": {"fps": 12, "loop": False, "frames": [stance(8, -4, 30, body={"angle": -4}),
                                                        stance(10, -6, 36, body={"angle": -5})]},
    "block_low": {"fps": 12, "loop": False, "frames": [posed("crouch")]},
    "hit_high": {"fps": 14, "loop": False, "frames": [
        stance(8, -14, 20, body={"dx": -30, "angle": -10}), stance(6, -8, 12, body={"dx": -18, "angle": -6}),
        stance(2, -3, 4, body={"dx": -6, "angle": -2})]},
    "hit_low": {"fps": 14, "loop": False, "frames": [
        stance(40, 10, -20, body={"angle": 12}), stance(26, 6, -12, body={"angle": 8}), stance(10, 2, -4)]},
    "knockdown": {"fps": 12, "loop": False, "frames": [stance(0, -10, 20, body={"angle": -8}), posed("slumped", -6),
                                                       posed("slumped")]},
    # KO (fighters.yaml): he slumps down into the sand with a long, rumbling sigh.
    "ko": {"fps": 6, "loop": False, "frames": [stance(20, 10, -30), posed("crouch"), posed("slumped", -4),
                                               posed("slumped")]},
    "wakeup": {"fps": 10, "loop": False, "frames": [posed("slumped"), posed("crouch"), stance(10)]},
    "dodge_forward": {"fps": 13, "loop": False, "frames": [posed("crouch"), posed("crouch", dx=40), posed("crouch", dx=80),
                                                           posed("crouch", dx=40), stance(10)]},
    "dodge_back": {"fps": 12, "loop": False, "frames": [
        stance(8, -4, 10, body={"dx": -30}), stance(10, -6, 14, body={"dx": -70}), stance(10, -6, 14, body={"dx": -70}),
        stance(4, -2, 4, body={"dx": -20})]},
    "throw": {"fps": 15, "loop": False, "frames": [stance(6, 6, -30, head={"dx": 30}), stance(4, 8, -40, head={"dx": 50})]},
    "throw_hold": {"fps": 8, "loop": False, "frames": [stance(4, 8, -40, head={"dx": 50}), stance(0, -10, 30),
                                                       stance(0, 10, -60), stance(4)]},
    "throw_whiff": {"fps": 10, "loop": False, "frames": [stance(4, 8, -40, head={"dx": 60}), stance(6, 4), stance(2)]},
    "thrown": {"fps": 15, "loop": False, "frames": [stance(-10, 14, 30, body={"dx": 20, "angle": 8}),
                                                    stance(-30, 18, 40, body={"dx": 30, "angle": 14})]},
    # Venom Bite: a lunging bite, the head darting in.
    "venom_bite": {"fps": 20, "loop": False, "frames": timed(
        12, 4, 24, stance(8, 10, body={"dx": -20}), stance(-4, -8, body={"dx": 60}, head={"dx": 70, "dy": 20}),
        stance(4, 4, body={"dx": 20}), stance(0))},
    # Sand Burrow: he sinks into the sand (the game draws the ridge he leaves).
    "sand_burrow": {"fps": 12, "loop": False, "frames": [posed("crouch"), posed("slumped"), posed("slumped", dy=60),
                                                         posed("slumped", dy=140)]},
    # Rise from the Dune: he erupts from below, mouth open.
    "rise_from_the_dune": {"fps": 20, "loop": False, "frames": timed(
        4, 6, 28, posed("crouch", dy=60), posed("leap"), stance(4, -10, 20), stance(0))},
    # Tongue Taste: the long tongue flicks out and pulls them in.
    "tongue_taste": {"fps": 20, "loop": False, "frames": timed(
        10, 6, 24, stance(4, 6), stance(2, -6, head={"dx": 60}), stance(4, 4), stance(0))},
    # Old Staff: the armored rising swing.
    "old_staff": {"fps": 20, "loop": False, "frames": timed(
        6, 6, 26, stance(10, 6, -40), [stance(0, -6, 10), stance(-6, -10, 30)], stance(4, 0, 10), stance(0))},
    "slow_hunger": {"fps": 20, "loop": False, "frames": timed(
        8, 36, 30, stance(8, 10), [stance(-4, -8, head={"dx": 70, "dy": 20}, body={"dx": 40}), stance(4, 6),
                                    stance(-4, -8, head={"dx": 70, "dy": 20}, body={"dx": 40})], stance(4), stance(0))},
    "feeding_time": {"fps": 20, "loop": False, "frames": timed(
        6, 4, 50, posed("slumped", dy=100), posed("leap"), stance(4, -12, 30), stance(0))},
    "taunt": {"fps": 6, "loop": False, "frames": [stance(0, -10), stance(-4, -20, 10), stance(-4, -22, 10), stance(0)]},
    # Victory: settles down in the sun, eyes closed, licking his lips.
    "victory": {"fps": 4, "loop": False, "frames": [stance(0), posed("crouch"), posed("crouch")]},
    # Victory (the other): leans on his staff and yawns, enormously.
    "victory_button": {"fps": 4, "loop": False, "frames": [stance(0, 0, -20), stance(4, -16, -24), stance(4, -20, -24)]},
    # Perfect: falls asleep standing up.
    "perfect": {"fps": 2, "loop": False, "frames": [stance(0), stance(4, 10, -10), stance(6, 14, -14), stance(6, 16, -14)]},
    "intro": {"fps": 4, "loop": False, "frames": [posed("slumped", dy=120), posed("slumped", dy=60), posed("crouch"),
                                                 stance(0)]},
}

for _name, _frames in STRIKES.items():
    _strike = "staff_arm" if _name.endswith(("_lp", "_hp")) else "front_leg"
    ANIMATIONS[_name] = {"fps": 20, "loop": False, "strike": [_strike], "frames": _frames}

# P2's alternate colours: his grey-brown hide turns a dusty desert red.
P2_RULES = [
    {"hue": (20, 70), "sat_min": 0.05, "val_min": 0.25, "shift": -30, "sat": 2.2},
]
