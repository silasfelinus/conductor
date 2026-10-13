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
