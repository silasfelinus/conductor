# Kind Pinball — tuning evidence (t-013)

Silas's finish line for AMI Village Rescue is "truly fun, complex, and quality,
as good as any Pinball FX3 table". This file holds the numbers behind that
judgement, so tuning rests on evidence rather than feel. Every rules or geometry
change reruns the harness and adds a dated section here; the newest section is
the table's current state.

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
