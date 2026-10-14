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
together, the roster and every enemy and boss get full sheets.

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
