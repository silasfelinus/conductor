# Slime City — Digital Coliseum CCG
**Working title only.** Permanent title, logo and public presentation remain undecided. Conductor slug: slime-city. Created 2026-10-29 PT.

## Elevator pitch
Above a toxic post-apocalyptic megacity, gladiator clans fight inside televised pentagonal death pits. Players collect flamboyantly grotesque creature, spell, trap and equipment cards, deploy combatants secretly, reveal and maneuver them on later turns, and watch all exposed fighters unleash **simultaneous directional violence at the end of each full round**. Three rival objectives reward different kinds of tactics: steal the flag and deliver it home, slay the arena's colossal neutral monster, or rout the other fighter force. Between battles, explore colorful slum districts, fight the AI, earn **Meat**, collect cards, and play distinct faction campaigns or challenge other players.

Think tactical chess with theatrical card reveals and a Saturday-morning-punk megacity turned up to 11. Inspiration is tonal and mechanical reference only; all rules, art, terminology and characters must be original.

## First principles
1. **Single-screen AAA console feel.** The board and fighters, not forms, dominate a 16:9 stage. The active card hand and turn controls remain reachable at 390/768/1440/XL widths. Cinematic, detailed illustrations, readable directional arrows, distinct silhouettes, snappy card flip/strike/death animation, and accessible reduced-motion equivalents.
2. **Tactics over hand luck.** Facing, placement, tempo, concealed intent, the three win paths, and predictable damage are legible. Colored factions are asymmetric without hiding counterplay. Deck-building creates surprises, not unavoidable wins.
3. **Earn in game.** Meat is fictional earned currency, never a cash-out or real-money wagering mechanism. Battle rewards, story, quests and card unlocks are attainable without purchase. Random encounter admission costs and returns are transparent and do not use paid currency.
4. **Authored faction lives.** Each campaign is its own outrageous city story rather than the same dialogue with a palette swap. A living city map joins battle, encounters, shop, collection and multiplayer.
5. **Reproducible and honest.** Versioned cards/rules, server-authoritative seeded RNG, replay logs, source-traced artwork, adversarial tests and realistic asset-progress reports. Concepts and queued images are not finished cards.

## Five chromatic factions (initial canon candidates)
| Color | Working faction | Identity | Tactical play |
| --- | --- | --- | --- |
| Red | Riot Saints | Chaotic fire-jugglers, mutated daredevils, demolition cults | Random effects with displayed possible outcomes, splash damage, chaotic redirection and risky power spikes |
| Blue | Undertow Intelligence | Surveillance witches, sewer spies, amphibious saboteurs | Face-down traps, misdirection, reaction windows, positional snares and information asymmetry |
| Purple | Midnight Brood | Vampire punks, rat swarms, goblin blitz crews | Low-cost mass deployment, fast action-point turns, flanking and sacrificed hordes |
| Green | Ironjaw Foundry | **Cybernetic ogres**, junk-surgeon smiths and irradiated scrap colossi | High armor, modular equipment, directional shield plates, pushing and slow unstoppable advances |
| Gold | Meat Exchange | Corporate corpse merchants, arena bosses and gilt-masked enforcers | Resource leverage, extortion, expensive champions, capture-point control and attrition |

Faction colors are rules-readable, never the sole carrier of identity. Dual-color decks are a later balancing exercise; start single-color plus neutral cards. Each faction earns specific counters to swarm, traps, armor and costly champions. Creature types can include goblins, ogres, vampires, rats, undead, mutants, cyborgs and other weird-city species. Each faction includes protagonists, antagonists, supporting cast, art bible and a unique campaign ending matrix.

## Board geometry: five directions must be real
Regular pentagons cannot tile a gapless Euclidean arena. Use a **Cairo-style irregular pentagonal tiling** or an equivalent validated edge-to-edge pentagonal topology with explicit edge-neighbor mapping, each cell a true five-sided playable polygon and up to five traversable edges. The first map is a symmetric compact Coliseum with both bases, a middle flag lane and an offset monster pit so objectives compete rather than overlap.

Store an adjacency graph with each edge index 0–4 mapped to neighboring tile and its reciprocal edge; check geometry validity, reciprocity, collision, blockers, rotations and rendering at every viewport. Orientation is a unit's edge index, never a screen-relative compass guess. A creature's directional attack and block vectors rotate with its facing. A tile's five edge labels remain consistent with the combat HUD. Coordinate effects such as push/teleport/pathfinding through graph neighbors, not rectangular-grid shortcuts.

## Turn, mana, concealment and action economy
**Design interpretation to prototype and playtest:** round 1 has 1 maximum/spendable mana, round 2 has 2, and each subsequent round gains 1 to a cap of 10; unspent mana does not carry across turns. The original brief mentions both one-cost cards in round two and two mana in round two, so this is an explicit *provisional assumption* rather than a confirmed rule. Tutorial/onboarding will show the chosen progression.

Each full round has Player A's turn then Player B's turn (alternate first player by seed/round or provide compensating initiative); each receives mana refresh for that round. On a turn, spend mana playing any affordable number of cards, rotate/move already revealed units within per-unit action points, lay traps, equip or cast. Creature placement begins **face-down and inactive** in legal deployment cells; show owner and card back but hide identity. It may not reveal on the turn it is deployed. On a later owner turn, a player may reveal it for free, face it, then spend that unit's AP to move, rotate or use explicit abilities. A newly revealed fighter participates in that full round's final combat. Face-down fighters do not attack, do not count as revealed for target effects unless a card explicitly permits it, and cannot silently move. Visibility and collision behavior must be specified in the engine and shown to both players, not improvised by the UI.

Movement to an adjacent free tile costs 1 AP; rotating one pentagonal edge step costs 1 AP. A card's action points refresh on its owner's next turn (not both turns). Directional ranged attacks and special abilities consume explicit AP/mana as printed; the normal edge attacks below are automatic at the end of every full round. Equipment modifies visible vectors, AP, status or keywords with meaningful tradeoffs.

## Simultaneous end-of-round combat
After **both** players end turns: trigger pre-combat effects; snapshot all revealed surviving fighters, orientation, neighbors, damage vectors and directional block vectors; resolve **all five edge attacks simultaneously** from that snapshot; apply damage, knockouts and aftermath once, with deterministic logged effect ordering. A fighter killed during resolution still delivers its snapshotted damage. No procedural first-mover edge advantage.

Each unit has HP, AP, cost, attack[5] and block[5]. Printed vectors are in *unit-relative edge order*, with facing/front identified clearly. On each side, collect all incoming attack points through that edge, then apply that side's block allowance for the round to the aggregate: damage = max(0, incoming - block). Block refreshes next combat; it is not an infinite per-hit negation. Explicit Piercing, Shield-break, Splash, Friendly-fire and Armor-bypass keywords may override this with logged precedence. Default is no friendly-fire unless a red chaos effect states it. Persistent statuses tick at a deterministic phase.

**Illustrative cards:** Ratpack Vermin (1 cost, 1 HP, 2 AP, attack [1,1,1,1,1], block [0,0,0,0,0]) bites any neighboring enemy, regardless of facing. Iron Centurion (3 cost, 3 HP, 2 AP, front attack 2, other directions 0, block [1,1,1,1,1]) can absorb the first point of incoming edge damage each combat; turn it to threaten a single neighbor. Exact balance is provisional. Show in-place five-edge damage/block overlays, damage forecasts, health, legal moves and the next automatic attack outcome; never hide the possibility that two units kill one another.

## Three independent victory routes
- **Flag extraction:** claim the central banner with an eligible revealed creature; carry it along the pentagonal network and deliver it to the owning base. Carrier restrictions, dropping and steals must be deterministic and visible.
- **Slay the Beast:** the arena's oversized neutral nightmare has distinct HP, five-edge attacks, telegraphed behavior and an objective award to the responsible player. It retaliates against both sides, including swarms and traps; boss kill directly ends the match (unless a clearly specified alternative tournament rule is selected).
- **Rout:** incapacitate the opponent's effective fighting force and prevent immediate redeployment, using a clearly shown surrender/attrition rule to avoid cheap round-one wins while both players have empty fields. A proposed test rule is two consecutive cleanup phases after round 4 with no live or deployable fighter. Revisit this after seed-stable AI and PvP playtests.

Win evaluation occurs **after** simultaneous cleanup. Define and test exact tie precedence (e.g., simultaneous flag deliveries or flag plus boss), with a neutral draw/tiebreak policy rather than arbitrary resolution order. At least one tutorial showcases each objective and its counterstrategy.

## Cards, collections and deck rules
Four primary card types: **Creature** (board fighter), **Spell** (instant or scheduled effect), **Trap** (concealed tile/edge trigger with reveal and counterplay), **Equipment** (attached to fighter, modifies directional vectors, HP/AP or keywords). Each has immutable ID, set, revision, color, rarity, art provenance, cost, keyword version, localized rules copy, collection ownership and deck legality. Runtime effect definitions are data-driven but restricted to an audited effect vocabulary, not arbitrary executable card scripts.

Prototype: a compact curated neutral + five-faction starter pool and one legal deck per faction. **Suggested** first live balance target: 30-card decks, 2-copy normal limit and 1-copy legendary limit, 5-card opening hand, mulligan, 1 draw per turn; all of these are trial rules, not user-confirmed requirements. Test empty-hand stalls, overdraw/fatigue, duplicates, trap loops, edge geometry and faction-lock abuse. Provide searchable collection gallery, faction codex, visual deck-builder, copy-count indicators, card craft/unlock sources and match-history collection milestones.

## Slime City overworld
A genuinely illustrated traversable **city map**, not a tile-menu web dashboard:
- **The Pitworks**: AI coliseum training and ranked-ish rival brawls; repeated fights award bounded Meat.
- **The Ironjaw Foundry**: cyber-ogre campaign, equipment and armor-upgrade quests.
- **The Undertow**: blue spy traps, sewer intelligence and hidden-information training.
- **Night Market / Blood Alley**: purple horde campaign, vampiric rival crews and faction relationships.
- **Redline Riot**: red chaos gauntlets, high-risk random combat modifiers.
- **The Meat Exchange**: gold syndicate campaign, shop/card packs or transparent direct card offers, deck-building and daily contracts.
- **The Rotting Crown**: citywide neutral beast chapter, cross-faction climax and rotating PvE challenge.

Available actions from map: start AI battle, faction campaign chapter, buy/unlock cards with Meat, open collection/decks, challenge another user, pay Meat to pull a clearly labeled **PvE encounter**, claim daily/weekly/permanent challenges, read progression and discover secrets. Map travel uses brief animated zoom/pan and large district key art but no time-wasting navigation friction. All actions remain accessible in a controller-friendly one-screen console shell. Different faction campaigns have unique authored dialogue, opponent decks, bosses, reversals, endings, and postgame replay.

## Meat, challenges and multiplayer
Meat is awarded based on recorded outcomes, objective completions, quests and loss consolation. Economy is capped/rate-controlled against repeat farming; avoid pay-to-win and make card acquisition explainable. Random encounters bought with Meat display cost, encounter pool and minimum rewards in advance, retain a deterministic per-user server seed, and never require payment in real money.

Daily, weekly and evergreen achievements have versioned criteria and server-verifiable progress; display rollover in Pacific time, avoid dark-pattern streak pressure, and keep archival earned rewards. Multiplayer starts with direct friend challenges and matched-turn, server-authoritative move validation, hide-card protection, per-match replay/RNG receipts, concession/timeout resolution and disconnect recovery. Any ladder or public matchmaking, real-money purchases, chat, moderation or promotion is a **separate human release gate**.

## Experience, art and audio
Art direction: saturated toxic neon, chunky high-fidelity 2.5D comic-painterly creatures and distressed industrial sculpture; a Judge Dredd-sized metropolis filtered through grotesque, humorous fantasy. Full-bleed character cards feature collectible close-up art, foil-like faction lighting, angular stat chrome and readable damage direction arrows. Giant beast has distinctive multi-cell scale and cartoonish excessive combat feedback without relying on gore for readability. Use differentiated body types/identities and original designs, not recognizable franchise copies. Rich sound design optional; mute and reduced motion always available.

An initial visual pass should include project icon/card/hero, at least one district panorama, five faction banners, arena terrain map, boss centerpiece, rat/centurion/cyber-ogre portraits and card backs. All requests specify dimensions and provenance; **no generated files, ArtJobs, live card assets or gameplay are claimed delivered by this brief.** Queue via the existing art pipeline only when actual tools are available and inspect delivered ArtImages before reporting complete.

## Implementation architecture
Kind Robots is the gameplay host (Nuxt/TypeScript/Prisma/Pinia). Begin with an internal /admin/slime-city preview and a complete illustrated playable duel, not public Play promotion. Isolate a pure TypeScript rules engine from Vue rendering. Version map layouts, game seed, player inventory/deck, turn commands, reveal state, AP/mana, directional effects, journal and victory outcome. Use legal-action validation on server for multiplayer and replay deterministic seeded commands for debugging; tests compare replay hashes and adversarial edge cases. Persist user progress through authorized scoped endpoints, never client-only authoritative inventory. Reuse Facet taxonomy and ArtImage/ArtJob provenance rather than copying invisible assets or inventing art delivery.

## Development gates and success
1. A satisfying, actually playable first duel and mobile/desktop art-first screenshots (not emoji placeholders).
2. Five faction starter decks and three proven, balanced, accessible victory strategies through seeded adversarial playtests.
3. Explorable single-screen map, one authored faction story slice, inventory/shop/challenges and transparent Meat economy.
4. Complete five campaign paths, durable player collection, safe user challenges, verified art provenance, visual QA at 390/768/1440/XL, gamepad/touch/keyboard, reduced motion, and load/reconnect tests.
5. **Subjective design acceptance** and **public deployment/community release** are different human gates. Merely creating this project does not approve either.

## Explicit design decisions still open
- Final brand/title.
- Whether first-round mana is 1 (the prototype default) or round-two unlocks the first cast.
- Combat balance numbers, boss tie resolution, draft deck size and opponent-rout rule.
- Whether the art direction should lean further comedic, grotesque or pulp-sci-fi.

All four can be prototyped and tested reversibly without blocking the project.
