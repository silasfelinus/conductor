"""River Croc's rig (zuzu-showdown t-012).

He is an animal on all fours (fighters.yaml look), so this rig is a quadruped's. Kontext drew him facing
left, so every source is mirrored (`mirror`) and the coordinates below are the mirrored images' pixels
(832 x 1216). The fighting stance (ArtImage 244352: low on all fours, jaws open, the harpoon in his back)
gives the moving parts: the head (LP snap, HP jaw lunge), the near front leg (claw swipes, the kicks) and
the tail; the body keeps his hind legs and the far legs. His bigger shapes are whole poses from the same
sheet, swapped in for the stance: flattened in the mud (crouch, 244358), leaping (244359), reared up on his
hind legs (244360) and rolled over (244361). Scale comes from the stance, so he stands his kit's 84 px.
The water, the swallow and the eruptions are the game's to draw.

Moves are timed with `timed`: at 20 fps each drawn frame covers three sim frames, so a move's active
frames always show its strike pose (sprites.ts pickSprite: index = (frame - 1) * fps / 60).
"""

from __future__ import annotations

HEIGHT = 84
PALETTE_COLOURS = 18
STANCE = 244352
CROUCH, LEAP, REAR, ROLLED = 244358, 244359, 244360, 244361
# Scale only, cropped above the shadow and the pebbles under his feet.
REFERENCE = {"art": STANCE, "mirror": True, "crop": (0, 0, 832, 852)}

NECK = (520, 470)
SHOULDER = (580, 630)
TAIL_ROOT = (170, 690)
# The fighter's spot on the ground: under the middle of his body, between his front and hind feet.
ANCHOR = (400, 840)


def whole(art, ground, polygon, z):
    """A whole-figure pose, placed so its own spot on the ground (`ground`) lands on ANCHOR."""
    return {"art": art, "mirror": True, "z": z, "pivot": ground, "follows": ["pose"], "polygon": polygon,
            "base": {"dx": ANCHOR[0] - ground[0], "dy": ANCHOR[1] - ground[1]}}


PARTS = {
    "tail": {"art": STANCE, "mirror": True, "z": 0, "pivot": TAIL_ROOT, "follows": ["body"],
             "polygon": [(8, 650), (80, 636), (170, 636), (196, 700), (160, 770), (112, 806), (30, 800),
                         (8, 724)]},
    # The trunk (not "body": that is the group every stance part follows).
    "trunk": {"art": STANCE, "mirror": True, "z": 1, "pivot": (400, 840), "follows": ["body"],
             "polygon": [(60, 130), (130, 130), (300, 380), (440, 340), (520, 380), (540, 470), (600, 520), (612, 590), (520, 640), (470, 700), (520, 760), (470, 840), (380, 830), (300, 800), (240, 856),
                         (100, 856), (110, 800), (150, 760), (196, 700), (170, 636), (200, 560), (240, 470)]},
    "front_leg": {"art": STANCE, "mirror": True, "z": 2, "pivot": SHOULDER, "follows": ["body"],
                  "polygon": [(520, 600), (600, 590), (650, 640), (670, 720), (680, 800), (650, 836), (590, 830),
                              (580, 780), (540, 740), (510, 680)]},
    "head": {"art": STANCE, "mirror": True, "z": 3, "pivot": NECK, "follows": ["body"],
             "polygon": [(470, 360), (540, 320), (640, 330), (760, 340), (792, 370), (760, 420), (700, 470),
                         (620, 500), (560, 520), (500, 500), (470, 440)]},
    # Whole poses: hidden unless a frame shows them (`pose_frames` below hides the others).
    "crouch_pose": whole(CROUCH, (420, 810), [(20, 120), (200, 120), (520, 300), (800, 300), (800, 975), (20, 975)], 4),
    "leap_pose": whole(LEAP, (450, 840), [(20, 120), (600, 120), (800, 200), (800, 860), (20, 860)], 5),
    "rear_pose": whole(REAR, (440, 1076), [(200, 90), (800, 90), (800, 1110), (200, 1110), (210, 940),
                                           (190, 900), (20, 900), (20, 600), (200, 560)], 6),
    "rolled_pose": whole(ROLLED, (450, 840), [(20, 120), (300, 120), (800, 300), (800, 880), (20, 880)], 7),
}

STANCE_PARTS = ["tail", "trunk", "front_leg", "head"]
POSES = ["crouch_pose", "leap_pose", "rear_pose", "rolled_pose"]

MEASURING = False  # set by rig.py while it measures reach


def merged(base: dict, more: dict) -> dict:
    out = {key: dict(value) if isinstance(value, dict) else value for key, value in base.items()}
    for key, value in more.items():
        out[key] = {**out.get(key, {}), **value} if isinstance(value, dict) else value
    return out


def stance(dy=0, snap=0, **more):
    """The stance's parts posed: the body dropped `dy`, the head turned `snap`, plus `more` per part. The
    whole poses are hidden."""
    return merged({"body": {"dy": dy}, "head": {"angle": snap}, "hide": POSES}, more)


def posed(name, angle=0, dx=0, dy=0, **more):
    """One whole pose shown alone (`crouch`, `leap`, `rear`, `rolled`), turned about its ground spot."""
    out = {"pose": {"angle": angle, "dx": dx, "dy": dy},
           "hide": STANCE_PARTS + [p for p in POSES if p != f"{name}_pose"]}
    return merged(out, more)


def fall(angle, pivot=(120, 840)):
    """The whole figure toppling (positive: over backwards about his tail end)."""
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
    # Standing LP: the snap, the head darting forward.
    "stand_lp": timed(4, 2, 6, stance(4, 6), stance(2, -4, head={"dx": 70}), stance(2, 2), stance(0)),
    # Standing HP: the big jaw lunge, the whole body thrown forward behind the head.
    "stand_hp": timed(8, 3, 16, stance(10, 10, body={"dx": -30}),
                      stance(-6, -8, body={"dx": 70}, head={"dx": 60}), stance(4, 4, body={"dx": 20}), stance(0)),
    # Standing LK: a claw swipe with the near forefoot.
    "stand_lk": timed(5, 3, 8, stance(4, front_leg={"angle": 14}),
                      stance(0, front_leg={"angle": 50, "dx": 30, "dy": -20}), stance(2, front_leg={"angle": 16}),
                      stance(0)),
    # Standing HK: a heavy raking claw, the forefoot raised high.
    "stand_hk": timed(10, 4, 18, stance(6, front_leg={"angle": 24}),
                      stance(-10, -6, body={"angle": -8}, front_leg={"angle": 78, "dx": 50, "dy": -60}),
                      stance(4, front_leg={"angle": 30}), stance(0)),
    "crouch_lp": timed(4, 2, 6, stance(40, 10, body={"angle": 4}),
                       stance(40, 0, body={"angle": 4}, head={"dx": 70, "dy": 20}), stance(40, 8, body={"angle": 4})),
    # Crouching LK: a claw along the mud.
    "crouch_lk": timed(5, 3, 8, stance(40, 8, front_leg={"angle": 10}),
                       stance(40, 8, front_leg={"angle": 40, "dx": 60, "dy": 10}), stance(40, 8)),
    # Crouching HP: the anti-air, the jaws snapped straight up.
    "crouch_hp": timed(7, 4, 16, stance(30, 10),
                       [stance(10, 30, head={"dy": -40}), stance(0, 50, head={"dy": -80, "dx": -20})],
                       stance(20, 10)),
    # Crouching HK: the low claw sweep.
    "crouch_hk": timed(9, 4, 20, stance(40, 8),
                       stance(50, 10, body={"angle": 6}, front_leg={"angle": 70, "dx": 70, "dy": 70}),
                       stance(40, 8, front_leg={"angle": 20})),
    "jump_lp": timed(4, 6, 4, stance(-20, 10), stance(-20, -16, head={"dx": 60, "dy": 30}), stance(-20, 10)),
    # Jumping HP: jaws first, coming down.
    "jump_hp": timed(7, 5, 6, stance(-20, 14), stance(-20, -30, head={"dx": 50, "dy": 80}), stance(-20, 0)),
    "jump_lk": timed(4, 8, 4, stance(-20), stance(-20, front_leg={"angle": 40, "dx": 30, "dy": 20}), stance(-20)),
    "jump_hk": timed(7, 5, 6, stance(-20, body={"angle": -10}),
                     stance(-20, body={"angle": -14}, front_leg={"angle": 60, "dx": 50, "dy": 30}), stance(-20)),
}

ANIMATIONS = {
    # Idle: still as a log, the breath rising and falling, the tail tip stirring.
    "idle": {"fps": 4, "loop": True, "frames": [stance(0), stance(-4, tail={"angle": 3}), stance(-6, tail={"angle": 5}),
                                                stance(-2, tail={"angle": 2})]},
    # Walking: a slow, heavy sprawl.
    "walk_forward": {"fps": 6, "loop": True, "frames": [
        stance(4, 2, front_leg={"angle": 14}, tail={"angle": 6}),
        stance(0, 0, front_leg={"angle": 4, "dy": -14}, tail={"angle": 0}),
        stance(4, -2, front_leg={"angle": -10}, tail={"angle": -5}),
        stance(0, 0, front_leg={"angle": -2}, tail={"angle": 0}),
    ]},
    "walk_back": {"fps": 6, "loop": True, "frames": [
        stance(4, front_leg={"angle": -10}, tail={"angle": -4}),
        stance(0, front_leg={"angle": 0, "dy": -14}),
        stance(4, front_leg={"angle": 10}, tail={"angle": 4}),
        stance(0, front_leg={"angle": 2}),
    ]},
    "crouch": {"fps": 12, "loop": False, "frames": [stance(30, 6), posed("crouch")]},
    "jump_up": {"fps": 12, "loop": False, "frames": [posed("crouch"), posed("leap"), posed("leap", -6)]},
    "land": {"fps": 20, "loop": False, "frames": [posed("crouch")]},
    "block_high": {"fps": 12, "loop": False, "frames": [stance(10, 20, body={"dx": -20}), stance(12, 24, body={"dx": -24})]},
    "block_low": {"fps": 12, "loop": False, "frames": [posed("crouch")]},
    "hit_high": {"fps": 14, "loop": False, "frames": [
        stance(8, 24, body={"dx": -30, "angle": -6}), stance(6, 16, body={"dx": -18, "angle": -4}),
        stance(2, 6, body={"dx": -6, "angle": -2})]},
    "hit_low": {"fps": 14, "loop": False, "frames": [
        stance(30, -10, body={"angle": 6}), stance(20, -6, body={"angle": 4}), stance(8, -2, body={"angle": 2})]},
    # Knockdown and KO (fighters.yaml): he rolls over, legs in the air.
    "knockdown": {"fps": 12, "loop": False, "frames": [
        stance(0, 20, body={"dx": -20, "angle": -8}), posed("rolled", 8), posed("rolled")]},
    "ko": {"fps": 8, "loop": False, "frames": [
        stance(0, 30, body={"angle": -10}), posed("rolled", 10), posed("rolled", 4), posed("rolled")]},
    "wakeup": {"fps": 12, "loop": False, "frames": [posed("rolled"), posed("crouch"), stance(10)]},
    "dodge_forward": {"fps": 13, "loop": False, "frames": [
        posed("crouch"), posed("crouch", dx=40), posed("crouch", dx=80), posed("crouch", dx=40), stance(10)]},
    "dodge_back": {"fps": 12, "loop": False, "frames": [
        stance(8, 10, body={"dx": -30}), stance(10, 14, body={"dx": -70}), stance(10, 14, body={"dx": -70}),
        stance(4, 4, body={"dx": -20})]},
    # Throws: the jaws take hold, then he shakes and flings.
    "throw": {"fps": 15, "loop": False, "frames": [stance(6, -6, head={"dx": 40}), stance(4, -10, head={"dx": 60})]},
    "throw_hold": {"fps": 8, "loop": False, "frames": [
        stance(4, -10, head={"dx": 60}), stance(0, 20, head={"dx": 40}), stance(0, -20, head={"dx": 40}),
        stance(4, 0)]},
    "throw_whiff": {"fps": 10, "loop": False, "frames": [stance(4, -10, head={"dx": 70}), stance(6, 6), stance(2)]},
    "thrown": {"fps": 15, "loop": False, "frames": [
        stance(-10, 20, body={"dx": 20, "angle": 8}), stance(-30, 24, body={"dx": 30, "angle": 14})]},
    # Death Roll: he seizes and rolls over and over.
    "death_roll": {"fps": 20, "loop": False, "frames": [
        stance(4, -10, head={"dx": 60}), posed("rolled", 0), posed("rolled", 0, dy=-20), stance(0, -6, head={"dx": 30}),
        posed("rolled", 0), posed("rolled", 0, dy=-20), stance(4)]},
    # Submerge: he sinks into the water (the game draws the surface over him).
    "submerge": {"fps": 12, "loop": False, "frames": [posed("crouch"), posed("crouch", dy=40), posed("crouch", dy=90)]},
    # Erupt: he bursts up out of the water, jaws wide.
    "erupt": {"fps": 20, "loop": False, "frames": [posed("crouch", dy=60), posed("leap"), posed("rear"), posed("rear")]},
    # Tail Sweep: he whips round, the tail scything low.
    "tail_sweep": {"fps": 20, "loop": False, "frames": [
        stance(20, tail={"angle": 20}), stance(30, tail={"angle": -30}), stance(30, tail={"angle": -60}),
        stance(20, tail={"angle": -20}), stance(0)]},
    # Bellow: reared up, roaring at the sky.
    "bellow": {"fps": 10, "loop": False, "frames": [stance(4, 10), posed("rear"), posed("rear", -2),
                                                    posed("rear", 2), posed("rear")]},
    # Swallow: the jaws close over them (the game hides the victim).
    "swallow": {"fps": 12, "loop": False, "frames": [stance(4, -10, head={"dx": 60}), stance(8, 10, head={"dx": 30}),
                                                     stance(10, 14), stance(4)]},
    # The Watering Hole: he rises out of the flood, reared and roaring.
    "the_watering_hole": {"fps": 10, "loop": False, "frames": [posed("crouch", dy=60), posed("leap"), posed("rear"),
                                                               posed("rear", -3), posed("rear")]},
    "taunt": {"fps": 6, "loop": False, "frames": [stance(0, -10), stance(-4, -24, head={"dy": -20}),
                                                  stance(-4, -26, head={"dy": -24}), stance(0)]},
    # Victory: sinks back until only the eyes remain, watching.
    "victory": {"fps": 4, "loop": False, "frames": [posed("crouch"), posed("crouch", dy=40), posed("crouch", dy=70)]},
    # Victory (the other): basks, jaws open in the sun.
    "victory_button": {"fps": 4, "loop": False, "frames": [stance(0, -10), stance(10, -20), stance(12, -24)]},
    # Perfect: doesn't move at all, for an uncomfortably long time.
    "perfect": {"fps": 2, "loop": False, "frames": [stance(0), stance(0), stance(0), stance(0)]},
    # Intro: rises from the shallows, water streaming off.
    "intro": {"fps": 4, "loop": False, "frames": [posed("crouch", dy=90), posed("crouch", dy=50), posed("crouch"),
                                                 stance(0)]},
}

for _name, _frames in STRIKES.items():
    _strike = "head" if _name.endswith(("_lp", "_hp")) else "front_leg"
    ANIMATIONS[_name] = {"fps": 20, "loop": False, "strike": [_strike], "frames": _frames}

# P2's alternate colours: his olive hide turns a muddy rust-brown (an older croc from another river).
P2_RULES = [
    {"hue": (50, 110), "sat_min": 0.12, "val_min": 0.2, "shift": -50, "sat": 1.2},
]
