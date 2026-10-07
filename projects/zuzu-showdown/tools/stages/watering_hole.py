"""The Watering Hole, the Coyote's and the croc's home stage (t-009): a low sun over the badlands, the
fenced pond, the street.

Art: T009-STAGES.yaml, Arthemy house lane. Backdrop wh-backdrop-1 (243061, bones on the plain; seed 2 drew
a lens streak through the sun). Every pond render added a longhorn despite the negative prompt, so the
midground is wh-pond-2 (243066) cut short of it at x 650 (between two fence posts) and closed with its mirror image: the fence and
the pond's left half, twice. Boxes and anchors are in source pixels of the 1536x640 renders; a point past
x 650 lands in the mirrored half (x 650 + d is the mirror of x 650 - d).
"""

SEED = 919
PALETTE_COLOURS = 40  # per layer

LAYERS = [
    {"name": "backdrop", "kind": "full", "art": 243061, "factor": 0.2, "height": 240, "top": 0},
    {
        "name": "pond",
        "kind": "keyed",
        "art": 243066,
        "crop": (40, 330, 650, 600),
        "mirror": True,
        "factor": 0.6,
        "height": 64,
        "bottom": 234,
    },
    {
        "name": "floor",
        "kind": "floor",
        "factor": 1.0,
        "top": 230,
        "colours": [(50, 34, 28), (84, 58, 44), (118, 84, 60)],
        "ruts": [11, 23],
    },
]

ANCHORS = {
    # The open water, both halves: glints, and the croc's eyes in fights the croc isn't in.
    "water": {"layer": "pond", "at": (310, 504, 990, 536)},
}
