"""Hollow Bell, Zuzu's home stage (t-009): dusk over the mesas, the bell house and its tower, the street.

Art: T009-STAGES.yaml, Arthemy house lane. Backdrop hb-backdrop-2 (243056, the sun on the horizon; seed 1
read as a volcano, seed 3 hid the sun), midground hb-town-1 (243058, the only one with the bell hanging in
the arch). Boxes and anchors are in source pixels of the 1536x640 renders.
"""

SEED = 909
PALETTE_COLOURS = 40  # per layer

LAYERS = [
    {"name": "backdrop", "kind": "full", "art": 243056, "factor": 0.2, "height": 240, "top": 0},
    # The bell house sits on the street, twice Zuzu's height to the roof peak.
    {"name": "town", "kind": "keyed", "art": 243058, "factor": 0.6, "height": 150, "bottom": 234},
    {
        "name": "floor",
        "kind": "floor",
        "factor": 1.0,
        "top": 230,
        "colours": [(56, 38, 30), (90, 64, 48), (124, 92, 66)],
        "ruts": [11, 23],
    },
]

CUTOUTS = {
    # The bell in the arch swings on its rope (the rope stays in the layer).
    "bell": {"layer": "town", "box": (698, 362, 748, 434)},
    # The torn pennant on the bunting flaps.
    "banner": {"layer": "town", "box": (322, 284, 374, 340)},
}

ANCHORS = {
    # The beam over the arch: the game letters HOLLOW BELL on it in the pixel font.
    "arch": {"layer": "town", "at": (548, 302, 898, 326)},
    # The town has no chimney; the smoke drifts off the street lantern's cap.
    "smoke": {"layer": "town", "at": (272, 258)},
}
