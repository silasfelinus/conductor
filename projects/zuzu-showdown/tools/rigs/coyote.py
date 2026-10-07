"""The Coyote Vagrant's rig (zuzu-showdown t-010).

His body is cut from the t-010 parts sheet's fighting stance (ArtImage 242880: a crouched, wide stance
facing right, boots planted, coat hanging open). Coordinates are that image's pixels (832 x 1216); about
11 of them make one game pixel at his 104 px height, with scale from his standing reference (242404).

Post-croc (Silas, 2026-10-07): his right hand is gone and a knife is lashed to the bandaged stump.
Kontext drew the stance with a whole hand gripping the knife, so both arms are cut away and drawn in
code instead: the stump arm (near side, in front of the coat) and his left arm with the revolver he
fires left-handed and badly (far side, behind it).
"""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw

import sprite_common as sc

HEIGHT = 104
PALETTE_COLOURS = 16
REFERENCE = {"art": 242404}  # scale only
STANCE = 242880

NECK = (420, 280)
HIP_BACK = (220, 830)
HIP_FRONT = (460, 690)
SHOULDER_NEAR = (480, 340)
SHOULDER_FAR = (420, 330)
# The fighter's spot on the ground in the source art: midway between his boots.
ANCHOR = (400, 1170)

PARTS = {
    "back_leg": {"art": STANCE, "z": 1, "pivot": HIP_BACK, "follows": [],
                 "polygon": [(140, 816), (304, 816), (284, 940), (254, 1060), (236, 1172), (96, 1172), (116, 1060),
                             (148, 940)]},
    "front_leg": {"art": STANCE, "z": 2, "pivot": HIP_FRONT, "follows": [],
                  "polygon": [(380, 640), (560, 620), (604, 760), (594, 880), (644, 980), (784, 1080), (774, 1134),
                              (540, 1134), (526, 1000), (468, 920), (398, 840)]},
    "torso": {"art": STANCE, "z": 3, "pivot": HIP_FRONT, "follows": ["body"],
              "polygon": [(182, 280), (300, 248), (432, 256), (520, 326), (530, 420), (580, 520), (580, 700),
                          (560, 800), (470, 822), (420, 862), (150, 862), (128, 760), (140, 600), (160, 420),
                          (150, 330)]},
    "head": {"art": STANCE, "z": 4, "pivot": NECK, "follows": ["body"],
             "polygon": [(256, 90), (400, 42), (562, 78), (604, 200), (562, 242), (500, 262), (432, 302), (330, 302),
                         (280, 242), (256, 160)]},
}

INK = (20, 16, 14)
SLEEVE = (98, 117, 92)
SLEEVE_FAR = (52, 72, 46)
BANDAGE = (212, 203, 165)
FUR = (171, 153, 124)
STEEL = (196, 204, 214)
STEEL_EDGE = (246, 248, 250)
GUNMETAL = (58, 60, 66)
FLASH = (255, 236, 150)
FLASH_CORE = (255, 255, 236)
SAND = (214, 186, 128)
BUTTON = (190, 160, 110)


# The parts sheet's isolated left arm (ArtImage 242883): a horizontal coat sleeve, bandaged wrist and fist,
# fist to the left, with a loose knife lying across the lower sleeve (left out of both cuts). The same
# sleeve dresses both arms: whole for the gun hand, cut at the bandaged wrist for the stump.
ARM_ART = 242883
GUN_SLEEVE = [(36, 390), (190, 370), (270, 420), (330, 420), (700, 390), (745, 430), (745, 470), (640, 600),
              (590, 665), (330, 680), (270, 640), (150, 670), (36, 640)]
STUMP_SLEEVE = [(262, 430), (330, 420), (700, 390), (745, 430), (745, 470), (640, 600), (590, 665), (330, 680),
                (262, 630)]
SLEEVE_SHOULDER = (745, 545)
GUN_SLEEVE_HAND = (60, 520)
STUMP_SLEEVE_END = (262, 530)
SLEEVE_ACROSS = 0.27  # the sleeve is drawn ~290 px thick; on the body an arm is ~80
SOURCE_DIR: Path | None = None  # set by rig.py
_sleeves: dict[str, Image.Image] = {}


def _sleeve(kind: str) -> Image.Image | None:
    if kind not in _sleeves:
        path = SOURCE_DIR / f"{ARM_ART}.png" if SOURCE_DIR else None
        if not path or not path.exists():
            return None
        keyed = sc.key_background(Image.open(path).convert("RGB"))
        mask = Image.new("L", keyed.size, 0)
        ImageDraw.Draw(mask).polygon(GUN_SLEEVE if kind == "gun" else STUMP_SLEEVE, fill=255)
        part = Image.new("RGBA", keyed.size, (0, 0, 0, 0))
        part.paste(keyed, (0, 0), Image.composite(keyed.getchannel("A"), mask, mask))
        _sleeves[kind] = part
    return _sleeves[kind]


def _paste_limb(canvas, part, s_img, h_img, s_t, h_t) -> bool:
    """Lay `part` from its shoulder point s_img to its hand point h_img onto the canvas from s_t to
    h_t: stretched along the arm to reach, a fixed SLEEVE_ACROSS thick, mirrored when needed so the
    top of the sleeve stays on top."""
    if part is None:
        return False
    vix, viy = h_img[0] - s_img[0], h_img[1] - s_img[1]
    vtx, vty = h_t[0] - s_t[0], h_t[1] - s_t[1]
    li, lt = math.hypot(vix, viy), math.hypot(vtx, vty)
    if lt < 1:
        return False
    uix, uiy = vix / li, viy / li
    utx, uty = vtx / lt, vty / lt
    nix, niy = -uiy, uix
    ntx, nty = -uty, utx
    if (niy < 0) != (nty < 0):
        ntx, nty = -ntx, -nty
    along = lt / li
    across = SLEEVE_ACROSS
    st_u = s_t[0] * utx + s_t[1] * uty
    st_n = s_t[0] * ntx + s_t[1] * nty
    coeffs = (
        uix / along * utx + nix / across * ntx,
        uix / along * uty + nix / across * nty,
        s_img[0] - uix / along * st_u - nix / across * st_n,
        uiy / along * utx + niy / across * ntx,
        uiy / along * uty + niy / across * nty,
        s_img[1] - uiy / along * st_u - niy / across * st_n,
    )
    laid = part.transform(canvas.size, Image.Transform.AFFINE, coeffs, resample=Image.Resampling.BICUBIC)
    canvas.alpha_composite(laid)
    return True


def _limb(d, start, end, width, colour):
    d.line([start, end], fill=INK, width=width + 16)
    d.line([start, end], fill=colour, width=width)


def stump_arm(canvas, offset, hand, knife=0, dy=0):
    """His right arm: the coat sleeve, the bandaged stump, the knife lashed to it pointing `knife`
    degrees (0 = straight ahead, positive = up)."""
    s = (SHOULDER_NEAR[0] + offset[0], SHOULDER_NEAR[1] + offset[1] + dy)
    h = (hand[0] + offset[0], hand[1] + offset[1])
    d = ImageDraw.Draw(canvas)
    a = math.radians(knife)
    ux, uy = math.cos(a), -math.sin(a)
    # The knife goes down first so the bandaged stump sits over its lashed handle.
    tip = (h[0] + ux * 220, h[1] + uy * 220)
    d.line([h, tip], fill=INK, width=30)
    d.line([h, tip], fill=STEEL, width=16)
    d.line([(h[0] - uy * 4, h[1] + ux * 4), (tip[0] - uy * 4, tip[1] + ux * 4)], fill=STEEL_EDGE, width=5)
    if not _paste_limb(canvas, _sleeve("stump"), SLEEVE_SHOULDER, STUMP_SLEEVE_END, s, h):
        _limb(d, s, h, 66, SLEEVE)
        d.ellipse([h[0] - 34, h[1] - 34, h[0] + 34, h[1] + 34], fill=INK)
        d.ellipse([h[0] - 26, h[1] - 26, h[0] + 26, h[1] + 26], fill=BANDAGE)
    for k in (-14, 0, 14):  # the bandage wraps lashing the knife on
        cx, cy = h[0] + ux * (30 + k), h[1] + uy * (30 + k)
        d.line([(cx - uy * 24, cy + ux * 24), (cx + uy * 24, cy - ux * 24)], fill=BANDAGE, width=8)


def gun_arm(canvas, offset, hand, aim=0, flash=False, dy=0, holding="gun"):
    """His left arm on the far side, holding the revolver aimed `aim` degrees (`flash` fires it), or
    `holding="button"` (the one thing he found in the loser's pockets), or `"open"`."""
    s = (SHOULDER_FAR[0] + offset[0], SHOULDER_FAR[1] + offset[1] + dy)
    h = (hand[0] + offset[0], hand[1] + offset[1])
    if not _paste_limb(canvas, _sleeve("gun"), SLEEVE_SHOULDER, GUN_SLEEVE_HAND, s, h):
        d0 = ImageDraw.Draw(canvas)
        _limb(d0, s, h, 58, SLEEVE_FAR)
        d0.ellipse([h[0] - 30, h[1] - 30, h[0] + 30, h[1] + 30], fill=INK)
        d0.ellipse([h[0] - 22, h[1] - 22, h[0] + 22, h[1] + 22], fill=FUR)
    d = ImageDraw.Draw(canvas)
    if holding == "button":
        d.ellipse([h[0] - 18, h[1] - 64, h[0] + 18, h[1] - 28], fill=BUTTON, outline=INK, width=6)
        d.ellipse([h[0] - 8, h[1] - 52, h[0] - 2, h[1] - 46], fill=INK)
        d.ellipse([h[0] + 2, h[1] - 52, h[0] + 8, h[1] - 46], fill=INK)
        return
    if holding != "gun":
        return
    a = math.radians(aim)
    ux, uy = math.cos(a), -math.sin(a)
    muzzle = (h[0] + ux * 150, h[1] + uy * 150)
    d.line([h, muzzle], fill=INK, width=40)
    d.line([h, muzzle], fill=GUNMETAL, width=26)
    d.ellipse([h[0] + ux * 30 - 26, h[1] + uy * 30 - 26, h[0] + ux * 30 + 26, h[1] + uy * 30 + 26], fill=GUNMETAL,
              outline=INK, width=6)
    if flash:
        cx, cy = muzzle[0] + ux * 60, muzzle[1] + uy * 60
        for k in range(8):
            r = 110 if k % 2 == 0 else 55
            t = a + k * math.pi / 4
            d.line([(cx, cy), (cx + math.cos(t) * r, cy - math.sin(t) * r)], fill=FLASH, width=22)
        d.ellipse([cx - 40, cy - 40, cx + 40, cy + 40], fill=FLASH_CORE)


def sand(canvas, offset, origin, reach=1.0):
    """A thrown fistful of grit: a widening cone of grains."""
    d = ImageDraw.Draw(canvas)
    ox, oy = origin[0] + offset[0], origin[1] + offset[1]
    for i in range(36):
        t = (i * 37 % 100) / 100
        x = ox + 60 + t * 360 * reach
        y = oy - 40 + ((i * 53) % 90 - 45) * (0.4 + t * 1.6)
        r = 9 if i % 3 else 13
        d.ellipse([x - r, y - r, x + r, y + r], fill=SAND, outline=INK, width=3)


BEDROLL = (122, 98, 70)
BEDROLL_STRIPE = (164, 60, 48)


def bedroll(canvas, offset, box=None, heap=None):
    """His bedroll: a blanket over him from the shoulders down (`box`, in standing source pixels, so a
    whole-figure fall lays it over him lying down), or a kicked-off heap on the floor (`heap`: x0, x1)."""
    d = ImageDraw.Draw(canvas)
    if box:
        x0, y0, x1, y1 = (box[0] + offset[0], box[1] + offset[1], box[2] + offset[0], box[3] + offset[1])
        d.rounded_rectangle([x0, y0, x1, y1], radius=60, fill=BEDROLL, outline=INK, width=14)
        for k in (0.3, 0.38, 0.7, 0.78):
            y = y0 + (y1 - y0) * k
            d.line([(x0 + 10, y), (x1 - 10, y)], fill=BEDROLL_STRIPE, width=20)
    if heap:
        x0, x1 = heap[0] + offset[0], heap[1] + offset[0]
        floor = 1172 + offset[1]
        d.chord([x0, floor - 160, x1, floor + 160], 180, 360, fill=BEDROLL, outline=INK, width=14)
        d.line([(x0 + 60, floor - 60), (x1 - 60, floor - 80)], fill=BEDROLL_STRIPE, width=18)


def stump(hand, knife=0, dy=0):
    return {"fn": "stump_arm", "args": {"hand": hand, "knife": knife, "dy": dy}}


def gun(hand, aim=0, flash=False, dy=0, holding="gun"):
    return {"fn": "gun_arm", "args": {"hand": hand, "aim": aim, "flash": flash, "dy": dy, "holding": holding}}


BACK_BOOT = (170, 1172)


def fall(angle):
    """Toppling backwards about his back boot: positive angles tip the head to the left (behind him)."""
    return {"whole": {"angle": angle, "pivot": BACK_BOOT}}


def rest_arms(dy=0):
    """Both arms at rest, following the body down: the stump hanging at his side with the knife
    pointing at the ground, and his empty left hand behind him near the holster."""
    return {
        "draw": [stump((540, 600 + dy), knife=-75, dy=dy)],
        "draw_behind": [gun((390, 610 + dy), aim=-80, dy=dy, holding="open")],
    }


def slouch(dy=0, head=0, sway=0):
    return {"body": {"dy": dy, "angle": sway}, "head": {"dy": head}}


CROUCH_DY = 160


def _merge(pose, more):
    for key, value in more.items():
        pose[key] = {**pose.get(key, {}), **value} if isinstance(value, dict) else value
    return pose


def crouched(**more):
    """The crouch's held frame (each leg squashed about its own hip so both boots stay on the floor)."""
    return _merge({"body": {"dy": CROUCH_DY, "angle": 12},
                   "front_leg": {"sy": -0.33, "sx": 0.1, "dy": CROUCH_DY, "angle": 4},
                   "back_leg": {"sy": -0.47, "sx": 0.1, "dy": CROUCH_DY, "angle": -4}}, more)


def tucked(**more):
    """The top of the jump, knees drawn up under the coat."""
    return _merge({"body": {"angle": -8}, "front_leg": {"sy": -0.4, "angle": 6},
                   "back_leg": {"sy": -0.55, "angle": 18}}, more)


ANIMATIONS = {
    # A slouching, coughing sway rather than a guard: he fights like someone with nothing left to lose.
    "idle": {"fps": 7, "loop": True, "frames": [slouch(0), slouch(-6, -2, 1), slouch(-10, -4, 2), slouch(-6, -6, 1)]},
    "walk_forward": {"fps": 11, "loop": True, "frames": [
        {"front_leg": {"angle": 16}, "back_leg": {"angle": -14}, "body": {"dy": 6, "angle": 2}},
        {"front_leg": {"angle": 8}, "back_leg": {"angle": -6, "dy": -10}, "body": {"dy": 14, "angle": 2}},
        {"front_leg": {"angle": -4}, "back_leg": {"angle": 6, "dy": -20}, "body": {"dy": 0, "angle": 1}},
        {"front_leg": {"angle": -14}, "back_leg": {"angle": 14}, "body": {"dy": -10, "angle": 0}},
        {"front_leg": {"angle": -18}, "back_leg": {"angle": 16}, "body": {"dy": 6, "angle": 1}},
        {"front_leg": {"angle": -6, "dy": -20}, "back_leg": {"angle": 6}, "body": {"dy": 0, "angle": 2}},
    ]},
    # Each leg squashes about its hip by its own amount (back 340 px of leg, front 490) so both feet
    # rise the same 160 px, then the legs and body drop 160 px to put the feet back on the floor.
    "crouch": {"fps": 12, "loop": False, "frames": [
        {"body": {"dy": 80, "angle": 6}, "front_leg": {"sy": -0.16, "dy": 80}, "back_leg": {"sy": -0.24, "dy": 80}},
        {"body": {"dy": 160, "angle": 12}, "front_leg": {"sy": -0.33, "sx": 0.1, "dy": 160, "angle": 4},
         "back_leg": {"sy": -0.47, "sx": 0.1, "dy": 160, "angle": -4}},
    ]},
    "jump_up": {"fps": 12, "loop": False, "frames": [
        {"body": {"dy": 60}, "front_leg": {"sy": -0.11, "dy": 60}, "back_leg": {"sy": -0.19, "dy": 60}},
        # His front leg is cut long (from under the coat), so it barely rotates; the squash does the tuck.
        {"body": {"angle": -4}, "front_leg": {"sy": -0.32, "angle": 4}, "back_leg": {"sy": -0.45, "angle": 10}},
        {"body": {"angle": -8}, "front_leg": {"sy": -0.4, "angle": 6}, "back_leg": {"sy": -0.55, "angle": 18}},
    ]},
    "stand_hp": {"fps": 15, "loop": False, "strike": ["draw"], "frames": [
        {**slouch(10, 0, -4), "draw": [stump((250, 520), knife=30, dy=10)]},
        {**slouch(6, 0, 6), "front_leg": {"angle": 12}, "draw": [stump((560, 470), knife=4, dy=6)]},
        {**slouch(4, 0, 10), "front_leg": {"angle": 16}, "draw": [stump((700, 440), knife=0, dy=4)]},
        {**slouch(8, 0, 4), "draw": [stump((480, 500), knife=10, dy=8)]},
    ]},
    # Wild Shot: a left-handed draw, a shaky aim, the shot, the kick, the gun drifting down.
    "wild_shot": {"fps": 14, "loop": False, "frames": [
        {**slouch(4), "draw_behind": [gun((470, 640), aim=-60, dy=4)]},
        {**slouch(2, 0, -2), "draw_behind": [gun((640, 430), aim=4, dy=2)]},
        {**slouch(2, 0, -2), "draw_behind": [gun((660, 430), aim=2, flash=True, dy=2)]},
        {**slouch(0, -4, -6), "draw_behind": [gun((620, 380), aim=24, dy=0)]},
        {**slouch(4, 0, 0), "draw_behind": [gun((560, 520), aim=-20, dy=4)]},
    ]},
    "walk_back": {"fps": 9, "loop": True, "frames": [
        {"front_leg": {"angle": -6}, "back_leg": {"angle": 8}, "body": {"dy": 4, "angle": -2}},
        {"front_leg": {"angle": -2}, "back_leg": {"angle": 4, "dy": -14}, "body": {"dy": 10, "angle": -2}},
        {"front_leg": {"angle": 4}, "back_leg": {"angle": -4}, "body": {"dy": 0, "angle": -1}},
        {"front_leg": {"angle": 8, "dy": -14}, "back_leg": {"angle": -8}, "body": {"dy": 6, "angle": -2}},
    ]},
    # Blocks: the stump arm comes up across his face (high) or down across his shins (low, crouched).
    "block_high": {"fps": 12, "loop": False, "frames": [
        {**slouch(8, 0, -6), "draw": [stump((460, 280), knife=80, dy=8)]},
        {**slouch(12, 4, -8), "draw": [stump((450, 290), knife=84, dy=12)]},
    ]},
    "block_low": {"fps": 12, "loop": False, "frames": [
        {"body": {"dy": 160, "angle": 10}, "front_leg": {"sy": -0.33, "sx": 0.1, "dy": 160},
         "back_leg": {"sy": -0.47, "sx": 0.1, "dy": 160}, "draw": [stump((560, 700), knife=-24, dy=160)]},
    ]},
    # Hits: the head snaps back (high) or he folds over the blow (low).
    "hit_high": {"fps": 14, "loop": False, "frames": [
        {"body": {"dy": 10, "dx": -30, "angle": -16}, "head": {"angle": -22, "dx": -50}},
        {"body": {"dy": 8, "dx": -20, "angle": -11}, "head": {"angle": -14, "dx": -30}},
        {"body": {"dy": 4, "dx": -8, "angle": -4}, "head": {"angle": -5, "dx": -10}},
    ]},
    "hit_low": {"fps": 14, "loop": False, "frames": [
        {"body": {"dy": 60, "angle": 26}, "head": {"dy": 24, "dx": 40, "angle": 14}},
        {"body": {"dy": 40, "angle": 18}, "head": {"dy": 14, "dx": 26, "angle": 8}},
        {"body": {"dy": 14, "angle": 6}},
    ]},
    # Knocked down: he topples over backwards about his back boot and lands flat.
    "knockdown": {"fps": 12, "loop": False, "frames": [
        {**fall(20), "body": {"angle": -6}, "head": {"angle": -8}},
        {**fall(48), "body": {"angle": -4}},
        {**fall(76)},
        {**fall(90)},
    ]},
    # KO pose (fighters.yaml): flat on his back, the crushed hat over his face, one boot sole flapping.
    "ko": {"fps": 6, "loop": True, "frames": [
        {**fall(90), "head": {"angle": 18, "dx": 60}, "front_leg": {"angle": 4}},
        {**fall(90), "head": {"angle": 18, "dx": 60}, "front_leg": {"angle": -4}},
    ]},
    # Play Dead (dd+D): a fast flop flat; the parry window is the lying frames.
    "play_dead": {"fps": 16, "loop": False, "frames": [
        {**fall(40), "body": {"angle": -4}},
        {**fall(90)},
        {**fall(90), "front_leg": {"angle": 3}},
    ]},
    # Reload (dd+P): the revolver up to his chest, the stump fumbling shells in, a flick shut.
    "reload": {"fps": 10, "loop": False, "frames": [
        {**slouch(8, 4, 4), "draw_behind": [gun((520, 470), aim=80, dy=8)], "draw": [stump((430, 560), knife=-40, dy=8)]},
        {**slouch(10, 6, 6), "draw_behind": [gun((530, 460), aim=84, dy=10)], "draw": [stump((480, 500), knife=-20, dy=10)]},
        {**slouch(10, 6, 6), "draw_behind": [gun((530, 460), aim=84, dy=10)], "draw": [stump((470, 520), knife=-30, dy=10)]},
        {**slouch(4, 0, 0), "draw_behind": [gun((600, 420), aim=10, dy=4)]},
    ]},
    # Taunt (fighters.yaml): blows into his empty revolver chamber, frowns, pats his coat for bullets.
    # The gun arm comes round in front of him for the taunt and the victory, where it has to be seen.
    "taunt": {"fps": 8, "loop": False, "frames": [
        {**slouch(0, 0, -2), "draw": [gun((500, 300), aim=150)]},
        {**slouch(0, -4, -4), "draw": [gun((500, 290), aim=156)]},
        {**slouch(6, 4, 2), "draw": [stump((330, 600), knife=-60, dy=6)]},
        {**slouch(6, 4, 2), "draw": [stump((360, 520), knife=-60, dy=6)]},
    ]},
    # Victory (fighters.yaml): rifles the loser's pockets and holds up a single button, disgusted.
    "victory_button": {"fps": 6, "loop": False, "frames": [
        {**slouch(10, 6, 6), "draw": [gun((560, 640), dy=10, holding="open")]},
        {**slouch(0, -4, -4), "draw": [gun((580, 200), dy=0, holding="button")]},
        {**slouch(0, -8, -6), "draw": [gun((580, 190), dy=0, holding="button")]},
    ]},
    # Pocket Sand (4 frames to the fling): a dig in the coat pocket, then the fistful flung short, which
    # hangs in the air for the active frames.
    "pocket_sand": {"fps": 20, "loop": False, "strike": ["draw"], "frames": [
        {**slouch(14, 0, 4), "draw": [stump((300, 640), knife=-70, dy=14)]},
        {**slouch(4, 0, 8), "draw": [stump((600, 380), knife=10, dy=4),
                                     {"fn": "sand", "args": {"origin": (600, 380), "reach": 0.5}}]},
        {**slouch(4, 0, 8), "draw": [stump((600, 390), knife=4, dy=4),
                                     {"fn": "sand", "args": {"origin": (600, 380), "reach": 0.6}}]},
        {**slouch(6, 0, 4), "draw": [stump((540, 460), knife=-20, dy=6)]},
    ]},
    # The normals (frame counts from fighters/placeholders.ts: an animation spans the move's startup +
    # active + recovery at its fps, clamping on its last frame if the move runs longer).
    # Standing LP: a short poke with the stump knife.
    "stand_lp": {"fps": 15, "loop": False, "strike": ["draw"], "frames": [
        {**slouch(6, 0, 2), "draw": [stump((560, 470), knife=6, dy=6)]},
        {**slouch(4, 0, 6), "draw": [stump((660, 450), knife=2, dy=4)]},
        {**slouch(6, 0, 2), "draw": [stump((560, 480), knife=-6, dy=6)]},
    ]},
    # Standing LK: a boot to the shin.
    "stand_lk": {"fps": 15, "loop": False, "strike": ["front_leg"], "frames": [
        {**slouch(4, 0, -2), "front_leg": {"angle": 12, "dy": -10}},
        {**slouch(4, 0, -6), "front_leg": {"angle": 30, "dy": -24}},
        {**slouch(4, 0, -6), "front_leg": {"angle": 28, "dy": -20}},
        {**slouch(4, 0, -2), "front_leg": {"angle": 10, "dy": -6}},
    ]},
    # Standing HK: a big, graceless front kick, leaning way back to get the boot up.
    "stand_hk": {"fps": 12, "loop": False, "strike": ["front_leg"], "frames": [
        {**slouch(10, 0, 4), "front_leg": {"angle": -6}},
        {**slouch(0, 0, -8), "front_leg": {"angle": 30, "dy": -40}},
        {**slouch(-6, 0, -14), "front_leg": {"angle": 60, "dy": -70, "sy": 0.06}, "back_leg": {"angle": -4}},
        {**slouch(-6, 0, -14), "front_leg": {"angle": 62, "dy": -70, "sy": 0.06}, "back_leg": {"angle": -4}},
        {**slouch(4, 0, -6), "front_leg": {"angle": 26, "dy": -30}},
        slouch(8),
    ]},
    "crouch_lp": {"fps": 15, "loop": False, "strike": ["draw"], "frames": [
        crouched(draw=[stump((600, 660), knife=0, dy=CROUCH_DY)]),
        crouched(draw=[stump((700, 640), knife=-4, dy=CROUCH_DY)]),
        crouched(draw=[stump((600, 670), knife=-8, dy=CROUCH_DY)]),
    ]},
    # Crouching LK: a low stamp at the toes.
    "crouch_lk": {"fps": 15, "loop": False, "strike": ["front_leg"], "frames": [
        crouched(front_leg={"angle": 18}),
        crouched(front_leg={"angle": 6, "sy": -0.27, "dx": 20}),
        crouched(front_leg={"angle": 4, "sy": -0.27, "dx": 20}),
        crouched(front_leg={"angle": 14}),
    ]},
    # Crouching HP: the anti-air, the stump knife driven straight up on the active frames.
    "crouch_hp": {"fps": 13, "loop": False, "strike": ["draw"], "frames": [
        crouched(draw=[stump((460, 680), knife=-40, dy=CROUCH_DY)]),
        crouched(body={"angle": 2}, draw=[stump((570, 420), knife=84, dy=CROUCH_DY)]),
        crouched(body={"angle": 2}, draw=[stump((570, 420), knife=86, dy=CROUCH_DY)]),
        crouched(body={"angle": 4}, draw=[stump((560, 500), knife=60, dy=CROUCH_DY)]),
        crouched(draw=[stump((580, 560), knife=40, dy=CROUCH_DY)]),
        crouched(),
    ]},
    # Crouching HK: the sweep, low on the floor with the front boot swung out along it.
    "crouch_hk": {"fps": 12, "loop": False, "strike": ["front_leg"], "frames": [
        crouched(),
        crouched(body={"dy": 230, "angle": 14}, back_leg={"sy": -0.62, "dy": 230},
                 front_leg={"sy": -0.2, "sx": 0, "dy": 230, "angle": 40}),
        crouched(body={"dy": 250, "angle": 16}, back_leg={"sy": -0.66, "dy": 250},
                 front_leg={"sy": -0.06, "sx": 0, "dy": 250, "angle": 76}),
        crouched(body={"dy": 250, "angle": 16}, back_leg={"sy": -0.66, "dy": 250},
                 front_leg={"sy": -0.06, "sx": 0, "dy": 250, "angle": 78}),
        crouched(body={"dy": 200, "angle": 12}, back_leg={"sy": -0.56, "dy": 200},
                 front_leg={"sy": -0.24, "dy": 200, "angle": 36}),
        crouched(),
    ]},
    # Jumping LP: the stump knife jabbed down and forward at a standing opponent.
    "jump_lp": {"fps": 15, "loop": False, "strike": ["draw"], "frames": [
        tucked(draw=[stump((560, 500), knife=-20)]),
        tucked(draw=[stump((620, 560), knife=-40)]),
        tucked(draw=[stump((570, 520), knife=-30)]),
    ]},
    # Jumping HP: the stump knife driven down and forward.
    "jump_hp": {"fps": 12, "loop": False, "strike": ["draw"], "frames": [
        tucked(draw=[stump((520, 300), knife=50)]),
        tucked(body={"angle": 4}, draw=[stump((640, 560), knife=-50)]),
        tucked(body={"angle": 6}, draw=[stump((640, 580), knife=-56)]),
        tucked(),
    ]},
    # Jumping LK: the flying kick, boot first.
    "jump_lk": {"fps": 12, "loop": False, "strike": ["front_leg"], "frames": [
        tucked(),
        tucked(body={"angle": 6}, front_leg={"sy": -0.04, "angle": 5}, back_leg={"sy": -0.6, "angle": 10}),
        tucked(body={"angle": 6}, front_leg={"sy": -0.04, "angle": 7}, back_leg={"sy": -0.6, "angle": 10}),
        tucked(body={"angle": 2}, front_leg={"sy": -0.2, "angle": 30}),
    ]},
    # Jumping HK: both boots at once, a two-footed dropkick leaning right back.
    "jump_hk": {"fps": 12, "loop": False, "strike": ["front_leg", "back_leg"], "frames": [
        tucked(body={"angle": -12}),
        tucked(body={"angle": -18}, front_leg={"sy": 0.04, "angle": 45}, back_leg={"sy": -0.15, "angle": 40}),
        tucked(body={"angle": -18}, front_leg={"sy": 0.04, "angle": 47}, back_leg={"sy": -0.15, "angle": 42}),
        tucked(body={"angle": -10}, front_leg={"sy": -0.2, "angle": 30}),
    ]},
    "land": {"fps": 20, "loop": False, "frames": [
        {"body": {"dy": 80, "angle": 6}, "front_leg": {"sy": -0.16, "dy": 80}, "back_leg": {"sy": -0.24, "dy": 80}},
    ]},
    # Dodges: too long in the leg to tuck, he cartwheels forward (22 frames; the sim moves him), or
    # staggers back (18).
    "dodge_forward": {"fps": 13, "loop": False, "frames": [
        crouched(),
        {**crouched(), "whole": {"angle": -90, "pivot": (400, 860), "dy": 60}},
        {**crouched(), "whole": {"angle": -180, "pivot": (400, 860), "dy": -130}},
        {**crouched(), "whole": {"angle": -270, "pivot": (400, 860), "dy": 60}},
        crouched(),
    ]},
    "dodge_back": {"fps": 12, "loop": False, "frames": [
        {**slouch(8, 0, -6), "body": {"dy": 8, "dx": -20, "angle": -6}, "head": {"dx": -24}},
        {**slouch(10, 0, -12), "body": {"dy": 10, "dx": -60, "angle": -12}, "head": {"dx": -70, "angle": -8},
         "back_leg": {"angle": -10}},
        {**slouch(10, 0, -12), "body": {"dy": 10, "dx": -60, "angle": -12}, "head": {"dx": -70, "angle": -8},
         "back_leg": {"angle": -10}},
        {**slouch(6, 0, -4), "body": {"dy": 6, "dx": -20, "angle": -4}, "head": {"dx": -24}},
    ]},
    # Wake-up (20 frames): up off his back, through the crouch, into the slouch.
    "wakeup": {"fps": 12, "loop": False, "frames": [
        fall(70),
        fall(40),
        crouched(),
        slouch(10),
    ]},
    # Throws: his good hand grabs a fistful of collar (5 frames), then he swings them round and lets go
    # (30 frames); a whiffed grab clutches air (20 frames).
    "throw": {"fps": 15, "loop": False, "frames": [
        {**slouch(8, 0, 6), "draw_behind": [gun((620, 460), dy=8, holding="open")]},
        {**slouch(8, 0, 8), "draw_behind": [gun((720, 440), dy=8, holding="open")]},
    ]},
    "throw_hold": {"fps": 8, "loop": False, "frames": [
        {**slouch(8, 0, 8), "draw_behind": [gun((720, 440), dy=8, holding="open")]},
        {**slouch(20, 0, -12), "draw_behind": [gun((300, 260), dy=20, holding="open")]},
        {**slouch(24, 0, 12), "draw_behind": [gun((700, 520), dy=24, holding="open")]},
        slouch(10, 0, 4),
    ]},
    "throw_whiff": {"fps": 10, "loop": False, "frames": [
        {**slouch(10, 0, 12), "body": {"dy": 10, "angle": 12, "dx": 20}, "draw_behind": [gun((760, 470), dy=10, holding="open")]},
        {**slouch(14, 6, 14), "body": {"dy": 14, "angle": 14, "dx": 24}, "draw_behind": [gun((700, 560), dy=14, holding="open")]},
        slouch(6),
    ]},
    # Thrown: hauled up by the collar before the toss lands him (then the knockdown plays).
    "thrown": {"fps": 15, "loop": False, "frames": [
        {"body": {"dy": -10, "dx": 20, "angle": 10}, "head": {"angle": 14, "dx": 30},
         "front_leg": {"angle": 10}, "back_leg": {"angle": -10}},
        {"body": {"dy": -30, "dx": 30, "angle": 16}, "head": {"angle": 18, "dx": 40},
         "front_leg": {"angle": 16, "dy": -20}, "back_leg": {"angle": -14, "dy": -20}},
    ]},
    # Stump Shiv (charge b,f+P, 38 frames, 3 hits): a lunging flurry of stabs with the knife-stump.
    "stump_shiv": {"fps": 12, "loop": False, "strike": ["draw"], "frames": [
        {**slouch(10, 0, -6), "draw": [stump((300, 520), knife=10, dy=10)]},
        {**slouch(4, 0, 10), "front_leg": {"angle": 14}, "draw": [stump((720, 440), knife=0, dy=4)]},
        {**slouch(6, 0, 6), "front_leg": {"angle": 12}, "draw": [stump((520, 480), knife=6, dy=6)]},
        {**slouch(4, 0, 12), "front_leg": {"angle": 16}, "draw": [stump((740, 480), knife=-6, dy=4)]},
        {**slouch(6, 0, 6), "front_leg": {"angle": 12}, "draw": [stump((520, 460), knife=10, dy=6)]},
        {**slouch(2, 0, 14), "front_leg": {"angle": 18}, "draw": [stump((750, 420), knife=4, dy=2)]},
        {**slouch(8, 0, 4), "draw": [stump((560, 520), knife=-30, dy=8)]},
        slouch(6),
    ]},
    # Pick Pocket (HCB+K, 35 frames): the good hand darts into the opponent's coat and comes back with
    # some of their meter (the button is the joke; the meter is the theft).
    "pick_pocket": {"fps": 10, "loop": False, "strike": ["draw_behind"], "frames": [
        {**slouch(8, 0, 8), "draw_behind": [gun((640, 470), dy=8, holding="open")]},
        {**slouch(6, 0, 14), "body": {"dy": 6, "angle": 14, "dx": 20}, "draw_behind": [gun((780, 480), dy=6, holding="open")]},
        {**slouch(6, 0, 10), "draw": [gun((560, 330), dy=6, holding="button")]},
        {**slouch(4, -4, 2), "draw": [gun((540, 300), dy=4, holding="button")]},
    ]},
    # Last Meal (Lv1, 55 frames, 4 hits): a desperate rush of kicks, a bite and a headbutt, then he
    # collapses coughing.
    "last_meal": {"fps": 12, "loop": False, "strike": ["front_leg", "head"], "frames": [
        {**slouch(10, 0, 6)},
        {**slouch(0, 0, -8), "front_leg": {"angle": 40, "dy": -50}},
        {**slouch(4, 0, 2), "front_leg": {"angle": 10}},
        {**slouch(-4, 0, -12), "front_leg": {"angle": 56, "dy": -66, "sy": 0.04}, "back_leg": {"angle": -4}},
        {**slouch(6, 0, 4), "front_leg": {"angle": 14}},
        # the bite: lunging in with the muzzle
        {**slouch(10, 0, 16), "head": {"dx": 70, "dy": 20, "angle": -10}, "front_leg": {"angle": 16}},
        {**slouch(10, 0, 16), "head": {"dx": 80, "dy": 24, "angle": -14}, "front_leg": {"angle": 16}},
        # the headbutt
        {**slouch(0, -10, -10), "head": {"dx": -20, "dy": -10, "angle": 12}},
        {**slouch(16, 0, 22), "head": {"dx": 90, "dy": 40, "angle": -20}, "front_leg": {"angle": 18}},
        # the collapse: down on his heels, coughing
        crouched(head={"dy": 30, "angle": -16}),
        crouched(head={"dy": 40, "angle": -22}),
    ]},
    # Six Bad Shots (Lv3 Showdown, 55 frames): he empties the revolver left-handed, wildly: high, low, his
    # own boot, and the sixth (which the game ricochets round the stage).
    "six_bad_shots": {"fps": 11, "loop": False, "frames": [
        {**slouch(2, 0, -2), "draw_behind": [gun((640, 430), aim=4, dy=2)]},
        {**slouch(2, 0, -4), "draw_behind": [gun((650, 380), aim=30, flash=True, dy=2)]},
        {**slouch(0, -4, -8), "draw_behind": [gun((620, 300), aim=56, dy=0)]},
        {**slouch(4, 0, 2), "draw_behind": [gun((660, 520), aim=-24, flash=True, dy=4)]},
        {**slouch(6, 0, 6), "draw_behind": [gun((600, 640), aim=-70, flash=True, dy=6)], "front_leg": {"angle": 6}},
        {**slouch(-6, -6, -10), "draw_behind": [gun((640, 300), aim=70, flash=True, dy=-6)]},
        {**slouch(2, 0, -2), "draw_behind": [gun((660, 430), aim=10, flash=True, dy=2)]},
        {**slouch(2, 0, -2), "draw_behind": [gun((660, 430), aim=2, flash=True, dy=2)]},
        {**slouch(4, 0, 0), "draw_behind": [gun((620, 470), aim=-10, dy=4)]},
        {**slouch(6, 2, 2), "draw_behind": [gun((560, 540), aim=-30, dy=6)]},
    ]},
    # Intro (the 90-frame round intro, fighters.yaml): crawls out from under his bedroll, coughs, spits,
    # and squints with his one eye.
    "intro": {"fps": 4, "loop": False, "frames": [
        {**fall(90), "draw": [{"fn": "bedroll", "args": {"box": (90, 300, 640, 1180)}}]},
        crouched(head={"dy": 30, "angle": -14}, draw_behind=[{"fn": "bedroll", "args": {"heap": (-160, 300)}}]),
        crouched(head={"dy": 40, "angle": -24}, draw_behind=[{"fn": "bedroll", "args": {"heap": (-160, 300)}}]),
        {**slouch(10, 10, 4), "head": {"dy": 10, "dx": 40, "angle": -10},
         "draw_behind": [{"fn": "bedroll", "args": {"heap": (-160, 300)}}]},
        {**slouch(0, 0, 0), "head": {"angle": 6}, "draw_behind": [{"fn": "bedroll", "args": {"heap": (-160, 300)}}]},
        {**slouch(0, 0, 0), "head": {"angle": 6}, "draw_behind": [{"fn": "bedroll", "args": {"heap": (-160, 300)}}]},
    ]},
    # Perfect (fighters.yaml): tips his crushed hat with the knife-stump and limps off whistling.
    "perfect": {"fps": 6, "loop": False, "frames": [
        {**slouch(0, 0, -2), "draw": [stump((520, 220), knife=70)]},
        {**slouch(0, 4, -4), "head": {"angle": 6, "dy": 4}, "draw": [stump((540, 160), knife=84)]},
        {**slouch(0, 4, -4), "head": {"angle": 6, "dy": 4}, "draw": [stump((540, 170), knife=80)]},
        {"front_leg": {"angle": 10}, "back_leg": {"angle": -8}, "body": {"dy": 14, "angle": 4}},
        {"front_leg": {"angle": -6}, "back_leg": {"angle": 8, "dy": -14}, "body": {"dy": 0, "angle": 1}},
        {"front_leg": {"angle": 10}, "back_leg": {"angle": -8}, "body": {"dy": 14, "angle": 4}},
    ]},
}

# P2's alternate colours: the green riding coat turns maroon, everything else stays (the boots and hat
# are the same brown leather as P1, which keeps him readable as the same vagrant).
P2_RULES = [
    {"hue": (55, 125), "sat_min": 0.1, "shift": -115, "sat": 1.3},
]
