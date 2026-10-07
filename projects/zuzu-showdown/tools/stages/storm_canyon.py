"""Storm Canyon, Storm Crow's home stage (t-009): a storm over red rock, the canyon floor between its walls.

Art: T009B-STAGES.yaml, Arthemy house lane. Backdrop sc-backdrop-2 (243123, rain and red peaks; seed 1's
lightning filled the sky). The midground is sc-mid-1 (243124), a ridge rising to the right, cropped from the
lone pillar to the peak and set after its own mirror image, so it walls the canyon on both sides (sc-mid-2
put a bird on its spire). The rain, the crows and the lightning are code.
"""

SEED = 939
PALETTE_COLOURS = 40  # per layer

LAYERS = [
    {"name": "backdrop", "kind": "full", "art": 243123, "factor": 0.2, "height": 240, "top": 0},
    {
        "name": "walls",
        "kind": "keyed",
        "art": 243124,
        "crop": (450, 40, 1500, 600),
        "mirror": "before",
        "factor": 0.6,
        "height": 160,
        "bottom": 236,
    },
    {
        "name": "floor",
        "kind": "floor",
        "factor": 1.0,
        "top": 230,
        "colours": [(52, 26, 24), (86, 44, 36), (120, 64, 48)],
        "ruts": [11, 23],
    },
]
