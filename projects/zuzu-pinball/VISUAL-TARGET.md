# The Last Bell: locked visual target from the October 10, 2026 mockup review

Status: **direction accepted by Silas**, not a claim that table art, mechanism layout or physics are finished.

Silas reviewed three generated, detailed pinball concepts and said: **"wonderful, ok, those should be a guide for the goal layout. now keep going and lets make that a reality!"**

The images were generated in the conversation and are **not yet delivered as verified production assets in GitHub**. Agents should reconstruct their compositional requirements from this source-backed reference and the existing version-controlled SVGs rather than imagining the pictures were already shipped. This document is the durable visual-to-engineering translation of that acceptance.

## The three reference views (complementary, not three competing tables)

1. **Three-quarter cabinet beauty view:** An authentic premium pinball cabinet with Zuzu, the grey koala Edo ronin, in a weathered straw kasa on the moonlit abbey backglass. Copper rails, brass corner guards, wood/lacquer cabinet art, a glowing giant Abbey bell behind a real raised playable deck, lantern houses on the perimeter, and River Croc half-submerged left. Strong amber/cyan contrast with oxblood-black printed playfield.
2. **Top-down layout view:** Use this as the geometry-first target. Two lower flippers are unobstructed, slingshots and inlanes are legible, outer orbit lanes route to returns, a three-bumper grouping sits near the centre, multiple elevated ramps visibly have entrances and destinations, and **River Croc's mouth is a deliberate shootable cross-table target** on the left bank, with a glinting steel ball visible in the throat.
3. **Multi-view detail sheet:** A full table, a close-up of Croc's tooth-lined catch and ball feed, a close-up of the Abbey bell and **two upper flippers**, and a second cabinet angle. This view establishes that signature mechanisms must be readable and physically credible at close range, not flat paintings or video-only tricks.

Canonical vector companions already tracked here: [cabinet concept](CONCEPT-ART.svg), [playfield shot map](PLAYFIELD-MOCKUP.svg), [gameplay framing](GAMEPLAY-SCREEN-MOCKUP.svg), and [River Croc mechanical closeup](RIVER-CROC-TOY-CONCEPT.svg). The newer generated references raise the art fidelity bar above these diagrams, but the diagrams are the committed technical baseline.

## Layout to model (normalized plan, not tested metre coordinates)

`x` is left-to-right from 0..1. `v` is top-of-table-to-player, 0..1. These are **design zones**, not collider positions. Convert to dimensioned metres and make collision-path tests pass before freezing each shot.

| Zone (x, v) | Feature | Required player path |
| --- | --- | --- |
| (0.50, 0.12–0.30) | **Abbey/bell upper deck** | Raised floor and **two independently controllable upper flippers**. Ball must travel there via central Bell spiral and be returned down safely. The bell itself is a visible mechanical target. |
| (0.13, 0.19–0.63) | Left perimeter orbit / copper ramp | Left flipper feeds orbit; distinct elevated copper Village switchback with a ball-width trough and **right inlane return**. |
| (0.84, 0.20–0.70) | Right perimeter orbit / Abbey ramp | Right flank has separate orbit and swooping elevated Abbey rail with **left inlane return**, not just a drawn sweep. |
| (0.52, 0.44–0.57) | Bumper courtyard | Three accessible pop bumpers, strong metallic inserts, visible open ball passages between structures. |
| (0.22, 0.49–0.68) | **River Croc watering hole** | Cross-table flipper shot into a realistic gaping jaw with a real one-ball capture sensor, 0.8s hold, animated Death Roll and controlled **right inlane spit**. The feeder is clear of overlapping ramp supports. |
| (0.47, 0.63–0.74) | Crypt / story seal | Mystery entry, lit progression insert and future hidden subtable portal. The trapdoor must not take an unearned ball. |
| (0.20–0.80, 0.76–0.93) | Player-controlled lower field | Open cradling, catch/pass room; meaningful fair slings/inlanes/outlanes; **two primary flippers**. Avoid a dense diorama here. |
| (0.93, 0.64–0.98) | Plunger and right shooter lane | Clearly separate, gated, collision-proof ball serve. |

The centre spiral and two perimeter ramps are **three distinct elevated ramp assemblies**. The two outer orbits are independent loop shots even where they run beneath raised rails. All five must support actual entrance sensors, trajectory tests and valid ball returns.

## Art must support actual play

- **Never cover a meaningful ball shot with a hut, torii, foliage, plastic, crocodile jaw mesh or overlay.** Extruded decorative assets must stay behind the ball or transparently fade when camera occlusion demands.
- Ensure the ball stays visible through the Croc's open jaws. Jaw closing should not destroy, clone or teleport a ball; capture/eject lives in the engine's ball ledger.
- Silas wants **FX3-grade finish**, not an attractive poster. Generate original world textures, sculpted signature toys, playfield decals, coherent GI, cabinet art, camera transitions and responsive sound independently of the mechanic tests.
- Amber village lanterns, red ritual flashes, cyan/waterline Croc cues, violet ancient-world discovery, white ball-save cues. Addressable cabinet splash/LED borders follow mode states, but active shot arrows stay legible during the brightest light show.
- Staged art pipeline: render clean **unpeopled** top-down playfield albedo, separate backglass with Zuzu, Croc head/jaw animation frames or 3D rig, Abbey bell + raised platform, then cabinet side and bezel art. Record ArtJob IDs and verify final URLs; queued is not delivered.
- The target should look good in **an overhead play view**, **three-quarter cabinet view**, and on a **portrait phone**. On phones favour a higher, less occlusive view and reduced sparkle. Never shrink the ball until it is hard to track.
- Retain Zuzu canon: the crocodile is the existing huge scarred River Croc, the Abbess is the later threat, and Zuzu is an Edo outsider in a haunted weird-west world. Do not steal existing machines' decals or copyrighted playfields.

## Implement and measure

- Stage A: distinct `zuzu-pinball` WebGL entry and **private** `/admin/zuzu-pinball` scene with an honest graybox.
- Stage B: dimensioned floor, fair flippers, simulated ball path and plunger; place Croc approach and safe scoop. Measure shooter success and drop-catch.
- Stage C: three real ramps, two valid orbits and the raised two-flipper Abbey deck. Record ball trajectories; flag ramps whose entry is blocked or exit unfair.
- Stage D: Croc jaw rig and Watering Hole jackpot; complete lock and multiball ball ledger; rig a crypt that returns to the main table.
- Stage E: art atlas, lighting, audio, game-grade visual comparison, 60fps target and mobile/input QA.
- Final acceptance remains **Silas's hands-on FX3-equivalent quality verdict**, not "all boxes checked" or "art looks close".

## Tests must disprove bad shortcuts

Automate shot reachability from lower-flipper positions, corridor clearance against a real 27mm ball, all ramp entrances/exits, croc capture/eject including multi-ball and tilt, stuck ball recovery, finite rules progression, render lifecycle, and visual screenshot comparison at multiple sizes. The visual target is a design contract, never a waiver for physical validation.
