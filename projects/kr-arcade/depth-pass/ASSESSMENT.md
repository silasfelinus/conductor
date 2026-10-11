# Depth Pass — Pipe Pals and Prize Show Panic

**Owner:** `kr-arcade`, milestone m7 (tasks t-023..t-029), code in kind_robots `utils/arcade/games/`.
**Direction:** Silas, 2026-10-11 (verbatim): *"Our kind robot arcade can still use some visual and gameplay
improvements. The first targets are our riffs on Mario bros and smash tv, as those we both favorites of mine
as a child. I want and assessment of levels. Smash tv had an extensive level system, an announcer, prize
screen, various enemies, and a final boss fight. Mario bros lasted multiple varied stages, including ice
levels, coin pickup challenges, and various enemies. We don't need to be 1:1 copies of these games, but we
should be equally complex or more so. For now especially the Mario riff looks just like a smaller formed
version, including to the point of toned down limited turtles. We should have more complex enemies,
variety, etc"*

**The bar:** each game has at least as much level variety, enemy variety and structure as the classic it
riffs on, then goes past it. The guardrails still hold: mechanics only, never the originals' names,
characters, sprites, sounds or level layouts; cartoon bonk/reboot only; no runtime LLM.

The assessment below was taken from the code on kind_robots `main` (6c6c8c8), 2026-10-11:
`pipePals.ts` (1,436 lines) and `prizeShowPanic.ts` (2,162 lines). Both passed the 16-bit render upgrade
(t-021); neither has had a gameplay pass since it first shipped on 2026-10-06/07.

---

## 1. Pipe Pals (Mario Bros. riff)

### What is in the game today

| Area | Today |
| --- | --- |
| Stages | **One** board (`PIPE_LEVELS`: floor + 7 ledges, 2 top pipes, 2 bottom pipes) and **one** backdrop (dusk city) for every phase. Nothing about the room changes, ever. |
| Enemies | **Two.** Shell crawler (one bump flips it) and crab bot (two bumps, second makes it angry and 1.4x faster). |
| Enemy behaviour | Walk, fall, wrap, re-enter from the top pipes. Flipped critters recover "madder" (+30% speed per recovery). Critters pass through each other. No last-critter rush. |
| Hazards | None. Nothing in the room threatens a player who stands still on an empty ledge. |
| KIND block | 3 uses for the **whole game**, never refilled. |
| Bonus round | Every 4th phase: static coins on the same board, 20 s. Same every time. |
| Scoring | 10 per flip, 800 per kick (flat, no chain), 800 per coin, 35% chance a kick drops a coin. |
| Difficulty | Curves plateau fast. Critter count maxes (9) at phase 7, recovery time and release rate at phase 10, crabs (3 max) at phase 10, speed at phase 13. **From phase 13 on, every phase is the same phase.** |
| Players | Solo. Co-op was deferred at ship ("open follow-up"), although the cabinet has seated up to four players since kind_robots#3316. |
| Ending | None. It loops until game over. |
| Scale | 448 x 336 logical world with a 12 x 18 hero and 16 x 9–10 critters. On a phone the actors are tiny, which is most of why it "looks like a smaller formed version". |

### Against the classic

The 1983 game it riffs on runs on one board too, but it keeps changing what happens on that board:

- **Six-plus enemy roles**, each asking for a different answer: the plain walker; the two-hit walker that
  gets faster; the **hopper** that can only be flipped when it lands; the **ice-maker** that walks onto a
  ledge and freezes it (bump it once to clear it, no kick needed); the **bouncing fireball** and the
  **sliding fireball** that punish a player who lingers; **icicles** that grow under ledges and drop.
- **Recovery tiers you can read**: a flipped enemy changes colour each time it rights itself and comes back
  faster, and the **last enemy of a phase sprints** at top speed.
- **Enemies bump into each other** and turn round, so the traffic pattern changes all the time.
- **Kick chains** pay escalating points, so clearing two or three at once is a skill.
- **Frozen floors** in later phases change the movement itself, and the **bonus phases** get harder too
  (slippery floors under the coins).
- The block that flips everything **comes back** at set points.
- **Two players** share the board and can bump each other, which is half the game's personality.

**Verdict:** Pipe Pals has the opening phase of the classic and nothing past it. Two enemies against six-plus,
no hazards, no ice, no chains, no enemy-enemy collisions, one fixed bonus round, a single room and a
difficulty curve that goes flat at phase 13. It is below the bar on every axis Silas named.

### The upgrade: Pipe Pals — a five-district campaign

Keep the single-screen bump-and-kick core. Grow everything around it.

**Structure.** Five **districts** of the plumbing city, each with its own board layout (original layouts:
ledge shapes, gaps, a moving lift or a crumble ledge where it fits), its own backdrop and tiles, its own
music, and a short roster ramp. Each district is **5 phases + 1 bonus round**, then a district card. After
district 5, a finale boss. A clear rolls credits and unlocks a harder Night Shift loop (New Game+). Progress
saves at each district start through `utils/arcade/saves.ts`, like Ghost Trail.

| District | Board idea | New threat | Bonus round twist |
| --- | --- | --- | --- |
| 1. **Rooftop Reservoir** (today's dusk city) | Today's layout, tightened | Shell crawler, crab bot | Static coins (today's round) |
| 2. **Greenhouse Mains** | Vine ledges, one moving lift | **Spring flea** (hops; only flippable while landed) | Coins that drift down from the pipes |
| 3. **Cold Storage** (the ice district) | Icy ledges: low friction, long stops | **Frost bot** (freezes the ledge it walks; one bump clears it, no kick) and **icicles** that grow under ledges and drop | Coins on all-ice floors |
| 4. **Boiler Works** | Steam vents that puff on a beat; a crumble ledge | **Ember spark** (bounces diagonally; bump the ledge under it to snuff it) and **lurker ember** (slides in along a floor if a phase drags; anti-camping) | Coins inside steam bursts, timed |
| 5. **Storm Drain at Midnight** | Dim board; lamps light pools around the pals | Everything, remixed; armoured **grease beetle** (needs a bump, a kick and leaves a slick) | "Test of skill": coins hung under ledges, bump to collect |
| Finale: **The Great Clog** | The whole board | **Clog King**: a big multi-segment clog creature that crawls through the pipes, surfaces on a ledge, and sheds smaller critters. Bump the ledge segments under it to crack its plates; kick the loose plates back into it. Three phases. | — |

**Enemy roster: 2 → 8** (crawler, crab bot, spring flea, frost bot, ember spark, lurker ember, grease beetle,
and the Clog King with its shed critters), plus icicles as a hazard.

**Systems every district uses:**
- Readable **recovery tiers**: calm → cross → furious colours with a speed step each, and a **last-critter
  rush**.
- **Enemy-enemy turnaround** when two walkers meet.
- **Kick chains**: 800 → 1,600 → 2,400 → 3,200 within a short window, shown as a growing floater.
- A coin out of a pipe on every kick (not 35%), so the board keeps feeding the player.
- The KIND block **refills at each district start**; its charge studs stay as today.
- **Two-pal co-op** on the shared board, teal and pink pals from the logo, through the cabinet's `players`
  frames. Pals can bump each other from below (a playful stun, never a kill).
- **Bigger actors**: hero ~24–28 px tall and critters ~18–22 px, either by drawing at double density or
  by moving the logical world down toward 320 x 240 (the Ghost Trail blueprint used a 40–48 px hero on a
  240-high screen). Three-plus animation frames for every walker, a flip/kick squash, and recovery colours.

**Target length:** a first clear of all five districts plus the finale in roughly 25–35 minutes, with the
difficulty coming from new threats and board changes, never from padding.

---

## 2. Prize Show Panic (Smash TV riff)

### What is in the game today

| Area | Today |
| --- | --- |
| Level structure | An endless line of single rooms ("studios"). Each room: a timed random spawn stream (22–36 s) from random doors, then one random exit opens. There is **no map, no route choice, no episodes**. |
| Room variety | Every room is the same square studio with four doors. Floors cycle **three palettes** (boss rooms get a fourth). No room has its own layout, hazards or script. |
| Enemies | **Four**: grabber (homes, comes in groups of 2–4), bouncer (2 hp, ricochets), conga line (4–8 that follow a weaving head), thrower (3 hp, keeps range, throws streamers). Unlocked at rooms 1, 2, 3 and 5. **Nothing new appears after room 5.** |
| Boss | **One** boss, the parade float with the grumpy cake. It slides left and right, fires a 3-way volley every 70 ticks and drops two grabbers every 240. It returns every fourth room with more HP (50 → 200). No phases, no destructible parts, no final boss. |
| Weapons | Confetti cannon plus three timed power-ups: spread, rapid, shield. |
| Prizes | Cash, toaster, car: points and a `haul` counter that is only shown on the game-over banner. **No prize screen.** |
| Announcer | **None.** "The host" exists only as the HUD countdown. Banners carry all the show patter. |
| Aiming | Single stick; hold B to lock the aim. The engine reads only the gamepad's left stick (`axes[0..1]`), so true twin-stick is not possible today. |
| Difficulty | Spawn rate maxes at room 11, grabber speed at room 12; only boss HP keeps rising. The ship probe ended runs around studio 6–7. |
| Players | Solo, although the cabinet seats four. |
| Ending | None. It loops until game over. |

### Against the classic

The 1990 game it riffs on is built as a **TV season**:

- **Three arenas**, each a **grid of rooms on a map** shown between rooms. The player picks a route by
  choosing which exit to take; some rooms are prize rooms, some are traps, the boss room is at the end.
- **Rooms are authored**: particular enemy mixes, mines on the floor, rooms of wall turrets and laser
  sweeps, and the doors throw enemies in on a script, not at random.
- **A large enemy roster** that asks for different answers: club-swinging swarms, rolling orbs, tanks that
  shoot back, mines and mine-layers, exploding shrapnel bombs, snakes, wall-mounted guns, mini-bosses.
- **A boss per arena, each a different fight**: a giant that loses body parts and changes attack as it
  breaks, a giant face/wall with pop-out guns, a segmented serpent, then a **final showdown** that ends
  the season.
- **An announcer** who talks over everything, and an **on-screen host**.
- **A prize screen** that tallies everything won at the end of each arena, and **keys** that unlock a secret
  final area.
- **A wide arsenal**: spread, rapid, grenades, rockets, spinning orbiters, force field, speed-up.
- **Two players** in the same arena, with true twin sticks.

**Verdict:** Prize Show Panic has the room loop, the countdown, prize drops and a boss, but it is one
studio repeated with three palettes, four enemies, one boss on repeat, no map, no host, no prize screen, no
ending. It is short of the classic on every structural axis Silas named.

### The upgrade: Prize Show Panic — a three-episode season

**Structure.** A **season of three episodes**, each a **map of 10–12 rooms** on a grid. Between rooms the map
screen shows where you have been, what each neighbouring door leads to (swarm, prize vault, trap, boss),
and the route you choose. Each episode ends in its own boss; episode 3 ends in the **Grand Finale**. Collect
**golden tickets** across the season; enough of them opens the secret **Grand Prize Vault** before the
finale (the true ending). A clear rolls credits and unlocks a Rerun season (New Game+). Progress saves at
each episode start.

**Rooms are data, not dice.** Each room is a script: which doors open when, which kinds and how many, floor
props, and a room type:

- **Swarm** (today's room, scripted), **Mine set** (whoopee-cushion and banana-peel mines on the floor),
  **Light rig** (spotlight beams sweep the floor on a beat), **Camera wall** (turret cameras along one wall),
  **Speed round** (short timer, double prize drops), **Prize vault** (no enemies, prizes on pedestals,
  closes fast), **Ambush** (all four doors at once), **Conga ballroom** (lines only, long and fast).

**Enemy roster: 4 → 10:**

| Crasher | Behaviour | Answer |
| --- | --- | --- |
| Grabber, bouncer, conga line, thrower | As today, scripted | As today |
| **Popper** | A balloon bot that bursts into a ring of streamer shards when confettied | Pop it at range |
| **Sweeper tank** | Slow, armoured front, fires a bubble burst | Flank it |
| **Stagehand** | Lays floor mines as it walks | Catch it early |
| **Spotlight drone** | Orbits, then locks a beam onto you for a charge | Break line or out-pace |
| **Mascot** | A big costumed mini-boss with a charge and a belly-bounce | Dodge the charge, hit its back |
| **Camera crane** | Wall turret (Camera wall rooms) | Out-angle it |

**Arsenal: 3 → 7.** Keep spread, rapid and shield; add **party poppers** (lobbed area blast), **bubble
rockets** (slow, heavy, pierce), **streamer orbiters** (two spinning ribbons that guard you) and **roller
skates** (speed). Short durations, stacking timers, all shown in the HUD.

**Bosses: 1 → 4, every one a different fight:**

1. **Episode 1 — The Big Wobble.** A giant inflatable mascot. Each arm and leg is a separate target;
   popping one changes its attack (arm gone: no slam; leg gone: it hops). Three phases.
2. **Episode 2 — The Jumbotron.** A wall of video screens with a face. Screens flip open to reveal
   turrets; the face moves screen to screen; crack the screens to corner it.
3. **Episode 3 — The Conga Dragon.** A long segmented parade dragon that weaves the studio. Segments drop
   off as you confetti them and each one becomes a small dancer; the head speeds up as it shortens.
4. **Grand Finale — The Host's Prize Machine.** The host rides a giant prize wheel machine that spins up
   different attack sets (the wheel shows the next one), with a last phase where the host jumps out.

The parade float stays as an episode-1 mid-boss.

**The show itself:**
- **The host and announcer.** A host robot portrait cuts in at the edge of the screen with short original
  lines in a speech panel: room start, a big prize, a near miss, low time, a boss intro, a death, a clear.
  A small bleep-speak voice (WebAudio pitch patterns, no speech synthesis needed). Lines are original
  writing; no catchphrases from the source.
- **The prize screen.** After each episode, a tally screen: each prize kind counts up with its sprite and a
  tick sound, then the totals, golden tickets and an episode bonus. The game-over screen lists the season
  haul the same way.
- **The studio.** An APPLAUSE sign that lights on kills, an audience band along the bottom wall that cheers
  on big moments, camera-flash juice on boss hits.
- **True twin-stick.** Extend the engine input with an optional aim vector (the way `plunger` is optional
  on `InputFrame`): the gamepad's right stick, a second on-screen stick on touch, and a split keyboard
  (move on WASD, aim on the arrows). Hold-B aim lock stays for single-stick players.
- **Two-contestant co-op** through the cabinet's `players` frames.

**Target length:** a first clear of the season in roughly 30–45 minutes.

---

## 3. Order of work

Both are `large` games under the factory rules: ship them in playable slices, each one merged, each one
verified with `test:arcade-engine`, eslint/prettier and vue-tsc plus a deterministic campaign test, and
Pixel/HD screenshots.

- **Pipe Pals:** t-023 (scale, systems and the first new enemies), then t-024 (the five districts, ice and
  bonus variety), then t-025 (Clog King, campaign end, save/resume, co-op).
- **Prize Show Panic:** t-026 (the season map and authored rooms), then t-027 (roster, arsenal, twin-stick),
  then t-028 (host, announcer, prize screen), then t-029 (four bosses, the vault, ending, save/resume,
  co-op).

Pipe Pals goes first: Silas called it out as the weaker of the two.
