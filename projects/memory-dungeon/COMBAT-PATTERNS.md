# Memory Dungeon RPG — Combat Patterns, Board Geometry and Puzzle Contract

**Date:** 2026-10-22 PT. Companion to DESIGN-BRIEF.md. These mechanics are **proposals for prototyping**, not shipped systems.

## New player direction

Silas: explore tools which uncover multiple cards at once, spatial weapons that carve patterns on a larger X-by-Y grid (a two-vertical-cell sword, a three-cell diagonal hammer), different match challenges, callbacks to Kind Robots games, and non-memory logic puzzles. This is a core combat-design priority, not optional future flair.

## Why the geometry matters

In basic memory match, **information** comes from flipping chosen cards and **success** comes from recalling earlier reveals to match a pair. A two-card simultaneous reveal changes information economics: it removes the need to pick the second card after seeing the first, but grants a spatial clue about two coordinates in one beat. A three- or five-cell reveal gathers yet more information, yet cannot be spammed for free or memory ceases to matter.

For N hidden cards containing N/2 random pairs, a k-cell *blind* shape contains, in expectation, `k(k-1)/(2(N-1))` complete pairs, regardless of shape. On 6x6 (N=36), two cells contain 0.0286 expected blind pairs, three contain 0.0857, five contain 0.2857. Shape only becomes strategic if the player can act on previous card-location knowledge, board landmarks and enemy intent. Therefore evaluate success against a *remembered map*, not merely blind random reveals.

Geometry should also alter tactics through **shape-constrained targeting**: after learning that cards A and B sit two rows apart, the player might need to rotate an L-shaped spear attack, burn one Focus to rotate a hammer, move an enemy's marked tile or save an artifact until a formation lines up. One-size-fits-all large blasts must not dominate precision.

## Recommended first ruleset: Scout, Commit, Resolve

**Two modes on the same RPG combat board:**

- **Scout** (baseline Classic-like move): player reveals one cell, then a second *chosen after seeing the first*, at any coordinates. If identical, they match, deal the standard memory-based attack and disappear/lock. On a miss, show both for a fixed readable interval, hide, then advance the enemy's telegraphed Tempo.
- **Weapon strike**: the player previews a shape mask (position, rotation, legal boundary) *without seeing hidden identities*, then **commits**. Reveal every cell in the mask at once. Matching pairs fully contained in the footprint resolve automatically for a hit; unmatched cards return face down after a fair interval. A striking player can deliberately target known pair positions. Multi-match attacks grant a bonus, with a strict per-attack cap, and visible overkill feedback. Strikes consume the enemy Tempo and perhaps Focus/cooldown based on their pattern.
- Later test a **hybrid variant**: a strike only damages a pair the player explicitly names among known tiles, while the rest of its footprint reveals information. Choose the variant with greater earned-memory skill spread and lower blind-spam success in automated tests. Avoid inventing an extra reflex-timing minigame.

Separate actions in state and event log: `preview` is free and reversible; `commit` freezes anchor/rotation/weapon; `reveal` is observable; `match` is deterministic; `damage` applies combat modifiers; `tempo` resolves the telegraphed enemy intention. No double-use of one pair. Never count arbitrary random unverified shapes as an automatic victory.

### First weapon family to prototype

| Tool | Shape / selectable footprint | Utility | Price and weakness |
| --- | --- | --- | --- |
| **Dagger / Scout** | 2 arbitrary selected cells, sequential | Exact control and second choice after first reveal | Lowest burst damage and no formation bonus |
| **Twinblade Sword** | 2 vertically adjacent cells; rotate to horizontal as upgrade | Reliable low-cost positional strike; 1 Guard even without a pair (tentative) | Narrow footprint; adjacent matching pair is rare on an unknown board |
| **Rune Hammer** | 3 cells along one diagonal; optional reverse diagonal | Reveals an extra clue, staggers one enemy action on a match | Longer cooldown; uncovered singleton is not a free match |
| **Hooked Spear** | L-triomino / 3 cells | Reaches around obstacles, may mark one exposed cell for the next action | Limited rotation or positional prerequisites |
| **Seer's Staff** | Cross of 5 cells (center + N/E/S/W) | Fast information discovery; two completed matches can charge an active skill | 2 Focus or 2-turn cooldown, higher threat exposure |
| **Memory Lantern** | Reveal the chosen 2x2 square briefly | Scout tool, no automatic damage unless upgraded | Limited charges; cannot endlessly map entire board |

Weapon graphics must visibly preview affected cells **before** commit. On edges, either disallow invalid mask placement with clear cue or show the exact clipped shape and reduced cost/effect; never silently alter target cells. Rotate with keyboard/touch buttons. On 4x4, 4x6, and 6x6 boards, use valid even playable-cell counts. If introducing a 5x5 board, mark one obstacle/empty slot so the remaining 24 cards still form 12 pairs.

### How shape weapons earn their place

- **Weapon damage** is primarily driven by accurately predicting or explicitly selecting a pair, not the number of revealed cells.
- **Big area tools are limited by Focus, cooldown, threat, or board hazards**, not arbitrary paywalls.
- **Small tools gain an independent benefit**, such as Guard, precise scouting, cheap use, or setup for a combo, so a three-cell hammer does not mathematically dominate a two-cell sword.
- **Environment matters**: mirrors show swapped card coordinates, slime blocks a column, treasure runes punish hitting the wrong symbol, an archivist locks one row, a leech remembers the last pair. Obstacles alter shape choices while keeping puzzle clues truthful.
- **Boss behavior must be legible**: e.g. "in two actions the Librarian seals the middle column" enables strategic repositioning. Explicitly telegraph board mutations; never punish the player for faithfully remembering a tile position that was secretly moved.

## Companions and meta-builds change the geometry, not just numbers

**Pip (ledger):** after the player reveals a complete pair, he can mark a coordinate on the next board; skill progression lets him inscribe one protected tile. Debt/trust determines whether he charges a price.

**Brass Knight (guard):** banks one correctly targeted pair as Guard to prevent a scheduled enemy strike. An oath violation costs the Knight trust, potentially losing protection.

**Vesper (navigation):** once per floor shifts a whole row by one position *with a preview of the transformation*. A remembered pair that previously didn't fit a hammer pattern may now fit. She might demand a map fragment, creating a story choice.

**Combination examples:** Bell relic + Pip unlocks a debt-negotiation story route and marks one tile; Vesper + Hooked Spear can rotate one pattern for free after a precise scouting action; Brass Knight + Twinblade can turn a guarded attack into a counterstrike on a successfully predicted pair.

No combination should reveal all pairs repeatedly. New runs unlock *ways to play and story access*, not permanently higher damage.

## Riddles and other logic challenges

Memory remains combat's exclusive resolution mechanic, but **non-combat** rooms can ask very different things. Each puzzle has a visible rule, legible answer and interesting failure continuation:

1. **Sequence lock:** reconstruct 4–6 glyphs using clues from earlier rooms. A prior-run journal entry can reveal a hint, not the entire answer.
2. **Truth-teller gate:** compare three NPC accounts and deduce who is concealing the key. Wrong accusations affect relationships.
3. **Spatial vault:** slide/rotate a small set of mirrors or rune tiles to guide a beam. Companion power can make an alternative solution possible.
4. **Path constraint:** draw a route across a miniature room grid without revisiting rune colors; practice deterministic reachability before shipping.
5. **Memory echo:** briefly study a pattern, then reconstruct it (a conscious remix of memory, not the ordinary pair match).
6. **Mini arcade callback:** an illustrated, compact, self-contained version of an existing Kind Robots puzzle mechanic (slide-tile, nonogram or pattern logic) housed in the dungeon interface. Keep it original, integrated and quick; do **not** send players to another route mid-run.

One or two puzzle rooms per short run is enough. Most rooms must remain encounters, choices, combats, discoveries and surprises rather than exhausting the player with homework.

## Enemy design as changing cognitive challenges

- **Mimic:** reveals a tempting high-value tile that may be an enemy marker; the player decides whether to attack or inspect.
- **Mirror Wraith:** occasionally reflects the pattern mask across one axis, telegraphed **before commit**.
- **Grave Scribe:** covers a previously seen coordinate in ink but cannot secretly swap its underlying identity.
- **Clockwork Collector:** demands a run-specific pair of symbols in a prescribed order; a generic hit deals reduced damage.
- **Memory Leech:** on a telegraphed turn remaps two *visibly specified* coordinates; an alert player can update their remembered map.
- **The Index:** phase-based guardian alternates between pairing, logic, and personal sacrifice, with no unavoidable blind guessing.

## Test scenarios, not just feature tests

For every board size and weapon:
- Compare blind random, remembering accurately, remembering 60% of observed cells, and deliberate shape-targeting play. Skill should strongly beat blind play.
- Compare use rates, damage, information gained, Focus spent, and encounter duration. No dominant pattern across all monsters.
- Verify every shape has at least one valid placement, including edge/corner and rotated placements, and no hidden out-of-bounds hit.
- Verify no weapon makes a 6x6 board solvable purely by indiscriminate scouting; cap large reveals and test resource loops.
- Verify save/replay restores remaining hidden identities, weapon cooldown and last revealed cells exactly.
- Verify touch/keyboard/grid screen reader access and reduced-motion timing.
- Verify Classic Match scoring, lives and reward system are unchanged.

**Prototype decision gate:** retain the simplest ruleset that makes an accurately remembered board meaningfully more powerful than an unknown board. Simulated board runs and real adversarial playtest observations, not an aesthetic preference, decide whether weapon shapes are *attacks*, *reveals*, or both.

## Bullseyes, precision damage and Minesweeper-style danger rooms (Silas, 2026-10-22 PT)

**Creative direction:** "a weapon can have a stronger hit if the image is inside the bullseye space ... having a giant minesweeper type screen for some levels, you can almost have to puzzle out to not mess up a solution."

### Bullseye is a position the player understands, not a random crit

Every weapon mask may designate one or more **sweet-spot cells** relative to its anchor. The preview must show the exact primary cell(s) and the peripheral coverage before commit. The damage/skill effect depends on what *the player correctly remembers and deliberately targets*, not on a hidden random crit probability.

Recommended prototype:
- A weapon's footprint reveals N cells. Complete matching pairs in the footprint are resolved according to the base combat rules.
- A complete pair that includes a marked **bullseye coordinate** gets an enhanced hit, guard effect or specific status (not a guaranteed extra match); a matched pair away from the bullseye is an ordinary hit. If the bullseye reveals an unmatched card, it gives information but no automatic critical.
- On some enemies, the player must target a telegraphed **specific symbol** in the bullseye (e.g. strike the oath sigil exactly at the hammerhead) for a stagger or pacification. Do not require guessing an unseen symbol to unlock mandatory progress.
- Some legendary items can offer offset or double bullseyes as a tradeoff to area size or tempo cost. Allow pattern rotation and clear touch/keyboard anchoring; target regions should be much larger than finger precision.

**Test case:** When a player has remembered two equal images in positions (2,3) and (4,3), the selected shape might capture both but put the wrong image in its bullseye. A more deliberate rotated strike should reward the player's knowledge. Compare mean turns/damage for correct-memory versus random targeting to validate.

### Dedicated puzzle-floor modifier: The Minefield Archives

Certain deeper floors or special vault rooms replace the small match stage with a **large, scroll-contained or zoomable grid** (e.g. 8×8 or 10×10). A Minesweeper-style room contains **reliable local clue numbers**, safe tiles, hidden traps and a goal path or relic. The player must deduce safe squares, decide whether to bypass optional loot and select weapon footprints without triggering known danger. It is *not* just a giant normal memory board.

- Floor draw announces this room type and its special rules. Board generation is seeded.
- Reveal a safe tile to uncover an adjacent-hazard count. Let players flag suspected mines and use visible known clues to reason forward.
- The solver/validator must establish that **mandatory objectives can be completed by logic, without a required blind guess** from the initially disclosed clues and subsequent deductions. If the generator cannot guarantee this, offer a visible hint/alternative route rather than disguising chance as logic.
- Weapon-mask strikes on these floors interact with hazards. A bullseye strike can **disarm** a correctly located trap, but broad accidental coverage can trigger a warning, curse or damage. Before commit, show known risks, shape, sweet spot and whether the action is reversible.
- Avoid catastrophic instant death on the first unknown mine. Use escalating, telegraphed consequences and a recoverable exit; optional treasure can carry voluntary risk.
- The player may need to protect a tile rather than clear it, route around a fragile clue, or remove just one precise trap. Nonlethal errors should alter the story or room resources.
- Accessibility: expose clue counts and coordinate navigation in text/ARIA; flags distinguishable by more than color, keyboard and touch accessible, no precision timers.

### Combinations worth prototyping

- **Needle Rapier:** only 1–2 cells, but when the marked image sits on the bullseye it deals high precision damage. Ideal for careful recollection, weak for blind scouting.
- **Mason's Hammer:** three diagonal reveals; a correctly placed center glyph stuns an armored enemy but missing the center lets it retaliate.
- **Surveyor's Lens:** reveals the hazard count around one cell without attacking. Synergizes with the Minefield Archives and a companion who remembers board changes.
- **Bombardier's Grimoire:** a 2×2 blast can remove multiple hazards but destroys nearby treasure unless an exact central pair is identified first.
- **The Oath Bell:** rings when a previously revealed image is centered on the sweet spot; it amplifies the damage but advances the dungeon's Danger track.

Treat these as candidate effects. The *smallest fun, provably fair ruleset* wins after playtest. A large board is appropriate for an occasional set piece, not for every corridor battle.

## Prototype results (t-006, 2026-10-23 PT)

The pure engine is `kind_robots/utils/memoryDungeon/combat.ts`, with `utils/scripts/verifyMemoryDungeonCombat.test.ts` (`npm run test:memory-dungeon-combat`) as its contract. It implements the first ruleset (strikes are **both** attacks and reveals: pairs wholly inside the footprint resolve, the rest of the footprint is information). The hybrid "name the pair" variant is not built; the numbers below already meet the decision gate, so it stays a later option, not a requirement.

**Rules the prototype settled**

| Rule | Value | Why |
| --- | --- | --- |
| Pair damage | 2; +2 when the pair touches a bullseye cell | Damage follows the pair found, never the cell count |
| Per-strike cap | 2 pairs, +1 multi-match bonus; extras stay face down and log as `capped` | Big shapes can't clear a lucky cluster in one blow |
| Twinblade | 2 cells, rotates; 0 Focus, no cooldown; +1 Guard **only on a hit**; Guard banks at most 1 | See finding below |
| Rune Hammer | diagonal or reverse diagonal; 1 Focus, 1-turn cooldown; staggers the enemy one beat on a match | |
| Hooked Spear | L-triomino, 4 rotations; 1 Focus, 1-turn cooldown | |
| Seer's Staff | 5-cross; 2 Focus, 2-turn cooldown; two pairs in one strike refund 1 Focus | |
| Memory Lantern | 2x2; 1 Focus, 2-turn cooldown; reveals only, never resolves a pair | |
| Needle Rapier | 2 cells, both bullseye; free, 1-turn cooldown | Precision tool for a remembered adjacent pair |
| Edges | An overhanging mask is shown whole and refused (`legal: false`), never clipped | |
| Tempo | Every scout or strike is one beat of the enemy's telegraph; a cleared board with the enemy standing redeals | |

**Simulation (200 seeds per cell; enemy HP = pairs on the board, attack 2, telegraph 4 beats on 4x4/4x6 and 5 on 6x6; win rate / mean actions)**

| Player | 4x4 | 4x6 | 6x6 |
| --- | --- | --- | --- |
| Blind random scouting | 6% / 19.6 | 0% / 20.0 | 0% / 25.0 |
| Spray: widest affordable shape at random, no memory | 37% / 17.6 | 6% / 21.5 | 0% / 26.8 |
| Remembers 60% of revealed cells | 100% / 9.7 | 99% / 14.9 | 86% / 22.8 |
| Remembers every revealed cell | 100% / 7.9 | 100% / 12.0 | 100% / 18.4 |
| Remembers, and aims shapes at known pairs | 100% / 7.5 | 100% / 11.6 | 100% / 17.7 |

Memory decides fights at every size, a wider reveal never substitutes for it (spray loses badly from 4x6 up), and aiming the right shape at a remembered pair is the fastest play. 4x4 is forgiving enough that blind area play sometimes wins; keep it for tutorial and corridor fights.

**Finding:** the tentative "Twinblade grants 1 Guard even without a pair" broke the economy. Memoryless Twinblade spam kept a Guard banked for every telegraphed hit, halving all damage, and won 58% of 4x4 fights by stalling. Guard is now earned by a struck pair and caps at one.

**Accessibility contract for t-007 (the board integration)**

- Every mask preview is also text: weapon, rotation and the covered coordinates ("Hammer, reverse diagonal: B2, C3, D4"), so a screen reader hears exactly what a sighted player sees before committing.
- Bullseye cells carry a glyph and an outline, never colour alone; illegal placements say why (`strikeBlocked` returns the sentence).
- Keyboard and touch both move the anchor by cell, rotate with a dedicated control, and commit with a separate confirm. No action depends on timing or reflexes.
- Reveal hold time is a setting (reduced motion swaps the flip animation for a fade), and the enemy's telegraph is shown as a number as well as an icon.
