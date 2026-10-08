"""The Thin Place, the boss's stage (t-009): a sky coming apart over dark ground, and a door standing alone.

Art: T009D-STAGES.yaml. The backdrop is tp-backdrop-2 (243161, a dark column dropping out of the sky; seed 1 drew
a volcano), the midground tp-door-1 (243162, a door in its frame with nothing around it). The tears of light
across the sky, the floating debris and the light at the door's edge (it widens round by round) are code.
Boxes and anchors are in source pixels of the 1536x640 renders.
"""

SEED = 969
PALETTE_COLOURS = 40  # per layer

LAYERS = [
    {"name": "backdrop", "kind": "full", "art": 243161, "factor": 0.2, "height": 240, "top": 0},
    {"name": "door", "kind": "keyed", "art": 243162, "factor": 0.6, "height": 120, "bottom": 234},
    {
        "name": "floor",
        "kind": "floor",
        "factor": 1.0,
        "top": 230,
        "colours": [(18, 22, 34), (32, 38, 56), (56, 64, 92)],
        "ruts": [11, 23],
    },
]

ANCHORS = {
    # The door's opening edge: the light behind it shows here, wider each round.
    "doorgap": {"layer": "door", "at": (840, 140, 862, 545)},
}
