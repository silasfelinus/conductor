# Arcade Generation 2 — the SMB3 / Super Mario World bar

**Direction (Silas, 2026-10-22 PT):** Save the Plumber and Zuzu: Ghost Trail "need a concept
evolution. I was saying the games needed an old school Mario Bros / Ghosts 'n Goblins vibe, but
they need to aim for Super Mario Bros 3 / Super Mario World for level design, gameplay conception,
gameplay depth, etc. The games should have persistent save states, long form exploration, etc.
Rainbow Space Princess should have the same consideration. Games should have memory, recognize
progress, etc. So we need open world maps, save states, etc. And probably upgrades to pixel
expectations and other factors." And: "we will need animations if we are upgrading our
platformers to N64 level expectations. Which we now are."

This file is the shared bar for the three long-form Arcade campaigns. Each project's DESIGN-BRIEF
carries its own "Generation 2" section that applies it. A Gen-1 feature that already exists (32
Plumber stages, six Ghost Trail stages, eight Rainbow Acts) is **raw material**, not a reason to
call a Gen-2 requirement met.

**Confirmed by Silas, 2026-10-22 PT:** "I meant 2d. super mario world should be the benchmark for save
the plumber. or any of the later 2d mario wonder level games. I authorize all projects to get them to
wonderful states." So the games stay **2D**; *Super Mario World* is Save the Plumber's benchmark and the
later 2D Marios (*Super Mario Bros. Wonder* and its kin) are fair targets for level ideas and polish. The
"N64 bar" is production value: smooth many-frame animation, a living camera, depth through parallax and
lighting, animated cinematics and a game that remembers you. Match the design quality and structure,
never the content: no borrowed names, characters, items, layouts or music.

## 1. The world is a place, not a level list

- **Walkable overworld per world** (SMB3 / SMW): nodes for levels, fortresses, bonus houses, shops
  and secrets, joined by paths that are revealed with an animation when earned.
- **Two exits where it matters.** A level's normal exit opens the next path; a hidden secret exit
  opens a different one (SMW keyhole logic). At least one secret exit per world, and secret routes
  that skip, branch or reach optional worlds.
- **Revisit freely.** Cleared levels stay enterable for collectibles and secret exits, and the map
  marks what is left in each (clear, secret exit found, all collectibles).
- **World-to-world travel** with a world select once a world is cleared, plus one optional
  "special" zone reached only through secrets (SMW Star Road / Special World in spirit, original
  in content).

## 2. Levels are longer, layered and authored

- **SMW-length levels**: 3–6 minutes for a first clear, with a midpoint checkpoint, one or more
  sub-areas (doors, pipes, ladders into rooms, vertical shafts) and a secret that needs a power or
  a thrown object to reach.
- **Level types beyond "run right"**: fortress/castle with a mid-boss, a haunted maze (ghost
  house) whose exit logic is the puzzle, auto-scrollers, vertical climbs, water levels, a
  switch-palace equivalent whose switch **changes other levels permanently** (blocks become
  solid across the whole campaign).
- **Introduce → combine → subvert → test** still holds inside each world, now over 6–9 nodes
  rather than four stages.

- **A wonder moment per level** (*Wonder* in spirit, original in content): an optional collectible that,
  once touched, transforms the level for a while (the floor becomes a river, the pipes start to sing and
  carry you, the camera turns, enemies change behaviour), with its own reward at the end. Every level
  should have one surprise you will want to tell someone about.

## 3. Memory: the game recognizes progress

- **Persistent save slots** (three per game) with: map position, each level's clear and secret-exit
  flags, collectible IDs, switches pressed, unlocked paths, power and reserve item, lives, total
  time, deaths and completion percent. Versioned and migrated; a v1 save loads into v2, never
  wiped.
- **The world reacts**: cleared fortresses crumble on the map, rescued characters appear at their
  home node, NPC lines change with what you have done, the title screen shows your furthest
  world.
- **Completion tracking** visible on the map and in a file-select screen (exits found x/y,
  collectibles x/y, percent).
- **Account sync** later through a Kind Robots save endpoint so a save follows the player between
  devices; until then saves live on the device with export/import.

## 4. Gameplay depth

- **Power-up economy of SMB3/SMW scale**: 5–7 distinct powers with movement consequences (flight
  or glide, a suit for water or fire, a heavy form, a carry/companion), a **reserve item** the
  player can call down, and a map-usable inventory (SMB3 item cards, original in kind).
- **A ride or companion** (Yoshi-scale idea, original creature) that changes traversal and eats or
  carries enemies.
- **Enemies as toys**: every family reacts to stomp, throw, carry, power and terrain differently,
  with a telegraph animation. 40+ behaviors across the campaign.

## 5. Pixel, animation and presentation bar

- **Sprites**: the hero reads at 32–48 logical px, with real animation sets: idle 6–8, walk 8, run
  8, jump/fall 4, skid, crouch, climb, swim, carry, hurt, power-up transform, victory. Enemies get
  idle/move/telegraph/attack/hurt/defeat. 12 fps or better, with squash and stretch.
- **World depth**: at least four parallax planes per level, animated tiles (water, lava, lights,
  grass), foreground occluders, per-level lighting tint and weather particles.
- **Camera**: look-ahead, vertical framing for climbs, a short zoom or pan for boss intros.
- **Cinematics**: opening, world interludes and finale as animated scenes (image-to-video clips
  between painted keyframes), skippable and subtitled.
- **Two renders of one art direction**: Pixel and HD share geometry; HD is painted at source
  resolution, not an upscale.

## 6. How the art gets made (pipeline that already works)

1. **Key art and poses**: painted keyframes and white-surround character poses through
   `scripts/enqueue_art_requests.py` ledgers (Arthemy, Z-Image, Krea 2, Nova Comic lanes).
2. **Motion**: WAN 2.2 first-and-last-frame image-to-video between two approved poses, the route
   proven by `projects/zuzu-pinball/art/T019-CROC-CLIPS.yaml` (round 3: 6/6 clips on model). The
   5B first-frame-only model does not make large prompted motion; use the A14B first/last pair.
3. **Atlas**: cut clips to frames, matte the white, normalize pivot and bounds, pack per action
   (the croc atlas tool is the template).
4. **Parallax**: per-level layer plates (sky / far / mid / near) rendered separately, never one
   flattened picture cut apart.
5. **Never count a queued job as art.** A picture counts when it is DONE, reviewed and wired into
   the game.

## 7. What finished means

A blind player can save, quit, return on the same device and find the map, flags and inventory as
they left them; can find a secret exit and see a new path open; can 100% a world and see it marked;
and Silas plays a world end to end and judges it SMB3/SMW-class. Silas's hands-on verdict stays
the final gate, as before.
