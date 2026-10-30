# Memory Dungeon: The Hoshimori Pair (e07 / e08) — production plan

**2026-10-30 superseding order and source-status note:** Hoshimori is the **fourth mandatory original→twisted pair**, not an optional branch. The existing e07 village now contains 64 connected authored sites and nine of 36 Red Oven rooms in Kind Robots source; the earlier 2026-10-29 inventory below is retained as historical evidence, not today's completion tally. e08 horror remains unimplemented and the preceding Morrow/Scylla worlds e03–e06 are not yet fully playable. Preserve the two fixed photo sites per reality. The sisters' fatal landward-departure history and player-reveal safeguards are defined in `EIGHT-PAIRED-WORLDS-CANON.md`; no early Hoshimori exposition may spoil it.

**Decision:** Silas-directed creative redesign, 2026-10-29 PT. **Status:** approved direction for reversible internal authoring, **not shipped maps**. **Ownership:** Conductor coordinates scope; Kind Robots owns executable `/play/memory` scenes, saves, runtime art and UI. Preserve all established first-six experiences, especially the two Briar worlds, Morrow's real-world chapters, and Scylla/Char's shore and underwater chapters.

## What exists today, and why these two

Evidence inspected against current `kind_robots` main on 2026-10-29 PT:

- `utils/memoryDungeon/reimaginerCampaign.ts` defines **eight concepts / sixteen experiences**; `e01/e02` are the first two Briar realities and `e03–e06` are Morrow and Scylla chapters. Its `planned: true` experience records are **narrative/route contracts**, not 8×8 authored live maps or evidence of delivered artwork.
- `e07` (`hearth`, Earth protagonist, storybook/original) and `e08` (`hearth`, Scylla, hybrid/wished-for) are the first optional middle pair. They preserve the same spatial concept while changing meaning, traversal, cast and visual language. Both currently have metadata and campaign route logic; a complete 64-site / 36-room playable pair was **not found** in the existing production manifests. Do not confuse the implemented Briar/Dark Briar and House/Dark House stages with future e07/e08 delivery.
- `utils/memoryDungeon/chronicle.ts` already assigns Earth photos to **e07 2,3 and 7,5**, and **e08 1,4 and 6,7**. These are fixed discoveries, with existing titles and spoiler-safe Morrow chronology. Keep their IDs, text intent and order unchanged.
- Existing Briar 64-site and 36-room House content, the first two-world art ledger and two House atlas ArtJobs belong to other tasks. Do not rebrand, overwrite, duplicate, or count those assets as Hoshimori delivery.
- `projects/memory-dungeon/SIXTEEN-REALM-PRODUCTION.md` is the earlier 16 individually named realm proposal. The later, executable **eight paired concepts / sixteen experienced realities** in `reimaginerCampaign.ts` and master issue `kind_robots#4136` govern ordering. This document updates the *hearth pair's* creative direction only, not the other fourteen experiences.

**Choice:** repurpose the existing `hearth` pair, not two random world indices and not a new ninth concept. Leave the stable machine IDs `hearth`, `e07`, `e08`; introduce evocative public-facing world titles at the implementation stage. Players must not be shown an explicit sixteen-world production counter.

## The paired story: the village that remembered everybody

### e07 — Hoshimori, the Lantern Village (light folklore)

*Production alias: Hearth and Hunger; on-screen working title: Hoshimori, the Lantern Village.*

A luminous mountain village gathers for the once-a-year lantern supper, inviting travelers and local **yōkai** to exchange food, songs and stories. Rain grows on persimmon branches; slippers return themselves from the river; the helpful household spirit knows every guest's name, except one. This is an **original hand-painted storybook-fantasy visual grammar**, with moss, cedar, golden rice terraces, little bridges, moving paper lanterns, calm humor and slight unease. Studio Ghibli is a tonal reference, **not** a copying brief for specific films, character designs or trademarked scenes.

**Character spine: Pip, the Goblin Bookkeeper.** Pip spent an uncertain stretch of his youth apprenticed to the village's ledger keeper. He can count every ration the village owes outsiders, but cannot remember who personally fed him when he first arrived. This is newly proposed backstory, not a prior-canon fact: establish it through an early scene and test against existing Pip debt/witness choices before treating it as settled. Do not give him an unearned Japanese ethnicity, or claim the place is a historical portrait of Japan. Local villagers and spirits have their own motivations independent of Pip.

**Fairy-tale question retained:** What may a community sacrifice to stay fed? The charitable baker's food can satisfy hunger by taking a memory, but no one initially understands which memories are being used. Village elders, a mischievous bakehouse tsukumogami and a hungry displaced family disagree over whether continuing the custom is ethical. Give each defensible reasons. A player can investigate, negotiate a new food pact, reject the exchange, or attempt a costly emergency solution, with distinct trust, ration and route outcomes.

**Yōkai cast, not a monster vending machine:** a kitsune who demands accurate names, a tanuki trader with an exaggerated claim to respectability, a zashiki-warashi who wants a household safe enough to stay in, and living tools/umbrellas that resent being treated as disposable. Spirits may be funny, angry, helpful or dangerous based on what happened, not a universal good/evil race label. Reference real folklore respectfully and document inspirations; write original characters rather than retell a single legend unchanged.

**Mechanical verb:** *Offer / remember.* The village's lanterns pair with offerings or recalled testimony. Memory matches reveal festival routes, but meaningful scene choices decide which households get access to food or shelter. A short sequence/lantern-order puzzle and a no-guess shrine route offer noncombat variety. A player can finish without fighting every spirit.

### e08 — Hoshimori: The Procession of Shut Doors (yōkai horror)

*Production alias: Hearth of Perfect Safety; on-screen working title: Hoshimori: The Procession of Shut Doors.*

Scylla returns to **the same 8×8 geographical village** after a wish has guaranteed that nobody will ever again go hungry, get lost or leave unprotected. At dusk, the last lantern goes dark. Protective promises have become rigid rules: doors will not open, household spirits refuse to let children go outdoors, the oven eats names rather than bread, and travelers hear the night procession of spirits crossing the roofline.

**Mechanical verb:** *Unbind / testify.* A route visible in e07 becomes a forbidding wall, but must have a fair, clue-bearing alternative. A `nurikabe` can be bargained past by remembering a promise; a processional mask can be confronted via a three-symbol memory sequence; a dangerous `oni` offers an apparent shortcut with a disclosed price. A skeletal giant or overwhelming supernatural shape is an environmental set piece, not an inevitable combat gate. Monsters are distinctive and sometimes frightening, not interchangeable random scares. Make the visual grammar decisively different: vermilion and soot, distorted roofs, moonlit fog, immense moving silhouettes, smoke-black lacquer, uncanny stillness and genuinely frightening negative space.

**Why Scylla sees this world:** her existing `e08` POV remains canonical. Her instinct to rescue everyone clashes with Pip's learned obligation to his village and Char's resistance to paternalistic safety. **Do not rewrite e08 to Pip POV**: he is the emotional anchor and quest companion while Scylla is the lens. Oren's logistics solve a tangible blocked-crossing problem without inventing a hidden childhood or unmasking plot. Give Pip agency, guilt and a possible break with the party, never a passive tragic mascot.

**Twist:** the supernatural night parade is not simply an invasion. Some yōkai are resisting the village's coercive “perfect safety”; some enforce it. The central wrong is a bargain made without informed consent. Endings should include opening the gates at personal risk, rewriting the pact with consent and limits, or preserving some protections while freeing the confined people. Each changes a saved route/relationship and one future-world callback. An apparently clean universal exorcism is deliberately not the optimal solution.

### Anchor map: same geography, different meanings

Propose these **working spatial anchors** for the 8×8 pair. Final coordinates for all *new* sites are assigned in the manifest pass; preserve the four Earth photograph coordinates exactly and reserve any shared cross-realm seals. Do **not** silently reuse an e07 site key as a new place in e08: a mirror at the same coordinate must be intelligible.

| Anchor | e07 read | e08 reimagining |
|---|---|---|
| Cedar footbridge | Lanterns guide neighbors to supper | Nuri-kabe seals the bridge until a broken promise is named |
| Festival square | Tanuki barters disguises and food | Masks perform a compulsory procession; performers cannot stop |
| Ember bakery / Red Oven | Gifts and missing memories behind generous food | Furnace keeps everyone safe by consuming names |
| Mountainside shrine | Zashiki-warashi seeks an inviting home | Door-guardian locks its wards against occupants |
| Rice terraces | Kodama-like tree spirits trade songs for paths | Crops grow under unmoving shadows; a route is trapped |
| Pip's ledger house | His apprenticeship and withheld kindness | A ledger of “rescued” residents conceals their captivity |

## Production and compatibility contract

1. **Do not overwrite e01/e02** (Briar and Briar Understory), **e03/e04** (Morrow's Earth and enchanted Earth), or **e05/e06** (Scylla's shore and underwater memory). Do not alter those route IDs, canon anchors, map art or saved locations.
2. Keep `e07/e08` as the first middle pair, their `hearth` concept, the route prerequisites, `e07` Earth-protagonist viewpoint and `e08` Scylla viewpoint. Maintain original `Hearth and Hunger` / `Hearth of Perfect Safety` as compatibility aliases wherever IDs/titles are serialized. Do not rename save keys without migration tests.
3. Deliver **64 distinct reachable 8×8 sites per incarnation (128 total)**, with individually authored actions and at least two meaningful outcomes for each actionable site; preserve shared geography but transform at least 3 gameplay/story dimensions. Reserve **e07 Earth photos 2,3 / 7,5** and **e08 Earth photos 1,4 / 6,7**. Show the correct photo without promoting the real-world environment to a Japanese fantasy setting.
4. Deliver **36 connected dungeon rooms per incarnation (72 total)** at the same oven anchor, with distinct puzzle, combat, bargaining, recovery and guardian functions. The original “Red Oven” remains an ID-compatible anchor. Give both dungeons escape/retreat options, valid choice continuations and at least three materially distinct guardian outcomes.
5. Honor **30 local + 2 cross-realm illustrated card faces** for each, totaling **64 collectibles**. Every card corresponds to an authored character, place, choice, enemy or reward and has a stable unique art identity. Add two per-world chronology-safe Earth photos already specified above, not freshly invented replacements.
6. Art pipeline: write production manifests first; commission a small style test of **2 world maps, 2 dungeon atlases, 4 portraits, 4 monsters/spirits, 4 encounter compositions and 4 card samples** before bulk submission. Use durable `ArtJob → ArtImage → attached URL → verified media` evidence. Separate **requested, queued, rendered, delivered, visually accepted**; no made-up ArtJob IDs or placeholder-as-done claim. Keep SVG/illustration fallbacks reachable and label them honestly. Commission full 30+2 collectible sets after the visual grammar and authored events are checked. Prefer a consistent model family only after comparing actual renders.
7. World-relevance tests: all coordinates unique, graph connected, e07/e08 same named landmarks, mirrored routes reversible and never blind-guess-gated, offer/promise mechanics affect decisions, each side character has distinct agency, no duplicate loot or softlocks, save/resume/Chronicle and cross-realm consequences stable, seeded trials and Classic mode unaffected.
8. Visual acceptance: art-first one-screen game stage and visible large scenes/maps, keyboard/touch access, readable dialogue at phone width, reduced motion, 390/768/1440 plus landscape tablet rendering, real media URLs, and side-by-side evaluation of the warm vs horror treatment. Neither “Japanese” nor “Ghibli” as prompt decoration alone meets the bar. Public deployment remains separately gated.

## Staged delivery, not a 200-room surprise PR

| Gate | Work package | Demonstrable acceptance |
|---|---|---|
| **0: Canon and data** | Lock e07/e08 design; existing-ID/photo/route inventory, new setting glossary, initial 8×8 coordinate plan | `reimaginerCampaign` contract passes, no new play-count or photo spoiler |
| **1: Warm proof** | First 16 linked e07 sites + one Pip youth scene, 1–2 functioning lantern/offer puzzles, first oven rooms and concept assets | One fresh seeded expedition can reach, choose, leave and restore; Classic unaffected |
| **2: Warm completion** | Remaining e07 map to 64, e07 oven to 36, 3 outcomes, 30+2 gallery briefs, two fixed Earth photos | Full realm graph and save/consequence tests; clear route to next middle pair |
| **3: Horror proof and finish** | 16 dark mirror scenes first, then 64 e08 sites + 36 rooms, Scylla/Pip/Char/Oren agency, distinct mechanics/guardian outcomes | Same geography demonstrably changed, full playable e08 story and cross-pair callbacks |
| **4: Art production** | Style tests, per-map/room art, then full 64 collectible faces and encounter illustration coverage | Traceable per-asset IDs and fetched delivered URLs; no pending counted as finished |
| **5: Adversarial acceptance** | 6+ seed and persona combinations, phone/tablet/desktop, save, refusal, failure, color/reduced-motion and earned ending variants | No shortcuts, infinite resource loops, narrative duplicates, missing maps or unreadable choices |

Art manifests and limited style renders may proceed alongside content writing. Hold expensive bulk variants until scripts and layout prove useful, and do not block authored exploration just because a renderer is backlogged.

## Writers' sample: one site, two realities

**At the Footbridge (e07):** The river carries a procession of empty sandals; a tanuki insists the shoes are coming to dinner and should be counted as guests. Pip says the village once fed him by counting a hungry visitor twice. The player can offer their own ration to settle the seating, investigate who is missing, or walk past. The chosen record changes who speaks for the village at the Oven.

**At the same Footbridge (e08):** The river has gone silent. A living wall prevents any crossing “for the traveler's protection”; inside it, names of people who asked to leave are still audible. Scylla can expose Pip's old ledger, trade her own safety guarantee for passage, or trace a fair symbol pattern to release the trapped travelers. The path is won by remembering who consented, not by killing everything behind the wall.

## Reporting rule

Until two complete realms and their real image deliveries pass the tests above, report **two planned middle-pair incarnations with narrative briefs and route/photo metadata**, not “two more completed overworlds.” Keep the Memory Dungeon master issue open and preserve unfinished art and viewport gaps separately.
