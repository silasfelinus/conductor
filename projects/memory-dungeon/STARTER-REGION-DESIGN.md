# Memory Dungeon RPG — Starter Region Design & Playable Slice

**Working title:** *The Cartographer's Folly* (region only; not canon)  
**Project:** memory-dungeon | **Route:** /play/memory | **Authoring date:** 2026-10-22 PT  
**Status:** implementable design proposal. No claim of playable RPG, approved world canon, finished artwork, or generated assets.

**Latest design authority:** This document applies the player's Zelda-style exploration, local thematic puzzle families, forgiving-to-challenging reset rooms, and find-the-difference direction on top of WORLD-AND-EXPLORATION.md and COMBAT-PATTERNS.md. The broader fantasy universe is unwritten. All people, location names, and mythic explanations below are disposable *starter-region working fiction*, not cross-project canon.

## 1. The experience in one paragraph

An original, mischievously strange fantasy adventure presented as a **video game**: a handcrafted landscape appears under carved, face-down map tiles. The player pushes into the fog one reachable tile at a time, learns stable geography, recognizes symbols, meets repeat visitors, and unlocks shortcuts. A revealed tile might become forest, treasure, a trickster, an argument, a monster, a riddle, or a stairway. When a monster or puzzle needs closer attention, the camera dives into a **separate challenge board** inside the same route. Matching cards remains the *only direct-combat resolver*, with pattern-shaped tools and precise bullseyes. Other rooms ask observation, logic, or moral courage. A failed expedition changes a character's immediate fortunes, not the geography they already discovered.

### Four design pillars

1. **World knowledge is real progress.** Fixed named anchors, traversable geography, marks, secrets, and characters are stable across sessions. The player can describe where they have been and why a shortcut matters.
2. **Every reveal has personality.** The overworld is not 121 generic matching cards; it is a map whose squares may reveal terrain, events, creatures and doors. Mix meaningful risks with restful discoveries.
3. **Memory and observation are tools, not chores.** Battles call the original two-card match; special rooms use difference spotting, pair families, rune order, Minefield logic and pattern manipulation. Different cognitive muscles get turns in the spotlight.
4. **Runs are short stories.** Named NPCs carry favors, debts and remembered choices; failures have aftermath; difficult decisions close/open routes. Better equipment changes how a player thinks or recovers, rather than permanently overpowering memory skill.

### Boundary

The main map can *feel* like the top-down, interconnected-world cadence of a classic Zelda adventure but has original art, fiction, mechanics, map and characters. Do not copy copyrighted creatures, room layouts, dialogue, music, or franchise visual identity. Use wacky fantasy comedy with emotional consequence, influenced by the irreverent LitRPG feeling requested, not any author's prose or specific setting.

## 2. Starter-zone scale and geography

**Working region:** The Crooked March, a 11 × 11 fixed square tile grid (x=0..10 west→east, y=0..10 north→south). **121 is the authored map footprint**, not 121 mandatory clicks or encounters. Initial playable critical path visits roughly 18–26 cells, 7 authored landmarks, two little sublevels, one major dungeon and one optional Edgeworld breach.

World coordinates must remain stable **per world version** and per save: coordinate (5,9) always refers to the starting camp, not a random shop on the next run. Art rendering may interpolate scenery between tile boundaries. Only *contents of explicitly instanced encounter pockets* use procedural variants.

### Site atlas (local positions are design coordinates)

| ID | Coordinate | Working site | Biome | Initial function | Persistence |
| --- | --- | --- | --- | --- | --- |
| START | (5,9) | Bent Compass Camp | meadow-road | Create/save adventurer, choose tools, return/extract | Always safe; hub |
| FORD | (5,7) | Lantern Ford | shallow river | Teaches reveal, route-finding and the price of haste | Dialogue choices remembered |
| ORCHARD | (2,6) | The Backwards Orchard | strange woods | Terrain-symbol clue A, difference-room entrance | Landmark fixed, interior variant |
| GROTTO | (2,5) | Reflection Grotto | wooded underlevel | Three connected comparison/matching trials | Local resets only |
| SHRINE | (5,5) | The Unlit Shrine | ruined meadow | First major upgrade, sequence clue, recovery | Cleared once; shrine remains |
| SPORE | (8,6) | Sneeze-Worthy Hollow | fungal ravine | Terrain-symbol clue B, second mini-dungeon | Entrance fixed, chamber layouts seeded |
| TOWER | (5,2) | The Clocktower with No Clock | masonry ruins | Forecasts dungeon threat and shortcut | Recognizable, recurring visitors |
| KEEP | (8,3) | The Receipt-Keep | old stone bastion | First main dungeon, room deck and boss | Same entrance; depths may shift |
| BREACH | (1,3) | The Door that Wasn't There | impossible border | Optional Edgeworld pocket, reached by rune order | Unlock stable; interior varies |

**Road spine**, four-neighbor adjacency unless a disclosed feature says otherwise: START (5,9) → (5,8) → FORD (5,7) → (5,6) → SHRINE (5,5) → (5,4) → (5,3) → TOWER (5,2). West branch via FORD → (4,7) → (3,7) → (2,7) → ORCHARD (2,6) → GROTTO (2,5). East branch via FORD → (6,7) → (7,7) → (8,7) → SPORE (8,6). KEEP route via SHRINE → (6,5) → (7,5) → (8,5) → (8,4) → KEEP (8,3). BREACH is reached from ORCHARD → (2,5) → (2,4) → (2,3) → (1,3) once unlocked. Additional surrounding tiles provide loops, detours, vistas, shortcuts and 1–3 surprises; **no mandatory path depends on blind selection or a procedurally blocked tile**.

**Mandatory unlock:** The KEEP opens through one of **two viable strategies**: (a) activate the matching terrain seals near ORCHARD and SPORE, learning clues from both; or (b) convince the caretaker at the TOWER to open an inconvenient back route, trading one persistent favor or rare carried item. This prevents a puzzle-style hard stop and allows character-driven alternatives.

**Secret unlock:** Three linked glyphs, one associated with ORCHARD, one with SHRINE, one with SPORE, are marked with a memory motif. Once the player has revealed the three, entering their **clue-signaled order** from the map journal opens BREACH. They can click glyphs consecutively in a Rune Focus mode without physically revisiting each coordinate between clicks. Ordinary navigation does not accidentally cancel the input. A wrong sequence reveals which *prefix length* was correct and raises Danger once per attempt, with a cooldown; no arbitrary irreversible lock.

### Overworld tile semantics

A map square has:
- **Underlay:** fixed terrain, blocked/free path, authored coordinates, biome and scenic art reference.
- **Fog cover:** hidden → glimpsed → revealed → visited; once revealed on this save it never reverts to unknown.
- **Point of interest:** authored landmark or seeded one-time/returning discovery from a biome-safe pool, with clear absence for unoccupied tiles.
- **Dynamic overlay:** wandering monster, weather, timed merchant, temporary hazard or world-choice aftermath; this can change without moving the terrain.
- **Rune / clue tags:** persistent world-symbol IDs. They can participate in ordered sequences, family matches and map puzzles without treating every square as an identical card pair.

**Legal reveal:** Starting square and orthogonally adjacent reachable cells are eligible. The camera can *look at* distant fog but cannot interact with a hidden tile across impassable ground. Discovering a tile does not automatically teleport the character there: it reveals its underlay, then the player decides to enter or auto-path along known safe terrain. As an accessibility setting, the Explore button can select from reachable adjacent frontiers without pixel-perfect clicking.

**Reveal costs:** Most safe terrain costs only an interaction, not health or stamina. Risk resides in choosing to **enter** a warned hazard, opening a chest, approaching a roaming foe, or using a broad detection tool. No attritional tax for learning the basic geography. Danger rises with avoidable greed, loud tools, lingering enemies and known hazard choices, and resets/relaxes at camp.

**Reveals are not mandatory matching.** A discovered mushroom tile stays mushroom; a monster tile starts an encounter; a bridge can become traversable; a clue becomes a journal entry. An overworld rune matching objective is a deliberate *landmark interaction*, not a hidden assumption that every grass tile has a twin.

## 3. The loop, playable in five minutes

**Opening 0:00–1:30 (target, not observed):** From a character creator embedded in the game scene, choose an appearance/name, one of three starting disciplines, starter shape tool and independent difficulty/depth. A wry caretaker offers a contract with one clause that cannot be read yet. The player can keep the contract (one protective ward) or burn it (one map clue). Both options later echo in dialogue. The hub shows 3–4 visually explorable frontier tiles.

**Exploration 1:30–3:30:** Click a veiled tile to reveal a path, then find the first small landmark; the player sees where a secret *might* be, even if they cannot open it. A person offers a route tip for a cost, a creature ambushes a side path, and a non-combat trinket is available. The game offers **choices**, not a mandatory gauntlet of full boards.

**Challenge 3:30–5:00:** One short 3×2 or 4×3 memory board, or one 2-difference illustrated puzzle, depending on action. The player earns a map annotation, tool/companion clue, or a new shortcut. Returning to the map restores exactly the same coordinate and fog state. The current goal is clear: investigate two symbols to open the Keep, or find another way.

**Ten-minute promise:** By the first extraction, the player should have 1 distinctive NPC memory, 1 earned upgrade, 1 unresolved mystery, and a route they can trace on the world map.

### Minute-to-minute cadence

A reasonable tuning *hypothesis* is 2–4 exploration reveals per encounter, and an average of one substantial puzzle per 3–5 minutes. Do not fill every hidden tile with a battle or chest. Include quiet landscape reveals, overheard jokes, suspicious but harmless objects, and small meaningful options. Use instrumentation, not arbitrary encounter density, to tune.

## 4. Three interconnected challenge families

The sublevel architecture should feel authored rather than randomly mixing every puzzle style. A player who understands one room learns a language that helps in its siblings. Shared motif, rules and clue shapes; varied consequences.

### Family A: Reflection Grotto (under the Orchard)

**Theme:** deceptive twins, missing details, the difference between *same* and *similar*.

- **A1, The Painted Door:** display two richly illustrated scenes with **exactly two large, intentionally designed differences** (e.g. the key hanging on the wrong hook, the statue holding a coin instead of a feather). Tap/keyboard-select regions or use coordinate names. Correct finds open the door. A wrong accusation marks a misstep but reveals a hint afterward.
- **A2, The Sibling Statues:** 3×2 image matching board where a *pair* means statues sharing an exact crest, while nearly identical faces are decoys. Preview tells the player what counts as a match. An item earned from A1 can highlight the distinctive features for one attempt.
- **A3, The Reflected Bargain:** a returning character offers to leave a trapped creature reflected forever in exchange for the shortcut, or break the mirror to save it while losing the free clue. Either choice completes this branch; future dialogue and helper availability diverge.

**Room-link logic:** Identifying the two differences in A1 reveals a crest clue later used by A2. A2's crest identifies which mirror in A3 can be safely broken. Early rooms teach later rooms rather than representing three random minigames.

### Family B: The Spore Gallery (beneath the fungal hollow)

**Theme:** biological families, deceptive colors, contagious patterns and environmental deduction.

- **B1, Spore Census:** reveal a handful of fungus illustrations; sort them into matching *families* using shape or vein count, not hue alone. Instructions show one clear sample. Family membership is not a binary card-pair identity.
- **B2, The Lung Bell:** 4×3 two-card memory board where different mushroom *kinds* are represented by pairs. Some cards gain visible spore counters: matching an infected symbol safely disarms that hazard, while repeated misses advance a telegraphed contamination meter.
- **B3, The Antidote Cabinet:** choose between two remedies using clues from B1 and B2. One heals the player's party but spends a scarce supply the settlement needs; the other preserves supplies and gives the player a permanent but modest marker clue in this region. Both are valid, with authored world consequences.
- **B4, Optional Deep Bloom:** one larger 4×4 difference-and-memory hybrid. Completing it reveals an optional wandering companion or a secret treasure; refusing is a valid exit.

### Family C: Receipt-Keep (main dungeon)

**Theme:** absurd magic bureaucracy, debts, old bargains and precise deduction. The place is funny and sometimes cruel, not merely a gag machine.

The **entrance hall and guardian chamber are authored**, while intermediate rooms are chosen from separate **Encounter**, **Monster**, and **Treasure** piles constrained to the site, floor and story flags. The first slice selects 5–7 rooms plus the guardian, including:
- One combat battle introducing weapon footprint **preview, anchor and bullseye**;
- One choice encounter with two defensible costs;
- One trap/treasure with an optional matching lock;
- One room from the **Reset Suite** below;
- One quiet lore/character interlude;
- One boss who changes the meaning of a known crest without moving already learned card faces.

A room does not need a match board if its story works better as dialogue or a find-the-difference puzzle. Rare rooms should be special enough to remember.

## 5. Reset Suite: pressure without erasing learning

The player explicitly requested rooms that reset after too many failures. These resets must communicate rules upfront and respect the distinction between **persistent map knowledge**, **run progress** and **temporary room state**.

| Category | Example | Trigger (first prototype) | What resets | What persists |
| --- | --- | --- | --- | --- |
| Gentle reset | Statue pairing lesson | 3 misses; warning at 2 | Unmatched face-up cards flip closed; same positions | Correct pairs, learned clues, map, rewards claimed |
| Pattern reset | Shuffling Chessroom | 4 misses; warnings at 2 and 3 | Only unmatched cards undergo an **animated, fully observable** row rotation | Matched cards, clue journal, room completion flags |
| Shrine loop | Crooked Clock Chamber | 5 misses or player chooses Restart | Local mechanism and puzzle sequence restart from a **documented deterministic variant** | Discovered hints, unlocked safe path, used supplies, map |
| Danger pressure | Guardian's Audit | Enemy's clearly shown Tempo budget runs out | Combat phase board returns to start of phase | Health loss, boss phase learned, earned guard and treasure constraints |

**Anti-frustration:** Within a run, a room may soft-reset once, then must offer a visible escalating alternative: a limited hint, a paid helper action, a retreat, a different route, or a voluntary hard-mode retry. Hard resets are rarer, clearly labeled and should never delete legitimate treasure the player already claimed. Harder difficulty changes warnings or hint economy *predictably*, not covertly.

**No exploit:** Reentering a reset room does not respawn claimed chest rewards, regenerate consumables, change hidden identities for free, or reroll a procedural boss until an easier version appears. The room's puzzle RNG and current transformations are part of the persisted expedition seed/log.

**No false memory failure:** If cards are moved, show the physical move clearly. A puzzle must never punish a player for remembering coordinates accurately when the game silently rearranged them.

## 6. Find-the-difference: a first-class room mechanic

This mechanic relies on artistic specificity. A polished scene can conceal two to four clearly identifiable changes: object added/removed, swapped emblem, altered pose, a shadow facing the wrong direction, or an inconsistent architectural feature. **Do not use random pixel noise or color-only changes.**

**Interaction:** Side-by-side pictures or a user-toggleable overlay with the same framing; zoom/pan and clear 44px+ tap targets; answer regions defined as polygon or rectangle hit areas. A correct find marks its counterpart in both views and remains marked. A wrong tap advances the visible Missteps budget but is not an instant failure. After two wrong guesses, offer a hint that narrows a broad region; a returning companion may supply a one-use clue at a relationship/resource cost.

**Variations:** Spot changes between remembered scene and newly visited location; catch a mimic impersonating a friend; compare maps and notice a moved stair; discover which treasure has been tampered with. These can trigger fights, change NPC trust or unlock a safe path.

**Validator:** Store authoritative original/changed image references, exact answer regions, hint regions and accessibility clue strings. Confirm every answer region is visible at all intended resolutions; screenshots must test tapping each; false-positive regions outside intended answers do not count. Text/audio alternative describes the same **set of discriminating features** without handing over the solution and supports keyboard-based candidate selection. No puzzle solved only by red/green or by a rapid timer.

## 7. Combat remains memory-driven; tools alter the problem

**Default:** two-card sequential matching as existing Classic mode. The RPG introduces clearly previewed alternate weapon shapes on the *nested* combat board.

| Item / tool | First playable action | Reward for skill | Tradeoff |
| --- | --- | --- | --- |
| Scout / Dagger | Choose first card, then a second anywhere | Exact pair gives reliable match damage | Slow, no special footprint |
| Twinblade | Preview 2 vertical adjacent cells; commit reveal | Correct matched pair involving marked tip cell triggers precise Guard | Low reach; adjacent blind pair unlikely |
| Mason Hammer | Preview 3 diagonal cells with center bullseye | Complete matching pair including bullseye staggers enemy | Longer recovery; extra exposed singleton |
| Lantern Charm | Briefly reveal a 2×2 square but no automatic attack | Reveals board information for future precise use | Limited Focus charge |
| Later Cross Staff | Center + 4 orthogonal cells | Multiple predicted pair matches may charge Focus | High cost/rarity; not starter |

Do not interpret a weapon's spatial *reveal* as automatically equal to multiple matches or damage. Shape targeting is strategic only if remembered spatial positions beat blind spam. A correctly predicted pair must decide actual combat damage; a bullseye enhances that earned hit. No tool should obsolete ordinary two-card matching, and weapons cannot create free infinite peeks.

**Room vs weapon geometry:** In the overworld, shape tools can scout adjacent *terrain categories* or interact with reachable mechanisms, not automatically deal damage to whatever the tile hides. In combat, shape tools modify card reveals/targeting on the dedicated board. In a logical minefield room, a narrow bullseye may disarm a deduced trap, while a broad strike risks breaking valuable scenery. Make the current interaction mode explicit.

## 8. First five earned conveniences, in useful order

The **player improves**, and the adventurer improves too. These first upgrades should change decisions, traversal and recovery rather than merely multiplying damage.

1. **Surveyor's Chalk** (FORD, first meaningful choice): 3 reusable map annotations per camp visit; notes persist in the Chronicle so players can mark suspected secrets.
2. **Lens of Discrepancy** (GROTTO A1/A2): one optional difference hint per puzzle; one stored charge, refreshed at camp; it highlights a *region*, not exact answer.
3. **Echo Locket** (SHRINE): on one match-combat attempt per encounter, hold one previously exposed card face visible for two player actions; cannot stack and does not auto-match.
4. **Diagonal Hammer** (SPORE B2): another weapon mask and bullseye strategy, acquired by choosing a modest trade or completing the optional fungus test, not by grinding raw XP.
5. **Trailhook** (TOWER or KEEP shortcut): interact with authored grappling anchors, crossing a **specific known obstacle**; upgrades the navigational graph, not combat numbers.

The player need not earn all five on the same route. A companion may help in lieu of a tool. Each acquisition has a scene and an actual first use within a few rooms, so it never feels like a numerical checkbox. Sidegrade choices at later floors can tune hint vs shield vs exploration reach.

**Important:** Powers reduce *friction*, not the need for memory. A high-skill player can finish without them; a new player is helped without being patronized. Persistent knowledge/shortcuts are stronger long-term rewards than permanent raw health/damage inflation.

## 9. People, choices and emotional hooks

Character names and identities are working placeholders. Roles should become richer than a shopkeeper repeating a tutorial.

- **The Ford Caretaker** knows two ways across the river. You can pay with a map note, accept a favor-debt, or help repair a bridge. Later, they remember which promise you honored. Their advice about the Keep is incomplete but not dishonest.
- **The Reflection Prisoner** appears in A3. Freeing them loses the cheap shortcut but introduces an optional traveling ally who remembers your mercy. Leaving them preserves convenience but causes an uncomfortable return visit.
- **The Fungus Physician** requests scarce medicine needed by their village. Claiming it for your own party improves this run; donating it changes future visits and a character's trust, but makes the next fight harder.
- **The Keeper of Receipts** at the main dungeon is attempting to preserve names against a spreading bureaucratic curse. Defeating them does not automatically prove they were wrong; the player's prior choices unlock negotiated and costly alternatives.

**Rule for writing:** Each important choice must change at least two of: immediate run resource; world route/character state; later authored reaction; available helper/tool; Chronicle revelation. No "obvious saint vs selfish fool" framing. If a skill check fails, the scene continues in an interesting *different* direction, not a generic "nothing happens" message.

**First-region narrative structure:** Recover a missing page from an adventurer's travel ledger. When found, the page lists someone the player met under the wrong name. Returning the page to the Ford Caretaker saves one person's memory but reveals another's complicity. Burn it and recover a map shortcut with a harder future relationship; carry it into the Edgeworld to learn its provenance but expose the party to a new hazard. These are three distinct first-run aftermath beats, not final cosmology.

## 10. Difficulty, depth, failure and next runs

**Separate knobs:** Difficulty affects number of card pairs, misstep budgets, threat pacing and help; Depth affects count of procedural dungeon floors/chambers, encounter density and ending ambition. Keep the existing four Classic difficulty labels in Classic mode. The RPG can use descriptive equivalents without silently changing Classic score/life math.

| RPG difficulty | Start board | Reset cues | Help |
| --- | --- | --- | --- |
| Story | 3×2 or 4×3 depending on room | Clear warning and slower threat | Hint available and safe extraction |
| Adventurer | 4×3 rising to 4×4 | Full warnings as designed | Earned tools, one paid retry |
| Veteran | 4×4 rising to 4×6 | Shorter budget, still telegraphed | Scarcer Focus and rests |
| Nightmare | Up to 6×6 in set pieces | Higher pressure, never hidden swaps | Optional difficult routes; fairness unchanged |

**Depths:** For the *first region* the default short expedition is one main dungeon floor plus branches (~15–25 minutes target), a full expedition opens two or three additional seeded floors (~35–60 minutes target), and Endless is deferred until save stability, balance and content variety exist. These are planning estimates, not measured durations.

**Loss:** Defeat returns the adventurer to the last safe anchor with lost *unbanked* expedition items, changed mood/reputation where authored, and a saved Chronicle entry. World fog already uncovered stays uncovered; major world decisions and unlocked paths persist. Avoid repetitive death-click-farming of treasure. A player can choose a fresh character while retaining discovered world/Chronicle knowledge according to save-slot rules.

**Run memory:** After each extraction/defeat, log decisive encounters, learned terrain-order sequences, NPC debts, important relic combinations, visited sites and discovered ways to use weapon patterns. Future run stories draw from those flags. Meta-unlocks grant new strategic *possibilities*, not permanent guaranteed victories. On repeat visits, suppress forced prologue and repeat-only tutorial cards.

## 11. Minimal save and generator contract

Suggested serializable, versioned IDs (TypeScript types/properties to agree in implementation, not yet coded):

- WorldMap: worldVersion, regionId, x/y tiles, fixed terrain/siteId, revealedFog, traversability, discoveredLandmarks, shortcutState, runeStates, worldFlags.
- Character: characterId, name, cosmetic appearance, starting discipline, portable tool unlocks, companion relationships, journal.
- Expedition: runId, characterId, worldVersion, difficulty, selectedDepth, currentCoord, siteInstanceId, floorIndex, seed, deck draw pointers, active room, revealed/matched combat cards, room reset state, Focus/HP/Danger, inventory and pending consequence.
- Chronicle: immutable event IDs, event sequence/version, action and outcome, involved NPC/site/content IDs, timestamp/seed metadata, portable discoveries and credited rewards.
- SiteInstance: parentWorldSiteId, biome constraints, layout seed, authored anchor nodes, generated branch nodes, encounters by ID, room state, claimed reward IDs.

**Conservation rules:** An overworld coordinate is never reshuffled by a run RNG. A dungeon instance cannot orphan its entrance, produce an unreachable mandatory key, generate a unique NPC twice, or allow a seed change to respawn claimed treasure. Save, reload, and replay a seed must preserve all chosen encounters, NPC reactions, used aids, monster positions, and room reset transformations. Reject or migrate saves with incompatible schema/content versions with a safe fallback, not data loss.

**Cross-project boundary:** The future fantasy worldbuilder will provide names/cosmology/lore, but this dungeon module provides self-contained working Site/Region/Encounter manifests, stable IDs and data migrations. Never hardcode a final global map, god, king, or world name here.

## 12. Concrete room inventory and art requirements

**First vertical slice** (content-authoring minimums, not implemented counts):

- Stable 11×11 authored base region; 9 anchor sites from atlas, with START/FORD/ORCHARD/SHRINE/SPORE/TOWER/KEEP indispensable and other sites optional.
- 15 authored overland discovery events across forest, river, ruins and fungus, including at least 5 quiet findings; 3 wandering monsters, 3 treasures, 3 NPC dilemmas, 2 map-rune symbols plus optional ordered triplet.
- Reflection Grotto: 3 linked authored rooms and two visual-difference image pairs with checked answer regions.
- Spore Gallery: 3 mandatory linked rooms + 1 optional deeper chamber.
- Receipt-Keep: first playable procedural floor with ≥6 varied encounter records, separate encounter/monster/treasure piles, one reset room, one character callback and one boss.
- Optional BREACH: 1 three-room Edgeworld sample with consistent root/portal, one rule variation and a worthwhile reason to revisit.
- One 4×3 memory-match combat, two distinct spatial masks and bullseye, one deliberate non-combat logic challenge and one find-the-difference room.
- Three first-run aftermath vignettes, one named recurring character interaction with a callback on return, and an autosave/load demonstration.

**Artwork that will be needed *after* this document is approved for art planning:** an authored-overworld master layout, each biome's isometric tile kit and fog states, camping hub, reflective grotto and fungal chambers, procedural keep room backdrops, choice/treasure cinematic art, character portraits and expressions, combat image-card backs/fronts, shape/bullseye overlays, 2+ precisely authored difference-image pairs, puzzle clue symbols, Edgeworld gateway and a character creator. Each scene/image needs a stable asset ID and art prompt with region/site/room binding. Concept art should show *gamescreens with the actual camera and HUD hierarchy*, not illustrated moodboards or web mockups.

## 13. Adversarial acceptance tests

1. Run the same 100 seeds twice. Fixed region coordinates, accessible roads and authored site identity never drift. Procedural room order is deterministic per seed.
2. Starting from (5,9), BFS verifies every mandatory site is reachable under each legal gate strategy, even if the player declines a companion.
3. Revealing each possible overworld tile yields a valid type; only enter actions launch fights/traps. The game returns to exactly the prior position after combat or narrative resolution.
4. A completed local room never rewards a second treasure copy after soft/hard reset, reload, defeat, rewind or same-run reentry.
5. Every difference puzzle has exactly its authored answer targets; tapping any target works in phone/tablet/desktop layouts. Distractors never trigger unintended positives.
6. Resets warn in advance; movable cards visibly transform; no hidden shuffle makes remembered positions false; all mandatory puzzles have escape/recovery.
7. No blind guess is necessary for mandatory Minesweeper-like logic rooms; a solver can finish using revealed clues.
8. Weapon masks have visible valid anchors, sensible edges, and test that accurate memory outperforms random targeting across 4×3, 4×4, 4×6 and 6×6 nested boards.
9. Partial save → reload → resume produces the same map fog, character state, pending room, earned reward and Chronicle entries as uninterrupted play.
10. At least three outcomes can be reached with different ethical tradeoffs; those outcomes visibly change the next trip, not merely the ending text.
11. A novice can reach a satisfying 5-minute checkpoint without solving multiple complete boards. A veteran still has meaningful tactics.
12. Classic mode, art deck selection, existing scores, achievements and reward flow remain unchanged at /play/memory.

## 14. Decisions for art and implementation to respect

**Locked for this slice:** fixed overworld landmarks; hidden tiles that reveal non-pairs; nested memory combat with spatial targeting/bullseye; thematic sublevels; limited fair resets; find-the-difference; branching consequential story; character creator and durable world/character/run/Chronicle saves; one existing /play/memory frontend; real full-game screen presentation.

**Working hypotheses to test, not canon:** 11×11 size, coordinates, named region/people, room counts, fail thresholds, first tool placement, scene dialogue and boss motives, whether maps use strict square tiles or softer visual edges. The future fantasy world's final lore is deliberately unspecified.

**Next after this design document:** user-requested **image concept art**, beginning with a master overworld gameplay screen and a matching combat + reset/difference room pair. Do not generate the artwork in this document-only task.
