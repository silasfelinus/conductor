# Memory Dungeon — World, Exploration and Encounter Layers

**Authoritative direction added 2026-10-22 PT.** This supersedes any overly specific names, cosmology, and linear descent assumptions in the initial DESIGN-BRIEF.md. The surrounding fantasy game's world has **not been authored yet**. Memory Dungeon is a special dungeon within that future, broad fantasy universe, not the source that defines the entire world. All character names, villain motives, regions and plot beats below are **non-canon working examples**.

## Creative register and world boundary

A wacky, expansive fantasy reality where magical regulations, absurd heroic economics, dangerous pantheons, talking infrastructure, and cosmic absurdity coexist with genuine stakes. Literary reference points named by Silas: Myth Inc, Munchkin, Dungeon Crawler Carl, Phil Foglio and comic LitRPG. Borrow only the *energy* (high imagination, irreverent problem-solving, consequences and warmth); build original characters, cosmology, visuals and humor. No recognizable copied world/lore, signature visual motif or licensed characters. Comedy should emerge from rules, personalities and contradictions, not nonstop punchlines.

The game has **two related but distinct boards**, plus a third layer of scripted interactions:

### 1. Persistent Overworld: reveal a place, not just an identical image

The primary giant tile board is an **explorable geographic surface** with a stable world coordinate model. Flip/explore a square to reveal: a terrain tile, a named location, a path, a hazard, a mystery, an encounter, a merchant, a companion, a monster, treasure or a link to a dungeon. These are **not all memory pairs**. The first click may have a discovery cost or risk, but the revealed location stays where it was. Navigation and gradual map revelation, not repetitive clearing of the same cards, is the primary activity.

- The overworld is **static in its landmark positions and persistent continuity**. Authored geography, city names (when eventually canonized), major gates, quest anchors and important character homes do not randomize each new run. A player can form a reliable mental map and revisit meaningful places across sessions.
- Every revealed tile has typed fields: `worldId`, coordinate, `terrain`, `regionId`, `feature`, `discoveryState`, `interactionState`, `artRef`, `storyFlags`. Unrevealed coordinates have fog and a deterministic discoverability mask, rather than an arbitrary pair ID.
- Terrain matters: a graveyard has cemetery-related encounters, a fungal gorge is more likely to spawn spore problems, a city must be inhabited by recurring shopkeepers who have schedules/memory. Art, encounters and lore are geographically constrained.
- **Sequential terrain-symbol matches:** discover two or three matching carved seals or connected landmarks **in the proper order**, possibly across geographically separated terrain types. Touching them consecutively with a remembered route unlocks a secret area, companion, branch or Edgeworld. A sequence should have discoverable clues, not require raw trial and error. A wrong input can sound an alarm, reveal partial lore or attract a monster, but not hard-lock core story.
- Overworld shape tools interact with cells via preview/confirm, archaeology/revelation or passage clearing. A cross staff can scout a cluster. A hammer may crack a geological diagonal at risk of shattering a fragile artifact. This is not automatically identical to combat damage mechanics.
- Auto-travel along discovered safe paths is welcome. Important junctions, interactions and surprises pause for player agency. No forced click-a-corridor chores.

### 2. Expandable underworlds, dungeons and Edgeworlds

From known overworld landmarks, **portals** lead to procedural spaces whose generation is bounded by a **biome, faction, story tier and entry point**. A fixed abandoned keep may always exist at world coordinate (x,y), with the same recognizable approach and residents, but its lower vaults rearrange or grow depending on seed and history. Edgeworlds are strange pockets, alternate cosmological rules or fantasy side-realms associated with specific breaches, not wholly random unrelated maps.

- Design the static macro-world as a **versioned authored skeleton** and constrain procedural expansions to room graph patterns, deck weights and theme/canon tags.
- A seed is stored per run and per instance. Each dungeon has `siteId`, `parentWorldLocation`, `generationSeed`, `themeId`, `floorTopology`, `encounterDecks`, `revealedTiles`, `clearedFlags`, `residents` and `lootClaims`.
- The generator must preserve meaningful geography (e.g. caves under mountains, drowned crypts under canals), foreshadowed threats, stories/relationships, and reliable exit paths. Do not randomize a specific returning NPC's identity or goal on each visit.
- A **returning player** can revisit a known site with persistent discoveries and changed inhabitants. A new expedition can grow deeper procedural floors while the anchor stays familiar. Repeated reruns must not reset player knowledge of the fixed surface.
- Bosses, mini-game callbacks and unique authored one-off scenes have gating and cooldowns. Use constraints so the party never encounters the same supposedly unique tragedy twice.

### 3. Encounter boards nested inside exploration

A clicked overworld tile might reveal a roaming monster. The game **transitions within the same full-screen game scene** to the memory-match combat board, then returns to the persistent map with a changed tile outcome. A treasure cache might open a special match-lock, a tiny sliding-tile puzzle, a negotiation, or a true Minesweeper deduction chamber. A wandering trader may offer a dangerous choice with **no matching minigame at all**. Selecting a companion can trigger dialogue, trust/debt changes and later callbacks.

State machine:

`world → revealed tile → resolve discovery → {choice | combat-match | riddle | treasure | portal | camp} → aftermath → world`.

Keep the *overworld* map and its saved position resident behind the encounter. Do not hard navigate away to an unrelated web page for every fight. Returning should feel like closing an illustrated encounter within the game camera.

## Character creation, worldbuilding and saves

**Character creation:** player chooses name, appearance/avatar, fantasy origin (cosmetic unless the player unlocks interesting dialogue), class/discipline, initial tool and difficulty/depth. Do not bind strength or skill penalties to body, identity, sex, ethnicity or age. Story acknowledgements validate customization, not generic "Welcome, adventurer."

**Persistent save layers (separate schemas):**

1. **World Save**: known stable map coordinates, discovered sites, unlocked terrain-link sequences, settled world-changing decisions, key NPC relationships, shrine activations and world generation/canon version.
2. **Character Save**: identity/portrait, discipline unlocks, notable reputation, journal of world discoveries, meta-level sidegrade unlocks, deaths/retirements, companion histories, account save slots.
3. **Expedition Run Save**: mutable HP/Focus/Danger, loadout, temporary injuries/curses, room graph, seed, run-specific loot, active companions, encounter log, dungeon deck draw history and floor/depth.
4. **Chronicle**: append-only meaningful player actions, notable past defeats, learned glyph combinations, altered NPC memories, notable relic combos, authored outcome callbacks; the next run can check these without granting raw permanent stat power.

Saves persist at every resolved action/room boundary and on tab/browser departure where feasible; no irreversible server writes for a mere tile preview. Versioned migrations and safe resume after content updates; preserve existing Classic game data and rewards. Provide at least two manual named save slots plus autosave, run archive and convenient rewind to a *safe anchor* if design supports it. Rewind does not erase permanent material consequences or allow infinite loot farming.

**Worldbuilder-ready:** author data as region/site/lore, terrain and encounter manifests, independent of future canonical world definitions. Avoid hard-coded world name, named map/cosmology or final overarching villain. Any future connected fantasy-game world should be able to import these as a **special dungeon module** and share NPC/world state via stable content IDs. Do not build that future game's unrequested frontend or commit its canon.

## The compelling loop, revised

1. See a lush, navigable isometric/top-down overworld with fogged and known tiles.
2. Survey terrain; discover a landmark and an oddity. Decide whether to trigger the suspicious rune.
3. If the oddity is a battle, play the actual match board, positioning shape weapons around bullseyes for remembered-symbol combos.
4. If the oddity is a relic or puzzle, use deduction, sequential terrain-link matching or a short original minigame to open a path.
5. Encounter a recurring character with a specific motivation; choice costs relationship, resource or access, and writes Chronicle flags.
6. Enter a procedural dungeon **rooted in this landmark**; gain one fresh surprise while story callbacks remain coherent.
7. Rest/extract/fail/return with the persistent map improved and new combo revelations. Story, world and future expeditions remember.

**One-session target:** within the first 2 minutes discover a map tile, trigger a meaningful choice, and experience either a miniature match combat or special surprise. Do not force four sequential full match boards before anything interesting happens.

## Presentation standard: an illustrated video game, not a website

- **No new route**: existing `/play/memory` and home/Play links stay. But the **interior of the game** receives a substantial new artistic layout; "no new front end" meant no duplicated second product or entrypoint, not that the existing gameplay visual stage must stay unchanged.
- Full-bleed or container-filling game camera, terrain dioramas, animated fog, dimensional depth, strong painting, art-led character interaction and weapon HUD; avoid generic text cards, dashboard metric strips, big white gutters, SaaS button grids or a multi-scroll web panel.
- Three distinct renderable scenes: **Overworld Explorer** (large grid/map, layered biome art, avatar, compact health/gear/HUD), **Match Combat** (large 4x6–6x6 image grid with weapon-mask projection, enemy portrait/pose and bullseye), and **Discovery / Narrative Cut-in** (full artwork, surprise treasure/character, short consequential dialogue and two or three gamepad-friendly options). Fourth **Minefield Vault** variant for 8x8/10x10 logical clue layout.
- Primary art cannot be a postage stamp. Use consistent painterly fantasy environments and warm tactile UI materials, readable text, responsive phone/tablet/desktop layout, controller/touch/keyboard, screen-reader alternatives and reduced motion.
- Character creator can be an illustrated in-world scene, not a web form. Menus and save management should be game-screen overlays (book, journal, altar), not disconnected admin views.
- Concept mockups should depict the finished experience, clearly marked as **proposed visual direction** rather than live gameplay or completed game art.
- Preserve existing actual match-card ArtImage source; newly authored art requests should cover main landscape tiles, terrain states, secrets, companions, weapons/overlays, boss scenes, loot revelations and narrator/ending vignettes.

## Vertical slice revised for world architecture

Before six floors or a huge map, implement a **small persistent authored overworld** (e.g. 7x7 revealable terrain cells with 4 named landmarks; **working count only**), one dungeon entrance with two seeded interior configurations, at least one portal to an uncanny themed Edgeworld, and three encounter types: a monster that opens the memory-match stage, a special terrain-symbol sequence unlocking a secret, and a narrative treasure/NPC dilemma. Include one 4x6 match board, two weapon shapes and one bullseye, plus one fair nonmemory logic puzzle. A save/load/restart must reproduce map, world and run state.

**First acceptance:** after a complete short expedition, a player can tell you where they went, who they encountered, why they chose the route, which clues they remembered and what changed on the map for the next visit. That is the RPG, not a bigger match scoreboard.
