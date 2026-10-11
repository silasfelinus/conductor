# Depth Pass — Pipe Pals and Prize Show Panic

**Owner:** `kr-arcade`, milestone m7 (tasks t-023..t-025, t-030, t-031 for Pipe Pals; t-026..t-029, t-032..t-034 for Prize Show Panic), code in kind_robots `utils/arcade/games/`.
**Direction:** Silas, 2026-10-11 (verbatim): *"Our kind robot arcade can still use some visual and gameplay
improvements. The first targets are our riffs on Mario bros and smash tv, as those we both favorites of mine
as a child. I want and assessment of levels. Smash tv had an extensive level system, an announcer, prize
screen, various enemies, and a final boss fight. Mario bros lasted multiple varied stages, including ice
levels, coin pickup challenges, and various enemies. We don't need to be 1:1 copies of these games, but we
should be equally complex or more so. For now especially the Mario riff looks just like a smaller formed
version, including to the point of toned down limited turtles. We should have more complex enemies,
variety, etc"*

Silas, 2026-10-11, on the first draft of this plan: *"Love the improvement suggestions, now I want you to
expand both pitches to add even more to each, so we really are homages with even more inspired levels and
gameplay depth."* The upgrade sections below are that expanded version.

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

### The upgrade: Pipe Pals — Three Shifts in the Plumbing City

Keep the single-screen bump-and-kick core that makes the classic great. Build a whole city of plumbing
around it, so every district asks something new of the same two verbs.

**Target length:** a first clear in roughly 45–60 minutes, with the difficulty coming from new threats,
new boards and new objectives, never from padding.

#### Structure

- The campaign has **three Shifts** (acts) with **eight districts**, plus a **boss at the end of each Shift**
  and a **secret ninth district**.
- Each district has **5 phases**:
  - phases 1–2 introduce the district's new threat;
  - phase 3 is the district's **special objective phase**;
  - phases 4–5 remix the district's threat with everything learned so far.
- Then come the district's own **bonus round** and a visit to **the Workshop**.
- Every district has its own board layout (original layouts), backdrop, tiles, music loop and title card.
- A clear rolls credits and unlocks the **Night Shift Overtime** New Game+.
- Progress saves at each district start through `utils/arcade/saves.ts`, as Ghost Trail does.

#### The districts

**Shift 1: Day Shift**

| # | District | Board and mechanic | New threats | Special phase | Bonus round |
| --- | --- | --- | --- | --- | --- |
| 1 | **Rooftop Reservoir** | Today's board, tightened; water tanks and the dusk city behind | Shell crawler, crab bot | **First Fix**: three leaky joints spray across a ledge until a pal bumps them shut | Static coins (today's round) |
| 2 | **Greenhouse Mains** | **Vine ledges** that sag under weight and drop you a floor if you stand too long; a moving lift; sprinkler rain | **Spring flea** (hops; can only be flipped while landed), **shell knight** (first bump knocks its armour off and the bare crawler sprints; a second bump flips it) | **Seedling Rescue**: potted sprouts sit on the ledges and critters trample them; save at least four | Coins drift down from the sprinkler heads |
| 3 | **Suds Works** (laundry basement) | **Soapy ledges** (slight slide); bumping a sudsy ledge blows a **bubble** up that can trap a walker. A trapped critter floats, and touching it pops it out for a kick. | **Lint moth** (flutters in a wave; flippable only while it rests on a ledge), **sock puppet** (flipping splits it into two small socks; kick both) | **Lost Socks**: matching-colour sock pairs tumble from the pipes; collect pairs, not singles | Coins ride rising bubbles |

**Boss 1: The Big Shell.** A shell crawler as wide as a ledge. It climbs the board floor by floor:
- bump the ledge under each of its feet to tip it over, then kick its soft underside;
- it takes three tip-and-kick cycles, and it sheds small crawlers from its shell between them;
- in its final phase it curls up and rolls along the bottom floor, and pals dodge it from the ledges.

**Shift 2: Swing Shift**

| # | District | Board and mechanic | New threats | Special phase | Bonus round |
| --- | --- | --- | --- | --- | --- |
| 4 | **Cold Storage** (the ice district) | **Icy ledges**: low friction and long stops. **Icicles** grow under ledges and drop on a visible tell. | **Frost bot** (freezes the ledge it walks; one bump clears it, no kick needed), **snowball roller** (grows as it rolls; bump it while small) | **Thaw Run**: spare robots frozen in ice blocks; bump each block three times to free them before the freezers re-ice them | Coins on all-ice floors |
| 5 | **Boiler Works** | **Steam vents** puff on a beat; a **crumble ledge** that breaks after two crossings and rebuilds next phase | **Ember spark** (bounces diagonally; bump the ledge under it to snuff it), **lurker ember** (slides in along a floor if a phase drags; anti-camping) | **Pressure Valves**: four gauges on the ledges creep toward red; bump each to vent it before it bursts and steams a floor shut | Coins inside timed steam bursts |
| 6 | **Clockwork Water Tower** | **Gear ledges** slide left and right on the clock; a **conveyor** ledge | **Gear bug** (winds up, pauses, dashes; flippable only when wound down), **cuckoo** (pops from a clock pipe on the hour and swoops one floor) | **Valve Routing**: bump the valve wheels to switch which pipes critters use. Route them all to one floor and bowl them for a giant chain. | Coins on moving gears |

**Boss 2: The Thermostat.** A great dial machine on the back wall that flips the board between
**FREEZE** (ice ledges, frost bots) and **HEAT** (embers, steam).
- Its needle points at one ledge at a time. Bump that ledge while the needle glows to send a shock up the
  pipe.
- Three phases, each with a faster dial and more of both elements at once.
- At the end both halves fight over the board in a half-frozen, half-boiling arena.

**Shift 3: Night Shift**

| # | District | Board and mechanic | New threats | Special phase | Bonus round |
| --- | --- | --- | --- | --- | --- |
| 7 | **Flooded Mains** | **Water rises and drains** on a telegraphed cycle. Underwater the pals move slower and jump floatier, and flipped critters bob upward, so kick them before they float off. | **Pipe eel** (strikes from the side pipes on a tell; bump the ledge by the pipe to send it back), **bubble jelly** (drifts up; bump it to pop it into a short-lived bubble platform) | **Pump Station**: bump three pump buttons in the right order to drain the board before it floods the top floor | Underwater coins, with air bubbles to grab |
| 8 | **Storm Drain at Midnight** | A **dim board**. Lamps light pools around the pals; lightning flashes light the whole board on a beat (the tell). | **Grease beetle** (bump, kick, and it leaves a slick), **mimic coin** (looks like a coin but blinks first; grab one and it bites), and remixes of every earlier threat | **Lights Out**: relight every lamp by bumping it from below while critters hunt in the dark | **Test of skill**: coins hung under ledges, bump to collect |

**Finale: The Great Clog.** The Clog King, a huge creature of tangled junk living in the city's main
drain.
- **Phase 1:** it surfaces from different pipes. Bump the ledges it rests on to crack its plates.
- **Phase 2:** it sheds critters from every district while the water rises.
- **Phase 3:** it wraps the central pipe. Kick the loose plates back into its glowing core.
- **The flush:** the city's water finally runs free and the pals **climb for the rooftop** ahead of the
  rising flood, a vertical escape that tops the campaign.

**Secret district: The Golden Main.** One **golden valve handle** is hidden in each district, earned by
completing that district's special phase perfectly.
- With all eight, a ninth district opens: mirrored boards, the fastest critters and coins everywhere.
- Clearing it gives the **true ending**: every fountain in the city runs rainbow water.

#### The roster: 2 → 15 critters, 3 bosses

| Critter | Answer it asks for |
| --- | --- |
| Shell crawler, crab bot | Bump, kick (crab: two bumps) |
| Shell knight | Bump off the armour, then deal with a sprinter |
| Spring flea, lint moth, gear bug | Timing: flip only while landed, resting or wound down |
| Sock puppet | Kick both halves; a chain opportunity |
| Frost bot, snowball roller | Clear the ice; catch it small |
| Ember spark, lurker ember | Snuff from below; don't camp |
| Cuckoo, pipe eel | Read the clock or the pipe tell |
| Bubble jelly | Turn it into a platform |
| Grease beetle | Three-step answer, mind the slick |
| Mimic coin | Read the blink before you grab |

Hazards: leaky joints, vine and crumble ledges, icicles, steam vents, gear and conveyor ledges, flood
water and the dark. Bosses: the Big Shell, the Thermostat and the Clog King.

#### Systems that run through the whole campaign

- **Readable recovery tiers:** calm, cross and furious colours, a speed step each, and a **last-critter
  rush**.
- **Turnaround:** walkers turn round when they meet.
- **Kick chains:** 800 → 1,600 → 2,400 → 3,200 → 5,000 inside a short window, shown as a growing floater.
- **Kick bowling:** a kicked critter slides along its ledge. It knocks any flipped critter in its path off
  with it, and that counts toward the chain. It flips an upright critter it hits.
- **Coins:** every kick sends a coin out of a pipe, so the board keeps feeding the player.
- **The KIND block** refills each district. The Workshop can give it a fourth charge and a **KIND burst**
  that also pulls every coin on the board to you.
- **Tool Belt pickups** now and then roll out of the top pipes, short and readable:
  - **Wide Wrench:** triple bump reach.
  - **Kick Boots:** kicks bowl the whole ledge.
  - **Bubble Wand:** blow a bubble that traps a walker.
  - **Magnet Cap:** coins come to you.
- **The Workshop** opens between districts. Spend coins earned in play (never real money) on:
  - an extra pal;
  - a KIND charge;
  - a starting tool;
  - **Lucky Pipe** (more coins next district);
  - a **valve hint** that shows where the district's golden valve is.

  Prices rise each Shift.
- **Medals:** each phase can earn Clean Sweep (no hit), Chain Master (a 4-chain) and Swift Fix (under par
  time). A medal board per district rewards replays.
- **Two pals with their own feel:** the teal pal has a longer bump reach; the pink pal jumps higher and
  floats a little. Solo players pick one; co-op seats both.
- **Modes:**
  - **Campaign.**
  - **Overtime:** endless score attack across random districts; this is the leaderboard's main event.
  - **Time Trial:** per district, unlocked on a clear.
  - **Versus:** two pals race to kick the most. They can bump each other from below to steal a flip; it's a
    playful stun, never a knockout.
- **Bigger actors:**
  - Hero ~24–28 px tall and critters ~18–22 px. Get there by drawing at double density, or by moving the
    logical world toward 320 × 240 (the Ghost Trail blueprint used a 40–48 px hero on a 240-high screen).
  - At least three walk frames per critter, a flip/kick squash, and recovery colours.
  - Every boss is drawn as its own large sprite with telegraph animations.

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

### The upgrade: Prize Show Panic — a full broadcast season

The classic is a single show. Prize Show Panic becomes a whole **network season**. Each episode is a
different kind of TV show on its own soundstage, with its own floor hazards, crashers and bosses. The host
holds it all together, and a ratings meter rewards style.

**Target length:** a first clear of the season in roughly 60–75 minutes.

#### Structure

- The season has **four episodes and a Live Finale**.
- Each episode is a **map of 12–14 rooms** on a grid, with a mid-boss partway through and a boss at the
  end.
- Between rooms, a **map screen** shows:
  - where you have been;
  - what each neighbouring door leads to: swarm, prize vault, trap, sponsor challenge or boss;
  - a **danger rating** and a reward icon for each room;
  - the route you choose.

  Branches matter: a safe route and a rich route always exist side by side.
- Between episodes come the **prize tally screen**, the **Prize Swap** and a **commercial break** (all
  below).
- Hidden across the season are **twelve golden tickets**. Ten of them open the **Grand Prize Vault**.
- A clear rolls credits and unlocks **Rerun** (New Game+ with remixed room scripts) and episode select.
- Progress saves at each episode start.

#### The episodes

| Episode | Set and hazards | New crashers | Mid-boss | Boss |
| --- | --- | --- | --- | --- |
| 1. **Opening Night** (the game show) | Today's studio with marquee bulbs. Mine sets, spotlight rigs, the camera wall. | Grabber, bouncer, conga line, thrower, popper, stagehand, camera crane | **The Parade Float** (today's cake float, now with a second phase) | **The Big Wobble** |
| 2. **Cooking Showdown** (the kitchen) | **Hot-plate tiles** glow, then sizzle; **flour clouds** hide crashers; **conveyor counters** carry everyone | **Pie chef** (lobs arcing pies whose splats leave slippery cream), **egg-timer bot** (ticks down, then hatches a clutch of tiny crashers), **meatball roller** | **The Pie Cart** | **The Soufflé Supreme** |
| 3. **Countdown Concert** (the music show) | **Beat-synced rooms**: speaker stacks thump **bass rings** on the beat; strobes; mosh-pit circles that shove you | **Roadie** (pushes flight cases that are moving cover and moving walls), **stage diver** (leaps across the room and lands in a shockwave), **heckler** (pumps up nearby crashers until you cheer it) | **The Mosh Mascot** | **The Jumbotron** |
| 4. **Galaxy Parade** (the sci-fi soundstage) | **Low-gravity rooms** where Sparkle drifts on momentum; a **rotating ring room**; **teleport doors** | **Saucer cam**, **mirror clone** (copies your moves a beat late), **fluffball** (multiplies if left alone), **spotlight drone** | **The Saucer Cam Mothership** | **The Conga Dragon** |
| **Live Finale** | One long run of rooms that remixes every set, a commercial break mid-run, then the main stage | All of them | — | **The Host's Prize Machine** |

**Room types** (all data-defined scripts):
- **Swarm** (today's room, scripted).
- **Mine set**: whoopee-cushion and banana-peel mines on the floor.
- **Light rig**: spotlight beams sweep the floor on a beat.
- **Camera wall**: turret cameras along one wall.
- **Speed round**: short timer, double prize drops.
- **Prize vault**: no enemies, prizes on pedestals, closes fast.
- **Ambush**: all four doors at once.
- **Conga ballroom**: lines only, long and fast.
- **Sponsor challenge**: clear without a hit, or grab every prize, for a golden ticket.
- **Secret room**: off the map, behind a cracked wall the host hints at.

**Room modifiers**, rolled from data on later visits and in Rerun:
- **Lights Out**: only spotlights.
- **Foam Party**: slippery for everyone.
- **Confetti Storm**: low visibility.
- **Double Time**: everything faster, prizes doubled.
- **Audience Participation**: the crowd throws helpful items.
- **Sudden Death**: one hit, but a huge prize.

#### The roster: 4 → 19 crashers

| Crasher | Behaviour | Answer |
| --- | --- | --- |
| Grabber, bouncer, conga line, thrower | As today, scripted | As today |
| **Popper** | A balloon bot that bursts into a ring of streamer shards | Pop it at range |
| **Sweeper tank** | Slow, armoured front, fires a bubble burst | Flank it |
| **Stagehand** | Lays floor mines as it walks | Catch it early |
| **Spotlight drone** | Orbits, then locks a beam on for a charge | Break line or out-pace |
| **Mascot** | A big costume with a charge and a belly-bounce | Dodge the charge, hit its back |
| **Camera crane** | Wall turret | Out-angle it |
| **Pie chef** | Arcing pies, slippery cream splats | Keep moving, mind the floor |
| **Egg-timer bot** | Counts down, then hatches a clutch | Cheer it before zero |
| **Meatball roller** | Rolls in long straight lines and ricochets | Sidestep, then spray |
| **Roadie** | Shoves flight cases around | Use the cases as cover |
| **Stage diver** | Leaps and lands in a ring | Read the shadow |
| **Heckler** | Pumps up the crashers around it | Cheer it first |
| **Saucer cam** | Hovers and beams prizes away | Save the prize, then the saucer |
| **Mirror clone** | Copies your moves a beat late | Move so it walks into your spray |
| **Fluffball** | Multiplies if left alone | Clear them early |

There is also a **boom mic** hazard that drops from the ceiling on a tell and lifts you away for a moment.

#### The arsenal: 3 → 10

- Kept from today: spread, rapid and shield.
- New:
  - **Party poppers:** a lobbed area blast.
  - **Bubble rockets:** slow, heavy and piercing.
  - **Streamer orbiters:** two spinning ribbons that guard you.
  - **Roller skates:** speed.
  - **Glitter laser:** a piercing beam.
  - **Foam cannon:** slows crashers and foams the floor under them.
  - **Cardboard cutout:** a decoy of you that crashers chase.
- Short durations and stacking timers, all shown in the HUD.

#### The bosses: 1 → 9

Every boss is a different fight with real phases and telegraphs, not an HP sponge.

1. **The Parade Float** (episode 1 mid-boss): today's float, plus a second phase where the cake's candles
   light and fire volleys.
2. **The Big Wobble** (episode 1): a giant inflatable mascot. Each arm and leg is its own target, and
   popping one changes its attacks (arm gone: no slam; leg gone: it hops).
3. **The Pie Cart** (episode 2 mid-boss): a runaway dessert trolley that circles the room firing pies and
   dropping cream slicks.
4. **The Soufflé Supreme** (episode 2): it rises (untouchable, raining steam rings) and falls (open to
   attack). At half health it splits into a swarm of cupcakes that re-form if you leave them.
5. **The Mosh Mascot** (episode 3 mid-boss): a giant costume that crowd-surfs across the room on a sea of
   crashers. Clear the crowd and it falls.
6. **The Jumbotron** (episode 3): a wall of video screens with a face. Screens flip open to turrets, and the
   face jumps from screen to screen in time with the music. Crack the screens to corner it.
7. **The Saucer Cam Mothership** (episode 4 mid-boss): it beams prizes up from the floor. Win them back by
   breaking its tractor beam.
8. **The Conga Dragon** (episode 4): a long segmented parade dragon in low gravity. Segments drop off as
   you confetti them and become dancers; the head speeds up as it shortens.
9. **The Host's Prize Machine** (Live Finale): the host rides a giant prize wheel. Each spin lands on a
   different attack set, and the wheel shows the next one. In a last phase the host jumps out and it's a
   one-on-one dance-off duel.

The **Grand Prize Vault** opens after the finale for anyone holding ten golden tickets. It is a gauntlet of
every set, the host cheering *for* you this time, and the **true ending**: the party crashers all join the
studio audience.

#### The show: what makes it a broadcast

- **The host and the announcer.**
  - A host robot portrait cuts in at the edge of the screen with short original lines in a speech panel.
    Lines trigger on: room start, a big prize, a near miss, low time, a boss intro, a death and a clear.
  - From episode 3 a dry **co-host** camera bot joins in.
  - The host reacts to your style: a long cheer chain, a no-damage room, a risky route.
  - Voice is WebAudio bleep-speak (pitch patterns; no speech synthesis needed).
  - All lines are original writing; no catchphrases from the source.
- **The ratings meter**, the signature system. It fills with style: cheer chains, near misses, prize grabs
  and no-damage rooms. It drains when you're idle or hit. Four tiers, from **Off Air** to **Prime Time**:
  - Each tier raises the score multiplier.
  - At Prime Time a **sponsor care package** drops.
  - Down at Off Air, the producer throws in a **plot twist**: an extra hazard, to win the viewers back.
- **Cheer chains:** cheering crashers in quick succession builds a multiplier that the announcer counts
  out.
- **The prize tally screen:** after each episode, each prize kind counts up with its sprite and a tick
  sound, followed by golden tickets, ratings and an episode bonus. The game-over screen shows the season
  haul the same way.
- **The Prize Swap:** after the tally, trade prizes for upgrades. A car buys an extra contestant, a toaster
  a starting power-up, cash extra seconds on the clock; a golden ticket can reveal one secret room. It is
  in-game prizes only, never real money.
- **Commercial breaks:** a short mini-game between episodes, each a TV homage:
  - **Spin the Wheel:** a timing game.
  - **Catch the Prizes:** run under falling prizes.
  - **Pie Dodge.**
  - **Higher or Lower:** guess whether the next prize is worth more.
- **The studio:** an APPLAUSE sign that lights on kills, an audience band along the bottom wall that cheers
  big moments, and camera-flash juice on boss hits.

#### The contestants and the modes

- **Four contestants**, each with their own sprite and feel:
  - **Sparkle:** balanced.
  - **Zippy:** fast, with a narrow spray.
  - **Boomer:** slow, with a wide heavy cannon.
  - **Glimmer:** a shield that recharges.

  Up to four play at once, through the cabinet's `players` frames.
- **True twin-stick aim:** extend the engine input with an optional aim vector (the way `plunger` is
  optional on `InputFrame`). It comes from the gamepad's right stick, a second on-screen stick on touch, or
  a split keyboard (move on WASD, aim on the arrows). Hold-B aim lock stays for single-stick players.
- **Modes:**
  - **Season.**
  - **Rerun:** NG+ with remixed scripts and modifiers.
  - **Marathon:** endless rooms, the leaderboard's main event.
  - **Episode select:** after a clear.
- **Medals per room:** Flawless, Full Haul, Prime Time. A medal board per episode.

---

## 3. Order of work

Both are `large` games under the factory rules, so they ship in playable slices. Each slice is merged and
verified with `test:arcade-engine`, eslint/prettier and vue-tsc, plus a deterministic campaign test, a pilot
probe showing runs still end, and Pixel/HD screenshots. Pipe Pals goes first, because Silas called it out as
the weaker of the two.

**Pipe Pals**

| Slice | Task | Scope |
| --- | --- | --- |
| 1 | t-023 | Bigger actors, recovery tiers, chains, kick bowling, turnaround, first new threats, tool belt |
| 2 | t-024 | Day Shift: districts 1–3, special phases, the Big Shell, the Workshop |
| 3 | t-025 | Swing Shift: districts 4–6 (ice, steam, clockwork), the Thermostat |
| 4 | t-030 | Night Shift: districts 7–8, the Clog King and the flush, the Golden Main, endings, save/resume |
| 5 | t-031 | Two pals (co-op and Versus), Overtime, Time Trial, medals |

**Prize Show Panic**

| Slice | Task | Scope |
| --- | --- | --- |
| 1 | t-026 | Season map engine, authored rooms and modifiers, episode 1 Opening Night, golden tickets |
| 2 | t-027 | Crasher roster and arsenal, true twin-stick aim |
| 3 | t-028 | Host, co-host, ratings meter, cheer chains, prize tally, Prize Swap, studio audience |
| 4 | t-029 | Episodes 2–3 (Cooking Showdown, Countdown Concert), their mid-bosses and bosses |
| 5 | t-032 | Episode 4 Galaxy Parade, the Live Finale, the Grand Prize Vault, endings, save/resume |
| 6 | t-033 | Commercial-break mini-games, four contestants, co-op for up to four |
| 7 | t-034 | Rerun, Marathon, episode select, medals |
