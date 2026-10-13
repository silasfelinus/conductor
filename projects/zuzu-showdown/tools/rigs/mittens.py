"""Jeffery Mittens's rig (zuzu-showdown t-032).

Built like the Swamp Witch's (t-028): the parts sheet's fighting stance (STANCE) is cut into moving parts,
the legs, the coat and body with its string of boots, the near arm with the little knife (LP, Little
Knife, Tied Laces), the far arm raised behind him with a boot to throw (HP, Boot Toss), and the head, and
his bigger shapes are whole poses from the same sheet: crouched low (CROUCH), leaping (JUMP), the Underfoot
slide (SLIDE) and knocked flat under his own boots (DOWN, the KO). Scale comes from the stance, so he
stands his kit's 88 px. Thrown boots and the jackals of the dry well are the game's to draw.

Moves are timed with `timed`: at 20 fps each drawn frame covers three sim frames, so a move's active
frames always show its strike pose (sprites.ts pickSprite: index = (frame - 1) * fps / 60).
"""

from __future__ import annotations

HEIGHT = 88
PALETTE_COLOURS = 20
# Filled from art/T032-MITTENS-PARTS.yaml once it renders.
STANCE = 0
CROUCH, JUMP, SLIDE, DOWN = 0, 0, 0, 0
REFERENCE = {"art": STANCE}  # scale only

NECK = (0, 0)
NEAR_SHOULDER = (0, 0)
FAR_SHOULDER = (0, 0)
HIP_BACK = (0, 0)
HIP_FRONT = (0, 0)
# The fighter's spot on the ground: midway between his boots.
ANCHOR = (0, 0)


def whole(art, ground, polygon, z):
    """A whole-figure pose, placed so its own spot on the ground lands on ANCHOR."""
    return {"art": art, "z": z, "pivot": ground, "follows": ["pose"], "polygon": polygon,
            "base": {"dx": ANCHOR[0] - ground[0], "dy": ANCHOR[1] - ground[1]}}


PARTS: dict = {}

STANCE_PARTS = ["far_arm", "back_leg", "front_leg", "torso", "head", "near_arm"]
POSES = ["crouch_pose", "jump_pose", "slide_pose", "down_pose"]

MEASURING = False  # set by rig.py while it measures reach


def merged(base: dict, more: dict) -> dict:
    out = {key: dict(value) if isinstance(value, dict) else value for key, value in base.items()}
    for key, value in more.items():
        out[key] = {**out.get(key, {}), **value} if isinstance(value, dict) else value
    return out


def stance(dy=0, tilt=0, near=0, far=0, **more):
    """The stance's parts posed: the body dropped `dy`, the head tilted, the knife (near) and boot (far)
    arms turned, plus `more` per part. The whole poses are hidden."""
    return merged({"body": {"dy": dy}, "head": {"angle": tilt}, "near_arm": {"angle": near},
                   "far_arm": {"angle": far}, "hide": POSES}, more)


def posed(name, angle=0, dx=0, dy=0, sy=0, sx=0, **more):
    """One whole pose shown alone (`crouch`, `jump`, `slide`, `down`), about its ground spot."""
    out = {"pose": {"angle": angle, "dx": dx, "dy": dy, "sy": sy, "sx": sx},
           "hide": STANCE_PARTS + [p for p in POSES if p != f"{name}_pose"]}
    return merged(out, more)


CROUCH_DY = 150


def crouched(**more):
    """Low on the stance parts (for crouching attacks): legs squashed about the hips, the body dropped."""
    return merged(stance(), merged({"body": {"dy": CROUCH_DY, "angle": 4},
                                    "front_leg": {"sy": -0.35, "sx": 0.1, "dy": CROUCH_DY},
                                    "back_leg": {"sy": -0.35, "sx": 0.1, "dy": CROUCH_DY}}, more))


def tucked(**more):
    """In the air on the stance parts (for jumping attacks): knees drawn up under the coat."""
    return merged(stance(), merged({"body": {"angle": -6}, "front_leg": {"sy": -0.45, "angle": 22},
                                    "back_leg": {"sy": -0.45, "angle": -4}}, more))


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


# The knife arm jabs forward and down (clockwise); the boot arm, raised behind him, swings over the top
# and through (the throw, the HP shove).
JAB = -30
THROW = -140


def kick(leg="front_leg", angle=50, dx=40, dy=-20, sy=0.1):
    return {leg: {"angle": angle, "dx": dx, "dy": dy, "sy": sy}}


STRIKES = {
    "stand_lp": ("near_arm", timed(4, 2, 6, stance(4, near=10), stance(2, near=JAB, near_arm={"dx": 50}),
                                   stance(2, near=-6), stance(0))),
    "stand_hp": ("far_arm", timed(8, 3, 16, stance(-4, -4, far=30), stance(6, 6, far=THROW, far_arm={"dx": 160},
                                                                           body={"dx": 20, "angle": 6}),
                                  stance(4, far=-30), stance(0))),
    "stand_lk": ("front_leg", timed(5, 3, 8, stance(4), merged(stance(4, body={"angle": -6}), kick(angle=40)),
                                    stance(2), stance(0))),
    "stand_hk": ("front_leg", timed(10, 4, 18, stance(8), merged(stance(0, body={"angle": -12}),
                                                                 kick(angle=80, dx=90, dy=-40, sy=0.2)),
                                    stance(4), stance(0))),
    "crouch_lp": ("near_arm", timed(4, 2, 6, crouched(), crouched(near_arm={"angle": JAB - 10, "dx": 50}),
                                    crouched())),
    "crouch_lk": ("front_leg", timed(5, 3, 8, crouched(),
                                     crouched(front_leg={"sy": 0.1, "sx": 0, "angle": 50, "dx": 40}), crouched())),
    "crouch_hp": ("near_arm", timed(7, 4, 16, crouched(), crouched(near_arm={"angle": 70, "dy": -40}),
                                    crouched())),
    "crouch_hk": ("front_leg", timed(9, 4, 20, crouched(),
                                     crouched(front_leg={"sy": 0.25, "sx": 0, "angle": 84, "dx": 100}),
                                     crouched())),
    "jump_lp": ("near_arm", timed(4, 6, 4, tucked(), tucked(near_arm={"angle": JAB - 20, "dx": 40}), tucked())),
    "jump_hp": ("far_arm", timed(7, 5, 6, tucked(), tucked(far_arm={"angle": THROW - 10, "dx": 160, "dy": 80}),
                                 tucked())),
    "jump_lk": ("front_leg", timed(4, 8, 4, tucked(), tucked(front_leg={"sy": 0.05, "angle": 18}), tucked())),
    "jump_hk": ("front_leg", timed(7, 5, 6, tucked(body={"angle": -12}),
                                   tucked(body={"angle": -14}, front_leg={"sy": 0.2, "angle": 24, "dx": 80}),
                                   tucked())),
}

ANIMATIONS = {
    # Idle: bouncing on his toes, the knife twitching, eyes everywhere.
    "idle": {"fps": 8, "loop": True, "frames": [stance(0), stance(-8, -2, 4, 4), stance(-12, -3, 6, 6),
                                                stance(-6, -2, 2, 2)]},
    "walk_forward": {"fps": 12, "loop": True, "frames": [
        stance(4, front_leg={"angle": 10}, back_leg={"angle": -8}),
        stance(-6, front_leg={"angle": 2}, back_leg={"angle": 2, "dy": -14}),
        stance(4, front_leg={"angle": -8}, back_leg={"angle": 10}),
        stance(-6, front_leg={"angle": 2, "dy": -14}, back_leg={"angle": 2}),
    ]},
    "walk_back": {"fps": 10, "loop": True, "frames": [
        stance(4, 2, front_leg={"angle": -6}, back_leg={"angle": 8}),
        stance(-4, 2, front_leg={"angle": 2, "dy": -12}),
        stance(4, 2, front_leg={"angle": 8}, back_leg={"angle": -6}),
        stance(-4, 2, back_leg={"angle": 2, "dy": -12}),
    ]},
    "crouch": {"fps": 12, "loop": False, "frames": [crouched(), posed("crouch")]},
    "jump_up": {"fps": 12, "loop": False, "frames": [posed("crouch"), posed("jump"), posed("jump", -4)]},
    "land": {"fps": 20, "loop": False, "frames": [posed("crouch")]},
    "block_high": {"fps": 12, "loop": False, "frames": [stance(8, -8, 60, 20), stance(10, -10, 66, 24)]},
    "block_low": {"fps": 12, "loop": False, "frames": [posed("crouch")]},
    "hit_high": {"fps": 14, "loop": False, "frames": [
        stance(8, -16, 30, 30, body={"dx": -30, "angle": -10}), stance(6, -10, 20, 20, body={"dx": -18, "angle": -6}),
        stance(2, -4, 6, 6, body={"dx": -6, "angle": -2})]},
    "hit_low": {"fps": 14, "loop": False, "frames": [
        crouched(body={"dy": CROUCH_DY, "angle": 14}), crouched(body={"dy": CROUCH_DY, "angle": 8}), stance(20)]},
    "knockdown": {"fps": 12, "loop": False, "frames": [stance(20, -14, 40, 40, body={"angle": -14}),
                                                       posed("down", 20, dy=-120), posed("down")]},
    # KO (fighters.yaml): sits down hard; the string of boots lands on top of him, one by one.
    "ko": {"fps": 6, "loop": False, "frames": [stance(40, 10, -20, 30), posed("crouch"), posed("down", 10, dy=-40),
                                               posed("down")]},
    "wakeup": {"fps": 10, "loop": False, "frames": [posed("down"), posed("crouch"), stance(20)]},
    "dodge_forward": {"fps": 13, "loop": False, "frames": [posed("crouch"), posed("slide"), posed("slide", dx=40),
                                                           posed("crouch"), stance(10)]},
    "dodge_back": {"fps": 12, "loop": False, "frames": [
        stance(8, -4, 20, 20, body={"dx": -30}), stance(10, -6, 30, 30, body={"dx": -70}),
        stance(10, -6, 30, 30, body={"dx": -70}), stance(4, -2, 6, 6, body={"dx": -20})]},
    "throw": {"fps": 15, "loop": False, "frames": [stance(6, 4, JAB, near_arm={"dx": 40}),
                                                   stance(8, 6, JAB - 10, near_arm={"dx": 60})]},
    "throw_hold": {"fps": 8, "loop": False, "frames": [stance(8, 6, JAB - 10, near_arm={"dx": 60}),
                                                       stance(20, -10, 40, 40, body={"angle": -12}),
                                                       stance(20, 10, -50, -60, body={"angle": 10}), stance(4)]},
    "throw_whiff": {"fps": 10, "loop": False, "frames": [stance(4, 8, JAB, near_arm={"dx": 70}),
                                                         stance(8, 6, body={"dx": 20, "angle": 10}), stance(2)]},
    "thrown": {"fps": 15, "loop": False, "frames": [stance(-10, 14, 30, 30, body={"dx": 20, "angle": 8}),
                                                    stance(-30, 18, 40, 40, body={"dx": 30, "angle": 14})]},
    # Boot Toss: the boot arm winds back and throws overarm (the game draws the boot in flight).
    "boot_toss": {"fps": 20, "loop": False, "frames": timed(
        12, 1, 18, stance(-6, -6, far=40), stance(8, 8, far=THROW, far_arm={"dx": 160}, body={"angle": 8}),
        stance(4, far=-30), stance(0))},
    # Scavenge: he crouches and snatches boots up off the ground onto the string.
    "scavenge": {"fps": 12, "loop": False, "frames": [crouched(near_arm={"angle": -60}), posed("crouch"),
                                                      crouched(far_arm={"angle": -40}), stance(10)]},
    # Underfoot: the slide, feet first along the ground and out the other side.
    "underfoot": {"fps": 20, "loop": False, "frames": timed(
        6, 14, 14, posed("crouch"), [posed("slide"), posed("slide", dy=4)], posed("crouch"), stance(10))},
    # Ledge Drop: from the leap, both boots first, straight down on them.
    "ledge_drop": {"fps": 20, "loop": False, "frames": timed(
        5, 22, 10, posed("jump"), posed("jump", 20), posed("crouch"))},
    # Tied Laces: he dives at their feet with the knife arm and comes up with the laces knotted.
    "tied_laces": {"fps": 20, "loop": False, "frames": timed(
        6, 3, 22, stance(10), crouched(near_arm={"angle": JAB - 40, "dx": 70}), crouched(), stance(6))},
    # Little Knife: a rising slash, the knife arm swung up overhead as he hops.
    "little_knife": {"fps": 20, "loop": False, "frames": timed(
        4, 8, 26, crouched(), [stance(-20, -6, 40, near_arm={"dy": -30}), stance(-30, -8, 90, near_arm={"dy": -60})],
        stance(4, near=30), stance(0))},
    # Weren't Me: he flinches back behind his own arms, the knife held out by accident.
    "werent_me": {"fps": 12, "loop": False, "frames": [stance(14, -14, 50, 50, body={"angle": -8, "dx": -20}),
                                                       stance(14, -14, 50, 50, body={"angle": -8, "dx": -20}),
                                                       stance(6, -4, 10, 10)]},
    # Every Last Boot: the whole string swung round on its laces as he scrambles forward.
    "every_last_boot": {"fps": 20, "loop": False, "frames": timed(
        5, 24, 28, stance(-4, far=40),
        [stance(6, far=THROW, far_arm={"dx": 140}), stance(4, far=-60, far_arm={"dx": 120}),
         stance(6, far=60, far_arm={"dx": 40}), stance(4, far=THROW, far_arm={"dx": 140})],
        stance(4, far=-20), stance(0))},
    # The Dry Well Pack: two fingers to his mouth, the whistle, and he ducks as the pack goes through.
    "the_dry_well_pack": {"fps": 12, "loop": False, "frames": [
        stance(-6, -10, 80, near_arm={"dy": -60}), stance(-6, -12, 84, near_arm={"dy": -60}), posed("crouch"),
        posed("crouch"), stance(4), stance(0)]},
    # Taunt: holds a boot up against the opponent's foot, squints, shakes his head. Wrong size.
    "taunt": {"fps": 6, "loop": False, "frames": [stance(0, 0, far=-90, far_arm={"dx": 120}),
                                                  stance(0, 6, far=-90, far_arm={"dx": 120}),
                                                  stance(0, -6, far=-90, far_arm={"dx": 120}), stance(0)]},
    # Victory: counts the boots on his string, loses count, starts again.
    "victory": {"fps": 5, "loop": False, "frames": [stance(0, 10, 40), stance(0, 12, 50), stance(0, 10, 40),
                                                    stance(0, -4, 0)]},
    # Victory (the other): laces the loser's boots back up properly (crouched, working).
    "victory_button": {"fps": 4, "loop": False, "frames": [crouched(near_arm={"angle": -50}),
                                                          crouched(near_arm={"angle": -40}), stance(0)]},
    # Perfect: pulls on a fresh pair, stamps twice, grins.
    "perfect": {"fps": 6, "loop": False, "frames": [posed("crouch"), stance(0, 6, front_leg={"dy": -30}),
                                                   stance(0, 6), stance(0, 6, back_leg={"dy": -30}), stance(0, -4)]},
    # Intro: drops off a ledge, boots thumping round his neck, and pulls the little knife.
    "intro": {"fps": 4, "loop": False, "frames": [posed("jump", dy=-200), posed("crouch"), stance(10, near=40),
                                                 stance(0)]},
}

for _name, (_strike, _frames) in STRIKES.items():
    ANIMATIONS[_name] = {"fps": 20, "loop": False, "strike": [_strike], "frames": _frames}

# P2's alternate colours: the brown coat turns a faded denim blue and the grey-green vest a rust red.
P2_RULES = [
    {"hue": (15, 45), "sat_min": 0.2, "val_min": 0.2, "shift": 190, "sat": 0.8},
    {"hue": (70, 170), "sat_min": 0.08, "val_min": 0.15, "shift": -110, "sat": 1.6},
]
