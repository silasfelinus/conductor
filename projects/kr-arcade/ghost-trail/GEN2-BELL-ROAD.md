# Zuzu: Ghost Trail, Generation 2: the Bell Road

**Task:** `kr-arcade/t-158` (milestone m9). **Bar:** [../GEN2-STANDARD.md](../GEN2-STANDARD.md).
**Direction (Silas, 2026-10-22 PT):** Super Mario World (and later 2D Mario such as *Wonder*) depth for level
design and play, on top of the Ghosts 'n Goblins feel; persistent saves, long-form exploration, a game
with memory, open world maps. Everything original.
**Status:** design target. Nothing here is shipped until a PR wires it and a player can walk it.
**Machine-readable graph:** `ghost-trail/bellRoad.json` (validated by `validate_bell_road.py`; port the
checks into `ghostTrail/bellRoad.test.ts` in t-160).

**Canon, every frame:** Zuzu is a koala with a stern expression, a broad straw kasa, a rust poncho with
orange zigzag trim, the katana hilt over his RIGHT shoulder. The first hit tears off poncho and hat (the
torn sprite set); the second hit is fatal. That two-hit rule is the Ghosts 'n Goblins spine. Nothing in
Gen-2 softens it: no health bar and no third hit. The reserve poncho (below) is the only buffer, and it
takes a button press.

## Key calls

1. **28 nodes, 7 map regions.** Each of the 18 Gen-1 acts becomes its own level. The node id stays the
   act id (`s1a1` and so on), so v1 saves and relic ids carry over untouched. Nine nodes are new: six
   haunted houses, two fortresses (Silver Gulch and the Bone Yard had none) and the Canyon Shrine. The
   act that ends in a Gen-1 boss becomes that region's `boss` node.
2. **Every region has a fortress, a house, a boss and at least one secret exit, 10 secret exits in all.**
   The main path is 22 levels, roughly 95 minutes for a first clear. A player who never finds a secret can
   still reach the credits, but misses five nodes.
3. **The Canyon Shrine is three things.** It is a hub reached only by secret exits, from three regions. Its
   normal exit is the switch: ringing its stone bell makes *spirit planks* solid in 12 levels, for good.
   Its secret exit opens the Lantern Road, a back door into the abbey. To stop that back door from skipping
   the story, the Abbess's node is **sealed** until all five earlier bosses fall.
4. **Wonder moments come from a "Thin Bell".** Every level hides one small spectral bell. Touching it
   transforms the level for about 30-45 seconds, and the transformation pays out a **bell note**, the
   level's second collectible.
5. **Saves are a three-slot file of per-node bitmasks.** The worst case is 4.6 KB, against 7.7 KB if the
   same data were stored as id lists, inside the arcade store's 8 KB per game. A v1 save becomes slot 1
   with its act, checkpoint, relics, captive, weapon and New Game+ tier kept.

## The map

The Bell Road is told on six Z-Image maps that were reviewed and kept in
`art/GHOST-TRAIL-GEN2-ROUND-1.yaml`. Every map has empty clearings where the code draws the node markers.
Node coordinates use the cabinet's 480 x 270 screen.

| Map (art_image_id) | Role |
| --- | --- |
| The Bell Road (251289) | Region select once a region is cleared; the hidden shrine fork lives here |
| Silver Gulch (251290) | Region 1 |
| Bone Yard (251291) | Region 2 |
| Drowned Watering Hole (251292) | Region 3 |
| Storm Crow Pass (251293) | Region 4 |
| Mission Bell Tower (251294) | Region 5 on the `above` layer; Region 6 on the `below` layer (the stair down into the crypts) |

House interiors use the Widow's Boarding House backdrop (251295) as their style source. The shrine level
uses the Canyon Shrine plate (251296). Each backdrop is a style source only: the collision geometry comes
from level data.

### Regions and nodes

Kinds: **S** start, **L** level, **F** fortress, **H** house, **B** boss, **Sh** shrine. *(new)* marks
content that has no Gen-1 act. `-n->` is a path opened by a normal exit; `-s->` is a path opened by a
secret exit. Paths can be walked both ways once open, as in the plumber model.

```
1 SILVER GULCH       S trailhead -> L s1a1 Main Street -n-> H s1-boarding-house (new)
                     H -n-> F s1-jailhouse (new) -n-> B s1a2 The Courthouse [Grave Marshal]
                     H -s-> B s1a2                          (the dumbwaiter: skips the jail)
                     B -n-> warp right -> s2a1
2 THE BONE YARD      L s2a1 The Crypts -n-> F s2-ossuary (new) -n-> B s2a2 The Broken Bridge [Bone Bull]
                     L s2a1 -s-> H s2-house Gravedigger's Lodging (new) -n-> B s2a2
                     B s2a2 -s-> warp down -> Sh canyon-shrine    (the ravine floor)
                     B -n-> warp right -> s3a1
3 DROWNED WATERING   L s3a1 The Shallows -n-> H s3-house The Stilt Hotel (new) -n-> F s3a2 The Sunken
  HOLE               Chapel -n-> B s3a3 The Ferry Crossing [Drowned Ferryman]
                     H -s-> B s3a3                          (dead-low-tide cellar: skips the chapel)
                     B -n-> warp up -> s4a1
4 STORM CROW PASS    L s4a1 The Switchbacks -n-> F s4a2 The Canopy [mid: Dust Devil] -n-> L s4cliff
                     The Cliff Road -n-> B s4a3 The Aerie [Storm-Crow Matriarch]
                     L s4a1 -s-> H s4-house The Way Station (new) -n-> L s4cliff   (skips the canopy)
                     L s4cliff -s-> warp left -> Sh canyon-shrine (the cave behind the lightning)
                     B -n-> warp right -> s5a1
5 MISSION BELL       L s5a1 Mission Steps -n-> L s5a2 Bell Gallery -n-> F s5stair The Bell Stair -n->
  TOWER              B s5a3 The Belfry [Bell Heretic]
                     L s5a1 -s-> H s5-house The Padre's Rectory (new) -n-> F s5stair (skips the gallery)
                     H -s-> warp up -> Sh canyon-shrine     (the wine-cellar tunnel)
                     B -n-> warp down -> s6a1
6 ABBEY BENEATH      L s6a1 The Undercroft -n-> F s6a2 The Ritual Halls -n-> B s6a3 The Bell Beneath
  THE BELL           [The Abbess; SEALED until s1a2, s2a2, s3a3, s4a3, s5a3 are cleared]
                     L s6a1 -s-> H s6-house The Novices' Dormitory (new) -n-> B s6a3
                     B s6a3 -n-> credits, then free roam
0 CANYON SHRINE      Sh canyon-shrine (new): normal = the shrine bell switch; secret -> warp down -> s6a1
  (hidden)           (the Lantern Road)
```

Count: 1 start, 8 levels, 6 fortresses, 6 houses, 6 bosses and 1 shrine, **28 in all**. There are 36 paths
and 10 secret exits. Totals for 100%: 27 clears, 10 secret exits, 30 relics and 27 bell notes.

### Haunted houses: the exit is the puzzle

Every house is a loop of rooms built from a data-driven door graph. Doors can open onto the wrong room,
and hallways can wrap around on themselves. A house never kills by puzzle alone: its threats are thrown
furniture and shades. Each house's rule is shown on screen at least once before it matters.

| House | Normal exit (the rule) | Secret exit |
| --- | --- | --- |
| **The Widow's Boarding House** (R1, main path; teaches the type) | The widow's portrait follows Zuzu with its eyes, except toward one door. That door is the back door. | Ring four service bells in the order the guest book lists the rooms (shoot the bell pulls through the stair rail). The dumbwaiter then drops to Courthouse Square. |
| **The Gravedigger's Lodging** (R2, behind a secret) | Each coffin Zuzu opens sinks the house one floor, and the earth climbs the windows. The exit appears on the floor whose number matches the tally marks on the gate headstone. | - |
| **The Stilt Hotel** (R3, main path) | The tide runs through the floors. The exit is on the one floor that stays dry at high tide; the dry flowers in its hall give it away. | At dead-low tide the cellar door is clear of water for 8 s. The Room Nine key (this house's relic) opens it. |
| **The Way Station** (R4, behind a secret) | Every slammed door reshuffles the rooms on the wind. The timetable names the last coach's gate letter, and the gate whose letter the roof weathervane points at is the exit. | - |
| **The Padre's Rectory** (R5, behind a secret) | Every door leads into one of two copies of the house, one lit and one dark. The exit is in the copy whose hall clock matches the toll count of the mission bell. | Snuff every candle in the dark copy with the returning kasa. The wine-cellar tunnel to the canyon opens. |
| **The Novices' Dormitory** (R6, behind a secret) | Follow the one sleepwalker who is alive. If the novice was freed in s6a1, she leads; otherwise read the dust, because only living feet leave prints. | - |

### Fortresses and mid-bosses

Every mid-boss gets three or more tells, 0.5-1.0 s of warning, and a recovery window to punish. The
blueprint's boss rules apply unchanged.

| Fortress | Mid-boss | Reward |
| --- | --- | --- |
| Boot Hill Jailhouse *(new)* | **The Turnkey**, a hulking ghost jailer. He swings a ring of keys on a chain overhead, then low, then hides behind a cell door and slams it, which leaves his back open. | Shuriken |
| The Ossuary Vault *(new)* | **The Ossuary Choir**, a wall of skulls in three voices: high fires arcing shots, middle rolls a ring along the floor, low drops ceiling bones. The skull that sings off-key glows; it is the one to hit. | - |
| The Sunken Chapel (s3a2) | **The Font Warden** *(new)*, a drowned sexton whose tolling raises and lowers the water in the nave | Lantern; the River Croc becomes a ride |
| The Canopy (s4a2) | **The Dust Devil** (already in `bosses.ts`; now a mid-boss) | Iai cut |
| The Bell Stair (s5stair) | **The Tolling Twins** *(new)*: two acolytes on one bell rope, one rising as the other falls, so their shots alternate between high and low | - |
| The Ritual Halls (s6a2) | **The Candle Prioress** *(new)*. Her wax candles relight the hall's fires until they are snuffed with the kasa or out-burned with the lantern. | - |

A cleared fortress crumbles on the map once, with an animation, and stays rubble.

## Relics, subweapons, companion

**Relics (30).** The 21 Gen-1 relics stay in their acts under the same ids. Every new node adds one:
`s1-jailhouse-cell-key`, `s1-house-guest-book`, `s2-ossuary-tuning-bone`, `s2-house-sexton-spade`,
`s3-house-room-nine-key`, `s4-house-last-timetable`, `s5-house-padre-spectacles`, `s6-house-lullaby` and
`shrine-pilgrim-candle`. The novice rescue (`s6a1-novice`) is still kept with the relics but does not count
as one. The true ending still requires every relic.

**Subweapons.** These are found once and kept in the satchel. In a level, a gear pickup still *swaps* the
equipped weapon, which keeps the Ghosts 'n Goblins feel. On the map and at lantern-post checkpoints, Zuzu
can switch to any weapon he has found, much like SMB3's map items.

| Weapon | Found | Trade-off and traversal use |
| --- | --- | --- |
| Kunai | start | Safe and fast; at most 3 in flight |
| Shuriken | Boot Hill Jailhouse (main path) | Throws three ways, so it can hit diagonal targets and switches; slower cadence |
| Spare kasa | Gravedigger's Lodging (secret branch) | Returns through everything in its path; Zuzu can hop once in mid-air off the returning hat |
| Lantern | Sunken Chapel (main path) | Lobbed ground fire for 2 damage; lights dark rooms; burns bramble and fuses |
| Iai cut | The Canopy (main path) | A short, brave lunge that crosses a 3-tile gap and cuts bolts out of the air |
| Bell charm | Canyon Shrine (secret) | Rings a note that stuns spirits and shows false walls and spirit planks; no damage, long cooldown |

**Reserve poncho.** This is the SMW reserve box in Ghost Trail's terms. The satchel holds one spare
poncho, found in poncho crates or bought at houses with nuggets. Calling it down restores the poncho and
kasa. It never adds a third hit.

**Companion.** After the croc ride in the Sunken Chapel, the River Croc waits at every deep-water stretch
in R3-R6 as a ride. He keeps Zuzu above the flood, swallows leeches and carries a crate across. He is never
hurt and never hurts anyone, as the blueprint requires.

**Shrine switch.** Ringing the shrine's stone bell (its normal exit) makes the cyan dotted *spirit
planks* solid in `s1a1`, `s1a2`, `s2a1`, `s2a2`, `s3a1`, `s3a2`, `s4a1`, `s4cliff`, `s5a2`, `s5stair`,
`s6a1` and `s6a2`. The planks open high roads and easier relic lines. They are never the only way through
a level.

## Memory: the game recognizes progress

- **Node pips.** Each node shows a lit lantern (cleared), a cyan flame (secret exit found, shown only on
  nodes that have one), bone tokens (relics, 1 or 2) and a small bell (bell note). A node with everything
  wears a gold kasa marker. New Gen-2 nodes sparkle until they are first entered, which matters most for
  migrated players.
- **The world reacts.** Fortresses crumble. Each boss node hangs its bell, cracked. The abbey door on the
  map carries five seals, and each one breaks, with an animation, when its boss falls. The moon on the
  title screen wanes one phase per boss, and the title plate shows the furthest region reached.
- **People remember.** After the boarding house's secret exit, the Widow stands on her porch node, and her
  line changes with the relic count. After the croc ride, the River Croc suns himself at the R3 dock. The
  freed novice waits at the Gulch Trailhead, and in the dormitory she leads instead of the footprints. The
  Turnkey's keys hang on the crumbled jail. In the Bell Beneath, the trail's dead appear as cameos, and the
  set depends on which bosses and mid-bosses this slot has beaten.
- **Your own trail.** On a revisit, small grave candles mark where this slot died in the level; the
  marker can be turned off. On a revisit after a clear, a faint "ghost trail" replays the slot's best
  clear as a pace-setter. This is opt-in, and its input log is stored on the device, never in the 8 KB
  save.
- **File select** shows, for each slot, the region, relics x/30, exits x/37, notes x/27, completion
  percent, play time, deaths, subweapon icons and the poncho state.
- **Completion percent** = (clears + secret exits + relics + bell notes) / 94.

## Save slots (3) and migration

The file is kept under the existing `zuzu-ghost-trail` key in `utils/arcade/saves.ts`:

```ts
type GhostFile = { v: 2; active: 0 | 1 | 2; slots: (GhostSlot | null)[] }
type GhostSlot = {
  node: string                       // where Zuzu stands on the map
  marks: Record<string, number>      // per node: 1 normal clear, 2 secret exit, 4 bell note,
                                     //   8 relic[0], 16 relic[1], 32 rescue (s6a1 captive)
  subweapons: Weapon[]; weapon: Weapon
  poncho: boolean; reserve: 'poncho' | null
  switches: string[]                 // ['shrine-bell']
  score: number; lives: number; deaths: number; time: number
  tier: number; continued: boolean   // New Game+ tier and the v1 continue rule, per slot
  best?: Record<string, number>      // per-level best clear, seconds
  run: { level: string; checkpoint: number; down: string[]; opened: number[] } | null
  updatedAt: number                  // for t-163 sync, last write wins
}
```

- **Untrusted on read.** Ids are validated against the catalog, unknown ids are dropped, numbers are
  clamped, and any bit for a relic slot that does not exist is masked off. `run` is the v1 mid-level
  ledger, kept only for the level in progress, so squads and crates still cannot be collected twice.
- **Score rules.** A level's score is banked on its first clear. A revisit can earn its missing relic,
  bell note or secret exit, plus a best time, and nothing else. Checkpoint suicide never resets the
  encounter ledger. The leaderboard still takes only a slot's first full clear of `s6a3`.
- **v1 to v2 migration.** `readSave()` runs on the old blob first, so only a valid v1 save migrates, and
  it goes into slot 1. `node` = `act`. Every node whose `gen1Act` comes before `act` in `ACTS` order gets
  the "cleared normally" bit, so earlier bosses count toward the seal. New Gen-2 nodes stay uncleared and
  sparkle. Each relic id sets its owning node's bit, and `s6a1-novice` sets the rescue bit. `weapon`
  becomes `subweapons: ['kunai', weapon]`, equipped. `score`, `lives`, `tier` and `continued` are copied.
  `run` = `{ level: act, checkpoint, down, opened }`, so "Continue" resumes mid-act exactly as v1 did.
  `deaths` and `time` start at 0. A post-win v1 save, which is a fresh New Game+ run, keeps its tier.
  Nothing is wiped. An unreadable blob leaves an empty file and is not overwritten until the player saves
  into a slot.
- **Budget.** The worst-case three-slot file is 4,603 bytes as bitmasks, measured by the validator, of the
  8,192 allowed. The same data as id lists would be 7,732 bytes, which is too close to the limit.

## Per-level beat sheets (first clear, Gen-2 target)

Each level has a midpoint lantern post, at least one sub-area, a secret that needs a power or a thrown
object, a relic and a Thin Bell. **Wonder** is what the Thin Bell does to the level.

**Silver Gulch**
- **s1a1 Main Street** (L, 4 min). The tutorial street: a barrel, a crate and narrow pits, then a spirit,
  a crow and a coyote one at a time before they come in pairs. Poncho crates sit just ahead of each harder
  stretch. The midpoint is the town square ambush. Sub-area: the water-tower interior, a ladder room up to
  the tank walk and the Tin Star; a kunai to the rusted weathervane drops its ladder. *Wonder:* the town
  remembers its last good day. Ghost townsfolk square-dance in the street, the boardwalk rises and falls on
  the fiddle's beat, the coyotes dance instead of biting, and the dancers toss Zuzu onto the hotel roof and
  the bell note.
- **s1-boarding-house** (H, 4 min). This house teaches the type. Hallways loop, doors open onto the wrong
  room, and chairs fling themselves (a kunai breaks them). The midpoint is the parlour lantern. The attic
  is the sub-area. The portrait rule is the normal exit; the guest-book bell order is the secret.
  *Wonder:* the house turns over. Ceilings become floors, chandeliers become islands, and the widow pours
  her tea upward.
- **s1-jailhouse** (F, 5 min). Timed cell doors, gallows trapdoors, and gunslinger guards behind cover.
  The midpoint is the gallows yard. Sub-area: the prisoners' crawl tunnel. The Turnkey drops the
  shuriken. The Cell Key hangs high and diagonal above the warden's desk; only the shuriken reaches it, so
  it waits for a revisit or the walk back. *Wonder:* the wanted posters come alive. Zuzu flattens into one
  and slides along the walls and across the bars, unseen by the guards.
- **s1a2 The Courthouse** (B, 6 min). Gunslingers and boot-hill ghouls, then the split between the
  rooftop run and the street of pits and gunfire. The Piano Key is in the saloon crawlspace, reached by
  turning back. Then the jailbreak ambush, the midpoint on the courthouse steps, the cupola sub-area and
  the high-noon standoff before the Grave Marshal. *Wonder:* twelve ghost jurors follow Zuzu and stack
  themselves under every jump, building a tower to the cupola early, then deliver their verdict, the bell
  note.

**The Bone Yard**
- **s2a1 The Crypts** (L, 5 min). Ghouls on the graves, spirits clawing up between the tombs, hyena packs
  in the rows, and bone spurs that thrust on a beat. The midpoint is at the twin graves; the sub-area is
  the ossuary chamber ambush. The rafters over the spikes lead to the Widow's Locket. Secret exit: a
  diagonal shuriken to the cracked keystone above the rafters collapses the roof into the Gravedigger's
  Lodging. *Wonder:* the ossuary's bones assemble into a skeleton serpent, and Zuzu rides it as it burrows
  in and out of the crypt walls.
- **s2-ossuary** (F, 5 min). Rotating bone wheels, coffin crushers and singing skull corridors. The
  midpoint follows the wheel room; the sub-area is the bone-wheel shaft, a vertical climb. Then the
  Ossuary Choir. The Tuning Bone is behind a false wall that only lantern fire (Region 3) or the bell charm
  reveals, so it is a revisit gate. *Wonder:* the skulls sing a scale, and each note lays a bone step in
  the air; jump the right notes to build a stair to the ceiling garden.
- **s2-house The Gravedigger's Lodging** (H, 4 min). Sinking floors and the tally puzzle. The kasa sits on
  the sexton's hat rack, the Sexton Spade in the cellar. *Wonder:* the lodgers come home. The beds fill
  with sleeping ghosts whose snores lift Zuzu like updrafts over the open grave pits.
- **s2a2 The Broken Bridge** (B, 6 min). Half the bridge's planks are gone: long jumps one after another,
  crows over the gaps and hyenas leaping them. The midpoint is the chapel yard, and the chapel loft is the
  sub-area. The swinging beam leads to the forgotten grave and the First Bell Sigil. Secret exit: a kunai
  to the knot of the grave's rope drops it to the ravine floor, and the sigils lead to the shrine. Then
  the Bone Bull. *Wonder:* the missing planks return as a stampede of ghost bulls, and Zuzu crosses the
  ravine on their backs.

**Drowned Watering Hole**
- **s3a1 The Shallows** (L, 4 min). The tide taught gently: rocks to climb, a shallow first flood, and
  the jetty high road to the Ferry Token. The midpoint is the ford. Sub-area: an orchard passage that is
  walkable only at low tide. *Wonder:* the flood becomes moonlit glass. Zuzu walks on the water, the
  drowned drift visible below, fish swim in the sky, and the leech beds turn into trampolines.
- **s3-house The Stilt Hotel** (H, 5 min). The dry-floor rule and the dead-low cellar (see the house
  table); the Room Nine key is upstairs. *Wonder:* the hotel tips 90 degrees in the flood. Its hallways
  become flooded shafts to swim up, and the beds float as rafts.
- **s3a2 The Sunken Chapel** (F, 6 min). A higher, faster flood and rafts. The chapel roof is the dry
  road; the crypt below, walkable only at low tide, holds the Chalice. At the croc pool, Zuzu crosses on
  the high jetties or puts down the bank squad and rides the River Croc. The midpoint is the churchyard.
  The Font Warden fight in the nave ends with the lantern. *Wonder:* the organ plays and the rain falls
  upward. The flood drains into the sky, the pews float as stepping stones, and the drowned rise away in
  peace.
- **s3a3 The Ferry Crossing** (B, 4 min plus the boss). A short run for the landing on fast tides that
  slow Zuzu and shorten his jump. The Boatman's Coin waits by the landing. The Drowned Ferryman fights in
  two water phases. *Wonder:* the river runs backward, and a ghost ferry of past passengers carries Zuzu
  upstream to a hidden upper dock and the bell note.

**Storm Crow Pass**
- **s4a1 The Switchbacks** (L, 5 min). The wind taught gently, then a cliff ride, a lift and a long gulf.
  The midpoint is the second switchback; the high walkway to the Storm Feather is the sub-area. Secret
  exit: an unmarked wind column off the rim, shown by the crow feathers drifting up it or by the bell
  charm. *Wonder:* the wind becomes visible as cyan ribbons, and Zuzu grinds along them like rails across
  the canyon.
- **s4a2 The Canopy** (F, 5 min). Boughs over a broken floor and the cave cache, whose way in faces back
  down the trail (the Miner's Lamp). A canopy shortcut crosses the hyena pit field, then the rope ferry,
  the midpoint, and the Dust Devil, who drops the iai cut. *Wonder:* the trees uproot and walk. Zuzu
  rides a striding tree across the pits while harpies nest in its crown.
- **s4-house The Way Station** (H, 4 min). The timetable and weathervane rule. The Last Timetable relic is
  in the ticket cage, opened by a lantern lobbed over its counter. *Wonder:* a stagecoach pulls up inside
  the station, and the house becomes an auto-scroll chase on the coach roof through the shuffling rooms.
- **s4cliff The Cliff Road** (L, 5 min, vertical). About four screens up the canyon wall: crumbling
  stairs, rope lifts and wind columns, with lightning on the landings. The midpoint is the halfway
  landing. The Thunder Egg is the existing relic. Secret exit: a cave behind a lightning column, entered
  between strikes; it is dark until the lantern lights it, then it leads to the shrine. *Wonder:* the
  camera turns. The cliff tips over, and the climb becomes a sprint along the wall's face above the storm.
- **s4a3 The Aerie** (B, 5 min plus the boss). Wider gulfs, the gondola between two crags, the nesting
  cliffs and the Crown of Quills, then the Storm-Crow Matriarch on the summit. *Wonder:* lightning freezes
  mid-strike into golden poles that Zuzu swings around to fling himself between the crags.

**Mission Bell Tower**
- **s5a1 The Mission Steps** (L, 5 min). Stone steps, braziers that burn on a beat, and the cloister-roof
  lift detour. The midpoint is the high plateau, the site of the first masonry ambush. The Padre Ledger is
  at the far climb. Secret exit: ride the cloister lift past its top and iai-lunge across the gap into the
  rectory window. *Wonder:* the toll turns the sky crimson, and every brazier becomes a hot-air lantern
  that carries Zuzu up the steps.
- **s5a2 The Bell Gallery** (L, 5 min). Bell lifts, swinging bell beams and acolytes tending the
  braziers. The midpoint is the gallery's centre; the sub-area is the clapper loft and its Cracked
  Clapper. *Wonder:* every bell rings at once, and their sound rings become hoops that Zuzu rides outward
  like ripples.
- **s5-house The Padre's Rectory** (H, 5 min). The two-copy clock rule; the candle secret leads to the
  shrine. The Padre's Spectacles show a hidden line on the hall clock. *Wonder:* the paintings become
  windows. Zuzu steps into one for a 20-second slice of an earlier region in that painting's palette and
  comes back with the bell note.
- **s5stair The Bell Stair** (F, 5 min, vertical). About 3.5 screens: stone stairs, bell lifts and a wind
  shaft. Every landing is a checkpoint, with the midpoint halfway. The Bell Rope relic sits up a side
  climb. The Tolling Twins wait at the top. *Wonder:* the tower turns inside out, and Zuzu climbs its
  outer face in the storm with the moon huge behind him.
- **s5a3 The Belfry** (B, 5 min plus the boss). Falling masonry, rotating hazards and the hardest optional
  climb, to the Bell Order (which is also the answer to the shrine's secret). Then the Bell Heretic.
  *Wonder:* the great bell tips over, and Zuzu runs inside it as it swings: a rotating room.

**Abbey Beneath the Bell**
- **s6a1 The Undercroft** (L, 6 min). Ritual tunnels: wait out the fire under the roof, or take the
  riskier roof road. Sisters, shades and two held rooms. The Novice Letter and the First Vow are on the
  roofs. The midpoint is the novices' hall. The novice cage is the sub-area. Secret exit: free the novice
  and follow her up the floating stair to the dormitory. *Wonder:* the candles go out, and only Zuzu's
  footsteps make light, each step a cyan ripple that sketches the room for a moment.
- **s6-house The Novices' Dormitory** (H, 4 min). The living-sleepwalker rule; the Lullaby relic is in
  the toy chest, which needs the kasa hop. *Wonder:* Zuzu shrinks to toy size. The beds are mesas, a toy
  train rattles between them, and the toy soldiers march.
- **s6a2 The Ritual Halls** (F, 6 min). Four held halls, each remixing everything taught so far, with
  ritual wind shafts between them and the burning long tunnel. The midpoint is the third hall. The
  Confession and the Foundry Mark relics are here. The Candle Prioress closes the act. *Wonder:* the
  ritual runs backward. Fire falls as water, and the foes walk backward into the doors they came from.
- **s6a3 The Bell Beneath** (B, 7 min plus the boss). The trail's dead return as cameos, filtered by this
  slot's history. The Abbess Ledger and the Last Litany are on the way. Then the Abbess in two phases and
  the escape. *Wonder:* the ghosts of every boss this slot has beaten walk behind Zuzu in procession, and
  each one shields one hit before it lies down. If the novice was freed, she carries a lantern ahead.

**The Canyon Shrine**
- **canyon-shrine** (Sh, 5 min). Three candle trials, one for each of tide, wind and bells, under the
  starry plate. Each trial is a short room that tests a learned mechanic. The midpoint is after the
  second trial. The Pilgrim Candle sits on the shrine roof, and the bell charm is on the altar. Normal
  exit: ring the stone bell (the spirit-plank switch). Secret exit: ring its six small bells in the Bell
  Order, which is read from the s5a3 relic or worked out from the six boss motifs, to open the Lantern
  Road. *Wonder:* the stars come down, and the six bosses' constellations become platforms to trace.

**Runtime.** The main path is 22 levels at about 95 minutes for a first clear, within the Act I target of
75-100. 100% takes about 2.5-3 hours. Only measured playtests count, as in the blueprint.

## Implementation order (t-160, t-161, t-162)

**t-160: the overworld and save slots.** Generalize the plumber module; do not copy it.
1. **`utils/arcade/overworld.ts`.** Move the pure rules out of `savePlumberOverworld.ts`: `pathOpen`,
   `openPaths`, `newlyOpened`, `nodeReachable`, `stepFrom` and completion. Generalize them to `unlock:
   { node, exit }`, string node kinds, an optional `seal` and pluggable per-node collectibles. Plumber
   node ids already equal its stage codes, so the plumber file becomes a thin adapter (`stage` to `node`)
   and its tests pass unchanged. Add `utils/arcade/saveSlots.ts`, a generic three-slot file reader
   (`readSlotFile(raw, readSlot, fromV1)`), and move plumber onto it in the same PR.
2. **`ghostTrail/bellRoad.ts`** with the graph from `bellRoad.json`, plus `bellRoad.test.ts`, which ports
   every validator check and cross-checks against `ACTS` and the relic ids. A node with no authored act
   is `planned`: it is drawn as a boarded-up signpost and treated as pass-through for paths. That keeps
   the map walkable before t-161 lands.
3. **Ghost save v2**: `GhostFile` with bitmask marks, migration from v1 (with one fixture per act) and the
   size test. Then the file-select screen: copy, erase, and export/import as a string.
4. **The Bell Road map screen in the cabinet.** Z-Image region plates are used once their URLs are
   verified, with a procedural fallback. Node markers and pips are code-drawn. The walker sprite, path
   reveals driven by `newlyOpened`, warp transitions and the region select come next. Entering a node
   runs the existing act; returning sets the exit, relics and note bits. Add `exits.secret` zones to the
   `Act` type, and wire the two secret exits whose geometry already exists: `s2a2` (the ravine floor) and
   `s4cliff` (the cave). At the end of t-160, all 18 acts are playable from a saving map.

**t-161: the stages, one region per PR.** A first shared-systems PR adds the house engine (a door graph,
loop rooms and puzzle state as data), the Thin Bell framework (a timed transform: palette, physics flags,
terrain overrides and the reward), spirit planks with the switch, midpoint lantern posts and the bell
note. Then the regions in order: R1 (it teaches the house, fortress and wonder), then R2 together with
the Canyon Shrine (the first shrine entry and the switch), then R3, R4, R5 and R6. Each region PR covers
its new nodes, its secret-exit zones, the sub-area, relic and Thin Bell for every level, and seeded
bot-walks of every main and secret route.

**t-162: animation, in parallel.** This is the art lane and does not depend on the code. Make key poses,
then WAN first/last-frame clips, then the atlas. First the in-level Zuzu (the poncho set and the torn
set, with the blueprint's action list), then a four-direction map walker at map scale, then the mid-bosses
and house props. Left-facing frames are drawn, never mirrored, so the hilt stays over the right shoulder.

**t-163 (save sync)** follows later. `updatedAt` on each slot already supports last-write-wins.

## Validation

`python3 validate_bell_road.py bellRoad.json /home/user/kind_robots` prints **PASS**.

- 28 nodes, 36 paths and 10 secret exits; every node is reachable with the seal honoured.
- A player who uses only normal exits reaches 22 of the 27 playable nodes and the ending.
- Every secret exit opens something; every non-final normal exit opens something.
- Each boss leads on to the next region's entry, and `s6a3` ends the game.
- Every region has a level, a fortress, a house, one boss and a secret exit. The shrine is entered only
  through secret paths.
- All 18 Gen-1 acts, 21 relics and the captive in `kind_robots` map exactly once.
- The worst-case save is 4,603 bytes of 8,192.

Negative runs fail as they should: a missing boss path, a dangling id, a shrine secret that opens
nothing, and an unsatisfiable seal.
