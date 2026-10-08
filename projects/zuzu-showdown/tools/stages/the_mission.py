"""The Mission, the Abbess's home stage (t-009): a moonlit desert night and the old church.

Art: T009B-STAGES.yaml, Arthemy house lane. Backdrop ms-backdrop-1 (243112, the full moon over the flats),
midground ms-mid-2 (243115, the church with its belfry, lit windows and a candle; ms-mid-3 put a cat on the
roof, ms-mid-1 has no belfry). Boxes and anchors are in source pixels of the 1536x640 renders.
"""

SEED = 929
PALETTE_COLOURS = 40  # per layer

LAYERS = [
    {"name": "backdrop", "kind": "full", "art": 243112, "factor": 0.2, "height": 240, "top": 0},
    {"name": "church", "kind": "keyed", "art": 243115, "factor": 0.6, "height": 140, "bottom": 234},
    {
        "name": "floor",
        "kind": "floor",
        "factor": 1.0,
        "top": 230,
        "colours": [(26, 32, 44), (44, 54, 70), (70, 84, 104)],
        "ruts": [11, 23],
    },
]

ANCHORS = {
    # The open bell arch in the belfry: between rounds a portal flickers in it.
    "portal": {"layer": "church", "at": (612, 226, 676, 270)},
    # The candle's flame by the door, and the chimney on the roof ridge.
    "candle": {"layer": "church", "at": (1187, 436)},
    "smoke": {"layer": "church", "at": (1000, 326)},
}
