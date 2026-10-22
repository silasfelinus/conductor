# Route Map, Medals, Palace Hangar and Memory (Generation 2)

**Rainbow Bullet Hell Space Princess** · conductor t-026 · 2026-10-22 PT · design contract for t-027 (memory) and t-028 (alternate stages).
Shared bar: [GEN2-STANDARD.md](../kr-arcade/GEN2-STANDARD.md). Data: [`rainbowRoute.json`](rainbowRoute.json) (nodes, paths, medals; validated).
Pacing and scenes: [ACT-STRUCTURE.md](ACT-STRUCTURE.md). Flags and endings: [COMMS-AND-ENDINGS-BIBLE.md](COMMS-AND-ENDINGS-BIBLE.md), [WORLD-BIBLE.md](WORLD-BIBLE.md).

**Benchmark, in spirit only:** a branching shooter route map where branches open from things done inside a stage, a medal per stage, and progress that persists. Every name, place, stage and line here is original.

## 0. Three rules this design keeps

1. **Detours, never skips.** Each alternate stage is a detour between two Acts and rejoins at the next one. Every route flies all eight Acts, so the 27 mandatory scenes, the Act VI Lilt reveal and the six rescue flags stay intact. This follows the World Bible rule that "branch exits reconnect". The validator checks it.
2. **The fork is flown, not picked from a menu.** ACT-STRUCTURE bans stage-select screens between Acts. When a branch opens, the Act's boss-aftermath bridge splits into two lit currents and the crew flies into one, using the same rule as the shipped Trench and Wreckyard forks (`splitY`). In co-op the lane with the most pilots wins and a tie goes to the lead pilot (`finaleChoiceFor`). Online, the host commits the choice. While the crew is in the transit corridor, a 3-second route-map pan plays as an overlay. It can be skipped and controls stay live. The full route screen appears only at title, continue, Sortie and run end.
3. **In-run flags make the story, slot memory makes the recognition.** Rescue flags belong to the run and decide endings. The slot remembers who was ever rescued, and uses that for cameos, map icons and lines. Memory never sets a story flag, so a friend from last run cannot count twice.

## 1. Route map structure

```
                 X1 Kelp Nebula            X2 Coral Comet         X3 Sunken Lighthouse   X4 Mirror Shoal
                 /  (rescuedNemi)  \       / (rescuedCourier) \   / (stoppedRelay) \     / (noContinue | rescuedNavigator) \
start ─ S01 ─ S02 ───────────────── S03 ─ S04 ─────────────── S05 ─ S06 ──────────── S07 ─────────────────────────── S08 ─ S09
```

| Node | Kind | Opened by | Branch condition, and where it already lives in code |
| --- | --- | --- | --- |
| S01–S08 | act (Acts I–VIII; checkpoint `act` 1–8) | clearing the previous node | none |
| **X1 Kelp Nebula Bypass** | alt, II → III | S02 **`rescuedNemi`**: a **rescued captive** | `rescuedNemi = true` in Act II (rainbowPrincessPreview). Nemi translates the kelp colony's current. |
| **X2 Coral Comet Trail** | alt, IV → V | S04 **`rescuedCourier`**: an **escort saved** | `rescuedCourier = true` when the courier pod reaches the end of the rails. The courier's route data (A04.TURN clue) charts the comet tail. |
| **X3 Sunken Lighthouse Ring** | alt, VI → VII | S06 **`stoppedRelay`**: the **generator destroyed** | `palaceFlags().stoppedRelay`: relay route, settled, every relay pylon down (`CROWN_REEF_PYLONS`). With the relay silenced, the drowned lighthouses can be seen. |
| **X4 Mirror Shoal** | alt, VII → VIII | S07 **`noContinue`** *or* **`rescuedNavigator`** | `actContinues === 0` at the Act VII clear (silver or gold rank), or `rescuedNavigator = true`. There are two keys: a clean flight (skill) or the Navigator who knows the shoal (kindness). |
| S09 | finale (`act` 9) | S08 clear | none |

- There are 5 named conditions, 2^5 = 32 combinations and 16 distinct routes (2^4 detour patterns). Every route ends at S09.
- Conditions are evaluated at the source Act's AFTER bridge. That is the only point where all of them, including `noContinue`, are known.
- A branch is **found** the first time its condition is met in a slot, whether or not the crew flies it. A found branch stays drawn on the map, and a Sortie can enter it from then on.
- **Revisit freely (Sortie).** From the route screen, any cleared node, and any found alt, can be flown alone. A Sortie counts toward medals, rank and best score. It never changes the campaign run in progress. The run's flags are seeded from the slot's best-known values, so scenes still resolve.
- **Map art.** The Krea 2 `rb2-route-map` (art_image_id 251317) is the backdrop. It paints nine rings and two side-trails, but there are 13 nodes, so rings, trails, medal pips and reveal animation are drawn in code over the painting. This matches the Plumber map, which draws nodes over the scenery.

## 2. Medals

There are two medal layers, and both are kept per node in the slot as the best ever:

- **Rank** (shipped as `rainbowMedal(hits, continues)`): gold for no hits, silver for no continues, bronze for a clear. This is unchanged.
- **Stage medal** (new): one authored goal per node, built from counters the game already tracks.

| Node | Medal | Goal | Existing counter |
| --- | --- | --- | --- |
| S01 | Pearl Keeper | Rescue the station and defeat the Urchin guardian before it escapes | `rescuedStation`, `guardians[1]` |
| S02 | Bell Ringer | Rescue Nemi and defeat the Lantern guardian | `rescuedNemi`, `guardians[2]` |
| X1 | Choir Keeper | Free all five Coral Choir pods and defeat the Kelp Warden | new (t-028) |
| S03 | Vault Diver | Settle the vault route without losing a life | `trenchRoute`, `routeSettled`, lives |
| S04 | Clean Rails | Bring the courier home and defeat the Courier guardian | `rescuedCourier`, `guardians[4]` |
| X2 | Full Wing | Bring all four cadet trainers out of the comet tail | new (t-028) |
| S05 | All Hands | Free the depot with all 7 pods reached | `podsSaved === WRECK_FORK.pods` |
| S06 | Lights Out | Silence the relay and defeat the Bulwark guardian | `stoppedRelay`, `guardians[6]` |
| X3 | Every Lamp | Relight all six lighthouse lamps | new (t-028) |
| S07 | True Reflection | Rescue the Navigator and defeat the Mirror guardian | `rescuedNavigator`, `guardians[7]` |
| X4 | Still Water | Clear Mirror Shoal without a hit | hits |
| S08 | Every Collar | Free every captive and defeat the Herald guardian | `captivesFreed === PALACE_CAPTIVES`, `guardians[8]` |
| S09 | Open Sky | Clear the Eclipse Crown with no continue and every seated pilot flying | continues, lives |

Every goal can be met with the default loadout, as the World Bible requires. A medal earned in co-op counts for the slot that hosts the run.

## 3. The Palace Hangar

Backdrop: Krea 2 `rb2-hangar` (art_image_id 251318).

**Crests** = stage medals + gold ranks, at most 13 + 13 = **26**. A crest is never spent. Hangar fittings **unlock** at crest thresholds and stay unlocked, so the player never has to grind or regret a purchase. Each seat equips **at most two** fittings per run, chosen at pilot select.

| Crests | Fitting | Effect, built on the shipped rule it bends | Bound |
| --- | --- | --- | --- |
| 2 | Petal Start | Launch at power 2 (`ship.power` starts at 1) | Power cap stays 3 |
| 4 | Long Cache | U12 Recovery Cache waits 6 s instead of 4 s | One dropped level, own pilot only |
| 6 | Second Wind | After a continue, ships relaunch at +1 power | Cap 3; continue rules otherwise unchanged |
| 9 | Quick Roll | Evade cooldown 84 → 72 frames (`RAINBOW_EVADE`) | Evade length unchanged |
| 12 | Quick Bloom | Special cooldown 360 → 320 frames (`RAINBOW_SPECIAL`) | Special power unchanged |
| 15 | Charge Seed | Each Act or Sortie starts with the charge meter at 25% | Bank limit unchanged |
| 18 | Lens Glint | U10 Mirror Lens outlines a boss's weak point for 60 frames at each phase change | Readability only; no damage |
| 22 | Friend Flyby | A friend rescued in an earlier run flies past once per Act and drops one power pickup | One pickup per Act |

Cosmetics are free and never fitted. Each stage medal unlocks a hull paint. Each ending seen adds a trophy to the hangar shelf. Rescued friends (Nemi, the courier, the Navigator, the Choir, the cadets) visit the hangar.

**Fairness walls, enforced in code and tests.** No fitting ever changes lives, shield layers (3), the central collision core, shot damage, boss HP, bullet speed or telegraph frames. **At Ace difficulty, combat fittings are off and only cosmetics apply**, so `ace-of-eclipse` and Ace scores stay unassisted. Recorded scores (`rainbowRecordedScore`) carry a `fitted` bit, and the leaderboard marks fitted runs with a petal.

## 4. Memory and progress recognition

The comms resolver (`selectDialogueEvent`) gains a **memory** tier, checked in this order: specific combination → **memory variant** → pilot → Lilt fallback. Its keys are `node + beat + partyMask + flags + via + memory`. Memory never removes a mandatory scene. A return visit only selects the scene's shorter **essential** variant, which keeps the same narrative purpose.

| Trigger (slot memory) | Where it plays | Sample (original) |
| --- | --- | --- |
| First visit (`best[node].visits === 0`) | OPEN, full | Shipped lines |
| Return visit | OPEN, essential | Lilt: "Pinkwake again. The buoys are still blinking at you." |
| Branch found this run | Source Act's AFTER plus the fork lanes | Lilt: "A current is opening through the kelp. Nemi says it is safe. Fly high to follow it." |
| Branch found earlier, condition missed this run | Source Act's TURN, one line | Lilt: "Last time Nemi showed us a way through. She is in the full corridor again." |
| Friend rescued in an earlier run (`friends`) | Their home Act's OPEN, plus a cameo icon at their map node | Nemi (as a recording): "I know this corridor, princesses. The full one." |
| Every branch found | Route screen | Lilt: "Four currents charted. Azure, I believe that is a complete map." |
| Ending already seen | Finale OPEN | Lilt: "We have flown this far before. I remember the choice. I will still not make it for you." |

**Title and route screen state.** The title sky moves from pink dusk toward palace eclipse as the furthest node advances, and shows dawn after the first ending. Each slot card on the file select shows the pilot portrait, the furthest node, stage medals x/13, golds x/13, branches x/4, friends, endings x/3, completion percent and play time. On the map:

- cleared nodes glow as lit rings;
- freed bosses swim at their node;
- found but unflown branches show as dashed trails;
- unfound branches show only as the painting's faint side-trails;
- medal pips sit under each ring;
- a newly opened trail draws itself on the first route screen after it is found.

**Completion percent** counts 46 items: 13 nodes cleared, 13 stage medals, 13 golds, 4 branches found and 3 endings.

## 5. Which branches change which scenes

`via` is the node the crew arrived from. Rows list only the scenes that change. Existing flag variants (station, Nemi, courier, depot, relay, Navigator, captives) stay as shipped.

| Act | OPEN | TURN | AFTER |
| --- | --- | --- | --- |
| I | First vs return | none | none |
| II | Return; Nemi-from-last-run cameo | Missed-branch hint (slot found X1, Nemi not yet rescued) | **X1 found**: Lilt marks the kelp current and the fork lanes light |
| III | **via X1**: arrive out of the kelp with Nemi and the Choir instead of jelly tendrils | **`freedChoir`**: the Choir vouches that the vault holds people's belongings, which changes the vault-vs-safe debate | none |
| IV | none | none | **X2 found**: the courier hands over the comet-tail route |
| V | **via X2**: the wreckyard seen from above the comet tail, with cadets in formation | **`freedChoir`** (Choir kin in the depot) and **`cadetsHome`** (Solenne's line) join the depot-vs-armory argument | none |
| VI | none | The mandatory Lilt reveal is unchanged; a return visit uses its essential variant | **X3 found**: with the relay dark, the drowned lighthouses show |
| VII | **via X3**: the lighthouse beams lead in; Lilt is steadier | **`liltMemoryRecovered`**: Lilt recognises the Navigator's mirrored signal (the fuller truth) | **X4 found**: a clean flight, or the Navigator's chart, opens the shoal |
| VIII | **via X4**: across the shoal, carrying the Crown's echo | **`cadetsHome`**: the cadets escort the captives | **`crownEcho`**: the freed Leviathan answers the Crown's first broadcast |
| Finale | Ending-seen memory line | **`liltMemoryRecovered` / `crownEcho`**: Lilt's pre-choice line variant | Route stinger (section 6) |

Alt stages carry their own optional `X1.OPEN / X1.TURN / X1.AFTER` through `X4.*`. These 12 scenes are optional and are not part of the 27 mandatory slots. Each is resolved against the 15 party masks with the same fallback chain.

## 6. Routes and endings

Every route reaches S09, and all three final choices (`restore | evacuate | sever`) stay available on every route. The composed ending keeps its four shipped layers: the world consequence of the choice, Lilt's resolution, the party epilogue, and credits from the six rescue flags. Routes add a fifth layer, a **route stinger**, and extra credit lines:

| Choice | Full stinger needs | Stinger | Detours |
| --- | --- | --- | --- |
| Restore | `liltMemoryRecovered` + `crownEcho` | **First Rule**: the Crown speaks its original directive, "protect, and ask", in its own voice | X3 + X4 |
| Evacuate | `freedChoir` + `cadetsHome` | **Whole Fleet**: the Choir and the cadets fly the evacuation escort | X1 + X2 |
| Sever | `stoppedRelay` + `liltMemoryRecovered` | **Kept Memory**: the shards go dark, but Lilt keeps what they carried | X3 (S06 relay) |
| Any | All four alt flags + all six rescues | **Open Sea**: a credits coda, the dawn title screen and an "Open Sea" hull paint | All four |

Without its keys, each choice plays its shipped ending as written. `finaleRescues` stays six-flag based. The alt flags (`freedChoir`, `cadetsHome`, `liltMemoryRecovered`, which already exists in the NarrativeState schema, and `crownEcho`) add credit lines but are not counted as rescues.

## 7. Alternate stages (for t-028)

Each alternate stage targets 5–7 minutes, has one guardian and no full boss, and reuses `recutTimeline` / `reinforcements`. Fairness rules match the Acts.

| Node | Mechanic (new) | Families remixed | Guardian (new `RainbowGuardianKind`) | Friend flag |
| --- | --- | --- | --- | --- |
| X1 Kelp Nebula Bypass | Swaying kelp fronds are moving cover for both sides; a gentle current drift is telegraphed by particle flow | E05, E06, E08; E09 previewed in the dark | **Kelp Warden** (`kelpwarden`): comb-sweep harvester with a frond-sweep telegraph | `freedChoir` (5 pods) |
| X2 Coral Comet Trail | Speed bursts; coral asteroids split into outlined fragments | E13, E15; E16 previewed | **Comet Herder** (`herder`): a lance-nosed tug that shoves asteroids into lanes | `cadetsHome` (4 trainers) |
| X3 Sunken Lighthouse Ring | Sweeping beams; six lamps to relight by shooting. Darkness dims only the backdrop, never bullets | E19, E21, E11 (false lights) | **Dark-Lamp Keeper** (`lampkeeper`): a cuttlefish lamp-ship | `liltMemoryRecovered` |
| X4 Mirror Shoal | Every craft has a reflection lane below the waterline. Solid shots are outlined and reflections are ghosts (the shipped `ghost` pellet) | E22, E23, E12 | **Shoal Koi** (`shoalkoi`): twin mirrored koi-fan craft | `crownEcho` |

Backdrops are the Krea 2 keepers 251319 / 251321 / 251320 / 251322. Each is one flattened plate, so a follow-up art round must render separate sky/far/mid/near plates (GEN2-STANDARD §6.4) before an alt counts as finished.

## 8. Save slots and migration

The cabinet keeps one JSON per slug, capped at `MAX_SAVE_BYTES = 8192`. The design worst case, with three full slots, every node, every friend and every ending, measures **5,857 bytes**. Per-node records are stored as tuples to keep that headroom, and a size test must pin it.

```ts
type RouteNodeId = 'S01'|'S02'|'S03'|'S04'|'S05'|'S06'|'S07'|'S08'|'S09'|'X1'|'X2'|'X3'|'X4'
type RainbowFile = { v: 2; active: 0 | 1 | 2; slots: (RainbowSlot | null)[] }   // 3 slots
type RainbowSlot = {
  pilot: number; difficulty: ArcadeDifficulty
  run: RainbowRun | null            // the flight in progress, saved at each node start (frame 0), as today
  best: Partial<Record<RouteNodeId, [rank: 0|1|2|3, medal: 0|1, score: number, visits: number]>>
  found: string[]                   // branch keys 'S02>X1' (at most 4)
  friends: string[]                 // ever rescued: station nemi salvage courier depot relay navigator choir cadets liltMemory crownEcho
  endings: FinaleChoice[]; stingers: string[]
  heard: Partial<Record<RouteNodeId, number>>   // bitmask OPEN=1 TURN=2 AFTER=4: scene gallery, first vs return
  fit: [string?, string?][]         // per seat (0-3), at most 2 fittings; unlocks derive from crests, never stored
  stats: [runs: number, clears: number, deaths: number, seconds: number]
}
type RainbowRun = Omit<RainbowSave, 'v'> & {
  node: RouteNodeId                 // the node this run resumes at (alt ids allowed)
  route: RouteNodeId[]              // nodes flown this run, in order
  partyMask: number
  // checkpoint gains: freedChoir, cadetsHome, liltMemoryRecovered, crownEcho (default false)
}
```

**Migration, v1 to v2.** The current `RainbowSave` v1 is a single Act start. It is read with the shipped `readRainbowSave` and moved into slot 1. Nothing is wiped.

- **Run.** v1 becomes `run`, with `node = S0{act}` and `route = S01..S0{act-1}`. v1 had no alts, so every earlier leg counts as direct.
- **Best and heard.** `best` is set from v1 `medals` for the earlier Acts: the rank only, with `medal: 0` and `visits: 1`. `heard` marks all three scenes for every earlier Act.
- **Friends and branches.** `friends` comes from the v1 checkpoint flags. **`found` is filled retroactively**: `rescuedNemi` with act > 2 finds `S02>X1`, and `rescuedCourier` with act > 4 finds `S04>X2`. A returning player therefore sees "A current you opened last time" on the first route screen.
- **Validation.** Untrusted input is checked field by field, as `readPlumberFile` does. Garbage becomes an empty file.
- **Tests.** A v1 fixture yields the expected v2 file, a v2 file round-trips, and the worst-case file stays under 8,192 bytes.

## 9. Implementation order

**t-027: memory and route screen** (one PR per step; each step is reversible and tested):

1. **Generalize the overworld.** Extract `utils/arcade/routeGraph.ts` from `savePlumberOverworld.ts`: nodes, paths with `unlock: {node, condition} | null`, `pathOpen`, `openPaths`, `newlyOpened`, `nodeReachable` and completion. The Plumber module maps `exit: 'normal' | 'secret'` onto conditions, and `verifySavePlumberOverworld.test.ts` must stay green. kr-arcade/t-160 (Ghost Trail) reuses the same module.
2. **Route data.** Add `rainbowRoute.ts`, which loads `rainbowRoute.json` and evaluates conditions against run state. Port `validate_route.py` into a vitest that checks reachability, alt gating, the finale on every route and that no Act is skipped.
3. **Save file.** Add `rainbowSave.ts` with the v2 file, the v1 migration and the size test. The cabinet reads and writes the active slot, and the existing continue flow resumes `run`.
4. **Medals and memory.** Track stage medals and the best rank per node, the `found` keys, `friends` and `heard`. Add the memory tier to the comms resolver, starting with OPEN first vs return and the branch-found AFTER lines.
5. **Screens.** Build the file select (3 slots), then the route screen: art 251317, lit and dashed trails, reveal animation, pips and Sortie entry. The in-flight overlay pan comes last.
6. **Hangar.** Hangar screen (art 251318), crest thresholds, two fittings per seat, Ace cosmetics-only, and the `fitted` score bit.
7. **Branch lanes.** Before t-028 lands, a found branch shows on the map as **"charted, sealed"** and the run flies direct. That keeps every PR shippable.

**t-028: alternate stages**, one PR each in campaign order (X1 Kelp, X2 Comet, X3 Lighthouse, X4 Mirror). Each PR contains:

- a `rainbow<Name>.ts` module shaped like the Act modules (sections, waves, guardian section, the three `X*.` scenes, friend flag, stage medal);
- the source Act's AFTER fork lane;
- a checkpoint refactor so `RainbowCheckpoint` carries `node`;
- `resumeTick`'s positional per-Act start arguments replaced by a node-keyed map;
- a deterministic replay test and a 1–4 player soak;
- a recorded first-clear time.

Silas plays each alt on `main` and gives the final verdict.
