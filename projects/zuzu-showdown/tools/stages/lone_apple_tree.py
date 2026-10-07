"""The Lone Apple Tree, the Siblings' home stage (t-009): a bleached wasteland at noon, the tree and its cart.

Art: the backdrop is la-day-backdrop-1 (243152, art/T009C-DAY.yaml). Both T009B backdrops came back as a
burning dusk under the house lane's dark prefix; seed 2 of the daylight lane drew an animal on its ridge and
seed 3 a skeleton; seed 1's one bone is painted out. The midground is la-mid-1 (243119, art/T009B-STAGES.yaml): the tree and the apple cart
(its crown came out red). The falling apples, the drifting leaves and the dust devils are code. Boxes and
anchors are in source pixels of the 1536x640 renders.
"""

SEED = 949
PALETTE_COLOURS = 40  # per layer

LAYERS = [
    {
        "name": "backdrop",
        "kind": "full",
        "art": 243152,
        "factor": 0.2,
        "height": 240,
        "top": 0,
        # A bleached bone in the foreground, painted out with the sand around it.
        "patches": [(110, 548, 400, 638)],
    },
    {"name": "tree", "kind": "keyed", "art": 243119, "factor": 0.6, "height": 130, "bottom": 234},
    {
        "name": "floor",
        "kind": "floor",
        "factor": 1.0,
        "top": 230,
        "colours": [(150, 116, 78), (196, 160, 112), (226, 196, 150)],
        "ruts": [11, 23],
    },
]

ANCHORS = {
    # The underside of the crown: apples drop from here, and leaves drift down from it.
    "canopy": {"layer": "tree", "at": (380, 230, 790, 290)},
}
