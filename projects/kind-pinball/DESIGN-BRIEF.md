# Kind Pinball — Design Brief

date: 2026-10-07
status: v1 (written the day the project was split out of kr-arcade)
author: Claude session (Silas-directed)

## What it is

A pinball game for the Kind Robots Arcade that plays like a real Williams/Bally DMD-era machine. Today it
is one cabinet in the arcade: a single table with two flippers, three pop bumpers, one ramp, a saucer and
a four-mode ladder, all shipped in one day by the kr-arcade game factory (kind_robots #3275, #3280,
#3282). Silas, 2026-10-07: *"Pinball needs a significant style and quality improvement. As good as a rom
for a Williams machine. Lots of improvements, but a few style passes would do wonders. Different levels,
multiple ramps, a REAL quality game."*

It stays in the arcade as a cabinet, keeping the hall tile, attract mode and leaderboard. It now has its
own project because the work is bigger than a factory slice.

## The quality bar: what the reference machines do

These are models for **how a good table plays and feels**. We do not copy their names, characters, art,
sounds, callouts or layouts. The arcade's riff rule (projects/kr-arcade/games.yaml header) applies here
too.

| Reference | What we take from it |
|---|---|
| **The Addams Family** (Williams 1992, Pat Lawlor) | A **mansion grid** of 12 award rooms, lit one by one from a central scoop, that ends in a **wizard mode** once every room is lit. A **third flipper** high on the left. A **magnet** that grabs the ball and throws it. A **random-award scoop** (the Thing hand). Two ramps that feed the inlanes. Lots of callouts. |
| **Terminator 2** (Williams 1991, Steve Ritchie) | Fast, flowing **ramp-to-ramp combos**. A **skill shot** off the plunger. A **ball lock** that builds to a multiball, then **jackpot / super jackpot** shots lit by the ramps. A big **DMD** animation for every major event. Steady escalation that pulls the player along. |
| **Godzilla** (Stern 2021, Keith Elwin) | A deep **shot map**: two ramps, two orbits and a scoop, each shot lit by its own **arrow insert**. **Battle modes** that light a different set of shots each time. A **city meter** that fills over the game. Several multiballs that **stack** with modes. Layered wizard modes. |
| **Pinball FX3** tables | **Several tables** in one game. A **table guide** that teaches the rules. Toys that animate on the playfield. **Mastery** goals and challenges. Ball physics that feel heavy and true. |

## What "Williams quality" means here, concretely

1. **Feel.** The ball has weight. Flippers snap up and can **cradle** and **post-pass** the ball. Slings
   kick, pops are lively, and a **tilt bob** gives warnings before it tilts. Outlanes are fair: there is
   a **kickback** and a ball save. Nothing gets stuck.
2. **Shot map.** At least **two ramps and two orbits**, plus a scoop, drop targets and a spinner. Each
   shot is easy to see and has its own **arrow insert** that lights when it is worth something.
3. **Display.** An amber **dot-matrix display** (the DMD) shows the score, the ball number and mode
   timers. It plays a short animation for every big moment: skill shot, lock, multiball, jackpot, mode
   start and finish, wizard mode, extra ball, match and tilt.
4. **Lights.** A lit, art-directed playfield: **GI** lamps along the rails, **inserts** that blink to
   show what to shoot, **lamp shows** for big moments, and an attract-mode light show.
5. **Rules depth.** Skill shot, combos, lock and multiball with jackpots, a **mode ladder** that lights
   different shots, a **wizard mode**, an extra ball, a bonus count with a multiplier, and a **match**
   at game end. A new player can just flip, and a good player can plan.
6. **Sound.** Punchy effects for every toy, a music bed that changes in modes and multiball, and
   synthesized callouts. The arcade's sound kit can be extended for this.
7. **Levels.** An **upper playfield** reached by a ramp (a mini-table with its own flipper), plus
   **several tables** to choose from, each with its own theme, layout and rules.

## Tables (themes are original to Kind Robots)

- **Table 1 — AMI Village Rescue.** The current table, rebuilt. Against-Malaria theme: deliver nets to
  villages, AMI multiball. The mansion-grid idea becomes a **village map**: 12 awards lit from the
  scoop that lead to a **"Malaria-Free" wizard mode**.
- **Table 2 — proposed: Zuzu's Dojo.** Zuzu the koala ronin (comic canon at
  projects/comic-creator/issues/zuzu-koala-assassin-01/). Battle modes against the cast, Godzilla-style.
  It ties pinball to the zuzu-lair and zuzu-showdown work. **Lighter tone**, per Silas's 2026-10-07
  zuzu-showdown note: more Street Fighter than Mortal Kombat.
- **Table 3 — proposed: Robot Factory** (or the Cthulhuquarium deep sea). A T2-style lock-and-jackpot
  machine with a toy that builds a robot as you play.

## MVP (what ships first)

1. **Engine split and style pass 1.** Split the 1,300-line file into a shared engine (physics, a table
   definition, rules, rendering). The first style pass adds the DMD, lit inserts, metal rails and
   wireforms, playfield art, shadows and a better ball. Layout: a **second ramp and two orbits**.
2. **Rules pass for Table 1.** Skill shot, combos, lock and multiball with jackpots, the village map and
   its wizard mode, tilt, match.
3. **Style passes 2 and 3.** Lamp shows, GI, DMD animations, sound and music, a pre-generated
   playfield backdrop.
4. **Upper playfield, then Tables 2 and 3** with a table select.

## Out of scope / guardrails

- No reference IP: no names, characters, art, logos, sounds, callouts or exact layouts from Addams
  Family, Terminator, Godzilla or any FX3 table. Mechanics and polish standards only.
- No LLM at runtime. All art is pre-generated through ArtJobs, and generated art carries no lettering
  (text is drawn in the pixel font or on the DMD).
- Stays a free arcade cabinet. No paywall, ads or spending.
- Zuzu content follows the comic's guardrails (CAST-PICKS.md, VIDEO-GUARDRAILS.md, bannedTerms).

## Open questions for Silas (soft, t-002)

1. "Different levels": does that mean **several tables**, an **upper playfield** on one table, or
   both? (The plan assumes both.)
2. Are Table 2 and Table 3 (Zuzu's Dojo; Robot Factory or Cthulhuquarium) the right themes?
3. Should each table get **its own leaderboard**, or one pinball board?
