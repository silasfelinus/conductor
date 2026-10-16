# Save the Plumber — in-game art plan

Queued 2026-10-13 in `projects/art-prompts.yaml` (ids `save-the-plumber-*`). Delivered files land on
the Kind Robots media host at `/images/arcade/save-the-plumber/<group>/<name>.webp`; they are not
committed to git. Queued is not rendered: check the live URL before calling an asset delivered.

## What was requested (84 game assets)

| Group | Count | Path | Size | How the engine uses it |
| --- | --- | --- | --- | --- |
| Stage backgrounds | 32 | `stages/<code>-<slug>` | 1344×768 | Opaque far plate per stage, panned slowly behind code-drawn parallax and terrain (the Ghost Trail pattern). |
| Ground tiles | 8 | `tiles/world-<n>-ground` | 1024×1024 | Seamless texture, downscaled and used as a pattern fill for each world's platforms. |
| Enemies | 14 | `enemies/<key>` | 1024×1024 | Every family in WORLD-ATLAS, side view facing right, on flat white. |
| Bosses | 16 | `bosses/<boss>-idle`, `-tell` | 1024×1024 | Eight bosses, an idle pose and a readable attack-tell pose each. |
| Teo | 2 | `cast/teo-caged`, `teo-helping` | 1024×1024 | Interludes and the finale, where he helps from inside the machine. |
| Items | 8 | `props/<key>` | 1024×1024 | Token, checkpoint pennant, goal valve, three power pickups, crate, health. |
| Cutscenes | 4 | `cutscenes/<key>` | 1344×768 | Intro (two), finale, credits vista. The heroine appears only from behind or in silhouette. |

World 1 assets and the items are priority 120; everything else 110. The front-page vignettes and
portraits queued earlier (`world-*`, `cast-teo`, `cast-lady-spigot`) already rendered.

## Transparency and animation

No checkpoint in the pipeline outputs alpha (krea2 and Flux cannot), and ComfyUI has no
background-removal node installed. Earlier arcade games (Ghost Trail, Rescue Rally, Sink Suds) never
used generated sprites in-engine: generated art was opaque far plates plus character reference
sheets, and every animated foe, boss and hero was drawn in canvas code to match its reference, with
idle, move, tell and attack poses and a facing flip.

Save the Plumber follows that pattern, with one addition:

- **Sprites are requested on plain flat white with a bold dark outline.** The engine keys the white
  out at load time by flood-filling from the image border, so a delivered sprite can be drawn
  directly (bob, squash, flip and tilt in code) before a hand-drawn animation cycle exists.
- **The same images are the references** for code-drawn animation cycles where motion matters
  (the heroine, walking enemies, boss tells).
- **The heroine stays code-drawn.** Her look is randomized per run, so no single painted sprite can
  represent her.

A cleaner long-term fix is an image-matting node (BiRefNet or RMBG-2.0) as a post-step in the
ComfyUI workflow, which would give every sprite request a true alpha channel. That is a change to
the home render box, not to this repo.

## Animation pilot (2026-10-14)

Silas: *"This game would live or die on the quality of the main character, and the enemies."* One
painted pose per character is not animation, and a code-drawn heroine is not that bar.

Image models drift between separate renders but stay consistent inside one image, which is why Kind
Robots' character-sheet workflow draws every view in a single canvas. The pilot (`anim/`, 8 sheets,
priority 125) applies that to animation: each sheet is one character in six frames on one ground
line, on white, which the engine keys out and slices into frames.

| Sheet | Frames |
| --- | --- |
| `heroine-a-run`, `heroine-b-run` | six-frame run cycle |
| `heroine-a-actions`, `heroine-b-actions` | idle, crouch, leap, fall, land, hurt |
| `heroine-a-turnaround` | front, three-quarter, side, back |
| `pumpbug-cycle` | four walk frames, squashed, flipped |
| `rivet-roller-cycle` | four roll frames, stunned, tipped over |
| `madame-pressure-attack` | idle, wind-up, steam burst, recover, hurt, defeated |

**Heroine proposal.** Painted animation cannot follow a per-pixel randomized look, so the heroine
becomes a roster: each new game randomly picks one of a set of fully painted young women (the way
Rainbow Princess picks among P1 to P4), each with her own name and complete animation sheets. Every
roster member keeps the same hitbox and abilities. The pilot tests two designs; if their frames hold
together, the roster and every enemy and boss get full sheets. Silas approved the roster on
2026-10-14 (see "The heroine roster" below).

### Round 1 findings (2026-10-14)

| Sheet | Character consistency | Poses | Slices |
| --- | --- | --- | --- |
| heroine-a-actions | identical across frames | six clearly different poses | 6/6 |
| heroine-a-turnaround | identical | four clean views | 4/4 |
| rivet-roller-cycle | identical | near-identical; asked-for roll ignored | 6/6 |
| heroine-a-run | identical | near-identical stride, figures overlap | rejected |

- krea2 holds one character steady inside a sheet, and draws categorically different poses
  (idle, crouch, leap, fall) well. It does not draw subtle cycle phases: it repeats the pose.
- Figures must not touch. Column slicing failed on organic poses (a raised hand shares columns with
  the next figure), so the engine slices by connected shape and cuts only each figure's pixels
  (kind_robots silasfelinus/kind_robots#3661).
- Design A read as a child (large head, short limbs). The brief wants a young adult.

Round 2 (`*-v2-*`): adult proportions spelled out (about seven heads tall, long legs), the run as four
categorically different poses rather than a smooth cycle, and every figure in its own section of the
sheet with a wide white gap. The engine tweens between key poses with bob and squash, so four strong
run poses are enough. Rolling enemies rotate a single sprite in code rather than painting a cycle.

**Prompt wording for sheets.** Never write "frame" in a prompt ("six frames", "every frame", "frame
one"): kind_robots' prompt contract rejects it (`frame-noun`), because Krea paints a picture frame.
Round 1 lost seven sheets and round 2 lost three to 422s this way. Say "poses" and "figures" ("six
poses of ...", "the same character repeated in every pose", "every figure the same scale", "first
pose ..."). Before pushing new rows, run `python scripts/check_art_prompts_live_contract.py --project
save-the-plumber` (needs a kind_robots checkout beside conductor).

### Round 2 findings and the enemy batch (2026-10-14)

- **Figure size decides separation.** Heroine B's sheets, the pumpbug and Madame Pressure all sliced
  cleanly because their figures sat small in their sections. Heroine A's adult-proportion sheets
  touched and failed to slice; her round-2 turnaround drew five views instead of four.
- Adult proportions worked: Heroine A v2 reads as a young adult.
- Heroine B's run sheet varies its stride across six frames and is now the game's first painted
  animation (kind_robots silasfelinus/kind_robots#3666), with the pumpbug walk cycle.
- Madame Pressure's body barely changes across frames, but her gauge needle (green, red, green) is
  the readable tell; steam and shake are added in code.

Enemy batch (`anim/*-cycle`, `anim/*-attack`, priority 115): the other 13 enemy families and the
other 7 bosses, six categorically different poses each (move, tell, attack, hurt, defeat), every
figure small in its own sixth of the sheet. The first push of this batch said "six frames" in 16
prompts and was reworded to "poses" before any render (see the prompt-wording note above).

### The heroine roster (Silas, 2026-10-14)

Silas chose the painted roster: *"Love multiple heroines, with notable differences in body type,
ethnicity, etc."* Each new game picks one of eight heroines at random. All share the hitbox and
abilities, and all wear the crew motif (brass goggles, a scarf, a small wrench on the belt). Each
has her own silhouette and palette so she reads at sprite size.

| Key | Heroine | Build and look | Palette |
| --- | --- | --- | --- |
| `pip` | Pip | slim, pale and freckled, magenta bob (pilot Heroine B, sheets already in game) | mustard, lavender, white |
| `marisol` | Marisol | slim athletic Afro-Latina, big curly hair, coral bandana (Heroine A, redrawn with small figures) | teal, cream, coral |
| `tala` | Tala | tall and fat Samoan, broad shoulders, thick braid with a hibiscus clip | sunflower, white, turquoise |
| `jiwoo` | Ji-woo | short, stocky and very muscular Korean, teal-topped undercut | safety orange, charcoal |
| `odette` | Odette | Black grandmother in her sixties, soft sturdy build, silver locs, gold glasses | plum, denim, mustard |
| `hodan` | Hodan | very tall and lanky Somali, sporty fitted hijab | teal, coral, olive |
| `priya` | Priya | short and curvy Indian, long braid, gold nose stud | burgundy, saffron, pink |
| `nova` | Nova | lean and wiry Indigenous North American, two braids, running-blade prosthetic right leg | denim, forest green, red |

Queued per heroine (priority 130): a character select portrait (`cast/heroine-<key>`, 1024 square,
painted backdrop), a six-pose run sheet and a six-pose action sheet (`anim/heroine-<key>-run`,
`anim/heroine-<key>-actions`), using the small-figure formula. Pip only needs her portrait. Nova's
blade is on her right leg so it shows on the near side in the right-facing sheets; if a sheet drops
it in some poses, re-roll that sheet rather than painting it in by hand.

When the sheets land: slice each one (4-connected, at 960px), re-roll any that fail, then replace
the code-drawn casting with the painted roster. `rollHeroineSeed` picks the heroine, and "keep"
remembers her.

### Roster round 1 findings (2026-10-14)

- Portraits for Pip, Marisol, Tala, Ji-woo, Odette and Hodan are on-model and read as clearly
  different builds. The small-figure formula sliced 8 of the 9 delivered sheets 6/6.
- Run sheets still repeat one stride across six figures (only the scarf changes), so the engine's
  bob carries the motion. Action sheets give distinct idle, crouch, leap and fall poses in the
  default order.
- Marisol's run overlapped into one shape again. She is re-rolled as `heroine-marisol-run-v2`
  with an explicit boot-to-fist gap; until it lands she steps between two action poses.
- Wired into kind_robots silasfelinus/kind_robots#3676 (casting picker, painted faces, sheets per heroine).

### Level-building batch (2026-10-16)

Queued for World 1 and the worlds after it (30 rows):

- `anim/heroine-marisol-run-v3`: her run failed twice with one connected shape. Her description
  carried "about seven heads tall" from Heroine A, which makes krea2 paint six large overlapping
  figures; the other heroines' descriptions do not, and their sheets slice. v3 drops it and asks for
  figures about a third of the image height.
- `anim/heroine-<key>-moves` for all eight heroines: wrench wind-up, wrench strike with a splash,
  lift overhead, throw, cheer, dazed. The game uses them for the tool, carrying (Pocket Lift),
  stage clear and losing a life.
- `tiles/world-<n>-ledge` and `tiles/world-<n>-block` for all eight worlds, in each world's ground
  palette: one-way ledges and solid walls, so a level is more than one floor texture.
- World 1 props: `steam-vent` (hazard), `pipe-door` (secret room entrance), `valve-switch`,
  `brass-lift` (moving platform) and `boss-gate`.

