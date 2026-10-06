# Production sheets: the first two music videos

Silas, 2026-10-06: "two videos in production, once the front end and back end are in sync": the
Zuzu intro (t-029) and a Kind Robots theme song (t-015). Both run from `/admin/music-video` with
**Produce** (kind_robots t-031). No script is needed.

## How to start one

1. On `/admin/music-video`, press **New video**, choose the video under **Create from spec**, and
   press **Create from spec** (kind_robots t-033). That creates it fully set up: pitch, settings,
   style bible, banned terms, lyrics, scenes on the beat grid with prompts, and the hero shots
   with their animation prompts. Nothing needs pasting. The specs live in kind_robots
   `utils/musicVideoSpecs.ts`. A session with an admin `KR_API_TOKEN` can do the same with
   `POST /api/music-video/import` and `{"specKey": "kind-robots-theme"}` or
   `{"specKey": "zuzu-intro"}`.
2. Press **Produce** and keep the tab open. Because the brief, lyrics, scenes and prompts are
   already there, it goes straight to the song, then the stills, then the hero clips, then the
   export and attach. Each clip can take 30 to 90 minutes on the 12 GB card, so a run with five
   hero shots is an overnight job. The page resumes after a reload.
3. While it runs, you can change anything on a scene card: edit the lyric lines under the image,
   replace the image (upload, a recent art job, or an ArtImage id), toggle **Hero** and edit its
   animation prompt, or set a different checkpoint and LoRAs for that one still. Press
   **Re-export final cut** when you are done.

The tables below are the reference for what each spec contains.

---

## A. Kind Robots theme song (t-015)

The splash or buzz trailer for the site: Kind Robots' own bots in an original homage to 80s and
early-90s Saturday-morning action cartoons.

| Field | Value |
|---|---|
| Title | `Kind Robots: Theme Song` |
| Length | `75` |
| Aspect | `16:9` |
| BPM | `140` |
| Vocal | `duet` |
| Hero shots to animate | `5` |
| Genre | `80s Saturday-morning cartoon theme, synth rock, shouted gang-vocal chorus` |
| Mood | `heroic, goofy, high-energy` |
| Comic series id / lane | leave blank (Krea 2) |

**Pitch**

```
The opening theme for the Kind Robots cartoon: a crew of small, friendly, mismatched robots who
build things, fix things and help people, racing across a neon city at night. Rooftop chases,
a workshop full of sparks, a junkyard team-up, a skateboarding robot, a giant friendly mech
assembled from scraps, and a final heroic group pose under a rainbow-lit sky. Kindness is the
superpower. The chorus is a shouted gang-vocal hook about being kind robots.
```

**Style bible** (the spec uses a reworded version: the Krea scene-prompt rules refuse negations
and lettering words, so "No text, logos or lettering" and "silhouette" would have blocked every
still)

```
An original homage to 80s and early-90s Saturday-morning action cartoons. Thick black ink
outlines, flat cel colour with hard two-tone shadows, saturated neon pinks, teals and oranges
against deep night blues. Painted cel backgrounds of a rain-slick neon city: rooftops, water
towers, fire escapes, a cluttered robot workshop, a junkyard at dusk. Comic-book action poses,
speed lines, low heroic camera angles, dramatic rim light. Every character is a small friendly
robot with a readable silhouette; no humans in close-up. No text, logos or lettering in frame.
```

**Banned terms** (keeps the homage original; the franchise name never enters a prompt)

```
teenage mutant, ninja turtle, ninja turtles, tmnt, turtle, turtles, shredder, splinter,
michelangelo, donatello, raphael, leonardo, krang, foot clan, cowabunga, april o'neil
```

Hero-shot ideas, if you would rather choose them yourself: the mech assembling, the skateboard
jump, sparks flying in the workshop, the rooftop leap, and the final group pose.

---

## B. Zuzu: Koala Assassin intro (t-029)

The full brief, with canon, guardrails, keyframes and the shot list, is
[`zuzu-intro.md`](zuzu-intro.md). These are the fields for the page.

| Field | Value |
|---|---|
| Title | `Zuzu: Koala Assassin — Intro` |
| Length | `55` |
| Aspect | `16:9` |
| BPM | `100` |
| Vocal | `instrumental` |
| Hero shots to animate | `5` (the brief's clip beats 6, 9, 10, 11, 12) |
| Genre | `cinematic samurai western title theme` |
| Mood | `slow, ominous, dusty, building to a hard final hit` |
| Comic series id | the Zuzu series' id (open it in Comic Studio; the id is in the URL) |
| Comic lane | `IL Arthemy Western Art` (`il-arthemy`) |

**Pitch**: the Pitch paragraph of `zuzu-intro.md`.

**Style bible**: copy the block under "Style bible (visuals)" in `zuzu-intro.md`, exactly.

**Banned terms**: copy the `settings.bannedTerms` block in `zuzu-intro.md`, exactly.

**Keyframes.** The brief wants character shots to come from vetted comic art, not fresh renders.
Once the stills have rendered, put the brief's ArtImage ids on the matching scene cards with **Use
art**: 241913 for Zuzu hero, title and draw; 241879 and 241883 for the siblings on the road; 242435
for the coyote; 241893 for the crocodile; 241899 for the wide road. Then set the clip beats to
*Animated clip* with the brief's motion prompts, and press **Re-export final cut** (or **Produce
again**) once their clips are in.

**Verdict (t-029).** Check fidelity to the comic (poncho, kasa, sword on the right shoulder, koala
proportions), cuts on beats, the title card, that no banned term appears anywhere, and that the
mood stays serious.

---

## Running these from a session instead

A cloud session can create either video with `POST /api/music-video/import` (step 1 above) if the
environment has an admin `KR_API_TOKEN` set as an environment variable. Add it in the
environment's settings, then start a new session, which picks it up. The front-end flow above
needs none of that.
