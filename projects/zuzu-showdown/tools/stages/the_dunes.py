"""The Dunes, Old Komodo's home stage (t-009): rolling sand under a long golden sun, a wreck half buried.

Art: the backdrop is dn-backdrop-2 (243169, art/T009E-DUNES-DAY.yaml, the daylight lane; the golden one). The
midground is dn-wreck-2 (243166, art/T009D-STAGES.yaml), an old wheel and wagon box half sunk in a drift (pale
sand alone would key away against white). The sun, the sand blowing off the crests and the slumping dune with
something vast moving under it are code. Boxes and anchors are in source pixels of the 1536x640 renders.
"""

SEED = 959
PALETTE_COLOURS = 40  # per layer

LAYERS = [
    {"name": "backdrop", "kind": "full", "art": 243169, "factor": 0.2, "height": 240, "top": 0},
    {"name": "wreck", "kind": "keyed", "art": 243166, "factor": 0.6, "height": 72, "bottom": 234},
    {
        "name": "floor",
        "kind": "floor",
        "factor": 1.0,
        "top": 230,
        "colours": [(168, 120, 70), (214, 170, 110), (238, 204, 150)],
        "ruts": [11, 23],
    },
]

ANCHORS = {
    # Where the long sun sits, low over the far dunes, and the band of crests the wind lifts sand from.
    "sun": {"layer": "backdrop", "at": (1080, 230)},
    "crest": {"layer": "backdrop", "at": (120, 252, 1416, 282)},
}
