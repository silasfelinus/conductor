"""Append -v2 idle cells that start from the shipped Fever Dream still (source_url), for loops whose first take
used a stale source image or barely moved. Appends text at the end of the ledger so the diff stays small."""
import sys
from pathlib import Path
import yaml
from PIL import Image
sys.path.insert(0, "/home/user/conductor/scripts")
from art_ledger_authoring import ledger_problems

KR = Path("/home/user/kind_robots/public/rainbow-princess-art/doodle")
L = Path("/home/user/conductor/projects/rainbow-bullet-hell-space-princess/art/ANIM-BACKLOG-2026-11-24.yaml")
CELLS = {
    "enemies/brood": "A spiky magenta star spore with four long points and an orange drip below spins a slow quarter turn back and forth, its points flexing and its core flashing pink.",
    "enemies/bulwark": "The dark armoured shell fish with the big yellow spiral eye bobs clearly up and down, both small fins paddling hard, its spiral eye whirling and the stripes on its dome shimmering.",
    "enemies/eel": "A glassy pale blue eel with dark netted scales coils and uncoils in a smooth S-curve, a ripple running down its long body to the flicking tail tip.",
    "enemies/harbinger": "A round stained-glass sea disc in deep blues, topped by a gold shell dome and a gold star, rocks gently while its star twinkles and the coloured panes pulse with light.",
    "enemies/mirror": "The magenta piranha with a yellow eye and jagged teeth snaps its jaw open and shut, its spiky back fins rippling and its lilac belly fins swinging under it.",
    "enemies/salvager": "A purple starry dome jellyfish craft drifts up and down as its curly golden tentacles curl and uncurl beneath the dome, glints crossing the speckled bell.",
    "enemies/skate": "A pale blue winged skate beats its broad translucent wings in slow strokes, its thin body steady and the long pink tip on its tail swaying.",
    "enemies/squid": "A crystal blue diamond squid with one dark eye pulses its facets brighter and dimmer while its fan of fine black tendrils sweeps behind it.",
    "enemies/turret": "A violet flower-bud turret on a teal stalk sways from its base, its petal crown opening a little and closing again like a breathing blossom.",
    "enemies/guardian-bulwark": "A violet armoured shell guardian with a spiral marking on its side sways forward and back, the pink fringe of short tentacles under its shell rippling.",
    "enemies/guardian-clawstrike": "A blue armoured crab walker with an orange belly shifts its weight from leg to leg, its long dark cannon bobbing as its shell plates catch the light.",
    "enemies/guardian-lantern": "A rainbow jellyfish with a glowing heart-shaped bell throbs warmly, its pastel tentacles streaming and curling below in long soft waves.",
    "enemies/guardian-salvager": "A grey metal helmet octopus with glowing orange eyes flexes its curled steel tentacles, its eyes brightening and dimming as it hovers.",
    "enemies/guardian-urchin": "A white armoured beetle walker with purple spikes and one yellow eye stamps lightly in place, the spikes along its back bristling up and settling.",
    "ships/comet-crown": "A lavender swept-wing jet hovers with a light bob, its engine glow flickering at the tail and a highlight sliding along its pointed nose.",
    "ships/halo-fin": "A yellow flying saucer with a cyan glass dome wobbles softly, the pink lights around its rim chasing each other in a circle.",
    "ships/petal-wing": "A pink and white jet fighter with a navy underside hovers and banks slightly, its wingtip lights blinking and exhaust flaring at the rear.",
    "ships/prism-lance": "A navy delta jet traced in white outline hovers steadily while its gold thruster pulses and a spark of light runs along its wing edges.",
    "bosses/b07-phase1": "A coiled glassy blue sea serpent with dark netted scales sways its head side to side, the coils of its body rolling in a slow wave.",
    "bosses/b07-phase2": "The cracked glassy sea serpent shudders, its coils tightening and loosening while sparks flicker along the fractures in its netted scales.",
    "bosses/b07-phase3": "The wounded glassy serpent rears back as a magenta starburst at its chest blazes and fades, its coils trembling and its jaw gaping.",
    "bosses/b09-phase1": "A dark navy leviathan outlined in white glides in place, its spiky back ridges rising and falling and its long tail sweeping slowly.",
    "bosses/b09-phase2": "The starry navy leviathan heaves, the constellations inside its body twinkling while its jagged fins flare out and fold back.",
    "bosses/b09-phase3": "The battered navy leviathan surges and sags as the golden heart in its chest beats bright, its torn fins fluttering.",
    "enemies/motherdrone": "A white and gold crystal drone ship with swept gold fins hovers and tilts nose up and down, its pink thruster flame flaring long and short behind it.",
    "enemies/pistol": "The blue barrel fish with a yellow cog mouth and pink core holds one spot at one size while its cog spins round, its core throbs and its little fins flap.",
}
TAILS = [
    "Locked view on a flat green field; its exact look and palette hold; neon school-folder airbrush.",
    "Still camera, solid green border all round, colours match the source; glossy 1980s sticker style.",
    "Fixed shot, even green surround, the same silhouette and paint throughout; airbrushed neon doodle.",
]


def size_for(rel):
    w, h = Image.open(KR / f"{rel}.webp").size
    m = max(w, h)
    W, H = w + 0.4 * m, h + 0.4 * m
    s = 832 / max(W, H)
    return f"{max(320, round(W * s / 16) * 16)}x{max(320, round(H * s / 16) * 16)}"


text = L.read_text()
have = {s["key"] for s in yaml.safe_load(text)["subjects"]}
new = []
for i, (rel, prompt) in enumerate(CELLS.items()):
    name = rel.split("/")[-1]
    key = f"idle-{name}-v2"
    if key in have:
        continue
    url = f"/rainbow-princess-art/doodle/{rel}.webp"
    new.append({
        "key": key, "lane": "wan-mp4", "entity": "sprite-animation", "title": f"{name} idle loop",
        "asset": f"rainbow-princess-art/doodle/anim/{name}-idle", "size": size_for(rel), "seed": 1125100 + i,
        "source_url": url, "last_image_id": url, "source_matte": "#08f408", "source_margin": 0.2,
        "duration": 2, "loop": True, "prompt_prose": f"{prompt} {TAILS[i % len(TAILS)]}",
    })
if new:
    if not text.endswith("\n"):
        text += "\n"
    text += yaml.safe_dump(new, width=118, sort_keys=False, allow_unicode=True)
    L.write_text(text)
D = yaml.safe_load(L.read_text())
print(len(new), "added;", ledger_problems(D))
