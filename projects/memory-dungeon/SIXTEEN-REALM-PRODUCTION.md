# Memory Dungeon — Sixteen-Realm Production Bible

**Authority:** Silas's 2026-10-23 PT creative session, superseding the explicitly provisional setting and cast in `DESIGN-BRIEF.md` and `STARTER-REGION-DESIGN.md`. **Stage:** authoring blueprint, not shipped content or a promise that 1,600 locations are implemented. Keep `WORLD-AND-EXPLORATION.md`'s save, geography, nested-combat and accessibility contracts.

## The story we are making

An androgynous adult from contemporary Earth has their life and body traded to **Morrow**, a fey changeling desperate to be a data researcher in a world without magic. The protagonist wakes in Morrow's existence and journeys through sixteen sinister, vivid fairy-tale realms. Photographs recovered during tile exploration reveal what Morrow is doing with the stolen life: fired from work and painfully awkward in friendships at first; then finding better work, authentic friends, romance and, devastatingly, parenthood. The final decision must acknowledge the children's bonds rather than granting a consequence-free reversal.

**Register:** darker Grimm, `Fables`, `Fable`, American McGee's `Alice`, `She-Ra and the Princesses of Power`, filtered into wholly original setting, prose, gameplay and visual design. Strange, adult, clever, funny, sometimes frightening, emotionally sincere; no indiscriminate gore, contemptuous gotchas, sexualization of the cast or morality-by-tooltip. Fairy-tale roles are expectations to interrogate, not destinies to obey.

**The party:** Scylla and Charybdis ("Char") are identical twin mermaids who have taken princess forms. Their faces, sturdy farm-built frames and mannerisms match; different coloring from distinct magical waters confuses surface-dwellers, not them. Scylla is meticulously proper; Char is committed to unmistakable goth culture, not simply a black dress. Both are kind, fast-witted instigators, confidently overqualified for every problem that their long-suffering attendant actually solves. **Oren Pike**, their royal headsman, never removes his executioner's hood, carries his axe, and is a logistical genius who makes impossible expeditions happen. No obligatory hidden trauma, unmasking or invented backstory. The twins' origin in Silas's *Mermaids of Venice* takes precedence over any future contradictory material. Their introductions and human/merfolk transformations must be illustrated and treated as narrative scenes, not exposition cards.

## Campaign progression

| # | Realm | Dungeon | Fairy-tale reversal / core conflict | Mechanical distinction | Morrow photo beat |
|---|---|---|---|---|---|
| 01 | Briar Marches | House That Remembers (existing Rootbound Vault site) | Wolves protect a frightened village from something worse than wolves | Remembered names; linked leaf seals | Job dismissal and a ruined gathering |
| 02 | Hearth & Hunger | The Red Oven | The charitable baker feeds villagers with pieces of their history | Recipes, exchange and ration puzzles | Halfhearted applications; an apology |
| 03 | Glass Orchard | Mirror-Root Palace | A ruler poisons beauty itself to prevent compulsory perfection | Identical-looking traps, honest reflections | A discouraging interview, new curiosity |
| 04 | Undertide Crown | The Drowned Conservatory | Mermaid succession depends on what the law calls "identical" | Tides; shared glyphs; twin disputes | The first reliable research mentor |
| 05 | Cinder Borough | Midnight Carriageworks | A godmother offers mobility through debt-bound magic | Timetables and transformation costs | A promising new job |
| 06 | Candle Fen | Wickmother's Abbey | Children govern a society that treats adulthood as a curse | Light and age states | A difficult but honest friendship |
| 07 | Carnival of Debts | Carousel of Teeth | Visitors exchange future joys for past losses | Probability with disclosed costs | Celebration without humiliation |
| 08 | Ironroot Mountain | The Last Forge | The seven miners' sleeping giant keeps their land alive | Crafted loadouts; resource tradeoffs | Professional success, loneliness |
| 09 | Winterglass Reach | Palace of Lost Winters | A queen froze a city to save it, then lost track of the danger | Delayed triggers and thaw routes | A meaningful first date |
| 10 | Bellspire City | Thousand-Bell Spire | A storyteller's tower broadcasts secrets in the public interest | Signal patterns and misinformation | A new relationship becomes real |
| 11 | The Red Hunt | Horned Keep | Heroic hunters create monsters to sustain the hunt | Predator/prey role reversals | Shared apartment, mutual care |
| 12 | Looking Lake | The Mirror Depths | Name and body exchanges mirror the protagonist's dilemma | Identities, double agents and masks | A family begins to form |
| 13 | Thorned Crown | Sleeping Cathedral | A princess sleeps willingly to imprison an ancient hunger | Dream / waking topology | Preparing for parenthood |
| 14 | Paper Kingdom | Index of Names | Every citizen must live the part assigned in official stories | Contract clauses and redaction | An adoption/birth preparation, no full reveal |
| 15 | The Between Sea | Ferry of Two Worlds | Lost lives wash ashore, including people who never requested exchange | Irreversible bargains and consent | Signs of children; still ambiguous |
| 16 | Unwritten Country | The Last Door | Nobody can author another person's future without consequence | Combined mastery; compassionate final choice | Morrow with children; full truth |

The photographed Earth timeline is **32 fixed discoveries (two per realm)**, each associated with a stable coordinate. Order-sensitive revelations are journaled chronologically when found out of order. Do not reveal the children unambiguously before the final-world reveal; earlier photos may plausibly foreshadow family life without falsifying the mystery. The photographs are rewards for discovery, not expendable items or random drops.

## Stable production targets

| Surface | Target | Acceptance |
|---|---:|---|
| Authored overworld positions | 16 × 64 = **1,024** | Every coordinate has stable ID, geography, primary hook, meaningful action/state change, and artwork contract |
| Authored dungeon positions | 16 × 36 = **576** | Each 6×6 baseline room has a different job; graph includes loops, shortcuts, escape and a resolvable climax |
| Distinct enemies | **96** | 4 regular + 1 elite + 1 guardian per realm; overlapping mechanics may be reused, not identical personalities |
| Distinct item definitions | **128** | 16 relics, 32 equipment charms, 48 consumables/tools, 32 keys/mementos; no runaway permanent stat boosts |
| Permanent unlocks | **64** | 4 per realm; knowledge, routes and optional tactics instead of pay-to-win power |
| World photographs | **32** | Two fixed locations per map; time-ordered journal with late reveal protected |
| Realm achievements | **64** | 4 per realm with separate gallery artwork; ending achievements additional |
| Secret areas | **16** | One substantial discoverable area per realm; not mandatory for first clear |
| Optional Edgeworld adventures | **4** | One per act; revealed through fair clues, not blind tile guessing |
| Ending variants | **12** | Three ethical decisions × four relationship/world-state epilogues, each illustrated |

The per-map **primary purpose budget** is 8 main scenes, 8 sidequests, 12 danger/combat, 8 puzzles, 8 secrets/lore, 8 treasures, 6 landmarks/travel, 4 companion developments, 2 Earth photographs. These are planning allocations, not permission for a scene to perform only one function. Every tile must have at least one authored response; no mandatory board match merely to read a line of description.

## Gameplay and balance

**Maps** keep canonical 8×8, currently numbered `1,1` through `8,8`, with fixed meaningful locations. Paths remain traversable and the same landmarks recur across runs. Biome-bound procedural expansions live **behind** stable dungeon sites, not in place of geography. An accessible map, no mandatory guess logic puzzles, no arbitrary speed gate and forgiving failure continuations are required.

**Dungeon** rooms mix negotiation, observation, two-card matching combat, sequence logic, memory puzzles, hazards, recovery, treasure and choices. Sixteen dungeons may each introduce one distinctive twist but must remain learnable; enemy pattern tools use the existing combat engine.

**Difficulty** is independent from **expedition depth** and adjusts clue visibility, incoming pressure, forgiveness and optional challenges. Difficulty does not alter a character's capability based on identity or body. Short sessions should make a decision early; a substantial run should feature a major scene about every 10–15 minutes. The 25–35 hour main-campaign target and 50–65 hour completionist target are hypotheses to test, not measured playtime.

**Consequences** use `World Save`, `Character Save`, `Expedition Save` and append-only `Chronicle`, with versioned migrations from current Briar saves. Players may fail, retreat or negotiate rather than face unrecoverable story locks. No unique tragedy can replay infinitely for rewards.

**Endings**: (1) reclaim Earth identity, displacing Morrow from a family that loves them; (2) remain by choice in the storybook world; (3) negotiate shared time or identities, only with the informed consent of everyone affected. Each has four epilogues grounded in actual campaign relationships and sacrifices. No apparently flawless spell should erase the dilemma.

## Delivery gates

1. **Authoritative canon + compatibility:** adopt this bible, reconcile old placeholder Pip/Index story without deleting already-earned progress, map coordinate IDs or Classic mode; save migrations before site renames.
2. **Briar vertical slice:** all 64 stable entries, accessible graph, tutorial, twin/Oren introductions, two Earth photographs, 36-room House That Remembers, puzzle/choice and at least two resolutions. Current two-room Rootbound Vault must grow without overwriting saved `vault-1`/`vault-2` outcome IDs.
3. **Reusable content engine:** typed map/dungeon manifests, choice prerequisites and consequences, IDs, world/room validation, seed/state replay tests and asset manifests.
4. **Realm production:** deliver subsequent three worlds in Act I, then Acts II–IV in groups of four, requiring writer's pass, playtest and art coverage per realm before claiming them complete.
5. **Quality:** adversarial multi-seed tests (expert, novice, pacifist, greedy, speedrun, completionist), replay/resume, mobile/tablet/desktop one-screen art-first verification and real art delivery tracking.
6. **Release:** a green reversible PR can merge, but production deployment and public promotion remain separately human-gated. A merged source branch is not a verified live deployment.

**First production document:** [BRIAR-MARCHES-FIRST-WORLD.md](./BRIAR-MARCHES-FIRST-WORLD.md) is the complete 64-position writers' registry and the first 36-room dungeon story skeleton. Each position below still needs code-level authored choices/art, test coverage and QA to be marked shipped.
