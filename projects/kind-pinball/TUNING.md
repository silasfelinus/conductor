# Kind Pinball — tuning evidence (t-013)

Silas's finish line for AMI Village Rescue is "truly fun, complex, and quality,
as good as any Pinball FX3 table". This file holds the numbers behind that
judgement, so tuning rests on evidence rather than feel. Every rules or geometry
change reruns the harness and adds a dated section here, newest first; the top
section is the table's current state.

## How the numbers are made

`npm run tune:pinball -- --games 10 --minutes 15` in kind_robots
(`utils/scripts/pinballTuning.ts`) plays seeded headless games on the real
Rapier physics and the real rules, with a bot at three skill levels
(`utils/arcade/pinball/tuning/bot.ts`):

| Bot | Saves | Flip timing | Cradles | Aims | Nudges |
|---|---|---|---|---|---|
| novice | 60% of balls | ±4 ticks | never | no | no |
| average | 80% | ±3 ticks | half the lone balls | blind | no |
| good | 93% | ±1 tick | most lone balls | from the aiming chart, at what is lit | dead-centre balls |

The bot flips once a ball (read two ticks ahead) is over the flipper, lets a
slow ball roll out toward the tip first, and flips again at a ball that comes
back down. The same flags give the same numbers.

**Drain causes:**
- **outlane:** the ball left past either inlane guide.
- **SDTM:** straight down the middle, untouched by a flipper in its last 0.75 s.
- **center:** between the flippers, just after touching one: a miss or a dribble.

**The aiming chart** (`tuning/aim.ts`) is the table's shot-geometry evidence.
It covers 90 timings (1.5 s) per flipper, from two feeds:
- **cradle:** the ball held on a raised flipper, released, then flipped after a delay;
- **inlane:** the ball rolled down the inlane onto a resting flipper.

It records which shot each timing makes.

**Targets from the brief:**
- a decent player's ball lasts 60–120 s (FX3-like);
- a new player reaches multiball within a few games;
- a good player can reach the wizard mode.

## 2026-10-10 — t-023: the Ridge's flippers and the Lookout (kind_robots#3417)

A small flipper pair above the Ridge's gate, and the Lookout saucer up its
right side (each one this ball worth more, and each spots an S-K-Y lane).
The bot now plays every zone's flippers: it had never flipped the hidden
room's. Thirty games per skill level; in brackets, the t-022 Ridge without
these flippers.

| Skill | Ball time (s) | Score median | Mode | Multiball | Sub-table | Villages | Lookouts / min |
|---|---|---|---|---|---|---|---|
| average | 21.5 (18.8) | 441,550 (293,880) | 80% | 17% (10%) | 13% (10%) | 1.0 (0.9) | 1.05 |
| good | 43.6 (33.0) | 3,411,180 (1,074,440) | 100% | 47% (47%) | 27% (40%) | 2.2 (1.7) | 2.53 |

### What it says

- **Ball time** is up a third for the good bot and by 2.7 s for the average
  one. The Ridge flippers hold a ball up there long enough to play it.
- **Reach** is up for the average bot. The good bot's multiball is level, and
  it finds the hidden room less often (27% against 40%): its ball spends
  more time on the Ridge, away from the locks that open the door.
- **The Lookout** is made from both Ridge flippers. In a 90-timing cradle
  sweep, the left makes it at 3 timings and the right at 2, about what a
  main ramp gets.

### Next tuning steps, in order

1. The hidden room's reach for good players: one fewer lock to open the
   door on the first visit, or a Ridge feature that counts as a key.
2. Silas's play-test numbers (t-013) on the full table.

## 2026-10-10 — t-022: the Ridge (kind_robots#3415)

The table now runs on 0.42 m past the arch, onto the Ridge. The upper feed
(shot 3) used to be a subway to the award saucer, whose kickout fed the left
flipper. Now it lifts the ball up there, and the ball comes back into the
village through a one-way gate in the arch's crown, above the pops.

Thirty games per skill level, the same seeds, with main measured alongside
from its own worktree:

| Skill | Build | Ball time (s) | Score median | Mode | Multiball | Sub-table | Villages | Drains outlane/SDTM/centre |
|---|---|---|---|---|---|---|---|---|
| average | main | 17.7 | 182,440 | 77% | 20% | 17% | 0.9 | 5/2/93% |
| average | Ridge | 18.8 | 293,880 | 80% | 10% | 10% | 0.9 | 5/1/94% |
| good | main | 29.7 | 1,323,340 | 97% | 50% | 50% | 1.7 | 9/3/88% |
| good | Ridge | 33.0 | 1,074,440 | 100% | 47% | 40% | 1.7 | 12/3/85% |

### What the Ridge run says

- **Ball time** is up for both bots, by 1.1 s and 3.3 s. A trip up the Ridge
  takes 2 to 8 s and never drains.
- **Reach** is level for the good bot's multiball (47% against 50%). It is
  lower for the hidden room (40% against 50%), and for the average bot's
  multiball and room (3 and 3 games of 30, against 6 and 5). The cause: the
  upper feed's return is now the gate above the pops, not the controlled
  award-saucer kickout to the left flipper. The first ten-game run showed a
  much bigger drop; at thirty games most of it was noise.
- **Up there**, balls kicked in at 0.6 to 1.2 m/s make the S-K-Y lanes and
  the pops on every trip, and the cloud standups on some.

### Next tuning steps, in order

1. The Ridge's flippers (t-023): a flipper pair at the funnel's foot keeps
   the ball up there for shots of its own. Re-run these numbers after they
   land.
2. If the room's reach stays lower after t-023: send the gate's ball down a
   guided path to an inlane, rather than through the pops.

## 2026-10-08 — step 3: fifteen-second ball save, and where t-013 stands

Measured with kind_robots#3374 on top of steps 1–2.

**What changed:** the ball save after the plunge is 15 s, up from 10 s.

| Skill | Games | Ball time (s) | Score median (p10–p90) | Mode | Multiball | Sub-table | Wizard | Extra ball | Villages | Drains outlane/SDTM/center | Aim |
|---|---|---|---|---|---|---|---|---|---|---|---|
| novice | 10 | 11.5 | 105,380 (85,110–276,580) | 40% | 0% | 0% | 0% | 0% | 0.4 | 3/3/93% | – |
| average | 10 | 17.1 | 215,600 (102,460–3,482,720) | 90% | 20% | 10% | 0% | 0% | 1 | 5/2/94% | – |
| good | 10 | 29.8 | 4,941,390 (286,540–6,371,370) | 100% | 60% | 60% | 0% | 0% | 1.8 | 6/4/90% | 37% |

### Where t-013 stands against its targets

| Target | Now | Verdict |
|---|---|---|
| A decent player's ball lasts 60–120 s | good bot 29.8 s | **Not met by the bots.** Their saving is weaker than a person's (see step 2); a human figure is needed. |
| A new player reaches multiball within a few games | novice bot 0% | **Not met by the bot.** It rarely makes a lit lock at all. |
| A good player can reach the wizard mode | good bot 0% (1.8 of 6 villages a game) | **Not met by the bots.** It is gated on ball time. |
| Every main shot is makeable | 4 ramps and orbits made at 0.3–0.9 a minute by the good bot | **Met.** The bowed rubber fixed it. |
| The hidden room is found by skilled play | 60% of good games | **Met.** |

**What three tuning steps fixed:**
1. The flipper physics. The flat bat was the cause of the unmakeable shots.
2. A ball trap in the ramp channel.
3. The impossible skill shot.
4. The reach levers: the first multiball's locks, the village relight, the
   wizard's six villages and the ball save.

**What the bots can't settle:** the three ball-time-bound targets. Every
remaining number moves with ball time, and ball time is limited by how well
a bot saves the ball. Pushing rules further to make bots succeed (a centre
post, a ball save on every drain) would tune the table for the bots, not for
people.

**The next evidence is human play,** as t-016's judgement requires: a few
games on desktop and touch, against these rows. If those show the same
shortfalls, the levers are, in order:
1. a lit centre post as an earned save;
2. the award kickout's landing spot;
3. the mode timers.

## 2026-10-08 — step 2: rules levers for reach

Measured with kind_robots#3373 (steps 1 and 2).

**What changed:**
- **The game's first AMI multiball takes two locks;** later ones take three.
- **Orbits count toward relighting the village saucer,** as ramps do.
- **The Malaria-Free wizard mode lights at six villages,** half the map, not
  all twelve.

| Skill | Games | Ball time (s) | Score median (p10–p90) | Mode | Multiball | Sub-table | Wizard | Extra ball | Villages | Drains outlane/SDTM/center | Aim |
|---|---|---|---|---|---|---|---|---|---|---|---|
| novice | 10 | 11.1 | 95,100 (35,440–276,580) | 40% | 0% | 0% | 0% | 0% | 0.4 | 3/3/93% | – |
| average | 10 | 15.7 | 213,660 (102,460–964,000) | 80% | 20% | 10% | 0% | 0% | 0.9 | 4/4/93% | – |
| good | 10 | 26.2 | 917,070 (286,540–6,939,510) | 100% | 50% | 30% | 0% | 0% | 1.8 | 6/5/89% | 36% |

| Skill | Down-the-middle drains came last from |
|---|---|
| novice | plunge 37%, award 14%, sling-right-kicker 12%, drop-m 11%, sling-left-kicker 9% |
| average | plunge 29%, drop-m 20%, sling-right-kicker 16%, award 13%, sling-left-kicker 9% |
| good | award 31%, plunge 15%, drop-m 11%, sling-left-kicker 11%, sling-right-kicker 11% |

| Skill | Shots made per minute |
|---|---|
| novice | award 0.72, left-orbit 0.54, lock 0.18, right-orbit 0.36, right-ramp 0.9, spinner 2.35, upper-feed 1.63 |
| average | award 0.58, left-orbit 0.18, left-ramp 0.09, lock 0.45, right-orbit 0.09, right-ramp 0.27, secret 0.04, spinner 1.17, upper-feed 0.36 |
| good | award 3.72, left-orbit 0.72, left-ramp 0.86, lock 2.29, right-orbit 0.21, right-ramp 1.86, secret 0.29, spinner 5.08, upper-feed 1.86 |

| Feed | Flipper | Shots it can make (timing windows, of 90 ticks) |
|---|---|---|
| cradle | left | spinner 5, upper-feed 2, award 2, right-ramp 2, right-orbit 1 |
| cradle | right | award 11, spinner 5, upper-feed 3, left-ramp 2, lock 1, left-orbit 1 |
| inlane | left | spinner 4, upper-feed 1, right-orbit 1, award 1 |
| inlane | right | award 2, left-orbit 2, spinner 1, upper-feed 1 |

### What step 2 says

1. **Reach is up for the average and good players.**
   - Multiball: average 0% → 20%, good 30% → 50%.
   - The good player's villages per game: 1.4 → 1.8.
   - No bot reaches the wizard mode yet: six villages at 1.8 a game is still
     several games' work.
2. **Nothing moved for the novice.** It rarely makes a lit lock at all, and
   its balls last 11 s.
3. **Ball time is the lever everything waits on.** Every feature needs time
   on the table.

### How far to trust the ball times

The bots save less well than people do, so their absolute ball times
understate a human's. The harness stays sound for comparing one change
against another.

The evidence:
- When the good bot does flip, the ball goes back up the table 74% of the
  time and drains within three seconds only 9% of the time.
- Most drains come from balls it never flips at:
  - its deliberate misses;
  - dead-centre balls passing between the flipper tips;
  - balls it reads too late.

Silas's own play, the t-016 judgement, is the check on the absolute numbers.

### Next tuning steps, in order

1. Ball time, by the levers a player would feel:
   - a longer ball save after the plunge and a short save after an early
     drain;
   - the inlane hand-off;
   - the award saucer's kickout, which feeds 15–22% of centre drains.
2. Re-measure. Then take the remaining features (the mode timers and award
   values) against the targets.

## 2026-10-08 — step 1: bowed flipper rubber, channel roof, flipper skill shot

Measured with kind_robots#3373 on top of the harness (kind_robots#3372).

**What changed:**
- **The flipper's rubber is bowed (5 mm), not flat.** The old collider's
  sides were flat, so a carried ball left near the same angle wherever it
  was struck. That plateau made the ramps one- or two-tick shots. Now the
  strike point steers the ball: on a cradled shot from the right flipper,
  the exit angle sweeps smoothly from about +11° to −34°.
  - The bat's physics face stands above the ball, so a hard tip strike
    can't be pushed over it.
  - The post pass becomes a real timing skill (about 17 ms).
- **The channel between the left ramp and the upper feed has a clear roof.**
  The attract soak found a ball wedging there for good.
- **The skill shot is a lit flipper shot.** Every plunge rounds the left
  orbit to the left flipper, so the bumpers it used to ask for were never
  reached. Now the plunge lights the upper feed, the spinner or the right
  ramp.
- **The bot aims from a chart measured where its own ball rests.**
- **The harness records what each down-the-middle drain last touched.**

| Skill | Games | Ball time (s) | Score median (p10–p90) | Mode | Multiball | Sub-table | Wizard | Extra ball | Villages | Drains outlane/SDTM/center | Aim |
|---|---|---|---|---|---|---|---|---|---|---|---|
| novice | 10 | 11.1 | 95,100 (35,440–276,580) | 40% | 0% | 0% | 0% | 0% | 0.4 | 3/3/93% | – |
| average | 10 | 14.8 | 213,660 (102,460–471,980) | 90% | 0% | 0% | 0% | 0% | 0.9 | 4/2/94% | – |
| good | 10 | 30.3 | 480,860 (186,040–2,882,590) | 100% | 30% | 40% | 0% | 0% | 1.3 | 10/0/90% | 35% |

| Skill | Down-the-middle drains came last from |
|---|---|
| novice | plunge 37%, award 14%, sling-right-kicker 12%, drop-m 11%, sling-left-kicker 9% |
| average | plunge 35%, drop-m 17%, award 15%, sling-right-kicker 13%, sling-left-kicker 10% |
| good | award 22%, plunge 18%, sling-right-kicker 17%, spinner 13%, drop-m 8% |

| Skill | Shots made per minute |
|---|---|
| novice | award 0.72, left-orbit 0.54, lock 0.18, right-orbit 0.36, right-ramp 0.9, spinner 2.35, upper-feed 1.63 |
| average | award 0.68, left-orbit 0.14, left-ramp 0.05, lock 0.27, right-orbit 0.09, right-ramp 0.14, spinner 0.91, upper-feed 0.45 |
| good | award 3.7, left-orbit 0.86, left-ramp 0.66, lock 2.18, right-orbit 0.33, right-ramp 0.59, secret 0.46, spinner 5.95, upper-feed 1.45 |

| Feed | Flipper | Shots it can make (timing windows, of 90 ticks) |
|---|---|---|
| cradle | left | spinner 5, upper-feed 2, award 2, right-ramp 2, right-orbit 1 |
| cradle | right | award 11, spinner 5, upper-feed 3, left-ramp 2, lock 1, left-orbit 1 |
| inlane | left | spinner 4, upper-feed 1, right-orbit 1, award 1 |
| inlane | right | award 2, left-orbit 2, spinner 1, upper-feed 1 |

### What step 1 says

1. **The good player shoots much better.** Aimed shots hit 35% of the time,
   up from 0% when the charts didn't match real cradles.
   - Shots made rose from about 9 to 16 a minute.
   - Both cross ramps and both orbits are made.
   - The hidden room is found in 40% of good games.
   - The left ramp has a cradle window from the right flipper for the first
     time, and the right orbit one from the left flipper.
2. **Ball time has not moved,** and centre drains are still around 90%.
   What feeds them:
   - A novice's first descent from the plunge, down the left inlane onto the
     flipper, accounts for 35–37% of their centre drains.
   - Then the award saucer's kickout, the slings and the centre drop target.
3. **Multiball is still out of a newcomer's reach,** and nobody reaches the
   wizard.

### Next tuning steps, in order

1. The inlane hand-off and the award kickout: where they deliver the ball
   onto the flipper, so a ball arriving there can be controlled.
2. Rules levers for reach:
   - the first multiball's lock count;
   - ball save (and a save after an early drain);
   - the village relight cost;
   - the wizard requirement.

## 2026-10-08 — baseline (after t-012)

kind_robots main at kind_robots#3370 (t-007 rules, t-012 sub-table).

| Skill | Games | Ball time (s) | Score median (p10–p90) | Mode | Multiball | Sub-table | Wizard | Extra ball | Villages | Drains outlane/SDTM/center |
|---|---|---|---|---|---|---|---|---|---|---|
| novice | 10 | 9.6 | 53,160 (5,220–211,100) | 40% | 0% | 0% | 0% | 0% | 0.4 | 2/13/86% |
| average | 10 | 14.7 | 194,550 (43,830–1,519,390) | 70% | 10% | 0% | 0% | 0% | 0.7 | 3/14/83% |
| good | 10 | 31 | 3,933,230 (184,100–9,081,050) | 90% | 50% | 30% | 0% | 0% | 1.4 | 10/12/78% |

| Skill | Shots made per minute |
|---|---|
| novice | award 0.2, left-orbit 0.05, left-ramp 0.1, lock 0.05, right-ramp 0.05, spinner 0.61, upper-feed 0.2 |
| average | award 1.45, left-orbit 0.92, left-ramp 1.19, lock 1.05, right-ramp 0.26, spinner 2.77, upper-feed 0.66 |
| good | award 1.14, left-orbit 0.23, left-ramp 1.17, lock 1.44, right-orbit 0.07, right-ramp 0.4, secret 0.13, spinner 2.89, upper-feed 0.7 |

| Feed | Flipper | Shots it can make (timing windows, of 90 ticks) |
|---|---|---|
| cradle | left | award 4, spinner 3, right-ramp 2 |
| cradle | right | award 5, spinner 3, upper-feed 3 |
| inlane | left | spinner 2, upper-feed 1, award 1, right-orbit 1 |
| inlane | right | award 3, spinner 3, upper-feed 2, left-orbit 1 |

### What the baseline says

1. **Balls are far too short.** Even the good bot's ball lasts 31 s, against
   FX3's 60–120 s, and the novice's under 10 s. **Centre drains are the cause:**
   - centre drains make up 78–86% of all drains; on real machines it is a
     third to a half;
   - outlanes are only 2–10%, so the outlanes and kickback are not where balls
     are lost.
2. **The ramps and orbits are close to unmakeable on purpose.** The aiming chart
   gives each one a timing window of at most two ticks from either feed.
   - Nothing makes the left ramp from the cradle at all.
   - The physics can drive a ball at 3–6 m/s, so power isn't the limit. The
     exit angle is:
     - it stays within a few degrees of straight up while the ball crosses
       most of the flipper;
     - it only fans out (−13° to −38° on the right flipper) over the last
       few ticks before the tip.
   - Most well-struck balls therefore go up the middle into the A-M-I bank,
     the spinner and the award saucer, which is what the shot rates show.
   - The left ramp's mouth accepts a straight shot from the right flipper's
     tip only between −30° and −32° (plus a bank shot near −50°).
   - Since the shot lanes don't fall on the angles the flipper actually
     produces, the ramps are made mostly by accident.
3. **Multiball is out of a newcomer's reach.** The novice never reached it in
   ten games and the average bot reached it once. Locks need a lit lock (all
   of A-M-I down) three times over.
4. **The wizard mode is out of everyone's reach.** It needs all twelve villages,
   and the good bot sees 1.4 a game. A village needs the saucer when it is
   lit, then two ramps to relight it, and the ramps are the hard shots.
5. **The hidden room is found by good players only** (30% of good games), which
   is about right for a secret. Its rescued villages are a real route to the
   wizard once the main route is reachable.

### Next tuning steps, in order

1. Centre drains: the flipper geometry (rest angle, length, tip gap) and the
   inlane-guide hand-off, with the flipper sweep re-measured on the aiming
   chart after each change.
2. Shot geometry: turn the ramp and orbit mouths to the angles the flippers
   actually produce, until each main shot has a usable cradle window (3+ ticks)
   from its cross flipper.
3. Rules: the first multiball's lock count, ball save length, the village
   relight cost and the wizard requirement, measured against the targets above.
