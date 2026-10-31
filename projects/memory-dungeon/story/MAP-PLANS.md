# World Maps · Geographic and production drilldown

[Writer's Room](../WRITERS-ROOM.md) · [Act pitches](ACT-PITCHES.md) · [Scene handoff](SCENE-ROOM.md)

**How to read:** all existing overworlds use **8×8 fixed locations (64 sites)**, not 64 successive memory-match boards. A completed square is a persistent place with choices and consequences. Nested dungeons generally use a separate **6×6, 36-room** atlas. The playable state is checked against Kind Robots code; this is not a rendered-gallery claim.

## World atlas, one line per reality

| ID | Who leads / geography | Recognizable anchors | What changes | Source status |
|---|---|---|---|---|
| e01 | Researcher · Briar | Camp, wolf road, House, rookery | Trust/witness puzzles and cross-realm sigils | 64 authored; gameplay present |
| e02 | Researcher · Dark Briar | SAME 8×8 camp/roads and mirror House | Old witnesses invert predator/protector claims | 64 authored; gameplay present |
| e03 | Morrow · Earth | Research desk, office, commute, hospital, neighborhood | Technology and human custom as unfamiliar mechanics | Outline; full 64-site stage missing |
| e04 | Morrow · Enchanted Earth | SAME Earth streets, office and station | Supernatural hazards, sea-side tide gate and three costs | Outline/branch state; map missing |
| e05 | Scylla · Childhood sea palace | Sisters' room, departure chart, tide court, shore route | Player remembers e04; younger Char does not | Outline/branch state; map missing |
| e06 | Scylla · Twisted palace | SAME palace and planned escape | Rewritten testimony, coercive repetition and altered routes | Outline/branch state; map missing |
| e07 | Vesper · Warm Hoshimori | Cedar bridge, orchard atlas, Red Oven, paper theatre, South Watch | Betrayal/redemption and communal refuge choices | 64 authored; 21/36 Oven rooms |
| e08 | Scylla POV / Vesper arc · Dark Hoshimori | SAME bridge, oven, map and shrine | Recursive domestic architecture, night procession, living addresses | 16 site briefs; playable map missing |
| **e09** | **Pip · Briar collision** | SAME Briar geography, office and sea-root overlaps | Forest monsters in office, submerged House paths | Crossover pitch only |
| **e10** | **Morrow · Earth collision** | SAME Earth geography, Hoshimori shelter and Briar canopy | Yōkai at work, impossible commuter timetables | Crossover pitch only |
| **e11** | **Playable Char · Sea collision** | SAME sea palace, subway station and Vesper route | Alternative Char memories, flooded transit, stolen maps | Crossover pitch only |
| **e12** | **Vesper · Hoshimori collision** | SAME Hoshimori geography, wolf-road and tide-gate overlays | The final question of what belongs on an atlas | Crossover pitch only |

**Earth photo invariants:** keep existing e01, e02 photos and their chronology; e07 fixed photos at **2,3 and 7,5**; e08 fixed photos at **1,4 and 6,7**. Existing 32-photo serialized journal must be migrated, not silently deleted to make a 24-photo campaign. For new finale collectible sites, choose exact coordinates only after inspecting the live Chronicle reservations and mapping tests.

## First-four-world map detail

**Briar e01/e02:** [64-site original geography and 36-room House](../BRIAR-MARCHES-FIRST-WORLD.md), plus [Briar first-two consequences](https://github.com/silasfelinus/kind_robots/blob/main/utils/memoryDungeon/firstTwoConsequences.ts). Preserve 1..8 canonical coordinates and four initially unmatched regional seals. A wolf and a refugee household are not generic enemy/treasure tokens; late encounters should remember which one the player helped.

**Morrow e03/e04:** build one **Earth** 8×8 floorplan whose two realities use the *same* connections: office/research district, transit, residential lanes, public services and tide-gate emergency access. A flooded research floor should still be navigably the research floor. Proposed site clusters, **not immutable coordinates**: work 16, transit 16, home 16, institutional/crossing 16. Reserve the tide gate as e04's major world-pair choice arena with visibly forecast three-route costs.

**Scylla e05/e06:** build one **underwater palace** 8×8 floorplan whose two realities retain the sisters' bedroom, tide court, departure charts, service tunnels and landward escape route. Proposed site clusters: childhood/court 16, craft and servants 16, waterways/approaches 16, exit and shore 16. e05 begins in *subjective real time travel* into younger Scylla, not a static memory. In e06 looped corridors and changing tide currents must still admit a fair route and replayable choice consequences.

**Hoshimori e07/e08:** warm source [64 exact authored e07 locations](https://github.com/silasfelinus/kind_robots/blob/main/utils/memoryDungeon/hoshimoriWarm.ts), and [Vesper childhood plus sixteen mirrored briefs](../VESPER-HOSHIMORI-CHILDHOOD-AND-HORROR.md). Both use the same 8×8 village geography. Protected warm sites: **1,1** childhood footbridge; **4,1** orchard atlas; **2,2** Pip ledger; **4,3** Red Oven entry; **4,4** road Vesper sold; **3,8** paper theatre; **8,8** South Watch. e08 transforms those precise landmarks into hostile manifestations of compulsory identification. e07 needs **15 more** Red Oven rooms to reach 36; no art or dark atlas is presumed delivered.

## Finale map plans: four crossover returns

### e09 · Briar, the forest between floors

Original 8×8 forest paths remain the primary geography. **Pip is the controllable finale lead.** Layer an office corridor across the House, sea-roots under the wolf road, and a distant paper-lantern ward above a refugee path. Write scenes where one rule breaks another: a timecard cannot convince a Briar wolf to let an evacuee leave; tide-current mapping can bypass House roots but threatens a hidden family.

**Required recovery:** `briar-office-key` (city rules) and `briar-tide-roots` (sea rules). Neither can be found by merely walking onto the marker; each needs a story/puzzle resolution. Save both in the shared fragment ledger and hand them to Morrow's next map.

### e10 · Earth, the office that ate a forest

Return to the original real-world office and transit locations. A yōkai house spirit enforces a workplace rest law nobody wrote, the old Briar canopy alters train times, and a mermaid palace flood makes an elevator travel sideways. Morrow's family remains real; do not prematurely reveal or erase children through comedy about corporate HR.

**Required recovery:** `city-lantern-charter` (Hoshimori rules) and `city-forest-hours` (Briar rules). A single flood rescue must be possible without a perfectly remembered prior branch, though earned allies improve outcomes.

### e11 · The sea above the station

Return to Scylla and Char's 8×8 sea kingdom, with subway arrival signs, Vesper's maps and Briar refuge laws intersecting its coral chambers. **Char is controlled**. Every e04/e05 history must define which time-context Char inhabits, whether she knows about the fatal original crossing, and why she has agency; a dead original Char cannot be silently resurrected. Scylla is a companion with memories of consequences the player may never have seen firsthand.

**Required recovery:** `sea-unwritten-map` (Hoshimori private refuge map) and `sea-sister-bell` (Earth transit testimony). Avoid a puzzle whose solution requires knowing unearned facts from a different branch.

### e12 · Hoshimori, the last unwritten road

Return to Vesper's childhood bridge, South Watch and Red Oven, with the same 8×8 village map now invaded by wolf paths, office transfers and flooded palace gates. Vesper must acknowledge both rescue and betrayal even if they helped earlier witnesses; no clean public atlas may expose protected refugees.

**Required recovery:** `village-wolf-door` (Briar rules) and `village-tidal-oven` (sea-gate rules). These eight fragments jointly make the final crossing *physically* navigable. The two final choices must give real rights of consent and departure, not a simplistic everything-is-fixed ending.

## Mapping acceptance contract

- Same site in original and distorted revisit: **same stable position and spatial relationships**, with a changed scene and at least three of meaning, mechanics, traversal, cast, and art style.
- Every 8×8 graph connected, all 64 sites discoverable, no mandatory blind guess, no resources farmable by reentry.
- All nested dungeons need individually justified room routes, not a colored number grid offered as a painted map.
- Original and crossover character, monster, art and matching mechanics are combined into new encounter rules, not merely cameo dialogue.
- Record per-site `worldId / siteId / branch prerequisites / choices / effects / fragment / art subject / regression seed` before a location is marked authored. [Use scene handoff](SCENE-ROOM.md).
