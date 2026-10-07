"""The Bone Yard, the Hyena Matriarch's home stage (t-009): a night of firelight, a ruined arch over a bonfire.

Art: the backdrop is by-backdrop-2 (243156, art/T009D-STAGES.yaml, a fire glow on the horizon under a black
sky). The brief's giant fossil ribcage would not render. "The ribcage of an ancient giant beast" (T009D) drew
the beast, "ribs like the arches of a ruined cathedral" (T009F seeds 1-3) drew a cathedral, and "a row of
enormous rib bones" (seeds 4-6) drew whole walking skeletons. So the midground is the cathedral attempt's
stone arch over a campfire (243171). Code-drawn ribs behind it read as a tent frame next to the painted art,
so the stage is the fire-lit ruin, and the pack's silhouettes perch on the arch. Boxes and anchors are in source
pixels of the 1536x640 renders.
"""

SEED = 979
PALETTE_COLOURS = 40  # per layer

LAYERS = [
    {"name": "backdrop", "kind": "full", "art": 243156, "factor": 0.2, "height": 240, "top": 0},
    {"name": "arch", "kind": "keyed", "art": 243171, "factor": 0.6, "height": 150, "bottom": 236},
    {
        "name": "floor",
        "kind": "floor",
        "factor": 1.0,
        "top": 230,
        "colours": [(34, 26, 24), (56, 42, 36), (86, 64, 50)],
        "ruts": [11, 23],
    },
]

ANCHORS = {
    # The bonfire under the arch: its glow flickers and embers rise from it.
    "fire": {"layer": "arch", "at": (690, 320, 790, 530)},
    # Where the pack perches (each hyena's feet): the left capital, the broken beam, the right capital.
    "perch-a": {"layer": "arch", "at": (565, 94)},
    "perch-b": {"layer": "arch", "at": (800, 176)},
    "perch-c": {"layer": "arch", "at": (915, 166)},
}
