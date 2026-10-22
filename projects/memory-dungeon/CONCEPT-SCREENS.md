# Memory Dungeon — Concept Screen Direction (2026-10-22 PT)

**Not shipped game art.** Four 1600×900 working comps were created during the creative session to visualize the intended *video-game* screen grammar. They are local exports shared in the conversation, not part of the app's official asset bundle. Rendered vector/blockout art shows hierarchy and interaction; the finished game must replace this with detailed coherent painted art, animation, sprites and level effects. Names in these mockups (Briarwater Expanse, Unwritten Atlas, Clockwork Choir, Pip) are provisional placeholders; the larger world is not canonized.

**Rule:** One shared in-game art/UX language and a full-screen camera with scene-dependent HUD, not a web-app dashboard with separate panels. Existing /play/memory route and classic matching stay. See WORLD-AND-EXPLORATION.md and COMBAT-PATTERNS.md.

## Screen A: explorable overworld

- Isometric big tile landscape, visually recognisable authored regions, roads and permanent landmarks, revealable fog and localized secrets. Standard camera follows the player; exploration can auto-traverse discovered safe routes.
- Click/tap a terrain cell to **discover** what's there; it might expose a battle, treasure, riddle, character, portal, settlement or environmental story. Not every tile is a pair.
- Linked terrain motifs/marks across landmarks invite sequential matching and reward inference with a secret site or Edgeworld.
- A small diegetic Cartographer journal at left, a current discovery/cut-in at lower right, compact in-game gear/party/journal HUD, no scrolling website headers.
- **Need art:** terrain tile palette (forest, mountain, marsh, town, cave, ruined road), fog and revealed states, compass, landmark silhouettes, multi-tile portals, environmental reflections, recurring NPC sprites and player avatar options.

## Screen B: nested memory battle

- Opening a monster tile transitions into a memory-match arena without changing the URL; the overworld map state and camera coordinate stay saved.
- Large 6×6 card board with image fronts, tactile backs, targetable shape preview, *marked bullseye cell*, positioning/rotation controls and crisp reveal animations. Monster on the other half of game stage and a large expressive enemy intention notice.
- Correctly remembered positions produce targeted weapon strikes; a matching pair at bullseye yields bonus status/damage. Distinguish match, reveal and damage so wider masks don't become automatic wins.
- **Need art:** full-body monster illustrations with condition frames, weapon effects (twinblade, hammer diagonal, staff cross), target decals, runes and damage/heal/stagger effects.

## Screen C: narrative treasure surprise

- Illustrated cinematic encounter with giant odd fantasy treasure, visible hero/companion silhouettes, and enough scene space to appreciate the art.
- Two or three visible *distinct, costly* choices. Choosing changes relationships, curse/loot and the world Chronicle; no "correct" option hiding an automatic bonus.
- Tone irreverent but character-centred: the treasure might negotiate contract terms or the apparent monster may have better ethics than its captor.
- **Need art:** surprise treasure/creature reveal plates, scene and reaction portraits, signature bizarre relics, environment-specific lighting and choice-outcome vignettes.

## Screen D: deduction vault

- Rare large 8×8–10×10 grid with numerical near-hazard clues and visible flags, integrated into a vast fantasy vault. No arbitrary mobile scroll clipping; zoom/pan or well-spaced bounded canvas.
- A weapon with a small exact bullseye can disable a deduced trap. A wide strike can reveal clues but risks damaged treasure or a named companion. Core progression is solver-proved without blind guesses.
- **Need art:** gate, field tile states, clue numbers with noncolor affordances, flags, danger effects, vault landmarks, large detailed mechanisms.

## Screen E: Character Creation & Journal (design next)

- In-world adventurer outfitting room/illustrated portrait, original fantasy species/body/age/gender variety with no identity-based penalties, practical starting disciplines and choice of initial reveal/strike tool.
- World/character/expedition/Chronicle save slots; visually style as adventurer's journal, a map desk and stained-glass memory leaves rather than a web settings form.
- Chronicle shows highlights across runs, encountered NPC relationships, remembered terrain-link combinations and persistent world changes, without grinding permanent stat inflation.

## Viewport/application boundary

The outer Kind Robots Play tab and discoverability link remain. Within `/play/memory`, the user enters a distinct cinematic game mode, with existing Classic Match also one click away. The full fantasy game scene uses all shell-available height, not 100vh, includes keyboard/joypad/touch equivalents, legible type at 390/768/1440 widths, reduced-motion and screen-reader alternatives. Text tutorial moves to existing help sidebar. Every scene should be reviewable via actual render tests; art prompts are not verified finished assets.
