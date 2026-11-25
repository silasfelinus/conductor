"""Append the remaining idle loops to ANIM-BACKLOG: fourth takes for spiral, relay, coral and skimmer (from the shipped
Fever Dream sprite, a different source than the three failed takes), and the captive, coral asteroid, flagship phases,
kelp hazard and pickups."""

import sys
from pathlib import Path

import yaml
from PIL import Image

sys.path.insert(0, "/home/user/conductor/scripts")
from art_ledger_authoring import ledger_problems

KR = Path("/home/user/kind_robots/public/rainbow-princess-art/doodle")
ids = {
    "enemies/captive": 262118,
    "enemies/coral-asteroid": 278622,
    "bosses/flagship": 279298,
    "bosses/flagship-phase2": 279493,
}
CELLS = {
    "enemies/spiral": "Seen side-on the whole time, the blue spiral fish keeps its profile toward the left while its orange crest fans open and shut and its tail flicks hard.",
    "enemies/relay": "The jellyfish relay drone pulses strongly, its bell squeezing and expanding while its long magenta tendrils whip in big lazy curls and its beacon blinks.",
    "enemies/coral": "The coral-crowned whale craft rocks bow to stern, the frilly coral crown on its back waving like seaweed in a strong current.",
    "enemies/skimmer": "The tall pink jellyfish skimmer bobs up and down, its bell pumping and its fringe of tentacles streaming and settling.",
    "enemies/captive": "A trapped little creature in a bubble cage wriggles and taps at the bars, the cage shimmering.",
    "enemies/coral-asteroid": "A tumbling coral asteroid turns slowly about its centre, its pink coral branches catching glints of light.",
    "bosses/flagship": "The white and gold Motherland flagship hangs in space, its deck lights blinking in sequence and its gun turrets panning.",
    "bosses/flagship-phase2": "The battered flagship lists slightly, fires flickering along its broken deck and smoke curling from its stacks.",
    "hazards/kelp-frond": "A tall kelp frond sways from its root, its leaves rippling in the current.",
    "pickups/charge": "A glowing charge orb spins and sparkles, its light swelling and fading.",
    "pickups/power": "A power-up gem rotates on the spot, flashing as its facets turn.",
    "pickups/shield": "A shield bubble emblem pulses and shimmers, a highlight sliding across it.",
    "pickups/comet-cadet-pod": "A tiny rescue pod bobs gently, its window light blinking.",
    "pickups/coral-choir-pod": "A small coral choir pod wobbles, music notes of light flickering around it.",
    "pickups/lighthouse-lamp": "A little lighthouse lamp rotates its beam and glows.",
}
TAILS = [
    "Steady framing, flat green margin, same colours, glossy neon doodle.",
    "Camera fixed; identical outline and palette; even green surround; 80s sticker art.",
    "Static shot on plain green; the design stays exact; airbrushed neon cartoon.",
]
path = Path(
    "/home/user/conductor/projects/rainbow-bullet-hell-space-princess/art/ANIM-BACKLOG-2026-11-24.yaml"
)
text = path.read_text()
head = text.split("round:")[0]
D = yaml.safe_load(text)
have = {s["key"] for s in D["subjects"]}


def size_for(rel):
    w, h = Image.open(KR / f"{rel}.webp").size
    L = max(w, h)
    W, H = w + 0.4 * L, h + 0.4 * L
    s = 832 / max(W, H)
    return f"{max(320, round(W * s / 16) * 16)}x{max(320, round(H * s / 16) * 16)}"


for i, (rel, prompt) in enumerate(CELLS.items()):
    name = rel.split("/")[-1]
    key = f"idle-{name}" + (
        "-v4"
        if rel
        in ("enemies/spiral", "enemies/relay", "enemies/coral", "enemies/skimmer")
        else ""
    )
    if key in have:
        continue
    src = (
        {"source_image_id": ids[rel], "last_image_id": ids[rel]}
        if rel in ids
        else {
            "source_url": f"/rainbow-princess-art/doodle/{rel}.webp",
            "last_image_id": f"/rainbow-princess-art/doodle/{rel}.webp",
        }
    )
    D["subjects"].append(
        {
            "key": key,
            "lane": "wan-mp4",
            "entity": "sprite-animation",
            "title": f"{name} idle loop",
            "asset": f"rainbow-princess-art/doodle/anim/{name}-idle",
            "size": size_for(rel),
            "seed": 1125000 + i,
            **src,
            "source_matte": "#08f408",
            "source_margin": 0.2,
            "duration": 2,
            "loop": True,
            "prompt_prose": f"{prompt} {TAILS[i % len(TAILS)]}",
        }
    )
path.write_text(
    head + yaml.safe_dump(D, width=118, sort_keys=False, allow_unicode=True)
)
print(len(D["subjects"]), ledger_problems(D))
