# Slime City: Square-Grid CCG Comparison Lab
**Working title, not final branding.** Conductor slug `slime-city`. Revised from Silas's 2026-10-30 PT gameplay direction; this document supersedes the 2026-10-29 pentagonal-board proposal.

## Creative compass
A noisy, fluorescent, gleefully excessive fantasy cyberpunk metropolis where genetically engineered catgirls, punk bloodfairies, cybernetic ogres, vampiric gangs, sewer spies and reckless demolition gladiators fight for fame, territory, and Meat. The art direction remains premium illustrated AAA-console rather than a web admin dashboard, with colorful exaggerated comic violence and distinct faction personalities.

**Authoritative change:** The arena is now a **rectangular board of square cells, with orthogonal up/down/left/right movement**. Remove all pentagonal topology, five-sided tile mapping, mandatory turning/facing AP, and five-direction attack/block vectors. Default combat is simple adjacent attack versus aggregate armor. Rich special abilities create depth, not awkward directional bookkeeping. Keep the three candidate victories (flag, boss, rout) in the broader design toolbox, but test simpler win conditions per prototype instead of assuming one solution.

**Do not decide Stratego vs football-style advancing line vs real time in documentation alone.** Build multiple genuinely playable proof-of-concept games using a common roster, card catalog and overworld, then compare experiences with concrete playtests. Choosing a final mode is a subjective human decision **after the variants exist**. Never block reversible development on a design-selection gate.

## What to try first: three distinct playable formats
| Variant | Board | Cadence | Setup and gameplay | First measurable objective |
| --- | --- | --- | --- | --- |
| **BLACKOUT** | 8 columns × 8 rows | Full turn-based | Whole teams begin deployed and **concealed** like Stratego; moving a fighter reveals it. Player chooses square-to-square tactical movement, CPU maneuvers its hidden army. | Claim central flag and return it to base; attrition/rout as fallback |
| **MEATBALL** | 12 × 6 | Turn-based lane rounds | A narrower football field with two endzones. Mana-funded fighters are deployed to home squares, then advance one square along their lanes and fight at end of each full round. | Score 3 breakthroughs into opposing endzone |
| **BLOODRUSH** | 14 × 6 | Timed live rounds | The same team cards and lanes but automatically advancing on a live clock, with Run/Pause and between-tick deployment or specials. | Score 3 breakthroughs against defensive waves |

These names are internal working labels. The current playable preview intentionally uses simplified combat and repeatable cards. **No match result awards persistent Meat, online wins or cards.** The early variants use deterministic fixed decks, not a full CCG economy or tournament balance. Expansion experiments should include alternate board sizes, interleaved turns versus simultaneous orders, concealed placement plus field lanes, monster-as-third-faction, and mixed objectives, but not before the first three variants are evaluated.

### Shared rules for the tests
- Squares have integer `(x,y)` coordinates; one movement step moves only to an **orthogonal** adjacent empty square. No diagonal shortcuts or rotation mechanics. Simple per-creature AP where manual movement is used.
- Mana cap increases round by round, initially 1, 2, 3, ..., capped at 10; exact turn-one tempo still provisional. It pays for creature, spell, trap and equipment cards.
- End-of-round combat is **simultaneous**: each revealed fighter attacks one adjacent enemy, damage `max(0, attack - armor)`. Simultaneous mutual knockouts are legal. Add adjacency/range/splash/status keyword exceptions incrementally only when tests explain them.
- Hidden enemy identity remains concealed until movement, attack, trap reveal or other explicit reveal. The local comparison lab has no networked hidden-state guarantee; a later server-authoritative PvP implementation must redact identities and seeds properly.
- Player versus CPU modes share data-driven cards and deterministic action/tick logs. Real-time is a discrete fixed-tick simulation in the first comparison, **not** a performance-intensive action shooter. Mobile input must remain usable while the clock is running.

## Teams versus colors
Five color philosophies remain from the original pitch, but **team/crew identity is its own axis**. Each team gets visually distinct uniforms, relationships, creature roster, unique special cards, city home turf, opening story and eventual unique campaign. Two highly specific teams are required permanent canon, not background flavor:

| Team | Color school | District | Character / play |
| --- | --- | --- | --- |
| **Gene Riot Catgirls** | Blue · biotech/ambush | Chimera Heights | Genetically engineered catgirls who escaped corporate laboratories; fast scouts, reknit serum, scent mines, catnip overdrive |
| **Punk Bloodfairies** | Purple · fast horde | Needle Alley | Tiny anarchic blood-magic fairies with punk style; swarms, brutal razorwings, bloodwire, moshpit effects |
| **Ironjaw Chrome Ogres** | Green · armor | The Foundry | Giant cybernetic ogres and scrap engineers; plating, bulldozing, body upgrades and overclock |
| **Riot Saints** | Red · chaos | Redline Riot | Demolition punk radicals; seeded volatile blast outcomes and risk/reward |
| **Undertow Intelligence** | Blue · traps | The Undertow | Sewer spy network; surveillance, concealed tripwires, timed sabotage |
| **Meat Exchange** | Gold · control | Crown Market | Corporate corpse merchants and collection agents; debts, contracts, expensive champions |

The two Blue teams illustrate why teams and colors are separate systems. Later teams can express other interpretations of colors without artificially inventing 12 new mana schools. The original five schools (Red chaos, Blue traps, Purple speed/horde, Green cybernetic armor, Gold market control) still matter for card flavor. Creature stats never derive penalties from real-world identities. The roster above provides **three named creatures and three special cards per crew** as the comparison minimum, 36 distinct starter cards; they are initial game-data experiments and are not final balanced, illustrated collectible editions.

## Special card grammar
- **CREATURE**: deploy fighter, cost, HP, attack, armor, AP; fixed short-square movement and a team illustration slot.
- **SPELL**: one-shot damage/heal/seeded chaos/temporary boost with a named target and previewed eligibility.
- **TRAP**: secretly place on a legal square; trigger on opponent entry, reveal and resolve in the shared simulation.
- **EQUIPMENT**: persistently improve armor, AP or a narrowly specified ability of one friendly unit; no open-ended executable scripting.
- Richer mechanics to prototype later: stealth scanning, flying, movement acceleration, summon token, knockback, charge, collision, shield break, friendly-fire chaos, monster lures. Each must have visible counterplay and deterministic replay.

Cards are designed to feel like collectible illustrated artifacts: large hero art, dramatic cost icon, readable combat values, discoverable deck filters and precise asset provenance. Generated art must be confirmed via actual ArtJob/ArtImage before counting it delivered; vector/CSS renderings are interim visualization only.

## City overworld
Build an **interactive city map** connecting each crew and system to place:
- **Chimera Heights**: forbidden genetic towers, catgirl liberation, stealth training and reknit serum.
- **Needle Alley**: bloodfairy punk roofs, moshpit fights, swarm tutorials and split loyalties.
- **The Foundry**: cyber-ogre forge, giant equipment and worker uprising.
- **The Undertow**: surveillance drains and trap-driven mysteries.
- **Redline Riot**: illegal demolitions and randomized gauntlets.
- **Crown Market**: Meat Exchange shops, deck upgrades, faction entanglements and contracts.
- **The Pitworks**: arena matchmaking, boss exhibition, CPU bouts and later 3-win-mode challenges.

The first internal map is interactive district selection plus roster and arena entry, not a completed walkable campaign. Next iterations attach distinct named rivals, city chapter choices, card unlocks and illustrated panoramas. A district's identity should be legible through art rather than a wall of text. Retain short layout and gameplay controls on one screen; deeper content in reachable galleries and help.

## Economy, challenges and campaigns (future milestones)
Meat is an **earned-only fictional game resource**, not gambling or cash. Players earn it through CPU matches and authored missions, buy specific cards or transparent encounter draws, complete daily/weekly/permanent challenges and build collectible decks. No real-money purchases, no paid RNG, no cash-out. PvP direct friend invites require server-authoritative actions, permissions, concealment redaction, reconnect and abuse controls. Public Play, live social challenges and account economy remain separately gated. Distinct campaigns per **team**, not simply palette variations, are the long-form narrative goal. No draft should be reported as completed story content or artwork.

## Comparative playtest / decision rubric
Record these for each mode with multiple player and CPU strategies, short and extended sessions, phone/tablet/desktop input and seeded replay:
1. Does the first meaningful choice happen quickly, and is its effect visible?
2. Can the player understand threats, movement and consequences without reading a rules essay?
3. Is there compelling counterplay to concealment, swarm, armor and card costs?
4. Does a comeback feel earned, or is the first few turns a foregone conclusion?
5. How often are units clogged, games stalemated, or turn times boring?
6. Does the game still feel like a **collectible card battle** rather than arbitrary units moving?
7. Is turn-based, timed, or a hybrid most fun, and at which board size?

Do not silently hard-code the winning mode after one automated match. Deliver **comparative screenshots, test runs and a short decision memo**; get Silas's experiential verdict. Preserve all three playable modes until the mode decision is made, rather than deleting unchosen code before evaluation.

## Delivery and safety
Start with a discoverable **ADMIN-only** `/admin/slime-city` route and matching Admin channel tab. Its initially playable simulation has six teams, 36 prototype cards, seven district selections and the three board/cadence test variants, with clear "local laboratory" state. Pure TypeScript rules should be independently testable, with a Pinia store owning state and timer. Avoid persistent production data or external publishing while design is in flux. Verify changed code through TypeScript, formatting, game tests and 390/768/1440 viewport review when a suitable runnable build is available. A self-hosted Kind Robots merge does not auto-deploy. The first slice is **not** a final CCG, multiplayer service, delivered art set, completed campaigns or Meat economy.

Only after robust comparison and human creative feedback should agents select final combat timing, board geometry/size, win conditions and development priorities. Final subjective game acceptance and public release remain distinct hard human gates.
