# Depth Pass — Every Other Cabinet

**Owner:** `kr-arcade`, milestone m8 (tasks t-035..t-145), code in kind_robots `utils/arcade/games/`.
**Direction:** Silas, 2026-10-11 (verbatim): *"After you do those two and the roadmaps are updated, I need an
assessment done of the other arcade games. I want the same level of quality improvements, they should not just be
thin veneers of the old games. But newer, better, even more awesome"*

"Those two" are Pipe Pals and Prize Show Panic; their assessment and upgrade plan is
[`ASSESSMENT.md`](ASSESSMENT.md), and it sets the bar this document holds every other cabinet to.

**The bar:**
- Each cabinet has at least the level variety, enemy variety and structure of the classic it riffs on, then goes
  past it with a signature twist of its own.
- No cabinet stays a "thin veneer". Where today's rules map one-for-one onto the original's (Battery Maze's chasers,
  Butterfly Blaster's rule set), the upgrade re-riffs them into something of our own.
- The guardrails still hold:
  - riff on mechanics only: never the originals' names, characters, sprites, sounds or level layouts;
  - cartoon bonk, cheer or reboot only;
  - no runtime LLM and no real money;
  - a deterministic 60 Hz seeded simulation, with gameplay on the game's `rng` and cosmetics on `backdropRng`;
  - the attract demo scores 0.

**How this was taken:**
- The assessment was taken from kind_robots `main` on 2026-10-11, after the 16-bit glow-up (m6).
- Each cabinet's file was read in full with its registry entry, and every `levelCurve` was traced to the level where
  it stops rising.
- Two attract-demo screenshots were taken per cabinet, one at a few seconds in and one about four minutes in.

## The short version

**Every one of the 25 is solo-or-thin, endless and flat:**
- **No ending or save:** none has a boss, an ending or a save.
- **Players:** only Kindness Gauntlet, Station Sweep and Seed Burst seat more than one.
- **Flat difficulty:** every one stops getting harder between level 7 and level 15.
- **No visible progress:** in every pair of screenshots, minute four looks like second five.

Pipe Pals had the same shape before its depth pass and now has eight districts, a secret district, 15 critters,
three bosses, a Workshop, medals, co-op and Versus. Each plan below is pitched at that scale.

**Two findings to fix early:**
- **Copies to re-riff:** Battery Maze reuses the classic's four chase rules exactly, and Butterfly Blaster maps almost
  one-for-one onto its 1979 source, down to the 10,000-point extra life.
- **Burrow Buddy's blurb:** it promises beetles "from the second garden", but they first arrive in garden 3 (its
  slice 1 fixes it).

**Order of work:**
- **Tier 1:** Silas's original favourites (2026-10-06: Joust, Gauntlet II, Robotron, the sink bubbles game, Pac-Man).
- **Tier 2:** the near-copies and the thinnest cabinets.
- **Tier 3:** the cabinets that already have the most.

Every cabinet's slice 1 is `ready`, and each later slice waits on the one before it.

| # | Cabinet | Classic | Lines | Flat from | The upgrade | Tier | Tasks |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [Rescue Rally](#1-rescue-rally-robotron-riff) | Robotron | 1,552 | wave 12 | Citywide Reboot | 1 | t-035..t-038 |
| 2 | [Battery Maze](#2-battery-maze-pac-man-riff) | Pac-Man | 1,877 | level 9 | The Charging Network | 1 | t-039..t-042 |
| 3 | [Sink Suds](#3-sink-suds-bubbles-riff) | Bubbles | 1,030 | sink 12 | The Big House Wash | 1 | t-043..t-046 |
| 4 | [Butterfly Joust](#4-butterfly-joust-joust-riff) | Joust | 1,499 | wave 11 | The Four Gardens Tourney | 1 | t-047..t-050 |
| 5 | [Kindness Gauntlet](#5-kindness-gauntlet-gauntlet-ii-riff) | Gauntlet II | 2,731 | floor 13 | The Deep Archive | 1 | t-051..t-054 |
| 6 | [Butterfly Blaster](#6-butterfly-blaster-asteroids-riff) | Asteroids | 1,572 | wave 13 | The Rainy Season | 2 | t-055..t-058 |
| 7 | [Bumper Bubbles](#7-bumper-bubbles-bubble-bobble-riff) | Bubble Bobble | 1,330 | round 14 | The Hundred Floors of Fizzwick Tower | 2 | t-059..t-063 |
| 8 | [Cable Crawler](#8-cable-crawler-nibbler-riff) | Nibbler | 1,279 | board 11 | The Mainframe Odyssey | 2 | t-064..t-068 |
| 9 | [Seed Lander](#9-seed-lander-lunar-lander-riff) | Lunar Lander | 1,143 | hill 8 | The Great Replanting | 2 | t-069..t-073 |
| 10 | [Ribbon Riders](#10-ribbon-riders-tron-light-cycles-riff) | Tron light cycles | 1,108 | round 9 | The Lantern Festival Circuit | 2 | t-074..t-077 |
| 11 | [Brick Bloom](#11-brick-bloom-breakout--arkanoid-riff) | Breakout / Arkanoid | 1,449 | stage 12 | The Glasshouse Grand Tour | 2 | t-078..t-082 |
| 12 | [Pixel Hop](#12-pixel-hop-qbert-riff) | Q*bert | 1,428 | round 12 | The Painted Planets | 2 | t-083..t-087 |
| 13 | [Glitch Garden](#13-glitch-garden-centipede-riff) | Centipede | 1,190 | wave 7 | The Four Seasons of the Glitch | 2 | t-088..t-092 |
| 14 | [Lantern Swarm](#14-lantern-swarm-galaga-riff) | Galaga | 1,400 | stage 12 | The Long Night Festival | 2 | t-093..t-097 |
| 15 | [Rover Ramble](#15-rover-ramble-moon-patrol-riff) | Moon Patrol | 1,405 | section 13 | The Five Moons Rally | 2 | t-098..t-101 |
| 16 | [Hedgehog Crossing](#16-hedgehog-crossing-frogger-riff) | Frogger | 1,704 | level 11 | The Long Way Home | 3 | t-102..t-105 |
| 17 | [Burrow Buddy](#17-burrow-buddy-dig-dug-riff) | Dig Dug | 2,099 | garden 13 | The Year Under the Garden | 3 | t-106..t-109 |
| 18 | [Repair Rampage](#18-repair-rampage-rampage-riff) | Rampage | 1,638 | city 11 | The Big Fix Tour | 3 | t-110..t-113 |
| 19 | [Rain Catcher](#19-rain-catcher-missile-command-riff) | Missile Command | 1,444 | wave 15 | Gardens of the World | 3 | t-114..t-117 |
| 20 | [Petal Post](#20-petal-post-paperboy-riff) | Paperboy | 1,640 | day 10 | A Season in Blossom Valley | 3 | t-118..t-121 |
| 21 | [Cocoa Counter](#21-cocoa-counter-tapper-riff) | Tapper | 1,407 | round 12 | The Cozy Cafe Tour | 3 | t-122..t-126 |
| 22 | [Quilt Quest](#22-quilt-quest-qix-riff) | Qix | 1,462 | quilt 9 | The Heirloom Quilt | 3 | t-127..t-131 |
| 23 | [Gloom Invaders](#23-gloom-invaders-space-invaders-riff) | Space Invaders | 1,451 | wave 12 | A Year of Weather | 3 | t-132..t-135 |
| 24 | [Seed Burst](#24-seed-burst-bomberman-riff) | Bomberman | 1,712 | round 12 | The Four Seasons Allotment | 3 | t-136..t-140 |
| 25 | [Station Sweep](#25-station-sweep-xenophobe-riff) | Xenophobe | 2,591 | station 7 | The Orbit Line | 3 | t-141..t-145 |

## Rules for every slice

These apply to every m8 task. Each task's note points here and to its game's `#### Slices`.

- **Read the game's section first.** It holds the "today" inventory, the upgrade spec and the slice scope.
- **Riff on mechanics only.**
  - Use original names, layouts, lines, sprites and music.
  - Cartoon bonk, cheer or reboot only.
  - No real money and no runtime LLM.
- **Determinism.**
  - Keep the 60 Hz seeded simulation: gameplay on the game's `rng`, cosmetics on `backdropRng`.
  - The attract demo still scores 0, and the score stays under the registry's `maxPlausibleScore`.
- **Content is data** (worlds, stages, waves, rooms), not branches in the update loop. Long campaigns save through
  `utils/arcade/saves.ts`, as Pipe Pals and Ghost Trail do.
- **Co-op** goes through the cabinet `players` frames. Set the registry `maxPlayers` and pass the engine co-op test.
- **Twin-stick aim** (`InputFrame.aim`, `twinStick` in the registry) is available to solo cabinets that want it, as
  Prize Show Panic uses it.
- **Verify every slice** with:
  - `test:arcade-engine` plus a deterministic test for the slice's rules;
  - eslint/prettier and `vue-tsc --noEmit`;
  - Chromium screenshots on the PR;
  - a pilot probe that shows runs still end.

  Update the attract pilot for new mechanics.
- **The last slice** of each cabinet updates the registry blurb, the howTo lines and its `games.yaml` entry.

---

## 1. Rescue Rally (Robotron riff)


### What is in the game today

| Area | Today |
| --- | --- |
| Structure | Endless waves in **one** bevelled arena. All foes are placed at the start of the wave; it ends when every hostile foe is gone. Three floor tints cycle. |
| Foes | **Five.** The drone shuffles toward you (1 hp, 100). The spawner drifts and births seekers (3 hp, 500). The seeker homes in (1 hp, 150). The tank is slow, takes 5 hp and is only nudged back by the beam (300). The puddle is a static hazard (1 hp, 25). |
| Threat | **Nothing shoots at the player.** Every foe is a touch hazard. |
| Rescuees | 4–9 per wave (people, cats, dogs, little bots) who wander at random. **Nothing threatens them**: the foes ignore them, so rescuing is only collecting. The multiplier runs 1,000 to 5,000 and resets on a death. |
| Aim | Move to aim, hold B to strafe (lock the aim), A to fire. There is no independent aim. |
| Wave design | None. Every wave is the same random mix from the curves; there are no wave types, layouts or scripts. |
| Difficulty | Rescuees max out at wave 6, puddles at 7, spawners at 8, tanks at 9, drones (50) at 10, the spawn rate at 11 and drone speed at 12. **From wave 12 on, every wave is the same wave.** |
| Players, saves, ending | Solo, with no save and no ending. An extra hero every 25,000. |
| Look | A tidy neon arena; the hero and the drones are about 12 px. Four minutes into the attract demo, the pilot had reached game over on wave 4. |
| Scale | `rescueRally.ts`, 1,552 lines. |

### Against the classic

The 1982 arena shooter is a pressure cooker built from a few sharp rules:

- **Twin sticks:** move with one, fire in eight directions with the other. This is the game's soul.
- **A roster where every enemy asks a different question:**
  - swarming walkers that converge;
  - **indestructible giants** that wander, stomp the humans, and can only be pushed back;
  - **brains** that hunt the humans and **reprogram them** into enemies, and fire slow homing missiles;
  - **two kinds of spawner**, one hatching enemies that fire leading shots, the other hatching tanks whose shells
    **bounce off the walls**;
  - **static obstacles** in wave-specific shapes.
- **The family is in danger:** rescuing is a race against enemies that harm them.
- **Wave types:** authored brain waves, tank waves and walker waves in a long cycle, each with a different texture.
- **A rescue bonus** that climbs 1,000 to 5,000 and resets on death (matched), and an extra life every 25,000 (matched).

**Verdict:** Rescue Rally has the arena, the rescue multiplier, a spawner and a tank, but it is toothless both ways.
Nothing shoots back, nothing threatens the family, nothing is unkillable, no wave has an identity, and the hero can
only fire where they walk, so the twin-stick that defines the classic is missing. From wave 12 it is one wave on
repeat in one room.

### The upgrade: Rescue Rally — Citywide Reboot

A glitch is spreading through the city's helper bots. The hero sweeps the city district by district, rebooting
glitched drones back into friends and getting every person, pet and little bot home. Two things make it new:

- **The Reboot Squad:** the drones you reboot can fight beside you.
- **Rescue under threat:** the glitch goes after the rescuees, and every rescue is a choice.

**Target length:** a first clear in roughly 50–60 minutes.

#### Structure

- The campaign has **five districts** of **eight waves**, 40 authored waves in all (a nod to the classic's long cycle):
  - waves 1–2 introduce the district's foe and floor;
  - wave 3 is the district's **signature wave type**;
  - waves 4–7 remix the district with everything learned so far;
  - wave 8 is the **district boss**.
- Waves are **data-defined scripts**: enemy mix, entry pattern (edges, corners, a ring, from vents), pylon shape,
  rescuee spots and floor hazards.
- **The Shelter** opens between districts (below).
- Progress saves at each district start.
- A clear rolls credits and unlocks **Rally 100**, a 100-wave cycle in the classic's style.

#### The districts

| # | District | Floor and hazards | New foes | Signature wave | Boss |
| --- | --- | --- | --- | --- | --- |
| 1 | **Neon Plaza** | Today's arena, sharpened | Drone, seeker, spawner, tank, puddle; **Stomper** (an unbeatable wind-up giant); **pylons** in shapes (hearts, stars, the letters K-I-N-D) | **Pylon Garden**: pylon shapes everywhere, threading the hero's path | **The Big Wind-Up** |
| 2 | **Toy Factory** | **Conveyor strips** carry everyone. **Crates** are cover until they're broken. | **Hypno** (hunts the rescuees and glitches them), **Sparker** (fires leading shots) | **Hypno wave**: three hypnos and a crowd of rescuees. Save who you can. | **The Jack-in-the-Box** |
| 3 | **Botanic Dome** | **Vine walls** grow between waves; **sprinkler zones** slow everyone; flowerbeds where rescuees hide | **Prism** (births thornballs), **Thornball** (its shells bounce off walls), **Splitter** (splits into four drones) | **Bounce wave**: prisms and thornballs, all ricochet | **Overgrowth** |
| 4 | **Data Docks** | **Teleport pads** for you and the foes; **laser gates** on a beat; **magnet floors** | **Mimic** (replays your last two seconds), **Shield bot** (a frontal shield), **Magnet** (pulls you and your beams) | **Mirror wave**: mimics of you and your past moves | **The Static Twins** |
| 5 | **Storm Rooftops** | **Lightning** strikes after a glowing-ring tell; **wind** pushes everyone; low roof edges | **Kite drone** (drops pylons in your path), and remixes of everything | **Storm wave**: every foe type at once | **The Glitch Core** (the finale) |

#### The bosses: 0 → 5

1. **The Big Wind-Up** (Neon Plaza): a giant tin robot with a key in its back.
   - Phase 1: it walks the arena stomping shockwave rings (they show as floor cracks first).
   - Phase 2: its key spins faster and little wind-ups pour from its hatch.
   - Phase 3: beam the key to wind it down while it staggers.
2. **The Jack-in-the-Box** (Toy Factory): a box that pops up in different corners. Phase 1, the spring head lunges in
   straight lines. Phase 2, the lid fires confetti fans. Phase 3, it rolls like a die, and the face that lands up picks
   its next attack (the die shows which).
3. **Overgrowth** (Botanic Dome): a great flower-bot. Its petals are turrets you break one by one; root whips
   telegraph as lines across the floor. Phase 3 it uproots and chases you through its own vines.
4. **The Static Twins** (Data Docks): two linked bots with a crackling beam between them that sweeps the arena. Break
   the link when they're far apart; each twin enrages when the other goes down.
5. **The Glitch Core** (finale): a floating core behind four rotating shields.
   - Phase 1: shoot the shields as their gaps line up.
   - Phase 2: it glitches every rescuee in the arena at once, and you must reboot them all while dodging.
   - Phase 3: it chases you around the rooftops, firing echoes of every boss's attacks.
   - **Ending:** the core reboots as a friendly bot and every friend from the Shelter comes up to the roof to cheer.

**Secret: The Reunion.** A **golden chip** is hidden in each district's signature wave, earned by saving every rescuee
in it. With all five, a bonus wave opens with every family reunited on the rooftop, and the **true ending**.

#### The roster: 5 → 17 foes, 5 bosses

| Foe | Tell | Answer |
| --- | --- | --- |
| Drone, seeker, spawner, tank, puddle | As today | As today |
| Stomper | Big, slow, wind-up clicking; the beam only pushes it | Steer it away from the family |
| Hypno | Swirly eyes, heads for rescuees | Priority target; get there first |
| Glitched friend | A rescuee with swirly eyes, chasing you | Beam it to reboot it back into a rescuee, never destroyed |
| Sparker | Flashes before each shot, which leads you | Change direction on the flash |
| Pylon | Static, in wave shapes | Thread it; pop it for small points |
| Prism | Glows before hatching | Kill it before the hatch |
| Thornball | Shells bounce off walls | Don't stand on rebound lines |
| Splitter | Cracks when hit | Finish all four pieces |
| Mimic | An echo of your recent path | Don't retrace your steps |
| Shield bot | Frontal shield | Flank it |
| Magnet | Pulse ring before a pull | Move across the pull, not against it |
| Kite drone | Shadow over the drop point | Stay off the shadow |

#### Systems that run through the whole campaign

- **True twin-stick aim:** reuse the optional aim vector that Prize Show Panic's slice t-027 adds to `InputFrame` (the
  right stick, a second on-screen stick on touch, or a split keyboard). Move-to-aim with B strafe stays for single-stick
  players.
- **Rescue under threat:** stompers knock rescuees dizzy (they wander off the arena and lose their bonus for the wave,
  but always make it home safe). Hypnos glitch them into glitched friends. Nobody is ever hurt, but every second
  counts.
- **Rescue choices:** touching a rescuee collects them at once, as in the classic. Or let up to three **follow you** in
  a little parade and walk them to a **beacon pad** for double the bonus, but a hit scatters the parade.
- **The Reboot Squad (signature):** every 15 drones rebooted inside one chain window frees a **squad bot** that orbits
  you and fires one sparkle a second, up to three at once. A hit costs one squad bot before it costs a hero. Play well
  and the arena gets kinder.
- **Power-ups**, short and shown in the HUD:
  - **Spread:** three-way beam.
  - **Rapid:** double fire rate.
  - **Bounce beam:** shots ricochet once.
  - **Wide beam:** a fat piercing beam.
  - **Bubble shield.**
  - **Sprint shoes:** extra speed.
  - **Rescue magnet:** rescuees run to you.
  - **Pause button:** every foe freezes for 3 s.
- **The Shelter** between districts: every friend rescued lives there and is shown as a growing crowd. Spend **thank-you
  hearts** (never real money) on a spare hero, a starting squad bot, a wider beam, a longer chain window, or a hint
  that shows where the district's golden chip waits.
- **Medals per wave:** Everyone Home (every rescuee saved), Untouched (no hit) and Full Squad (three squad bots).
- **Bigger actors:** draw the hero, foes and rescuees at about 1.5× today's size, with walk cycles and a big sprite
  per boss.

#### Modes

- **Campaign.**
- **Rally 100:** 100 authored waves in the classic's cycle, the leaderboard's main event.
- **Co-op:** 2–4 heroes through the `players` frames. A downed hero becomes a dizzy hero that a partner revives by
  standing close for 2 s, and the rescue multiplier is shared.
- **District Time Attack:** unlocked per district.
- **Classic Rally:** today's rules, kept.

#### Signature features to match or beat

| The classic's feature | Rescue Rally |
| --- | --- |
| Twin sticks | True twin-stick, with strafe kept for single-stick players |
| Indestructible giants that harm the family | The Stomper |
| Brains that reprogram humans | Hypnos and glitched friends, who can be rebooted back |
| Spawners of shooters and wall-bouncers | Sparkers, prisms and thornballs |
| Wave-shaped static obstacles | Pylon shapes per wave |
| Authored wave types in a long cycle | 40 authored waves in the campaign, 100 in Rally 100 |
| A rescue bonus from 1,000 to 5,000 | Kept, plus the escort-to-beacon double |
| **Past the classic** | The Reboot Squad, five districts with floor mechanics, five bosses, the Shelter, co-op with revive, an ending |

#### Slices

Roadmap: t-035 (slice 1), t-036 (slice 2), t-037 (slice 3), t-038 (slice 4). Slice 1 is `ready`; each later slice waits on the one before.


1. **Twin-stick and teeth.** True twin-stick aim (on Prize Show Panic's aim vector from t-027, or landing it here first
   if t-027 hasn't merged); the Stomper, Hypno and glitched friends, Sparker and pylon shapes; rescuees under threat
   with dizzy and glitched states; the escort-to-beacon choice; data-defined wave scripts replacing the random mix; and
   bigger actors. Deterministic tests cover the glitch and reboot round trip and a wave script, and a pilot probe shows
   runs still end.
2. **Neon Plaza, Toy Factory and the Shelter.** The district engine with save/resume; districts 1 and 2 with conveyors,
   crates and their signature waves; the Big Wind-Up and the Jack-in-the-Box; the Reboot Squad; the power-up set; and
   the Shelter with thank-you hearts.
3. **Districts 3–5, the Glitch Core and the endings.** The Botanic Dome (vines and sprinklers), Data Docks (teleports,
   laser gates, magnet floors) and Storm Rooftops (lightning and wind); the prism, thornball, splitter, mimic, shield
   bot, magnet and kite drone; Overgrowth, the Static Twins and the Glitch Core; credits, the golden chips, the Reunion
   and the true ending.
4. **Co-op and the long rally.** Co-op for 2–4 players with revive and a shared multiplier; Rally 100 as the
   leaderboard event; District Time Attack; Classic Rally; and the medals with a board per district. Registry
   `maxPlayers` and the blurb and how-to lines are updated.

---

## 2. Battery Maze (Pac-Man riff)


### What is in the game today

| Area | Today |
| --- | --- |
| Mazes | **One** maze (23 × 21 tiles, 204 sparks, 4 power cells, one tunnel row) for every level. Three wall colour themes cycle, so a long run is the same maze in three colours. |
| Hunters | **Four** gremlins with the classic's four targeting rules, one for one. The chaser targets the robot. The ambusher aims 4 tiles ahead of it. The flanker doubles the vector from the chaser through a point 2 tiles ahead of the robot. The wanderer chases until it is within 8 tiles, then retreats to its corner. |
| Hunter timing | One fixed scatter/chase schedule (7 entries, then chase forever), **the same on every level**. Gremlins leave the dock on a timer only. |
| Power cells | Sleepy time drops from 7 s to 1 s by level 9 and never reaches zero, so a cell never stops being a weapon. Bumps chain 200 / 400 / 800 / 1,600. |
| Bonus prizes | Eight (gear 100 up to crown 5,000) by level, with the crown from level 8 on. A prize appears at the dock twice per level, for 9 s. |
| Intermission | **One** cutscene ("Coffee Break"), the same every third level. |
| Missing rules | No hunter speed-up as the sparks run out. The robot does not slow while eating and has no cornering advantage. No late levels where cells stop scaring the gremlins. |
| Difficulty | Robot and gremlin speed max out at level 6, sleepy time and release rate at level 9. **From level 9 on, every level is the same level**, apart from the wall colour. |
| Players, saves, ending | Solo, with no save and no ending. An extra robot at 10,000, then every 20,000. |
| Look | A handsome neon circuit-board maze with bevelled walls and glowing sparks. Four minutes into the attract demo, the pilot had reached game over on level 2. |
| Scale | `batteryMaze.ts`, 1,877 lines. |

### Against the classic

The 1980 maze game looks like one board, but it changes under the player's feet:

- **Four hunters with personalities**, which Battery Maze already matches.
- **Level tables:** the scatter/chase timing, every speed, and the time the hunters stay frightened all change level
  by level. By the late levels the power pellet barely frightens them and finally doesn't at all, so the pellets turn
  from weapons into escape tools.
- **The lead hunter's cruise mode:** it speeds up twice as the dots run out, so the endgame of every board tightens.
- **Feel rules:** the hero slows while eating dots and corners faster than the hunters, and the hunters crawl in the
  tunnel. The skill lives in these details.
- **A fruit progression** that ends in keys, and **three intermissions** that tell a little comic story.
- The **1981 follow-up** that shares its rules added **four mazes** with extra tunnels, **fruit that bounces through the
  maze**, less predictable hunters, story intermissions and two players.
- The genre's modern reinventions went further still: timed score attacks, mazes that refill, and sleeping hunters you
  can string together for huge combos.

**Verdict:** Battery Maze copies the 1980 game's hunters faithfully and draws them beautifully, but it stops at the
hunters. It has one maze, one schedule, no endgame squeeze, no late-level shift and one intermission, and every level
from 9 on is identical. It is a faithful first board of the classic, with none of what the follow-up added and
nothing of its own.

### The upgrade: Battery Maze — The Charging Network

The city's power grid has gone glitchy, and the little cat-eared robot travels inside the machines to recharge them,
board by board. Every **board** is the inside of a different appliance with its own maze shapes and its own rule. Two
signature twists make it more than a maze chase:

- **Rewire:** switches at junctions let the robot re-route the maze itself.
- **The Friend Train:** rebooted gremlins don't just go home; they join you for a while.

**Target length:** a first clear in roughly 45–55 minutes.

#### Structure

- The campaign has **six boards** in **three Power Phases** (acts), a **boss maze** at the end of each phase and a
  **secret seventh board**.
- Each board has **three mazes**, each its own original layout:
  - maze 1 introduces the board's mechanic and new gremlin;
  - maze 2 is the board's **special maze**;
  - maze 3 remixes the board with everything learned so far.
- After each board comes a **story intermission**: a different short comic each time, not one cutscene on repeat.
- Every board has its own wall art, floor, palette, music loop and title card.
- **The Charging Bay** opens between phases (below).
- Progress saves at each board start.
- A clear rolls credits and unlocks **Overclocked**, a New Game+ with the late-level tables from the first maze.

#### The boards

**Power Phase 1: Morning Boot**

| # | Board | Maze and mechanic | New gremlins | Special maze |
| --- | --- | --- | --- | --- |
| 1 | **Cozy Charger** | Today's maze, retuned with the per-level tables, plus two new layouts | Chaser, ambusher, flanker, wanderer | **Prize Parade**: the bonus prizes walk the maze from the tunnels, the follow-up's roaming fruit reimagined. Catch all eight. |
| 2 | **Toaster Works** | **Conveyor corridors** that carry robot and gremlins one way, and **pop-up toast** that blocks a corridor on a beat (the slot glows first) | **Sprinter** (spots you down a straight, flattens its ears, then dashes at double speed), **Crumb Snacker** (eats sparks too; after 15 it overclocks and turns red) | **Breakfast Rush**: three toast pops, each a big prize for a few seconds. |

**Boss 1: Gremlin Mama.** A gremlin two tiles wide that can't fit the narrow corridors.
- **Phase 1:** she patrols the wide halls and drops babies (small, fast, harmless when sleepy).
- **Phase 2:** she needs three bumps, one per power cell, and each bump sends her round the board backwards.
- **Phase 3:** she plugs the dock. Rewire the maze to lure her into a dead end, then bump her home.

**Power Phase 2: Afternoon Load**

| # | Board | Maze and mechanic | New gremlins | Special maze |
| --- | --- | --- | --- | --- |
| 3 | **Greenhouse Grid** | **Vines** grow across corridors on a timer (the leaf buds show first), and a watering-can pickup clears them. **Flower gates** open when every spark in a bed is eaten. | **Copycat** (mirrors your stick; lead it into dead ends), **Bramble** (lays a short-lived thorn wall behind it) | **Bloom Run**: open all six flower gates before the vines close the board. |
| 4 | **Cold Storage** | **Ice corridors**: on ice the robot and the gremlins slide to the next junction with no stopping and no reversing. **Fans** blow along whole rows. | **Blinker** (blinks twice, then hops two tiles through a wall), **Snowball** (rolls downhill along a fan row, growing as it goes) | **Thaw**: the ice melts maze by maze as you eat its sparks; finish before the freezer door shuts. |

**Boss 2: The Glitch Train.** A segmented gremlin, a head and eight cars, that snakes through the maze.
- **Phase 1:** only the caboose can be bumped, and only while it is sleepy. Each bump reboots one car and shortens the
  train.
- **Phase 2:** the head speeds up as the train shortens, and it starts using the tunnels.
- **Phase 3:** it splits into two trains that pincer. Rewire them into each other.

**Power Phase 3: Night Shift**

| # | Board | Maze and mechanic | New gremlins | Special maze |
| --- | --- | --- | --- | --- |
| 5 | **Arcade After Hours** | **Lights out**: only a cone around the robot and the blinking cabinet lamps are lit; sparks glow faintly. | **Static** (invisible outside the light, but it leaves crackle on the tiles it crosses), **Gatekeeper** (parks on a junction and shuts it; bump it while sleepy to open a shortcut) | **Lamp Lighter**: every spark eaten near a cabinet relights it. Light the whole arcade. |
| 6 | **Rooftop Solar Farm** | A **day/night cycle**: sparks respawn on the solar panels in the sun, and **mirror junctions** rotate on the clock | **Twins** (a pincer pair; reboot one and the other sulks slowly home), and remixes of every gremlin | **Sunset Charge**: bank the panels' sparks before the sun goes down. |

**Finale: The Overload.** The grid's master gremlin, a great face that fills the charging dock.
- **Phase 1:** it fires power surges down whole rows and columns; the row lights up for a second first.
- **Phase 2:** it rewires the maze itself, sliding walls to cut you off. Your switches fight its switches.
- **Phase 3:** it climbs out and chases you, three tiles wide. Eat the four plug cells, then bump its four plugs to
  unplug it.
- **Ending:** the grid hums back to life, and the gremlins, rebooted for good, gather at the dock to wave the robot
  home.

**Secret board: The Battery Garden.** One **golden bolt** is hidden on each board, earned by completing its special
maze without losing a robot.
- With all six, a seventh board opens: shifting mazes, every gremlin, and prizes everywhere.
- Clearing it gives the **true ending**: the gremlins plant a garden of glowing flowers on the rooftop.

#### The roster: 4 → 13 gremlins, 3 bosses

| Gremlin | Tell | Answer |
| --- | --- | --- |
| Chaser, ambusher, flanker, wanderer | As today, plus the chaser's overclock glow | Learn their targets; use the corners |
| Sprinter | Ears flatten and eyes glow on a straight | Break line of sight at a corner |
| Crumb Snacker | Heads for sparks, not you | Race it; bump it while sleepy before it overclocks |
| Copycat | Moves when you move, mirrored | Steer it into dead ends |
| Bramble | A thorn trail behind it | Don't follow it; go round |
| Blinker | Blinks twice, then hops a wall | Don't stand two tiles from a thin wall |
| Snowball | Rolls along fan rows and grows | Catch it small, or step out of its row |
| Static | Crackle left on tiles | Read the crackle in the dark |
| Gatekeeper | Parks on a junction | Bump it while sleepy for a shortcut |
| Twins | Approach from opposite ends | Reboot one; the other gives up |

Hazards: conveyors, pop-up toast, vines, ice, fans, the dark and the day/night cycle. Bosses: Gremlin Mama, the
Glitch Train and the Overload.

#### Systems that run through the whole campaign

- **Per-level tables (match the classic):**
  - the scatter/chase schedule, every speed, sleepy time and the dock release counters all come from a table per maze;
  - the chaser **overclocks** (+5% at 30 sparks left, +10% at 15) with a glowing-ears tell;
  - from the late mazes on, sleepy time reaches zero and the cells become **shield cells**: 2 s of safety and every
    gremlin turns round, so the cells stay useful;
  - the robot slows a little while eating and **corners** a little faster than the gremlins, as in the classic.
- **Rewire (signature):** switch tiles sit at chosen junctions. Press A on one to flip it: one corridor closes, another
  opens, and the gremlins re-path at once. Each maze grants three flips, refilled by power cells. Trapping a gremlin in
  a loop, or bowling a whole pack into a dead end, is the high skill.
- **The Friend Train (signature):** every gremlin you bump during one power cell reboots into a friendly bot that joins a
  train behind the robot, following its path and eating any spark it passes. When the cell ends the friends peel off
  home, and the train pays 500 × its length². A four-friend train is the board's big moment.
- **Roaming prizes:** prizes enter from the tunnels and wander the maze. Two new ones (a golden plug, a rainbow
  battery) sit beyond the crown.
- **Story intermissions:** six short comics (Coffee Break, Spilled Oil, Charging Party, Snow Day, Lights Out, Sunrise),
  one after each board.
- **Power-ups** roll out of the dock now and then:
  - **Magnet:** sparks within three tiles come to you.
  - **Turbo Wheels:** +25% speed for 6 s.
  - **Decoy Bot:** a cardboard robot the gremlins chase.
  - **Freeze Pop:** gremlins freeze but are not bumpable.
  - **Watering Can / Lamp:** the board's own tool.
- **The Charging Bay** between phases: spend **bolts** earned in play (never real money) on a spare robot, an extra
  rewire flip, a starting magnet, or a hint that shows where the board's golden bolt is.
- **Medals per maze:** Clean Charge (no robot lost), Full Train (a four-friend train) and Prize Hunter (every prize).

#### Modes

- **Campaign.**
- **Rush Hour:** a timed score attack in which sparks flow back into the maze in waves; eat a battery bar to bank them.
  This is the leaderboard event.
- **Co-op:** two robots through the `players` frames, sharing the sparks. A sleepy gremlin bumped by both robots at
  once pays a Pair Bonus. A caught robot becomes a little flickering spark bot that its partner revives by touch.
- **Gremlin Tag:** asymmetric versus for 2–4 players, with player 1 as the robot and the others steering gremlins. A
  sleepy gremlin's player must flee.
- **Classic Maze:** today's single maze and rules, kept.

#### Signature features to match or beat

| The classic's feature | Battery Maze |
| --- | --- |
| Four hunter personalities | Kept, plus eight more gremlins with their own tells |
| Per-level scatter/chase, speeds and fright time | Per-maze tables, with fright time reaching zero and shield cells |
| The lead hunter's cruise mode | Overclock, with a visible tell |
| Hero slows while eating; cornering; tunnel slowdown | All three |
| Fruit progression | Ten prizes, now roaming |
| Three intermissions | Six story intermissions |
| Four mazes and bouncing fruit (follow-up) | Six boards, 18 mazes, 3 boss mazes, roaming prizes |
| Two players | Co-op and Gremlin Tag |
| **Past the classic** | Rewire switches, the Friend Train, board mechanics, bosses, an ending |

#### Slices

Roadmap: t-039 (slice 1), t-040 (slice 2), t-041 (slice 3), t-042 (slice 4). Slice 1 is `ready`; each later slice waits on the one before.


1. **The rules engine and the Friend Train.** Turn the maze into data so many layouts can load (validated by the
   existing `BATTERY_MAZE` connectivity test, generalised to every layout); per-maze tables for scatter/chase, speeds,
   sleepy time and dock release counters; overclock with its tell; shield cells; the eating slowdown and cornering;
   roaming prizes with the two new ones; the Friend Train; and Rewire switch tiles. Deterministic tests cover the
   tables, the train payout and switch re-pathing, and a pilot probe shows runs still end.
2. **Power Phase 1 and the Charging Bay.** The board engine (boards, mazes and special mazes as data) with save/resume;
   Cozy Charger with two new layouts and the Prize Parade; Toaster Works with conveyors, pop-up toast, the Sprinter and
   the Crumb Snacker; Gremlin Mama's boss maze; the first two story intermissions; the power-up roll; and the Charging
   Bay.
3. **Power Phases 2 and 3, the Overload and the endings.** Greenhouse Grid (vines and flower gates), Cold Storage (ice
   and fans), Arcade After Hours (lights out) and the Rooftop Solar Farm (day/night and mirror junctions), each with its
   special maze; the Copycat, Bramble, Blinker, Snowball, Static, Gatekeeper and Twins; the Glitch Train and the
   Overload; the remaining intermissions; credits, the golden bolts, the Battery Garden and the true ending; and
   Overclocked New Game+.
4. **Together and versus.** Two-robot co-op with revive and the Pair Bonus; Gremlin Tag for 2–4 players through the
   `players` frames; Rush Hour as the leaderboard event; Classic Maze; and the medals with a board per board. Registry
   `maxPlayers` and the blurb and how-to lines are updated.

---

## 3. Sink Suds (Bubbles riff)


### What is in the game today

| Area | Today |
| --- | --- |
| Stages | **One** sink, the same oval basin, for every level ("SINK n"). One kitchen backdrop. Nothing about the room ever changes. |
| Food | Crumbs (10 points, +1 growth) and grease (25 points, +2). Drips from the tap add more mess over time. |
| Growth | Five bubble stages, 8 growth each (about 32 crumbs to fill). Full size lights the drain; sail down it for a bonus of 1,000 × level, less 50 per crumb left. Losing a life shrinks the bubble one stage. |
| Pests | **Two.** The rust mite pops a small bubble but is food (100) from stage 3; a swallowed mite drops a new crumb. The scrub brush hunts the bubble within 120 px, otherwise eats the mess, and is **always deadly and can never be beaten**. |
| Moves | Steer with momentum; A gives a puff of speed (70-tick cooldown). |
| Scoring | Flat points per bite, plus the drain bonus. No chains. An extra bubble every 15,000. |
| Difficulty | Starting mess (50) and brushes (3) max out at level 7, mites (9) at 8, brush speed and the drip rate at 11, mite speed at 12. **From level 12 on, every sink is the same sink.** |
| Players, saves, ending | Solo, with no save and no ending. |
| Look | A charming chrome basin on violet tiles, a cheerful bubble face, crumbs, mites and two brushes. Sink 5 looks exactly like sink 1. Four minutes into the attract demo, the pilot had reached game over on sink 5. |
| Scale | `sinkSuds.ts`, 1,030 lines: the smallest cabinet in this batch. |

### Against the classic

The 1982 sink game is small too, but every pest does a job:

- **Grow by cleaning:** crumbs, grease and little crawlers feed the bubble, and the bubble visibly grows into a
  character as it fills.
- **A cast of pests with different rules:** crawlers that are food once you're big enough; scuttlers that come up out
  of the drain; sponges and brushes that **clean the sink too**, racing you for the mess; blades that skate across and
  are always deadly. As the bubble grows, the pests it can take on change.
- **The race:** dawdle and the cleaners take the mess, leaving you hungry with the drain still shut.
- **Momentum steering** that is slippery on purpose.
- **The drain exit** as the goal of every sink.

**Verdict:** Sink Suds has the premise (grow, then sail down the drain) and two of the pests, but it is one basin in one
kitchen with an unbeatable brush, and it has nothing to say after sink 5. It is the thinnest cabinet in this batch: no
stage identity, no reason to come back, and a growth system that is only a size meter.

### The upgrade: Sink Suds — The Big House Wash

The whole robot house needs a wash, and one brave bubble does it room by room. Every room is a different **basin with
its own shape and its own water physics**: a tub with a current, a spinning drum, a fish tank you see from the side,
a car wash on a conveyor. Two twists make it newer than the classic:

- **Size is everything:** your size is your health, your weapon and your ammunition.
- **Watch it get clean:** the basin visibly comes clean wherever you roll.

**Target length:** a first clear in roughly 40–50 minutes.

#### Structure

- The campaign has **six rooms** in **three Wash Cycles** (acts), a **boss at the end of each cycle** and a **secret
  room**.
- Each room has **four basins**:
  - basins 1–2 introduce the room's water physics and pest;
  - basin 3 is the room's **special basin**, with its own objective;
  - basin 4 remixes the room with everything learned so far.
- Every room has its own basin shapes (as data), backdrop, palette and music loop.
- **The Soap Shop** opens between rooms (below).
- Progress saves at each room start.
- A clear rolls credits and unlocks **Deep Clean**, a New Game+ with dirtier basins and faster pests.

#### The rooms

**Wash Cycle 1: Morning Rinse**

| # | Room | Basin and physics | New pests | Special basin |
| --- | --- | --- | --- | --- |
| 1 | **Kitchen Sink** | Today's oval basin, plus a **double sink** joined by an overflow gap and a **drying rack** whose shadows hide crumbs | Rust mite, scrub brush (now beatable, below), **Sponge** (soaks suds: touching it shrinks you a stage instead of popping you), **Drain Gremlin** (the drain gurgles, then it pops out and darts) | **Dish Stack**: floating plates, each with its own grime. Scrub every plate clean. |
| 2 | **Bath Time** | A long tub with a **faucet current** flowing along it. Rubber ducks bob (bumpers); shampoo slicks are fast lanes. | **Scum Slug** (leaves a sticky trail that slows you), **Loofah** (big and slow; soaks a stage on touch) | **Duck Round-up**: nudge five rubber ducks up to the faucet end, against the current. |

**Boss 1: Bristleton, the Big Brush.** A scrub brush as long as the tub.
- **Phase 1:** it sweeps arcs across the basin; the bristle shadow shows the arc first.
- **Phase 2:** it spins like a top and throws suds rings.
- **Phase 3:** it sheds mini-brushes. At full size, bump it on the handle end three times to tip it into the bath.

**Wash Cycle 2: Midday Spin**

| # | Room | Basin and physics | New pests | Special basin |
| --- | --- | --- | --- | --- |
| 3 | **Laundry Drum** | A round drum that **rotates**: everything drifts round the rim. The spin speed changes on a dial tell. | **Lint Ball** (grows as it rolls up crumbs; catch it small), **Sock Snake** (a chain of socks; nibble it from the tail) | **Odd Socks**: bump matching socks together to pair them before the spin cycle. |
| 4 | **Fish Tank** | **Side view with buoyancy**: the bubble rises on its own and steering down costs effort. Gravel floor, swaying plants, friendly fish. | **Algae Puff** (blooms and clouds the water), **Snail** (armoured; only a full-size bubble can roll it over), **Pufferfish** (inflates on a tell; never touch it inflated) | **Clear the Glass**: scrub the algae off the front glass until you can see the fish. |

**Boss 2: Mossback.** An old giant snail covered in algae, living in the tank.
- **Phase 1:** it crawls the glass shedding algae puffs.
- **Phase 2:** it hides in its shell and rolls along the gravel; buoyancy lets you rise out of its way.
- **Phase 3:** the shell opens. Scrub its mossy back at full size until it shines.

**Wash Cycle 3: Evening Shine**

| # | Room | Basin and physics | New pests | Special basin |
| --- | --- | --- | --- | --- |
| 5 | **Garden Birdbath** | Outdoors: **rain** adds drips everywhere, floating **leaves** drift as moving cover, and **ripples** push the bubble outward | **Water Strider** (skates straight across at speed, the always-deadly skater; a ripple line on the rim is its tell), **Leaf Boat** (a pest riding a leaf, sheltered from the front) | **Rain Race**: the rain keeps falling. Out-clean it until the shower passes. |
| 6 | **The Car Wash** | The floor is a **conveyor**; **roller brushes** sweep whole lanes after a lane-light tell; **wax jets** puff on a beat | **Wax Blob** (hardens into a wall if left), **Spinner** (a rolling wheel brush that ricochets) | **Full Detail**: clean a whole robot car, panel by panel, as it rides through. |

**Finale: The Grime King** at the town fountain.
- **Phase 1:** the fountain's jets push the bubble about while grime minions guard the King.
- **Phase 2:** the King splits into grime drops that try to re-form. Swallow them before they do.
- **Phase 3:** the fountain runs clear, and the bubble, filled past full, becomes a **giant bubble** as wide as the
  basin. Sweep the King down the drain.
- **Ending:** the whole town's fountains sparkle and the house robots blow bubbles from every window.

**Secret room: The Bubble Bath Palace.** A **golden soap bar** is hidden in each room, earned by finishing its special
basin 95% clean.
- With all six, a seventh room opens: a palace bath of rainbow foam with every pest.
- Clearing it gives the **true ending**.

#### The roster: 2 → 14 pests, 3 bosses

| Pest | Tell | Answer |
| --- | --- | --- |
| Rust mite | Small, scuttling | Avoid while small; eat it from stage 3 |
| Scrub brush | Hunts at short range, eats mess | Avoid while small; at full size bump it from behind to tip it (stunned 4 s) |
| Sponge | Fat and porous | Keep away, or trap it with a soap shot |
| Drain Gremlin | The drain gurgles first | Don't loiter over the drain |
| Scum Slug | Sticky trail | Don't cross the trail |
| Loofah | Big and slow | Go round; trap it for a big bonus |
| Lint Ball | Grows as it rolls | Catch it small |
| Sock Snake | A chain of socks | Nibble from the tail |
| Algae Puff | Swells before it blooms | Pop it before the bloom |
| Snail | Armoured shell | Roll it over at full size |
| Pufferfish | Inflates on a tell | Wait for it to deflate |
| Water Strider | A ripple line on the rim | Get off the line |
| Wax Blob | Glossy, then hardens | Clear it before it sets |
| Spinner | Rolls and ricochets | Read the bounce |

Hazards: drips, the faucet current, the drum's spin, buoyancy, rain, the conveyor and roller brushes. Bosses:
Bristleton, Mossback and the Grime King.

#### Systems that run through the whole campaign

- **Size is everything (signature):**
  - B blows a **soap shot**, a little bubble that costs one growth stage (never below stage 2);
  - it floats straight and traps the first pest it touches, and the trapped pest drifts to the drain for 300 × a chain
    count;
  - growth is health (a hit shrinks you), weapon (bigger eats more), ammunition (soap shots) and the drain key (full
    size). Every choice spends the same meter.
- **Watch it get clean (signature):** each basin starts under a grime layer, and the bubble's path scrubs it away.
  - The HUD shows the percentage clean, and **Squeaky Clean** (95% or more) pays a big bonus.
  - Sponges and brushes clean too, racing you for both the grime and the food, as the classic's cleaners did.
- **The bubble grows a face:** its expression changes with each stage, from a nervous blob to a beaming full bubble with
  cheeks and sparkle eyes.
- **Chains:** eat or trap within a second of the last for ×2, ×3, ×4.
- **Power-ups** float up from the drain:
  - **Rubber Duck:** a bodyguard that bumps pests away.
  - **Lemon Zest:** pests flee for 6 s.
  - **Super Suds:** instant full size for 8 s.
  - **Squeegee:** wipes a stripe of grime clean.
  - **Bath Bomb:** a fizz burst that traps every pest nearby.
  - **Magnet Sponge:** crumbs drift to you.
- **The Soap Shop** between rooms: spend **soap bars** collected in play (never real money) on a spare bubble, a longer
  puff, starting at stage 2, a sturdier bubble (one free hit) or a hint for the room's golden soap. Bubble skins
  (rainbow, starry, frosted) are cosmetic unlocks.
- **Medals per basin:** Squeaky Clean (95%), No Pop (no life lost) and Quick Rinse (under par).

#### Modes

- **Campaign.**
- **Squeaky Clean:** a time attack per basin on cleanliness and speed. Endless Sink (sinks forever, every pest) is the
  leaderboard event.
- **Bubble Buddies:** 2–4 bubbles through the `players` frames. Two bubbles that touch **merge** into one big bubble
  steered by both players (their inputs averaged); B splits it again.
- **Suds Sumo:** versus for 2–4. Bigger bubbles push smaller ones, and the last bubble in the basin wins.
- **Classic Sink:** today's single sink, kept.

#### Signature features to match or beat

| The classic's feature | Sink Suds |
| --- | --- |
| Grow by cleaning; the bubble becomes a character | Five stages with a face that grows up, plus the grime layer |
| Pests with distinct rules | 14 pests with tells |
| Cleaners that race you for the mess | Sponges and brushes clean grime and food too |
| Always-deadly skaters | Water Strider and Spinner, telegraphed |
| Drain scuttlers | The Drain Gremlin |
| What you can take on changes as you grow | Mites at stage 3, brushes tipped at full size, snails rolled at full size |
| Momentum steering | Kept, plus current, spin, buoyancy and conveyor physics |
| **Past the classic** | Size as ammunition, a visible clean, six rooms with different physics, three bosses, merge co-op, an ending |

#### Slices

Roadmap: t-043 (slice 1), t-044 (slice 2), t-045 (slice 3), t-046 (slice 4). Slice 1 is `ready`; each later slice waits on the one before.


1. **The basin engine and size-as-ammunition.** Basins as data (oval, double sink, tub, drum, side-view tank, conveyor)
   with a physics hook per shape; the grime layer with percentage clean, drawn as a cached mask; the soap shot and
   trapping, with chains; the growing bubble face; beatable brushes; the sponge and the Drain Gremlin; and a
   double-density pest pass. Deterministic tests cover growth spending, trapping and the clean percentage, and a pilot
   probe shows runs still end.
2. **Wash Cycle 1 and the Soap Shop.** The room engine with save/resume; Kitchen Sink (double sink and drying rack) and
   Bath Time (faucet current, ducks, slicks) with their special basins; the scum slug and loofah; Bristleton; the
   power-ups; and the Soap Shop.
3. **Wash Cycles 2 and 3, the Grime King and the endings.** The Laundry Drum (rotation), Fish Tank (side view and
   buoyancy), Garden Birdbath (rain and ripples) and Car Wash (conveyor and rollers), with their pests and special
   basins; Mossback and the Grime King with the giant-bubble finish; credits, the golden soaps, the Bubble Bath Palace
   and the true ending; and Deep Clean New Game+.
4. **Bubble Buddies and Suds Sumo.** Merge-and-split co-op for 2–4 players; Suds Sumo versus; Squeaky Clean time attack;
   Endless Sink as the leaderboard event; Classic Sink; and the medals with a board per room. Registry `maxPlayers` and
   the blurb and how-to lines are updated.

---

## 4. Butterfly Joust (Joust riff)


### What is in the game today

| Area | Today |
| --- | --- |
| Arena | **One** arena: seven ledges over a pond, one sunset sky. From wave 3 the bottom ledge crumbles in from both ends, up to 56 px a side by wave 10. Nothing else about the arena ever changes. |
| Riders | **Three tiers.** The drifter (500 points) wanders. The hunter (750) chases your height. The shadow (1,500) tries to get above you. 2–8 riders a wave, shimmering in at five spawn spots. |
| Jousting | The higher rider wins; riders within 6 px of the same height bounce apart. A bonked rider curls into a cocoon. Scoop it for 250–1,000 (plus 500 in mid-air), or it hatches into the next tier up. |
| Predator | A storm cloud comes hunting after 45 s of a wave (25 s by wave 8). It is deadly, but bonking it from above pops it for 2,000. |
| Wave types | **Two.** A normal wave, and a cocoon wave every fifth wave. A survivor bonus (3,000) for a wave without a death. |
| The pond | Fall in and you lose a life. Riders who fall in simply vanish. Nothing reaches up out of the water. |
| Difficulty | Rivals max out (8) at wave 7. The hunter share stops rising at 5, the shadow share and storm timing at 8, the hatch time at 9, the crumble at 10, rider and storm speed at 11. **From wave 11 on, every wave is the same wave** (with a cocoon wave every fifth). |
| Players, saves, ending | **Solo**, with no save and no ending. An extra butterfly every 20,000. |
| Look | A gorgeous sunset with parallax ridges, rainbow-edged floating ledges and a glittering pond: the best-looking backdrop in this batch, and the only one the game has. Four minutes into the attract demo, the pilot had reached game over on wave 5. |
| Scale | `butterflyJoust.ts`, 1,499 lines. |

### Against the classic

The 1982 flap-and-lance game is built around a few big ideas:

- **Height is everything,** with three enemy tiers whose eggs hatch into tougher riders (matched).
- **A mount flies in to collect a hatched rider**, so a hatch is a second chance to stop it.
- **Announced wave types:** an egg wave, a survival wave (bonus for not dying), a gladiator wave (bonus for the first
  kill) and a team wave (a co-op bonus if neither player unhorses the other).
- **A hand reaches up out of the lava** to grab low fliers; flapping hard breaks free.
- **The arena changes:** the bridge over the lava burns away and ledges vanish on set waves.
- **A flying predator** that arrives if you dawdle and can only be beaten by a precise hit to its open mouth, an
  expert's skill check.
- **Two players at once,** as allies or rivals. Jousting each other is allowed, and that is half the game's character.

**Verdict:** Butterfly Joust is the closest thing to a faithful remake in this batch. The flap feels right, the three
tiers and hatching cocoons are there, and it looks wonderful. But it has one arena, no hand in the pond, only two wave
types, a predator easier to beat than the classic's, and no second player, which is the classic's heart. From wave 11
nothing changes.

### The upgrade: Butterfly Joust — The Four Gardens Tourney

The grumpy moth riders have challenged the robot and the rainbow butterfly to a tourney, season by season, garden by
garden. Each arena is a different garden with its own ledges, weather and pond-dweller. Every arena ends in a
**champion bout**, a boss rider with phases. Three new verbs make the height game richer:

- **Air Combo:** bonk after bonk without landing.
- **Charge Joust:** a lunge that breaks level stalemates.
- **Thermals and wind:** height you can read off the arena.

**Target length:** a first clear in roughly 45–60 minutes.

#### Structure

- The tourney has **five arenas** and the **Moon Garden** final. Each arena has **six waves** and a **champion bout**:
  - waves 1–2 introduce the arena's mechanic and new rider;
  - wave 3 is the arena's **signature wave type**;
  - waves 4–6 remix the arena with everything learned so far;
  - then the champion steps out.
- Waves are **announced on a banner** with their bonus rule, as the classic's are.
- Every arena has its own ledge layout (original layouts, as data), backdrop, palette and music loop.
- **The Wing Garden** opens between arenas (below).
- Progress saves at each arena start.
- A clear rolls credits and unlocks **Champion's Circuit**, a New Game+.

#### The arenas

| # | Arena | Ledges and mechanic | Pond or floor | New riders | Signature wave | Champion |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | **Sunset Pond** | Today's ledges; the bottom ledge crumbles | **The Pond Frog**: bubbles rise, the eyes surface, then its tongue snatches a low flier. Mash flap to break free. | Drifter, hunter, shadow | **Survival** (no butterfly lost) | **Sir Bumbleton** |
| 2 | **Spring Meadow** | **Flower ledges** open at dawn and fold shut on a petal-cycle tell. **Dandelion puffs** float up as one-use stepping clouds. **Sun-patch thermals** lift you for free. | A lily pond; the frog returns | **Glider** (rides thermals, never flaps), **Twin riders** (two moths on one mount; a bonk splits them into two cocoons) | **Gladiator** (bonus for the first bonk) | **The Dandelion Duchess** |
| 3 | **Thunderhead Heights** | No ground at all: **drifting cloud ledges**. **Lightning** flashes a ledge, then strikes it. **Rain** soaks your wings (heavier, more flaps); a **rainbow updraft** dries them. | Open sky below: falling drops you to the lowest cloud bank, at a cost | **Diver** (stoops from above; its shadow on the ledge below is the tell), **Lancer** (lowers a long lance before a charge and wins level clashes) | **Storm** (the predator from the start) | **Old Thunderhead** |
| 4 | **Autumn Orchard** | **Branch ledges** sway in the **wind**, and a weather vane turns before each gust. **Falling apples** (bonk one and it knocks a rider down a ledge; land on one and you bounce). **Leaf piles** hide cocoons. | An apple-strewn stream with the frog's cousin | **Shield Beetle** (needs two bonks; the first knocks its shell off), **Carrier** (swoops in to collect a hatched rider; scoop the cocoon first, or bonk the carrier for 1,000) | **Cocoon** (today's wave, with carriers) | **The Scarecrow Kite** |
| 5 | **Lantern Snowfield** | Night festival. **Icy ledges** slide on landing. **Paper lanterns** rise slowly as moving ledges, then fade. | **A frozen pond** that cracks after landings | **Frost Moth** (freezes the ledge it touches), and remixes | **Team** (co-op: no friendly bonk) or **Lantern** (solo: collect the lanterns) | **The Frost Moth Queen** |
| — | **The Moon Garden** (final) | Moonlit ledges that appear only while the moon is out of the clouds | A mirror pool | All of them | **The Gauntlet**: one wave of each type in a row | **The Mirror Moth** |

#### The champions: 0 → 6

1. **Sir Bumbleton** (Sunset Pond): a big bumblebee rider with a long lance. Phase 1, he wins every level clash, so
   get above him. Phase 2, he calls a bee escort that flies in formation. Phase 3, he dives from the ceiling; read his
   shadow.
2. **The Dandelion Duchess** (Spring Meadow): she floats on a dandelion clock. Each bonk blows off seed parachutes that
   land as drifters. Pop the seeds before they land.
3. **Old Thunderhead** (Thunderhead Heights): a storm cloud with one eye. The eye opens only between lightning strikes;
   a bonk to the open eye is the only hit, the classic's predator check made kind.
4. **The Scarecrow Kite** (Autumn Orchard): a giant kite flown by three moth riders. Bonk each rider to cut a string;
   with each string gone the kite dives harder. With all three cut, it tumbles into the leaves.
5. **The Frost Moth Queen** (Lantern Snowfield): her wingbeats freeze ledges in sequence. Phase 2 she shatters the frozen
   pond; phase 3 she flies only at the top of the screen, so ride the lanterns up to her.
6. **The Mirror Moth** (the final):
   - Phase 1: it rides your exact moves one second late.
   - Phase 2: it splits into two mirrors.
   - Phase 3: it flies against you on equal terms, with your lance and your combo.
   - **Ending:** the moth riders lower their lances, and the tourney becomes a festival where everyone flies together.

**Secret: The Rainbow Lists.** A **golden petal** is hidden in each arena, earned by clearing its signature wave
without losing a butterfly. With all five, a bonus arena opens with every rider at full speed, and the **true ending**.

#### The roster: 4 → 13 riders and fliers, 6 champions

| Rider | Tell | Answer |
| --- | --- | --- |
| Drifter, hunter, shadow | As today | Get above them |
| Glider | Never flaps; circles up a thermal | Intercept it at the top of the thermal |
| Twin riders | Two moths on one mount | Bonk to split, then scoop both cocoons |
| Pollen Bomber | Drops a pollen puff that makes you sneeze (half a second of lost control) | Fly round the puff, not through it |
| Diver | Its shadow on the ledge below | Get under a ledge |
| Lancer | Lowers its lance before a charge | Never meet it level; get above |
| Shield Beetle | A shell glints | Bonk twice |
| Carrier | A whistle as it swoops in for a hatchling | Scoop the cocoon first, or bonk the carrier |
| Frost Moth | Ice spreads where it lands | Leave the ledge |
| Thundercap (predator) | Arrives if a wave drags; its eye opens between flashes | Bonk the open eye |
| Pond Frog (pond hazard) | Bubbles, then eyes | Stay high; mash flap if caught |

The Pollen Bomber appears in Spring Meadow's remix waves. Hazards: crumbling and folding ledges, lightning, rain,
wind, apples, ice and lantern fade.

#### Systems that run through the whole tourney

- **Air Combo (signature):** bonk after bonk without touching a ledge builds a multiplier (×2, ×3, ×4 …) shown as a
  rainbow streamer behind the butterfly. Landing banks it.
- **Charge Joust:** hold B to brace (wings back), then release for a short horizontal lunge that wins level clashes,
  with a 2 s cooldown. Lancers are the counter-threat.
- **Thermals and wind:** sun patches and updrafts lift fliers for free, and gusts push sideways. Reading them is the new
  height game.
- **Wave types:** Survival, Gladiator, Cocoon, Storm, Team, Lantern and the Gauntlet, each announced with its bonus.
- **The pond-dwellers:** the frog and its cousins replace the classic's grabbing hand. A catch is never instant: flap
  hard to break free.
- **The Wing Garden** between arenas: spend **pollen** collected in play (never real money) on a spare butterfly, a
  stronger flap, a longer combo window, a firmer frog escape, or a hint for the arena's golden petal. Wing patterns
  (monarch, morpho, swallowtail) are cosmetic unlocks.
- **Medals per wave:** Unbonked (no life lost), Air Ace (a ×4 combo) and Quick Lance (under par).

#### Modes

- **Tourney:** the campaign.
- **Jousting Party:** 2–4 riders through the `players` frames.
  - **Co-op:** the classic's team wave runs throughout, with a bonus for not bonking each other.
  - **Versus, Last Butterfly Flapping:** a free-for-all in which a bonked player becomes a cocoon and hatches back in
    5 s; the most bonks in three minutes wins.
- **Endless Pond:** endless waves in today's arena with every rider, the leaderboard event.
- **Classic Pond:** today's rules, kept.

#### Signature features to match or beat

| The classic's feature | Butterfly Joust |
| --- | --- |
| Height wins; three tiers; hatching eggs | Kept, plus ten more riders |
| A mount collects hatched riders | The Carrier |
| Announced wave types | Seven wave types, each with its bonus |
| The hand from the lava | The Pond Frog and its cousins |
| The arena changes | Five arenas with folding, drifting, swaying, icy and moonlit ledges |
| A predator with a precise weak spot | The Thundercap and Old Thunderhead's eye |
| Two players, co-op or rivals | 2–4 players, co-op and versus |
| **Past the classic** | Air Combo, Charge Joust, thermals and wind, six champions, an ending |

#### Slices

Roadmap: t-047 (slice 1), t-048 (slice 2), t-049 (slice 3), t-050 (slice 4). Slice 1 is `ready`; each later slice waits on the one before.


1. **Party and pond.** Two to four riders through the `players` frames, with co-op (the team bonus) and Last Butterfly
   Flapping versus; announced wave types (Survival, Gladiator, Cocoon, Storm, Team); the Pond Frog with its tell and
   the flap-to-escape; the Carrier; Air Combo and Charge Joust; and the Thundercap's eye check. Deterministic tests
   cover combo scoring, frog escape and the team bonus, and a pilot probe shows runs still end.
2. **Arena engine, Sunset Pond and Spring Meadow.** Ledge layouts as data, with moving, folding and one-use ledges,
   thermals and wind; save/resume at arena start; Sunset Pond retuned and Spring Meadow (flower ledges, dandelion
   puffs, thermals) with their own backdrops and music; the glider, twin riders and pollen bomber; Sir Bumbleton and
   the Dandelion Duchess; and the Wing Garden.
3. **Heights, Orchard, Snowfield and the Moon Garden.** Thunderhead Heights (drifting clouds, lightning, rain), Autumn
   Orchard (sway, apples, leaf piles) and Lantern Snowfield (ice, lanterns, a cracking pond); the diver, lancer, shield
   beetle and frost moth; Old Thunderhead, the Scarecrow Kite, the Frost Moth Queen and the Mirror Moth; the Gauntlet;
   credits, the golden petals, the Rainbow Lists and the true ending; and Champion's Circuit New Game+.
4. **Medals and the endless pond.** Endless Pond as the leaderboard event, Classic Pond, and the medals with a board per
   arena. Registry `maxPlayers` and the blurb and how-to lines are updated.

---

## 5. Kindness Gauntlet (Gauntlet II riff)


### What is in the game today

| Area | Today |
| --- | --- |
| Floors | Endless and procedural. Each floor carves up to 9 random rooms out of a 40 × 30-tile map, joins each room to the last by a two-wide corridor, and puts the stairs in the room farthest from the start. Four wall tints cycle by floor. The map is dark until explored. |
| Classes | **Four, with real differences**: Hugs (power: double damage to generators, sparks pass through a glitch), Fix (armour), Sage (magic: three pulses that also hit generators) and Zip (speed). This is the strongest part of the game. |
| Enemies | **One**: the glitch. It homes on the nearest bot within 14 tiles and clings on, draining charge. There is **one** generator kind (3 → 6 hp), which releases a glitch every 150 → 50 ticks while a bot is near, up to 10 → 26 glitches on the floor. |
| Items | Snacks (+40 charge), a pulse (+1 kindness pulse, which clears the screen), cages (a rescued bot is worth points and nothing more), and from floor 2 one key for one locked door, when the floor has a corridor the door can cut cleanly. |
| Battery | 300, draining a point every 45 ticks. Clinging glitches drain 3 → 9 per bite, scaled by the class's armour. |
| Co-op | Up to 4 bots on one screen with a leash. Keys and score are shared. Rolling up to a flat partner shares a charge with them, and a flat bot comes back on the next floor with a quarter charge. |
| Difficulty | Cages max out at floor 5, generators at 7, glitch count and generator hp at 9, the spawn rate at 10, glitch speed at 12 and cling damage at 13. **From floor 13 on, every floor is the same floor.** |
| Structure | No bosses, no traps or maze tricks, no treasure rooms, no choice of exits, no authored floors, no secrets and no ending. Scoring is 10 per glitch, 100 × floor per generator, 250 × floor per rescue, 100 per door and 500 + 100 × floor per floor cleared. No saves, no music. |
| Code | `kindnessGauntlet.ts`, 2,731 lines, the largest of this batch. The seed-5 attract pilot was still going on floor 8 after 4½ minutes. The single enemy type barely threatens it. |

The screenshots show server racks with vents, drive bays and cable runs that read well. But floor 1 and floor 8 differ only in wall tint, the bots are about 14 px, and the only moving threat is one glitch sprite.

### Against the classic

The 1986 sequel is a menagerie inside a trick box:

- **A dozen monster kinds, each asking for a different answer:**
  - ghosts that ram you;
  - melee grunts;
  - fireball-throwing demons;
  - lobbers that throw over walls;
  - sorcerers that blink invisible;
  - an unkillable reaper-like drainer that only a magic potion stops;
  - a **thief** who steals and runs;
  - a **mugger** who steals health;
  - **acid puddles** that can't be destroyed;
  - **teleporting super-sorcerers**;
  - **dragons** that take many hits.
- **Generators in three tiers** for each monster kind.
- **A tag curse**: whoever is "it" draws every monster on the floor until they pass it on.
- **Maze tricks:**
  - walls that reflect shots;
  - walls that are invisible, that appear and vanish, or that can be shot away;
  - stun tiles, force fields, transporters and trap tiles;
  - fake exits, and exits that skip several floors.
- **Treasure rooms** you must loot against a timer, and a **secret trick on each level**, hinted on screen, that pays a bonus.
- **Amulets** (invisibility, invulnerability, repulsion, transportability, reflecting shots, super shots) and **potions that permanently improve** armour, magic, speed, shot power and shot speed.
- **Food you can destroy by accident**, and an **announcer** who comments on everything: who is low on health, who shot the food.
- **More than a hundred mazes,** then random ones.

Kindness Gauntlet already matches the four distinct classes, four-player co-op, health draining over time, food, keys, doors and generators.

**Verdict:** it is structurally the closest of the six to its classic and the only one with true four-player co-op, but its dungeon is one enemy chasing you through random rooms. It has none of the monsters, maze tricks, treasure, amulets or announcer that made the sequel what it was, and the attract pilot strolled through eight floors untouched.

### The upgrade: Kindness Gauntlet — The Deep Archive

Below the server floors lies the **Deep Archive**: the memory of the **Old Mainframe**, a kindly machine that ran the city for decades and has begun to forget itself. Each of its five wings is a different era of computing, with its own glitches, tricks and Guardian. The bots go down to fix her memories.

There are two signature twists:

- **Kindness is a mechanic.**
  - A spark that hits a partner **shares charge** with them instead of hurting them.
  - The classic's tag curse becomes the **Hug Token**, which draws every glitch on the floor to whoever holds it. Pass it to a partner by touch, or carry it into a generator to overload it.
- **Big glitches turn helper.** A strong enemy you fix doesn't vanish: it follows you for a short while as a helper drone that sparks alongside you.

**Target length:** a first clear in roughly 60–80 minutes.

#### Structure

- The Archive has **five wings** (acts), each of:
  - **six authored floors**;
  - a **Lost & Found** treasure floor;
  - a **Guardian** (boss).
  - Floor 5 of each wing ends at a **Big Bluescreen** mid-boss.
- Floors are authored data: walls, tricks, generators, items, exits, the floor's **note** (its hinted secret), and a par time. That makes 30 hand-built floors; the procedural builder stays for Endless mode with the full trick set.
- **Some floors have several stairs**: an ordinary one, and an **express lift** that skips two floors at the price of missing those floors' treasure.
- **The Mainframe's voice** (the announcer, below) comments throughout.
- Progress saves at each wing through `utils/arcade/saves.ts`. A clear rolls credits and unlocks **Reboot**, a New Game+.

#### The wings

| # | Wing | Floor tricks | New glitches | Guardian |
| --- | --- | --- | --- | --- |
| 1 | **The Punch-Card Vault** (beige cabinets, card feeders) | Today's keys and doors; **card walls** that sparks break; **static mats** (stun tiles); express lifts | Static brute, Pop-up, Pickpocket | **The Card Sorter** |
| 2 | **The Tape Library** (reel-to-reel stacks) | **Mirror racks** that bounce sparks; **sticky tape** floors that slow; **sliding shelves** on a timer; **patch-cable transporters** | Firewall imp, Coffee spill, Worm | **The Twin Reels** |
| 3 | **The Arcade Basement** (old cabinets) | **Dark cabinets**, invisible except in a pulse's light; **fake stairs**; **dance-floor tiles** that stun when lit on the beat | Blinker, Mimic snack, Bug swarm | **The Attract Mode** |
| 4 | **The Cloud Atrium** (soft white servers under a skylight) | **Wind vents** that push bots; **cloud tiles** that vanish and reform; **trap tiles** that remove a wall somewhere | Leech, Pop-up wizard | **The Cloud Bank** |
| 5 | **The Core** | **Firewall gates** on the beat; **defrag floors** whose sections slide and swap; every earlier trick remixed | Sleepy Cursor, and all the others | **The Old Mainframe** |

Each wing hides one **Memory Card** behind its hardest floor secret. With all five, the finale's ending changes (below).

#### The roster: 1 → 14 glitches

| Glitch | Behaviour | Tell | Answer |
| --- | --- | --- | --- |
| **Glitch** | As today: homes and clings | — | Spark it |
| **Static brute** | Melee, 3 hp, shoves you back a tile | Stomps | Keep your distance; Hugs' sparks pierce |
| **Pop-up** | Lobs packets over racks | Winds up with a "!" | Get into its room; it can't lob at close range |
| **Firewall imp** | Fires slow sparks in straight lines | An inhale glow | Move diagonally |
| **Blinker** | Invisible except for one frame each beat | A flicker | A pulse reveals it, and Sage's pulse also stuns |
| **Sleepy Cursor** | Can't be sparked; drains charge fast on contact; drifts toward the fullest battery | A spinning hourglass | Only a kindness pulse puts it to sleep, for big points; otherwise outrun it |
| **Pickpocket** | Steals a key or a pulse and runs for the stairs | A sly grin | Spark it before it leaves and it drops the loot |
| **Leech** | Steals charge and runs | A battery icon on its back | Spark it to get the charge back |
| **Coffee spill** | A puddle that can't be destroyed, sliding along corridors | Ripples | Avoid it; a pulse dries it for 5 seconds |
| **Pop-up wizard** | Teleports and fires three ways | Sparkles where it will appear | Spark the sparkle |
| **Worm** | Segmented; a hit mid-body splits it into small glitches | A segmented trail | Spark the head |
| **Bug swarm** | Ten tiny, fast glitches | Buzzing | A pulse, Hugs' piercing sparks or Zip's fast ones |
| **Mimic snack** | Looks like a snack and bites | Blinks | Spark it and it becomes a real snack |
| **Big Bluescreen** (mid-boss, floor 5 of each wing) | Huge; takes many hits; breathes static in a cone | Fills with blue | Circle round it; it's best with every bot sparking at once |

Every glitch kind has its own generator (card feeder, tape reel, cabinet, router), each in **three tiers** as in the classic. A tier-3 generator releases the toughest version, and every hit drops it a tier.

#### The Guardians: 0 → 5 bosses

1. **The Card Sorter:** a great machine that deals walls.
   - **Phase 1:** it shuffles the rack walls into new rows on a whistle. Find the gap.
   - **Phase 2:** it fires fans of punch cards.
   - **Phase 3:** it jams. Spark its card slot while the walls are still.
2. **The Twin Reels:** two tape reels joined by a tape that sweeps the room like a moving wall.
   - **Phase 1:** the tape sweeps. Ride the gaps.
   - **Phase 2:** the reels spin apart and the tape tightens across the room. Each reel is fought separately, which suits a split co-op team.
   - **Phase 3:** the tape snaps and whips. Spark both reels within 3 seconds of each other.
3. **The Attract Mode:** a giant cabinet in the basement playing a demo of the earlier floors.
   - **Phase 1:** its screen projects ghost copies of earlier glitches.
   - **Phase 2:** it "plays" you: its pilot moves the floor's walls in demo patterns.
   - **Phase 3:** its game-over screen counts down. The bots stand on its four coin slots to continue (solo, each slot holds for 6 seconds), and the cabinet turns friendly.
4. **The Cloud Bank:** a fluffy cloud of servers that rains glitch drops.
   - **Phase 1:** drops fall, each on a tell.
   - **Phase 2:** wind pushes the bots toward the vents.
   - **Phase 3:** lightning chases whoever holds the Hug Token. Use the Token to steer the lightning back into the Bank.
5. **The Old Mainframe** (finale): a wall of tape drives with a face.
   - **Phase 1, memory recall:** the four earlier Guardians return one at a time at half strength.
   - **Phase 2, defrag:** the floor's sections slide and swap.
   - **Phase 3, reboot:** hold four terminals while her boot bar fills. In co-op that's one bot per terminal; solo, each terminal holds for 6 seconds after you touch it.

   She wakes up herself again and thanks the bots. With all five Memory Cards, she remembers everything: the old staff photos, the city she ran and her first boot. That is the true ending.

#### Systems that run through the whole descent

- **The Mainframe's voice:** an announcer portrait at the screen's edge with short, original bleep-speak lines (WebAudio pitch patterns, no speech synthesis, no runtime LLM). For example:
  - "ZIP IS RUNNING LOW"
  - "DON'T SPARK THE SNACKS"
  - "HUGS HAS THE TOKEN"
  - "A KEY IS NEAR"
  - "SAGE FOUND A SECRET"
- **Snacks can be sparked by accident,** as in the classic, and the Mainframe will tell you off.
- **Spark-to-share:** a spark that hits a partner moves 5 charge from you to them, never damage.
- **The Hug Token:** a bouncing heart.
  - Whoever holds it draws every glitch on the floor and earns double points for every glitch fixed.
  - Pass it to a partner by touch.
  - In solo play, carry it into a generator to overload it.
- **Helpers:** a fixed brute, imp or wizard follows the bot that fixed it for 20 seconds as a helper drone.
- **Charms** (timed, 20 seconds), the classic's amulets:
  - **Ghost:** glitches lose track of you.
  - **Shell:** clinging glitches drain nothing.
  - **Shoo:** glitches flee.
  - **Hop:** walk through one rack.
  - **Mirror:** sparks bounce off racks.
  - **Mega:** sparks pierce everything.
- **Chips,** the classic's upgrade potions: permanent for the run, one class stat each (spark power, speed, armour, spark range, pulse power, spark speed).
- **Treasure:** keepsakes (floppies, gold chips) for score, and a **Lost & Found** floor in each wing with 30 seconds to grab them.
- **Floor notes:** each floor's hint names its secret ("find the hidden pulse", "leave by the far stairs"). Solving it pays a bonus and, on one floor per wing, the Memory Card.
- **Scores per seat:** the team score stays, and each seat's own score shows on the floor-clear and game-over screens.
- **Five wing tilesets** instead of four tints, a distinct sprite for every glitch, and large animated Guardians.
- **Music:** one loop per wing.

#### Modes and players

Up to four players (`maxPlayers: 4`, as today).

- **Descent:** the campaign, 1–4 players.
- **Endless Archive:** random floors with the full roster and every trick, getting harder as you go deeper. This is the leaderboard's main event.
- **Lost & Found:** a treasure-floor score attack.
- **Score Duel:** an option on any mode that ranks the seats' own scores at the end.

#### The classic's signatures, matched or beaten

- **Four distinct heroes and four-player co-op:** already matched.
- **Health draining over time, food, keys, doors and generators:** already matched. Generator tiers are now matched too.
- **The monster roster:**
  - **the unkillable drainer:** matched by the Sleepy Cursor;
  - **the thief and the mugger:** matched by the Pickpocket and the Leech;
  - **acid:** matched by the Coffee spill;
  - **super-sorcerers:** matched by the Pop-up wizard;
  - **dragons:** matched by the Big Bluescreen.
- **The tag curse:** matched and turned kind by the Hug Token.
- **Maze tricks, treasure rooms, floor secrets and exits that skip floors:** matched.
- **Amulets and potions:** matched by charms and chips.
- **The announcer:** matched by the Mainframe's voice.
- **Authored mazes:** 30 floors against the classic's hundred-plus. This is short on count, made up for by the Guardians.
- **Beyond the classic:**
  - five Guardians with phases (the classic has no true bosses);
  - spark-to-share;
  - helpers;
  - the Memory Card ending.

#### Slices

Roadmap: t-051 (slice 1), t-052 (slice 2), t-053 (slice 3), t-054 (slice 4). Slice 1 is `ready`; each later slice waits on the one before.


| Slice | Scope |
| --- | --- |
| 1 | Eight new glitches, three generator tiers, the Mainframe's voice, sparkable snacks, spark-to-share, the Hug Token, seat scores |
| 2 | Authored floor format and maze tricks, the Vault and the Tape Library (12 floors + 2 Lost & Found), the Worm, Big Bluescreen, the Card Sorter and Twin Reels, charms and chips, save/resume |
| 3 | The Arcade Basement and the Cloud Atrium, Blinker and Pop-up wizard, helpers, the Attract Mode and the Cloud Bank, Memory Cards |
| 4 | The Core, the Old Mainframe, endings, Reboot, Endless Archive, Lost & Found mode, Score Duel, medals |

- **Slice 1, a menagerie.**
  - **Delivers:**
    - Eight glitch kinds, each with its own sprite, tell and steering: Static brute, Pop-up, Firewall imp, Pickpocket, Leech, Coffee spill, Bug swarm and Mimic snack.
    - Their generators, each in three tiers.
    - The Mainframe's announcer panel with its bleep-speak lines.
    - Snacks that sparks can destroy.
    - Spark-to-share between partners.
    - The Hug Token.
    - Seat scores alongside the team score.
    - Retuned battery drain and spawn rates, so that the attract pilot no longer clears eight floors untouched.
  - **Verified by:** a new `verifyKindnessGauntlet.test.ts` in `test:arcade-engine` covering each glitch's answer, plus the existing co-op tests.
- **Slice 2, the first two wings.**
  - **Delivers:**
    - An authored floor format in `utils/arcade/kindnessGauntlet/`.
    - The maze tricks: card walls, static mats, mirror racks, sticky tape, sliding shelves, transporters and express lifts.
    - The Punch-Card Vault and the Tape Library: twelve floors and two Lost & Found floors, with their own tilesets.
    - The Worm, which the Tape Library introduces.
    - The Big Bluescreen mid-boss.
    - The Card Sorter and the Twin Reels.
    - The six charms and six chips.
    - Floor notes and their secrets.
    - Save and resume per wing through `saves.ts`.
  - **Verified by:** a scripted clear of the Vault and screenshots of each floor.
- **Slice 3, the middle wings.**
  - **Delivers:**
    - The Arcade Basement and the Cloud Atrium: twelve floors and two Lost & Found floors, with dark cabinets, fake stairs, dance tiles, wind vents, cloud tiles and trap tiles.
    - The Blinker and the Pop-up wizard.
    - Fixed-glitch helpers.
    - The Attract Mode and the Cloud Bank.
    - The Memory Card secrets.
  - **Verified by:** boss-phase tests.
- **Slice 4, the Core and the modes.**
  - **Delivers:**
    - The Core's six floors, with firewall gates and defrag floors.
    - The Sleepy Cursor.
    - The Old Mainframe finale with its four-terminal reboot.
    - The standard and Memory Card endings, and Reboot (New Game+).
    - Endless Archive on the procedural builder with every trick, as the leaderboard mode.
    - Lost & Found mode.
    - The Score Duel option.
    - The per-floor medal board.
  - **Verified by:** a scripted full-campaign test.

---

## 6. Butterfly Blaster (Asteroids riff)


### What is in the game today

| Area | Today |
| --- | --- |
| Structure | Endless waves on **one** wrapping night sky (480 × 360). A wave spawns 4–11 big swarms on the edges. Clear them all and a village is "safe", then the next wave starts. |
| Enemies | **Two.** The mosquito swarm comes in three sizes: a big one splits into two medium, a medium into two singles (20 / 50 / 100 points). The malaria cloud arrives from wave 3: it crosses the sky firing aimed drops and is worth 200. From wave 6 there is also a small cloud, twice as accurate and worth 1,000. |
| Enemy behaviour | Swarms fly in a straight line at a fixed speed until they are hit. They never steer, flock or chase, and they react to neither the player nor each other. The cloud arrives on a timer, whatever the player is doing. |
| Hazards | None beyond the swarms and the cloud's drops. |
| Power-ups | **One.** AMI flies over on a timer and drops a bed net, a one-hit shield for 8 s (250 points). |
| Moves | Turn, flutter (thrust with drift), sparkle (5 shots on screen) and hop (a teleport to a random spot with a 1 s cooldown and no risk). |
| Scoring | Flat points per kill, with no chain, multiplier or wave bonus. An extra butterfly every 10,000. |
| Difficulty | The big-swarm count maxes out (11) at wave 8. The cloud's fire rate and aim stop rising at wave 10, its frequency at wave 11, AMI's interval at wave 12 and swarm speed at wave 13. **From wave 13 on, every wave is the same wave.** |
| Visual variety | One backdrop: a moonlit savanna village with eight huts. The only change across a run is one more lit window per wave cleared. A single mosquito is a 15 × 8 sprite and the butterfly is about 22 px across on a 480-wide field, so on a phone a swarm reads as specks. |
| The cause | AMI, the bed nets and the villages carry the malaria-project theme, but the villages are only a counter: nothing ever threatens a hut. |
| Players, saves, ending | Solo, with no save and no ending. |
| Scale | `butterflyBlaster.ts`, 1,572 lines. Four minutes into the attract demo, the pilot had lost every butterfly on wave 5. |

### Against the classic

The 1979 vector game is famously lean, but every part of it pulls on the player:

- **Rocks in three sizes** that split, with more of them each wave.
- **Two saucers with different jobs.** The big one fires at random. The small one aims, and it turns up more often as the
  score climbs, so success itself raises the danger. Saucer shots break rocks too.
- **Anti-lurking:** hang back sniping the last rock and the small saucer comes sooner and aims better.
- **Hyperspace with a real risk:** an escape that can drop you into trouble.
- **A heartbeat** that speeds up as the wave thins, tension you can hear.
- **Momentum mastery:** thrust, drift and wrap are the skill.
- **Two players** taking turns.
- Its 1981 deluxe follow-up added a **shield that drains**, rocks that **hunt you**, and a **spinning cluster of
  wedges** that breaks into hunters when it is shot.

**Verdict:** Butterfly Blaster is the 1979 ruleset in a lovely coat of paint. The three-size swarms are the rocks, the
cloud is the saucer, the hop is hyperspace, and even the 10,000-point extra life is the same. It is missing the
anti-lurk, the score-driven saucer and the heartbeat, its swarms behave like rocks rather than insects, nothing new
appears after wave 6 and nothing changes after wave 13. Worst of all, its premise (AMI, bed nets, villages to protect)
is the strongest theme in the arcade and is used only as a lit-window counter. It is a thin veneer.

### The upgrade: Butterfly Blaster — The Rainy Season

The rains are coming, and every village down the river needs the night watch. Butterfly Blaster becomes a
**season-long flight** down a river valley:

- each night defends a real village;
- the mosquitoes behave like mosquitoes: they flock to light and breed in standing water;
- the butterfly gets a signature move, the **Rainbow Lasso**, which turns the classic's lone sniping into sweeping,
  chaining flight.

**Target length:** a first clear in roughly 45–60 minutes.

#### Structure

- The season has **three Moons** (acts) of **two regions** each, a **nest boss** at the end of each Moon, and a
  **secret seventh region**.
- Each region has **four nights**, and each night is two waves and a **dawn tally**:
  - nights 1–2 introduce the region's new pests and sky mechanic;
  - night 3 is the region's **special night**, with its own objective;
  - night 4 remixes the region with everything learned so far.
- A **river map** between nights shows the villages along the route, each with its health, and a festival lantern on
  every village that came through a night unbitten.
- Each region has its own backdrop, ground line, palette, music loop and title card.
- **The Clinic** opens between regions (below).
- Progress saves at each region start through `utils/arcade/saves.ts`.
- A clear rolls credits and unlocks **Dry Season**, a New Game+ with remixed nights.

#### The regions

**Moon 1: First Rains**

| # | Region | Sky and mechanic | New pests | Special night |
| --- | --- | --- | --- | --- |
| 1 | **Riverbend** | Today's moonlit savanna and village. Swarms now flock toward lit huts. | Swarm (three sizes), malaria cloud | **Lantern Walk**: villagers carry eight lanterns along the riverbank. The swarms flock to them; keep at least five unbitten. |
| 2 | **Rice Terraces** | Stepped paddies along the ground line. **Standing-water pools** glint and breed larvae. Wind gusts push everything sideways on a flag tell. | **Wriggler** (a larva rises from a pool and hatches into a small swarm unless it is sparkled at the surface), **Skimmer** (skates along the waterline) | **Tip the Pots**: sparkle six water jars to tip them. Every jar tipped dries a pool and shuts its hatchery. |

**Boss 1: The Hum.** A mega-swarm the size of a cloud that holds shapes: a ring, a spiral, a grinning face.
- **Phase 1:** shoot gaps in its outer orbit to reach the core.
- **Phase 2:** it splits into four sub-swarms that circle whichever hut the butterfly is nearest.
- **Phase 3:** the core, a fat swarm-in-training, bolts in straight dashes on a rising-buzz tell. Lasso it.

**Moon 2: Heavy Rains**

| # | Region | Sky and mechanic | New pests | Special night |
| --- | --- | --- | --- | --- |
| 3 | **Mangrove Delta** | The **tide** rises and falls, moving the ground line and shrinking the sky. **Fog banks** hide swarms; fireflies light pools of fog. | **Shade swarm** (invisible except in firefly light or a lightning flash), **Needle** (stops, glows red for half a second, then dashes straight across the wrap) | **Firefly Escort**: guide a drifting firefly cloud across the delta; the fog only lifts where it shines. |
| 4 | **Market Town** | **Strings of festival lights** cross the sky and the swarms flock to the lit bulbs. Sparkle a bulb string to dim it and send the flock elsewhere. | **Bloom cluster** (a spinning hexagon of six petals; break it and it scatters into six hummers), **Hummer** (small, slow, never stops homing) | **Night Market**: the stall lights blink on in sequence. Defend whichever stall is lit: a moving defend point. |

**Boss 2: Old Puddle.** A living overflow from the town's rain barrel, spreading along the ground.
- **Phase 1:** lily pads rotate over its three spawn mouths. Sparkle the mouths between the pads.
- **Phase 2:** it rains. Every drop that lands becomes a new mini-pool, and wrigglers rise from them.
- **Phase 3:** it rears up as a water spout and sweeps the sky. Drop AMI's lantern lure to pull it into the first
  sunbeam of dawn, which dries it out.

**Moon 3: Last Rains**

| # | Region | Sky and mechanic | New pests | Special night |
| --- | --- | --- | --- | --- |
| 5 | **Tea Hills Storm** | A thunderstorm. **Lightning** lights the whole sky on a beat and strikes ground spots after a 1 s glow tell. **Rain** soaks the wings, so the butterfly drifts heavier until a rainbow updraft dries it. | **Storm cell** (a small dark cloud that crackles over a column, then drops a lightning line down it), **Sticky swarm** (its hits stick to the wings and slow your turning until you hop) | **Hold the Hill**: the tea pickers' shelter at the summit must stay unbitten through a storm that only builds. |
| 6 | **The Great Swamp** | The source of it all: reeds, low mist and breeding pools everywhere, with the river's last village on the far bank. Every pest returns in a remix. | **Decoy glow** (it looks like AMI's falling net but blinks twice; catch it and it bursts into hummers) | **Long Night**: the longest night of the season, in three waves, with no dawn tally until all three are done. |

**Finale: The Night Queen.** A giant mosquito matriarch, the cartoon queen of the swamp.
- **Phase 1:** she circles the sky dropping egg rafts on the pools. Sparkle the rafts before they hatch.
- **Phase 2:** her wings fan gusts that push every sparkle sideways, so you lead your aim into the wind.
- **Phase 3:** she dives at the village. AMI arrives with every ally (bats, dragonflies, swallows), and the player draws
  one sky-wide rainbow lasso around her.
- **Dawn:** the sun rises on the dry season and every village waves its lanterns.

**Secret region: The Moonlit Lagoon.** Each region hides one **golden net thread**, earned by finishing its special
night with no hut bitten.
- With all six, a seventh region opens: mirrored skies, every pest at full speed, and coins of moonlight everywhere.
- Clearing it gives the **true ending, Zero Night**: a festival for a whole season in which nobody was bitten.

#### The roster: 2 → 11 pests, 3 bosses

| Pest | Tell | Answer |
| --- | --- | --- |
| Swarm (big, medium, single) | Hums toward light; splits when sparkled; left alone, the pieces regroup | Shoot from range, or lasso the whole flock |
| Malaria cloud (big and small) | Warning tone, enters from the side | Pop it early; the small one aims true, so keep moving |
| Wriggler | A ripple on a pool, then a larva rises | Sparkle it at the surface before it hatches |
| Skimmer | Skates along the ground line, throwing a spray | Shoot low, or dash over it |
| Shade swarm | Invisible outside firefly or lightning light | Fly near the fireflies; wait for the flash |
| Needle | Stops and glows red for half a second | Sidestep across its line |
| Bloom cluster | A spinning hexagon of six petals | Break it at range, then lasso the six hummers |
| Hummer | Small, slow, always homing | Lead it into a loop |
| Storm cell | Darkens and crackles over one column | Leave the column |
| Sticky swarm | A dull, heavy hum | Hit it at range, or hop to shake it off |
| Decoy glow | Looks like a falling net but blinks twice | Read the blink |

Hazards: wind gusts, the tide, fog, lightning and rain. Bosses: the Hum, Old Puddle and the Night Queen.

#### Systems that run through the whole season

- **The Rainbow Lasso (the signature):**
  - the flutter trail is a rainbow ribbon about 1.5 s long;
  - cross your own ribbon to close a loop, and every mosquito inside is netted at once (a big swarm counts as its
    whole split tree);
  - it pays 100 per mosquito × the loop's count multiplier, so it is the best way to clear a flock and the natural
    answer to lurking.
- **Living swarms:** swarms flock (boids) toward lit huts, lanterns and the butterfly's own glow. Split pieces scatter,
  then regroup, so a swarm split and left alone merges back.
- **Village health:** each hut can take three bites. A swarm that reaches a lit hut bites it and its window flickers.
  The **dawn tally** pays for every unbitten hut.
- **Breeding pools:** standing water on the ground spawns wrigglers until it is dried. It is the real-world lesson,
  removing standing water, taught by play rather than a lecture.
- **The heartbeat:** a music loop, through the engine's `music`, whose tempo rises as the swarms thin. The last mosquito
  of a night **sprints**.
- **Anti-lurk:** idle near an edge for 8 s and the malaria cloud comes early and aims tighter, as in the classic. The
  small cloud's frequency also rises with score.
- **The hop with a choice:**
  - tap B for a **flutter-dash**, a short aimed blink with a 1 s cooldown;
  - hold B for the classic random **long hop**, which keeps the risk. Land within 40 px of a swarm and survive 2 s for a
    **Brave Hop** bonus.
- **Chains:** sparkles within a second of each other chain ×2, ×3, ×4, shown as a growing floater.
- **AMI's kit:** power-ups AMI drops, each short and shown in the HUD.
  - **Bed Net:** today's shield.
  - **Repellent Ring:** orbiting citronella sparkles.
  - **Spray Fan:** three-way sparkle.
  - **Dragonfly Wingman:** an ally that hunts singles.
  - **Bat Squadron:** one sweep across the sky that gobbles singles. The natural predators are the cavalry.
  - **Lantern Lure:** a decoy that clusters swarms for a lasso.
  - **Long Sparkle:** +60% range.
- **The Clinic** between regions: spend **thank-you beads** (dropped by villages at the dawn tally, never real money)
  on an extra butterfly, a longer ribbon, a quicker dash, a starting net, a sturdier net (two hits) or a hint that shows
  where the region's golden thread is. Prices rise each Moon.
- **Medals per night:** Not a Bite (no hut bitten), Lasso Master (20 or more in one loop) and Swift Night (under par).
- **Bigger actors:** draw the swarm and the butterfly at double density (a single mosquito about 24 px across), with
  three flap frames per pest and a telegraph animation for every boss.

#### Modes

- **Season:** the campaign.
- **Long Night:** endless waves with every pest mixed in, the leaderboard's main event.
- **Co-op Flight:** 2–4 butterflies through the cabinet's `players` frames. When two players' ribbons cross they
  close a shared loop, a **team lasso** worth double.
- **Region Time Attack:** unlocked per region on a clear.
- **Classic Night:** today's rules on today's sky, kept as a tribute mode.

#### Signature features to match or beat

| The classic's feature | Butterfly Blaster |
| --- | --- |
| Three-size splitting rocks | Kept; the swarms now flock, and they merge back if left alone |
| Two saucers, the small one aimed and more frequent with score | The malaria cloud pair, with the small one tied to score, plus storm cells |
| Anti-lurking | Explicit, with the last-mosquito sprint |
| Risky hyperspace | The long hop keeps the risk; the flutter-dash adds control |
| The heartbeat | Music tempo tied to the swarms left |
| The draining shield (deluxe) | The bed net and its durability upgrade |
| The wedge cluster that splits into hunters (deluxe) | The bloom cluster and its hummers |
| Two players | Simultaneous co-op with the team lasso |
| **Past the classic** | The Rainbow Lasso, village defence, breeding pools, six regions, three bosses, a real ending |

#### Slices

Roadmap: t-055 (slice 1), t-056 (slice 2), t-057 (slice 3), t-058 (slice 4). Slice 1 is `ready`; each later slice waits on the one before.


1. **Flight and the living swarm.** Rebuild the core so every later slice stands on it: double-density sprites for the
   butterfly and the swarms; swarms as flocking boids drawn to light, with regrouping; the Rainbow Lasso (ribbon trail,
   loop detection and netting of a swarm's whole split tree); chains; the anti-lurk rule and a score-tied small cloud;
   the flutter-dash and the risky long hop; a heartbeat music loop that speeds up as the wave thins, with a
   last-mosquito sprint; village health with bites and the dawn tally; and the first new pests (wriggler, skimmer,
   needle) with breeding pools on the ground. Deterministic tests cover lasso netting, regroup and hut bites, and a
   pilot probe shows runs still end.
2. **Moon 1, the river map and the Clinic.** The season engine: regions, nights and special nights as data; the river
   map between nights; save/resume at region start; the Riverbend and Rice Terraces regions with their own backdrops,
   palettes and music; the Lantern Walk and Tip the Pots special nights; AMI's kit (repellent ring, spray fan, dragonfly
   wingman, lantern lure, long sparkle); the Clinic with thank-you beads; and the first boss, the Hum, in three phases.
3. **Moons 2 and 3, the bosses and the endings.** The Mangrove Delta (tide and fog), Market Town (festival lights) and
   Tea Hills Storm (lightning and rain) regions, then the Great Swamp, each with its special night; the shade swarm,
   bloom cluster and hummers, storm cell, sticky swarm and decoy glow; the bat squadron; Old Puddle and the Night Queen
   with their phases; the dawn ending and credits; the six golden threads, the Moonlit Lagoon and the Zero Night true
   ending; and Dry Season New Game+.
4. **Together and forever.** Co-op Flight for 2–4 players through the `players` frames, with the team lasso and shared
   village health; the Long Night endless mode as the leaderboard event; Region Time Attack; Classic Night; and the
   three medals per night with a medal board per region. Registry `maxPlayers` and the blurb and how-to lines are
   updated.

---

## 7. Bumper Bubbles (Bubble Bobble riff)


### What is in the game today

`bumperBubbles.ts`, 1,330 lines. Registry entry: 256 x 240, solo, no mastery ladder.

| Area | Today |
| --- | --- |
| Rounds | Endless, but there are only **four platform layouts and four backdrop themes**, both picked by (round − 1) mod 4. Round 5 is round 1. **The round-13 screenshot is round 1, platform for platform and star for star.** |
| Enemies | **Five colours with four behaviours.** Green and red are identical walkers. Gold hops twice as often. Blue walks 1.25x faster. Pink hops toward the player when the player is above it. **All are walkers** on the same physics: nothing flies, floats, shoots, throws or passes through walls. |
| Bubble rules | A shot flies for 26 ticks, then rises. It traps any gremlin it touches and holds it for 520 → 240 ticks; a gremlin that bursts free comes out angry (1.5x speed). **You can't ride bubbles.** Popping one bubble pops only that one: **no cluster pops**. There is **no screen wrap**. |
| Hurry | At 30 s every gremlin turns angry. There is no invincible chaser. |
| Items | Gems only (300 each). There are **no special bubbles, no letter bubbles, no food or power-up items, and no secret rooms**. |
| Scoring | A pop is worth 200 x chain (max x4, inside 70 ticks), a gem 300, an empty bubble 10. A clear under 25 s pays 1,000 x round. An extra life every 25,000. |
| Difficulty | Gremlins 3 → 9 (capped at round 7), all five colours by round 8, hop rate capped at round 9, hold time at round 11, speed at round 14. **From round 14 on, every round is the same round.** |
| Bosses, players, ending, saves | None; solo; none; none. |

### Against the classic

Silas named the 1986 classic's depth himself: 100 levels, two-player co-op, secret rooms, special items and multiple endings. Specifically:

- **100 hand-built levels**, each a distinct shape (many draw pictures or letters), each with its own **air currents** that steer floating bubbles. There are **secret rooms** you can only reach under hidden conditions.
- **Two players at once**, and **the true ending requires two players** to finish the last level together. There are **multiple endings**.
- **An enemy roster of distinct behaviours**: walkers, jumpers, a diagonal flyer that ricochets off walls, a rock thrower, a fire or laser shooter, a ghost that floats through platforms, a fast dasher, and the **invincible hurry-up chaser** that comes for players who dawdle.
- **Bubbles are platforms**: bouncing on them to climb is half the movement game.
- **Popping a trapped enemy pops every touching bubble.** Multi-kills drop escalating treats (1,000 → 2,000 → 4,000 … up to 64,000 for seven at once).
- **Special bubbles**: water (a wave that washes enemies down the level), fire (flames along the floor) and lightning (a horizontal bolt that also hurts the final boss). **Letter bubbles** spell out an extra-life word.
- **Dozens of items with hidden trigger conditions** (jump a set number of times, pop a set number of bubbles, and so on): speed shoes, sweets that improve your bubbles, umbrellas that skip three, five or seven levels, a potion that fills the screen with bonus treats, and more.
- **Screen wrap**: fall through the floor and come out at the top.
- **A final boss** on the last level.

**Verdict:** Bumper Bubbles is a handsome single round of the classic: the bubble film, the trapped gremlin, the chain and the hurry. But it is four boards on repeat (round 13 is round 1, frame for frame) with five colours sharing four walking behaviours. It has:

- no bubble riding, cluster pops or air currents;
- no special bubbles, letters or items;
- no wrap, secret rooms, bosses, co-op or ending.

Against the game Silas named for its 100 levels, co-op, secret rooms, items and endings, this is the thinnest of the six.

### The upgrade: Bumper Bubbles — The Hundred Floors of Fizzwick Tower

**Fizzwick Tower** is a hundred-floor soda works. Its great Carbonator has broken, everything inside has gone flat and grumpy, and the gremlins are fizzed-up grumps. The bubble robots climb all hundred floors, popping every grump into a cheerful treat and gathering the five lost recipe cards, to reach the top and restart the Carbonator. The classic's whole shape is matched: a hundred levels, two-player co-op, secret rooms, special bubbles, hidden-condition items, a final boss and multiple endings. Then it goes further.

**The signature twist is the Fizz Taps.** Soda taps stand on some floors, and touching one changes your **bubble flavour** until you lose a robot. Each flavour changes what a bubble *is*:

- **Classic:** today's bubble.
- **Gum:** sticks to walls and ceilings and hangs there for ten seconds as a **platform you build**.
- **Frost:** a trapped grump freezes into an ice block that drops and **slides along the platform**, bowling every grump in its path (a bowling chain).
- **Float:** big, slow bubbles that carry a robot upward when it stands on one: an elevator.
- **Fizz:** rockets straight up and bursts at the ceiling in a shower that traps whatever is beneath.

The classic lets you ride bubbles; Fizz Taps let you **design your own route through each floor**, and many floors are built around a flavour (a gum-bridge floor, a frost-bowling floor). That is newer and better, not a reskin.

**Target length:** a first clear of all 100 floors in roughly 70–90 minutes. Umbrellas and good routes shorten it, and the secret pantries lengthen it.

#### Structure

- **100 floors in ten wings of ten.** Each wing has its own tile set, backdrop, palette, music loop and two new grumps.
- **Mid-bosses** on floors **25, 50 and 75**, and the **final boss on floor 100**.
- **Floors are ASCII data** on the classic's grid (32 x 30 tiles of 8 px at 256 x 240): authored shapes (many draw a picture or a letter), an **air-current map** that steers floating bubbles, and a grump script.
- **Screen wrap:** fall through a floor gap to come out at the top.
- **Five Secret Pantries.** A pantry door appears on floors **20, 40, 60, 80 and 90** if **no robot was lost since the previous wing began**, the classic's kind of hidden condition. Each pantry holds a **recipe card** and a room of treats.
- **Umbrellas** skip three, five or seven floors, at the cost of whatever those floors held.
- Progress saves at each wing start through `saves.ts`, with a continue that keeps the score at half.

#### The wings

| Wing (floors) | Theme and mechanic | New grumps | Flavour tap introduced | Boss |
| --- | --- | --- | --- | --- |
| 1. **Bottling Hall** (1–10) | Today's candy-night look, now with air currents and wrap; bubble riding taught | Waddler, hopper, dasher, climber (today's four behaviours, one colour each) | Classic | — |
| 2. **Gumdrop Gardens** (11–20) | **Springy gumdrop** blocks that bounce robots high | **Bouncer**, **sprout sneak** | **Gum** | — |
| 3. **Lagoon Cellar** (21–30) | **Water channels** push bubbles sideways; **Splash bubbles** introduced | **Puddle puffer**, **diver** | — | **The Big Cork** (25) |
| 4. **Starlight Observatory** (31–40) | **Low-gravity floors**: floaty jumps and slow bubbles; **Zap bubbles** introduced | **Comet sprite**, **telescope tick** | **Float** | — |
| 5. **Ember Kitchen** (41–50) | **Hot plates** that glow, then puff; **Toasty bubbles** introduced (pepper flames along the floor) | **Steam grumbler**, **toast popper** | **Fizz** | **The Kettle Colossus** (50) |
| 6. **Frost Freezer** (51–60) | **Icy floors** (slide), and ice blocks to push | **Snow-flinger**, **skater** | **Frost** | — |
| 7. **Gearworks** (61–70) | **Conveyor platforms**, **moving lifts** and wind-up doors | **Cog crawler**, **wind-up** | — | — |
| 8. **Haunted Pantry** (71–80) | **Dark floors**: lamplight only, and the robots' antennae glow | **Phantom**, **mimic gem** | — | **The Jelly Mould** (75) |
| 9. **Storm Rooftop** (81–90) | **Strong wind** across the floor, rain, and lightning hazards on a tell | **Thunder puff**, **gliding umbrella grump** | — | — |
| 10. **The Carbonator** (91–100) | Remixes of every wing; the floors draw the tower's story | All of them | All taps | **The Grumble Fizz King** (100) |

#### The roster: 4 behaviours → 18 grumps

| Grump | What it does, and its tell | The answer it asks for |
| --- | --- | --- |
| **Waddler** | Walks and turns (today's green and red). | A bubble at range. |
| **Hopper** | Hops often (today's gold). | Trap it at the top of its hop. |
| **Dasher** | Fast walker (today's blue). | Lead your shot. |
| **Climber** | Hops toward you when you're above it (today's pink). | Stay on its level, or bait it up into a bubble. |
| **Bouncer** | A **diagonal flyer** that ricochets off walls (the classic's flyer). | Read its line and leave a bubble on it. |
| **Sprout sneak** | Hides as a flower on a platform and pops up when you pass. **Tell:** the petals twitch. | Bubble the flower. |
| **Puddle puffer** | Spits a horizontal water jet. **Tell:** its cheeks puff for one second. | Hop over the jet and trap it from behind. |
| **Diver** | Swims through water channels, out of reach. | Trap it as it surfaces. |
| **Comet sprite** | A fast straight-line flyer. | Set a bubble wall in its lane. |
| **Telescope tick** | Fires a horizontal beam across its row. **Tell:** a lens glint. | Leave the row. |
| **Steam grumbler** | Puffs a hot cloud ahead of it. **Tell:** a red nose. | Trap it during the wind-up. |
| **Toast popper** | Hides in a toaster and pops up on a beat. | Leave a bubble over the slot. |
| **Snow-flinger** | Lobs snowballs in arcs (the classic's rock thrower). **Tell:** a wind-up. | Dodge, and trap it on the throw. |
| **Skater** | Slides along icy floors and can't stop. | A bubble at the end of its slide. |
| **Cog crawler** | Walks on walls and ceilings. Bubbles pass beneath it. | Trap it when it drops. |
| **Wind-up** | Speeds up as it runs, then stops to rewind. **Tell:** its key turns. | Trap it during the rewind. |
| **Phantom** | Floats through platforms (the classic's ghost). It can only be trapped while it is solid. **Tell:** it turns opaque. | Wait for solid. |
| **Thunder puff** | A cloud grump that charges, then zaps the column below it. | Trap it while it is discharged and grey. |
| **Mimic gem** | Looks like a gem but blinks off-beat. | Trap it: popping it drops a real gem. |
| **Gliding umbrella grump** | Glides down on the wind. | Trap it upwind. |

**The hurry chaser: Old Flat Fizz.** After the floor timer (30 s, as today), a deflated soda ghost drifts in. It cannot be trapped, it follows the nearest robot and it bonks on touch, and it leaves only when the floor is clear. It is the classic's invincible hurry-up chaser, replacing today's "everyone gets angry".

#### The bosses: 0 → 4

1. **The Big Cork** (floor 25). A giant cork bot that bounces diagonally around the room.
   - **Phase 1:** bubbles can't hold it. It spits out little corks: trap them and **pop their bubbles against the Big Cork** to damage it, the classic's way of hurting a boss.
   - **Phase 2:** it wedges in the ceiling and drops down onto your platform. **Tell:** a creak.
   - **Phase 3:** it fizzes around the room at double speed, and Float bubbles are your only way up.
2. **The Kettle Colossus** (floor 50).
   - **Phase 1:** its lid rattles (the tell), then a steam column blasts one side of the room.
   - **Phase 2:** it pours hot water that floods the bottom floors. Ride the Splash bubbles' wave back at it.
   - **Phase 3:** it spins whistling across the room. Zap bubbles stun it.
3. **The Jelly Mould** (floor 75, in the dark). A wobbling giant jelly. Each hit splits it: into two, then four, then eight small jellies. Trap and pop them all quickly, or they slide back together. Its core shows only in lamplight.
4. **The Grumble Fizz King** (floor 100). A huge, sulking bottle on a throne of crates.
   - **Phase 1:** he throws bottle caps in fans. Only Zap bubbles, and minions popped beside him, hurt him.
   - **Phase 2:** he shakes himself up, and fizz floods the room upward. Climb on bubbles and gum ledges ahead of the rising fizz.
   - **Phase 3:** his cap pops off and he shrinks into a tiny, cheerful soda bot.

#### Endings

- **Solo clear:** the Carbonator restarts, but the tower's treat shop stays shut.
- **Co-op clear** (two or more robots reaching floor 100 together): the tower throws a party, as the classic gates its true ending behind two players.
- **True ending** (co-op, with all five recipe cards): the King bakes the tower's lost recipe. Every grump you popped comes back as a guest at a hundred-floor celebration, and the credits roll down the tower floor by floor.

#### Bubbles, items and meta

- **Bubbles as platforms:** hold Hop on a bubble to bounce up it.
- **Air currents** are shown as faint streamers, so currents can be read rather than guessed.
- **Cluster pops:** popping one bubble pops every bubble touching it. Multi-pops drop escalating treats: 1,000, 2,000, 4,000, 8,000, 16,000, 32,000 and 64,000 for seven. They replace today's x4 chain cap.
- **Special bubbles** float in from the floor's edges:
  - **Splash:** a water wave that washes every grump it carries down the floor and off it.
  - **Zap:** a horizontal bolt.
  - **Toasty:** pepper flames that run along a platform.
- **F-R-I-E-N-D letter bubbles** spell out an extra robot, and each spelling raises the next floor's treat tier.
- **Hidden-condition items**, as data rules. Each appears after a hidden condition is met, the classic's deep layer:
  - **Speed shoes:** walk 500 tiles.
  - **Sugar cube:** faster bubbles, after popping 30 empty bubbles.
  - **Bubble gum:** longer range, after 25 hops.
  - **Umbrellas:** skip floors, after riding 10 bubbles in a row.
  - **Party popper:** fills the floor with treats, after a 7-pop.
  - **Lucky star:** a rain of Zap bolts, after 3 Zaps in one floor.
  - **Lamp:** lights dark floors.
  - **Necklace:** points for every jump.
  - **Clock:** freezes grumps for 5 s.
  - **Map:** shows the next pantry's floor.
- **Medals per wing:** No Robot Lost, Full Treats and Speedy. There is a star rating per floor in Floor Select.

#### Modes

- **Tower:** the campaign for **1–4 robots** through the cabinet's `players` frames (with `maxPlayers: 4` in the registry). Each robot has its own colour and its own flavour, and the robots share lives and score. Two or more are needed for the co-op endings.
- **Pop Party:** 2–4 players on shared floors. Most treats wins. Popping a rival's trapped grump steals it: playful, never a knockout.
- **Endless Fizz:** random floors, a score attack, and the leaderboard's main event.
- **Floor Select and Time Trial:** any floor reached, unlocked as you climb.

#### Classic features: matched or beaten

| The classic has | Bumper Bubbles answers with |
| --- | --- |
| 100 authored levels with air currents | 100 floors in ten themed wings |
| Secret rooms | Five pantries behind no-loss conditions |
| Two-player co-op, with the true ending gated on it | Up to four robots; co-op endings |
| Multiple endings | Solo, co-op and true |
| Distinct enemy behaviours, including flyer, thrower, shooter and ghost | 18 grumps |
| Invincible hurry chaser | Old Flat Fizz |
| Bubble riding; cluster pops with the 64,000 ladder | Kept |
| Water, fire and lightning bubbles | Splash, Toasty and Zap |
| Extra-life letters | FRIEND |
| Hidden-condition items, umbrellas | Kept |
| Screen wrap | Kept |
| Boss on the last level | Three mid-bosses and a final boss |
| Bubbles you can ride | **Beaten**: Fizz Taps let you build your own route with gum, frost, float and fizz |

#### Slices

Roadmap: t-059 (slice 1), t-060 (slice 2), t-061 (slice 3), t-062 (slice 4), t-063 (slice 5). Slice 1 is `ready`; each later slice waits on the one before.


**Slice 1: Bubble physics and the first two wings.**
- The ASCII floor format with air-current maps, replacing the four `LAYOUTS` and `BUBBLE_CURVES`.
- Screen wrap.
- Bubbles as platforms.
- Cluster pops and the treat ladder.
- Old Flat Fizz, the hurry chaser.
- FRIEND letters.
- Grumps: waddler, hopper, dasher and climber as separate behaviours, plus bouncer and sprout sneak.
- Wings 1–2, Bottling Hall and Gumdrop Gardens (floors 1–20), with the Gum tap.
- Save/resume at each wing start.

Verified with the engine tests, a deterministic floor-clear test, a pilot probe showing runs end, and screenshots.

**Slice 2: Special bubbles, flavours, items and Wings 3–4.**
- Special bubbles: Splash, Zap and Toasty.
- Fizz Taps: Float, Fizz and Frost.
- The hidden-condition item rules and umbrellas.
- Wings 3–4, Lagoon Cellar and Starlight Observatory (floors 21–40): water channels, low gravity, puddle puffers, divers, comet sprites and telescope ticks.
- The Big Cork.
- The first two Secret Pantries.

**Slice 3: Wings 5–7.**
- Ember Kitchen, Frost Freezer and Gearworks (floors 41–70).
- Hot plates, ice, conveyors and lifts.
- Grumps: steam grumbler, toast popper, snow-flinger, skater, cog crawler and wind-up.
- The Kettle Colossus.
- The third pantry.

**Slice 4: Wings 8–10 and the endings.**
- Haunted Pantry, Storm Rooftop and the Carbonator (floors 71–100).
- Dark floors, wind and lightning.
- Grumps: phantoms, mimic gems, thunder puffs and umbrella grumps.
- The Jelly Mould and the Grumble Fizz King.
- The last pantries, recipe cards, and the solo, co-op and true endings.

**Slice 5: Co-op and the extra modes.**
- Tower co-op for 1–4 robots through `players` frames (`maxPlayers: 4`), with the co-op ending gates.
- Pop Party.
- Endless Fizz.
- Floor Select and Time Trial.
- Medals and per-floor stars.

---

## 8. Cable Crawler (Nibbler riff)


### What is in the game today

`cableCrawler.ts`, 1,279 lines. Registry entry: 240 x 224, solo, no mastery ladder.

| Area | Today |
| --- | --- |
| Boards | **One generator.** Blocks no bigger than 2 x 2 are scattered on a three-cell lattice (55% → 85% filled) and mirrored. The result is an **open field of small chips**, not a maze of corridors: the screenshots show wide crossroads everywhere and almost no long runs, hairpins or dead ends. There are no authored mazes. |
| Visual variety | **Four** colour themes (teal, purple, sky, leaf) on the same chip-and-trace art, taken in turn. |
| Food | Sparks on every other open cell (about 150 a board). **One golden spark** blinks in every 15 s for 6 s (500 x board). Nothing else is ever on the board. |
| Enemies and hazards | **None.** The only threats are your own cable and the battery, which runs 75 s at board 1 down to 40 s. |
| Feel | Walls pause the cable instead of killing it, and a corner with only one way on turns it by itself: the classic's signature, done well. |
| Death | The cable resets to four cells and the battery refills, but **eaten sparks stay eaten**, so a long board gets easier each time you die. |
| Scoring | 10 x board per spark, 500 x board per gold spark, and a battery bonus of 5 x board per second left. An extra cable every 15,000. |
| Difficulty | Block fill capped at board 7, battery at board 10, crawl speed (8 → 3 ticks a cell) at board 11. **From board 11 on, every board is the same board.** |
| Players, ending, saves | Solo; none; none. |

### Against the classic

The 1982 game it riffs on:

- **Hand-drawn mazes** of long corridors, tight hairpins and dead ends, in a set cycle. Learning each maze, and where your growing body will trap you, is the game.
- **Length carries the puzzle:** the snake grows with every bite and starts each wave longer, so later waves are about not boxing yourself in with your own tail in narrow halls.
- **A shrinking clock per wave**, with the time left paid as a bonus, and **food icons that change** from wave to wave.
- **A steep speed ramp** and a nine-digit score counter, famously built for marathon runs.
- Walls only stop you, and you turn at corners by yourself. Cable Crawler copies this, and copies it well.
- Later snake games added enemies, keys and doors, level goals, multiplayer and bosses.

**Verdict:** Cable Crawler has the classic's feel: the pause at walls, the auto-turn and a beautifully shaded cable. But its boards are open chip fields, so the classic's real puzzle (a long body in narrow corridors) barely exists. There are no authored mazes, no enemies, no hazards, no carried-over length and no variety beyond a gold spark and four colour swaps. It is flat from board 11. It is the weakest structure of this batch after Bumper Bubbles.

### The upgrade: Cable Crawler — The Mainframe Odyssey

The cable bot travels into a giant old computer, the Mainframe, which has gone dark and is full of little glitches. It works through the machine one component at a time, slurping stray sparks and **re-powering each part until the whole Mainframe boots**. Every component is a world of authored mazes, its own spark art, its own board mechanic and its own glitches.

**The signature twist is the Plug-In Surge.** Each maze has two to four **sockets**. Drive the plug into one and the current runs down the **entire length of the cable**:

- every spark touching the cable's sides is slurped at once, as a climbing chain (10, 20, 40...);
- every glitch touching the cable reboots: stunned, and turned into points;
- the battery tops up by the cable's length.

Then the socket recharges for ten seconds. In the classic your length is only a danger. Here it is also your weapon: the longer the cable you dare to lay across the maze, the bigger the sweep when you plug in. That makes routing a real plan, and it is newer and better than the original.

**Target length:** a first clear in roughly 50–60 minutes.

#### Structure

- **Six components** (worlds). Each has **five authored mazes**, a **Screensaver** bonus board after maze 3, and a **boss board**.
- A **secret seventh component, the BIOS**: three monochrome green-screen mazes and the true boss.
- In all: **33 mazes, 6 Screensavers and 7 bosses**.
- Mazes are ASCII data in the classic style: long corridors, hairpins, dead ends and pinch points, mirrored or not.
- **Length carries over within a component:** each maze starts the cable two cells longer than the last (the classic's ramp). A new component resets it.
- Each component has its own spark sprite, board art and palette, wall style and music loop: bits, notes, pixels, flakes and so on.
- Every maze hides **one golden byte**: the gold spark, now placed by the maze data. All 30 golden bytes in the six main components unlock the BIOS.
- **The Workbench** opens between components, and progress saves at each component start through `saves.ts`.

#### The components

| Component | Board mechanic | New glitches | Screensaver | Boss |
| --- | --- | --- | --- | --- |
| 1. **The Power Strip** | Sockets and surges introduced; classic narrow corridors | **Static bug**, **dust bunny**, **mimic spark** | **Starfield**: sparks stream past an open board; the battery never drains | **The Surge Protector** |
| 2. **RAM Rows** | Long parallel rows. **Refresh**: on a beat, whole rows swap their sparks with the next row. **Diodes**: one-way arrow tiles. | **Cache crab**, **bit flipper** | **Defrag**: push loose blocks into rows | **The Memory Leak** |
| 3. **The Cooling Fan** | **Rotating fan sectors**: whole wall quarters turn 90° on a tell. **Airflow** lanes push the cable along. **Heat tiles** drain the battery twice as fast. | **Hot spot**, **leak drip** | **Breeze**: ride airflow loops to collect sparks | **The Big Whirr** |
| 4. **The Sound Card** | **Beat gates** open and shut on the music. **Speaker cones** pulse and shove the plug one cell. | **Echo**, **noise gnats** | **Equaliser**: sparks rise and fall in bars | **The Subwoofer** |
| 5. **The Graphics Card** | **Picture boards**: sparks are the pixels of an original image, and slurping them reveals it. **Scanlines** sweep the board: be off the line when it passes, or lose your tail end. | **Glitch sprite**, **z-fighter wall** | **Paint**: colour a picture by its numbered sparks | **The Glitch** (a rival cable) |
| 6. **The CPU Core** | **Clock cycles**: the whole board speeds up and slows down in a cycle. Every earlier mechanic is remixed. | **Interrupt**, **rival cable** | None | **The Sleepy Kernel** |
| 7. **Secret: The BIOS** | Green-screen mazes; text-mode walls that rewrite themselves line by line | Remixes of everything | None | **The Boot Loader** |

#### The roster: 0 → 13 glitches

| Glitch | What it does, and its tell | The answer it asks for |
| --- | --- | --- |
| **Static bug** | Wanders the corridors. Meeting the plug head-on unplugs you; it bounces off your body. **Tell:** a crackle. | Lead it alongside your cable and surge. |
| **Dust bunny** | A soft block sitting in a corridor. The plug pushes it, Sokoban-style. | Push it into a dead end, or surge it away. |
| **Mimic spark** | Looks like a spark but twinkles out of phase. Slurping it shorts ten seconds off the battery. | Read the twinkle. |
| **Cache crab** | Scuttles sideways along rows and **snips your cable**, cutting off the tail end. A shorter cable is safer, but the snipped length (and its sparks) is lost. **Tell:** its claws rise. | Cross its row when its claws are down, or surge it. |
| **Bit flipper** | Flips every diode it passes. | Watch the arrows change behind it. |
| **Hot spot** | A warm glow that grows slowly and drains the battery inside it. | Surge it to cool it. |
| **Leak drip** | Leaves goo cells that take two steps to cross. | Route around, or through on purpose to slow down for a tight turn. |
| **Echo** | A ghost cable that **retraces your exact path** four seconds behind you. | Don't cross your own trail, or cross it on purpose so the echo walks into a socket surge. |
| **Noise gnats** | A trio that orbits the plug when you're near them. | Surge with them touching the cable. |
| **Glitch sprite** | Teleports onto the spark you're heading for. **Tell:** a scanline flicker at the target one second before. | Change route. |
| **Z-fighter wall** | Flickers between solid and passable. | Time your pass. |
| **Interrupt** | Drops a wall right in front of the plug. **Tell:** a one-second outline. | Turn early. |
| **Rival cable** | Another cable racing you for sparks. Its body is a wall; plug against plug pauses you both. | Out-route it, or trap it against your own length. |

#### The bosses: 0 → 7

1. **The Surge Protector** (Power Strip). A great fuse beetle walking the maze's ring corridor.
   - **Phase 1:** lay your cable across its path, then surge through it. It takes three surges.
   - **Phase 2:** it pulls the sockets around the board.
   - **Phase 3:** it charges down the corridors. Pause at a wall and let it pass.
2. **The Memory Leak** (RAM Rows). A blob that drips goo down the rows. Each surge through it shrinks it. In its final phase it splits into row-crawling drips that must all be swept in one surge.
3. **The Big Whirr** (Cooling Fan). The whole board is a giant fan whose blades are walls, turning.
   - **Phase 1:** slip between the blades to reach the hub sockets.
   - **Phase 2:** the fan reverses.
   - **Phase 3:** it spins up. The airflow drags your cable, so wrap it around the hub and surge.
4. **The Subwoofer** (Sound Card). A speaker that pulses the board on the beat: gates flip and cones shove. Surge it in the gap between beats. In its last phase the tempo doubles.
5. **The Glitch** (Graphics Card). **A rival cable** made of corrupted pixels.
   - **Phase 1:** a race for sparks.
   - **Phase 2:** it tries to cut you off, and trapping it against your length stuns it.
   - **Phase 3:** it splits into two and must be trapped together.
6. **The Sleepy Kernel** (CPU Core). A huge, drowsy chip in the centre of the board with four pin banks.
   - Route your cable through all four banks without a bite, then surge. Each phase adds clock-cycle speed swings and interrupts.
   - When all four banks light, it yawns and the Mainframe boots: the first ending, with the machine's screen showing your score.
7. **The Boot Loader** (BIOS, the true boss). The machine's oldest code. It rewrites the maze walls a line at a time while you hunt its three checksum sockets. **True ending:** the whole Mainframe comes alive, and every glitch you rebooted waves from the screen.

#### Power and meta

- **Pickups** that drop out of surged glitches:
  - **Capacitor:** battery +20 s.
  - **Heat sink:** five seconds of slow crawl.
  - **Insulation:** one free pass through your own body.
  - **Coil:** winds eight cells off the tail.
  - **Magnet:** sparks one cell away jump to the plug.
- **The Workbench** between components. Spend copper earned in play (never real money) on:
  - an extra cable;
  - longer surge reach;
  - starting insulation;
  - cable colours;
  - a **golden-byte hint**.
- **Medals per maze:** No Bites, Big Surge (twenty or more in one surge) and Battery Saver.

#### Modes

- **Odyssey:** the campaign.
- **Tangle:** 2–4 cables through the cabinet's `players` frames.
  - **Team Tangle** shares one battery and one score.
  - **Tangle Race:** most sparks wins. Bodies are walls, and plug against plug is a playful pause, never a knockout.
- **Marathon:** the classic homage. All 33 mazes in a fixed cycle, the steep speed ramp, a per-wave clock and a **nine-digit score counter**; the leaderboard's main event.
- **Maze Trials:** time attack per maze, unlocked on a clear.

#### Classic features: matched or beaten

| The classic has | Cable Crawler answers with |
| --- | --- |
| Authored, cycling mazes | 33 mazes, Screensavers and the BIOS |
| Growing start length | Kept |
| Shrinking clock with a time bonus | The battery, kept |
| Changing food icons | A spark set per component |
| Marathon play with a nine-digit counter | Marathon mode |
| Walls pause; auto-turn at corners | Kept |
| No enemies in the original | 13 glitches and 7 bosses (later snake games added these) |
| Length is only a danger | **Beaten** by the Plug-In Surge, which turns length into a weapon |

#### Slices

Roadmap: t-064 (slice 1), t-065 (slice 2), t-066 (slice 3), t-067 (slice 4), t-068 (slice 5). Slice 1 is `ready`; each later slice waits on the one before.


**Slice 1: Maze engine, surge and the Power Strip.**
- The ASCII maze format, with mirrored mazes and the start-length ramp, replacing the lattice generator and `CABLE_CURVES`.
- Sockets and the Plug-In Surge: side sweep, chain scoring, glitch reboot and battery top-up.
- Glitches: static bug, dust bunny and mimic spark.
- The Power Strip: five mazes, the Starfield Screensaver and the Surge Protector.
- A per-component spark set and board art.
- Golden bytes.

Verified with the engine tests, a deterministic maze-clear test, a pilot probe showing runs end, and screenshots.

**Slice 2: RAM Rows and the Cooling Fan.**
- Mechanics: diodes, row refresh, rotating fan sectors, airflow lanes and heat tiles.
- Glitches: cache crab (tail snip), bit flipper, hot spot and leak drip.
- Screensavers: Defrag and Breeze.
- Bosses: the Memory Leak and the Big Whirr.
- The Workbench, pickups, and save/resume at each component start.

**Slice 3: The Sound Card and the Graphics Card.**
- Mechanics: beat gates, speaker cones, picture-reveal boards and scanlines.
- Glitches: echo, noise gnats, glitch sprite and z-fighter walls.
- Screensavers: Equaliser and Paint.
- Bosses: the Subwoofer and the Glitch rival-cable fight.

**Slice 4: The CPU Core, the BIOS and the endings.**
- CPU Core: clock cycles, interrupts and rival cables; the Sleepy Kernel.
- The BIOS green-screen mazes and the Boot Loader.
- The boot ending and the true ending.
- Medals and medal boards.

**Slice 5: Multiplayer and the extra modes.**
- Tangle (Team and Race) for 2–4 cables through `players` frames, setting `maxPlayers` in the registry.
- Marathon, with the fixed cycle and the nine-digit counter.
- Maze Trials.

---

## 9. Seed Lander (Lunar Lander riff)


### What is in the game today

Taken from `seedLander.ts` (1,143 lines) on kind_robots `main` (6fb4809).

| Area | Today |
| --- | --- |
| Hills | Endless. Each hill is **one random screen** of terrain (32 segments) that wraps round at the edges, with **three pads** (x1, x2, x4) flattened into it. There is no map, no scrolling and nothing to do but land once. |
| Backdrop | One dawn sky with the same ringed planet, sun and clouds on every hill. Four ridge silhouettes cycle behind it. In the demo, hill 15 looked exactly like hill 1. |
| Hazards | The **terrain and the wind**, and nothing else. The gust strength changes every 3 s. Nothing moves, nothing is in the air and there is no weather. |
| Pod | Lean and puff. Sunlight (fuel) holds 900 ticks of puffing and **is shared by every pod**. Each planting refills 260; a bonk refills nothing, and a new pod starts with whatever is left. When the sun runs dry, every remaining pod drops like a stone, which is what the demo showed on hill 15. |
| Landing | Soft (plants), bumpy (up to 1.7x safe speed, plants for a third of the points), or bonk (too fast, too tilted or off a pad). Lean must be within 0.22 rad. |
| Scoring | 500 x pad multiplier x softness, plus a sunlight bonus on every landing; 15 x hill for a bonk. |
| Difficulty | The narrow pad bottoms out at hill 6; roughness, the wide pad and the wind cap at hill 8. **From hill 8 on, every hill is the same.** The demo reached hill 15 four minutes in. |
| Camera and scale | A fixed 320 x 240 screen. The pod is about 13 px tall and the camera never zooms, so the precise last few pixels of a landing are the hardest thing to see. |
| Structure | No objectives besides landing, no boss, no ending, no save. Solo only. |

### Against the classic

Lunar Lander (1979) is itself a lean game, so the bar includes what the genre did next:

- **A wide scrolling moonscape** several screens across, with a fixed mountain map. The camera **zooms in** close to touchdown.
- **Pads up to x5**, the best ones tucked into narrow valleys or on peaks, so they are hard to reach, not just narrow.
- **Fuel is the life bar**: a crash costs fuel, and the game ends when the tank is empty.
- **An abort button** rights the craft and fires full thrust.
- **Four difficulty tiers** (training to command) change gravity and handling.
- **Landing ranks** (good landing, hard landing, crash with a crater).
- The games that followed made the formula deep: **cavern flying** and **towing cargo on a tether** (Thrust), **gravity planets and missions** (Gravitar), **rescue runs** (Lunar Rescue).

**Verdict:** Seed Lander handles nicely, and its wind is a real addition. But it is smaller than its 1979 source. It has one screen instead of a scrolling world, no zoom, x4 at best instead of x5, no abort, no difficulty choice and no landing ranks. From hill 8 nothing changes, and the only thing ever asked is "land once". The classic is thin itself, so matching it is not enough: the upgrade has to bring places, missions and threats.

### The upgrade: Seed Lander — The Great Replanting

The seed pod flies a mission across a sky archipelago of wilted islands, replanting each one. The signature idea is that **what you plant changes the island**:
- a **sunflower** becomes a refuelling pad;
- a **beanstalk** becomes a tall landing ledge to reach the high pads;
- a **mushroom** becomes a bouncer;
- a **vine** becomes a ladder of perches up a cliff.

Every island is a short landing puzzle: you choose what to plant where so the island helps you finish it.

**Target length:** a first clear in about 45–60 minutes across 6 islands, 30 missions and 6 boss set-pieces.

#### Structure

- **Six islands** and a secret seventh, **the Seed Vault**.
- Each island is a **wide map**, 3–6 screens across (some are tall caverns), with **5 missions and a boss set-piece**. Missions are data-defined:
  - **Plant:** land on the marked pads.
  - **Deliver:** tow a seedling crate on the **tether winch**.
  - **Water:** carry a water bubble from a spring and drop it on a dry bed.
  - **Rescue:** pick up stranded sprout-bots and fly them home.
  - **Lantern Run:** land beside unlit lanterns to relight them.
  - **Ring Race:** fly through petal rings against the clock.
- **The camera scrolls and zooms** smoothly in close below about 40 px of altitude (the classic's zoom), so the pod reads at 30+ px for touchdown.
- An island map screen between missions; progress saves at each island.
- A clear unlocks **Gale Season** (New Game+: stronger gravity, stronger wind and less sun).

#### The islands

| # | Island | Terrain and physics | New hazards | Special mission | Boss |
| --- | --- | --- | --- | --- | --- |
| 1 | **Meadow Isle** (dawn) | Today's hills, wider and scrolling; sunflower refuel pads | Gusts (now shown as streamers), **updraft vents** | **First Bloom**: plant three pads, then use your own sunflower to refuel | **Old Scarecrow** |
| 2 | **Windmill Downs** | **Gust lanes** you can see; **windmill blades** to time through | **Dandelion drift** (fluff that sticks and adds drag), **crow-bot** | **Pollen Post**: tow seed crates on the tether to three farms | **The Gale Mill** |
| 3 | **Waterfall Gorge** | A tall **cavern descent**. **Waterfalls** push the pod down, and spray slows it. | **Drip stalactites**, **pebble rollers** | **Thirsty Terraces**: carry water bubbles from the falls to dry terraces | **The Geyser Tortoise** |
| 4 | **Firefly Caverns** | **Dark caves** lit only by your puff glow, fireflies and the lanterns you relight. Crystal bumpers bounce the pod gently. | **Spore puffball** (blurs your gauges for 2 s), **bumble buoys** | **Lantern Run**: relight the cave before the fireflies tire | **The Glowworm Queen** |
| 5 | **Storm Shelf** | **Cloud platforms** drift as pads. **Rain** makes the pod heavier while it is wet. | **Lightning clouds** (a visible charge-up tell), **hail** | **Sun Seeds**: plant on cloud tops between strikes | **Thunderhead** |
| 6 | **Moon Garden** (the homage) | **Low gravity, no wind, huge inertia**; craters; x5 pads | **Dust devils**, **meteor drizzle** (tell: streak marks) | **Old Friends**: find and wake the six sleeping landers | **The Old Lander** |
| ★ | **The Seed Vault** (secret) | All physics remixed, the narrowest pads and the strongest weather | All | **Every Seed**: plant one of each kind of plant | — |

#### The roster: 2 → 15 hazards

| Hazard | Tell | Answer it asks for |
| --- | --- | --- |
| Gust (today) | Streamers along the gust lane | Lean into it and land between gusts |
| **Updraft vent** | Leaves spiral up the column | Cut the puff and ride it up, saving sun |
| **Windmill blade** | A steady sweep with a creak at the top | Time the gap |
| **Dandelion drift** | Fluff drifting across your path | Puff hard to shake it off before landing |
| **Crow-bot** | Caws, circles, then dives on its shadow | Swing the tethered cargo away, or land to guard it |
| **Waterfall** | White water | Duck into the alcove behind it |
| **Drip stalactite** | A drop swells before it falls | Wait one beat |
| **Pebble roller** | Pebbles wobble on a slope | Don't park on a pad below a slope |
| **Spore puffball** | It swells as you fly over | Fly over it high, or accept 2 s of blurred gauges |
| **Bumble buoy** | Buzzing arcs | Give it room; a bump knocks your lean |
| **Lightning cloud** | It crackles and glows for 1.5 s | Be elsewhere |
| **Hail** | The clouds turn white and rattle | Shelter under a ledge; a hailstone knocks your lean |
| **Rain** | Clouds darken and the pod's paint gets wet | Expect the extra weight and puff earlier |
| **Dust devil** | A dust spiral | Go round it; low gravity makes a spin long |
| **Meteor drizzle** | Streak marks in the sky | Land under a crater rim |

Bonks stay cartoon: the pod boings, seeds scatter into wildflowers, and a spare pod drops in.

#### The bosses: 0 → 6 set-piece landings

1. **Old Scarecrow** (Meadow Isle): a giant scarecrow-bot whose **hands are moving pads**. Plant on his hands as he waves; the waves get faster each phase. In the last phase crows land on his hands and you must time between them.
2. **The Gale Mill** (Windmill Downs): a windmill with a storm face. Land on its **sail-tip platforms** at the slow top of each turn. The wind reverses each phase, and the last phase spins the other way.
3. **The Geyser Tortoise** (Waterfall Gorge): its shell is a pad that rides up on a geyser. Land when the column calms. In phase 2 it swims across the pool; in phase 3 it surfaces in three places in turn.
4. **The Glowworm Queen** (Firefly Caverns): a cave-long glowworm whose **lit segment is the only pad**. The light runs down her body in a sequence you learn, and each phase speeds it up.
5. **Thunderhead** (Storm Shelf): a grumpy storm cloud. Plant sun seeds on its puffy tops to cheer it up. Its phases are rain (heavy pod), lightning (telegraphed strikes) and hail (bounces), and the last seed clears the sky.
6. **The Old Lander** (Moon Garden): a grey lander-bot from long ago, asleep in the dust (the homage). Dock gently with it, **tow it on your tether** across the low-gravity garden, and set it down on the great pad. Together you plant the last seed, and the moon blooms.

#### Systems that run through the campaign

- **Living gardens** (the signature). Planted seeds become plants that stay and change the map:
  - **sunflower:** a refuel pad;
  - **beanstalk:** a tall ledge;
  - **mushroom:** a bounce pad;
  - **vine:** a ladder of perches.

  The mission tells you what each pad will grow, and the order you plant in is the puzzle.
- **Sun per mission:** each mission has its own sun budget, refilled at sunflowers. Running dry ends the mission (retry), not the run, which fixes today's shared-tank death spiral.
- **Hop (B):** the classic's abort. It snaps the pod upright and fires a strong puff for a big sun cost.
- **Tether winch:** hold A over cargo to hook it. Cargo swings as a pendulum and lands gently or bumps, and a bumped crate drops a seedling.
- **Landing ranks:** Feather, Soft, Bumpy and Bonk. A **Feather streak** raises a multiplier that carries across missions.
- **Pads x1–x5.** x5 pads sit where only good flying or a well-placed beanstalk reaches.
- **Flight tiers** chosen at the start (the classic's difficulty select):
  - **Breezy:** shows a predicted landing arc and gives 25% more sun.
  - **Standard.**
  - **Gale:** stronger gravity, and only one hop per mission.
- **The Pod Shed** between islands. Spend nectar earned in play on a bigger sun tank, springier legs (more bumpy tolerance), steadier gyros, a brighter lamp for the caves and a longer winch line.
- **Golden acorns:** three per island. All 18 open the Seed Vault.
- **Medals per mission:** Feather (all Feather landings), Thrifty (sun under par) and Swift (time under par).

#### Modes and players

- **The Great Replanting:** the campaign.
- **Free Flight:** today's endless hills, now scrolling, with the new hazards seeded in by hill number. It is the leaderboard's main event and **never plateaus**: each 4 hills unlocks a new hazard from the roster.
- **Daily Hill:** one hill seeded from the date.
- **Time Trial:** per mission, after a clear.
- **Tandem** (`maxPlayers: 2`): two pods on one island in co-op. One can winch the other's cargo, and a **double plant** (both land on the same wide pad) pays a bonus.
- **Relay:** players take landings in turn, the classic's alternate play, with a shared score.

#### The classic's signature features, matched or beaten

| The classic had | Seed Lander will have |
| --- | --- |
| A scrolling moonscape with a zoom near the ground | Scrolling islands 3–6 screens wide and tall caverns, with a smooth zoom below about 40 px |
| Pads up to x5 | x1–x5 pads, the x5s reached by flying skill or by your own beanstalks |
| Fuel as the life bar | Sun per mission, refilled at the sunflowers you plant |
| Abort | Hop |
| Four difficulty tiers | Breezy, Standard and Gale flight tiers |
| Landing ranks | Feather, Soft, Bumpy and Bonk, with a Feather streak multiplier |
| The genre's later caves, towing and rescue | Cavern islands, the tether winch, Rescue and Deliver missions |

#### Slices

Roadmap: t-069 (slice 1), t-070 (slice 2), t-071 (slice 3), t-072 (slice 4), t-073 (slice 5). Slice 1 is `ready`; each later slice waits on the one before.


**Slice 1 — Flight core.** Replace the single wrapped screen with **wide scrolling maps** and a **zoom-to-land camera**, so the pod is drawn at 30+ px near touchdown. The slice also adds:
- **Hop**, landing ranks with the Feather streak, x1–x5 pads and the **tether winch**;
- **sun per mission** with sunflower refuel;
- the three **flight tiers**;
- a data-driven island/mission format;
- Free Flight rebuilt on the new maps, its hazard unlock every 4 hills replacing the hill-8 plateau.

Verified by a pilot probe that lands every pad type, plus Pixel/HD screenshots at both zoom levels.

**Slice 2 — Meadow Isle and Windmill Downs.** Ten missions across islands 1–2: **living gardens** (sunflower, beanstalk, mushroom, vine) and the Plant, Deliver and Ring Race mission types. It adds:
- updrafts, gust lanes, windmills, dandelion drift and the **crow-bot**;
- **Old Scarecrow** and **The Gale Mill**;
- the island map screen, the **Pod Shed**, golden acorns 1–6;
- save/resume per island.

**Slice 3 — Waterfall Gorge and Firefly Caverns.** Islands 3–4: vertical caverns, waterfalls and spray, **water carrying**, and the dark-cave light radius with relightable lanterns. It adds:
- stalactites, pebble rollers, spore puffballs and bumble buoys;
- the Water, Rescue and Lantern Run missions;
- **The Geyser Tortoise** and **The Glowworm Queen**.

**Slice 4 — Storm Shelf, Moon Garden and the Seed Vault.** Islands 5–6: cloud platforms, wet-pod weight, lightning and hail, low-gravity moon physics, dust devils and meteor drizzle. It adds:
- **Thunderhead** and the **Old Lander** finale with its towing set-piece;
- the secret Seed Vault;
- credits, endings and **Gale Season** New Game+.

**Slice 5 — Two pods and the modes.** `maxPlayers: 2` with **Tandem** co-op (shared cargo and the double-plant bonus) and **Relay**. It adds:
- **Daily Hill**;
- per-mission **Time Trial**;
- the medal boards and a mastery ladder.

---

## 10. Ribbon Riders (Tron light cycles riff)


### What is in the game today

| Area | Today |
| --- | --- |
| Arena | **One** open 72 × 72-cell square (4 px cells) with nothing in it: no pillars, gates, pads or layouts. The floor cycles **three** palettes by round. The arena never changes shape except for the closing wall. |
| Rivals | **One** steering brain shared by every rival. It flood-fills for the roomiest turn (capped at 90 cells), pulls toward a point 8 cells ahead of the player ("cunning" 0 → 1 by round 5), and takes a random free turn now and then (8% → 2%). Rivals differ only in colour. Their count goes 1 → 4 by round 4. |
| Hazards | The closing wall moves one cell in from every side each 600 → 300 ticks, up to 20 cells, with a 90-tick flashing tell. There is nothing else. |
| Player tools | Steering and a turbo meter (120 ticks, refilling a tick every 3). No brake, no pickups, no way to cross or clear a ribbon. |
| Scoring | 1 point per 4 cells ridden, 500 × round per rival out (only while you are still riding), 1,000 × round per round cleared, and an extra rider every 20,000. No combos, no near-miss or slipstream reward. |
| Difficulty | Rivals max out at round 4, cunning and wander at round 5, speed (0.33 → 0.5 cells a tick) at round 8 and the wall's pace at round 9. **From round 9 on, every round is the same round.** |
| Structure | A crash replays the round from scratch. The only objective is being the last rider rolling. There are no bosses, no ending, no saves and no music. |
| Players | Solo (no `maxPlayers`), in the genre that head-to-head play made famous. |
| Scale | A 6 × 11 px bike on a 288 × 312 screen. On a phone the player is a dot. |
| Code | `ribbonRiders.ts`, 1,108 lines, the smallest of this batch. The seed-5 attract pilot was out at round 5 after about 100 seconds. |

The screenshots show the neon grid and glowing tube ribbons looking great. But the arena is an empty tiled square, the bike reads as a speck, and two rounds apart the only change is the grid's palette.

### Against the classic

The 1982 cabinet's light-cycle stage is one of four games on each level. It and the wall games around it in the genre (the two-player games before it, the light-cycle games after) have what a single empty grid lacks:

- **A level ladder you climb.** Each level has a name and a harder set of opponents, and a hub lets you choose which of the four games to play next.
- **Speed control.** Pushing or pulling the stick speeds the cycle up or slows it down, so you can bait a rival into a corner or let it overshoot.
- **Rival cycles that change by level.** There are more of them, they are faster, and they get more aggressive about cutting across your nose.
- **Head-to-head play.** The two-player wall games are the root of the genre, and they had rule variants: wrap-around edges, speed-up, and trails that erase.
- **Later light-cycle games** added **slipstream** (grinding along a wall for speed), **brakes**, **arenas with obstacles** and **team play**.

**Verdict:** Ribbon Riders is a handsome, faithful light-cycle screen and nothing more. It has one empty arena, one rival brain in four colours, no speed control, no pickups, no layouts, and no versus mode in the most versus genre there is. Its curve is flat by round 9. Of the six games in this batch, it is the thinnest.

### The upgrade: Ribbon Riders — The Lantern Festival Circuit

The riders tour a travelling festival's four fairgrounds. Each fairground has its own arenas, its own rival crews and a Grand Marshal to beat.

The ribbon also stops being only a wall. **Close a loop and your ribbon gift-wraps whatever is inside**: sparkles, pickups, and any rival caught in the loop, who pops out tied in a bow and sits the round out. Boxing a rival in becomes something you draw on purpose instead of something you wait for. That is the signature twist.

**Target length:** a first clear in roughly 40–50 minutes.

#### Structure

- The campaign has **four fairgrounds** (acts) of **five arenas** each, a **Grand Marshal** (boss) at the end of each, and a secret fifth fairground.
- Each arena is authored data: a layout (pillars, gates, pads, wrap edges), a rival crew, an objective, a par time and three medals.
- Between arenas, the **Festival Board** (a map) offers two or three next events, the way the classic cabinet let you pick your next game. Every route reaches the Grand Marshal; side events pay tickets and medals.
- The **Paint Shop** opens between fairgrounds (below).
- Progress saves at each fairground through `utils/arcade/saves.ts`. A clear rolls credits and unlocks **Encore**, a New Game+ with mirrored arenas and faster crews.

**Objectives** (all data-defined):

- **Last Rider Rolling:** today's rule, now on authored layouts.
- **Gift Wrap:** wrap every rival before time runs out. A rival that crashes on its own doesn't count.
- **Glowbug Run:** glowbugs drift over the arena. Wrap them or ride through them; the first rider to collect the target number wins.
- **Ribbon Art:** a faint outline glows on the floor. Trace it with your ribbon, within a tolerance, while rivals try to cut across it.
- **Parade Escort:** a slow parade float crosses the arena. Keep the rivals' ribbons out of its path.
- **Tag Lap:** ride through the checkpoint arches in order, racing the crew.

#### The fairgrounds

| # | Fairground | Arenas and mechanics | New rivals | Special arena | Grand Marshal |
| --- | --- | --- | --- | --- | --- |
| 1 | **Boardwalk at Dusk** | Today's square, tightened. Then **lamp-post pillars**; the **carousel**, a rotating ring of solid horses in the centre; and **wrap edges** on the pier (ride off the right, come in on the left). | Roamer, Cutter, Copycat, Lantern Kid | **Glowbug Run** over the pier | **The Carousel Keeper** |
| 2 | **Frostlight Rink** | **Ice tiles**: a turn queued on ice takes one extra cell. **Snowbanks** block like walls until a ribbon brushes them, then melt. **Turn pads** force a 90° turn along a glowing arrow. | Snowplow, Pacer, Tandem | **Ribbon Art**: skate a snowflake | **The Zamboni Swan** |
| 3 | **Clockwork Bazaar** | **Gates** open and shut on the beat, with one beat of flashing as the tell. **Conveyor lanes** shift a bike one cell sideways every 8 cells. **Bell pads** make every ribbon flare for 2 seconds, and a flared ribbon is wider. | Hugger, Dasher, Gatekeeper | **Tag Lap** through the bazaar's arches | **The Clockwork Conductor** |
| 4 | **Starlight Loom** (the night sky) | **Portals** (paired swirls). **Comet tails**: every ribbon on the board fades after 6 seconds. A **spiral wall** closes inward instead of the square one. | Glimmer, Shield Rider, Sprinter | **Parade Escort** of the moon float | **The Loom Spinner** |
| ★ | **The Rainbow Spool** (secret) | Remixes of every hazard and every arena, mirrored | All four crews | — | **The Spool Itself** |

The secret fairground opens to a rider holding **four Golden Bows**. Each fairground has one, earned by gold-medalling its special arena. Clearing the Rainbow Spool gives the true ending: the riders' ribbons light the whole festival from the sky.

#### The roster: 1 brain → 13 rivals

Each rival has its own steering personality, its own bike art and a tell you can read.

| Rival | Behaviour | Tell | Answer |
| --- | --- | --- | --- |
| **Roamer** | Today's flood-fill wanderer | A wobbly headlight | Give it space and it boxes itself in |
| **Cutter** | Today's cunning brain: aims 8 cells ahead of you | Its headlight swings toward you | Brake, let it cut across empty air, then wrap it |
| **Copycat** | Mirrors your turns across the arena's centre line | Its ribbon is your colours reversed | Turn so that the mirror runs it into a wall |
| **Pacer** | Matches your speed and rides alongside | Rides parallel, two cells away | Brake hard; it overshoots and you cut in behind |
| **Hugger** | Slipstreams along ribbons and walls for speed | Sparks off its side | Lead it down a dead-end channel |
| **Dasher** | Lays a dotted ribbon, every other cell | A dashed trail | Slip through the gaps; its own wall leaks |
| **Snowplow** | Erases any ribbon it drives over | A shovel nose and white spray | Don't shelter behind your ribbon near it; bait it into pillars |
| **Tandem** | Two bikes that turn together | A bright tether between them | One loop round both wraps both |
| **Gatekeeper** | Parks across a gate, then lunges when you come near | Idles with its headlight dimmed | Come at it from the side, never head-on |
| **Glimmer** | Its ribbon is invisible except on the beat flash | A faint shimmer each beat | Watch the beat and ride its last-seen line |
| **Shield Rider** | Can pass through one ribbon cell per round | A bubble round the bike that pops when used | Make it spend the shield, then wrap it |
| **Sprinter** | Turbo-bursts whenever it lines up with you | Half a second of afterburner flicker | Never sit on its line |
| **Lantern Kid** | Harmless; rides only to collect glowbugs | Carries a lantern | Race it to the glowbugs; wrapping it costs a medal |

#### The Grand Marshals: 0 → 5 bosses

Every Marshal is a big rider (3 × 3 cells or larger) with phases. You beat it by **wrapping**: closing a loop round its glowing hub.

1. **The Carousel Keeper:** a carousel on wheels.
   - **Phase 1:** it circles the arena laying a solid ring that shrinks. Gaps open on a chime, which is the tell. Ride through a gap and wrap one of its pony riders.
   - **Phase 2:** the ponies break off as three small rivals. Wrap them to crack the ring.
   - **Phase 3:** the ring winds into a spiral round the Keeper. Close your loop round its hub before the spiral reaches you.
2. **The Zamboni Swan:** a great ice machine that erases every ribbon in its wake.
   - **Phase 1:** it sweeps in straight lines and wipes out your work, so build behind it.
   - **Phase 2:** its wake freezes into ice tiles.
   - **Phase 3:** it chases you. Lure it over a snowbank to stall it, then wrap it.
3. **The Clockwork Conductor:** a segmented train of five cars.
   - **Phase 1:** the cars uncouple one at a time on the clock's chime. Wrap each loose car.
   - **Phase 2:** the tracks (conveyor lanes) switch on the beat.
   - **Phase 3:** the engine alone runs at full speed, drawing its own maze.
4. **The Loom Spinner:** a spidery loom in the centre that throws **shuttle threads** across the arena.
   - **Phase 1:** horizontal threads with gaps, each on a tell.
   - **Phase 2:** a woven grid with a moving hole.
   - **Phase 3:** it unravels. Each thread you wrap becomes yours, and the last loop closes round the loom.
5. **The Spool Itself** (secret): every Marshal's pattern in turn, then a four-colour ribbon duel.

#### Systems that run through the whole festival

- **Brake and turbo:** hold B to brake to half speed and A for turbo. This brings back the classic's push-pull speed control.
- **Slipstream:** riding within one cell of any ribbon refills turbo and builds a **slipstream chain**, paying more per cell as it grows. It is the risk-and-reward score engine.
- **Wrap-ups:** a closed loop up to a size limit fills with your colour. Your ribbon, the wall and pillars all count as sides. Everything inside is collected or wrapped. A wrap scores its area × the chain multiplier, and two wraps within 3 seconds chain.
- **Near-miss whiskers:** turning one cell away from a ribbon at speed pays a small bonus and throws a spark.
- **Pickups** appear on cells at set times:
  - **Snip:** the next ribbon cell you hit is cut instead of crashing you.
  - **Spool:** your ribbon lays two cells wide for 5 seconds.
  - **Eraser:** your oldest 40 cells vanish.
  - **Bow:** your next wrap's size limit doubles.
  - **Freeze Frame:** rivals pause for half a second.
  - **Turbo Spark:** refills turbo.
- **The Paint Shop:** spend festival tickets earned in play (never real money) on:
  - **Grip Tyres** (no turn delay on ice);
  - **Bigger Spool** (a larger wrap size limit);
  - a **Sidecar** (a spare rider);
  - a **starting Snip**;
  - cosmetic ribbon patterns (stripes, hearts, stars).
- **Medals** per arena: **Gift Wrapper** (wrap every rival), **Close Shave** (ten whiskers) and **No Brakes** (never brake).
- **Bigger actors:**
  - Move to 6 px cells on a 48 × 48 grid, so the bikes are about 10 × 16 px.
  - Each bike gets four-frame wheel and lean animations.
  - Every Marshal is its own large sprite.
- **Music:** one loop per fairground. The beat drives the gates, Glimmer's flash and the Conductor's chime, so every tell can be heard as well as seen.

#### Modes and players

The cabinet seats up to four (`maxPlayers: 4`), each rider on their own `players` frame.

- **Festival:** the campaign, solo or in co-op.
- **Co-op Festival:** two riders on one team against the crews. Teammates can pass through each other's ribbons, and a rider can wrap a rival against a partner's ribbon.
- **Versus:** 2–4 riders on any unlocked arena, best of five, with optional rival bots filling empty seats. The classic wall games' rule toggles are available:
  - wrap edges;
  - comet tails;
  - speed-up;
  - ribbons that erase after a crash.
- **Midnight Marathon:** endless rounds on random arenas against a growing crew. This is the leaderboard's main event.
- **Time Trial:** Tag Lap arenas against a ghost of your best run.

#### The classic's signatures, matched or beaten

- **The level ladder and the pick-your-game hub:** matched by the fairgrounds and the Festival Board.
- **Speed control:** matched by brake and turbo, and beaten by slipstream.
- **Escalating rival cycles:** beaten by 13 readable personalities instead of faster copies of one.
- **Two-player head-to-head:** matched and beaten by four-seat Versus with rule toggles, plus co-op.
- **Boxing a rival in:** beaten by wrap-ups, which reward drawing the box on purpose.

#### Slices

Roadmap: t-074 (slice 1), t-075 (slice 2), t-076 (slice 3), t-077 (slice 4). Slice 1 is `ready`; each later slice waits on the one before.


| Slice | Scope |
| --- | --- |
| 1 | Bigger grid, brake, slipstream, wrap-ups, whiskers, pickups, the first six rivals, the arena data format, music |
| 2 | Boardwalk at Dusk and Frostlight Rink, the Festival Board, the objectives, the Carousel Keeper and the Zamboni Swan, the Paint Shop, save/resume |
| 3 | Clockwork Bazaar and Starlight Loom, the remaining rivals, the Conductor and the Loom Spinner, the Rainbow Spool, endings, Encore |
| 4 | Co-op Festival, Versus with rule toggles, Midnight Marathon, Time Trial, medals |

- **Slice 1, the riding feel and the wrap-up.**
  - **Delivers:**
    - It moves the arena to 6 px cells (48 × 48) with bigger, animated bikes.
    - It adds a B brake beside the A turbo, plus slipstream chains and near-miss whiskers.
    - It adds the wrap-up rule: a closed loop under the size limit fills, and it wraps any rival or collects any pickup inside.
    - It adds the six pickups.
    - It splits today's single steering function into a rival-personality table. Roamer, Cutter, Copycat, Pacer, Hugger and Dasher ship first, each with its own tell.
    - It adds a data format for arenas (pillars, gates, pads, wrap edges) in `utils/arcade/ribbonRiders/`, so that today's endless rounds play on authored layouts.
    - It adds the first music loop.
  - **Verified by:** a new `verifyRibbonRiders.test.ts` in `test:arcade-engine` covering:
    - wrap-up fill and rival capture;
    - slipstream;
    - brake;
    - a deterministic seeded round;
    - a pilot probe showing runs still end.
- **Slice 2, the first two fairgrounds.**
  - **Delivers:**
    - Boardwalk at Dusk and Frostlight Rink: ten authored arenas, their palettes, and the carousel, wrap-edge, ice, snowbank and turn-pad mechanics.
    - The Festival Board route map.
    - Five of the objectives (Last Rider Rolling, Gift Wrap, Glowbug Run, Ribbon Art, Tag Lap).
    - The Snowplow, Tandem and Lantern Kid rivals.
    - The Carousel Keeper and the Zamboni Swan, three phases each.
    - The Paint Shop and its ticket economy.
    - Save and resume at each fairground through `saves.ts`.
  - **Verified by:** a deterministic test that clears the first fairground by script, plus screenshots of every arena.
- **Slice 3, the last two fairgrounds and the endings.**
  - **Delivers:**
    - Clockwork Bazaar and Starlight Loom: ten more arenas, with gates on the beat, conveyors, bell pads, portals, comet tails and the spiral wall.
    - Parade Escort, the last objective.
    - The remaining rivals: Gatekeeper, Glimmer, Shield Rider and Sprinter.
    - The Clockwork Conductor and the Loom Spinner.
    - The Golden Bows and the secret Rainbow Spool with the Spool Itself.
    - The credits, the true ending and Encore (New Game+).
  - **Verified by:** a scripted full-campaign test and boss-phase tests.
- **Slice 4, the people slice.**
  - **Delivers:**
    - `maxPlayers: 4`, with each rider on their own `players` frame.
    - Co-op Festival, where teammates pass through each other's ribbons.
    - Versus for 2–4 riders, best of five, with bot fill and the four rule toggles.
    - Midnight Marathon as the leaderboard mode.
    - Tag Lap Time Trial with a best-run ghost.
    - The per-arena medal board.
  - **Verified by:** engine tests for four seats in one round and for each rule toggle.

---

## 11. Brick Bloom (Breakout / Arkanoid riff)


### What is in the game today

Taken from `brickBloom.ts` (1,449 lines) on kind_robots `main` (6fb4809), plus the registry row and an attract-mode probe.

| Area | Today |
| --- | --- |
| Stages | Endless. **Six wall formulas** (full bands, pyramid, checkerboard, diamond, two towers, gapped stripes) on one 12 x 9 grid, cycling. Stage 7 is stage 1's wall again with tougher numbers. Nothing is authored by hand. |
| Backdrop | One greenhouse, painted in **four sky tints** that cycle (dusk, moonlight, dawn, teal night). Same glass, hedge and soil bed every stage. |
| Crates | **One crate kind** with 1–4 hits (the top rows are toughest), plus **bolted crates** that never break (from stage 5, up to 8, placed at random). No moving, regrowing, exploding or switching crates. |
| Enemies | **One.** The gloom puff: it drifts in a box in the middle of the screen, takes 2 hits, and knocks the ball off at a random upward angle. One puff from stage 4, two from stage 7. |
| Power-ups | Five seeds: **W** (wide, 14 s), **S** (sticky), **M** (three balls, up to five), **C** (calm, 0.7x speed) and **+** (spare paddle). The drop chance falls from 16% to 9%. There is no laser, no warp and no piercing ball. |
| Player verbs | Move and launch. No spin, no aim help, no action while the ball is in flight. |
| Scoring | (9 − row) x 10 x hits per crate, 5 per chip, 100 x stage per puff, 1,000 x stage clear bonus. **No chains or combos.** Spare paddles at 20k, 60k and 120k only. |
| Difficulty | Crate toughness caps at stage 7, puffs at stage 7, seed chance at stage 8, ball speed at stage 11 and bolts at stage 12. **From stage 12 on, every stage is one of the same six walls at the same numbers.** |
| Pacing | The attract pilot (seeds 5, 9 and 13, lives held at 3) cleared stages 1–3 in 98–162 s each. **Stage 4 took 260–516 s, and its last three crates alone took 96–261 s.** The end of every wall turns into a hunt for the last crate. Four minutes into the demo, the screen showed stage 2 with two lone crates on an empty sky. |
| Structure | No boss, no ending, no route, no save. Solo only (`maxPlayers` unset). |

### Against the classic

Breakout (1976) and Arkanoid (1986) set the bar, and Arkanoid's 1987 sequel raised it:

- **33 authored rounds**: hand-made layouts with cages, gaps and shapes, each with its own colour scheme and border, ending in a **final boss round**.
- **Brick roles**: coloured bricks worth different points; silver bricks that need more hits the later the round; gold bricks that never break. The sequel added moving and regenerating bricks.
- **Seven capsules**: slow, catch, expand, three-ball disruption, **laser** (the paddle shoots), **break** (a warp gate opens to skip the round) and an extra life.
- **Hatch enemies**: several shapes float down from ceiling hatches, each with its own drift. They deflect the ball and pop when the ball or the paddle touches them.
- **The final boss**: a giant face that fires at the paddle and has to be hit again and again.
- Breakout's **speed steps** (after 4 and 12 hits, and when the ball reaches the back rows) and its **paddle shrink** after the ball first touches the top wall.
- **Route choice**: the sequel's two warp exits let the player pick the next round.
- Two players alternate turns.

**Verdict:** The greenhouse looks good, and Brick Bloom has the opening minutes of Arkanoid. Past that it falls short on every axis: six formula walls instead of authored rounds, one breakable crate kind plus a bolt, one enemy, five seeds with no laser or warp, no boss, no ending, no route choice, and no score depth beyond points per crate. The measured last-crate hunt (up to four minutes chasing three crates) is the opposite of the "newer, better" Silas asked for. It is below the bar.

### The upgrade: Brick Bloom — The Glasshouse Grand Tour

Brick Bloom becomes a tour of five glasshouses that the gloom has darkened. Each house has its own crates, pests, weather and boss. The signature idea is that **the flowers you free stop being decoration**. They drift down and plant themselves in the soil bed under the paddle, and a bed in full bloom bounces a missed ball back into play. Playing fast and well builds your own safety net. It is a kind, visible system the classic never had.

**Target length:** a first clear in about 45–60 minutes across 30 walls and 5 bosses, with 45 authored walls in total, so a second run takes a different route.

#### Structure

- **Five glasshouses** and a secret sixth, the **Moonflower Conservatory**.
- Each glasshouse is a small **branching map of 9 authored walls**. Every wall has two exit vents (left and right) that pick the next wall: the left vent is usually the safe route and the right the rich one. A run passes through **5 walls, then the house boss**.
- Each house brings its own crate types, a new pest, a backdrop and tile set, a music loop, a title card and a seed it introduces.
- Between houses comes the **Potting Bench** shop (below).
- Progress saves at each glasshouse through `utils/arcade/saves.ts`.
- A clear rolls credits and unlocks **Second Bloom** (New Game+: mirrored walls, faster ball and the bed starts bare).

#### The glasshouses

| # | Glasshouse | Wall mechanic | New crates | New pests | Seed introduced |
| --- | --- | --- | --- | --- | --- |
| 1 | **Seedling House** (dawn) | Today's walls, rebuilt as authored layouts with cages and gaps | **Sprout crate** (always drops a seed), **hinge crate** (swings open and shut like a gate on a beat) | Gloom puff, **pollen mite** | **R: Rain Spray** (the paddle sprinkles droplets upward that chip crates; the laser) |
| 2 | **Vine Hall** | **Vine crates** regrow from a root crate every few seconds until the root is cracked; a **trellis row** slides left and right | Root and vine crates, **trellis crates** | **Snail bot**, **ladybot ring** | **T: Thorn Ball** (pierces crates for 8 s) |
| 3 | **Cactus Dome** (desert house, noon) | **Prickle crates** speed the ball up; **sand-timer crates** are unbreakable while their sand runs, then flip | Prickle, sand-timer and **puffball crates** (burst and crack all eight neighbours, so chains are possible) | **Tumbleweed**, **shell beetle** | **V: Vent** (a side vent opens; fly the ball out to skip the wall, as with Arkanoid's break) |
| 4 | **Lily Pond House** | The lower third of the wall is **under water**: the ball moves slow and floaty there. **Lily-pad crates** drift on a current. | Lily-pad, **bubble crates** (pop into a short-lived bumper) | **Frog bot**, **mirror bug** | **D: Duo Paddle** (a second paddle bot hovers above yours) |
| 5 | **Night Bloom House** | **Dark walls**: only the ball's glow and lit **lantern crates** show the crates, and a cracked **glow crate** lights its row for a while | Lantern, glow and **switch crates** (cracking one toggles every bolt of its colour) | **Moth**, plus remixes of all earlier pests | **Q: Queen's Compass** (shows the ball's path two bounces ahead for 10 s) |
| ★ | **Moonflower Conservatory** (secret) | Every mechanic remixed on mirrored walls, the fastest ball, seeds everywhere | All | All | All |

#### The roster: 1 → 9 pests

Every pest is bonked by the ball or the paddle, never hurt. A bonked pest pops into petals.

| Pest | Behaviour and tell | Answer it asks for |
| --- | --- | --- |
| **Gloom puff** (today) | Drifts and frays before it shoves the ball. Its deflection becomes readable: it always shoves the ball away from its face. | Two hits; keep the ball off its face side |
| **Pollen mite** | Sways down from roof vents in a line of three (the hatch enemies) | Pop the line for a petal chain |
| **Snail bot** | Crawls along the tops of crates and **re-seals cracks** behind its silver trail | Knock it off its ledge before it reaches the tough crates |
| **Ladybot ring** | Five dots orbit one crate and shield it | Break the ring dot by dot, then crack the crate |
| **Tumbleweed** | Rolls along the soil bed **flattening your blooms**; a dust puff at the wall is the tell | Bonk it with the ball before it reaches your best bloom |
| **Shell beetle** | Walks along a row, armoured at the front | Bank the ball in behind it |
| **Frog bot** | Puffs its cheeks for a second, then tongues the nearest falling seed | Catch the seed first, or bonk the frog while it puffs |
| **Mirror bug** | Splits a **ghost ball** off yours. The ghost cracks nothing and fades in 4 s. | Follow the ball that casts a shadow on the glass |
| **Moth** | Drawn to the ball's glow, it bends the ball's path toward itself; its wings flash orange when it locks on | One hit while it dives |

#### The bosses: 0 → 5, plus a secret duel

1. **Mister Mulch** (Seedling House): a compost-crate golem hanging from the roof.
   - Phase 1: crack the crate plates that armour its face.
   - Phase 2: it drops dirt clods. A clod that lands on the paddle makes it sluggish for 2 s, and the paddle can bonk clods away.
   - Phase 3: it lowers and sweeps side to side. The last hit makes it sneeze a shower of flowers.
2. **The Tangle Rose** (Vine Hall): a thorny rose bush.
   - Phase 1: three vine roots at the edges feed its shield; crack them.
   - Phase 2: petal volleys rain down. A hit stuns the paddle; it doesn't cost a life.
   - Phase 3: its vines become brick walls that sweep down the screen. Hit the bud through the gaps.
3. **Sunny Saguaro** (Cactus Dome): a cactus robot with spinning arms that knock the ball around.
   - Its flower crown blooms on a visible count, and it can only be hit while blooming.
   - In phase 2 it lobs prickle balls that split off as extra balls. Catch them for bonus points.
4. **Queen Koi** (Lily Pond House): a great clockwork koi circling under the lily pads.
   - Hit her as she leaps.
   - Phase 2: she flips the lily pads.
   - Phase 3: she stirs a whirlpool that spirals the ball toward the centre.
5. **The Gloom Bloom** (Night Bloom House): the giant dark bud that smothered the glasshouse lights and seeds every gloom puff.
   - Phase 1: relight its four lanterns.
   - Phase 2: its petals open and close like shutters; hit the core when they open.
   - Phase 3: it sends puffs to smother your bloom bed.
   - The last hit opens it into a moonflower, and the houses light up.
6. **Thorn** (Moonflower Conservatory, the true finale): a shadow paddle bot playing Breakout back at you from the top of the screen, with a shared wall between you. Crack the crates on its side and get the ball past it. When beaten it admits it was lonely, joins the garden, and becomes player 2's paddle in the credits.

#### Systems that run through the tour

- **The Bloom Bed** (the signature). Each cracked crate's flower drifts down and plants in one of eight bed plots under the paddle. A plot grows from bud to bloom as flowers land in it. A **plot in full bloom bounces one missed ball back up**, then drops back to a sprout. The bed is drawn big and bright, so its state is always readable, and the tumbleweed and the Gloom Bloom threaten it.
- **Pollen Chain:** every crate cracked between paddle touches adds to a chain (x1, x2, x3 … x8). The ball's trail changes colour with each step, and touching the paddle cashes the chain in. Puffball crates make big chains possible.
- **Last-Crate Rush:** fixes the measured hunt. When four or fewer breakable crates remain:
  - **Bumble**, a helper bee bot, loops around the nearest one.
  - The ball curves gently toward the crates that are left (10% steering).
  - A rush bonus counts down, so clearing fast pays.
- **Leaf Curl:** hit the ball with the paddle moving and press B for a curve shot. The ball bends for half a second, so the player can aim, not just move.
- **Ball heat:** speed steps you can read. The ball glows gold, orange then white as it speeds up, the classic's speed steps made visible. Calm and a bloom-bed save cool it a step.
- **Roof chime:** hitting the roof glass rings a chime and doubles the next crate's points. Breakout punished the top wall with a smaller paddle; this rewards the risky shot instead.
- **Seeds 5 → 10:** W, S, M, C and + stay. R (Rain Spray), T (Thorn Ball), V (Vent), D (Duo Paddle) and Q (Queen's Compass) are new. Short timers show in the HUD as today.
- **The Potting Bench** opens between houses. Spend petals earned in play (never real money) on:
  - a starting seed;
  - a wider base paddle;
  - two bloom plots pre-grown;
  - an extra Bumble pass;
  - a **vent hint** that marks the rich route on the house map.
- **Golden seeds:** one is hidden in a vault crate in each house. All five open the Moonflower Conservatory.
- **Medals per wall:** Clean (no ball lost), Quick (under par time) and Full Chain (an x8 Pollen Chain), with a medal board per house.

#### Modes and players

- **Grand Tour:** the campaign.
- **Endless Greenhouse:** walls stitched from authored chunks on a seeded rng, the leaderboard's main event.
- **Daily Wall:** one wall seeded from the date, the same for everyone that day, one attempt on the board.
- **Time Attack:** per glasshouse, unlocked on a clear.
- **Two paddles** (`maxPlayers: 2`, through the cabinet's `players` frames):
  - **Co-op:** a sky paddle and a leaf paddle share the lane and the balls. Passing the ball between them extends the Pollen Chain.
  - **Pollen Duel:** a versus mode on the Thorn layout. One player plays from the top and one from the bottom, racing to crack their own colour of crates.

#### The classic's signature features, matched or beaten

| The classic had | Brick Bloom will have |
| --- | --- |
| 33 authored rounds | 45 authored walls on five branching maps, plus endless and daily walls |
| Silver and gold bricks | Tough and bolted crates plus 14 more crate kinds, with moving, regrowing, exploding, switching and timed crates |
| Seven capsules including laser and break | Ten seeds including Rain Spray (the laser) and Vent (the warp) |
| Hatch enemies | Nine pests, each with its own tell and answer |
| One final boss | Five bosses with phases, and a paddle-versus-paddle finale |
| Speed steps, top-wall paddle shrink | Visible ball heat, and a roof chime that rewards the top wall |
| Two exits (sequel) | Two vents on every wall, choosing a safe or rich route |
| Two players alternating | Co-op on one lane, and the Pollen Duel |

#### Slices

Roadmap: t-078 (slice 1), t-079 (slice 2), t-080 (slice 3), t-081 (slice 4), t-082 (slice 5). Slice 1 is `ready`; each later slice waits on the one before.


**Slice 1 — The bloom core.** Brick Bloom's walls become **authored data**: string layouts with a legend for crate kinds, replacing the six pattern lambdas. The slice adds:
- the **Bloom Bed** safety net;
- the **Pollen Chain** multiplier;
- **Last-Crate Rush** with Bumble;
- the **Leaf Curl** shot;
- readable **ball heat** and the **roof chime**;
- the first new crates (sprout, hinge, puffball);
- the first new seeds (R Rain Spray, T Thorn Ball, Q Queen's Compass).

Verified by an attract-pilot probe showing stage times no longer blow out at the end of a wall. The target is the last three crates in under 30 s on the probe seeds.

**Slice 2 — Seedling House and Vine Hall.** The first two glasshouses: 18 authored walls on two branching vent maps, with root/vine and trellis crates. It also brings:
- the **pollen mite**, **snail bot** and **ladybot ring**;
- **Mister Mulch** and **The Tangle Rose** with their phases;
- the **Potting Bench**, golden seeds 1–2, the house map screen and title cards;
- save/resume at each house through `saves.ts`.

**Slice 3 — Cactus Dome and Lily Pond House.** Houses 3–4: prickle, sand-timer, lily-pad and bubble crates, and the under-water ball physics. It adds:
- the **tumbleweed**, **shell beetle**, **frog bot** and **mirror bug**;
- the V (Vent) and D (Duo Paddle) seeds;
- **Sunny Saguaro** and **Queen Koi**;
- golden seeds 3–4.

**Slice 4 — Night Bloom House, the Conservatory and the endings.** The dark-wall renderer (ball glow, lantern and glow crates), switch crates and the **moth**. It adds:
- **The Gloom Bloom**;
- the secret **Moonflower Conservatory** and the **Thorn** duel;
- credits, the true ending and **Second Bloom** New Game+.

**Slice 5 — Two paddles and the modes.** `maxPlayers: 2`, with co-op (a shared lane and chain passing) and the **Pollen Duel** versus mode. It adds:
- **Endless Greenhouse** (the leaderboard mode);
- **Daily Wall**;
- per-house **Time Attack**;
- the medal board per house and a mastery ladder for the how-to-play page.

---

## 12. Pixel Hop (Q*bert riff)


### What is in the game today

Taken from `pixelHop.ts` (1,428 lines) on kind_robots `main` (6fb4809).

| Area | Today |
| --- | --- |
| Board | **One** 7-row pyramid of 28 cubes, the same shape every round. Two escape discs per round, placed at random on rows 2–5. |
| Rules | **Four painting rules** that cycle by level, at 4 rounds a level: one hop paints; two hops via a halfway colour; finished tiles flip back; and both at once. Level 5 repeats level 1's rule. |
| Colour schemes | **Four**, cycling per round: palette swaps of the same space backdrop. Round 9 looks exactly like round 1 (seen in the demo at level 3). |
| Foes | **Four**: the red gumball (bounces down), the purple gumball that hatches into **Boing** (chases you), the green gumball (a freeze pickup, 4 s) and the **repaint gremlin** (undoes paint; catch it for 300). At most 4 on the board and one Boing at a time. |
| Discs | Lure Boing off for 500; each unused disc pays 50. |
| Scoring | 25 per paint; round bonus 1,000 + 250 per round; extra hopper every 12,000. No combos. |
| Difficulty | The gremlin chance caps at round 10, the enemy hop rate at round 11 and the drop rate at round 12. **From round 12 (level 3, round 4) on, every round is the same**; rules repeat every 4 levels and colours every 4 rounds. The demo was at level 3 four minutes in. |
| Missing | No sideways foes, no rule demonstration between levels, no special tiles, no boss, no ending, no save. Solo only. |

### Against the classic

Q*bert (1982):

- **9 levels x 4 rounds** (36 rounds). Each level adds a rule: intermediate colours, toggling, and toggling with an intermediate step. The cube colours change round by round.
- **Seven foes**:
  - red balls;
  - the purple ball that hatches into the chasing snake;
  - the green ball (freeze);
  - **two green imps** who turn tiles back and can be caught;
  - **two purple creatures who run along the cube sides**, at right angles to gravity, coming in from the bottom corners. They are the classic's most surprising threat.
- **Discs** lure the chaser off the edge for big points, and leftover discs pay a bonus.
- **An intermission** before each new level, in which the hero demonstrates the new rule.
- The famous cursing speech balloon when you're caught. Pixel Hop already has its own "#?%!".
- Two players alternate turns.

**Verdict:** Pixel Hop is the most faithful of these six riffs. It has the rules, the chaser, the discs, the freeze and the repainter. That is the problem: it is a careful reduction of Q*bert, not more. It lacks the sideways pair and the rule demonstrations, and it stops escalating at round 12 with nothing new after. The classic only ever had one pyramid, so a single board matches it; "newer, better, even more awesome" needs boards that change shape, tiles that do things, and a destination.

### The upgrade: Pixel Hop — The Painted Planets

Pip hops from planet to planet across a candy galaxy where every planet is a different kind of hop board: pyramids, rings, bridges, floating islands and towers. The signature idea lives in the game's name: **Pixel Hop paints pixel art**. On picture boards, every tile has its own target colour from a small palette, and a mini-map in the HUD shows the picture you are painting. You plan your route like a puzzle while the foes hunt you. A finished picture is added to the **Gallery**: a smiley, a flower, the arcade hosts, a robot cat.

**Target length:** a first clear in about 45–60 minutes across 36 rounds and 6 bosses, the classic's round count, plus a secret planet.

#### Structure

- **Six planets** and a secret seventh, **the Blank Canvas**.
- Each planet has **6 rounds**:
  - rounds 1–4 teach and remix the planet's rule and board shape;
  - round 5 is a **picture board**;
  - round 6 is the **boss board**.
- Every new rule opens with a **rule demonstration** (the classic's intermission): Pip shows it on a 3-tile mini-pyramid in a speech panel before the round starts.
- Every planet has its own sky, cube art, music loop and title card.
- A planet map between planets; progress saves at each planet.
- A clear unlocks **Repaint** (New Game+: harder rules on every board, and foes 20% faster).

#### The planets

| # | Planet | Board shapes | New tile | New rule | New foes | Boss |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | **Candy Comet** | Today's pyramid, plus a wide pyramid (8 rows) | — | One hop; two hops (today's rules) | Gumball, Boing, mint freeze, gremlin (today's four) | **Gumball Machine Max** |
| 2 | **Rondo Ring** | A **ring** of cubes with an inside edge and an outside edge, and a **bridge** board | **Spring tile** (launches you two cubes along the line) | Flip back (today's rule 3) | **Skitter & Scoot**, the sideways twins | **Ringmaster Rattle** |
| 3 | **Glacier Moon** | A pyramid with an ice field, and a **twin-peak** board | **Ice tile** (you slide one more cube the way you hopped) | **Cycle**: each hop advances the tile through three colours and wraps | **Snowball Sid**, **frost flake** (freezes you, not them, for 1 s) | **The Snow Globe** |
| 4 | **Clockwork Planet** | A **tower** (stacked rings) and a **gear** board | **Conveyor tile** (carries you one cube after you land) | Both at once (two hops plus flip back) | **Tick-Tock**, **Boing & Doing** (two chasers) | **Grandfather Cog** |
| 5 | **Bubble Nebula** | **Floating islands**: three small pyramids joined only by bubble discs | **Paint bucket tile** (paints its neighbours to target) | **Picture boards** become standard rounds | **Bubble ghost**, **Mirror Pip** | **The Bubble Queen** |
| 6 | **Rainbow Core** | Boards that **rebuild themselves** between rounds | **Star tile** (4 s of stomp-anything) | Every rule, remixed | **Smudge**, plus all foes | **Coil King** |
| ★ | **The Blank Canvas** (secret) | One huge picture board in five layers | All | Picture plus cycle | All | — (the final picture is the whole crew) |

#### The roster: 4 → 13 foes

| Foe | Behaviour and tell | Answer it asks for |
| --- | --- | --- |
| Gumball (today) | Bounces straight down at random | Stay out of its column |
| Boing (today) | Hatches at the bottom and chases | Lure him off a disc |
| Mint gumball (today) | The freeze pickup | Grab it |
| Repaint gremlin (today) | Hops down undoing paint | Catch it |
| **Skitter & Scoot** | Enter from the bottom corners and run along the **cube sides**, sideways to gravity; a corner glow is the tell | They never use your diagonal, so plan along it |
| **Snowball Sid** | Rolls down, **grows each hop** and unpaints its path | Catch him while he's small, or freeze him |
| **Frost flake** | Drifts down; touching it freezes Pip for 1 s | Avoid it |
| **Tick-Tock** | Hops strictly on the beat and paints the wrong colour; you hear a metronome | Hop on the off-beat and land on him from behind to catch him |
| **Boing & Doing** | Two chasers working as a pincer | A disc lures only the nearer one, so split them first |
| **Bubble ghost** | Drifts slowly; touching it traps Pip in a bubble that floats up a row | Keep moving, or use it as a free lift |
| **Mirror Pip** | Copies your hops **mirrored** across the board's middle. He paints too, but bonks you if you meet. | Plan symmetric routes so he paints the other half for you |
| **Smudge** | Invisible except for its footprints; it undoes paint | Read the footprints and catch it |
| **Paint bucket bot** (friendly) | Waddles down from the top | Catch it before it falls off and it paints a 3-tile splash |

#### The bosses: 0 → 6

1. **Gumball Machine Max** (Candy Comet): a giant gumball dispenser at the apex.
   - Paint the ring of tiles around its coin slot to make it sneeze. Three sneezes win.
   - Each phase spits gumballs in faster patterns (lines, then spirals).
2. **Ringmaster Rattle** (Rondo Ring): a spinning top bot circling the ring.
   - Paint the tiles ahead of it to target so it slips and spins out, then hop onto it to bonk it.
   - Phase 2 reverses its direction; phase 3 sends the sideways twins in with it.
3. **The Snow Globe** (Glacier Moon): a giant globe-bot that shakes ice across the board.
   - Land on the four **crack points** while they glow.
   - Every shake turns tiles to ice and changes the sliding routes.
4. **Grandfather Cog** (Clockwork Planet): a clock-face board.
   - Paint the hour tiles **in order** while the hands sweep rows clear.
   - Every phase, the board turns a notch.
5. **The Bubble Queen** (Bubble Nebula): she floats islands away in bubbles.
   - Finish an island's picture to pop her bubble and pull it back.
   - In the last phase all three islands drift at once.
6. **Coil King** (Rainbow Core): a giant Boing on a mega-spring.
   - He crushes rows when he lands, with a shadow tell.
   - Phase 2 sends spring twins.
   - In phase 3 the discs fly free, and you lure him off the last disc.
   - He boings off into the stars and comes back as a friend in the credits.

#### Systems that run through the campaign

- **Picture boards** (the signature): per-tile targets drawn from a 3–4 colour palette, shown in a HUD mini-map. A finished picture goes to the **Gallery**, and a no-miss picture earns a gold frame.
- **Rules 4 → 8:** one hop, two hops, flip back, both, **cycle**, **picture**, **cycle-picture**, and **ink trail** (foes leave their colour behind).
- **Board shapes:** any set of iso cells, not just a pyramid. Rings, bridges, towers, twin peaks and islands are authored as data.
- **Special tiles:** spring, ice, conveyor, paint bucket and star.
- **Hop combos:**
  - **Stripe:** paint a whole row in one run.
  - **Prism:** finish a 3-cube triangle.
  - **Speed Paint:** clear the board under par.
- **Rainbow discs:** from planet 3, some discs also paint the row they pass.
- **Medals per round:** Clean (no lost hopper), Combo (three Stripes) and Swift.
- **Golden brushes:** one per planet, earned on a no-miss picture board. All six open the Blank Canvas.

#### Modes and players

- **The Painted Planets:** the campaign.
- **Endless Pyramid:** the classic-rules marathon on today's pyramid, now never plateauing: a new foe joins every 4 rounds from the roster. It is the leaderboard's main event.
- **Picture Puzzle:** a gallery of 30 picture boards unlocked through the campaign, with no foes, played for fewest hops.
- **Two hoppers** (`maxPlayers: 2`):
  - **Co-op:** Pip and Pep paint one board together. Landing on the same tile at once is a **High Five** bonus.
  - **Paint War** (up to 4 players on the big ring and island boards): every player paints their own colour, and the most tiles at the bell wins. Bonks are a 1 s stun, never a knockout.

#### The classic's signature features, matched or beaten

| The classic had | Pixel Hop will have |
| --- | --- |
| 36 rounds, rules that change by level | 36 campaign rounds, 8 rules, 6 bosses and a secret planet |
| The chasing snake and the disc lure | Boing, Boing & Doing, the Coil King, and rainbow discs |
| Sideways creatures on the cube sides | Skitter & Scoot |
| Repainting imps | The gremlin, plus Smudge (footprints only) |
| The green freeze ball | The mint gumball, plus the star tile |
| Rule intermissions | A rule demonstration before every new rule |
| One pyramid | Rings, bridges, towers, twin peaks, islands and self-rebuilding boards |
| One colour target | Picture boards: you paint pixel art |

#### Slices

Roadmap: t-083 (slice 1), t-084 (slice 2), t-085 (slice 3), t-086 (slice 4), t-087 (slice 5). Slice 1 is `ready`; each later slice waits on the one before.


**Slice 1 — The board and rule engine.** Generalise the board from a fixed 7-row pyramid to **data-defined iso cell sets**, with their own disc slots and fall edges. It adds:
- the **special tiles** (spring, ice, conveyor, paint bucket, star);
- the rule engine with **cycle** and **picture** rules and the HUD mini-map;
- **Skitter & Scoot** with sideways movement on cube faces;
- the **rule demonstration** intermission;
- Stripe, Prism and Speed Paint combos;
- Endless Pyramid's foe unlock every 4 rounds, replacing the round-12 plateau.

**Slice 2 — Candy Comet and Rondo Ring.** Planets 1–2: 12 rounds including the wide pyramid, ring and bridge boards and two picture boards. It adds:
- **Gumball Machine Max** and **Ringmaster Rattle**;
- the planet map and title cards, the **Gallery** and golden brushes 1–2;
- save/resume per planet.

**Slice 3 — Glacier Moon and Clockwork Planet.** Planets 3–4: twin-peak, tower and gear boards and the ice and conveyor tiles. It adds:
- **Snowball Sid**, the frost flake, **Tick-Tock** (beat-synced) and **Boing & Doing**;
- **The Snow Globe** and **Grandfather Cog**;
- rainbow discs.

**Slice 4 — Bubble Nebula, Rainbow Core and the Blank Canvas.** Multi-island boards joined by discs, and boards that rebuild themselves. It adds:
- the **bubble ghost**, **Mirror Pip** and **Smudge**;
- **The Bubble Queen** and **Coil King**;
- the secret five-layer Blank Canvas, endings and **Repaint** New Game+.

**Slice 5 — Two hoppers and the modes.** `maxPlayers` up to 4: co-op with the High Five bonus, and **Paint War** for up to four. It adds:
- **Picture Puzzle** mode with its 30-board gallery;
- medal boards and a mastery ladder.

---

## 13. Glitch Garden (Centipede riff)


### What is in the game today

Taken from `glitchGarden.ts` (1,190 lines) on kind_robots `main` (6fb4809).

| Area | Today |
| --- | --- |
| Field | One lawn, 30 x 36 cells, with a 6-row flowerbed. **34 lamps are planted once**, at the start of wave 1, and kept for the whole game. One cached backdrop for every wave. The worm's colours never change. |
| Foes | **Four**: the glitch-worm, the beetle and the moth below, plus the **loose heads**: one-segment heads, none on wave 1, one more each wave up to 5 at wave 7. |
| Foe behaviour | The **glitch-worm** has 12 segments and splits where it is hit; the piece behind grows a head. The **beetle** comes from wave 2: it zig-zags through the bed, eats lamps, and pays 300/600/900 by distance. The **moth** comes from wave 2 too: it dives when the bed has fewer than 5 lamps, plants lamps on the way down, takes 2 hits, and speeds up after the first. |
| Missing behaviour | **No scorpion analog and no poison**, so the worm never plunges. **No new heads enter from the sides** when the worm reaches the bed. The queue entry in `games.yaml` promises "heads that dive straight down once they reach the bed", but the code has none: in the bed the worm only zig-zags up and down. |
| Weapon | One beam on screen at a time. **No power-ups.** |
| Flowers | Bloomed lamps and sprouts become flowers that are **pure decoration**, kept up to 120 at a time. |
| Scoring | 100 per head, 10 per body segment, 1 per lamp bloom (5 per sprout), 200 per moth, 300/600/900 per beetle; extra sprayer every 12,000. No multipliers. |
| Difficulty | Speed caps at wave 3; loose heads and the beetle timer cap at wave 7. The worm's `length` curve is flat at 12. The `lamps` curve is read only once, at wave 1, so its 55 cap is dead config. **From wave 7 on, every wave is the same**, except the beetle's speed creeps up without a cap. |
| Visual | Four minutes into the demo (wave 11): the same dusk lawn, the same purple worm, and a field choked with lamps and flowers. The sprites are 6–8 px on a 240 x 304 screen. |
| Structure | No boss, no ending, no save. Solo only. |

### Against the classic

Centipede (1981), and Millipede (1982), which built on it:

- **Four foes, four answers**:
  - the **centipede**, which splits, and whose heads speed up;
  - the **spider**, which zig-zags in the player zone, eats mushrooms, and scores by distance;
  - the **flea**, which drops when the player zone thins, plants mushrooms, takes 2 hits and speeds up;
  - the **scorpion**, which crosses the upper field **poisoning mushrooms**. A centipede that touches a poisoned mushroom **dives straight down**.
- **New heads enter from the sides** while the centipede lingers in the player zone.
- **Each wave** the centipede has one more head and one fewer body segment, and **the whole palette changes**.
- Damaged and poisoned mushrooms are restored at death for points.
- Rapid fire, one shot on screen: getting closer fires faster.
- **Millipede** added:
  - earwigs, inchworms (shoot one and everything slows), bees, dragonflies, mosquitoes and a beetle that turns mushrooms into flowers;
  - **DDT bombs** in the field that clear a radius when shot;
  - mushrooms that **creep down a row** each wave;
  - bonus swarms;
  - a **start-wave select**.

**Verdict:** Glitch Garden has three of Centipede's four foes and the split, and its beetle even pays by distance like the classic. But it has no scorpion and no poison (the one thing that makes the classic's centipede plunge at you), no side-entering heads, no palette change per wave and no power-ups. It has one lawn forever, decorative flowers, and a difficulty curve that stops at wave 7. It is missing a feature its own queue entry promised. It is below the 1981 game and far below its 1982 sequel.

### The upgrade: Glitch Garden — The Four Seasons of the Glitch

A garden-tending bot defends and restores a walled garden through a year of seasons, chasing the glitch to its root. The signature idea is the **Prism Garden**: **the flowers you bloom power your beam**. A fix-it beam that passes through a bloomed flower takes on that flower's power:
- **pink** splits the beam in two;
- **gold** makes it pierce;
- **cyan** freezes the worm segment it hits for 2 s;
- **violet** makes the beam home a little.

Where you bloom flowers becomes a strategy: you build your own firing lanes. The flowers that are wallpaper today become the game's depth. Nothing like it existed in the classic.

**Target length:** a first clear in about 45–60 minutes across 8 gardens (40 waves) and 4 season bosses, plus a secret garden.

#### Structure

- **Four seasons** of two gardens each, a **season boss** after each pair, and a secret **Midnight Garden**.
- Each garden has **5 waves**:
  - waves 1–2 introduce the garden's mechanic and foe;
  - wave 3 is the **special wave** (an objective);
  - waves 4–5 remix it with everything so far.
- Every garden has an **authored lamp layout** (fixing today's one-time scatter), its own backdrop and palette, and a palette shift every wave (the classic's colour change).
- Lamps **creep down a row** between waves (Millipede's drift), so the field never chokes the way today's wave 11 does.
- Between gardens comes the **Compost Shed** shop. Progress saves at each garden, and a **garden select** unlocks as you reach each one (Millipede's start-wave select).
- A clear unlocks **Overgrown** (New Game+: longer worms, faster heads, a fuller field).

#### The gardens

| Season | # | Garden | Mechanic | New foes | Special wave |
| --- | --- | --- | --- | --- | --- |
| Spring | 1 | **Kitchen Plot** | Today's lawn, with the prism flowers | Worm, loose heads, beetle, moth, **slime snail** (poison) | **First Bloom**: bloom a flower in each of four marked lanes |
| Spring | 2 | **Orchard Rows** | **Fruit trees** drop apples that are obstacles, or bonus points if you catch them | **Side-crawlers** (heads entering from the bed's sides) | **Apple Harvest**: catch 10 apples while the worm comes |
| Summer | 3 | **Sunflower Maze** | **Tall sunflowers** are walls that cannot be sprayed; the worm follows the lanes they make | **Dragonfly bot** | **Maze Runner**: fix the worm before it finds the maze exit |
| Summer | 4 | **Lily Pond** | A strip of **drifting lily pads** carries lamps and segments across | **Bee bots** (friendly) and the **wasp-glitch** that hides among them | **Pollinators**: escort three bee bots across without spraying them |
| Autumn | 5 | **Leaf Pile Lane** | **Falling leaves** cover lamps and soak up one shot; gusts blow them along | **Crow-bot** | **Rake Up**: clear the leaf piles from the bed |
| Autumn | 6 | **Pumpkin Patch** | **Pumpkins**: 2 x 2 obstacles that take 8 hits and burst into seed sprouts | **Inchworm**, **pumpkin roller** | **Great Pumpkin**: crack one giant pumpkin while it rolls toward the bed |
| Winter | 7 | **Frost Frame Greenhouse** | **Frost spreads** over lamps, and frozen lamps take 8 hits; **heaters** thaw a radius when sprayed | **Frost sprite** | **Warm Up**: light four heaters |
| Winter | 8 | **Snowball Hill** | The sprayer **slides on the icy bed**, and snowballs roll down the columns | **Snowball**, **mole-bot** | **Snow Day**: fix a worm made of snowball segments |
| ★ | 9 | **Midnight Garden** (secret) | Dark. Fireflies light the lamps, and your bloomed flowers glow. | Everything, remixed | — |

#### The roster: 4 → 15 foes

| Foe | Behaviour and tell | Answer it asks for |
| --- | --- | --- |
| Glitch-worm (today) | Splits where hit; the piece behind grows a head | Split it high, then pick off the heads |
| Loose head (today) | Zig-zags alone | Track the zig-zag |
| Beetle (today) | Zig-zags in the bed and eats lamps; pays 300/600/900 by distance | Let it come close for the 900 |
| Moth (today) | Dives when the bed thins and plants lamps | Two hits; the second must lead it |
| **Slime snail** (the scorpion) | Crosses the upper field and **glitches** every lamp it touches (they turn static-grey). A worm that meets a glitched lamp **dives straight to the bed.** | Fix the snail before it crosses, or bloom the glitched lamps |
| **Side-crawler** | Enters from the bed's sides while any worm has been in the bed more than 6 s | Clear the bed fast |
| **Dragonfly bot** | Darts across in straight bursts with a stop between (tell: its wings blur, then stop) | Lead the shot into the stop |
| **Bee bot** (friendly) | Carries pollen across the lawn. Spraying it costs the round's Kind bonus. | Hold fire |
| **Wasp-glitch** | Hides among the bees; its stripes jitter | Pick it out and fix it |
| **Crow-bot** | Swoops diagonally and **plucks a prism flower** | Fix it during the swoop |
| **Inchworm** | Inches along a row; fix it and **everything slows for 5 s** | A helper-foe: time it for a crowded moment |
| **Pumpkin roller** | Rolls down a column | Four hits; it bursts into sprouts |
| **Frost sprite** | Drifts and freezes the lamps it touches | Spray it before it reaches your lanes |
| **Snowball** | Rolls down a column, growing and flattening lamps | Spray it to shrink it before it lands |
| **Mole-bot** | A soil mound swells under the sprayer, then it pops up | Move off the mound |

#### The bosses: 0 → 4 season bosses, plus the Root Kernel

1. **Queen Wiggle** (Spring): a 24-segment rainbow glitch-worm with an armoured head.
   - Phase 1: she splits only at her coloured joints.
   - Phase 2: she splits into three worms that move in step.
   - Phase 3: her head detaches and buzzes the bed until fixed.
2. **Mow-Bot 3000** (Summer): a runaway lawnmower bot crossing the garden row by row, clearing lamps and heading for the bed.
   - Fix its three fuel caps.
   - It speeds up each phase and finally chases sideways in the bed.
   - Fixed, it parks and mows the garden into a neat pattern for the credits.
3. **The Gourd Hydra** (Autumn): a vine-worm with three pumpkin heads.
   - Each head can only be fixed while it is lit.
   - Fixing one makes the other two faster, and the last head rolls.
4. **The Frost Millipede** (Winter): a crystal millipede made of frozen lamps.
   - Thaw its segments with heater shots, bounced off the heaters you have lit, before they can be fixed.
   - In phase 3 it coils round the bed.
5. **The Root Kernel** (Midnight Garden, the true finale): the glitch's root, a giant bug living in the garden's code.
   - It rewrites the lawn's layout between phases.
   - It spawns each season's foes.
   - Its core opens only to a beam that has passed through all four prism colours.
   - Fixed, it reboots kindly and the whole garden blooms at once.

#### Systems that run through the year

- **Prism Garden** (the signature). The colour of a bloom is chosen by the lamp or sprout it came from (shown on the lamp's cap), not at random, so you can plan your lanes. Beams pick up flower powers in passing; a beam can carry two.
- **Sprinkler cans:** cans placed in the field. Spray one to burst a fix-it splash that clears a radius and chains to cans nearby (Millipede's DDT, made kind).
- **Patch multiplier:** consecutive hits without a miss raise a multiplier (x1 to x5) shown on the sprayer's nozzle. A miss drops it one step.
- **Poison and plunge:** glitched lamps make worms dive. The rule `games.yaml` promised now ships, with a readable static-grey lamp as the tell.
- **Side-crawlers and lamp creep** keep the bed tense and the field open.
- **Wave palettes:** every wave shifts the palette of the lawn, the lamps and the worm, so wave 11 never looks like wave 1.
- **The Compost Shed** between gardens. Spend petals earned in play (never real money) on:
  - a wider nozzle;
  - a second beam on screen;
  - a pre-bloomed prism flower in a chosen lane;
  - an extra sprinkler can;
  - a **snail siren** that chimes when a slime snail enters.
- **Golden trowels:** one per garden, for a no-miss special wave. All eight open the Midnight Garden.
- **Medals per wave:** Clean (no sprayer lost), Kind (no bee sprayed) and Full Patch (reach x5).
- **Readability:** sprites drawn at double density, so worm segments read as 12–14 px. Every foe gets a two-frame tell animation.

#### Modes and players

- **The Four Seasons:** the campaign, with garden select once reached.
- **Endless Lawn:** today's game with seasons rolling over every 5 waves. It brings in a new foe every wave until the roster is complete. It is the leaderboard's main event.
- **Daily Garden:** one seeded layout and foe mix per day.
- **Two sprayers** (`maxPlayers: 2`): co-op on one bed, each with their own beam. A **Crossfire** bonus pays when both beams fix the same worm within half a second, and prism flowers can be shared.
- **Garden Rivals:** a versus mode on a split bed. Each player owns half the lawn's lamps; fix the most worm.

#### The classic's signature features, matched or beaten

| The classic had | Glitch Garden will have |
| --- | --- |
| Centipede, spider, flea, scorpion | Glitch-worm, beetle, moth, and the slime snail, plus 11 more foes |
| Poisoned mushrooms and the plunge | Glitched lamps and the plunge, with a clear static-grey tell |
| Side-entering heads | Side-crawlers |
| Palette change every wave | A palette shift every wave and an authored look per garden |
| DDT bombs, mushroom creep, start-wave select (sequel) | Chaining sprinkler cans, lamp creep, garden select |
| Flowers from mushrooms (sequel's beetle) | The Prism Garden: flowers that power your beam |
| No boss, endless | Four season bosses, the Root Kernel and an ending |

#### Slices

Roadmap: t-088 (slice 1), t-089 (slice 2), t-090 (slice 3), t-091 (slice 4), t-092 (slice 5). Slice 1 is `ready`; each later slice waits on the one before.


**Slice 1 — Prism core and the classic's missing rules.** The **Prism Garden**: bloom colour chosen by the source, beam powers, and up to two powers per beam. The slice also adds:
- **sprinkler cans** with chaining;
- the **slime snail**, glitched lamps and the **plunge** (the `games.yaml` promise);
- **side-crawlers**, **lamp creep**, **wave palettes** and the patch multiplier;
- a data-driven garden format (authored lamp layouts, waves and objectives), retiring the dead `lamps` curve and capping the beetle's speed;
- double-density sprites.

Verified by a pilot probe through waves 1–10 and Pixel/HD screenshots.

**Slice 2 — Spring and Summer.** Gardens 1–4 (20 waves) with fruit trees, sunflower walls and drifting lily pads. It adds:
- the **dragonfly bot**, the **bee bots** and the **wasp-glitch**;
- the special waves;
- **Queen Wiggle** and **Mow-Bot 3000**;
- the **Compost Shed**, golden trowels 1–4, title cards;
- save/resume with garden select.

**Slice 3 — Autumn and Winter.** Gardens 5–8 with falling leaves, pumpkins, frost and heaters, and the icy bed. It adds:
- the **crow-bot**, **inchworm**, **pumpkin roller**, **frost sprite**, **snowball** and **mole-bot**;
- **The Gourd Hydra** and **The Frost Millipede**;
- golden trowels 5–8.

**Slice 4 — The Midnight Garden and the endings.** The dark garden, with firefly-lit lamps and glowing blooms, and **The Root Kernel** with its layout rewrites and its four-colour core. It adds:
- credits, the true ending and **Overgrown** New Game+.

**Slice 5 — Two sprayers and the modes.** `maxPlayers: 2`: co-op with the Crossfire bonus and shared prisms, and **Garden Rivals**. It adds:
- **Endless Lawn** with season rollover;
- **Daily Garden**;
- medal boards and a mastery ladder.

---

## 14. Lantern Swarm (Galaga riff)


### What is in the game today

`lanternSwarm.ts`, 1,400 lines. Registry entry: 224 x 288, solo (no `maxPlayers`), no mastery ladder. The only game-specific engine tests are the two twin-lantern docking checks in `verifyArcadeEngine.test.ts`.

| Area | Today |
| --- | --- |
| Stages | **One formation** (4 queens, 16 lunas and 20 moths: 40 in all), filled by the **same six entry groups** on the **same four entry paths** (two pairs of mirror images) every stage. |
| Visual variety | **Two skies**: the night sky for every normal stage, and the aurora for glow stages. The stage-10 screenshot is indistinguishable from stage 1. |
| Enemies | **Three**: moth (50, or 100 diving), luna (80/160) and queen (2 hits, 150/400; turns blue when hurt). **One dive shape**: a five-point sweep aimed at the lantern. Moths drop dust; entering moths drop dust too from stage 2. |
| Capture | 45% of a queen's dives (when not twinned) shine a tractor glow. Getting caught costs a lantern. Beaming the queen sends the lantern back to dock as **twin beams**, or as a spare if you have none. |
| Glow (challenging) stage | Every third stage. It is the **same 40 moths flying the same four entry paths** and off screen, every time: 100 each, 10,000 for all forty. One pattern, ever. |
| Bosses and escorts | None. Queens dive alone; there is no escort bonus and no transforming enemy. |
| Scoring | Diving moths pay double, a rescue pays 1,000, and extra lanterns come at 20,000 and then every 70,000. There is no hit-ratio or results screen. |
| Difficulty | Max divers 2 → 7 (capped at stage 6). Dive gap capped at stage 10, dust at stage 11, dive speed at stage 12. **From stage 12 on, every stage is the same stage.** |
| Players, ending, saves | Solo; none; none. |

### Against the classic

The 1981 game, and its sequels' additions:

- **Entrances change stage to stage**: different groups, different looping paths, different fill orders, and enemies that fire while they fly in.
- **Challenging stages cycle through several distinct choreographies**, each with its own enemy art, and the perfect bonus climbs.
- **Bosses dive with escorts**: shooting the escorts first and then the boss pays an escalating bonus.
- **Capture and the dual fighter.** The captured fighter then flies in the enemy formation and **turns against you**, and shooting it while it is held loses it for good.
- **Transforming enemies** in later stages: a regular enemy splits into a trio of new ones, with a bonus for getting all three.
- **The last few enemies dive non-stop and faster.** Stage badges count your progress.
- **A results screen**: shots fired, hits and hit-miss ratio.
- **Two players** (alternating).
- The sequels added **warps to new zones with branching routes**, bosses, power capsules, **multiple endings**, and a tractor that captures enemies as wingmen.

**Verdict:** Lantern Swarm's loop is right:

- the formation sways;
- dives sweep at you;
- the queen's glow and twin beams work.

But it is the classic's first two stages forever: one formation, one entrance, one dive shape, three moth kinds, one glow-stage pattern and two skies. There are no escorts, transforms, bosses, results, routes or co-op. The difficulty is flat from stage 12. Below the bar on every axis.

### The upgrade: Lantern Swarm — The Long Night Festival

One festival night, from dusk to dawn, over a city of lanterns. The moths aren't villains. They are dazzled by **the Glare**, a stray, too-bright light that rose at dusk, and your paper lantern guides them home one beam at a time. The night is a journey across the sky, with a **Sky Chart** of forking routes, so two runs need not see the same zones.

**The signature twist is the Welcome Glow and your Flock.**

- **Hold B** to open a soft, warm cone above the lantern. It drains a glow gauge, and beaming refills the gauge.
- **Befriend a moth:** a moth that **dives through the cone** while the gauge is full is befriended. It joins your **Flock**, up to four moths flying in a small formation around the lantern and beaming with you:
  - a moth adds a straight beam;
  - a luna adds an angled side beam;
  - a rescued queen adds a slow piercing beam.
- **Shield:** a Flock moth that is hit flutters home instead of costing a lantern.
- **Homecoming dive:** tap B to send the whole Flock on a dive into the formation that clears a column. Spending your shield to make a play is a decision the classic never asks for.

The queen's capture glow stays, and now it can take Flock moths as well as the lantern.

**Target length:** a first dawn in roughly 40–50 minutes, with a different route on the next run.

#### Structure

- The night has **five Watches** (acts): Dusk, Evening, Midnight, Small Hours and Dawn.
- Dusk and Dawn are single zones. **Evening, Midnight and Small Hours each fork** into two zones, and you choose a branch on the Sky Chart at the end of each Watch. That makes **eight zones**, and any one run visits five.
- Each zone has **six stages**:
  - three formation stages;
  - a **Glow Stage** (the challenging stage, with its own choreography);
  - a fourth formation stage that remixes the zone;
  - a **Guardian** (boss) stage.
- Each zone has its own sky, parallax layers, moth art and palette, music loop and title card.
- **Entrances are data**: groups, paths, fill order and entry fire are scripted per stage, so stage 2 of a zone no longer flies stage 1's entrance.
- A **results card** after each Watch shows shots, hits, hit ratio, Flock size, perfect Glows and escort bonuses. The game-over screen shows the whole night's ratio.
- Progress saves at each Watch start through `saves.ts`.

#### The zones

| Watch | Zone | Sky and mechanic | New moths | Glow Stage (its own art) | Guardian |
| --- | --- | --- | --- | --- | --- |
| Dusk | **Rooftop Festival** | Today's sky, with paper lanterns rising through the parallax | Moth, luna, queen, **escort lunas** | **Paper Cranes**: a figure-of-eight weave | **The Grand Lantern Moth** |
| Evening (left) | **Orchard Canopy** | Treetop silhouettes along the bottom. **Fireflies** blink across the screen and light it. | **Cocoon moth**, **firefly sparker** | **Falling Leaves**: a spiral down and back up | **The Silk Spinner** |
| Evening (right) | **River of Lights** | A river reflects the formation along the bottom; **floating candles** drift past as cover | **Skimmer**, **dust duster** | **Fish Kites**: a long serpentine school | **The Heron Kite** |
| Midnight (left) | **Thunderhead** | **Cloud banks** hide parts of the formation; **lightning** flashes reveal dark storm moths on a beat | **Static moth**, **cloud puffer** | **Raindrops**: columns that fall then loop | **The Storm Drummer** |
| Midnight (right) | **Aurora Sea** | **Aurora curtains** bend beams that pass through them, the way the curtain leans | **Comet moth**, **mirror moth** | **Starlings**: a murmuration that splits in two | **The Aurora Ribbon** |
| Small Hours (left) | **Old Clocktower** | **The formation turns like a clock face**: the swarm rotates slowly around a hub instead of swaying | **Pendulum moth**, **chime moth** | **Clock Hands**: two sweeping arms | **The Clockwork Owl** |
| Small Hours (right) | **Moon Garden** | **Moonflowers** in the formation open and close and swallow beams while open | **Moon moth** (front shield), **mimic lantern** | **Petals**: rings that bloom outward | **The Moonflower Queen** |
| Dawn | **Dawn Bonfire** | The sky warms stage by stage to sunrise; every earlier trick is remixed | All of them | **Sunrise**: all forty in a fan | **The Glare** |

#### The roster: 3 → 15 moths

| Moth | What it does, and its tell | The answer it asks for |
| --- | --- | --- |
| **Moth, luna** | As today, but with dive shapes from a library (sweep, loop, zig-zag, and swoop-and-return-from-below). | Beam them diving for double. |
| **Queen** | As today: two hits and the capture glow. | Dodge the glow, or let her take your lantern to win twins. |
| **Escort luna** | Peels off with a diving queen, one on each side. | Beam both escorts, then the queen: 800 → 1,600 → 3,200. |
| **Cocoon moth** | Mid-dive it wraps itself in silk (**tell:** a shimmer), then splits into three fast moonlets. | Beam all three for a bonus, or beam it before it wraps. |
| **Firefly sparker** | Can only be hit while it is lit; it blinks on a rhythm. | Beam on the beat. |
| **Skimmer** | Crosses the screen just above the lantern in a sine wave that has one gap. **Tell:** a ripple on the river horizon. | Slide into the gap, or beam it as it lifts. |
| **Dust duster** | Fans out a wide curtain of dust. **Tell:** its wings shake. | Get right under its body: the safe pocket. |
| **Static moth** | Fires a zig-zag spark. **Tell:** a crackle and a glow. | Sidestep at the zig. |
| **Cloud puffer** | Drops a cloud layer that hides the formation. | Beam through the cloud on a lightning flash, or clear it with a Homecoming dive. |
| **Comet moth** | Enters **from below the lantern** and dives upward. **Tell:** a glow on the bottom edge of the screen. | Slide away, then beam it on the way past. |
| **Mirror moth** | Mirrors your left and right movement from the top of the screen. | Move so it walks into your beam. |
| **Pendulum moth** | Swings on a silk thread under the formation. | Time the swing; beam the thread for a bonus. |
| **Chime moth** | On the clock's chime the whole formation dives at once. **Tell:** the bell glows. | Clear its row before the chime. |
| **Moon moth** | Shielded from the front. | Hit it when it turns side-on in a dive, or with a luna's side beam. |
| **Mimic lantern** | A moth carrying a fake captive lantern that flickers the wrong colour. Beam it and it bursts into dust. | Read the flicker. Your real captive lantern flies in the formation and **drops dust on you**, as in the classic. |

**Last-moth frenzy:** the final three moths of every stage dive without stopping and get faster each pass.

#### The Guardians: 0 → 8

Every Guardian is its own fight with phases and telegraphs.

1. **The Grand Lantern Moth** (Rooftop).
   - **Phase 1:** four wing panels, each a separate target.
   - **Phase 2:** it sweeps a wide capture glow across the screen.
   - **Phase 3:** its body dives with a ring of escorts.
2. **The Silk Spinner** (Orchard). It hangs on three threads; beam them to lower it into range. It drops cocoons that hatch into moonlets, and in its last phase it emerges as a giant moonlet trio.
3. **The Heron Kite** (River). A huge kite skimming the river. Its reflection shows where it will dive next. Beam its tail ribbons to make it stall.
4. **The Storm Drummer** (Thunderhead). A cloud creature beating three drums. Each drum calls lightning down a lane on the beat. Silence the drums one by one, and each lost drum changes the rhythm.
5. **The Aurora Ribbon** (Aurora Sea). A long segmented ribbon weaving through the curtains. Each beamed segment drifts off as a friendly moth, and the head speeds up as the ribbon shortens.
6. **The Clockwork Owl** (Clocktower). The formation orbits it as a clock face, and its two hands sweep the screen. Beam the gears behind each hand to stop it; then the owl swoops.
7. **The Moonflower Queen** (Moon Garden). Petal shields open and close around her. Phase 2 captures your Flock, and you win them back by beaming the petals that hold them.
8. **The Glare** (Dawn, the finale).
   - **Phase 1:** a blinding orb ringed by orbiting moths. Beam its four prisms.
   - **Phase 2:** it captures your lantern and your whole Flock in one beam. Rescue them with a single remaining lantern.
   - **Phase 3:** it dims and softens. Guide it down with the Welcome Glow until it settles as the festival's centre lantern, and the sun rises.

#### Endings, power and meta

- **Endings:**
  - **Dawn:** the plain clear.
  - **True ending:** reach Dawn with a full four-moth Flock and every Glow Stage on your route perfect. Every moth of the night flies a lantern parade across the sunrise.
- **Festival charms** float down from perfect Glow Stages and from escort bonuses. They are short and readable:
  - **Paper Crane**: wide beam;
  - **Sparkler**: rapid beam;
  - **Moon Mirror**: blocks one hit of dust;
  - **Kite String**: beams curve toward the nearest moth.
- **The Lantern Workshop** opens between Watches. Spend festival tokens earned in play (never real money) on:
  - a twin start;
  - an extra lantern;
  - a larger glow gauge;
  - a starting charm;
  - a **route hint** that shows which zone hides more charms.
- **Medals per stage:** Perfect Glow, Full Flock and No Dust, with a medal board per zone.

#### Modes

- **Festival:** the campaign.
- **Lantern Duet:** two players at once through the cabinet's `players` frames, which is better than the classic's alternating turns.
  - Two lanterns share the sky.
  - Touching lanterns **link** them into a Duet Lantern with a combined, wide beam until one is hit.
  - Either lantern can rescue the other's captive.
- **Endless Night:** the classic loop with every zone's tricks in rotation; the leaderboard's main event.
- **Glow Gallery:** practise any Glow Stage seen, unlocked on a clear.

#### Classic features: matched or beaten

| The classic has | Lantern Swarm answers with |
| --- | --- |
| Changing entrances | Scripted entrances per stage |
| Several challenging-stage patterns | Eight Glow choreographies with their own art |
| Escort bonus | Kept |
| Capture, dual fighter and the turncoat captive | Kept, and the captive now drops dust on you |
| Transforms | Cocoon moths |
| Last-enemy frenzy | Kept |
| Results screen | A results card after each Watch |
| Warps and routes | The Sky Chart forks |
| Bosses | Eight Guardians |
| Multiple endings | Dawn and the true ending |
| Two players | Simultaneous Duet with link-up |
| Capturing enemies as wingmen | **Beaten**: Flock moths are shields you can spend as a Homecoming dive |

#### Slices

Roadmap: t-093 (slice 1), t-094 (slice 2), t-095 (slice 3), t-096 (slice 4), t-097 (slice 5). Slice 1 is `ready`; each later slice waits on the one before.


**Slice 1: Formation engine and the Rooftop Festival.**
- Data-defined entrance scripts: groups, paths, fill order and entry fire.
- A dive-shape library: sweep, loop, zig and swoop-from-below.
- Escort lunas and the escort bonus; the last-moth frenzy.
- The turncoat captive lantern.
- The per-Watch results card with hit ratio.
- Zone 1, Rooftop Festival, with its sky, the Paper Cranes Glow Stage and the Grand Lantern Moth.
- `SWARM_CURVES` replaced by per-zone stage data.

Verified with the engine tests (including the existing twin-dock checks), a deterministic stage test, a pilot probe and screenshots.

**Slice 2: Welcome Glow, the Flock and the Evening fork.**
- The Welcome Glow cone and gauge.
- The Flock: four slots, per-kind beams, shield behaviour and the Homecoming dive.
- Festival charms.
- The Sky Chart route screen.
- The Evening fork:
  - Orchard Canopy: cocoon moths, firefly sparkers, the Falling Leaves Glow and the Silk Spinner;
  - River of Lights: skimmers, dust dusters, the Fish Kites Glow and the Heron Kite.

**Slice 3: The Midnight and Small Hours forks.**
- Thunderhead: cloud banks, lightning, static moths and cloud puffers; the Storm Drummer.
- Aurora Sea: bending curtains, comet and mirror moths; the Aurora Ribbon.
- Old Clocktower: the rotating clock-face formation, pendulum and chime moths; the Clockwork Owl.
- Moon Garden: moonflowers, moon moths and mimic lanterns; the Moonflower Queen.
- Each zone's Glow Stage.

**Slice 4: Dawn and the endings.**
- The Dawn Bonfire zone and the Glare.
- The Dawn and true endings, and credits.
- The Lantern Workshop.
- Medals and the medal boards.
- Save/resume at each Watch start through `saves.ts`.

**Slice 5: Lantern Duet and the extra modes.**
- Two-player simultaneous co-op through `players` frames (`maxPlayers: 2` in the registry), with lantern link-up and cross-rescue.
- Endless Night.
- Glow Gallery.

---

## 15. Rover Ramble (Moon Patrol riff)


### What is in the game today

`roverRamble.ts`, 1,405 lines. Registry entry: 320 x 240, solo, no mastery ladder.

| Area | Today |
| --- | --- |
| Course | An endless line of 2,400 px sections, about 25 seconds each at cruise speed. They are lettered A–Z and then **loop back to A**; there is no course end. Obstacles are rolled at random along each section with a gap curve. |
| Visual variety | **One moonscape** for every section: a banded purple sky, one blue planet, three parallax mountain ranges and one track. The section-D screenshot is the section-A screenshot with a flag in it. |
| Obstacles | **Four**: craters (16 → 44 px wide; in pairs from section 3), small boulders, big boulders (two zaps: the first knocks them down to small) and **rollers** (from section 4, rolling toward you at 0.6 px/tick). Pebbles that land ahead dig fresh craters. |
| Enemies | **One**: "meteor sprite" saucers in trios (from section 2), flying a sine wave and dropping pebbles. There are no ground shooters, no mines and nothing coming from behind. |
| Weapons | A forward zap (one at a time, 170 px reach) and up-shots (three at a time), both on A. |
| Scoring | Small boulder 50, big boulder or roller 100, 50 for each obstacle jumped, saucer 150. A checkpoint pays 500 x section plus 100 per second under par. Extra rovers come at 10,000 and then every 20,000. |
| Difficulty | Widest crater at section 7, pebble rate at section 8, saucer wave gap at section 9, obstacle gap at section 10, par (26 → 20 s) at section 13. **From section 13 on, every section is the same section.** |
| Crash | Restart from the start of the section. |
| Players, ending, saves | Solo; none; none. |

### Against the classic

The 1982 game it riffs on is a **course**, not a loop:

- **Two courses** (beginner and championship), **each lettered A–Z with an end**. Major checkpoints every five letters give a time report against the average and your best, and finishing Z hands you the next course.
- **A real roster:** several kinds of saucer, including one whose bombs blast new craters and fast low ones. There are **tanks on the ground that shoot back**, **mines on the track** that must be jumped, **vehicles that chase you from behind**, rolling boulders, and **plants that grow up out of the ground**.
- **Speed sets jump length**, so the throttle is part of every jump, not just a pace setting.
- **The parallax backdrop changes** as the course goes on: different ranges, domes and skylines.
- Pace-setting jingles and a points summary at each major checkpoint.

**Verdict:** Rover Ramble's bounce-zap-jump loop works and its parallax is lovely. But it is one moonscape, four obstacles and one saucer, with no tanks, no mines, nothing from behind, letters that loop forever, no course end and no second course. It is flat from section 13. It is the classic's first five checkpoints, repeated.

### The upgrade: Rover Ramble — The Five Moons Rally

The rover is a goodwill courier on the **Five Moons Rally**, a race across five moons of one big ringed planet. It carries care crates to the outposts along the way, and each moon brings its own terrain physics. The meteor sprites aren't villains; they're pranksters, and the last leg reaches their mothership.

**The signature twist is the Tow Train.** At outposts the rover picks up **trailer pods**, up to three, that hitch behind it. Each pod gives a power:

- a **turret pod** fires backward and upward on its own, at pursuers;
- a **shield pod** takes a pebble meant for the rover;
- a **lamp pod** lights the dark side;
- a **magnet pod** pulls in moon gems;
- a **spring pod** gives a second jump in the air.

But **every pod follows the rover's exact track with a delay**. A jump timed for the rover alone can drop the last pod into a crater, losing the pod and its crate but not a life. The longer your train, the earlier and faster you have to jump. The classic's "speed sets jump length" rule becomes a fresh puzzle on every crater.

**Target length:** the Rally Course first clear in roughly 40–50 minutes. The Championship Course, a remixed second lap, takes as long again and holds the true ending.

#### Structure

- **The Rally Course runs A–Z across five moons**, five or six letters each:
  - Moon 1: A–E
  - Moon 2: F–J
  - Moon 3: K–O
  - Moon 4: P–T
  - Moon 5: U–Z
- **Sections are authored data**: scripted obstacle beats with seeded variation inside each beat. They run 35–60 s, so pacing varies instead of every section being the same length.
- **The last letter of each moon (E, J, O, T, Z) is an outpost with a Guardian fight.** Then comes the classic-style **checkpoint report**: time against par and against your best split, crates delivered, pods kept and gems.
- **Forks:** after each outpost the road splits.
  - The **ridge road** has more air threats and more gems.
  - The **canyon road** has more ground threats and a shorter par.
  - The HUD map shows the choice.
- Each moon has its own sky, planet phase, three parallax layers, track texture, palette and music loop.
- Clearing Z rolls credits and opens **the Championship Course**: the same five moons at night, with tighter gaps, mixed threats and new forks.
- Progress saves at each moon start through `saves.ts`.

#### The moons

| Moon (letters) | Terrain and physics | New threats | Guardian at the outpost |
| --- | --- | --- | --- |
| 1. **Pebble** (A–E) | Today's grey moonscape, tightened. Normal grip. **Ramps** launch long jumps. | Meteor sprite (today), **bomber saucer**, **landmine**, **dust devil** | **The Big Tumble** (E) |
| 2. **Rime** (F–J) | **Ice**: speed changes slowly (momentum), so the throttle has to be read early. **Ice bridges crack** behind you, so you can't slow down on them. **Icicle arches** overhead drop if you zap upward under them. | **Snowplough tank**, **skate pursuer**, **frost mine** | **The Glacier Grinder** (J) |
| 3. **Cinder** (K–O) | Volcanic glass. **Lava vents** erupt on a beat. **Geysers** fling the rover into huge jumps over long chasms. **Ash fall** hides what is ahead. | **Magma tank**, **cinder swooper**, **lava bubble**, **moon creeper** | **The Kiln Crawler** (O) |
| 4. **Prism** (P–T) | **Low gravity**: floaty, long jumps, and pebbles fall slower too. **Crystal arches** bend the forward zap upward. **Floating rocks** hang at jump height. | **Prism drone**, **gravity well**, **zig saucer** | **The Geode Matriarch** (T) |
| 5. **The Far Side** (U–Z) | **Night side**: only the headlight cone and the lamp pod light the road. **Flare pods** on the track light the sky for a few seconds. Every earlier threat is remixed. | **Mimic crate**, **shadow pursuer** | **Big Mischief**, the sprites' mothership (Z) |

#### The roster: 5 → 18 threats

| Threat | What it does, and its tell | The answer it asks for |
| --- | --- | --- |
| **Crater, boulder, big boulder, roller** | As today. | Jump or zap. Rollers now come in sizes. |
| **Meteor sprite** | Today's pebble dropper. | Up-zap, or change pace. |
| **Bomber saucer** | Flies high and drops a bomb that blasts a crater exactly where it lands. **Tell:** a whistle and a target ring on the track ahead. | Change speed so the new crater lands behind you, or jump it. |
| **Zig saucer** | Fast and low; it zig-zags at bumper height. | Up-zap on its high zig, or jump its low one. |
| **Landmine / frost mine** | Sits on the track and can't be zapped. **Tell:** a blinking sparkle. | Jump it. Mines punish zap-everything play. |
| **Snowplough / magma tank** | Parked ahead; fires a slow shell along the ground. **Tell:** its turret lifts. | Zap it twice, or jump the shell and then zap. |
| **Skate pursuer / shadow pursuer** | **Comes up from behind** and fires forward. **Tell:** a rear-view blip on the HUD and a horn. | The turret pod, or jump as it passes under you. Mirrors the classic's chasing vehicles. |
| **Dust devil** | A whirlwind crossing the track; it shoves your speed. **Tell:** a dust swirl. | Feather the throttle. |
| **Cinder swooper** | Dives at an angle. **Tell:** its shadow grows on the track. | Change pace. |
| **Lava bubble** | Rises out of a pit and pops. | Time the jump between pops. |
| **Moon creeper** | A vine that grows up across the track. **Tell:** a bud swelling for two seconds. | Zap the bud before it grows, or jump the full vine. A riff on the classic's plants. |
| **Prism drone** | Splits up-shots harmlessly. | Hit it with the forward zap from the top of a jump. |
| **Gravity well** | Lifts the rover and the train. | Steer the drop by holding speed, so the pods land clear. |
| **Floating rock** | Hangs at jump height in low gravity. | Zap it first, or keep the rover on the ground. |
| **Mimic crate** | A fake care crate that blinks off-beat. Hitch it, and it bites a pod off. | Read the blink. |

#### The Guardians: 0 → 5

1. **The Big Tumble** (E). A boulder golem.
   - **Phase 1:** it rolls at you, stops, and hurls rocks in arcs. **Tell:** a wind-up. Zap its knees.
   - **Phase 2:** it splits into three rollers of different speeds.
   - **Phase 3:** it curls up and bounces. Drive under the arc of each bounce.
2. **The Glacier Grinder** (J). A giant plough that **chases you from behind**; the scroll speed is forced.
   - **Phase 1:** it throws ice blocks over you, and they become obstacles. The turret pod hits its headlamps.
   - **Phase 2:** it carves a crevasse ahead of you; jump it with the whole train.
   - **Phase 3:** it overtakes, turns, and comes at you head-on. Zap its blade.
3. **The Kiln Crawler** (O). A long lava caterpillar that arcs out of one pit and into another across the track. **Tell:** the pit glows. Up-zap its glowing segments as it passes overhead. Each lost segment shortens its arc, until the head comes straight at you.
4. **The Geode Matriarch** (T). A crystal mothership, fought in low gravity.
   - **Phase 1:** its facets shield it. Hit them with the forward zap from the top of a jump.
   - **Phase 2:** a floating-rock barrage.
   - **Phase 3:** it sinks low, and its gravity lifts the rover. Steer between the shards in the air.
5. **Big Mischief** (Z, the finale). The meteor sprites' mothership.
   - **Phase 1:** it carpets the track with crater bombs.
   - **Phase 2:** it lifts your trailer pods with a tractor beam. Zap the beam to drop them back onto the train.
   - **Phase 3:** it lands and races you as a giant buggy. Jump onto its ramp at full speed. The sprites cheer, and the last crates are delivered.

#### Systems, power and meta

- **The Tow Train:** pods, crates and track-following lag, as above.
- **Care crates** pay **goodwill** (the currency) at each outpost.
- **The jump is fuller:**
  - holding Up gives a slightly higher jump;
  - landing on top of a boulder is a **stunt** (points);
  - jumping off a ramp at full speed earns a big-air bonus.
- **Outpost garages** between moons. Spend goodwill earned in play (never real money) on:
  - pods;
  - an extra rover;
  - paint jobs;
  - wider tyres (better grip on ice);
  - a **route scout** that previews the next fork.
- **Checkpoint reports:** a per-letter split board with par, your best split and a stamp for each:
  - Under Par;
  - No Scrape;
  - Full Train.
- **Moon gems:** five hidden per moon, high on the ridge roads or under canyon overhangs. Collecting all 25 is one of the conditions for the true ending.
- **Endings:**
  - **Rally finish:** the plain clear.
  - **True ending:** win the Championship Course with all 25 gems. The sprites throw a rally party and paint the rover gold.

#### Modes

- **Rally:** the campaign.
- **Championship:** unlocked by the first Rally clear.
- **Tandem:** two players through the cabinet's `players` frames, splitting the classic's two jobs.
  - Player 1 **drives**: throttle and jump.
  - Player 2 **is the gunner**: aims the zap up, forward or back, and runs the turret pod.

  It's a cabinet-native co-op that the solo classic never had.
- **Time Attack** per moon, against your best splits.
- **Endless Ramble:** today's loop with every threat in it; the leaderboard's main event.

#### Classic features: matched or beaten

| The classic has | Rover Ramble answers with |
| --- | --- |
| A–Z course with an end; major-checkpoint time reports | Kept, with outposts and reports |
| Two courses | Rally and Championship |
| Saucers that blast new craters | Bomber saucers |
| Ground tanks; mines; pursuers from behind; boulders; plants | Tanks; mines; pursuers with a rear-view tell; rollers in sizes; moon creepers |
| Speed sets jump length | **Beaten** by the Tow Train, which makes every jump a timing puzzle for the whole train |
| Changing parallax | Five moons, each with its own physics as well as its own art |
| No bosses, one player | Five Guardians; Tandem driver-and-gunner co-op |

#### Slices

Roadmap: t-098 (slice 1), t-099 (slice 2), t-100 (slice 3), t-101 (slice 4). Slice 1 is `ready`; each later slice waits on the one before.


**Slice 1: Course engine and Moon 1.**
- Authored section beats with seeded variation, replacing `ROVER_CURVES`.
- The A–Z course with an end and checkpoint reports.
- The rear-view HUD and pursuers from behind.
- New threats: landmines, ground tanks, bomber and zig saucers, moon creepers and dust devils.
- Ramps and the stunt system.
- Moon 1, Pebble, with its own backdrop set and the Big Tumble.

Verified with the engine tests, a deterministic course test, a pilot probe showing runs end, and screenshots of each moon.

**Slice 2: The Tow Train, outposts, Rime and Cinder.**
- The Tow Train: pods with track-following lag, care crates and goodwill.
- Outpost garages.
- Rime: ice momentum, cracking bridges and icicle arches; snowplough tanks and skate pursuers; the Glacier Grinder.
- Cinder: lava vents, geysers and ash; magma tanks, cinder swoopers and lava bubbles; the Kiln Crawler.
- Save/resume at each moon start.

**Slice 3: Prism, the Far Side and the endings.**
- Prism: low gravity, crystal arches, floating rocks, prism drones and gravity wells; the Geode Matriarch.
- The Far Side: headlight darkness, flare pods, mimic crates and shadow pursuers; Big Mischief.
- Route forks, moon gems, credits and the Rally ending.

**Slice 4: Championship, Tandem and modes.**
- The Championship Course remix and the true ending.
- Tandem driver-and-gunner co-op through `players` frames (`maxPlayers: 2`).
- Time Attack with per-letter splits.
- Endless Ramble.
- Stamps and medal boards.

---

## 16. Hedgehog Crossing (Frogger riff)


### What is in the game today

| Area | Today |
| --- | --- |
| Board | **One** board for every level: five road lanes (two cars, a tractor, a racer, a two-tile bus), a grass median, five creek lanes (three of logs, two of turtles), and a hedge with five burrows. One backdrop. |
| Hazards | Traffic; the creek (land in the water or drift off the edge and it's a splash); **diving turtles** (with a short warning); the **fox**, who sleeps in a burrow for 4 s at a time from level 2; a 30 s timer per hedgehog. |
| Bonus | A **ladybug** visits an empty burrow (200 points). |
| Scoring | 10 per new row reached, 50 plus a time bonus per hedgehog home, 1,000 when all five are home. An extra hedgehog every 10,000. |
| Escalation | Lane speed rises; logs shrink by up to 2 tiles (at level 5); more turtle groups dive, but at most two per turtle lane, so that stops at level 3; the fox from level 2. **From level 11 on, every level is the same level**, and nothing new appears after level 2. |
| Missing | Nothing on the median or the logs; no creature in the creek that bites; no escort bonus; no change of board, time of day or season. |
| Players, saves, ending | Solo, with four lives, no save and no ending. |
| Look | A clean, readable board with good vehicle and turtle sprites, under a moon behind the hedge. It never changes. Four minutes into the attract demo, the pilot had reached game over on level 1 with three hedgehogs home. |
| Scale | `hedgehogCrossing.ts`, 1,704 lines. |

### Against the classic

The 1981 crossing game is one screen, but it keeps adding to it level by level:

- **Five road lanes and five river lanes to five homes** (matched), against the clock (matched).
- **New hazards with each level:** a **snake** on the median, and later on the logs; **crocodiles** in the river (ride
  the back, never the jaws) and crocodile heads waiting in the homes; **otters** that come at you in the water;
  **diving turtles**.
- **The escort bonus:** a little companion rides a log, and carrying it home pays big.
- **A fly in a home** for bonus points (matched by the ladybug).
- **Music that changes** with the section of the crossing.
- **Two players** taking turns.
- The genre's modern reinventions turned the crossing into **long scrolling journeys** across ever-changing terrain.

**Verdict:** Hedgehog Crossing has the classic's board and its bonus visitor, and its fox stands in for the home
lurker. But it stops at the first level's cast: no snake, no biting log, no escort, no new lane types. Once the turtles
dive and the fox wakes, nothing new happens: it is one board, one look, one level on repeat from 11. It is a faithful
level 1 of the classic and not much past it.

### The upgrade: Hedgehog Crossing — The Long Way Home

Autumn is ending, and the hedgehog family must travel from the city park to the old orchard to hibernate. The journey
crosses six regions, each a different kind of crossing: market streets, a railway and canal, farm fields, a frozen
pond, a storm-swollen gorge. Each region ends in a **Big Crossing**, a long scrolling set piece. Two twists:

- **The Family Parade:** lead a line of hoglets that follow your hops exactly.
- **Bristle Dash:** a double hop that rewards bold timing.

**Target length:** a first clear in roughly 45–60 minutes.

#### Structure

- The journey has **six regions** in **three legs** (acts), then the **Old Orchard** finale and a **secret region**.
- Each region has **four crossings**, then its **Big Crossing**:
  - crossings 1–2 introduce the region's lanes and creature;
  - crossing 3 is the region's **special crossing**, with its own objective;
  - crossing 4 remixes the region with everything learned so far;
  - the **Big Crossing** is a vertically scrolling board three screens tall, with checkpoints.
- Every region has its own lanes (as data), ground art, time of day, palette and music. The music changes between the
  land half and the water half of a board, as in the classic.
- **The Burrow Pantry** opens between regions (below).
- Progress saves at each region start.
- A clear rolls credits and unlocks **Spring Return**, a New Game+ that makes the journey back with a bigger family.

#### The regions

**Leg 1: Leaving Town**

| # | Region | Lanes and mechanic | New creatures | Special crossing | Big Crossing |
| --- | --- | --- | --- | --- | --- |
| 1 | **Park Lane** | Today's road and creek, retuned | **Grass snake** on the median (its tongue flicks before it turns), **lost hoglet** riding a log (escort it home), the fox, the ladybug | **Ladybug Hunt**: carry five ladybugs home. | **The Ring Road**: a ten-lane road with a roundabout whose traffic circles |
| 2 | **Market Day** | **Pedestrian lanes** of robot shoppers moving both ways; **delivery bots** that change lanes on a blinker; **barrels** rolling down a ramp lane. The water half is a **canal of floating crates**. | **Delivery bot**, **barrel**, **pigeon flock** (scatters across a lane when you land near it) | **Fruit Stall**: collect the fallen fruit before the stall robot sweeps it up. | **The Fair**: a carousel to ride and bumper cars to dodge |

**Leg 2: Across the Country**

| # | Region | Lanes and mechanic | New creatures | Special crossing | Big Crossing |
| --- | --- | --- | --- | --- | --- |
| 3 | **Railway and Canal** | **Trains** that clear a whole row (crossing lights and a bell for 2 s first); **canal locks** whose rows fill and drain, so a lane is water, then dry, then water; **barges** as long, slow platforms | **Train**, **swan** (hisses, then swims fast across its lane), **snapping log** (its eyes open before it yawns; ride its tail half) | **Signal Box**: the hedgehogs throw the signals; time a crossing between trains. | **The Swing Bridge**: the bridge swings open on a timer, mid-crossing |
| 4 | **Farm Fields** | **Combine harvester** (three tiles wide and slow; a dust cloud warns of it); **tractor trailers**; **sheep flocks** whose backs you can hop across (rideable lanes on land); **sprinkler rows** on a beat; **duck families** as moving platforms on the pond | **Combine**, **sheep** (friend), **ducks** (friend), **heron** (its shadow sweeps a creek column before it stabs) | **Round-up**: walk the hoglets across on the sheep. | **The Harvest**: the field is cut in sweeping passes as you climb it |

**Leg 3: Into the Storm**

| # | Region | Lanes and mechanic | New creatures | Special crossing | Big Crossing |
| --- | --- | --- | --- | --- | --- |
| 5 | **Frozen Pond at Dusk** | **Ice floes** that crack after two hops (the cracks show); **slippery ice** (land and slide one tile on); **snowploughs** that sweep a row and leave snowbanks as short-lived walls | **Skating bot** (weaves across lanes), **snowplough**, **ice floe** | **Lantern Walk**: carry a lantern; only the lit tiles are safe to read. | **The Thaw**: the floes break up as the board scrolls |
| 6 | **River Gorge in the Storm** | **Rapids** (fast creek lanes); **rope bridges** that sway, so your position drifts; **rafts**; a **waterfall row** that washes you back unless you're on a raft | **Heron**, **rapids raft**, **falling branch** (a shadow, then a crash across a lane) | **Rescue**: three hoglets stranded on rocks mid-river. | **The Flood**: the river rises behind you as the board scrolls up, a chase |

**Finale: The Old Orchard.** The hibernation hedge, deep in the fox family's patch.
- The **fox prowls the hedge row**, burrows open and close, and apples fall.
- The whole family must be home before the first snow, and the snowflakes are the timer.
- **Ending:** the family curls up under the leaves as the snow falls, followed by a spring flash-forward of the burrow,
  now with baby hedgehogs.

**Secret region: The Hidden Meadow.** A **golden acorn** is hidden in each region, earned by finishing its Big Crossing
with the full parade intact. With all six, a seventh region opens, with every lane type at full speed, and the **true
ending**: the whole hedgerow's animals gather for the family's spring wake-up.

#### The roster: 8 → 27 lanes and creatures

| Creature or lane | Tell | Answer |
| --- | --- | --- |
| Cars, tractor, racer, bus | As today | As today |
| Logs, diving turtles | Turtles bubble before they dive (today) | As today |
| Fox (burrow) | Sleeping "Z"s | Don't wake it; pick another burrow |
| Grass snake | Its tongue flicks before it turns | Never share its tile; time its turn |
| Snapping log | Its eyes open before it yawns | Ride the tail half |
| Delivery bot | Blinker light before a lane change | Read the blinker |
| Barrel | Rumbles down the ramp lane | Hop between barrels |
| Pigeon flock | Ruffles when you land near | Land, then wait a beat |
| Train | Crossing lights and a bell for 2 s | Never stand on the track when the lights flash |
| Swan | Hisses, then charges across | Wait out the charge |
| Barge, canal lock | The lock's water level gauge | Cross the lock when it's dry, or ride a barge |
| Combine harvester | A dust cloud ahead of it | Slip into the gap behind it |
| Sheep (friend) | Bleats as it starts to move | Ride its back across the field |
| Ducks (friend) | Quacks before the family turns | Ride the ducklings |
| Heron | Its shadow sweeps a column | Leave the column |
| Skating bot | Weaving trail | Read its weave |
| Snowplough | Flashing amber light | Cross ahead or behind; mind the snowbank |
| Ice floe | Cracks show after the first hop | Hop off on the second |
| Rapids raft | Fast-moving lane | Time the hop; the drift is strong |
| Falling branch | A shadow crosses the lane | Get out of the shadow |
| Fox (prowling) | Its ears show above the hedge | Read its patrol; dash past behind it |

#### Systems that run through the whole journey

- **The Family Parade (signature):**
  - pick up hoglets waiting on the median or riding a log (the classic's escort, multiplied);
  - up to three follow you in a line, each copying your hops one step behind;
  - a hoglet that is bumped scurries back to the start (no harm done) and the parade's multiplier drops;
  - getting the whole parade into one burrow pays a **Parade Bonus** of 1,000 × hoglets².
  It turns every crossing into planning a path the whole line can follow.
- **Bristle Dash:** B hops two rows at once, with a 3 s cooldown. It is a skill move for a gap that closes too fast,
  and a parade can follow it only if there is a safe tile for each hoglet.
- **Per-level escalation, past level 11:** in the endless modes the lane tables keep turning (new lane kinds, mixed
  directions, faster divers), so there is no plateau.
- **Visitors:** the ladybug stays; **worm snacks** pay points on the median; a **magpie** steals an uncollected bonus
  if you dawdle.
- **The Burrow Pantry** between regions: spend **acorns** gathered on the way (never real money) on a spare hedgehog,
  +5 s on the timer, an extra dash charge, a **lantern** for the night boards, or a **sniffer** hint that shows which
  turtle group dives next.
- **Medals per crossing:** Full Parade (three hoglets home in one trip), No Bumps (no life lost) and Quick Paws (under
  par).

#### Modes

- **Journey:** the campaign.
- **Endless Hedgerow:** an endless, seeded vertical crossing that mixes every region's lanes and keeps getting harder,
  the leaderboard's main event.
- **Daily Crossing:** an Endless Hedgerow seeded from the date, the same for every player that day, with its own daily
  board.
- **Co-op:** 2–4 hedgehogs through the `players` frames. Each can lead their own parade, and burrows are shared, so
  players plan who takes which.
- **Classic Crossing:** today's board and rules, kept.

#### Signature features to match or beat

| The classic's feature | Hedgehog Crossing |
| --- | --- |
| Five road lanes, five river lanes, five homes, a timer | Kept on Park Lane; every region has its own lanes |
| Snakes on the median and the logs | The grass snake |
| Crocodiles (ride the back, not the jaws) and lurkers in the homes | The snapping log and the fox |
| Otters in the water | Swans and herons |
| Diving turtles | Kept, with the bubble tell and the sniffer |
| The escort bonus | The Family Parade |
| Fly in a home | The ladybug, worm snacks and the magpie |
| Section music | Land and water music per region |
| Two players | 2–4 player co-op |
| Long scrolling journeys (modern reinventions) | Big Crossings and Endless Hedgerow |
| **Past the classic** | The Family Parade, Bristle Dash, six regions plus a finale, a daily seed, an ending |

#### Slices

Roadmap: t-102 (slice 1), t-103 (slice 2), t-104 (slice 3), t-105 (slice 4). Slice 1 is `ready`; each later slice waits on the one before.


1. **Lanes as data and the Family Parade.** Lanes and boards as data (lane kinds with their own update and draw); a real
   escalation table with no plateau; the grass snake, snapping log, heron and delivery bot with their tells; the lost
   hoglet escort and the Family Parade (follow-the-leader hops, bump-back, Parade Bonus); and Bristle Dash.
   Deterministic tests cover parade path-following, snake and log safety, and dash landing, and a pilot probe shows runs
   still end.
2. **Leg 1 and the scrolling engine.** Vertical scrolling with checkpoints for the Big Crossings; save/resume at region
   start; Park Lane and Market Day with their special crossings and Big Crossings (the Ring Road, the Fair);
   pedestrians, barrels and pigeons; land and water music; visitors (worm snacks, magpie); and the Burrow Pantry.
3. **Legs 2 and 3, the Old Orchard and the endings.** Railway and Canal (trains, locks, barges, swans), Farm Fields
   (combine, sheep, ducks, sprinklers), Frozen Pond (floes, ice, ploughs) and River Gorge (rapids, rope bridges, the
   waterfall), each with its special crossing and Big Crossing; the Old Orchard finale with the prowling fox; credits,
   the golden acorns, the Hidden Meadow and the true ending; and Spring Return New Game+.
4. **Endless and together.** Endless Hedgerow as the leaderboard event, Daily Crossing with a date seed and a daily
   board, co-op for 2–4 players through the `players` frames, Classic Crossing, and the medals with a board per region.
   Registry `maxPlayers` and the blurb and how-to lines are updated.

---

## 17. Burrow Buddy (Dig Dug riff)


### What is in the game today

| Area | Today |
| --- | --- |
| Field | **One** 16 × 14-tile garden. The starting tunnels, enemy burrows and turnips are placed at random each garden; nothing is authored. Three soil sets (four strata each) cycle by garden. The sky, sun, fence and flowers above never change. |
| Enemies | **Two.** The **grub** crawls the tunnels, chasing Buddy at junctions 70% of the time and turning at random otherwise, and ghosts through the soil every 520 → 220 ticks. The **beetle** does the same, plus a 40-tick glow and then a 2-tile flame along its row that passes through soil. Grubs go 3 → 5 (garden 3) and beetles 0 → 3 (gardens 3, 5 and 7). The blurb says beetles arrive "from the second garden", but `Math.floor` of the 0.5 step puts the first beetle in **garden 3**. |
| Enemy behaviour | A ghost is harmless until it settles back into a tunnel. Once a garden is 5 seconds old, the last enemy floats for the top-left corner and escapes. That is all the behaviour there is. |
| Puffing | Reach of 3 tiles. Four puffs pop an enemy; a puffed enemy deflates after 50 ticks. A pop pays by depth (200, 300, 400 or 500), and double for a beetle puffed side-on. |
| Turnips | 3 → 5 per garden (garden 6), placed at random. Dig under one and it wobbles for 40 ticks, then falls. Crushes pay 1,000 → 12,000 by the number caught, and a falling turnip can bonk Buddy. |
| Bonus | Two dropped turnips bring out **one** veggie in the centre for 10 seconds: always a **carrot**, worth 400 × garden up to 8,000. |
| Difficulty | Grubs max out at garden 3, beetles and turnips by garden 7, the ghost timer at garden 9 and speed at garden 13. **From garden 13 on, every garden is the same garden.** |
| Structure | Endless numbered gardens. The only objective is to puff them all. There are no bosses, no ending, no saves and no music. The HUD shows up to ten flower markers, which are cosmetic. |
| Players | Solo. |
| Code | `burrowBuddy.ts`, 2,099 lines. The seed-5 attract pilot was out in garden 5 after about 80 seconds. |

The screenshots show some of the prettiest art in the hall: the banded strata, the picket fence and the sky. Buddy and the grubs read well on 16 px tiles. But garden 2 and garden 5 are the same rectangle with different tunnels.

### Against the classic

The 1982 game is compact, and Burrow Buddy already has most of its core:

- two enemies;
- ghosting through the soil;
- an escaping last enemy;
- depth scoring;
- double points for puffing the fire-breather side-on;
- rocks that crush groups;
- the vegetable after two rocks.

What it lacks:

- **The vegetable ladder.** The classic shows a different vegetable for each band of rounds, each worth more than the last, up to a top prize. That gives you a reason to drop rocks round after round.
- **Round identity.** The soil colours change with groups of rounds, flower markers count the rounds (a small flower for 1, a big one for 10), and the early rounds have authored starting layouts.
- **Fire through the soil that you learn to read,** with the fire-breather turning to face you.
- **Escalating pressure.** In later rounds the enemies ghost more often and the last one escapes sooner.
- **Fault lines.** The sequel let you **break the ground apart along fault lines** and sink whole chunks with the enemies on them. It is the series' best idea, and it is missing entirely.
- **Two players**, taking turns.

**Verdict:** Burrow Buddy is the closest of the six to its classic, but the classic is a short loop, and this keeps only its opening: one carrot instead of a ladder of prizes, random gardens instead of authored ones, three palettes, and flat by garden 13. It needs to go where the sequel went, and further.

### The upgrade: Burrow Buddy — The Year Under the Garden

Buddy digs through a whole year beneath one great garden: **four Seasons**, each a different underground world, from the spring topsoil down to the warm deep at the bottom. Above ground, the garden visibly grows with every patch Buddy makes safe.

The signature twist is **slumps**. Soil is held up by what's around it. Cut a cracked block free on its sides and the whole block slides down, carrying turnips, stones and grumps with it. It is the sequel's fault lines turned on their side, and it makes every garden a puzzle as well as a chase.

**Target length:** a first clear in roughly 45–60 minutes.

#### Structure

- The campaign has **four Seasons** (acts) of **six gardens** each, a **Season Grump** (boss) at the end of each, a **finale** and a secret **Moonlit Greenhouse**.
- Each garden is authored data: the starting tunnels, stones, turnips and slump blocks, the grump roster and burrows, the objective, a par time and medals.
  - Gardens 1–2 of a Season teach its new idea.
  - Garden 3 is the Season's **special garden**.
  - Gardens 4–6 remix everything learned so far.
- **The surface garden:** each cleared garden plants its patch on the map above, so you can see how far down you have come.
- **The Potting Shed** opens between Seasons (below).
- Progress saves at each Season start through `utils/arcade/saves.ts`. A clear rolls credits and unlocks **Second Year**, a New Game+ with remixed gardens and faster grumps.

**Objectives** (all data-defined):

- **Puff Them All:** today's rule.
- **Plant the Seeds:** carry seeds from the surface down to glowing beds deep below.
- **Dig Out the Baby Moles:** they are trapped in pockets; reach them before a grump does.
- **Water the Roots:** dig a channel from a buried spring to a thirsty root (Seasons 3–4).
- **Keepsakes:** dig up five buried trinkets, two of them under slump blocks.
- **Worm Escort:** lead a lost worm up to the surface. The grumps chase the worm, not you.

#### The Seasons

| # | Season | Soil and mechanics | New grumps | Special garden | Season Grump |
| --- | --- | --- | --- | --- | --- |
| 1 | **Spring Topsoil** | Today's soil, tightened. **Slump blocks** arrive, along with **stones** that can't be dug and move only when a slump carries them. The veggie ladder starts. | Grub, beetle, **pill bug**, **mole cricket** | **Plant the Seeds** | **Queen Thimble** |
| 2 | **Summer Clay Caves** | **Clay** digs at half speed, but tunnels in clay never slump. **Dark pockets** are lit only round Buddy's headlamp. **Glowworm lanterns** light a whole chamber when puffed. | **Snail**, **firefly**, **mimic turnip** | **Keepsakes**, in the dark | **Old Kettle** |
| 3 | **Autumn Root Cellar** | **Roots** cross the soil as tough walls that only a slump can snap. **Water**: a buried spring flows down any tunnel you open to it (a simple cellular flow). It washes grubs along, slows Buddy and puts out fire. | **Root worm**, **termite crew** | **Water the Roots** | **The Tangle** |
| 4 | **Winter Frost Burrows** | **Frozen soil** can be dug only after a puff thaws it. **Ice tunnels** slide Buddy to the next junction. **Icicles** fall into open shafts on a tell. | **Frost spider**, **snow vole** | **Dig Out the Baby Moles** before the frost seals them in | **Grandmother Glacier** |
| Finale | **The Warm Deep** | One long garden that scrolls downward, remixing all four Seasons | All | — | **Wiggleworth** |
| ★ | **The Moonlit Greenhouse** (secret) | Glass soil you can see through, and every veggie on the ladder at once | All, at their fastest | — | — |

Each Season has one **Golden Seed**, earned by gold-medalling its special garden. With all four, the Moonlit Greenhouse opens. Clearing it gives the true ending: the whole garden above in bloom at night.

#### The roster: 2 → 12 grumps

| Grump | Behaviour | Tell | Answer |
| --- | --- | --- | --- |
| **Grub** | As today | — | Puff it, or crush it |
| **Beetle** | As today, but now turns to face you through the soil | Glows before its flame | Puff from the side for double |
| **Pill bug** | Curls into a ball that bounces puffs away | Curls up when you face it | Wait for it to uncurl, or slump on it |
| **Mole cricket** | Digs new tunnels of its own toward you | A spray of dirt ahead of it | Use its tunnels; trap it under a turnip |
| **Snail** | Slow; its shell bounces puffs from the front; leaves a slime trail that slows Buddy | A shiny trail | Puff it from behind |
| **Firefly** | Flies the tunnels of dark pockets; harmless, but lights Buddy up for every grump | Blinks before it dives | Puff it and it becomes a lantern instead |
| **Mimic turnip** | Looks like a turnip and bites | Blinks | Two puffs make it a real turnip |
| **Root worm** | Long and segmented: each segment needs its own puffs, and the head steers | The soil ripples along its path | Puff the head first and the body curls up |
| **Termite crew** | Three small termites that chew the props under slump blocks and set them off on Buddy | A chewing sound and wood dust | Puff the queen termite and the crew wanders off |
| **Frost spider** | Spins an ice web across a tunnel that blocks and slows | Glinting silk | Puff the web to melt it, then the spider |
| **Snow vole** | Burrows under the snow, then pops up beside you | A moving snow hump | Stand still and puff where it surfaces |
| **Ghost** (any grump) | As today | Goggle eyes drifting through soil | Wait until it settles back into a tunnel |

#### The Season Grumps: 0 → 5 bosses

1. **Queen Thimble:** a grub as big as a 3 × 3 room.
   - **Phase 1:** she tunnels along a visible ripple. Puff her as she surfaces; she needs 12 puffs and deflates fast.
   - **Phase 2:** she lays grublets, which must be cleared before she can be puffed again.
   - **Phase 3:** she ghosts through the soil. Slump a block onto her to finish.
2. **Old Kettle:** an armoured beetle who breathes steam along whole rows, through the soil, after a long tell.
   - **Phase 1:** rows of steam. Stay off her row.
   - **Phase 2:** drop turnips on her shell plates to crack them.
   - **Phase 3:** she charges through the soil. Dodge into a side tunnel and puff her soft underside.
3. **The Tangle:** a living knot of roots filling the bottom of the cellar.
   - **Phase 1:** tendrils dig toward Buddy, and slumps snap them.
   - **Phase 2:** the spring floods the cellar. Route the water through your tunnels to the Tangle's heart.
   - **Phase 3:** watered, it blooms, and the grumps it was hiding scatter for one last chase.
4. **Grandmother Glacier:** an ancient ice mole who freezes whole tunnels shut.
   - **Phase 1:** freeze waves, each on a tell.
   - **Phase 2:** icicle rain.
   - **Phase 3:** she curls into an ice ball that rolls through every tunnel. Slump a block into her path.
5. **Wiggleworth** (finale): the giant earthworm whose grumpy rumbling has been shaking the garden all year.
   - **Phase 1:** he passes through the field on huge ripples, and his rings must be puffed one by one.
   - **Phase 2:** the soil of every Season returns around him.
   - **Phase 3:** Buddy's puffs become **lullaby bubbles**. Sing him back to sleep, then dig for the surface ahead of the last rumble, a vertical escape that tops the year.

#### Systems that run through the whole year

- **The veggie ladder:** twelve prizes in Season order, worth 400 → 8,000: radish, carrot, turnip greens, mushroom, cucumber, eggplant, pepper, tomato, onion, pumpkin, watermelon and star fruit. A **Golden Beet** appears only after a five-grump crush.
- **Slump chains:** grumps carried down by a slump count toward the crush bonus, and a slump that sets off another slump multiplies it.
- **Readable moods:** a grump changes colour as it gets bored (calm, then restless, then ghost). The escaping last grump shows its path.
- **Bubble tools** come out of cracked stones:
  - **Wide Puff:** hits two grumps in a line.
  - **Long Puff:** reach of 5 tiles.
  - **Quick Puff:** three puffs pop.
  - **Drill Boots:** dig at walking speed for 10 seconds.
  - **Headlamp:** a wider light radius.
  - **Sprinkler:** washes a tunnel clear.
- **The Potting Shed:** spend seeds earned in play (never real money) on:
  - an extra Buddy;
  - a starting tool;
  - an extra turnip in the next garden;
  - faster digging;
  - a **map hint** showing where a Season's Golden Seed is.

  Prices rise each Season.
- **Medals** per garden: **Clean Dig** (no hit), **Big Crush** (three or more grumps in one crush) and **Under Par**.
- **Music:** one loop per Season, with a darker layer in the dark pockets.

#### Modes and players

- **The Year:** the campaign.
- **Two Buddies:** simultaneous co-op on one field (`maxPlayers: 2`, each Buddy on its own `players` frame). There is a teal Buddy and a pink Buddy, so one can puff while the other drops. A slump that would bonk your partner creaks and pauses for a moment first.
- **Deep Dig:** an endless vertical score attack. The field scrolls down as you dig, depth is your score, and slumps and grumps rise from below. This is the leaderboard's main event.
- **Garden Time Trial:** per garden, unlocked on a clear.

#### The classic's signatures, matched or beaten

- **The vegetable ladder:** matched, by twelve prizes and the Golden Beet.
- **Round identity:** beaten by authored gardens, four Season worlds and the surface garden.
- **Rocks that crush groups:** beaten by slumps, whole blocks of soil that carry everything with them.
- **Fire through the soil:** matched, and pushed further by Old Kettle's row-wide steam.
- **The sequel's fault lines:** matched by slumps, turned on their side.
- **Two players:** beaten by simultaneous co-op instead of taking turns.

#### Slices

Roadmap: t-106 (slice 1), t-107 (slice 2), t-108 (slice 3), t-109 (slice 4). Slice 1 is `ready`; each later slice waits on the one before.


| Slice | Scope |
| --- | --- |
| 1 | Garden data format, slump blocks and stones, the veggie ladder, moods, bubble tools, pill bug, mole cricket and mimic turnip, the beetle's arrival fixed to garden 2 |
| 2 | Spring and Summer (12 gardens), objectives, dark pockets, snail and firefly, Queen Thimble and Old Kettle, the Potting Shed, the surface garden, save/resume |
| 3 | Autumn and Winter (12 gardens), water flow, roots, frozen soil and ice tunnels, the remaining grumps, the Tangle and Grandmother Glacier, Wiggleworth and the escape, the Moonlit Greenhouse, endings, Second Year |
| 4 | Two Buddies co-op, Deep Dig, Garden Time Trial, medals |

- **Slice 1, soil that moves.**
  - **Delivers:**
    - An authored garden format (tunnels, stones, turnips, slump blocks, burrows, objective, par) in `utils/arcade/burrowBuddy/`. Today's endless loop runs on it.
    - Slump blocks that fall as one piece and carry turnips, stones and grumps, plus slump-chain scoring.
    - The twelve-veggie ladder and the Golden Beet.
    - Readable grump moods and a visible escape path.
    - The six bubble tools.
    - The pill bug, mole cricket and mimic turnip.
    - Beetles arriving in garden 2, as the blurb already promises.
  - **Verified by:** a new `verifyBurrowBuddy.test.ts` in `test:arcade-engine` covering slump physics, the crush count and a deterministic seeded garden.
- **Slice 2, Spring and Summer.**
  - **Delivers:**
    - Twelve authored gardens, the Season palettes and the clay, dark-pocket and glowworm mechanics.
    - The Plant the Seeds, Keepsakes and Worm Escort objectives.
    - The snail and the firefly.
    - Queen Thimble and Old Kettle, three phases each.
    - The surface-garden overworld.
    - The Potting Shed and its seed economy.
    - Save and resume per Season through `saves.ts`.
  - **Verified by:** a scripted clear of Spring and screenshots of every garden.
- **Slice 3, Autumn, Winter and the deep.**
  - **Delivers:**
    - Twelve more gardens.
    - Cellular water flow from buried springs: it carries grubs, slows Buddy and puts out fire.
    - Roots, frozen soil, ice tunnels and icicles.
    - The Water the Roots and Dig Out the Baby Moles objectives.
    - The root worm, termite crew, frost spider and snow vole.
    - The Tangle and Grandmother Glacier.
    - The Warm Deep finale with Wiggleworth and the vertical escape.
    - The Golden Seeds and the Moonlit Greenhouse.
    - The credits, the true ending and Second Year.
  - **Verified by:** a scripted full-campaign test and boss-phase tests.
- **Slice 4, together and endless.**
  - **Delivers:**
    - Simultaneous two-Buddy co-op through the `players` frames (`maxPlayers: 2`), with a partner-safe slump creak.
    - Deep Dig, the vertical scrolling score attack, as the leaderboard mode.
    - Garden Time Trial.
    - The per-garden medal board.
  - **Verified by:** engine tests for two seats and a Deep Dig pilot probe that ends.

---

## 18. Repair Rampage (Rampage riff)


### What is in the game today

| Area | Today |
| --- | --- |
| City | Endless numbered cities. Each has 2 → 4 towers (city 5), every tower 3 windows wide and 4 → 11 floors tall (city 6), with windows broken at random (45% → 90%, city 7). There is **one** backdrop for every city, the post-storm dusk with sun and rainbow, painted once. Towers cycle three masonry colours. |
| The robot | Bolt alone: walk, climb (8 ticks a window), fix (A), and shoo (A beside a drone). One charge meter of 100 drains a point every 2 seconds. There are no spare lives (`lives = 1`). |
| Threats | **One**: the news drone. It crosses at a random height, hovers for 40 ticks when level with Bolt, and flashes. A flash costs 15 charge and knocks Bolt off the wall. Up to 2 → 5 drones fly at once. |
| Towers | Each tower has a stability timer: 10 seconds of grace plus 2.6 → 1.1 seconds per broken window. It wobbles in its last 10 seconds, then falls, costing 25 charge, or 45 if Bolt is on it. |
| Window contents | Glass, and nothing else. One **kitten** at a time appears at a broken upper window for 9 seconds (500 × city). Each fix has a 3% chance of giving 12 charge. |
| Scoring | 100 per fix, 150 per shoo, 500 × city per kitten, and 1,000 × towers standing × city per cleared city. No chains, no row or tower bonuses. |
| Difficulty | Tower count maxes at city 5, height at 6, damage and drone count at 7, the drone rate at 8, and tower patience and drone speed at 11. **From city 11 on, every city is the same city.** |
| Structure | No bosses, no city identities, no ending, no saves and no music. |
| Players | Solo. |
| Code | `repairRampage.ts`, 1,638 lines. The seed-5 attract pilot ran out of charge in city 6 after about 95 seconds. |

The screenshots show the best backdrop of the six, and Bolt is big and readable. By city 6, though, the screen is four identical 3-wide grids of cracked glass in front of the same sunset, and the drone is the only thing moving.

### Against the classic

The 1986 game is a **three-player** brawler across a whole continent:

- **Three giant monsters at once,** one per player, who can also punch each other.
- **Well over a hundred days in different cities,** each with its own skyline.
- **Windows full of things:** food and people to grab for health, electrical things like lamps and TVs that zap you, and other pickups that hurt.
- **A ground and air force that answers back:** soldiers in the windows and on the street, tanks, police cars, helicopters, trolleys and trains, each a different threat.
- **A health bar with a famous way to fail:** run out and the monster shrinks back to a human and walks off the screen, embarrassed.
- **Collapsing buildings,** which are the whole goal.

Inverting it into a game about fixing instead of smashing is the right idea. But Rampage's breadth (three players, a continent of cities, windows full of surprises, a dozen threats) is what made it great, and Repair Rampage has none of it.

**Verdict:** a lovely inversion of the premise, with one robot, one threat, one backdrop and nothing in the windows but glass. It is short on players, variety and structure alike.

### The upgrade: Repair Rampage — The Big Fix Tour

Bolt and two friends follow the storm's path across the country, town by town, fixing as they go: **Rivet**, a quick little climber, and **Gizmo**, a big, slow, sturdy one. Every town has its own skyline, its own weather and its own window surprises, and the storm itself waits at the end.

The signature twist is that **the city works with you**:

- Each window you fix lights up, and the people inside come to the glass. They wave, toss you tools and snacks, and shout warnings when something is coming.
- A fully fixed tower switches on its **rooftop**: a billboard, a water tower, a radio mast or a lighthouse, each of which helps with the rest of the town.
- A fallen tower isn't gone for good. A **crane** delivers girders, and you can rebuild it floor by floor.

**Target length:** a first clear in roughly 45–60 minutes.

#### Structure

- The tour has **five regions** (acts) of **five towns** each, with a **storm boss** at the end of each region.
- Each town is authored data:
  - its skyline (tower count, heights and widths, special buildings);
  - its weather and window contents;
  - its threats;
  - a special objective;
  - its medals.
- **Day and night:** a town's clock runs from dawn through noon and dusk to night. Night brings different threats, and its lit windows make breaks easy to spot.
- **Between regions:**
  - **Town Hall**, where thank-you letters earned in play buy upgrades;
  - the **Postcard Album**, with one postcard per town and a gold one for a perfect fix.
- Progress saves at each region through `utils/arcade/saves.ts`. A clear rolls credits and unlocks the **Encore Tour**, a New Game+.

#### The regions

| # | Region | Skylines and mechanics | New threats | Special town | Storm boss |
| --- | --- | --- | --- | --- | --- |
| 1 | **Harbourside** | Today's towers, plus **lighthouses** (one wide column), **dock cranes** you can ride, and the **sea wall**: waves wash over the street on a tell. | News drone, **gull flock**, **rascals**, **wave** | **Lighthouse Night**: relight every lamp before the ferries come in | **Wrecking Wanda** |
| 2 | **Old Brick Town** | Brick towers with **chimneys**; **clock towers** whose minute hand sweeps across one face; **washing lines** between buildings that Bolt can swing along | **Gusts**, **pigeons**, **falling flowerpots** | **Bell Run**: fix the clock tower before noon so its bells ring | **The Storm Cloud Sulk** |
| 3 | **Hilltop Village** | Towers on a slope, so their floors stagger; **cable cars** between towers; **mud slides** along the street | **Billy-goat bots**, **runaway cart**, **lightning** | **Cable Car Rescue**: fix the pylons while the passengers wait | **The Big Blimp** |
| 4 | **Neon Downtown** | Glass towers of 12 or more floors, **skybridges**, **window-washer gondolas**, and **billboards** whose bulbs need fixing | **Paparazzi blimp**, **searchlight copter**, **sparky wires** | **Opening Night**: fix the cinema marquee's letters in order before showtime | **Old Ironjaw** |
| 5 | **The Eye of the Storm** | Every town in one stormy skyline at night, with lightning, wind and rain all at once | All | — | **The Storm Itself** |

#### Window contents: glass → 12 surprises

The classic's windows were full of things; Repair Rampage's are too, in its own kind way.

| In the window | What it does |
| --- | --- |
| **Kitten** | Rescue it for points (as today) |
| **Grandpa waving** | Rescue him and he throws you a toolbox the next time you pass |
| **Snack** (pie, sandwich) | Restores charge |
| **Toolbox** | A power-up (below) |
| **Leaky pipe** | Sprays sideways as the window opens and pushes Bolt one column over; fix it fast |
| **Sparky wire** | Zaps away charge unless Bolt wears Rubber Gloves; fixing it lights the whole floor |
| **Beehive** | Bees chase Bolt for 5 seconds; fixing the window shuts them in and pops out a jar of honey (charge) |
| **Birthday cake** | A big bonus, and the whole floor of partygoers cheers |
| **Lost balloon** | Floats up the tower; catch it at the top for a bonus |
| **Grumpy neighbour** | Shuts the window in your face if you're slow fixing the one next door |
| **Radio** | Turns the town's music up; nearby drones turn round |
| **Rascal's toolkit** | A rascal is hiding inside, and fixing the window shoos it |

#### The roster: 1 → 13 threats

| Threat | Behaviour | Tell | Answer |
| --- | --- | --- | --- |
| **News drone** | As today | Hovers, lens glints | Shoo it, or change rows |
| **Paparazzi blimp** | Slow; flashes a whole row at once | The row lights up | Climb off the row |
| **Searchlight copter** | Sweeps a column with a beam that holds Bolt still | The beam fades in | Leave the column; shoo it from a rooftop |
| **Gull flock** | Drops down a column and knocks Bolt down a floor | A squawk and a shadow | Step aside |
| **Pigeons** | Land on Bolt's head and slow its climbing | Cooing | Wiggle left and right to shake them off |
| **Gust** | Pushes Bolt one column sideways | Leaves blow across | Hold Down to grip |
| **Falling flowerpot** | Knocked off a sill by a gust | Wobbles on the sill | Fix that window first, or wait |
| **Rascal** | A little prankster bot that **unfixes** windows | A giggle and a glinting tool | Shoo it before it reaches a fixed window |
| **Billy-goat bot** | Butts Bolt off its feet on the street | Paws the ground | Jump (Up) on the street |
| **Runaway cart** | Rolls along the street | Its bell | Keep off the street, or fix its kiosk to stop it |
| **Sparky wire** | Lives in windows (above) | Crackles | Gloves, or a fast fix |
| **Lightning** | Strikes the tallest antenna | The antenna glows | Don't be on the top floor |
| **Wave** | Washes over the street | The sea rises | Climb |

#### The storm bosses: 0 → 5

1. **Wrecking Wanda:** a runaway demolition crane who thinks she's helping.
   - **Phase 1:** she swings her ball at the towers and knocks windows out. Fix behind her.
   - **Phase 2:** she lowers her hook to grab Bolt. Climb out of reach and fix her cab windows.
   - **Phase 3:** climb her arm, a tower turned on its side, to the control box and fix it. She becomes the crane that rebuilds towers for the rest of the tour.
2. **The Storm Cloud Sulk:** a grumpy cloud over Old Brick Town.
   - **Phase 1:** rain columns, each on a tell.
   - **Phase 2:** lightning to the antennas, then gusts.
   - **Phase 3:** fix the church's stained-glass windows in rainbow order to make a rainbow, and the cloud cheers up.
3. **The Big Blimp:** the news network's mothership.
   - **Phase 1:** it launches drones in waves from its hangar.
   - **Phase 2:** it flashes the rows from top to bottom.
   - **Phase 3:** ride the cable car up and fix its leaking gas bags from above.
4. **Old Ironjaw:** an abandoned giant robot, a building-sized cousin of Bolt, left out in the storm. He stomps through downtown because he is rusted and sore.
   - **Phase 1:** climb his legs between stomps, each on a tell.
   - **Phase 2:** fix his arm joints while he swings them.
   - **Phase 3:** fix the lights round his chest core. He stands up straight and helps rebuild the town.
5. **The Storm Itself:** a swirl over all three robots.
   - **Phase 1:** every kind of weather at once.
   - **Phase 2:** lightning chases whichever robot has the most charge.
   - **Phase 3:** switch on every rooftop in town (billboards, masts, the lighthouse), and their light pushes the storm apart into the sunrise.

#### Systems that run through the whole tour

- **Fix chains:** fixing windows in quick succession builds a chain.
  - A whole floor lit pays **Floor Lit!**
  - A whole column pays **Elevator Run**.
  - A whole tower pays **Lights On** and switches on its rooftop.
- **Rooftops,** one per tower type:
  - a **billboard** shows threat warnings;
  - a **water tower** cools a sparky floor;
  - a **radio mast** scrambles drones;
  - a **lighthouse** lights the night windows;
  - a **roof garden** grows snacks.
- **Rebuild:** a fallen tower leaves rubble. After Wanda joins the tour, her crane drops girders that a robot carries up one floor at a time. A collapse can be undone.
- **Toolbox power-ups:**
  - **Super Wrench:** fixes a 2 × 2 block of windows.
  - **Paint Roller:** fixes every window you climb past for 5 seconds.
  - **Hard Hat:** shrugs off one falling thing.
  - **Rubber Gloves:** make sparky wires safe.
  - **Umbrella:** blocks one flash.
  - **Rocket Boots:** one jump straight up three floors.
- **Charge** stays the life meter, but running out is no longer an instant game over.
  - The robot sits on the kerb with a cup of oil and is out until the next town, a nod to the classic's famous walk-off.
  - Solo play has three robots in reserve.
- **Town Hall** upgrades: a bigger battery, faster climbing, a longer chain window, a starting toolbox, and a postcard hint.
- **Medals** per town: **All Standing**, **Long Chain** and **Under Par**.
- **Art:**
  - distinct sprites for Rivet and Gizmo;
  - a palette and time of day for every skyline;
  - large animated sprites for every boss.
- **Music:** one loop per region, with a night variant.

#### Modes and players

The cabinet seats up to three (`maxPlayers: 3`), each robot on its own `players` frame. Each robot has its own feel:

- **Bolt** is balanced.
- **Rivet** climbs twice as fast but is lighter, so gusts and gulls knock it off more easily.
- **Gizmo** climbs slowly but fixes two side-by-side windows per swing, and gusts can't move it.

The modes:

- **Tour:** the campaign, solo with any robot or in co-op for up to three.
- **Team Lift:** in co-op, two robots at a wobbling tower's base can push it straight again, resetting its stability.
- **Fix-Off:** a versus race for 2–3 robots to fix the most windows in a town. Shooing a drone into a rival's row is fair play.
- **Rush Hour:** endless towns at a rising pace. This is the leaderboard's main event.
- **Postcard Run:** a time trial per town.

#### The classic's signatures, matched or beaten

- **Three players at once:** matched by three robots, and beaten by Team Lift and Fix-Off.
- **A continent of cities:** matched by 25 authored towns in five regions, each with its own skyline and weather.
- **Windows full of surprises:** matched by twelve window contents.
- **An army that answers back:** matched by 13 threats, each with a tell.
- **A health bar with a funny way to fail:** matched by the kerb and the cup of oil.
- **Collapsing buildings:** beaten, because a collapse can now be rebuilt.

#### Slices

Roadmap: t-110 (slice 1), t-111 (slice 2), t-112 (slice 3), t-113 (slice 4). Slice 1 is `ready`; each later slice waits on the one before.


| Slice | Scope |
| --- | --- |
| 1 | Town data format, window contents, fix chains, rooftops, toolbox power-ups, the first threats (rascal, gust, pigeons, gull flock, paparazzi blimp), charge-out on the kerb, music |
| 2 | Harbourside and Old Brick Town (ten towns), day and night, Wrecking Wanda and the Storm Cloud Sulk, rebuilding with the crane, Town Hall, the Postcard Album, save/resume |
| 3 | Hilltop Village, Neon Downtown and the Eye of the Storm, the remaining threats, the Big Blimp, Old Ironjaw and the Storm Itself, endings, the Encore Tour |
| 4 | Rivet and Gizmo, three-robot co-op, Team Lift, Fix-Off, Rush Hour, Postcard Run, medals |

- **Slice 1, a city with something in it.**
  - **Delivers:**
    - An authored town format (skyline, weather, window contents, threats, objective) in `utils/arcade/repairRampage/`. Today's endless cities are rebuilt on it.
    - Eleven of the twelve window contents, with their effects (all but the grumpy neighbour).
    - Fix chains with the Floor Lit!, Elevator Run and Lights On bonuses.
    - Rooftops that switch on when a tower is complete.
    - The six toolbox power-ups.
    - The rascal, gust, pigeons, gull flock and paparazzi blimp, each with a tell.
    - Charge-out as a sit-down on the kerb with three robots in reserve, instead of an instant game over.
    - The first music loop.
  - **Verified by:** a new `verifyRepairRampage.test.ts` in `test:arcade-engine` covering chains, rooftops and a deterministic seeded town.
- **Slice 2, the first two regions.**
  - **Delivers:**
    - Harbourside and Old Brick Town: ten towns with their own skylines, palettes, lighthouses, dock cranes, sea wall, clock towers and washing lines.
    - The day-and-night clock.
    - The wave, falling flowerpot and grumpy neighbour.
    - The Lighthouse Night and Bell Run special towns.
    - Wrecking Wanda and the Storm Cloud Sulk.
    - Rebuilding fallen towers with Wanda's girders.
    - Town Hall upgrades and the Postcard Album.
    - Save and resume per region through `saves.ts`.
  - **Verified by:** a scripted clear of Harbourside and screenshots of each town.
- **Slice 3, the rest of the tour and the storm.**
  - **Delivers:**
    - Hilltop Village, Neon Downtown and the Eye of the Storm (fifteen towns) with their mechanics: sloped towers, cable cars, mud, skybridges, gondolas and billboards.
    - The remaining threats: billy-goat bots, the runaway cart, the searchlight copter, sparky wires and lightning.
    - The Big Blimp, Old Ironjaw and the Storm Itself.
    - The credits and endings, a true ending for the gold postcards, and the Encore Tour.
  - **Verified by:** a scripted full-tour test and boss-phase tests.
- **Slice 4, the crew.**
  - **Delivers:**
    - Rivet and Gizmo with their own sprites and handling.
    - `maxPlayers: 3` through the `players` frames.
    - Co-op Tour with Team Lift.
    - Fix-Off versus.
    - Rush Hour as the leaderboard mode.
    - Postcard Run time trials.
    - The per-town medal board.
  - **Verified by:** engine tests for three seats.

---

## 19. Rain Catcher (Missile Command riff)


### What is in the game today

| Area | Today |
| --- | --- |
| Field | **One** field: six seedling beds and three sprout launchers with 10 umbrellas each, under **one** stormy dusk sky with a moon, painted once, for every wave. |
| Threats | **Four**: hail (a straight line to a bed or launcher); hail that **splits** once (from wave 2, up to a 35% chance by wave 7); the **thunder-goose** bomber (from wave 2, up to 3 a wave by wave 4); and **lightning sprites** that swerve round blooms at 1.25 × speed (from wave 5, up to 4 by wave 8). |
| Defence | A burst blooms where the sight was, at a fixed 16 px radius. The nearest launcher with umbrellas fires, and the centre launcher's shots are faster. A launcher that's hit is soaked until the next wave. |
| Beds | Two hits each: the first makes a bed droop, the second wilts it. Drooping beds perk up between waves, and a wilted bed grows back for every 10,000 points. |
| Scoring | 25 per hailstone, 100 per goose, 125 per sprite, × a wave multiplier that climbs to 6 × by wave 11. Between waves: 5 per spare umbrella plus 100 per bed. No chains. |
| Difficulty | The geese max out at wave 4, the sky's capacity and split chance at 7, sprites at 8, the volley rate at 10, the hail count at 11 and hail speed at 15. **From wave 15 on, every wave is the same wave.** |
| Structure | No bosses, no sky changes, no ending, no saves, no music. |
| Players | Solo. |
| Code | `rainCatcher.ts`, 1,444 lines. The seed-5 attract pilot lost its last bed on wave 5 after about 2½ minutes. |

The screenshots show a soft, lovely dusk with a glowing moon and launchers that have little faces. But the hail are 5 px dots, and wave 2 and wave 5 look identical apart from the HUD's multiplier badge.

### Against the classic

The 1980 game is a single screen, and Rain Catcher matches it more completely than any other cabinet here:

- **Incoming fire that splits partway down, bombers and satellites that drop more, and smart weapons that dodge your explosions:** all present, as split hail, the goose and the sprites.
- **Three bases with ten shots each,** the centre one firing faster: present.
- **Six things to protect,** with a bonus one every 10,000: present.
- **A score multiplier that climbs with the waves to 6 ×:** present.
- **The colour scheme changes every two waves,** so the screen itself tells you how far you've come. This is **missing**.
- **A trackball:** the sight that speeds up while held stands in for it well.

**Verdict:** a faithful, near-complete riff that is still thin, because the classic is a single screen. One field, one sky, four threats and the same wave from 15 on. To be "newer, better" it has to build past the original, and today nothing does.

### The upgrade: Rain Catcher — Gardens of the World

A little hot-air-balloon greenhouse carries the sprout launchers round the world's gardens, each with its own weather, its own sky and a **Storm Spirit** that is having a bad day.

There are three signature twists:

- **Rain and hail are different.** Silver **raindrops** are good: let them fall and they water the beds. Icy **hail** is bad. Reading the sky becomes the skill, and a bed that's watered grows through five stages (seedling, sprout, bud, bloom, fruit) over a garden's waves. The harvest at the end of a garden pays for how far the beds grew.
- **Petal chains.** A caught hailstone bursts into petals that make a small bloom of their own, and anything caught in it chains. The classic's explosions finally cascade.
- **The sky changes.** Every two waves the colours shift, as in the classic, on top of each garden's own sky.

**Target length:** a first clear in roughly 40–50 minutes.

#### Structure

- The tour has **six gardens** (acts) of **five waves** each, a **Storm Spirit** (boss) after each, and a secret **Rainbow Garden**.
  - Waves 1–2 of a garden teach its new weather.
  - Wave 3 is its **special wave**.
  - Waves 4–5 remix everything learned so far.
- Waves are authored data: volleys, threat mixes, rain share, wind, sky band and par.
- The **Greenhouse** opens between gardens (below), followed by the **Harvest**, which tallies the beds' growth and fruit.
- Progress saves at each garden through `utils/arcade/saves.ts`. A clear rolls credits and unlocks **Second Season**, a New Game+.

#### The gardens

| # | Garden | Sky and mechanics | New weather | Special wave | Storm Spirit |
| --- | --- | --- | --- | --- | --- |
| 1 | **Orchard Hills** | Today's field. **Rain against hail** and **growing beds** are introduced; two **rain barrels** stand between the launchers. | Hail, splitters, the thunder-goose, raindrops | **First Bloom**: grow all six beds to bud | **Nimbus** |
| 2 | **Terrace Paddies** | Beds on three terraces at different heights; **monsoon bands** of heavy rain, then bursts of hail | **Hail moths**, **sleet sliders** | **Fill the Paddies**: fill all three barrels from rain caught over them | **The Monsoon Drummer** |
| 3 | **Desert Oasis** | A hot day: rain is rare and precious. **Sand gusts** bend shots in flight. | **Gusts**, **dust devils** | **Every Drop**: let 30 raindrops reach the palms and catch every hailstone | **The Dust Bunny** |
| 4 | **Mountain Tea Garden** | Snow. **Frost fog** hides the upper sky; launchers ice up and need a tap to thaw. | **Snowballs**, **ice crows** | **Tea Harvest**: three waves without a single soaked launcher | **The Frost Owl** |
| 5 | **Seaside Cliffs** | Wind off the sea brings hail in from the side; **sea spray** bursts low | **Storm kites**, **sea spray** | **Kite Festival**: pop 20 storm kites without touching a festival kite | **The Squall Whale** |
| 6 | **Aurora Greenhouse** (finale) | Night. **Aurora ribbons** bend shots that pass through them, and every weather returns. | **Comets** | — | **The Great Storm** |
| ★ | **The Rainbow Garden** (secret) | The classic's endless rules under a rainbow sky, with every threat at once | All | — | — |

Each garden has one **Golden Watering Can**, earned by gold-medalling its special wave. With all six, the Rainbow Garden opens. Its clear gives the true ending: a rainbow over every garden on the map.

#### The roster: 4 → 15 kinds of weather

| Weather | Behaviour | Tell | Answer |
| --- | --- | --- | --- |
| **Hailstone** | As today | — | Catch it |
| **Splitter** | Splits once in mid-sky | A crack line 30 ticks before it splits | Catch it before the crack |
| **Thunder-goose** | Flies across dropping hail (as today) | A honk | Bloom it and it flies off happy |
| **Lightning sprite** | Swerves round blooms (as today) | Zigzags | Bloom where it is swerving to, not where it is |
| **Raindrop** | Friendly: waters the bed it lands on | A silver teardrop with a soft sparkle | Let it fall, or catch it over a barrel |
| **Hail moths** | Eight slow, tiny stones flying in a cluster | A flutter | One bloom catches the lot: chain bait |
| **Sleet slider** | Falls, then skids along the ground toward a bed | A skid streak | Bloom on the ground in front of it |
| **Snowball** | Grows as it falls; a big one takes two blooms | Visibly grows | Catch it high |
| **Gust** | A band of wind that pushes hail and bends shots | Leaves streak across the sky | Aim upwind |
| **Dust devil** | A spinning column that curls hail into spirals | A swirl of sand | Wait for the hail to leave the spiral |
| **Ice crow** | Dives at an angle and drops hail | A caw, then the dive | Bloom the crow; it flies off |
| **Storm kite** | A tethered kite that zigzags down dropping hail | The string glints | Bloom the kite to cut it loose |
| **Sea spray** | A low volley from the side | A wave crest | A low bloom |
| **Comet** | Fast hail with a long tail | A glowing head | Lead it by a long way |
| **Rainbow sprite** | A bonus: catch it for a launcher refill | Rainbow sparkle | Bloom it |

#### The Storm Spirits: 0 → 6 bosses

1. **Nimbus:** a sulky puff of cloud.
   - **Phase 1:** hail in patterns: lines, Vs, rings.
   - **Phase 2:** it sneezes a gust that bends everything.
   - **Phase 3:** it cries a downpour. Its tears are raindrops, so let them water the beds and catch them over the barrels, and Nimbus smiles.
2. **The Monsoon Drummer:** a cloud beating thunder drums.
   - **Phase 1:** lightning strikes on the beat (the drums flash first), hitting a launcher unless a bloom covers it.
   - **Phase 2:** the drumsticks fall as giant hail.
   - **Phase 3:** the beat speeds up, and catches made on the beat chain double.
3. **The Dust Bunny:** a huge bunny made of sand.
   - **Phase 1:** it kicks up dust devils.
   - **Phase 2:** it hops along the horizon throwing dune hail.
   - **Phase 3:** it sneezes a sandstorm that hides the sky. Only the glow of your blooms lights it.
4. **The Frost Owl:**
   - **Phase 1:** snowflakes fall from its wing beats in fans.
   - **Phase 2:** it ices the launchers one at a time. Tap to thaw.
   - **Phase 3:** it dives. Catch its loose feathers and it settles on the greenhouse roof.
5. **The Squall Whale:** a cloud shaped like a whale.
   - **Phase 1:** it spouts columns of water, mostly rain but laced with hail.
   - **Phase 2:** tail slaps send volleys of sea spray.
   - **Phase 3:** it dives and the tide rises. Catch the wave crests low.
6. **The Great Storm:** the finale.
   - **Phase 1:** every Spirit's pattern in turn.
   - **Phase 2:** a spiral storm eye pulls your blooms toward it.
   - **Phase 3:** the eye opens. Make blooms in rainbow order (each launcher's umbrellas cycle the colours) to build a rainbow across it, and the storm clears.

#### Systems that run through the whole tour

- **Growing beds:** water moves a bed up a stage. Hail knocks it down a stage, and a bed at stage 0 is wilted, as today.
  - Fruiting beds also refill the nearest launcher by one umbrella per wave.
  - The bonus bed every 10,000 points stays.
- **Rain barrels:** raindrops caught over a barrel fill it, and a full barrel refills a launcher mid-wave.
- **Petal chains:** each petal bloom that catches something adds to a chain shown as a growing floater, at × 2, × 3 and up.
- **Wave-pair colour shifts,** as in the classic, layered over each garden's own sky (dawn orchard, monsoon afternoon, desert noon, snowy evening, sea twilight, aurora night).
- **The Greenhouse:** spend seeds earned in play (never real money) on:
  - **Wide Umbrella:** blooms 25% larger.
  - **Quick Sprout:** faster shots.
  - **Deep Pockets:** three more umbrellas per launcher.
  - **Sunflower:** a sunflower between the beds that catches one hailstone every 5 seconds.
  - **Vine Net:** a one-time net over one bed each wave.
  - **Barrel Pump:** barrels fill faster.
- **Medals** per garden: **Not a Drop Lost** (no bed damaged), **Chain Gardener** (a six-chain) and **Full Bloom** (every bed blooming).
- **Bigger art:**
  - hail at 8–10 px with a sparkle, instead of 5 px dots;
  - a distinct sprite for every kind of weather;
  - a large animated sprite for every Spirit.
- **Music:** one loop per garden, with thunder accents on the Drummer's beat.

#### Modes and players

- **Gardens of the World:** the campaign.
- **Two Sights:** simultaneous co-op (`maxPlayers: 2`, each sight on its own `players` frame). Each player fires from the launcher nearest their own sight, and the chains are shared. The classic made two players take turns.
- **Classic Storm:** the endless arcade rules (today's six beds, the 1 × → 6 × multiplier, and now the colour shifts). This is the leaderboard's main event.
- **Daily Forecast:** a fixed seed per calendar day, derived deterministically from the date, so everyone gets the same weather. One try a day.

#### The classic's signatures, matched or beaten

- **Splitting fire, bombers and smart weapons that dodge:** already matched, and extended to 15 kinds of weather.
- **Three bases of ten with a faster centre:** already matched.
- **Six cities with a bonus every 10,000:** already matched.
- **The 1 × → 6 × multiplier:** already matched.
- **Colour shifts every two waves:** matched; missing today.
- **Beyond the classic:**
  - rain against hail;
  - beds that grow and fruit, and the harvest;
  - petal chains;
  - six gardens and six Storm Spirits;
  - simultaneous co-op.

#### Slices

Roadmap: t-114 (slice 1), t-115 (slice 2), t-116 (slice 3), t-117 (slice 4). Slice 1 is `ready`; each later slice waits on the one before.


| Slice | Scope |
| --- | --- |
| 1 | Rain against hail, growing beds, barrels, petal chains, wave-pair colour shifts, hail moths, sleet sliders, snowballs and gusts, bigger art, wave data format, music |
| 2 | Orchard Hills and Terrace Paddies, the Harvest, Nimbus and the Monsoon Drummer, the Greenhouse, save/resume |
| 3 | Desert Oasis, Mountain Tea Garden, Seaside Cliffs and the Aurora Greenhouse, the remaining weather, four more Spirits, the Rainbow Garden, endings, Second Season |
| 4 | Two Sights co-op, Classic Storm, Daily Forecast, medals |

- **Slice 1, reading the sky.**
  - **Delivers:**
    - Raindrops as a friendly threat, and beds that grow through five stages with water and drop a stage per hail hit.
    - Two rain barrels that refill launchers.
    - Petal-chain blooms with a chain counter.
    - Colour shifts every two waves.
    - Hail moths, sleet sliders, snowballs and gusts, each with its tell.
    - Hail and threats redrawn at 8–10 px.
    - A wave data format (volleys, threat mix, rain share, wind, sky band) in `utils/arcade/rainCatcher/`.
    - The first music loop.
  - **Verified by:** a new `verifyRainCatcher.test.ts` in `test:arcade-engine` covering rain watering, chain cascades and a deterministic seeded wave.
- **Slice 2, the first two gardens.**
  - **Delivers:**
    - Orchard Hills and Terrace Paddies: ten authored waves with their skies, terraced beds and monsoon bands.
    - The First Bloom and Fill the Paddies special waves.
    - The end-of-garden Harvest tally.
    - Nimbus and the Monsoon Drummer.
    - The Greenhouse with its six upgrades and seed economy.
    - Save and resume per garden through `saves.ts`.
  - **Verified by:** a scripted clear of Orchard Hills and screenshots of every sky.
- **Slice 3, around the world.**
  - **Delivers:**
    - The Desert Oasis, Mountain Tea Garden, Seaside Cliffs and Aurora Greenhouse: twenty waves.
    - Sand gusts, frost fog, iced launchers, sea wind and aurora shot-bending.
    - Dust devils, ice crows, storm kites, sea spray, comets and the rainbow sprite.
    - The Dust Bunny, the Frost Owl, the Squall Whale and the Great Storm.
    - The Golden Watering Cans and the Rainbow Garden.
    - The credits, the true ending and Second Season.
  - **Verified by:** a scripted full-campaign test and Spirit phase tests.
- **Slice 4, together and every day.**
  - **Delivers:**
    - Two Sights co-op through the `players` frames (`maxPlayers: 2`), with shared chains.
    - Classic Storm as the endless leaderboard mode with the colour shifts.
    - Daily Forecast, seeded deterministically from the calendar date.
    - The per-garden medal board.
  - **Verified by:** engine tests for two seats and a determinism check that the same date gives the same waves.

---

## 20. Petal Post (Paperboy riff)


### What is in the game today

`petalPost.ts`, 1,640 lines. Registry entry: 256 x 240, solo, no mastery ladder.

| Area | Today |
| --- | --- |
| Route | **One street**, houses on **one side only**. **Twelve houses** are rolled once per game and **kept for every day**, with the same colours in the same order. Each day runs 220 px of lead-in, twelve 110 px house gaps, then a 700 px bonus run: about 30 seconds of riding. |
| Visual variety | One lawn, one sidewalk, one road, two bush sprites and a tree per yard. Six house colours plus grey. Day 9 looks exactly like day 1. |
| Hazards | **Four**: skateboarding cats (bounce across the road), rolling bins (roll down toward you), parked cars (still, in the right lane) and lawn sprinklers (spray over the sidewalk on a 90-tick cycle). There are no chasers, no pedestrians, no moving traffic, no roadworks and no weather. |
| Tossing | **Left only.** One fixed arc of 40 ticks. Mailbox 250, doorstep 100, a subscriber's lawn 50, a grey house's garden 25. Bundles refill the satchel to ten. |
| Subscribers | About 60% of the twelve houses to start (the first always subscribes). A missed subscriber cancels at day end, and a perfect day signs up one neighbour. In the demo all **twelve subscribed by day 9**: once the street is full there is nothing left to win back, and nothing at stake but the crash count. |
| Bonus run | Eight bullseye targets in three fixed columns, every day; a crash ends the run. |
| Difficulty | Hazards per gap capped at day 9, cat and bin speed at day 10. **From day 10 on, every day is the same day.** |
| Players, ending, saves | Solo; none (no week, no Sunday, no last day); none. |

### Against the classic

The 1985 game it riffs on:

- **A week**: seven days with a **Sunday paper** that is heavier, and an ending after Sunday (or the sack if you lose every subscriber).
- **A choice of street**: easy, middle or hard.
- **A day-end newspaper** with the subscriber map, showing who cancelled and who came back after a perfect day.
- **A big, lively roster**: dogs that chase, breakdancers, remote-control cars, rolling tyres, storms, workers, construction holes and fences, moving traffic at intersections, drain grates and more. Each moves its own way.
- **The training course** at the end of each day: ramps, jumps and timed targets.
- **Handlebar riding**: speed and steering, with the toss reaching further at speed.
- **The sequel** added **both sides of the street**, a choice of two riders and trick routes.

**Verdict:** Petal Post has a satisfying toss and real subscriber stakes. But it is one twelve-house street ridden left-handed, with four hazards and one fixed bonus run. There are no days of the week, no Sunday and no ending. The stakes can be maxed out by day 9, and from day 10 every day plays the same. It is the classic's Monday morning on repeat.

### The upgrade: Petal Post — A Season in Blossom Valley

The delivery bot takes over the seed-and-letters round for **Blossom Valley**, four neighbourhoods across one season. Every delivery makes a garden grow, and by the end of the season the whole valley can be in flower.

**The signature twist is the Blooming Route.** The classic's subscriptions are on or off. Here every house has a **bloom level from 0 to 3** that **persists across the week** and shows on the house: a bare yard, then sprouts, then flower beds, then a garden in full bloom with bunting.

- **Delivering** raises a house's bloom.
- **Meeting the house's request** raises it twice. Each morning some subscribers put out a **request sign**: "mailbox please", "porch", "window box" or "gate post".
- **Missing a house** wilts it by one level. At 0 it cancels.
- **Grey houses** can be **won over kindly**: two **flower gifts** tossed onto their lawn, and they sign up. There is no vandalism; that is the classic's prank layer replaced with generosity.
- **Tips:** fully bloomed houses tip coins, and a fully bloomed street at the week's end becomes a **street party** with a big bonus.

The stakes now build all week instead of maxing out by Thursday.

**Target length:** a first season clear in roughly 60–70 minutes: 28 days at about 1.5–2 minutes each, plus the Sunday events and the finale.

#### Structure

- **Four weeks**, one neighbourhood each. Each week is **Monday to Sunday**:
  - Monday to Saturday each **introduce one new neighbour** and a **weather of the day**: sunny, breezy (packets drift), rain (puddles, slippery), fog (houses appear late), or market day (crowds);
  - **Sunday** is the heavy-parcel day and ends with the neighbourhood's **Sunday Event**, its boss.
- Then the **Grand Delivery** finale.
- **Streets are authored data**: houses **on both sides**, side roads, intersections, slopes, parks and shops. Each day's street grows a little: more houses and new side roads.
- Each neighbourhood has its own house styles, trees, road surface, palette, season and music loop. The street visibly changes as the week goes on, because bloom levels persist.
- A choice of **Gentle, Brisk or Busy** at the start mirrors the classic's three streets (easy, middle, hard). It sets the traffic and the subscriber count.
- **The Valley Gazette** at each day end:
  - a front page with the street map, every house's bloom level, cancellations and sign-ups, tips and requests met;
  - a templated headline from data ("Primrose Lane in full bloom!").
- Progress saves at each week start (and each Sunday) through `saves.ts`.

#### The weeks

| Week | Neighbourhood and mechanic | New neighbours (one a day) | Day-end bonus course | Sunday Event (boss) |
| --- | --- | --- | --- | --- |
| 1. **Primrose Lane** (spring suburb) | Today's street, now on **both sides**, with a park and a corner shop. Flat. | Skate cat, rolling bin, parked car, sprinkler (today's four), then **gate puppy**, **kite kid**, **puddles** | **Park Loop**: ramps, jumps and targets on the paths | **The Runaway Lawnmower** |
| 2. **Maple Market** (summer town centre) | **Intersections with moving traffic** and traffic-light tells; **market stalls**; **roadworks** with plank ramps over trenches | **Crossing traffic**, **van pull-out**, **pigeon flock**, **busker bubbles**, **roadworks**, **shopping trolleys** | **Trolley Slalom** through the car park | **The Carnival Float** |
| 3. **Hilltop Heights** (autumn hills) | **Slopes**: downhill speeds you up and uphill slows you, and speed sets toss distance. **Windy corners** curve packets; windsocks show the wind. | **Rolling pumpkins**, **goat**, **gust**, **leaf drifts**, **apple drop** | **Hill Jump**: big-air ramps with targets mid-air | **The Big Wheel** |
| 4. **Snowdrop Village** (winter) | **Ice patches**, snowbanks that narrow the road, and **evening rounds** after dark: lamplit, with porch lights showing subscribers | **Snowball kids**, **sledgers**, **snowmen**, **ice patch**, **carol singers** | **Sledge Run** with gate targets | **The Snow Plough Parade** |
| **Finale: The Grand Delivery** | One long route through all four neighbourhoods on Valley Day, every neighbour out at once | All of them | — | **The Post Office's founding parade**: deliver to every house in the valley |

#### The neighbours: 4 → 22

Petal Post's hazards are neighbours, not villains. A bump tips the bot over (a crash); nobody is hurt.

| Neighbour | What they do, and their tell | The answer they ask for |
| --- | --- | --- |
| **Skate cat, rolling bin, parked car, sprinkler** | As today (the sprinkler's sputter is its tell). | Read the cat's bounce; time the sprinkler. |
| **Gate puppy** | Bounds out and play-chases you for three seconds after you pass its gate. **Tell:** the gate swings open and its tail wags. | Speed up, or ring the bell (a Depot upgrade). |
| **Kite kid** | The kite string sweeps across the sidewalk. **Tell:** the kite's shadow. | Slow down, pass after the sweep. |
| **Puddle** | Slides you sideways. | Ride straight through, or go round. |
| **Crossing traffic** | Cars cross at intersections. **Tell:** the light changes. | Ease off and time the gap. |
| **Van pull-out** | A parked van pulls out. **Tell:** its indicator blinks. | Change lane early. |
| **Pigeon flock** | Scatters into the air, and packets bounce off it. | Toss after it lifts, not into it. |
| **Busker bubbles** | A busker blows bubbles that drift across and nudge packets. | Toss through the gaps. |
| **Roadworks** | A trench with a plank ramp. | Take the ramp: it's a jump, and a toss from the air flies further. |
| **Shopping trolley** | Rolls out of the shop doors and drifts downhill. | Dodge, or bump it ahead of you on purpose. |
| **Rolling pumpkin** | Rolls downhill toward you. | Dodge, or toss into it for points. |
| **Goat** | Headbutts from yards near the fence. **Tell:** it lowers its head. | Ride the far side of the lane. |
| **Gust** | Curves packets. **Tell:** windsocks. | Aim upwind. |
| **Leaf drift** | Hides what's under it, sometimes a bundle and sometimes a bin. | Ride over the trail of leaves you've cleared. |
| **Apple drop** | Apples fall from overhanging trees and bounce. | Read the shake of the branch. |
| **Snowball kid** | Lobs snowballs. **Tell:** a shadow on the landing spot. | Keep moving. |
| **Sledger** | Shoots out of a side road. **Tell:** whoosh lines. | Brake. |
| **Snowman** | Stands still and blocks a lane. | Steer round. A packet in its hat pays a bonus. |
| **Carol singers** | A slow group across the sidewalk. | Wait, or take the road. |
| **Hungry letterbox** | A mischief box on a grey house that gobbles packets. | Don't toss into it; it's not a subscriber. |

#### The Sunday Events: 0 → 5 bosses

1. **The Runaway Lawnmower** (Primrose Lane). A ride-on mower bot with nobody on it chases you down the street.
   - **Phase 1:** dodge it.
   - **Phase 2:** it trims hedges into green blocks across the sidewalk.
   - **Phase 3:** toss packets into its seed hopper until it fills, and it stops in a shower of flowers.
2. **The Carnival Float** (Maple Market). A giant duck float drifting driverless down the parade route. Toss parcels into the windows of its four cabins as they open, while the crowd surges across the road. Each filled cabin slows it.
3. **The Big Wheel** (Hilltop Heights). A giant runaway cheese wheel rolling down the hill behind you; you can't stop on the slope.
   - **Phase 1:** steer clear as it bounces lane to lane.
   - **Phase 2:** it splits into four wedges.
   - **Phase 3:** at the bottom, toss into the creamery's chute to finish the delivery.
4. **The Snow Plough Parade** (Snowdrop Village). A plough clears the street ahead and throws up snow walls with gaps; the evening lights come on one by one as you deliver. Deliver every lamplit house before the parade reaches the square.
5. **Valley Day** (the Grand Delivery). The founding parade passes through all four neighbourhoods, and every neighbour is out. Deliver to every house in the valley in one run. **True ending:** reach Valley Day with every house at full bloom and see the valley in flower from the hilltop.

#### Systems, power and meta

- **Both sides:** A tosses left and B tosses right, as in the sequel. **Toss distance follows speed**, as in the classic.
- **Sunday parcels** are heavy: a shorter arc, and double points.
- **Requests, bloom levels and flower gifts**, as above.
- **Stunts:** ramps and trench planks make the bot airborne. A toss from the air flies further, and a mailbox from the air is a **Special Delivery** (x2).
- **Day-end bonus courses** that change each week (Park Loop, Trolley Slalom, Hill Jump, Sledge Run), each with timed targets and jumps. A perfect course earns a **golden stamp**.
- **The Depot** between days. Spend **tips** earned in play (never real money) on:
  - a bigger satchel (12, then 15);
  - a **bell** that sends puppies home;
  - a **rain cape** (puddles don't slide you);
  - **springy wheels** (bigger ramp jumps);
  - a **basket** that collects bundles you ride near;
  - paint jobs.
- **Stamps per day:** Perfect Round, All Requests, No Tumbles and the Golden Course. There is a stamp book per week.

#### Modes

- **Season:** the campaign, with Gentle, Brisk or Busy.
- **Double Round:** two bots through the cabinet's `players` frames, one working each side of the street, sharing the satchel refills and the street's bloom. Like the sequel's two riders, but together.
- **Rush Hour:** an endless street with every neighbour; the leaderboard's main event.
- **Course Challenge:** any bonus course alone, unlocked on a clear.

#### Classic features: matched or beaten

| The classic has | Petal Post answers with |
| --- | --- |
| A seven-day week, a heavy Sunday paper, an ending | Four weeks, Sunday parcels and Sunday Events, and an ending |
| Three streets | Gentle, Brisk and Busy, plus four neighbourhoods |
| Day-end subscriber map | The Valley Gazette |
| Cancel and win back after a perfect day | **Beaten**: graded bloom, requests and flower gifts |
| Moving-hazard roster | 22 neighbours |
| Training course | Four bonus courses |
| Speed-based toss | Kept |
| Both sides; two riders | Kept; together in Double Round |
| Vandalism layer | **Replaced** by generosity: gifts that win neighbours over |

#### Slices

Roadmap: t-118 (slice 1), t-119 (slice 2), t-120 (slice 3), t-121 (slice 4). Slice 1 is `ready`; each later slice waits on the one before.


**Slice 1: Street engine and Primrose Lane.**
- Authored street segments: houses on both sides, side roads, intersections, slopes and parks, replacing the fixed twelve-house strip and `POST_CURVES`.
- Two-sided, speed-based tossing.
- Bloom levels, requests and flower gifts.
- The Valley Gazette day-end page.
- A day-of-week and weather table.
- Week 1, Primrose Lane, Monday to Saturday, with gate puppies, kite kids and puddles, and the Park Loop course.

Verified with the engine tests, a deterministic week test, a pilot probe showing runs end, and screenshots.

**Slice 2: Sundays and Maple Market.**
- The Sunday Event framework and the Runaway Lawnmower.
- Week 2, Maple Market: intersections with traffic lights, van pull-outs, pigeon flocks, busker bubbles, roadworks ramps and trolleys.
- The Trolley Slalom course and the Carnival Float.
- The Depot and upgrades.
- Stamps, and save/resume at each week start through `saves.ts`.

**Slice 3: Hilltop Heights, Snowdrop Village and the finale.**
- Week 3, Hilltop Heights: slope physics, gusts and windsocks, goats, pumpkins, leaf drifts and apples; the Hill Jump course; the Big Wheel.
- Week 4, Snowdrop Village: ice, evening rounds, snowball kids, sledgers, snowmen and carol singers; the Sledge Run course; the Snow Plough Parade.
- The Grand Delivery finale, Valley Day, and the endings.

**Slice 4: Co-op and the extra modes.**
- Double Round two-bot co-op through `players` frames (`maxPlayers: 2`).
- Gentle, Brisk and Busy settings.
- Rush Hour.
- Course Challenge.
- The stamp book.

---

## 21. Cocoa Counter (Tapper riff)


### What is in the game today

Taken from `cocoaCounter.ts` (1,407 lines) on kind_robots `main` (6fb4809).

| Area | Today |
| --- | --- |
| Venue | **One** snowy cafe. Four counters of the same length; the same wallpaper, windows and urns on every row and every round. Four minutes into the demo (round 10), the screen looked exactly like round 1. |
| Patrons | **One kind**, the thirsty robot, in 5 colours that only change the look. It shuffles (stepping two-thirds of each second), is pushed back by a mug, drinks for 70 ticks, slides the empty back, and either leaves happy or walks on, still thirsty. The thirsty chance rises from 25% to 70%. |
| Fail states | A robot reaches the urn; a full mug slides off the door end (the **mop-bot** cleans 2 spills per life); an empty slides off the urn end. |
| Server | Up/down hops between counters (wrapping, always to the urn end), left/right walks, A pours (10 ticks). |
| Tips | A 22% chance per serve: 250 points for 6 s, and **nothing else**. |
| Scoring | 50 per serve, 100 out the door, 100 per empty caught, 250 per tip, 500 x round clear bonus. **No combos, and no extra lives at all.** |
| Difficulty | Thirst caps at round 7, push-back at round 9, the arrival gap at round 10, empty-mug speed at round 10, the crowd (6 → 26) at round 11, and walking speed at round 12. **From round 12 on, every round is the same.** |
| Missing | No bonus round, no entertainment or distractions, no special patrons, no orders, no boss, no ending, no save. Solo only. |

### Against the classic

Tapper (1983):

- **Four venues**, each with its own look and patrons: a Wild West saloon, a sports bar, a punk club and a space bar with aliens.
- **Tips set off a show**: a tip on the bar brings out entertainers, and the patrons stop to watch. It is a breather you earn and choose when to trigger.
- **The bonus round** between venues: a shell game where five of six cans are shaken, and you pick the one that isn't.
- The same three failure modes and the slide-and-catch juggling, exactly as Cocoa Counter has them.
- Rising crowds and speed per level, and an extra bartender at score thresholds.

**Verdict:** Cocoa Counter has Tapper's core loop (pour, slide, catch empties, push-back, tips) and a kind mop-bot of its own. But it is one venue and one patron forever. Tips do nothing, there is no bonus round and no distraction, there are no extra lives and no combos, and the curve is flat from round 12. It is Tapper's first screen, repeated.

### The upgrade: Cocoa Counter — The Cozy Cafe Tour

The mug-bot takes the cocoa cart on tour: five cafes across the Kind Robots world, each with its own counters, patrons, drinks and a rush-hour regular. The signature idea is **orders**:
- patrons show a drink bubble;
- **tap A** pours plain cocoa;
- **hold A** adds marshmallows (a longer pour);
- **hold A and press B** at the urn adds a mint or peppermint swirl.

The wrong drink is politely handed back: the mug slides back to you full, and you have to catch it. A clean round of the right drinks fills the **Cozy meter**, and a full meter starts the **Sing-along**: everyone stops to sway for 5 s. That is Tapper's entertainers, earned through good service.

**Target length:** a first clear in about 45–60 minutes across 5 venues of 4 shifts each, 5 rush-hour bosses, 5 bonus rounds and a secret venue.

#### Structure

- **Five venues** and a secret sixth, **the Rainbow Diner**.
- Each venue has **4 shifts** (rounds), a **Rush Hour** boss shift and a **bonus round**. Shifts 1–2 introduce the venue's patrons and counters; shifts 3–4 remix them with everything earlier.
- Every venue has its own room art, counter layout, music loop, drinks and title card.
- The **Cafe Fund** shop opens between venues; progress saves at each venue.
- A clear unlocks **Double Shift** (New Game+: two patrons per arrival, faster empties, more orders).

#### The venues

| # | Venue | Counters | Drinks | New patrons | Rush Hour boss | Bonus round |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | **Snowdrop Cafe** (today's cafe) | Today's four counters | Cocoa, marshmallow cocoa | Thirsty robot (today), **toddler-bot**, **the trio** | **The Snow Golem Regular** | **Marshmallow Mix-up** (the shell game) |
| 2 | **Seaside Smoothie Shack** (summer boardwalk) | Counters with a **boardwalk gap**: mugs cross it only at full speed, so a slow mug sinks into the sand (a spill) | Smoothies (berry, mango) | **Surfer-bot**, **seagull-bot** | **Captain Crab** | **Catch the Coconuts** |
| 3 | **Moonbase Milk Bar** (the homage to the space bar) | **Low gravity**: mugs float in shallow arcs and bounce once on the counter | Moon milk, stardust shake | **Blob alien**, **teleporter-bot** | **The Mothership Patron** | **Stack the Mugs** (a tower) |
| 4 | **Clocktower Tea Room** | **Conveyor counters** speed mugs up or slow them; **turntable ends** spin an empty onto the next counter | Tea, cocoa | **Grumpy gear**, **cuckoo-bot** | **Grandfather Clock** | **Tea Leaf Reading** (memory) |
| 5 | **Campfire Canteen** (forest night) | Log counters with **bumpers**, and the campfire as the urn | Cocoa, s'more cocoa | **Sleepy bear-bot**, **raccoon-bot** | **The Big Bear Picnic** | **Toast the Marshmallows** (timing) |
| ★ | **The Rainbow Diner** (secret) | Every counter feature, mixed | Every drink | Every patron | **The Rainbow Rush** (every regular returns) | — |

#### The roster: 1 → 13 patrons

| Patron | Behaviour and tell | Answer it asks for |
| --- | --- | --- |
| Thirsty robot (today) | Shuffles, is pushed back, drinks, sometimes walks on | Steady pours |
| **Toddler-bot** | Small and quick, pushed back only half as far | Two quick mugs |
| **The trio** | Three robots walking close together, each wanting a mug | Three pours in a row down one counter |
| **Surfer-bot** | Rides in on a wave fast, then slows | Pour early, aimed for where the wave stops |
| **Seagull-bot** | Swoops to snatch a sliding mug; its shadow crosses the counter first | Pour after the swoop, not into it |
| **Blob alien** | Splits into two blobs when served | Two mugs for one patron |
| **Teleporter-bot** | Sparkles, then blinks three steps forward | Serve it before the sparkle ends |
| **Grumpy gear** | Only drinks tea; a cocoa comes straight back | Read the order bubble |
| **Cuckoo-bot** | Pops out of the clock every 15 s and slides you an extra empty | Be at that counter's urn on the hour |
| **Sleepy bear-bot** | Very slow, pushed back only a little, leaves a big tip | Patience, and grab the tip |
| **Raccoon-bot** | Steals tips off the counter; its mask glints first | Grab tips fast, or serve it first |
| **VIP** (every venue) | Gold order bubble, wants a topped drink | Hold to top; a perfect serve fills the Cozy meter a quarter |
| **Critic-bot** (from venue 3) | Tastes, then rates; a wrong drink drains the Cozy meter | Never get its order wrong |

#### The bosses: 0 → 5 rush-hour regulars, plus the Rainbow Rush

1. **The Snow Golem Regular** (Snowdrop Cafe): a big snowman-bot who fills a whole counter.
   - Each mug pushes him back only a step, and he lobs snowballs that knock sliding mugs off (his arm winds up first).
   - Phase 2 splits his head and body onto two counters.
   - In phase 3 he melts, smiling, into a puddle the mop-bot happily cleans.
2. **Captain Crab** (Seaside Smoothie Shack): a giant crab-bot who walks **across** the counters, changing rows on a click-clack tell.
   - His claws catch mugs and slide them back full, and you must catch those.
   - Serve him three berry smoothies while he's on one row.
3. **The Mothership Patron** (Moonbase Milk Bar): a saucer over the bar that beams patrons onto random counters.
   - Serve the beamed patrons before the beam lifts them to the urns.
   - In phase 3 the beam tries to lift the urns themselves, so pour fast to weigh them down.
4. **Grandfather Clock** (Clocktower Tea Room): his pendulum swings time **fast and slow** across the room. Serve during the slow swing.
   - In phase 2 the conveyors reverse on the hour.
   - In phase 3 every cuckoo comes out at once.
5. **The Big Bear Picnic** (Campfire Canteen): a family of bear-bots with an ever-growing **order ladder** (s'more, cocoa, s'more, s'more…). The raccoons try to steal the picnic tips, and the last bear wants the perfect topped mug.
6. **The Rainbow Rush** (Rainbow Diner, the true finale): every regular returns, one per counter, on every counter feature at once. When all are served, the whole Kind Robots crowd sings along, and the true ending is the cafe tour's group photo.

#### Systems that run through the tour

- **Orders and toppings** (the signature): tap for plain, hold for marshmallow, hold-and-B for a swirl. Order bubbles are big and colour-coded, and a wrong drink comes back full.
- **The Cozy meter and Sing-along:** right drinks, caught empties and tips fill the meter. When it's full, press B to start the Sing-along, 5 s when everyone stops to sway. Choosing when to use it is the skill, as with Tapper's dancers.
- **Tips that matter:** tips fill the Cozy meter, pay into the **Cafe Fund**, and can be stolen.
- **Rush combo:** consecutive serves without a miss raise a multiplier (x1 to x5).
- **Juggle bonus:** catch an empty in the same moment you finish a pour.
- **Extra mug-bots** at 30k, 80k and 150k. Today there are none.
- **Counter features:** gaps, conveyors, turntables, bumpers and low gravity, all as counter data.
- **The mop-bot** stays, and the Cafe Fund can buy it a third mop.
- **The Cafe Fund** between venues. Spend tips earned in play (never real money) on:
  - a faster pour;
  - a third mop;
  - a stickier counter (pushed patrons slide back further);
  - a bigger Cozy meter;
  - a **regular's card** that shows the next shift's patron mix.
- **Golden mugs:** one per venue for a no-spill shift. All five open the Rainbow Diner.
- **Medals per shift:** No Spill, Full House (everyone leaves happy) and Big Tipper.

#### Modes and players

- **The Cozy Cafe Tour:** the campaign.
- **Endless Shift:** venues rotate every 4 rounds, adding a patron every round until the roster is complete. It is the leaderboard's main event.
- **Daily Special:** one seeded venue, patron mix and order list per day.
- **Bonus Bar:** play any bonus round you've reached.
- **Two baristas** (`maxPlayers: 2`):
  - **Co-op:** each mug-bot moves freely over all four counters. A **hand-off** (one pours, the other catches that patron's empty) pays a bonus.
  - **Barista Battle:** each barista has their own mug colour and serves the same patrons; the most happy patrons wins. Snatching a rival's tip is allowed, which is half the fun.

#### The classic's signature features, matched or beaten

| The classic had | Cocoa Counter will have |
| --- | --- |
| Four venues with their own patrons | Five venues and a secret diner, 13 patron types |
| Tips that trigger entertainers | The Cozy meter and Sing-along, when you choose |
| The shake-the-cans shell game | Marshmallow Mix-up, plus four more venue bonus rounds |
| Pour, slide, catch, push-back | Kept, plus orders, toppings and counter features |
| Extra bartenders | Extra mug-bots at 30k, 80k and 150k |
| One drink | Eight drinks and two toppings |
| No boss | Five rush-hour regulars and the Rainbow Rush |

#### Slices

Roadmap: t-122 (slice 1), t-123 (slice 2), t-124 (slice 3), t-125 (slice 4), t-126 (slice 5). Slice 1 is `ready`; each later slice waits on the one before.


**Slice 1 — Orders and the Cozy core.** Order bubbles with **tap, hold and hold-and-B pours**, and wrong drinks that come back full. The slice adds:
- the **Cozy meter** and **Sing-along**;
- tips that fill the meter and the fund, and the tip-stealing hook;
- the **Rush combo** and **Juggle bonus**;
- extra mug-bots;
- a data-driven **venue / counter feature / patron table** format;
- Endless Shift's patron unlock every round, replacing the round-12 plateau.

Verified by a pilot probe that serves mixed orders, and Pixel/HD screenshots.

**Slice 2 — Snowdrop Cafe and the Seaside Smoothie Shack.** Venues 1–2 with the boardwalk-gap counters and the smoothie and marshmallow drinks. It adds:
- the **toddler-bot**, **the trio**, **surfer-bot**, **seagull-bot** and **VIP**;
- **The Snow Golem Regular** and **Captain Crab**;
- the **Marshmallow Mix-up** and **Catch the Coconuts** bonus rounds;
- the **Cafe Fund**, golden mugs 1–2;
- save/resume per venue.

**Slice 3 — Moonbase Milk Bar and Clocktower Tea Room.** Venues 3–4: low-gravity mugs, conveyor and turntable counters. It adds:
- the **blob alien**, **teleporter-bot**, **grumpy gear**, **cuckoo-bot** and **critic-bot**;
- **The Mothership Patron** and **Grandfather Clock**;
- the **Stack the Mugs** and **Tea Leaf Reading** bonus rounds.

**Slice 4 — Campfire Canteen and the Rainbow Diner.** Venue 5: log counters with bumpers, the **sleepy bear-bot** and **raccoon-bot**, **The Big Bear Picnic** and **Toast the Marshmallows**. It adds:
- the secret Rainbow Diner and **The Rainbow Rush**;
- credits, the true ending and **Double Shift** New Game+.

**Slice 5 — Two baristas and the modes.** `maxPlayers: 2` with co-op hand-offs and **Barista Battle**. It adds:
- **Daily Special**;
- **Bonus Bar**;
- medal boards and a mastery ladder.

---

## 22. Quilt Quest (Qix riff)


### What is in the game today

Taken from `quiltQuest.ts` (1,462 lines) on kind_robots `main` (6fb4809).

| Area | Today |
| --- | --- |
| Board | One rectangular cloth, 61 x 51 cells, every quilt. **Three cloth colours** cycle. Patches cycle through six fabrics with prints (dots, gingham, stripes, sprigs, pinstripes, plaid). The finished quilt is a random patchwork, **not a picture**. |
| Foes | The **tangle sprite** roams the open cloth: brushing a thread mid-stitch snaps it. There are 1–3 tangles, reaching 3 at quilt 6. |
| Edge foes | **Sparks** run along the edges: none on quilt 1, then one more per quilt up to 4 at quilt 5. A spark that reaches the start of your thread only lights the fuse; **sparks never chase onto the thread**. |
| Pressure | The **fuse** starts if you stand still 45 ticks mid-stitch. There is no clock. |
| Moves | Fast stitch (A); slow stitch (B, half speed, double points). |
| Scoring | 1 per stitched cell (2 when slow). A claim pays cells x 1–2 x (1 + 0.25 per quilt). The quilt bonus is 1,000 x quilt plus 1,000 per percent over the target; extra needle every 25,000. |
| Difficulty | The target rises from 75% to 85% (caps at quilt 6), sparks cap at quilt 5, spark speed at quilt 7, tangle speed at quilt 9. **From quilt 9 on, every quilt is the same.** |
| Visual | **The best-looking of these six**: a wooden frame with brass tacks, fabric prints, and yarn-ball tangles trailing strands. Quilt 5 in the demo is quilt 1 with more patches. |
| Missing | No timer pressure, no split-the-enemy gamble, no enemy whose **shape** is the threat, no power-ups, no boss, no ending, no save. Solo only. |

### Against the classic

Qix (1981), and the field-claiming games that followed it:

- **The Qix**: a writhing **line** entity, not a ball. Its sweeping shape makes every stitch a read.
- **Sparx** on the border, and a **timer**. When it runs out the Sparx turn into **Super Sparx** and can **chase you onto your unfinished line**. It is the classic's pressure.
- Fast draw and slow draw (slow pays double), and a **fuse** when you stop. Quilt Quest has both.
- **Two Qix** in later levels. **Splitting them** into separate areas ends the level at once and **doubles the score multiplier** for the next.
- 75% threshold, with a bonus per percent over.
- Its descendants added **picture reveals**, **power-up boxes** hidden in the field, **shaped fields**, small enemies you capture by enclosing them, and a **boss creature** per round (Volfied, 1989).

**Verdict:** Quilt Quest is the most complete and best-looking of these six. It has fast and slow stitch, the fuse, edge sparks and a rising target. But it misses what makes Qix tense (the timer and the Super Sparx that chase onto your line), the split gamble, and an enemy whose shape matters. It plateaus at quilt 9 and has no destination: no picture, no boss, no ending. A good game that ends after ten minutes of the same quilt.

### The upgrade: Quilt Quest — The Heirloom Quilt

The needle-bot is sewing the Kind Robots' **Heirloom Quilt**, one block at a time. Every block hides a **picture** under the blank cloth: a sunflower, the arcade hosts, a robot picnic, the moon garden. Every patch you claim reveals that part of it. The signature idea is that the finished blocks **assemble into one great story quilt** in the Heirloom gallery, so a run has a destination you can see growing. Picture reveal is the field-claiming genre's best idea, and building one big heirloom out of it is new.

**Target length:** a first clear in about 45–60 minutes across 25 blocks and 5 boss blocks, at 1.5–2 minutes a block.

#### Structure

- **Five sewing circles** and a secret sixth, **the Heirloom Frame**.
- Each circle has **5 picture blocks and a boss block**. The 30 blocks together are the Heirloom Quilt, and the secret frame adds a 31st, the centrepiece.
- Every circle has its own **frame shape** (rectangle, hoop, hexagon, heart, star), backdrop, cloth, music loop and title card.
- **Pre-sewn islands** (buttons, pins, appliqué) sit in the cloth as obstacles to sew around.
- A sewing-circle map; progress saves at each circle.
- A clear unlocks **Double Stitch** (New Game+: higher targets, faster foes, a shorter stitch clock).

#### The sewing circles

| # | Circle | Frame and cloth | New mechanic | New foes | Picture themes |
| --- | --- | --- | --- | --- | --- |
| 1 | **Patchwork Parlour** | Today's rectangle | The **stitch clock** and **wildfire sparks**; **twin tangles** and the split bonus | Tangle (today), spark (today), wildfire spark, twin tangles | Flowers and fruit |
| 2 | **Hoop Studio** | **Round and oval hoops**, with **pins** as islands | **Wrap capture**: enclose a small foe in a patch under 3% to tie it into a bow | **Bobbin**, **pincushion** | The arcade hosts |
| 3 | **Button Box** | Hexagon frames with **button islands** | **Power-up buttons** hidden in the cloth: enclose one to claim it | **Button beetle**, **static fluff** | Robot friends |
| 4 | **Lace Loft** | Heart frames with **lace holes** that can't be stitched across | **Window wind** drifts tangles one way on a visible cycle | **Cloth moth**, **yarn serpent** | Seasons |
| 5 | **Starlight Attic** | Star frames in the **dark**: only your seams glow | **The Knot**: tangles that merge into one big tangle and split again | Remixes of every foe | The night sky |
| ★ | **The Heirloom Frame** (secret) | One great hexagon | All of them | All | The centrepiece: every robot from the arcade |

#### The roster: 2 → 11 foes

| Foe | Behaviour and tell | Answer it asks for |
| --- | --- | --- |
| Tangle sprite (today) | Roams the open cloth and snaps a thread it brushes | Stitch while it's far; box it in small |
| Spark (today) | Runs the edges | Time your launch off the edge |
| **Wildfire spark** | When the **stitch clock** empties, sparks flare gold and **can run onto your unfinished thread**; the clock bar flashing is the tell | Finish your stitch before the clock |
| **Twin tangles** | Two tangles share a field | **Split them** into separate areas to finish at once with a x2 multiplier on the next block |
| **Yarn serpent** (the line foe) | A long ribbon of yarn that **sweeps** a wide arc; it coils before it lunges | Make short, safe boxes while it's coiled, long ones while it lunges away |
| **Bobbin** | Small and fast, ricocheting off seams | Wrap it in a small box for a bow bonus |
| **Pincushion** | Sits still and fires pins along its row and column on a beat | Cross its lines between volleys |
| **Button beetle** | Crawls the seams and hops onto your thread at a junction; it wiggles before the hop | Don't start a stitch beside a junction it's near |
| **Static fluff** | Drifts and clings to the needle, slowing it until you reach an edge | Shake it off by returning to an edge |
| **Cloth moth** | Nibbles **claimed** cloth back to open, one cell a second | Wrap it fast; it lives on the cloth you claim |
| **The Knot** | Several tangles merge into one big slow tangle, then burst apart; it pulses before it bursts | Box the big Knot in small while it is merged |

#### The bosses: 0 → 5, plus the Grand Knot

Every boss lives inside the field and is beaten by the sewing itself.

1. **Mama Tangle** (Patchwork Parlour): a giant ball of yarn. Every claimed patch unwinds her by its share.
   - Phase 1: she rolls slowly.
   - Phase 2: she sheds tanglets that roam on their own.
   - Phase 3: she splits into two halves. Split them for the double bonus and the win.
2. **The Hoop Wyrm** (Hoop Studio): a yarn serpent wound round the hoop. Wrap its tail sections one by one; it lunges faster each phase. The last section is its head, and you have to box it under 3%.
3. **The Button Baron** (Button Box): a giant four-holed button in the centre. It fires **thread lines** across the field from its holes, and they snap any unfinished thread they cross; each hole glows before it fires. Enclose the space beside each hole to close it. With each hole closed it spins faster.
4. **The Moth Matriarch** (Lace Loft): she lays cocoons that hatch cloth moths. Wrap each cocoon before it hatches, then wrap her while the window wind holds her still.
5. **The Unravel** (Starlight Attic): a sentient knot pulling the Heirloom apart.
   - Phase 1: the frame shrinks.
   - Phase 2: seams move like conveyor belts.
   - Phase 3: you must stitch its heart closed (enclose it under 3%) while every circle's foe returns.
   - It ties itself into a bow and becomes the Heirloom's binding.
6. **The Grand Knot** (Heirloom Frame, the true finale): a Knot of every colour. It splits into one tangle per circle, and each must be wrapped in its own circle's fabric. The finished centrepiece completes the Heirloom Quilt, and the true ending shows it hung in the arcade hall.

#### Systems that run through the campaign

- **Picture reveal** (the signature). Each block is an authored 61 x 51 pixel picture drawn in the six fabric ramps. A claimed area shows the picture there, sewn in that cell's fabric. The **Heirloom gallery** shows every finished block in place, empty slots stitched with chalk outlines.
- **The stitch clock:** visible on the HUD. It refills on each claim, and when it empties the wildfire sparks come. This is the classic's pressure.
- **The split bonus:** splitting twin tangles finishes the block at once and doubles the next block's multiplier.
- **Wrap capture:** enclosing a small foe ties it into a bow for points. Tangles too big to wrap stay a threat.
- **Power-up buttons**, enclosed to collect:
  - **Thimble:** forgives one snap.
  - **Treadle:** the needle moves 50% faster.
  - **Spool:** refills the stitch clock.
  - **Pause Pin:** freezes every foe for 4 s.
  - **Magnet:** pulls the sparks off the edge for 6 s.
- **Seam combos:**
  - **Big Block:** claim 10% or more in one stitch.
  - **Square Seam:** claim an exact rectangle.
  - **Picture Perfect:** reveal a picture's marked feature, such as a face, in one patch.
- **The Workroom** between circles. Spend buttons earned in play on:
  - a starting Thimble;
  - a longer fuse delay;
  - a faster needle;
  - a bigger stitch clock;
  - a **picture peek** that ghosts the block's picture faintly through the cloth.
- **Golden thimbles:** one per circle for a 90%+ block with no snaps. All five open the Heirloom Frame.
- **Medals per block:** Over 90, No Snap and Swift.

#### Modes and players

- **The Heirloom Quilt:** the campaign.
- **Endless Quilting:** today's game with pictures and frames drawn from the pool and a new foe every 2 quilts until the roster is complete. It is the leaderboard's main event.
- **Daily Quilt:** one seeded frame, picture and foe mix per day.
- **Two needles** (`maxPlayers: 2`):
  - **Co-op:** a claim by either needle counts for both, and a **relay stitch** (one needle's thread finished by the other) pays a bonus.
  - **Quilt War:** each needle sews its own fabric, and the most cloth claimed wins. A rival's thread can be snapped only by herding a tangle into it, never by touching it.

#### The classic's signature features, matched or beaten

| The classic had | Quilt Quest will have |
| --- | --- |
| The Qix, a sweeping line | The yarn serpent and the Hoop Wyrm, with a coil-then-lunge tell |
| Sparx, the timer and the Super Sparx | Sparks, the stitch clock, and wildfire sparks that run onto your thread |
| Fast and slow draw, the fuse | Kept |
| Two Qix and the split multiplier | Twin tangles and the split bonus, plus Mama Tangle's split phase |
| 75% target and a bonus per percent | Kept, rising by circle |
| Picture reveals, power-ups, capture and bosses (descendants) | 31 authored pictures forming one Heirloom Quilt, five power-up buttons, wrap capture, six bosses |
| One rectangle | Rectangles, hoops, hexagons, hearts and stars, with islands and lace holes |

#### Slices

Roadmap: t-127 (slice 1), t-128 (slice 2), t-129 (slice 3), t-130 (slice 4), t-131 (slice 5). Slice 1 is `ready`; each later slice waits on the one before.


**Slice 1 — Pressure and pictures.** This slice brings the classic's tension:
- the **stitch clock** and **wildfire sparks** that run onto an unfinished thread;
- **twin tangles** with the **split bonus**;
- **wrap capture**.

It also adds:
- the **picture-reveal renderer**, with authored 61 x 51 pictures mapped to the fabric ramps;
- **shaped frames and islands** as data;
- the **power-up buttons**;
- seam combos;
- Endless Quilting's foe unlock every 2 quilts, replacing the quilt-9 plateau.

**Slice 2 — Patchwork Parlour and Hoop Studio.** Circles 1–2: 10 picture blocks plus **Mama Tangle** and **The Hoop Wyrm**, round and oval hoops with pin islands, and the **bobbin** and **pincushion**. It adds:
- the **Heirloom gallery**, golden thimbles 1–2, the circle map and title cards;
- save/resume per circle.

**Slice 3 — Button Box and Lace Loft.** Circles 3–4: hexagon and heart frames, button islands, lace holes and window wind. It adds:
- the **button beetle**, **static fluff**, **cloth moth** and **yarn serpent**;
- **The Button Baron** and **The Moth Matriarch**;
- the **Workroom** shop.

**Slice 4 — Starlight Attic and the Heirloom Frame.** The dark circle where only seams glow, and **The Knot**. It adds:
- **The Unravel**;
- the secret Heirloom Frame and **The Grand Knot**;
- the assembled Heirloom Quilt in the credits, the true ending, and **Double Stitch** New Game+.

**Slice 5 — Two needles and the modes.** `maxPlayers: 2` with co-op (shared claims, relay stitch) and **Quilt War**. It adds:
- **Daily Quilt**;
- medal boards and a mastery ladder.

---

## 23. Gloom Invaders (Space Invaders riff)


### What is in the game today

| Area | Today |
| --- | --- |
| Formation | **One** formation shape, a 9 × 5 grid of 45 gloom clouds in three looks (storm anvil 30, grey puff 20, small grump 10). It marches, drops a row at the edges and hurries as it thins; the last cloud races. |
| Enemy fire | **One** kind of drop. A third of the drops come from the column over Sunny; the rest are random. All fall straight at the same speed range. |
| Cover | Four rainbow umbrellas (22 × 13 cells each), worn away by drops, by Sunny's own beams, and by clouds marching through them. |
| Player | Left, right and a sunbeam, one on screen at a time. A beam can pop a drop on its way up. |
| Bonus | A rainbow kite crosses the top; its mystery value comes from a 15-entry table indexed by beams shone (the classic's shot-count trick). The kite skips the end of a wave. |
| Waves | Each wave starts lower (52 → 100 px) and marches faster. If the gloom lands, Sunny loses a life and the wave regroups (kinder than the classic). Wave-clear bonus 100 × wave. |
| Visual progression | The sky brightens over six cleared waves, with a sun rising behind the hills, and up to eleven flowers grow in the garden: the only cabinet in this batch whose look changes with progress. It stops changing at wave 7. |
| Difficulty | March pace and starting height max out at wave 7, drop rate and drop count at 9, kite frequency at 11, drop speed at 12. **From wave 12 on, every wave is the same wave.** |
| Players, saves, ending | Solo, with no save and no ending. An extra Sunny at 1,500, then every 10,000. |
| Look | Crisp, cute cloud sprites in a portrait 288 × 384 field. Four minutes into the attract demo, the pilot had reached game over on wave 2 with all four umbrellas gone. |
| Scale | `gloomInvaders.ts`, 1,451 lines. |

### Against the classic

The 1978 game is the template of the genre, and it is subtler than it looks:

- **A 55-strong formation** (5 × 11) in three types, whose march speeds up as it thins, with a four-note heartbeat.
- **Three different enemy shots:** one that targets your column and two that follow column tables, with a reload that
  tightens as the score climbs.
- **Bunkers** worn away from both sides, and erased by invaders that march through them.
- **The mystery saucer** and its shot-count scoring trick.
- **Starting heights** that step down in a cycle.
- **Invasion is total:** if they land, the game is over.
- Its 1979 follow-up added **invaders that split in two** when hit and a **mothership** bonus wave. The genre's next
  generation added enemies that **peel out of formation and dive**, and **tractor beams** that capture your ship.

**Verdict:** Gloom Invaders is a faithful, charming take on the 1978 game, and its rising sun and growing garden are the
best progression idea in this batch. But it has a smaller formation than the classic, one shot type where the classic
has three, no splitters, no divers and no bosses, and every wave from 12 on is identical. The garden it grows is
decoration; it never does anything.

### The upgrade: Gloom Invaders — A Year of Weather

Sunny's garden needs a whole year of weather: rain to drink, and sunshine to drive away the gloom. Gloom Invaders
becomes a **calendar**: twelve months, each a different kind of weather front with its own formation and its own
clouds, and a great weather system to face at the end of each season.

The signature twist is **The Garden Grows Back**: every cloud you cheer rains on the plot below it, and the garden that
grows fights beside you. Where you cheer clouds matters.

**Target length:** a first clear in roughly 45–60 minutes.

#### Structure

- The year has **four seasons** (acts) of **three months** each, a **season boss** at the end of each season, and a
  **secret thirteenth month**.
- Each month has **three fronts** (waves):
  - front 1 introduces the month's formation and cloud;
  - front 2 is the month's **special front**;
  - front 3 remixes the month with everything learned so far.
- **The garden** carries across a season and is replanted each spring (below).
- Each season has its own sky ramp, palette, ground and music loop. The sky still brightens front by front, now inside
  every month.
- **The Seed Shed** opens between seasons (below).
- Progress saves at each season start.
- A clear rolls credits and unlocks **Leap Year**, a New Game+.

#### The months

**Spring**

| Month | Formation | New clouds and drops | Special front |
| --- | --- | --- | --- |
| **March** | The **Cumulus Grid**: the classic block, now 11 × 5 | **Drizzler** (darkens, a drop forms, then it fires a column-seeking drizzle) | **First Shoots**: water five plots in one front to sprout the garden. |
| **April** | **Showers**: rows that drift at different speeds | **Splitter Puff** (splits into two small clouds when cheered) | **Rainbow Hour**: after every fourth cheer a rainbow arcs; beam through it for a prism shot. |
| **May** | **Kite Day**: a looser formation with gaps | **Wind Sock** (blows every drop sideways for a few seconds) | **Kite Festival**: three kites at once, each carrying a mystery prize. |

**Spring boss: The April Shower Mother.** A great grey raincloud with three drainpipe spouts.
- **Phase 1:** each spout pours a drizzle stream that sweeps sideways. Cheer the spouts shut one by one.
- **Phase 2:** she rains splitter puffs.
- **Phase 3:** she lowers toward the garden. Hold her off long enough for the sunflowers to open, and they finish her
  with a sunburst.

**Summer**

| Month | Formation | New clouds and drops | Special front |
| --- | --- | --- | --- |
| **June** | **Thunderhead Rows** | **Thunderhead** (three hits; its column lights up on the ground for a second before a lightning strike) | **Brownout**: lightning has knocked out the umbrellas; the bean vines are your only cover. |
| **July** | **The Squall Line**: a diagonal front that sweeps the sky | **Diver Gust** (wiggles, its edge turns red, then it peels out and swoops at Sunny and back) | **Picnic**: protect the picnic blanket on the lawn. |
| **August** | **Hailstorm** stacks | **Hailer** (hail that bounces once off the umbrellas or the ground) | **Heat Haze**: the formation shimmers in and out of sight; beam the shimmer. |

**Summer boss: Cumulonimbus Rex.** A towering anvil cloud that fills the top of the sky.
- **Phase 1:** lightning strikes walk across the ground, each lighting its column first.
- **Phase 2:** its anvil top spins off diver gusts.
- **Phase 3:** it rains hail that bounces. Cheer its glowing heart through gaps you open in its body.

**Autumn**

| Month | Formation | New clouds and drops | Special front |
| --- | --- | --- | --- |
| **September** | **Fog Banks** | **Fog Veil** (invisible until a beam passes close) | **Harvest Moon**: the moon lights one column at a time; only lit clouds can be cheered. |
| **October** | **Leaf Storm**: the rows ride a falling-leaf swirl | **Tractor Cloud** (beams an umbrella up into the sky; cheer it to drop the umbrella back) | **Scarecrow**: the garden's scarecrow lends a second beam while it stands. |
| **November** | **The Spiral Low**: a rotating ring formation | **Sleet Cloud** (a zig-zag sleet drop) | **Long Night**: the front arrives at dusk and darkens as it goes. |

**Autumn boss: The Leaf Twister.** A spinning funnel of leaves that roams the sky.
- **Phase 1:** a ring of debris orbits it; break the ring.
- **Phase 2:** it sucks umbrellas toward it. Cheer the umbrellas free.
- **Phase 3:** it touches down and crosses the garden. Cheer its eye before it reaches the sunflowers.

**Winter**

| Month | Formation | New clouds and drops | Special front |
| --- | --- | --- | --- |
| **December** | **Snow Clouds** | **Snow Cloud** (slow flakes that pile up on the ground and slow Sunny until a sunbeam melts them) | **Lantern Night**: the garden's lanterns light the gloom for the beam. |
| **January** | **The Jet Stream**: each row slides at its own speed, and some rows reverse | Remixes | **Thaw**: melt the snow off every plot in time for spring. |
| **February** | **Everything at once** | Every cloud and drop | **The Last Grey Day**: a front with no gaps. |

**Finale: The Gloom Front.** A sky-wide storm system with a sulky face.
- **Phase 1:** it advances as a wall of every cloud type, marching like the classic but three formations deep.
- **Phase 2:** its face opens and fires every drop pattern in turn.
- **Phase 3:** it runs out of rain, and the whole garden blooms at once and helps Sunny shine it away.
- **Ending:** spring arrives: the garden in full bloom, every cheered cloud floating by as a happy little cloud.

**Secret month: Rainbow Day.** A **sun charm** is hidden in each month, earned by finishing its special front with all
four umbrellas standing. With all twelve, a thirteenth month opens, every cloud dressed in rainbow, and the **true
ending**: a festival in Sunny's garden.

#### The roster: 3 → 13 clouds, 5 drop types, 4 bosses

| Cloud | Tell | Answer |
| --- | --- | --- |
| Grump, grey puff, storm anvil | As today | As today |
| Drizzler | Darkens, then a drop forms over your column | Step off the column |
| Splitter Puff | A seam across its middle | Cheer both halves for a bonus |
| Wind Sock | Its streamer flicks | Lead your dodge downwind |
| Thunderhead | The ground under its column lights up | Leave the lit column |
| Diver Gust | Wiggles and turns red-edged | Beam it mid-swoop for double |
| Hailer | Ice glints | Beam the hail in the air, or keep clear of the bounce |
| Fog Veil | A faint shimmer | Sweep beams to reveal it |
| Tractor Cloud | A beam reaches for an umbrella | Cheer it to drop the umbrella |
| Sleet Cloud | Zig-zag streaks | Wait for the zig, then step |
| Snow Cloud | Flakes drifting slowly | Melt the drifts; keep moving |
| Rainbow Kite, Paper Plane (bonus) | A whistle as it crosses | Hit it for a mystery prize or a power-up |

Drop types: straight (today), column-seeking drizzle, bouncing hail, zig-zag sleet and lightning. Bosses: the April
Shower Mother, Cumulonimbus Rex, the Leaf Twister and the Gloom Front.

#### Systems that run through the whole year

- **The Garden Grows Back (signature):**
  - the ground is eleven plots, and each cloud cheered rains on the plot beneath where it was cheered;
  - a plot blooms after five waterings into a helper, chosen by plot position and season:
    - **Sunflower:** a sunbeam straight up from its plot every 3 s.
    - **Bean Vine:** climbs into a living umbrella that regrows.
    - **Beehive:** a bee intercepts one drop every 4 s.
    - **Pumpkin:** a one-time launch that cheers a whole column.
    - **Strawberry:** an extra Sunny at ten waterings.
  - gloom drops that reach the ground wilt a plot a little;
  - the garden carries across a season, so the late months reward the cheering you did early.
- **Sun Lance:** hold A for 0.6 s to charge a wide sunbeam that pierces a whole column. It is still one beam at a time,
  so charging is a choice.
- **The heartbeat:** a music loop through the engine's `music`, whose tempo rises with the march.
- **The classic's shot-count kite** stays, now joined by the **Paper Plane** courier, which carries a power-up:
  - **Prism:** three beams.
  - **Double:** two beams on screen.
  - **Umbrella Patch:** repairs the cover.
  - **Sunglasses:** drops fall at half speed for 6 s.
  - **Solar Flare:** cheers the lowest row.
- **The Seed Shed** between seasons: spend **seeds** dropped by cheered clouds (never real money) on starting plots, a
  sturdier umbrella, a faster Sun Lance charge, a spare Sunny, or a hint for the season's sun charms.
- **Medals per front:** Dry Feet (no hit), Full Bloom (every plot watered) and Clear Skies (under par).

#### Modes

- **Calendar:** the campaign.
- **Endless Forecast:** endless fronts from every month in turn, the leaderboard's main event.
- **Daily Forecast:** a month remix seeded from the date, the same for every player that day (the sim is
  deterministic), with its own daily board.
- **Co-op:** two Sunnys side by side through the `players` frames, sharing the umbrellas and the garden. Each player's
  cheers water their own half, so the garden shows who did what.
- **Classic Sky:** today's game, with the original 55-cloud grid as an option.

#### Signature features to match or beat

| The classic's feature | Gloom Invaders |
| --- | --- |
| A 55-strong formation in three types, speeding up as it thins | Kept, plus eleven more formations |
| Three distinct enemy shots | Five drop types |
| Bunkers eroded from both sides | Kept, plus bean-vine umbrellas that regrow |
| The mystery saucer and its shot-count trick | The kite keeps the trick; the paper plane adds power-ups |
| Splitting invaders (follow-up) | Splitter Puffs |
| Divers and capture beams (the genre's next generation) | Diver Gusts and the Tractor Cloud |
| The heartbeat | Music tempo tied to the march |
| **Past the classic** | The Garden Grows Back, Sun Lance, twelve months, four bosses, a daily seed, co-op, an ending |

#### Slices

Roadmap: t-132 (slice 1), t-133 (slice 2), t-134 (slice 3), t-135 (slice 4). Slice 1 is `ready`; each later slice waits on the one before.


1. **Weather and the garden.** The 11 × 5 grid; formations as data (grid, drifting rows, diagonal sweep, ring,
   jet-stream rows); the five drop types; the drizzler, splitter puff, diver gust, hailer and thunderhead; the Sun
   Lance; the heartbeat loop; and The Garden Grows Back with all five helpers and wilting. Classic Sky keeps today's
   rules behind a mode switch. Deterministic tests cover plot watering, splitter scoring and formation paths, and a
   pilot probe shows runs still end.
2. **Spring and Summer.** The calendar engine (seasons, months and fronts as data) with save/resume; March to August,
   with their special fronts, skies and music; the wind sock; the paper-plane courier and its power-ups; the April
   Shower Mother and Cumulonimbus Rex; and the Seed Shed.
3. **Autumn, Winter and the Gloom Front.** September to February, with the fog veil, tractor cloud, sleet cloud and
   snow cloud and their special fronts; the Leaf Twister and the Gloom Front; the spring ending and credits; the twelve
   sun charms, Rainbow Day and the true ending; and Leap Year New Game+.
4. **Forecasts and company.** Two-Sunny co-op through the `players` frames, with the split garden; Endless Forecast as
   the leaderboard event; Daily Forecast with a date seed and a daily board; and the medals with a board per season.
   Registry `maxPlayers` and the blurb and how-to lines are updated.

---

## 24. Seed Burst (Bomberman riff)


### What is in the game today

Taken from kind_robots `main` (454021d; the six game files are unchanged there since they shipped): `seedBurst.ts`, 1,712 lines. Registry entry: 240 x 232, `maxPlayers: 4`, no mastery ladder.

| Area | Today |
| --- | --- |
| Boards | **One** 15 x 13 grid with stone pillars on every even cell. Only the hedge scatter changes: 45% of free cells at round 1, up to 66%. There are no authored layouts, no exit to find and no floor gimmicks. |
| Visual variety | **Three** garden palettes (spring, deep summer, twilight), taken in turn. They are the same grass, the same pillars and the same brick wall, just recoloured. The round-5 screenshot looks like round 1 with more hedges. |
| Enemies | **One.** The grumpy gnat wanders at random and turns down a side path 25% of the time at each cell. From round 3 a "drifter" variant (purple, 0.8x speed) passes through hedges. Nothing chases, shoots, splits, hides or needs more than one bloom. |
| Hazards | None, apart from your own blooms. When the 150-second timer runs out, a single **wind gust** blows in three fast drifter gnats. |
| Bosses | None. |
| Power-ups | **Three**, hidden under 22% of hedges: seed packet (+1 pod, max 6), fertiliser (+1 bloom reach, max 7) and quick shoes (+0.25 speed, max 2). They are **never lost**: a bonked gardener keeps everything. In the attract demo the gardener is maxed at 6/7/5 by round 5, so there is nothing left to chase. |
| Scoring and chains | Each pod's burst counts its own gnats: 100, 200, 400, up to 1,600 (x16). Every pod that a chain sets off starts its own count from 100. Hedges pay 10, pickups 50, and a round clear pays 1,000 x round plus 10 per second left. |
| Difficulty | Gnats 3 → 10 (capped at round 8). Hedge density capped at round 8. Drifters up to 4 (capped at round 9). Gnat speed 0.5 → 1.15 (capped at round 12). **From round 12 on, every round is the same round.** |
| Players | Up to four gardeners on one screen, sharing one score and one pool of spares (2). This is real co-op, and the best thing in the cabinet. There is no versus or battle mode. |
| Ending and saves | None. It loops until the garden closes. |

### Against the classic

The 1983/85 game it riffs on, and its 16-bit sequels, are much more than a pillar grid:

- **An exit hidden under a breakable block**, and a power-up hidden under another. Blowing up the exit lets out a fresh wave of enemies, so finding it is a risk as well as a goal.
- **Eight-plus enemy roles**: slow wanderers, fast wanderers, enemies that track you, enemies that drift through soft walls, and a near-unkillable enemy that arrives when the clock runs out.
- **A deep power-up list**: bomb up, fire up, speed, remote detonation, wall-pass, bomb-pass, flame-pass and short invincibility. The sequels add kick, throw, punch, line bombs, piercing bombs and rideable mounts that take a hit for you. Losing a life costs power, which keeps the tension up.
- **Bonus stages** at set intervals.
- **Themed worlds** in the 16-bit games, each with a floor gimmick (conveyors, warps, ice, trampolines, mine carts) and **a boss at the end of each world**.
- **The battle mode**: four players, many arenas, closing walls for sudden death and curse items. It is the mode most people remember.

**Verdict:** Seed Burst has the plant-burst-chain core and real four-seat co-op, which is more than most cabinets. Everything around that core is missing:

- one pillar grid, three palettes and one enemy plus a variant;
- three power-ups that max out by round 5 and are never lost;
- no exit to find, no world gimmicks, no bosses and no battle mode.

The difficulty goes flat at round 12. Today it is the first world of the classic, solo or co-op, on repeat.

### The upgrade: Seed Burst — The Four Seasons Allotment

The gardeners take over a sprawling old estate garden that has gone grumpy. They work through it one season at a time, turning every grump into a butterfly. The plant-and-step-clear core stays. Around it go authored plots, a hidden Garden Gate in every plot, seasonal floor gimmicks, fifteen grumps that each ask a different question, five bosses, and a battle mode recast as a flower show.

**The signature twist is the Seed Pouch.** The classic has one bomb shape and makes its variety from upgrades. Seed Burst gives every gardener a pouch of **six seed varieties**, each bursting in its own shape, swapped with B:

- **Sunflower**: today's cross.
- **Clover**: a diagonal X, which no grid bomb game offers as a basic shape and which changes how every board is read.
- **Dandelion**: its fluff drifts downwind over hedges.
- **Pumpkin**: rolls when walked into.
- **Bramble**: lays a line of up to four pods in the facing direction.
- **Puffcap**: bursts when you press A again.

Some grumps can only be reached by one shape, so the pouch is a puzzle tool and not just more firepower.

**Second twist: the garden grows.** Every tile a bloom crosses becomes a flowerbed: sprout, then bud, then flower over ten seconds.

- Grumps walking through flowered tiles slow to half speed.
- A plot's **In Bloom %** shows on the Garden Gate and pays out at the end.

Playing well visibly turns the board into a garden.

**Target length:** a first clear in roughly 55–65 minutes.

#### Structure

- **Four seasons** (acts). Each has **six plots**, a **Bonus Bed** after plot 3 and a **boss plot** at the end.
- A **secret fifth season, the Midnight Greenhouse**: four plots and the true boss.
- In all: **28 plots, 4 Bonus Beds and 5 bosses**.
- Every plot is **authored data**: a hedge mask, gimmick tiles and a grump script. Hedges inside the mask still roll from the seeded rng, so replays differ but the shape is designed.
- Every plot hides the **Garden Gate** under one hedge. Blooming the gate's hedge "rings the gate bell", which calls three extra grumps out of the compost heap: a risk, as in the classic.
- Clear every grump, then step through the open gate.
- Each plot also hides one **golden seed** under a hedge. All 28 open the Midnight Greenhouse.
- Each season has its own tile set (pillar style, ground, wall), backdrop details, music loop and title card.
- **The Potting Shed** opens between seasons, and progress saves at each season start through `utils/arcade/saves.ts`.

#### The seasons

| Season | Plots and floor gimmick | New grumps | Bonus Bed | Boss |
| --- | --- | --- | --- | --- |
| 1. **Spring: The Kitchen Allotment** | Vegetable rows between stone pillars. **Regrowing hedges**: an unbloomed hedge stump sprouts back after 20 s. **Watering cans** stand as tiles; blooming one soaks its row and doubles the next bloom's reach along it. | Grumpy gnat, drifter gnat, **sulky slug**, **burrow mole** | **Butterfly Release**: 30 s and no grumps. Bloom wandering caterpillars into butterflies; every chain doubles. | **Old Bramblebeard** |
| 2. **Summer: The Glasshouse Rows** | **Irrigation channels**: water lanes that carry pods, gardeners and grumps along them. **Glass panes** take two blooms (crack, then shatter). **Springy mushrooms** bounce a gardener two tiles over a hedge. | **Hedge hopper**, **buzz bully**, **seed thief**, **puffball** | **Sprinkler Dash**: collect seeds on conveyors before they fall off the end. | **Hothouse Hector** |
| 3. **Autumn: The Orchard and Pumpkin Patch** | **Gusts** blow the way the windsocks point and change on a tell. Dandelion fluff and falling leaves follow them. **Leaf drifts** cover tiles (pods and grumps can hide in them). **Apple trees**: a bloom that reaches a trunk drops apples that roll down their lane and bonk grumps. | **Pod weevil**, **acorn lobber**, **leafpile lurker** | **Apple Bowling**: roll apples down the rows at grump targets. | **The Harvest Scarecrow** |
| 4. **Winter: The Frost Conservatory** | **Ice paths**: gardeners and kicked pumpkins slide until they stop. **Snowdrifts** take two blooms. **Frozen ponds** crack after two crossings and dunk you back at your corner (a bonk). | **Frost moth**, **snowball roller**, **mimic sprout** | **Snow Angels**: paint a picture by blooming the right tiles in 40 s. | **The Frost Topiary** |
| 5. **Secret: The Midnight Greenhouse** | **A dark board**: lamps light pools, and moonflowers glow when bloomed. Each plot remixes the gimmicks of two seasons. | **Night owl**, plus remixes of everything | None | **The Grumble Blight** |

#### The roster: 1 → 15 grumps

| Grump | What it does, and its tell | The answer it asks for |
| --- | --- | --- |
| **Grumpy gnat** | Today's wanderer. | A plain bloom. |
| **Drifter gnat** | Today's ghost: drifts through hedges, glows purple. | Cover the open lanes it has to cross; Dandelion fluff reaches it inside hedges. |
| **Sulky slug** | Slow. The first bloom knocks its shell off and the bare slug hurries. It leaves slime that slows gardeners. | Two blooms in a row: a Bramble line, or a second pod placed ahead of it. |
| **Burrow mole** | Tunnels under the board and surfaces beside the nearest gardener. **Tell:** its dirt mound wobbles for one second. | Plant on the mound before it pops up. |
| **Hedge hopper** | Hops one hedge in a straight line. **Tell:** crouches and winds its legs. | Bloom its landing tile. |
| **Buzz bully** | Wanders until a gardener is in a clear straight lane, then charges at double speed. **Tell:** antennae spark and a "!". | Step out of line; bait it into a waiting pod. |
| **Seed thief** | Runs to pods and power-ups and carries them away down its burrow. | Bloom it to drop the loot (with a bonus); a Clover catches it on a diagonal. |
| **Puffball** | A bloom bursts it into four spore gnats. | Pre-plant so the spores land in a second burst: a chain. |
| **Pod weevil** | Swallows any pod it walks over. The pod still goes off two seconds later, wherever the weevil has walked. **Tell:** its belly glows with the fuse. | Use it: steer it toward other grumps and keep clear. A walking chain-starter. |
| **Acorn lobber** | A squirrel in a tree that lobs acorns over hedges at your tile. **Tell:** a shadow ring on the landing tile. | Keep moving; bloom the tree trunk to bring it down. |
| **Leafpile lurker** | Hides in a leaf drift and pops out when a gardener passes. **Tell:** the drift rustles. | Blow the drifts away first, with a bloom or by turning the wind. |
| **Frost moth** | Freezes any pod it flies over; a frozen pod won't burst until another bloom thaws it. **Tell:** a frost trail. | Chain-thaw on purpose: a frozen pod is a bomb you set off on your own schedule. |
| **Snowball roller** | Rolls down a lane, growing. Small: one bloom. Big: two, and it blocks blooms behind it. | Catch it small. |
| **Mimic sprout** | Looks like a power-up but blinks off-beat. Biting one costs a power level. | Read the blink before you grab. |
| **Night owl** | Seen only in lamplight; swoops along a whole lane. **Tell:** a hoot, then two eyes in the dark. | Light the lamps first. |

**When the timer runs out:** the gust becomes **the Grumble Cloud**, a slow rain cloud that cannot be bloomed. It drifts toward the nearest gardener, and the only escape is to finish the plot. This is the classic's time-out pressure, recast in the game's own tone.

#### The bosses: 0 → 5

1. **Old Bramblebeard** (Spring). A walking thorn hedge three tiles wide.
   - **Phase 1:** it strolls the plot and drops bramble hedges behind it. Its four root tiles glow when exposed; bloom them, three hits.
   - **Phase 2:** it roots in the centre and sprouts bramble lines across whole rows on a tell (the row rustles).
   - **Phase 3:** it uproots and charges down lanes. Bloom its back as it passes, and it settles into a flowering rose bush.
2. **Hothouse Hector** (Summer). A heating robot that has overheated and taken over the glasshouse.
   - **Phase 1:** it rolls along the top row firing steam down the columns (tell: its gauge needle swings to a column). Bloom its four valve tiles to vent it.
   - **Phase 2:** it switches on the irrigation channels. Ride pods into it on the water.
   - **Phase 3:** it hops around the plot and lands with a shockwave; bloom its open boiler hatch. It ends up as a friendly sprinkler.
3. **The Harvest Scarecrow** (Autumn).
   - **Phase 1:** it points, and crows (gnats) fly to that tile. Roll pumpkins into its pole.
   - **Phase 2:** it spins and turns the wind every few seconds. Dandelion fluff and drifting pods have to be steered on the gusts.
   - **Phase 3:** its hat flies off and swoops as its own grump. Bloom the hat, and the scarecrow waves goodbye.
4. **The Frost Topiary** (Winter). A great hedge swan that dances the board.
   - **Phase 1:** on its beat, whole hedge columns slide one tile, rearranging the maze.
   - **Phase 2:** it splits into three cygnet topiaries. Bloom all three inside a short window, or they rejoin.
   - **Phase 3:** its heart freezes every pod. Ring it with pods and thaw them all at once.
5. **The Grumble Blight** (Midnight Greenhouse, true boss). The grumpiness itself: a cloud built from every grump.
   - **Phase 1:** it rains grumps from all four seasons.
   - **Phase 2:** it blacks out the board, and only lamp-lit tiles can be seen.
   - **Phase 3:** it shrinks to one sad seed. Plant it, and it grows into the estate's great tree: the **true ending**, with the whole estate in bloom.

#### Power-ups and meta-progression

- **The Seed Pouch** (six varieties, above). Plots offer varieties as hedge pickups; the shed sells starting ones.
- **Upgrades:**
  - seed packet (+pod), fertiliser (+reach) and quick boots (+speed), as today;
  - **garden gloves**: lob a pod over a hedge;
  - **wellies**: walk through your own blooms for one plot (the classic's flame-pass);
  - **trellis boots**: walk through hedges for 20 s (wall-pass);
  - **puffcap**: remote bursting.
- **The Bumblebee Buddy**: a rideable mount, hatched from an egg found in some hedges. It hovers one tile faster and **takes one bonk for you**. It then buzzes away to wait for the next egg.
- **Power has a price again.** A bonked gardener drops one level of each stat as pickups around its tile, and can win them back. This restores the classic's tension without wiping a run.
- **The Potting Shed** between seasons. Spend **seeds** earned in play (never real money) on:
  - an extra spare;
  - a starting variety;
  - a bee egg;
  - a **golden-seed hint**.

  Prices rise each season.
- **Medals per plot:** Full Bloom (100% In Bloom), No Bonks and Swift Gate (under par). There is a medal board per season.

#### Modes

- **Tour:** the campaign for 1–4 gardeners through the cabinet's `players` frames, with a shared spares pool, as today.
- **Flower Show:** the battle mode, recast kindly, for 2–4 players.
  - Each gardener's blooms paint flowerbeds in their own colour.
  - A gardener caught in a rival's bloom is **dizzy** for two seconds and drops a seed; nobody is knocked out.
  - After two minutes the most flowered tiles wins. Then **Last Bloom** begins: border hedges creep inward.
  - Eight arenas, each borrowing a season gimmick: conveyors, ice, wind, springy mushrooms, warp rabbit-holes, falling leaves, lamps and glass.
  - **Sneezy spores** are curse pickups: reversed controls, tiny blooms or auto-planting, passed on by touch.
- **Endless Allotment:** score attack across random plots; the leaderboard's main event.
- **Plot Trials:** time attack per plot, unlocked on a clear.

#### Classic features: matched or beaten

| The classic has | Seed Burst answers with |
| --- | --- |
| Exit hidden under a block; bombing it releases enemies | The Garden Gate and its bell |
| Hidden power-ups; losing a life costs power | Hidden pickups, and dropped power that can be won back |
| Eight-plus enemy roles; a time-out enemy | Fifteen grumps; the Grumble Cloud |
| Remote, pass and pierce power-ups; kick and throw; mounts | Puffcap, wellies, trellis boots, Dandelion, Pumpkin, gloves and the Bumblebee Buddy |
| Line bombs | Bramble, **plus** a diagonal X that the classic never had |
| Bonus stages | Four different Bonus Beds |
| World gimmicks and bosses | Five seasons' gimmicks and five phased bosses |
| Battle mode for four | The Flower Show, with eight arenas, Last Bloom and sneezy spores |

#### Slices

Roadmap: t-136 (slice 1), t-137 (slice 2), t-138 (slice 3), t-139 (slice 4), t-140 (slice 5). Slice 1 is `ready`; each later slice waits on the one before.


**Slice 1: Seed Pouch, Garden Gate and the first grumps.**
- The Seed Pouch: six burst shapes, swapped with B.
- Growing flowerbeds and In Bloom %.
- The Garden Gate with its bell, and golden seeds.
- Dropped power on a bonk that can be won back.
- The Grumble Cloud replaces the wind gust.
- Six new grumps, each with a readable tell: sulky slug, burrow mole, hedge hopper, buzz bully, seed thief and puffball.
- Plot data (hedge mask, gimmick tiles, grump script) replaces `SEED_CURVES` as the source of difficulty.

Verified with `test:arcade-engine`, a deterministic plot test, a pilot probe showing runs still end, and screenshots.

**Slice 2: Spring and Summer.**
- Spring (Kitchen Allotment) and Summer (Glasshouse Rows): 12 authored plots, each season with its own tile set, backdrop and title card.
- Gimmicks: regrowing hedges, watering cans, irrigation channels, glass panes and springy mushrooms.
- Bonus Beds: Butterfly Release and Sprinkler Dash.
- Bosses: Old Bramblebeard and Hothouse Hector.
- The Potting Shed, and save/resume at each season start through `saves.ts`.

**Slice 3: Autumn and Winter.**
- Autumn: gusts with windsock tells, leaf drifts and apple trees.
- Winter: ice paths, snowdrifts and cracking ponds.
- Grumps: pod weevil, acorn lobber, leafpile lurker, frost moth, snowball roller and mimic sprout.
- Bonus Beds: Apple Bowling and Snow Angels.
- Bosses: the Harvest Scarecrow and the Frost Topiary.
- Upgrades: gloves, wellies and trellis boots, and the Bumblebee Buddy mount.

**Slice 4: The Midnight Greenhouse and the endings.**
- The secret season: four dark plots with lamps and moonflowers, and the night owl.
- The Grumble Blight, credits and the true ending.
- Medals and the per-season medal board.
- Endless Allotment and Plot Trials.

**Slice 5: The Flower Show.**
- The 2–4 player battle mode through the cabinet's `players` frames, with tile painting, dizzy stuns and Last Bloom.
- Eight arenas built from season gimmicks.
- Sneezy spore curses.
- A results podium.

---

## 25. Station Sweep (Xenophobe riff)


### What is in the game today

| Area | Today |
| --- | --- |
| Stations | Endless numbered stations of 2 → 4 decks (station 4). Every deck is the same 1,600 px corridor, with two lifts at the same two spots (x = 180 and x = 1,420). Four deck looks (bulkhead, trim, floor and the planet outside) cycle per deck. |
| Critters | **Three.** The **roller** bowls along the floor and has to be swept crouching. The **crawler** drops from a ceiling sac and clings, draining charge until Mop jumps. The **biter** (3 hp) stalks and spits at waist height. Each grows **big** after 26 → 10 seconds left alone: tougher, harder-hitting, and a big biter spits faster. |
| Sacs | Floor sacs (3 hp, 4 hatches): 3 → 9 per deck by station 7. Ceiling sacs (can't be shot, 2 hatches): 1 → 5. |
| Weapon | **One** sweeper beam (A), with a crouching shot. No weapon pickups and no grenades. |
| Items | A repair kit (+30), dropped by 25% of popped sacs. |
| Clock | 45 seconds plus 24 per deck. Running out loses the station and a spare Mop. |
| Players | **Up to 3, split screen**, one strip per Mop, each free to ride to a deck of its own, with a shared clock and shared spares. This is a real strength. |
| Difficulty | Critters toughen on a "heat" of 1 + 3 × (station − 1). Biters max out at station 3, the hatch rate and growth timer at station 4, critter speed at station 5, and sac counts at station 7. **From station 7 on, every station is the same station.** |
| Scoring | 100 / 150 / 300 × station per critter, 200 × station per sac, 1,000 × station per clean deck, and 3,000 × station plus health and time per clean station. Spares come at 25,000, 75,000, 175,000 and so on. |
| Structure | No rooms or doorways, no adult or queen critter, no station identities, no ending, no saves, no music. |
| Code | `stationSweep.ts`, 2,591 lines. The seed-5 attract pilot lost its last station on station 3 after about 4 minutes. |

The screenshots show handsome decks, with portholes, ringed planets and lit pilasters, and Mop reads well at about 26 px. But the critters are 7–18 px tall, and the deck is one 160 px bulkhead tile repeated for 1,600 px. Deck 1 of station 1 and deck 2 of station 3 differ only in palette.

### Against the classic

The 1987 game Station Sweep riffs on is a three-player split-screen hunt through **many kinds of base**:

- **Three players at once,** each in their own strip, free to go their own way.
- **Floors joined by elevators,** and **doorways into side rooms**, so every floor of a base is a little map to explore, not a corridor.
- **Aliens with a life cycle:** eggs hatch rollers and ceiling droppers, which grow into larger crawlers and spitting adults, plus wall and floor ambushers.
- **Height-based fighting:** duck for the low ones, shake off the ones that grab you.
- **A range of weapon pickups and throwable grenades,** and objects lying around to collect for points or use.
- **A tally at the end of each base** of how much of it you cleared.

Station Sweep already matches the three-player split screen, the lifts, crouching and shaking off, growth, and a station clock.

**Verdict:** it has the classic's best bones, but every deck is the same corridor with the same three critters. There is one weapon, no rooms, no adult life stage or queen, nothing to collect and no reason for one station to differ from another. Its curve is flat by station 7.

### The upgrade: Station Sweep — The Orbit Line

Mop and two crewmates, **Squeegee** and **Dusty**, ride a little shuttle round a ring of six stations that circle a big, friendly gas giant. Each station has a job, a layout and a mess of its own.

Critters are never hurt: they are swept into Mop's **bin**. At the end of each station the bin is emptied into the **Critter Terrarium**, a nature dome that fills up with every species you have collected.

The signature twist is the **Infestation Map**. Every station is drawn as a cross-section (decks, rooms, vents), which shows in the radar and between lift rides. Left alone, sacs and nests spread **goo** through their rooms, and goo seeps through the vents to the deck above. A room that fills with goo grows a new nest. Crouch-sweeping a gooey floor mops it clean. The station becomes a living board you race. In co-op, splitting up across decks (the split screen's whole point) becomes the strategy, and the final Queen spans three decks at once.

**Target length:** a first clear in roughly 60–75 minutes.

#### Structure

- **Six stations** (acts) of 3–5 decks each. Every deck is a corridor with **2–4 doorways into side rooms**, and lifts sit wherever the layout puts them.
- Each station is authored data:
  - its deck lengths, rooms, lifts and vents;
  - its hazards and critter families;
  - its **station job** (a special objective);
  - its clock.
- A **Nest Mother** mid-boss guards the middle deck, and a **Queen** waits on the bottom deck.
- **Between stations:**
  - the **Supply Locker**, where credits earned in play buy upgrades;
  - the **Terrarium**.
- Progress saves at each station through `utils/arcade/saves.ts`. A clear rolls credits and unlocks **Double Shift**, a New Game+.

**Rooms behind the doorways** (press Up at a doorway; lifts keep their lit frames so the two never look alike):

- **Supply closet:** a tool pickup.
- **Crew cabin:** a stranded crewmate to walk to a lift. Each one rescued adds 10 seconds to the clock.
- **Lab:** specimen jars (bonus points), and sometimes a mimic.
- **Galley:** snacks that restore charge.
- **Vent shaft:** a shortcut to the same spot on the deck above or below.
- **Nest room:** a cluster of sacs. Clearing it stops goo spreading on that deck.
- **Control room:** switches one hazard off (vents, lights or gravity).

#### The stations

| # | Station | Decks and hazards | New critters | Station job | Queen |
| --- | --- | --- | --- | --- | --- |
| 1 | **Greenhouse Ring** | Today's decks with doorways added; **sprinklers** whose mist (after a tell) makes floors slippery; **vine curtains** that hide critters | Rollers, crawlers and biters with full growth chains; **puffer** | **Seed Vault**: reach the seed vault before the goo does | **Mother Gloop** |
| 2 | **Laundry Moon** | **Conveyor floors**; **steam vents** that hiss before they blow; **washing-machine rooms** that tumble critters out | **Gloop**, **mimic crate** | **Spin Cycle**: clean every room while the conveyors run | **The Laundry Kraken** |
| 3 | **Star Observatory** | **Dark decks** where Mop's headlamp lights a cone ahead; a **telescope room** whose beam swings; light switches in the control rooms | **Lamp moth**, **hopper** | **Lights On**: restore every deck's lighting | **Professor Puff** |
| 4 | **Cargo Dock** | **Airlocks** that tug everything toward a hatch after a tell (crouch to hold the rail); **cargo crates** to stand on; **crane hooks** | **Vent eel**, **bin raider** | **Inventory**: escort three crates to the lift | **The Cargo Crab** |
| 5 | **Zero-G Gym** | **Low gravity**: jumps go high and float, and critters drift; **trampolines**; **rotating rings** | **Tumbler**, **bounce-ball** | **Gym Class**: clean while the gravity flips | **Big Bouncy** |
| 6 | **The Hive** | Goo everywhere, every hazard, decks linked by vents | Every family at full growth | — | **Queen Mumble** (three decks at once) |

#### The roster: 3 → 12 families

Every family has a readable life stage, so the classic's growth runs through the whole roster. The three original families grow through three stages each.

| Family | Stages | Behaviour | Tell | Answer |
| --- | --- | --- | --- | --- |
| **Roller** | rollerbub → roller → boulderbelly | Bowls along the floor; the adult rolls in pairs and bounces | A growl before it charges | Crouch-sweep; the Foam Gun stops it |
| **Crawler** | ceiling bub → clinger → web weaver | Drops and clings; the adult spins a ceiling web that drops babies | A shadow on the floor | Jump to shake it off; the Vac Pack pulls it down |
| **Biter** | nipper → biter → snapper | Stalks and spits at waist height; the adult spits three ways | Puffed-out cheeks | Crouch; get round behind it |
| **Puffer** | puff → puffer → spore cloud | Swells and pops into sticky spores | Swells up | Sweep it at range before it gets close |
| **Gloop** | blob → gloop → big gloop | Splits in two when swept, unless foamed first | Wobbles | Foam, then sweep; or vacuum it whole |
| **Lamp moth** | — | Flies at Mop's headlamp on dark decks and dazzles | Flutters toward the light | Switch the lamp off (Down + B) |
| **Hopper** | — | Leaps over standing shots | Crouches before it leaps | Shoot it mid-air |
| **Vent eel** | — | Lunges from floor vents | The grate rattles | Crouch-sweep at the grate |
| **Mimic crate** | — | A crate that blinks, then snaps | A blink | Sweep it before you stand on it |
| **Bin raider** | — | Steals critters out of Mop's bin and lets them loose | Sniffs at the bin | Sweep it before it reaches you |
| **Tumbler** | — | Floats in arcs in zero gravity | Spins up before it changes course | A Bubble Grenade |
| **Bounce-ball** | — | Bounces between floor and ceiling | Squashes as it lands | Time your shot for the bottom of its bounce |

**Nest Mothers** (one per station) sit in the middle deck's nest room and lay fresh sacs until swept. Each wears its station's family colours.

#### The tools: 1 → 8

Tools are found in supply closets and upgraded at the Locker. The classic's weapon pickups and grenades become cleaning gear:

- **Sweeper Beam:** today's tool.
- **Wide Nozzle:** three-way spread (low, level and high).
- **Foam Gun:** stops critters and glues them to the floor.
- **Vac Pack:** pulls critters in at short range, straight into the bin.
- **Bubble Grenades:** lobbed, and trap critters in floating bubbles. The answer to hoppers and tumblers.
- **Zap Broom:** a piercing shot.
- **Steam Wand:** cleans goo and stuns biters.
- **Squeegee Shield:** blocks spit from the front.

#### The Queens: 0 → 6 bosses

1. **Mother Gloop:** a pond of goo filling a room.
   - **Phase 1:** she slops blobs off her surface. Sweep the blobs.
   - **Phase 2:** she splits into four gloops that re-form if left. Foam them.
   - **Phase 3:** she pours herself into the vents. Ride a lift after her and finish her in the nest room on the deck above.
2. **The Laundry Kraken:** tentacles out of six washing machines.
   - **Phase 1:** tentacles slam down, each with a shadow as its tell.
   - **Phase 2:** it flings socks (spit) while the conveyor speeds up.
   - **Phase 3:** its head rises from the big machine. Steam Wand it, then sweep it.
3. **Professor Puff:** a huge puffer in the dark observatory.
   - **Phase 1:** he floats in the dark, seen only in the headlamp.
   - **Phase 2:** spore clouds fill the room. The Steam Wand clears them.
   - **Phase 3:** swing the telescope's beam onto him to shrink him.
4. **The Cargo Crab:** a crab the size of the cargo bay.
   - **Phase 1:** its claws snap from left and right, and its shell is armoured at the front.
   - **Phase 2:** the airlocks tug. Hold the rails.
   - **Phase 3:** it hides under the crates. Bubble Grenades lift them.
5. **Big Bouncy:** a giant ball-critter in zero gravity.
   - **Phase 1:** it bounces off floor and ceiling in arcs.
   - **Phase 2:** it splits into four bouncing halves.
   - **Phase 3:** gravity flips every 5 seconds.
6. **Queen Mumble:** she spans three decks.
   - **Phase 1:** her **head** on the top deck spits, her **middle** on the second lays eggs, and her **tail** on the third sweeps the floor. Each part grows back if left alone for 20 seconds.
     - With three players, each takes a part on their own split screen.
     - Solo, Mop rides the lifts between them, and the lifts run fast during the fight.
   - **Phase 2:** she pulls herself into the shaft, and the parts swap decks.
   - **Phase 3:** the whole station shakes. Sweep her crown on the top deck while the crew holds the lifts.

   She was only lonely, and she becomes the Terrarium's queen.

#### Systems that run through the whole line

- **Goo and the Infestation Map:** goo spreads from nests through rooms and vents, and mopping cleans it. Each station ends with a **clean percentage**, the classic's end-of-base tally, and a bonus for it.
- **The bin and the Terrarium:**
  - Swept critters fill the bin, and a full bin slows Mop a little. Empty it at a lift.
  - The Terrarium's species book has a page for each family and each stage, and a medal for each finished family.
  - With every page full, the true ending opens the dome to the public.
- **Crew rescues** add time to the clock.
- **The Supply Locker:** credits buy tool upgrades, a spare Mop, more clock, a bigger bin, and a radar that shows the sacs.
- **Bigger critters:** young critters 14–28 px tall instead of 7–18 px, adults 32 px or more. Mop stays at about 26 px.
- **Deck art:** six station tilesets, each with its own rooms, so the 160 px bulkhead no longer repeats for a whole deck.
- **Music:** one loop per station, with an alarm layer when the clock runs low.

#### Modes and players

Up to three players on the split screen (`maxPlayers: 3`, as today).

- **The Orbit Line:** the campaign, 1–3 players.
- **Night Shift:** endless stations. This is the leaderboard's main event.
- **Speed Clean:** a time attack per station.
- **Sweep-Off:** 2–3 players, each on their own copy of the same station, racing to 100% clean.

#### The classic's signatures, matched or beaten

- **The three-player split screen:** already matched, and beaten by a Queen built for three screens.
- **Floors joined by elevators, and doorways into rooms:** matched.
- **Aliens that grow from eggs into adults:** matched and deepened, with twelve families and three stages for the originals.
- **Height-based fighting:** already matched.
- **Weapon pickups and grenades:** matched by eight tools and the Bubble Grenades.
- **Many kinds of base:** matched by six stations with their own jobs.
- **The clear tally at the end of a base:** matched by the clean percentage.
- **Beyond the classic:** goo spread and the Infestation Map, crew rescues, and the Terrarium.

#### Slices

Roadmap: t-141 (slice 1), t-142 (slice 2), t-143 (slice 3), t-144 (slice 4), t-145 (slice 5). Slice 1 is `ready`; each later slice waits on the one before.


| Slice | Scope |
| --- | --- |
| 1 | Growth chains for the three families, puffer and gloop, bigger critters, the eight tools, the bin, the Supply Locker, music |
| 2 | Doorways and side rooms, authored deck format, Greenhouse Ring and Laundry Moon, mimic crate, Nest Mothers, Mother Gloop and the Laundry Kraken, crew rescues, save/resume |
| 3 | Goo spread and the Infestation Map, Star Observatory and Cargo Dock, lamp moth, hopper, vent eel, bin raider, Professor Puff and the Cargo Crab |
| 4 | Zero-G Gym and the Hive, tumbler and bounce-ball, Big Bouncy and Queen Mumble, the Terrarium, endings, Double Shift |
| 5 | Night Shift, Speed Clean, Sweep-Off, medals |

- **Slice 1, critters that grow up, and tools to match.**
  - **Delivers:**
    - Three-stage growth chains for rollers, crawlers and biters, with adult behaviours (paired rollers, web weavers, three-way snappers).
    - The puffer and gloop families.
    - Critters redrawn at 14–28 px, with adults at 32 px or more.
    - The eight tools, as pickups from popped sacs for now.
    - The bin and the critter count.
    - The Supply Locker with its credit economy.
    - The first music loop.
  - **Verified by:** a new `verifyStationSweep.test.ts` in `test:arcade-engine` covering growth timing, each tool's answer and a deterministic seeded deck, plus the existing three-seat tests.
- **Slice 2, rooms and the first two stations.**
  - **Delivers:**
    - Doorways into side rooms: supply closet, crew cabin, lab, galley, vent shaft, nest room and control room.
    - An authored station and deck format in `utils/arcade/stationSweep/`, with lifts and vents placed per deck.
    - The Greenhouse Ring and the Laundry Moon, with sprinklers, vine curtains, conveyors, steam vents and washing-machine rooms.
    - The mimic crate.
    - The Nest Mother mid-boss.
    - Mother Gloop and the Laundry Kraken.
    - Crew rescues that add clock time.
    - The Seed Vault and Spin Cycle station jobs.
    - Save and resume per station through `saves.ts`.
  - **Verified by:** a scripted clear of the Greenhouse Ring and screenshots of every deck and room.
- **Slice 3, the living station.**
  - **Delivers:**
    - Goo that spreads through rooms and vents, crouch-mopping, and the Infestation Map in the radar and between rides.
    - The clean percentage.
    - The Star Observatory and the Cargo Dock: dark decks and the headlamp cone, the telescope beam, airlocks, crates and crane hooks.
    - The lamp moth, hopper, vent eel and bin raider.
    - Professor Puff and the Cargo Crab.
    - The Lights On and Inventory station jobs.
  - **Verified by:** a deterministic test of goo spread and boss-phase tests.
- **Slice 4, the Gym, the Hive and the ending.**
  - **Delivers:**
    - The Zero-G Gym with low-gravity physics, trampolines and rotating rings.
    - The tumbler and the bounce-ball.
    - Big Bouncy.
    - The Hive, and Queen Mumble across three decks: one part per split-screen strip, and fast lifts for solo play.
    - The Terrarium and its species book.
    - The credits, the true ending and Double Shift.
  - **Verified by:** a three-seat Queen test and a scripted full-campaign test.
- **Slice 5, the modes.**
  - **Delivers:**
    - Night Shift as the endless leaderboard mode.
    - Speed Clean time attacks.
    - Sweep-Off versus for 2–3 players on mirrored copies of one station.
    - The per-station medal board.
  - **Verified by:** engine tests for Sweep-Off seats.
