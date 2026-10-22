# Memory Dungeon: The Forgotten Depths — Design Brief

> **2026-10-22 PT latest direction:** Read `WORLD-AND-EXPLORATION.md` first. The game now has a **persistent explorable overworld of discovery tiles**, with matching combat/puzzles **nested inside** exploration. Procedural themed dungeons and Edgeworlds extend from **fixed** landmarks. The broader fantasy universe has not been built; the title `The Forgotten Depths`, named supporting cast, premise and three-floor linear descent below are strictly **non-canon examples to revise**, not final worldbuilding or a mandatory plot. The existing route stays, but its inner video-game scene will be visually redesigned.

**Project:** `memory-dungeon` | **Kind Robots route:** `/play/memory` | **Type:** single-player, offline-resolvable, seeded narrative roguelite RPG | **Status:** design direction, not implemented functionality | **Date:** 2026-10-22 PT

## Promise

A customizable adventurer descends into a sentient dungeon that steals names and memories. Explorations advance automatically between illustrated, consequential room cards; decisions determine risk, relationships, and the encounter decks. Battles are settled by the *existing* two-card memory-matching game, not ordinary dice attacks. A lost run is a story chapter, not an erased afternoon.

**Design test:** A player should be able to describe a run as a sequence of people, dilemmas and surprises, rather than "I matched ten boards."

## The existing game is the foundation, not a casualty

Verified in `kind_robots` on 2026-10-22 PT:

- `stores/memoryStore.ts` has four difficulties (Goblin Picnic, Haunted Hallway, Mimic Audit, Butterfly Catacombs), scaling card-pair counts, lives, streaks, special challenges, power-ups, awards, art card sources and scores.
- `components/pages/memory-dungeon.vue` is the current game surface; `content/channels/arcade/experiments.md` mounts it at `/play/memory`.
- `components/home/home-visitor-directory.vue` *already links* Memory Dungeon to `/play/memory`. Preserve this link and game, not another top-level front end.

Build an **RPG mode on the existing route and board**, preserving an immediately playable Classic Match mode and its current rewards. Refactor only behind a versioned encounter/board adapter; do not let RPG economy rules silently alter Classic scoring or achievements. Existing art collections can supply match-card images. No LLM or paid image call is needed while a player explores, battles or solves a room. Pre-author text, art prompts and narrative branches.

## The fiction: the dungeon remembers you

A buried archive holds things the world has forgotten. Its doors are made of misplaced promises; its curators claim each vanished adventurer willingly deposited their name. Deep within is **the Index**, a keeper who insists that true memories belong to the dungeon. The player's apparent task is to retrieve a lost name, but each descent uncovers that someone else's memory must be surrendered to recover it. The question at the end is not "Can I defeat the monster?" but "Whose story will I preserve?"

Tone: uncanny fairytale, quick dark comedy and surprising tenderness. Existing goblin accountants, the butterfly oracle, mimics and skeletons remain recognizable, but may evolve into complicated recurring people. Never make every joke a quip, nor make a companion just a passive stat modifier.

**Initial recurring cast** (write scene and relationship bibles before full production):
- **Pip, the Goblin Bookkeeper:** records the debts of abandoned parties, friendly unless asked what makes a debt fair. Can become an ally, rival or merchant.
- **The Brass Knight:** animated, badly repaired armor carrying somebody else's vows. Protects you but refuses to forget a promise.
- **Vesper, the Moth Cartographer:** draws maps that change after each visit. Offers shortcuts at the price of secrets; loyalty is earned.
- **The Index:** face-changing custodian and final antagonist or tragic steward. Remembers alternate run outcomes in fragments, not omniscient exposition.

Recurring characters have three tracked axes, **trust**, **debt**, and **revelations**. Their scenes must have personal stakes and at least two defensible choices. Personality and identity are not numerical disadvantages. Companion dialogue changes at thresholds, and at least one companion may oppose a seemingly optimal player choice.

## Start a run

1. **Character creation:** name, portrait/avatar from pre-authored selectable designs, cosmetic origin and one starter discipline. Customization must have an immediate narrative acknowledgement. Identities/body types do not determine penalties.
2. **Choose difficulty** (the current four names can be kept, renamed or surfaced with explanatory subtitles): changes clue exposure, board complexity, enemy pressure and recoverability. **Choose descent depth separately:** Short Expedition = 3 floors (~15–25 minutes target), Full Descent = 6 floors (~40–60 minutes), Endless = unlocked later. These are *design targets*, not measured durations.
3. **Experience an authored opening:** a debt collector returns a memory the character does not recognize; the gatekeeper asks who deserves to own it. The opening choice sets first relic or relationship rather than moral alignment.
4. **Explore automatically** through a seeded node/room map after every resolved room. Show upcoming fork choices where meaningful; do not require manual corridor clicking.
5. **Resolve rooms** via decisions, matches, combat, item use, companion action or a combination. Show clear consequences before committing irreversible decisions. Allow safe confirmation/cancel before the action actually resolves.
6. **Camp, extract or push deeper** at each floor exit. Extraction banks discoveries and some resources; defeat preserves a meaningful chronicle and knowledge, with less material return.
7. **Aftermath:** an illustrated ending vignette summarizes the choice that mattered, who survived, what changed in the dungeon, and one intriguing lead for next time.

## The room engine: exploration with pressure and agency

Each floor is a procedural but **seeded** sequence of ~5–8 resolved rooms, then a floor guardian or narrative confrontation (tune through playtests). Build from three user-specified shuffled piles plus bounded authored story injections:

| Pile | Examples | Principal choice |
| --- | --- | --- |
| **Encounter** | shrine, stranded traveler, locked memory vault, faction messenger, moral dilemma, riddle | Investigate, bargain, sacrifice or leave |
| **Wandering Monster** | skeletal collector, mimic, memory leech, oathbreaker | Fight, hide, negotiate or spend scarce aid |
| **Treasure** | trapped coffer, cursed relic, abandoned journal, hoard guarded by oath | Claim, share, trade, seal or walk away |

A director uses weighted draws with floors, tags, prerequisites, cooling periods, unique flags and encounter history. A visible **Danger** track rises with time, noise, failed attempts and greed. Higher Danger increases wandering-monster draws and makes already announced threats act more frequently; it must never secretly rewrite the just-revealed room. Treasure streaks attract risk; battles and riddles cannot appear in unfair, unavoidable chains. Guarantee a refuge or meaningful extraction option before lethal story beats.

Room results modify health, supplies, curse, trust/debt, card-board conditions, deck weights and floor secrets. Seeds + an append-only event log reproduce room order and dice-like random choices for debugging and replay. Record versioned rules/content IDs with saves so balancing later does not corrupt active runs.

**Example room:** The Bell Chest contains a relic and a handwritten confession. Taking both causes a persistent memory curse and raises Danger. Giving the confession to Pip clears his debt but means a later witness won't trust you. Leaving it earns the witness's favor and loses the relic. If the player chooses the chest, a miniature three-pair memory trap determines *how much damage* the mistake causes, not which moral option was correct.

## Matching IS combat

Use the existing two-card flip/pair mechanic as the only resolution for direct attacks. RPG encounters may differ in tactical pressure and objective while preserving honest memory skill.

- **Match:** deals attack damage or charges the chosen class/companion skill; doubles as Guard, Insight or Mending when the player selected those effects before revealing a pair.
- **Miss:** consumes a **Tempo** beat. Enemies telegraph a future action; after N beats they strike, steal a visible card clue or add a curse. Avoid punitive HP drain on every single miss, which makes big boards a slog.
- **Streak and special challenge:** create Focus for tactical skills and harder optional objectives. The current Lantern, Shield and Oracle's Eye power-ups remain recognizable and are adapted into RPG resources through an explicit compatibility layer.
- **Enemy intentions:** show "attacks in two misses," "reshuffles one unmatched pair after three turns," or "grabs an item if ignored." A shuffled board must provide a clear warning and fair learning opportunity. Never reshuffle already-matched pairs.
- **Encounter variants:** a duel needs X damage, a swarm asks for a streak to control adds, a guardian demands specific rune pairs, a spellbound ally must be rescued before damage, and a mimic offers risky false treasure.
- **Telegraphed consequences and accessibility:** animations never conceal cards before the agreed viewing interval; no surprise hidden timers as default. Color, sound or speed alone never encode identity. Support keyboard, touch, reduced motion, large cards, screen reader labels, difficulty adjustments that don't demean players.

Memory *skill* should matter more than grind or equipment. Equipment modifies risk and tactical choice, not auto-matches the board. Run-specific powers are a way to recover a mistake, trade health for clues or change objectives, never an infinite skip-match generator.

## Progression: restrained, combinatorial, and story-bearing

**Run stats:** Vitality, Focus, Supplies, Danger and one slot for a Curse. Avoid six additional meters. A character can carry **two relics** and bring **one active companion**; a second person may appear in camp/story but should not introduce a second combat UI. No inventory Tetris.

**Three starter disciplines** (same board, distinct decisions):
- **Warden:** correct matches may be banked as Guard before a predictable enemy strike.
- **Seer:** trade Focus for a one-use peek or to bind an exposed rune briefly.
- **Trickster:** convert a streak to loot leverage or redirect one pending enemy effect.

Per floor, offer **one level-up choice from three** upgrades with a meaningful opportunity cost. Use bounded rank caps and sidegrades rather than permanent damage multipliers. E.g. Warden's Last Stand lowers Guard efficiency for a one-time revive; Seer's Recollection increases clue duration but also Danger; Trickster's Borrowed Luck consumes supplies on a failed gambit. Companion abilities improve with trust, shared scenes and *run-earned* experience, not only arbitrary XP thresholds.

**Metaprogression = knowledge and relationships first.** After every run, write a compact **Chronicle**: chosen identity, seed, depth, allies, major decisions, relic combinations, discoveries and endings. Unlock alternate openings, routes, encounter variants, rumors, new starter disciplines, and limited new relic synergies; do not permanently boost raw damage or render future boards trivial. Discovering "the Bell remembers Pip" might enable a unique conversation plus a Bell + Bookkeeper relic combination in a future run. Characters recall rumors and debts, but there are no contradictory multiverse claims by default.

**Failure has material:** on death show what the hero learned, what relationship survives as rumor, and what a returning dungeon NPC now knows. Ensure the player can retry rapidly, skip repeated prologue after first completion, and see a never-before-seen possibility without needing to survive six full floors.

## Narrative architecture and content volume

Author a **three-floor vertical slice** before scaling to six:
- Floor 1: The Ledger Halls, learns risk/reward, introduces Pip and an NPC in trouble.
- Floor 2: The Library of Borrowed Voices, companion conflict and first faction trade.
- Floor 3: The Vault of Unwritten Names, first memorable boss, an ugly choice and **at least three** outcome vignettes.

Vertical-slice target: **24 distinct room records** (8 encounters, 8 monsters, 8 treasures), **6 additional authored rare/surprise scenes**, **6 riddles/puzzle prompts with valid solutions and failure continuations**, **3 recurring characters with at least 3 context-aware scenes each**, **3 guardian/boss variants** and **3 genuinely distinct end states**. Each important room/choice/outcome gets an image reference and prewritten prompt; runtime can show a reusable fallback where generated art is pending. These counts are initial design budgets, not claims of completion.

Story tags support callbacks like `saved_witness`, `owed_pip`, `gave_up_name`; each finale selects 1–2 salient callbacks for a bespoke paragraph and corresponding art prompt. Prefer surprising recontextualization and credible consequences over hundreds of interchangeable endings. Riddles must be solvable from information on screen, and failure must open another path at a cost instead of freezing progression.

## A single great sample run

- The opening identifies a Warden who does not remember promising to protect a stranger.
- Floor 1 treasure gives a brass bell, but touching it announces the party to wandering monsters. The player keeps it.
- Pip appears at a crossroads: help him collect a debt from a frightened skeleton, or pay it yourself in supplies. The player pays.
- A memory leech attacks. First correct pair charges Guard; a mistake advances its telegraphed theft; a second match kills it. The player *chooses* to protect Pip instead of maximizing damage.
- A shrine riddle reveals the bell's former owner. Vesper offers to draw a safe route but asks for the owner's name. Player refuses; route becomes longer, relationship warms with Pip.
- At the guardian, the Bell + Pip combination permits a negotiation unlocked by a past-run revelation, **not** a free victory. Player sacrifices a relic to save the skeleton. Extraction banks a remembered promise and a new opening scene for the next run.

This should be replayable with a different class, branch, companion or sacrifice and feel like a different *story*, not merely a different shuffled set of pictures.

## Build sequence and acceptance

1. **Foundation:** map current store contracts, isolate Classic mode, define typed, serializable seeded RPG state and deterministic reducer; add a text-fixture simulator first. No new route.
2. **Playable vertical slice:** start flow, 3-floor director, room choices, combat adapter, one companion, camp/extract/death, save/resume, journal. Use the current UI and scale up its art-first stage, not a new homepage.
3. **Story and variety:** expand content records to targets, authored branching companion arcs, riddles, relic interactions and endings. Each path needs an interesting miss/failure consequence.
4. **Polish:** card art, accessibility, mobile/tablet/desktop 1-screen viewport, seeded adversarial runs, board-balance calibration, exploit tests and progression fairness.
5. **Release:** Conductor's project stays active until reviewed against goal. Making material externally public or deploying production changes remains human-gated.

**QA invariants:** seeded replay exactly reproduces draws and consequences; all depths can terminate; every encounter has at least one legal outcome; no unreachable non-optional locks; save/load at room boundaries matches uninterrupted play; room draw cooldowns and one-off character beats work; death/extraction preserve the Chronicle; no infinite free Focus/health/loot loop; no board re-roll exploit; all branching moral alternatives have distinct consequences; existing Classic mode behavior and score/reward flow remain intact.

## What to resist

- Do not make the player solve a full board for every door, chest and conversation. Keep combat and selected stakes as matching challenges; let exploration breathe.
- Do not add a dozen RPG stats or permanent numerical upgrades. The game must reward better memory, not hours logged.
- Do not make "randomness" a substitute for writing or remove meaningful player choice with automatic exploration.
- Do not force lengthy repeated intros; the first 90 seconds should contain a decision and a memorable character.
- Do not create another front-end route, dashboard or detached version of Memory Dungeon just to display this system.

## Additional defining mechanic: geometrical attacks and minefield vaults (Silas, 2026-10-22 PT)

The follow-up direction materially expands the match-combat architecture. Weapons use visibly previewed **spatial masks**, not ordinary fixed damage rolls: one sword reveals two vertical cells, a hammer reveals three along a diagonal, and other equipment uses crosses/L-shapes. Every mask has a visible **bullseye** coordinate: when a deliberate strike resolves a real matching pair at that marked location, it gets a special crit/stun/guard reward. Revealing a symbol in the bullseye without its matched counterpart is information, not free damage. Larger masks trade precision for information, cooldown and risk; correct remembered positions must outperform blind attack spam.

Deduction rooms may use *large Minesweeper-like* X-by-Y boards with safe-tile numbers, flags, hidden dangers and a route/relic goal. They must be solver-verified so mandatory progress does not require a blind guess. In these rooms exact bullseye placement can defuse danger and a careless area strike may threaten treasure or companions. Use a zoomable/contained stage and accessible grid navigation. Puzzle failures create consequences or alternative paths, rather than arbitrary run-ending coin flips.

Memory-matching remains the combat resolver. Non-combat riddles and logic puzzles (sequence, truth testimony, spatial route, nonograms/sliding tiles or original echoes of other Kind Robots minigames) can diversify exploration without requiring another page. The authoritative mechanics and fairness tests are in COMBAT-PATTERNS.md.
