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
