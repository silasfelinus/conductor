# Save the Plumber: Gen-2 worlds

This is the authoritative Gen-2 world design (conductor `save-the-plumber` t-002). It applies
[projects/kr-arcade/GEN2-STANDARD.md](../kr-arcade/GEN2-STANDARD.md) and Silas's 2026-10-22 direction:
*Super Mario World* (or the later 2D Wonder-style games) is the benchmark for structure and quality. **None
of their content is used.** Every name, creature, item, layout and tune here is original, and the
match is to design quality and structure only.

- **Machine-readable graph:** `gen2Worlds.json`, an array of nine worlds (eight campaign worlds plus Upstream Sky).
  Each world has `nodes [{id, kind, name, stage, secretExit?}]` and `paths [{from, to, unlock: {node, exit} | null, warp?}]`.
- **Validator:** `validate_gen2_worlds.py`. It checks that every node is reachable from `w1-start`, that every
  secret exit opens something, that each castle warps to the next world's start, that the main route never needs a
  secret, that no id dangles, and that each Gen-1 stage is used exactly once. Current result: PASS (81 nodes, 87 paths).
- **Kept from Gen-1:** world names, bosses, palettes, enemy families, the 14 enemy toys and the three powers
  ([WORLD-ATLAS.md](WORLD-ATLAS.md), `savePlumberWorlds.ts`). The 32 Gen-1 stages are raw material (see §3.4).

---

## 0. Conventions

| Term | Meaning |
| --- | --- |
| **Node ids** | `w{n}-start`, `{n}-{k}` for levels, `{n}-f` fortress, `{n}-h` Hush House, `{n}-b` bonus cottage, `{n}-s` shop, `{n}-c` Valve Chapel, `{n}-castle`, `sky-{k}` for Upstream Sky. Ids are unique across the campaign. A node id is a **Gen-2 course id, not a Gen-1 code** (node `2-3` is built from Gen-1 `2-2`). |
| **Node kinds** | `start`, `level`, `fortress`, `house`, `bonus`, `shop`, `chapel`, `castle`, `special`. The courses are `level`, `fortress`, `house`, `castle` and `special`. A `chapel` is a short course that presses a switch. `bonus` and `shop` are menus or mini-games with no exit and are always leaves of the graph. |
| **Normal exit** | The Goal Valve that already exists in Gen-1 (`G`). |
| **Secret exit** | The **Bypass Valve**: a red-handled valve with its own fanfare, hidden off the main line. It often needs a carried **valve wheel** (Pocket Lift) or a Bottled Storm hit to turn. In a Hush House the secret exit is a second, hidden door. Either way the course reports `exit: 'secret'` to the overworld. |
| **Wild Tap / Wildwater / Wild Pearl** | The wonder moment (pillar 2). |
| **Golden Gear** | The existing hard-route collectible, one per course. |
| **Pennant** | The midpoint checkpoint (Gen-1 `K`). |
| **Path notation** | `A → B` means clearing A by its normal exit opens the path. `A ⇢ B` means A's secret exit opens it. `⇒` is a warp off the map edge. Every path is revealed from the node that earns it. |

**Completion is 200 units, half a percent each:** 61 courses × (clear + Gear + Pearl) = 183, plus 13 secret
exits and 4 chapels pressed.

---

## 1. Design pillars

1. **A world is a walkable place with two kinds of exit.** Each world is a 7–9 node map in the SMW structure:
   levels, a fortress with a mid-boss, a Hush House, a cottage or shop, the castle, and in four worlds a Valve
   Chapel. Each world has at least one Bypass Valve (13 across the campaign). They open chapels, cottages, a back
   gate into Valveheart, or **Upstream Sky**, the optional sky zone of six courses where rivers rise into the
   clouds. The main route never needs a secret exit.
2. **Wildwater: one wonder moment per course.** Each course hides a **Wild Tap**, a small winged brass faucet
   placed off the obvious line but easier to find than the Gear. Turning it ripples the screen, shifts the music
   into a new key and makes the course go **Wildwater**: an original, course-specific change to how the level
   plays. Examples are rain that freezes into steps, a tower that tilts 30°, crates that fall upward, or a heroine
   who becomes a shadow on paper screens. Wildwater lasts until she grabs the **Wild Pearl** at the end of that
   section, or until she loses a life (the tap can be turned again). No two Wildwaters are alike.
3. **The level-type mix grows each world.** Every world adds one new level type or power: water, dark,
   auto-scroll, mirror maze, vertical climb, descent or chase. Inside each world the order is still
   introduce → combine → subvert → test, now spread over 7–9 nodes.
4. **The game remembers.** Save v3 tracks the 200 completion units, the chapels pressed, where Gurgle is, the
   Spare Thermos, the Tool Roll, deaths per node and which NPC lines have been seen. Rivers on the map run back
   downhill as worlds are freed. Repaired bosses move in at home nodes. The title screen shows how far you are (§6).
5. **Six powers with movement consequences, a reserve and a companion.** The existing Springstep, Bottled Storm
   and Pocket Lift are joined by **Tidecoat** (water), **Ballast Boots** (heavy form) and **Bellows Glider**
   (glide and climb). A **Spare Thermos** holds a reserve power, and a **Tool Roll** of map items is used between
   courses. **Gurgle**, a cistern newt, is a ride companion who slurps and spits (§2).
6. **Fair mastery.** All eight roster heroines can reach every exit, Gear and Pearl with the shared moveset. A
   heroine's Y-button special (dash, double jump, pound and so on) may shorten a route but never gates one.
   Every hazard is telegraphed, and every blind drop has a visible tell.

---

## 2. Powers, reserve, map items and companion

The hit rule stays as in Gen-1: a hit costs the current power before a heart. Picking up a new power while
powered sends the old one to the Spare Thermos.

| Power | First found | Movement consequence | Counterplay / limits | Art needs |
| --- | --- | --- | --- | --- |
| **Springstep** (existing) | 1-1 cellar | A higher jump, plus hold-to-float that extends horizontal reach. Precision platforming. | Low ceilings bonk the float. Headwind corridors cancel it. Floating is slow, so chasers punish it. | Glowing spring soles, float pose, landing squash. Pip key poses queued in GEN2-ROUND-1. |
| **Bottled Storm** (existing, grows) | 1-h attic | A charged gust that strikes foes, valves, crates and open bosses, and spins turbines. **Gen-2:** a full charge fired in the air recoils her half a tile backward, a small air-dash she can use for routing. | Cork crabs and gasket plates absorb it. Crystal faces (W6) ricochet it back. Charging roots her on the ground. | Bottle-throw pose, gust projectile in three charge sizes, recoil pose. |
| **Pocket Lift** (existing, grows) | 1-2 potting shed | Lift and throw crates, stunned enemies, keys and valve wheels. Thrown crates land as steps. **Gen-2:** stack up to two crates and carry keys to fortress doors. | Carrying slows her run by 20% and blocks float and glide. A hit drops what she holds. Water floats crates away. | Lift-overhead, carry-walk, throw (the `moves` sheets cover it). |
| **Tidecoat** (new) | 2-2 | A waxed oilskin. Free eight-way swimming, swimming against currents, an underwater kick-dash, and a belly slide on wet ground. | Soggy on land: run speed −15% and a lower jump. Steam vents dry it off in one hit. | Swim cycle (8 frames), kick-dash, belly slide, oilskin pickup. |
| **Ballast Boots** (new) | 4-2 | Heavy form. Wind, currents and belts do not push her. She sinks and walks on riverbeds, breaks cracked floors by landing, flattens gasket golems in one stomp, and holds down seesaws and scale plates. She also makes noise, which opens echo gates (W6). | Shorter jump, no float or glide, faster falls, cannot swim. The noise wakes puddle mimics. Lightning rods (5-4) attract strikes to her. | Heavy walk, impact landing with dust ring, riverbed walk, boot pickup. |
| **Bellows Glider** (new) | 5-2 | A bellows pack with canvas fins. Hold jump to glide. Tap jump to pump short lifts, each draining the pressure gauge on her back. The gauge refills on the ground or inside updrafts. | Rain from umbrella mites soaks the canvas (no lift for 3 s). Low ceilings. Paper kites tangle the fins. No carrying while gliding. | Glide pose, pump pose (2 frames), gauge prop, soaked droop. |

**Spare Thermos (reserve).** One stored power shows on the HUD. Press Select to pour it out: it drops from the
top of the screen and bounces once before settling, so she can catch it even mid-jump. It is saved per slot.
*Art:* a thermos HUD icon and six power-drop icons.

**Tool Roll (map inventory).** Up to six items, used on the world map before entering a course:

- **Power vials**, one per power: start the next course with that power.
- **Gurgle Whistle**: call Gurgle to the next course's start.
- **Plumb Bob**: for one map walk, shows which nodes still hide a Bypass Valve, Gear or Pearl.
- **Spare Heart**: start with one extra heart.

Tool Roll items come from cottages, shops and chapel caches. *Art:* a leather tool-roll panel and seven item icons.

**Gurgle, the cistern newt (companion).** A round, rubbery amphibian with a water-tank belly and a siphon snout.
She meets him in 2-1, where he hatches from a rain barrel at the pennant. While she rides him:

- **Slurp:** his snout inhales a short cone, pulling in one small enemy, one item or a belly of water. Gasket
  golems are too heavy.
- **Spit:** fires the held enemy as a projectile. A held enemy keeps its own behaviour, so a spat rivet roller
  keeps rolling.
- **Spout hop:** spitting stored water straight down gives one extra lift per jump. Touching water or a puddle
  refills it.
- **Surface swim:** he swims on the water's surface and carries her across currents.
- **Weight:** he can be parked on a scale plate or seesaw while she goes on alone.

**On a hit,** Gurgle bursts into a puddle and she falls off. If she stands in the puddle for one second within
five seconds, he re-forms. Otherwise he drains back to the last pennant's rain barrel.

Gurgle will not enter Hush Houses (too scared), fortresses or castles (too hot). He waits at that node, and the
map shows him sitting there. *Art:* idle, walk, run, slurp, spit, spout hop, swim, puddle-burst and re-form, and
a ridden pose for each roster scale. He is a WAN clip candidate (t-025).

---

## 3. Campaign structure

### 3.1 Level types and what each world adds

| World | Courses | New this world | Level-type mix |
| --- | --- | --- | --- |
| 1 Bluebell Pipeworks | 7 | Bypass Valves, Hush House, first chapel, three base powers, Thermos | standard ×2, underground, vertical climb, house, fortress, tower castle |
| 2 Tideglass Marina | 7 | Water levels, **Tidecoat**, **Gurgle**, first shop, first Upstream Sky spout | standard, underwater, raft ride, lock puzzle, house, sea fort, castle |
| 3 Lantern Orchard | 7 | Dark courses (lanterns), carry chains, first on-rails cart | standard, dark ×2, house, fortress, auto-scroll cart, castle |
| 4 Clockwork Fair | 7 | **Ballast Boots**, auto-scroll rides, mirror-maze house | auto-scroll ×2, standard, mirror house, rhythm fortress, vertical, castle |
| 5 Cloudrail Commons | 7 | **Bellows Glider**, tall vertical climbs, airship deck | vertical ×2, wind, house, airship auto-scroll, fortress, castle |
| 6 Crystal Underworks | 7 | Reflection and echo logic, the first *descent* level | standard, lit-timing, water, house, descent, fortress, castle |
| 7 Night Market Rooftops | 7 | Chase courses (pursuer), three-way trade route | speed run, chase ×2, trade branch, house, fortress, castle |
| 8 Stardrain Citadel | 6 | Remix: every power and level type, back-gate secret | water remix, power gauntlet, memory house, fortress, vertical gauntlet, castle and escape |
| Upstream Sky | 6 | Expert courses, downspout warps, Downstream mode | one per spout theme, plus The Headwater |

### 3.2 Valve Chapels (switch palaces)

Pressing a chapel's great valve makes that colour's outlined blocks solid everywhere for the rest of the save. A
pressed chapel's coloured pipes glow on every world map.

**Hard rule:** chapel blocks only add. Every course can be finished, with every exit, Gear and Pearl, with no
chapel pressed. Chapel blocks make routes safer and open **chapel caches**: token and 1-up rooms, and a Tool Roll
item per chapel.

| Chapel | Reached by | Blocks made solid | Where they matter |
| --- | --- | --- | --- |
| **1-c Verdigris** (green) | 1-3 ⇢ Bypass Valve behind the waterfall | Pit fillers and safety ledges | W1–W4 early pits; cache in 1-1, 2-3 |
| **3-c Brass** (gold) | 3-2 ⇢ sealed root tunnel | High-road stairs to upper routes | Upper routes in 4-1, 5-1, 7-1, 8-2; cache in 3-3 |
| **4-c Cobalt** (blue) | 4-h ⇢ inside the mirror | Dams, underwater floors, current breaks | 2-2, 2-4, 6-3, 8-1, sky-1 |
| **6-c Rose** (pink) | 6-2 ⇢ the dead glowpipe | Crystal bridges that stay solid unlit; chase rails | 6-2, 6-4, 7-2, 7-4, 8-3, sky-4 |

A chapel course is 60–90 seconds: a short walk past its own outlined blocks, which turn solid the moment the
valve turns so the player sees the effect. Revisiting a chapel opens its cache room.

### 3.3 Upstream Sky (special zone)

There are five secret entrances, each an **updraft spout**: a waterfall that runs *up* off the top edge of the
world map, revealed when its Bypass Valve is found. Inside Upstream Sky the courses form a chain
(`sky-1 → … → sky-6`), so each spout lands partway along it.

| Spout | Found in | Lands at |
| --- | --- | --- |
| Lighthouse lamp | 2-h ⇢ | sky-1 Lamplight Rapids |
| Treetop firefly hole | 3-3 ⇢ | sky-2 Orchard Updraft |
| Windmill updraft | 5-2 ⇢ | sky-3 Cloudwell |
| The silent wall | 6-h ⇢ | sky-4 Prism Rain |
| Water-tower drain | 7-3 ⇢ | sky-5 Lantern Comet |

There are two **downspouts**, deliberate skips in the SMB3 warp spirit: sky-2 ⇢ `w6-start` and sky-4 ⇢ `w8-start`.
Spouts and downspouts work in both directions once open.

**sky-6 The Headwater** opens from sky-5's normal exit. Clearing it switches on **Downstream mode** (§6).

### 3.4 Gen-1 reuse

Each Gen-1 stage becomes the spine of one Gen-2 course (`stage` in the JSON). The course is extended with a
pennant, sub-rooms, a Bypass Valve where one is listed, a Wild Tap and Wildwater. Gen-1 x-4 boss stages become the
castles.

| Gen-1 → node | | | |
| --- | --- | --- | --- |
| 1-1→1-1 | 1-2→1-2 | 1-3→1-3 | 1-4→1-castle |
| 2-1→2-1 | 2-2→2-3 | 2-3→2-4 | 2-4→2-castle |
| 3-1→3-1 | 3-2→3-2 | 3-3→3-3 | 3-4→3-castle |
| 4-1→4-1 | 4-2→4-3 | 4-3→**4-h** | 4-4→4-castle |
| 5-1→5-1 | 5-2→5-2 | 5-3→5-3 | 5-4→5-castle |
| 6-1→6-1 | 6-2→6-2 | 6-3→6-3 | 6-4→6-castle |
| 7-1→7-1 | 7-2→7-2 | 7-3→7-3 | 7-4→7-castle |
| 8-1→8-1 | 8-2→8-2 | 8-3→8-3 | 8-4→8-castle |

Second uses as rooms and set-pieces (not in the JSON):

- 1-2's piston shaft becomes the lower climb of 1-f.
- 1-3's moving steps become the dam rooms of 1-4.
- 2-1's bobbing piers become the rapids of sky-1.
- 3-1's springfruit slope becomes sky-2's opening.
- 3-2's cellar, 1-1's courtyard and 5-2's windmill are the three framed exhibits inside 8-2.
- 5-2's wind corridors are reused in sky-3.
- 6-2's lit bridges are reused in sky-4.
- 7-1's sign run is reused in sky-5.
- Every x-4 arena returns in miniature in 8-f's mid-boss medley.

---

## 4. The eight worlds

Each world below gives its route, its mid-boss, and a beat sheet for every course. Beat sheet fields: first-clear
target · mechanic beat · **Mid** (pennant) · **Sub** (sub-areas) · **Secret** (Bypass Valve and Gear) ·
**Wildwater** · **Test**.

### World 1: Bluebell Pipeworks (template world)

```
w1-start → 1-1 → 1-2 → 1-h → 1-3 → 1-f → 1-4 → 1-castle ⇒ w2-start
                        1-h ⇢ 1-b Tinker's Cottage
                               1-3 ⇢ 1-c Verdigris Chapel (behind the waterfall)
```

Nine nodes, matching the GEN2-ROUND-1 map plate: seven clearings, the pump tower at the far end, a cottage beside
the path and the hidden clearing behind the waterfall. Only the three existing powers and the Thermos are needed.
Mid-boss: **Foreman Flange**. New haunts: **teacup haunts**, which drift in formation toward the nearest open tap,
and **wallpaper shades**, which step out of the pattern when she stands still for more than two seconds (they
punish idling).

**1-1 Rainy Courtyard** (level, Gen-1 1-1, 3.5 min). *Introduce* momentum on wet slopes, bopping pumpbugs and
valve gates. **Mid:** the fountain plaza after the first high/low split. **Sub:** a pipe door under the fountain
leads to a flooded cellar with a token trail and the Springstep box. **Secret:** the Gear sits on the gutter high
road. Throw a stunned rivet roller into a valve to raise the ledge. **Wildwater, "Rain Stands Still":** the Tap is
behind a rain barrel at the cellar exit. Every raindrop freezes as a one-way step, and the courtyard becomes a climb
to the rooftops. The Pearl hangs on the bell. **Test:** the downhill finish, with three pumpbugs speeding up toward
her on the slope.

**1-2 Copper Greenhouses** (level, Gen-1 1-2, 4 min). *Introduce* rising pistons, then *combine* them with
pumpbugs riding the pistons. **Mid:** the orchid house. **Sub:** a greenhouse chimney (a vertical room with its own
camera bounds) and a potting shed through a pipe door. The shed has the Pocket Lift box and teaches crate steps.
**Secret:** the Gear is above the glass roof. Throw a crate onto a piston so it carries her past the roof seam.
**Wildwater, "Overgrowth":** the Tap is in the shed rafters. Vines burst through the glass and every piston becomes
a bluebell stalk that bounces on contact. The Pearl tops the tallest bloom. **Test:** a staircase of
out-of-phase pistons over a pit lined with steam vents.

**1-h The Drip Parlour** (Hush House, new, 4 min). *Exit logic:* the rooms loop, and the true door is whichever
one the ceiling drips run toward (upward, against sense). Drips change direction in later rooms. **Mid:** the
music room. **Sub:** the attic by ladder, which holds the Bottled Storm box, and the cellar by floor grate.
**Secret (⇢ 1-b):** in the attic, a peeling wallpaper panel hides a back stair. Blasting it with Bottled Storm is
the lesson. **Gear:** in the cellar, guarded by wallpaper shades that only move while she stands still.
**Wildwater, "Upside Parlour":** the Tap is inside the grandfather clock. Gravity follows the drips, so ceilings
become floors for one full loop. The Pearl sits on the chandelier. **Test:** the final hallway, where the drip
direction flips mid-room twice.

**1-b Tinker's Cottage** (bonus). This is Teo's old workshop. Three pipes hum, and she picks the one running
uphill to win a Tool Roll item. It refills each time a new course in World 1 is cleared. After 1-castle,
**Madame Pressure** (repaired) runs it.

**1-3 Buried Meter** (level, Gen-1 1-3, 4.5 min). *Subvert:* steps that slide away when she lands on them, and an
underground route that runs under the main path. **Mid:** the dial chamber. **Sub:** a vertical shaft down into
the meter-works, and a flooded crawlway. **Secret (⇢ 1-c):** a valve wheel lies in the meter room. Carry it up the
moving steps to the grotto behind the waterfall and fit it to the Bypass Valve. **Gear:** under the dial, under a
low ceiling that needs Springstep's float, not its height. **Wildwater, "Meter Runs Backward":** the Tap is inside
the dial. The moving steps reverse and the screen scrolls *back* toward the start along a ceiling route that did
not exist before. The Pearl waits at the entrance arch. **Test:** a moving-step descent while rivet rollers climb
up toward her.

**1-c Verdigris Chapel** (chapel, 75 s). A mossy walk past green outlined blocks, then the great valve. The blocks
turn solid as the valve turns, and every world map's green pipes light up.

**1-f Rustbolt Keep** (fortress, new, 5 min). *Combine* pistons, crushing presses and steam vents, and introduce
the fortress **key door**: carry the key with Pocket Lift, and a hit drops it. **Mid:** the boiler. **Sub:** a
crawlspace beneath the presses (1-2's piston shaft, reused). **Secret:** the Gear is in a press alcove that opens
for one press cycle. **Wildwater, "Assembly Line":** the Tap is in the foreman's office. Every enemy is boxed into
a crate and the floor becomes a belt, so she stacks the moving crates into stairs. **Mid-boss Foreman Flange:**
rides a rivet roller and whistles one beat before sending rollers down the ramps. In phase two he mounts a wheel
twice his height. Stun a roller and throw it into his axle. **Test:** the press corridor, four presses timed out
of phase.

**1-4 Sluicegate Steps** (level, new, vertical climb, 4 min). *Combine* pistons, moving steps and valve gates on
a dam face, using rooms built from 1-3's moving steps. **Mid:** the spillway ledge. **Sub:** a ladder room inside
the dam. **Secret:** the Gear is on a ledge behind the falling water, reached by floating with Springstep through
the sheet. **Wildwater, "Spillway Opens":** water sheets run upward and become escalators she rides. **Test:** the
last gate sequence with the reservoir rising below her (the first rising-water beat in the game).

**1-castle The Pump Tower** (castle, Gen-1 1-4, 6 min with the boss). A vertical tower of pistons and vents, with
a boiler loop that holds a heart. **Mid:** the stairs before the boss gate. **Secret:** the Gear is on the
tower's outside face, through a window. **Wildwater, "Tower Tilt":** the tower leans 30°, every floor becomes a
slope and pumpbugs slide downhill like bowling balls. **Boss Madame Pressure:** her gauge needle swings red one
beat before each steam burst. In phase two she vents the floor, which lifts her into float zones. In phase three
the room pressurizes and Bottled Storm must hit her relief valves in order. **Test:** the boss.

### World 2: Tideglass Marina

```
w2-start → 2-1 → 2-2 → 2-3 → 2-h → 2-4 → 2-f → 2-castle ⇒ w3-start
                  2-2 → 2-s Chandler's Shop
                               2-h ⇢ sky-1 (updraft spout, warp up)
```

Mid-boss: **Bosun Brine**, a cork crab as big as a dinghy.

**2-1 Floating Wharves** (level, Gen-1 2-1, 4 min). *Introduce* currents and bobbing piers in a first half
without a companion. **Mid:** the fish market, where **Gurgle** hatches from a rain barrel. The second half
teaches slurp, spit and spout hop over open water. **Sub:** an under-pier tunnel. **Secret:** the Gear is on a
buoy chain that only a spout hop reaches. **Wildwater, "High Tide":** the sea rises and the wharves become a swim
course, with crane tops as islands. **Test:** a run of sinking piers in a cross-current, with clockwork minnows
leaping.

**2-2 Kelpglass Shallows** (level, new, underwater, 4 min). *Introduce* the **Tidecoat**: glass-kelp forests,
with currents as rivers. **Mid:** an air-bell pocket. **Sub:** a wreck's hold. **Secret:** the Gear is behind a
current only the Tidecoat can swim against. Cobalt blocks later add a resting floor. **Wildwater, "Low Tide":** the
water drains in two seconds and every fish flops as a bouncy platform, so she *runs* where she swam. **Test:** a
current slalom past cork crabs that unplug vents in bursts.

**2-s Chandler's Shop** (shop). Tokens buy the Tidecoat and Springstep vials, the Gurgle Whistle and a Spare
Heart. After 2-castle, **Captain Barnaclejack** (repaired) keeps the till.

**2-3 Glassboat Boneyard** (level, Gen-1 2-2, 4.5 min). *Combine* throwing and riding driftwood with Gurgle.
Glass gulls steal tokens and drop all of them when caught. **Mid:** inside a beached hull. **Sub:** hull rooms
through doors, and a mast climb. **Secret:** the Gear is in the crow's nest, reached by riding a thrown driftwood
log up a waterspout. **Wildwater, "Ghost Fleet Sails":** the wrecks refloat and sail across the screen in a
ship-to-ship auto-scroll. **Test:** a raft ride under gull dive-bombs.

**2-h The Lighthouse Hush** (Hush House, new, 4 min). *Exit logic:* rooms exist only while the beam lights them.
Hitting the lens with Bottled Storm turns the beam and changes which rooms exist. **Mid:** the keeper's study.
**Sub:** the spiral stair and the oil cellar. **Secret (⇢ sky-1):** on the beam's third turn, climb past the lamp
onto the outside gallery. The Bypass Valve in the lens housing turns the beam into the first updraft spout.
**Wildwater, "Lamp Out":** the house goes dark, only her scarf glows, and wallpaper shades show only as outlines.
**Test:** a lens-timed staircase that exists for two seconds per turn.

**2-4 Moonpool Locks** (level, Gen-1 2-3, 5 min). *Subvert* the canal gates: filling a lock lowers the water
*above* her, and she climbs by draining. **Mid:** the lock-keeper's hut. **Sub:** three lock chambers, each a room
with its own water level. **Secret:** the Gear is in a flooded lock that only the right order of valves drains.
**Wildwater, "Moonpool Inversion":** water and air swap places, so the water hangs as a ceiling band and she swims
in the "sky". **Test:** the three-lock sequence against a tide timer, with minnows.

**2-f Barnacle Bulwark** (fortress, new, 5 min). Water levels rise and fall inside a sea fort. The Tidecoat helps
but is optional. **Mid:** the powder room. **Sub:** a flooded magazine. **Secret:** the Gear is in a cell that
opens only at low water. **Wildwater, "Barnacle Bloom":** barnacles sprout across the walls as handholds, giving a
wall-climb section. **Mid-boss Bosun Brine:** plugs the arena drains so the water rises. His claws clack twice
before he lunges. A thrown crate pops him out of a drain and the water rushes out with him. **Test:** a rising-water
shaft escape.

**2-castle Tidal Drydock** (castle, Gen-1 2-4, 6 min). Board the dry-docked ship. **Mid:** the gangway.
**Secret:** the Gear is under the keel. **Wildwater, "Hull Roll":** the ship rolls over, and she runs along the
keel while the deck becomes the ceiling. **Boss Captain Barnaclejack:** his anchor glows before it swings, and the
tide always pulls the same way. In phase two the tide tilts the whole arena. In phase three the dock floods. Gurgle
waits outside, but the Tidecoat shines here. **Test:** the boss.

### World 3: Lantern Orchard

```
w3-start → 3-1 → 3-2 → 3-h → 3-3 → 3-f → 3-4 → 3-castle ⇒ w4-start
           3-1 → 3-b Beekeeper's Cottage
                  3-2 ⇢ 3-c Brass Chapel
                               3-3 ⇢ sky-2 (warp up)
```

Mid-boss: **Old Pulpjaw**, a living cider press.

**3-1 Apricot Slope** (level, Gen-1 3-1, 3.5 min). *Introduce* springfruit: bounce on it, carry it and throw it to
make bounce pads. **Mid:** the picker's ladder. **Sub:** a climb up the inside of a hollow trunk. **Secret:** the
Gear is on the canopy, reached by a chain of three thrown springfruit. **Wildwater, "Harvest Wind":** every fruit
drops at once and rolls downhill as a bouncing avalanche she rides down. **Test:** a spring-hare bounce chain up a
cliff.

**3-b Beekeeper's Cottage** (bonus). Catch falling honey lanterns in a jar for 1-ups and a Tool Roll item.
Repaired **Overripe Baron** later, telling bad fruit jokes.

**3-2 Rootcellar** (level, Gen-1 3-2, dark, 4.5 min). *Combine* carrying with light: a moss lantern lights a short
radius, and scale plates need fruit or Gurgle's weight. **Mid:** the cider-barrel room. **Sub:** three root
tunnels. **Secret (⇢ 3-c):** carry a lantern into the sealed tunnel, where the light shows a Bypass Valve no unlit
view reveals. **Gear:** in a pitch-black alcove, found by the sound of a hare. **Wildwater, "Roots Wake":** roots
grow and retract like bridges that follow her light. **Test:** carrying a flickering lantern across crumbling roots
before it dims.

**3-c Brass Chapel** (chapel, 75 s). Gold outlined stairs turn solid all the way up the nave.

**3-h Hollow Cider House** (Hush House, new, 4 min). *Exit logic:* doors "ferment". A door changes its destination
whenever a teacup haunt passes through it. Follow one particular haunt, the chipped one, through the house to the
exit. **Mid:** the vat room. **Sub:** the attic still. **Gear:** the chipped haunt detours past it once. Normal exit
only. **Wildwater, "Bubbling Over":** cider rises as a buoyant liquid she can launch out of for very high jumps.
**Test:** a six-door chase in which a second haunt tries to scramble the doors.

**3-3 Firefly Canopies** (level, Gen-1 3-3, dark, 5 min). *Subvert:* firefly swarms showed the path in 3-2, but
here one swarm leads to a pit. The true path is lit by swarms of exactly three. **Mid:** the lantern bridge.
**Sub:** treehouses linked by ziplines. **Secret (⇢ sky-2):** follow the single blue firefly off-screen up through
a gap in the canopy to the Bypass Valve in the treetop. **Gear:** a dark canopy drop with a moss-lantern tell.
**Wildwater, "Lights On":** every firefly ignites at once, the course is fully lit and its hidden platforms appear,
but so do the sleeping spring hares. **Test:** the false-swarm crossing.

**3-f Pressroom Keep** (fortress, new, 5 min). *Combine* presses, a conveyor of springfruit and key doors.
**Mid:** the bottling line. **Sub:** a pulp drain. **Secret:** the Gear is in a press bed, reached by riding a
pressed fruit's rebound. **Wildwater, "Juice Flood":** the keep fills with sticky juice that slows her walk but lets
her cling to walls. **Mid-boss Old Pulpjaw:** drips gather under his plate before each slam. Lure him to press
springfruit, and the rebound launches her to his release valve. **Test:** a crusher corridor where only a carried
fruit is safe to stand on.

**3-4 Windfall Ridge** (level, new, on-rails cart, 4 min). *Combine* the world on a fruit cart that runs downhill
through a storm. Lantern tunnels go dark and moss lanterns on the walls light the next jump. **Mid:** the cart
depot. **Sub:** a switch to the lower track. **Secret:** the Gear is on a high track, reached by jumping off the
cart at the broken trestle. **Wildwater, "Orchard Takes Flight":** the cart sprouts seed sails and floats, becoming
a gentle flying auto-scroll. **Test:** a dark-tunnel jump sequence.

**3-castle Hanging Conservatory** (castle, Gen-1 3-4, 6 min). A climb through swinging planters. **Mid:** the
palm house. **Secret:** the Gear is on the roof lantern. **Wildwater, "Greenhouse Spin":** the conservatory
rotates 90°, so the swinging planters hang as stairs. **Boss The Overripe Baron:** he wobbles and drips before
every belly-slam. In phase two he spits seeds that sprout as platforms. In phase three he goes soft and bouncy,
and she must bounce *on* him to reach the stem. **Test:** the boss.

### World 4: Clockwork Fair

```
w4-start → 4-1 → 4-2 → 4-3 → 4-h → 4-f → 4-4 → 4-castle ⇒ w5-start
                  4-2 → 4-s Prize Booth
                               4-h ⇢ 4-c Cobalt Chapel
```

Mid-boss: **The Calliope**, a steam organ that plays to fight.

**4-1 Parade Street** (level, Gen-1 4-1, auto-scroll, 4 min). *Introduce* auto-scroll on conveyor floats. **Mid:**
the bandstand float. **Sub:** float interiors, rooms that ride along with the scroll. **Secret:** the Gear is on a
balloon float, reached by a brass-block upper route or a well-timed hop off a stilt-walker. **Wildwater, "Parade
Reversal":** the floats turn round and the scroll reverses. **Test:** float-hopping past gasket golems.

**4-2 Strongman Alley** (level, new, 4 min). *Introduce* **Ballast Boots**: high-striker bells she rings by
landing, seesaws, cracked floors and belts that cannot push her. **Mid:** the weigh-in tent. **Sub:** an
under-stage basement through a cracked floor. **Secret:** the Gear tops the tallest high-striker. Pour Springstep
from the Thermos to make the jump after ringing it, which teaches power swapping. **Wildwater, "Big Top
Gravity":** gravity triples and every jump is tiny, but the boots smash through anything. **Test:** a seesaw
launch chain using a gasket golem as the counterweight.

**4-s Prize Booth** (shop). Tickets (tokens) buy the Ballast vial, Plumb Bob and Spare Heart. Repaired
**Tick-Tock Duchess** later.

**4-3 Cottongear Coaster** (level, Gen-1 4-2, auto-scroll, 4.5 min). *Combine:* the boots weigh a car down so it
takes the lower track at forks, and it rides light without them. **Mid:** the station. **Sub:** a maintenance
tunnel. **Secret:** the Gear is at the broken loop's apex. **Wildwater, "Spun Sugar":** the tracks dissolve into
candy-floss clouds she bounces between. **Test:** a five-fork switch sequence at speed.

**4-h Mirror Ticket Hall** (Hush House, Gen-1 4-3, 4.5 min). *Exit logic:* every time she turns around, the room
mirrors left to right. The true exit appears only in reflections. **Mid:** the ticket window. **Sub:** a
hall-of-mirrors loop. **Secret (⇢ 4-c):** a cracked floor-mirror, broken with Ballast Boots, drops her into the
mirror side, where the Bypass Valve stands. **Wildwater, "Hall of Two":** a mirror twin copies her moves on the
other side, and both must stand on plates at once. **Test:** a corridor that must be crossed with exactly six
turns.

**4-c Cobalt Chapel** (chapel, 75 s). Blue dams seal a flooding hall as the valve turns.

**4-f Calliope Keep** (fortress, new, 5 min). Platforms move only on the beat. **Mid:** the organ loft.
**Sub:** the bellows room. **Secret:** the Gear is behind an off-beat door. **Wildwater, "Music Box":** the
keep winds down like a music box, and platforms move only while *she* moves. **Mid-boss The Calliope:** its pipes
light in sequence before each volley of note-shaped steam puffs. Stomp its keys to play the volley back at it.
**Test:** a beat corridor at double tempo.

**4-4 Big Top Rigging** (level, new, vertical, 4.5 min). *Subvert* trampolines: Ballast Boots kill a bounce, so
she switches between heavy and light while climbing the tent. **Mid:** the trapeze platform. **Sub:** inside a
tent pole. **Secret:** the Gear is on the high wire. **Wildwater, "Tent Collapse":** the canvas drops into one
huge trampoline sheet. **Test:** trapeze swings timed to a chime.

**4-castle Clocktop Big Wheel** (castle, Gen-1 4-4, 6 min). Ride the wheel's gondolas up to the clock. **Mid:**
the top gondola. **Secret:** the Gear is on the hub. **Wildwater, "Clock Stops":** everything freezes except her,
and frozen enemies become platforms until the clock restarts. **Boss Tick-Tock Duchess:** her chimes count down,
and the fourth chime is always the swing. In phase two she rewinds the enemies. In phase three the wheel spins
free. **Test:** the boss.

### World 5: Cloudrail Commons

```
w5-start → 5-1 → 5-2 → 5-h → 5-3 → 5-f → 5-4 → 5-castle ⇒ w6-start
                  5-2 → 5-b Kitemaker's Loft
                  5-2 ⇢ sky-3 (warp up)
```

Mid-boss: **The Weathercock**, a brass rooster weathervane.

**5-1 Ropeway Home** (level, Gen-1 5-1, vertical, 4 min). *Introduce* cable-car lifts up a cliff of hanging
homes. **Mid:** the cable station. **Sub:** cliffside homes through their front doors. **Secret:** the Gear is
reached by running along the cable itself. **Wildwater, "Cables Snap Loose":** the cables whip like skipping ropes,
giving a rhythm climb. **Test:** lift timing while umbrella mites rain on her.

**5-2 Windmill Platform** (level, Gen-1 5-2, 4.5 min). *Introduce* the **Bellows Glider** in wind corridors.
**Mid:** the miller's deck. **Sub:** windmill interiors whose gear rooms rotate. **Secret (⇢ sky-3):** ride the
updraft above the top sail into the cloud bank, where the Bypass Valve sits on a cloud island. **Gear:** inside the
sail hub. **Wildwater, "Tailwind":** every corridor reverses into a tailwind and the course becomes a high-speed
glide race. **Test:** a crosswind glide over a gap, with paper kites.

**5-b Kitemaker's Loft** (bonus). Hold a paper kite's ribbon and steer through rings for items. Repaired
**Admiral Gust** later.

**5-h The Becalmed Inn** (Hush House, new, 4.5 min). *Exit logic:* no wind blows indoors, so the glider is dead
weight except at open windows. Weathervanes over the doors point to the true route, but only while a window is
open. **Mid:** the dining room. **Sub:** the bell tower. **Gear:** the far side of a window draught. Normal exit
only. **Wildwater, "Storm Indoors":** the windows burst and the furniture flies as platforms. **Test:** a window
relay crossing four rooms on one breath of the glider.

**5-3 Airship Sorting Yard** (level, Gen-1 5-3, auto-scroll, 5 min). *Subvert* falling cargo: crates are the
only floor on an airship deck, and they rest a moment before falling. **Mid:** the sorting crane. **Sub:** the
cargo hold. **Secret:** the Gear is in a crate she must carry off the ship onto the next one. **Wildwater, "Cargo
Rains Up":** crates fall upward. **Test:** the final sorting chute.

**5-f Gondola Keep** (fortress, new, 5 min). Wind direction changes room by room. **Mid:** the winch room.
**Sub:** an outside walkway. **Secret:** the Gear is upwind, reachable only with Ballast Boots. **Wildwater,
"Dead Calm":** all wind stops, the glider routes fail, and the keep becomes a precise jump course. **Mid-boss The
Weathercock:** its tail rattles before it spins and changes the wind. The boots hold her in place, and Bottled
Storm jams its pivot. **Test:** crossing the windmill blades.

**5-4 Lightning Rod Run** (level, new, vertical, 4.5 min). *Combine* a storm-tower climb with lightning strikes,
each telegraphed by a humming rod. The boots attract strikes, so wearing them is a risk. **Mid:** the transformer
landing. **Sub:** the tower's coil room. **Secret:** the Gear is on the top rod, reached in the gap between two
strikes. **Wildwater, "Charged":** she is magnetized to every metal surface and walks walls and ceilings. **Test:**
a climb of four rods in a strike sequence.

**5-castle Thunder Station** (castle, Gen-1 5-4, 6 min). **Mid:** the signal house. **Secret:** the Gear is on
the storm mast. **Wildwater, "Eye of the Storm":** dead calm with zero gravity, and everything floats. **Boss
Admiral Gust:** his sails fill and creak before each gale. In phase two the station rotates. In phase three the
fight moves inside the eye. **Test:** the boss.

### World 6: Crystal Underworks

```
w6-start → 6-1 → 6-2 → 6-h → 6-3 → 6-f → 6-4 → 6-castle ⇒ w7-start
           6-1 → 6-b Prospector's Cabin
                  6-2 ⇢ 6-c Rose Chapel
                         6-h ⇢ sky-4 (warp up)
(sky-2 ⇢ w6-start downspout lands here)
```

Mid-boss: **The Echo Warden**, a bronze bell.

**6-1 Silica Steps** (level, Gen-1 6-1, 4 min). *Introduce* reflection guidance: some platforms show only in the
pool's reflection, and Bottled Storm ricochets off crystal faces. **Mid:** the quartz arch. **Sub:** the drip
cave. **Secret:** the Gear is visible only in reflection, so she jumps "blind" by reading the pool. **Wildwater,
"Through the Pool":** she steps into the reflection and plays the course upside down. **Test:** a ricochet puzzle
under a time limit.

**6-b Prospector's Cabin** (bonus). Echo chimes: listen and repeat a chime sequence for items. Repaired **Prism
Mole** later.

**6-2 Glowpipe Caverns** (level, Gen-1 6-2, 4.5 min). *Combine* crystal bridges that stay solid only while the
glowpipes pulse with reflections. **Mid:** the miners' lamp room. **Sub:** a lower mine. **Secret (⇢ 6-c):** carry
a glowstone (Pocket Lift) to the dead glowpipe at a dead end. Lit, it reveals the Bypass Valve. **Gear:** a
bridge run of three pulses. **Wildwater, "Blackout Beat":** the light pulses to the music, so she plays by rhythm.
**Test:** a pulse bridge with a puddle mimic at its far end.

**6-c Rose Chapel** (chapel, 75 s). Pink crystal bridges stay solid as the lights go out.

**6-h Hall of Hums** (Hush House, new, 4.5 min). *Exit logic:* each door hums a pitch, and the exit is the door
that answers the note the chipped haunt sings. Crouch-walk on quiet floors to keep the wallpaper shades asleep.
**Mid:** the organ alcove. **Sub:** the whispering gallery. **Secret (⇢ sky-4):** one wall gives no echo. Hit it
with Bottled Storm to find the Bypass Valve. **Wildwater, "Hush Breaks":** every haunt sings at once and the house
becomes a chase. **Test:** a three-note door sequence while a shade stalks her.

**6-3 Echo Sluice** (level, Gen-1 6-3, water, 5 min). *Subvert* noise: gates open to sound (pound, Ballast landing,
Bottled Storm), but noise wakes puddle mimics. **Mid:** the sluice control. **Sub:** a flooded gallery for the
Tidecoat. **Secret:** the Gear is behind the quietest gate, opened by a single dropped crate. **Wildwater, "Sound
Made Solid":** her footsteps leave solid ring-waves she can stand on. **Test:** a noise-gate sequence over open
water.

**6-f Quartz Keep** (fortress, new, 5 min). Ricochet halls. **Mid:** the cutting room. **Sub:** a geode vault.
**Secret:** the Gear is behind a three-bounce ricochet. **Wildwater, "Crystal Growth":** crystals grow where she
lands, leaving ledges for the rest of that section. **Mid-boss The Echo Warden:** it tilts before ringing and
repeats her last three actions back at her as shockwaves. Vary your moves and it hits itself. **Test:** the echo
corridor.

**6-4 The Long Drop** (level, new, descent, 4 min). *Introduce* a course that goes *down*. The camera frames
below her. The Bellows Glider slows the fall, and Ballast Boots break through crystal floors. **Mid:** a
mid-shaft ledge. **Sub:** a side cave entered mid-fall. **Secret:** the Gear is in that cave, entered by gliding
against the shaft wind. **Wildwater, "Falling Up":** gravity reverses and she falls back up the shaft through
routes she passed. **Test:** a choice between gliding and dropping through a field of mimic puddles.

**6-castle The Geode Filter** (castle, Gen-1 6-4, 6 min). **Mid:** the filter bed. **Secret:** the Gear is in a
prism alcove. **Wildwater, "Prism Split":** she splits into three coloured copies under one control, each lighting
a different bridge. **Boss Prism Mole:** light bends toward the spot it will burrow up through. It digs faster in
each phase, and in the last phase it splits the light four ways. **Test:** the boss.

### World 7: Night Market Rooftops

```
w7-start → 7-1 → 7-2 → 7-3 → 7-h → 7-f → 7-4 → 7-castle ⇒ w8-start
                  7-2 → 7-s Lantern Stall
                         7-3 ⇢ sky-5 (warp up)
```

Mid-boss: **Sir Steepwell**, captain of the tea-kettle knights.

**7-1 Neon Tiles** (level, Gen-1 7-1, 4 min). *Introduce* rooftop speed: momentum on tiles, with sign letters as
blinking platforms. **Mid:** the noodle-stand roof. **Sub:** attic laundries. **Secret:** the Gear is up a
brass-block high road, or reached with a full-speed long jump. **Wildwater, "Neon Rush":** the signs come alive and
slide, giving a forced-speed rhythm sprint. **Test:** a blink-timed sign run at full speed.

**7-2 Chimney Lantern Chase** (level, Gen-1 7-2, chase, 4.5 min). *Introduce* the pursuer: a soot tide rises
from the chimneys while chimney spirits arc soot across the climb. **Mid:** the bell roof, where the tide pauses.
**Sub:** a flue climb. **Secret:** the Gear is a short detour that costs exactly the slack the tide allows.
**Wildwater, "Lanterns Fly":** every paper lantern lifts off, and she rides the swarm upward ahead of the soot.
**Test:** the last climb, where the tide speeds up.

**7-s Lantern Stall** (shop). A barter shop: swap one Tool Roll item for another, or pay tokens. Repaired
**Umbrella Dragon** later.

**7-3 Midnight Plumbing Bazaar** (level, Gen-1 7-3, 5 min). *Three-way trade:* at the pennant, three vendors each
sell a route. The high road costs her current power, the middle road costs Gurgle (he waits at the node), and the
low road costs a heart. **Secret (⇢ sky-5):** refuse all three. A fourth route through the drain grate under the
stalls leads to the Bypass Valve on the water tower. **Sub:** each route is its own room chain. **Gear:** on the
middle route. **Wildwater, "Market Folds Up":** the stalls fold into one tall tower. **Test:** whichever route she
chose, each ends in its own beat.

**7-h The Paper Lantern Teahouse** (Hush House, new, 4.5 min). *Exit logic:* shadows on the paper screens show the
true layout, and sliding a screen redraws the rooms. Tea-kettle knights patrol. **Mid:** the tea room. **Sub:**
the garden pavilion. **Gear:** in a room seen only in shadow. Normal exit only. **Wildwater, "Shadow Play":** she
becomes a shadow walking along the screens. **Test:** a screen-sliding puzzle under a kettle's whistle timer.

**7-f Pagoda Keep** (fortress, new, 5 min). Tiered floors with kettle steam vents. **Mid:** the third tier.
**Sub:** a bell loft. **Secret:** the Gear is on the eaves outside. **Wildwater, "Steeping":** the keep fills with
rising tea and floating cups become boats. **Mid-boss Sir Steepwell:** he whistles before he lunges, and she
strikes when the steam stops. In phase two he boils over the floor. **Test:** steam-timed tiers.

**7-4 Laundry Line Leap** (level, new, chase plus auto-scroll, 4.5 min). *Combine:* the Umbrella Dragon's shadow
chases her across laundry lines, and it snaps its canopy shut before each dive. **Mid:** a water-tower roof.
**Sub:** a drying loft. **Secret:** the Gear hangs from a dive-cut line. **Wildwater, "Washday Wind":** the laundry
inflates into floating sails. **Test:** three dive dodges on a single line.

**7-castle Market Clock Spire** (castle, Gen-1 7-4, 6 min). **Mid:** the clock face. **Secret:** the Gear is on a
pendulum. **Wildwater, "Hands Move":** the clock hands become platforms that turn in real time. **Boss The Umbrella
Dragon:** it snaps its canopy shut right before it dives. In phase two it rains from above. In phase three it
fights in the bell cage. **Test:** the boss.

### World 8: Stardrain Citadel

```
w8-start → 8-1 → 8-2 → 8-h → 8-f → 8-3 → 8-castle   (finale)
                        8-h ⇢ 8-castle (back gate)
                                     8-3 → 8-s The Last Tap Room
(sky-4 ⇢ w8-start downspout lands here)
```

Mid-boss: **Undercurator Ewer**, Lady Spigot's polite water-jug assistant.

**8-1 Reservoir Assault** (level, Gen-1 8-1, 5 min). *Test* currents: Gurgle, the Tidecoat and Cobalt dams, a
W2 remix. **Mid:** the intake grille. **Sub:** a pump gallery. **Secret:** the Gear is in the current of a turbine
intake. **Wildwater, "Reservoir Empties":** the basin drains, leaving a canyon of beached machinery. **Test:** a
crossing of three currents.

**8-2 The Pump Archives** (level, Gen-1 8-2, 5.5 min). *Every power:* each section needs a different power, from
power booths. **Mid:** the reading room. **Sub:** three framed exhibits she steps into, remixes of 1-1, 3-2 and
5-2. **Secret:** the Gear needs a Thermos swap mid-jump. **Wildwater, "Archives Open":** filing drawers slide out
as staircases. **Test:** a six-booth section with one booth broken.

**8-h The Curator's Gallery** (Hush House, new, 5 min). *Exit logic, built on memory:* paintings of the seven
worlds are doors, and the exit is the painting that matches *her current save*. A world whose river she has freed
is painted with its water running downhill. **Mid:** the sculpture hall. **Sub:** the restoration studio.
**Secret (⇢ 8-castle):** the painting of Valveheart's service lift is a back gate past 8-f and 8-3, a deliberate
replay shortcut that still leads to the full boss. **Wildwater, "Paint Runs":** the paintings drip and flood the
gallery with paint currents. **Test:** a sequence of four paintings.

**8-f Spillway Bastion** (fortress, new, 5.5 min). A reversing spillway. **Mid:** the gatehouse. **Sub:** the
overflow tunnels. **Secret:** the Gear is behind the spillway curtain. **Wildwater, "Backflow":** the spillway runs
uphill as a moving staircase. **Mid-boss Undercurator Ewer:** bows before each pour. In phase two Ewer does the
seven earlier mid-bosses' tricks in miniature, in order. **Test:** the medley.

**8-3 The Sky Siphon** (level, Gen-1 8-3, vertical gauntlet, 6 min). A climb up the inside of the siphon using
updrafts, pistons, boots and Rose rails. **Mid:** the halfway valve. **Sub:** three side chambers. **Secret:** the
Gear is outside the siphon on a window ledge. **Wildwater, "Siphon Stalls":** the water hangs in a column she swims
up. **Test:** a full-stack climb with no power booths.

**8-s The Last Tap Room** (shop). The last shop. Teo's handwritten notes line the walls, and new notes appear for
each Bypass Valve she has found.

**8-castle Valveheart** (castle, Gen-1 8-4, 6 min plus the escape). **Mid:** the heart gate (a back-gate entry
starts here). **Secret:** the Gear is in Teo's cell. **Boss Lady Spigot:** whichever valve hisses is the one she
opens. Her three phases echo the worlds. In phase three Teo signals from inside and opens a valve on her cue.
**Wildwater, "Teo's Tap":** Teo turns the Wild Tap from inside, and the citadel goes Downstream for the escape. The
Pearl is waiting at the outflow. **Test:** the escape run, then the reunion.

---

## 5. Upstream Sky (`sky-1` to `sky-6`)

These are expert courses, 4–6 minutes each. Each has a Wild Tap and a Gear, and they are reached only through the
spouts in §3.3. The palette is prismatic daytime stars, with rivers rising into cloud (the `gen2-type-upstream-sky`
plate).

**sky-1 Lamplight Rapids** (spout from 2-h). Rising rapids ridden on driftwood and Gurgle, using 2-1's pier
rooms. Cobalt blocks add rests. **Wildwater, "Rapids Freeze":** the rapids freeze into ice slides. **Test:** a
current-switch slalom.

**sky-2 Orchard Updraft** (spout from 3-3). Springfruit in wind, opening on 3-1's slope. **Secret (⇢ w6-start
downspout):** the Bypass Valve is under the lowest cloud. **Wildwater, "Fruit Becomes Moons":** fruit orbits her
in low gravity. **Test:** a springfruit chain in a crosswind.

**sky-3 Cloudwell** (spout from 5-2). Glider endurance through 5-2's corridors turned vertical. **Wildwater, "Well
Fills":** a well of cloud water to swim through. **Test:** one glide with three gauge refills.

**sky-4 Prism Rain** (spout from 6-h). 6-2's lit bridges in falling rain, with Rose rails. **Secret (⇢ w8-start
downspout):** a ricochet-revealed valve. **Wildwater, "Rain Splits Light":** each raindrop becomes a coloured
platform. **Test:** a pulse-bridge run in rain.

**sky-5 Lantern Comet** (spout from 7-3). A night chase of 7-1's sign run along a comet tail. **Wildwater, "Tail
Catches":** she rides the comet. **Test:** a forced-speed run.

**sky-6 The Headwater** (from sky-5's normal exit, 6 min). Every power and Gurgle, at the source of all upward
water. **Wildwater, "Source Turns":** the course plays in reverse, downhill. **Test:** the hardest course in the
game. Clearing it switches on **Downstream mode** and the hidden-valves coda after the credits (WORLD-ATLAS
finale beat).

---

## 6. Memory and progress recognition

**World map**
- **Node badges:** a ring for a normal clear. A hollow red valve appears once the node is cleared if it still hides
  a Bypass Valve, and fills when the secret is found. There is a pip for the Gear and a pip for the Pearl. A node
  with everything found turns gold.
- **Path reveals:** pipe segments clack into place one by one and water runs through them before she can walk
  them. `newlyOpened()` already gives the list to animate.
- **Fortresses:** a cleared fortress crumbles on the map, and the rubble stays as its marker. It can still be
  entered for its Gear and Pearl.
- **Rivers:** each castle clear makes that world's map river run downhill again (animated tiles reverse) and warms
  its palette.
- **Chapels:** a pressed chapel's coloured pipes glow on every world map.
- **Gurgle:** when Gurgle waits at a node, he is drawn there, asleep.
- **Repaired bosses:** each world's repaired boss moves into its bonus or shop node with new lines.
- **Teo's clue marks:** Teo's chalk tool-marks stay at the node where each interlude clue was found. Stepping on
  one replays the clue.
- **Plumb Bob:** shows what remains in each node for one walk.

**NPCs.** Lines are keyed to save flags rather than random barks:
- secrets left in this world ("Something in the Rootcellar hums when the lamp is near")
- deaths on a node: at 5 or more, a specific hint for that node's Test beat
- Gurgle with her or waiting at a node
- chapels pressed
- the heroine's name
- arriving by downspout ("You came down the spout? Then you never saw the orchard.")
- 100% of a world

Teo's pipe-phone messages at each start node change with her progress.

**Assist memory.** In forgiving mode, after five lives lost at the same pennant, the pennant offers a Spare
Heart. The offer is remembered per node, so it is not repeated.

**Title screen and file select.**
- The title screen shows the last slot's furthest world vista (the GEN2-ROUND-1 arrival vistas), that slot's
  heroine, and Gurgle if he is with her.
- Freed rivers run down on the title screen.
- After the finale, Teo stands beside her. After the Headwater, the whole title palette goes Downstream.
- Each file-select slot shows the heroine portrait, world and node, percent (of 200 units), exits found x/13,
  Gears x/61, Pearls x/61, four chapel dots, play time and deaths.

**Downstream mode** (after sky-6). Every map river and level waterfall runs the right way. Each course gains a
remixed palette and its enemies switch to their "tamed" variants, which changes how they react to being played
with. The title screen remembers it.

**Save v3** (extends the shipped v2 slot):
- per-node `{clear, secret, gear, pearl}`, keyed by **node id**
- `chapels[]`, `thermos`, `toolRoll[]`, `gurgle: {with, node?}`, `downstream`
- `deathsByNode`, `npcSeen[]`, `assistsOffered[]`

**Migrating from v2:** v2 `done`, `secrets` and `gears` hold Gen-1 codes. They are mapped through each node's
`stage` field, so Gen-1 `2-2` becomes node `2-3`. **Never compare by id across versions,** because Gen-2 ids reuse
Gen-1-looking codes with different meanings. A Gen-1 castle clear also opens the next world's start. Nothing is
wiped.

---

## 7. Implementation order

World 1 is the template Silas plays before Worlds 2–8 are rebuilt (t-021).

1. **t-002 (this doc).**
   - Commit `GEN2-WORLDS.md` and `gen2Worlds.json` to `projects/save-the-plumber/`.
   - Copy the JSON to kind_robots as `utils/arcade/games/savePlumberGen2Worlds.json`, or as a typed TS const.
   - Port `validate_gen2_worlds.py` to a vitest (`verifySavePlumberOverworld.test.ts`) so CI enforces the graph rules.
2. **t-011 follow-up: data-driven overworld.** In `savePlumberOverworld.ts`:
   - Widen `NodeKind` to the nine kinds.
   - Change `unlock.stage` to `unlock.node`. Keep `stage` as the Gen-1 source.
   - Use `warp: 'up' | 'down'` for spouts. `MapDirection` already allows them.
   - Change completion to the 200 units.
   - Add save v3 with the stage-mapped migration.
   - Take node x and y from per-plate clearing coordinates (t-024 note).
3. **t-020: level engine.**
   - sub-rooms with their own camera bounds, vertical shafts and descent framing
   - the pennant
   - the Bypass Valve and valve-wheel carry, reporting `secret`
   - four chapel block tiles (outlined until pressed, solid after), read from the save
   - auto-scroll and on-rails carts
   - a chase pursuer
   - a Hush House door graph with conditional destinations (drip, beam, ferment, mirror, pitch, shadow and painting rules)
   - a Wild Tap → Wildwater → Wild Pearl state machine with one script hook per course, ending on the Pearl or a lost life
   - replay tests: every exit reachable, chapel-free completion, sub-room return positions
4. **t-005: powers.**
   - The Spare Thermos and Tool Roll first, because World 1 uses them.
   - Then the Tidecoat and Gurgle (World 2), Ballast Boots (World 4) and Bellows Glider (World 5).
   - The haunts: teacup haunts and wallpaper shades.
   - Each power ships behind its world, so World 1 is never blocked.
5. **t-021: World 1.** Build the nine nodes and seven beat sheets above. Record first-clear times against the
   3.5–6 minute targets. Wire in the map plate and far-sky plate.
6. **Art and motion (t-024 and t-025, in parallel).**
   - **Props:** Wild Tap, Wild Pearl, Bypass Valve, valve wheel, the four chapel blocks (outlined and solid),
     Thermos and Tool Roll icons, and three new power pickups.
   - **Sheets:** Gurgle (§2), eight mid-bosses (idle, tell, attack, hurt, defeat), and the two haunt families.
   - **Interiors:** a Hush House, a fortress and a chapel interior per world, starting from the generic
     `gen2-type-*` plates.
   - **Heroine:** power pose sets for Pip first (swim, heavy, glide).
7. **t-022:** Worlds 2, 3 and 4, one PR each.
8. **t-023:** Worlds 5 to 8, then Upstream Sky last, because its spouts sit in Worlds 2, 3, 5, 6 and 7.
   Downstream mode ships with sky-6.
