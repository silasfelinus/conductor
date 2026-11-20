# Memory Dungeon playtest-readiness assessment, 2026-11-20 PT

**Bar (Silas, 2026-11-20 PT):** *"You should have all 12 worlds 12 dungeons, full opening, endings, art for all choices, scripted interactions."* A same-day handoff that cut scope at e10 and marked the game `playtest` (conductor#7650) was wrong and has been reverted. This file records what kind_robots main (`31524805`) actually ships against that bar. Production art was checked with ranged GETs, because the media host answers HEAD requests with 404 even for files that exist.

## Overworlds (64 sites each)

| World | Hand-written sites | Boilerplate sites | Playable stage |
|---|---|---|---|
| e01 Briar Marches | 64 | 0 | yes |
| e02 Dark Briar | 64 | 0 | yes |
| e03 Morrow's Shift | 64 | 0 | yes |
| e04 Unbelieving City | 64 | 0 | yes |
| e05 Scylla's Shore | 64 | 0 | yes |
| e06 Undertide Crown | 64 | 0 | yes |
| e07 Lantern Village | 64 | 0 | yes |
| e08 The Shut Doors | 64 | 0 | yes |
| e09 Pip's broken forest | 22 | **42** | yes |
| e10 Morrow's broken city | 10 | **54** | yes |
| e11 Char | 0 | **64** | **no** |
| e12 Vesper | 0 | **64** | **no** |

"Boilerplate" sites are generated from `overworldEventRecipes.json`: the title is "District / Device", the opening ends "X must decide Y", and the two choice outcomes are fixed text ("The care and its cost belong to this coordinate").

## Dungeons

These eight exist and are playable: House That Remembers (e01, 36 rooms), Dark House (e02, 36), Sublevel B (e03), Drowned Archive (e04), Breathing Works (e05), Choking Works (e06), the Red Oven (e07) and the Furnace of Names (e08). **e09, e10, e11 and e12 have none.** → t-077

## Opening

One prologue screen: a background image, four paragraphs and one choice. There is no illustrated intro or cutscene. → t-079 (with t-020)

## Endings

The 12 House epilogues are live, with plates served. The ~32 core endings exist only as titles and summaries in `reimaginerCampaign.ts`. They need e12, and no component renders them. → t-078 (with t-028)

## Art actually displayed

| Surface | Present / required |
|---|---|
| e01 sites and choices | 64/64 and 128/128 |
| e02 sites and choices | 60/60 and 120/120 |
| House rooms and choices | 36/36 and 77/77 |
| Dark House choices | 72/72 |
| e03-e12 site scenes at catalog paths | **0/640**, and the stages show "Illustration pending" because `art()` hard-codes `status: 'placeholder'` |
| e03-e06 choices at current paths | **4/127, 7/127, 7/131, 9/139**: earlier plates were painted for the old boilerplate labels, and the paths moved when the sites were rewritten |
| e07/e08 choices at catalog paths | 0/128 each |
| e09 / e10 choices | 122/130 and 130/130 |
| e11 / e12 | 0 |
| Hoshimori stages and the five later dungeons | **no images rendered at all** |

→ t-074 (display wiring), t-075 (scene plates), t-076 (Hoshimori and dungeon art), t-045, t-035, t-033

## What already passes

- All seven `test:memory-*` suites pass (World One: 20 seeded runs, 0 softlocks; Dark Briar: 36 runs, 0 softlocks).
- The start flow works on production at 390, 820 and 1440 wide.
- Classic Match is unchanged.

## Build order

1. t-074: wire delivered art so it displays (unblocks every art task).
2. Rewrite the 96 boilerplate sites in e09 and e10 (t-047 and t-057).
3. Author and build e11 and e12, 64 sites each, with stages and transitions (t-047, t-028).
4. Build the e09-e12 dungeons (t-077).
5. Build the endings sequence and gallery (t-078).
6. Build the full opening (t-079).
7. Art: t-075, t-076 and the gallery tasks.
8. Adversarial, device and accessibility acceptance (t-031, t-046, t-036).
9. Only then the playtest handoff, the master-issue flag and the lifecycle change.
