# Kind Pinball — AMI Village Rescue: four-state visual direction

**2026-10-10 PT · exploratory visual direction, not human acceptance or production art.**

This complements `FX3-QUALITY-BLUEPRINT.md`, `SYSTEM-DESIGN-SPEC.md`, and milestone m6 in `roadmap.yaml`. Silas supplied a screenshot of the live 3D table and three *Zuzu: The Last Bell* render concepts, setting a substantially higher standard for Kind Pinball's density, modeled toys, lighting, ramps, and illustration. The Zuzu scenes are **quality references, not assets to re-theme or copy**.

## Visual baseline and non-negotiables

The physical/illustrative bar is `mockups/quality-bar-2026-10-10-overview.webp`, `mockups/quality-bar-2026-10-10-playfield.webp`, and `mockups/quality-bar-2026-10-10-cabinet.webp`. Earlier vector layouts (`01-fx3-table-hero.svg`, `02-shot-map.svg`, `03-responsive-shell.svg`) describe mechanics, **not the final rendering quality**.

A screenshot must look like a miniature **manufactured cabinet** containing a densely illustrated world. Wooden/metal enclosure; real bridges and hardware; reflective chrome rails and glass; curved transparent ramps **above** other objects; suspended props casting shadows; dozens of lighting points with actual sources; layered printed playfield art with depth and material response. A line/flat color pretending to be a ramp, a flat printed bumper and a pastel polygon standing in for a toy are explicit failures. FX3-class polish is the objective, not a claim that it has been reached.

This is **one** AMI Village Rescue table with a discoverable Ridge sub-table and **one** leaderboard. Do not add unrelated tables or import Zuzu's croc, bell, pagodas, architecture, or story. Keep the Kind Robots color DNA (cyan, pink, violet and rainbow) while anchoring it in warm amber lanterns, deep midnight-blue shadows and creamy wood/satin metal.

**Camera:** fixed flipper-facing perspective during main-table play. **No ball following, auto-reframe, view cycling, or per-shot chase camera.** When *all* balls transfer to The Ridge, one eased pan in; hold while playing; one eased pan out at return. At least two playable tiers (main and upper); more than a one-screen-flat playfield. Preserve the current physics and shot-to-sensor mapping until changed with replay tests.

## Visual study 1: The physical machine

**Purpose:** demonstrate the composition of a physically layered hero table.

- Backbox is a genuine illuminated object, with physical DMD and themed backglass.
- Center: sculpted AMI rescue automaton, articulated butterfly, operating net-delivery drone and readable illuminated village. Lighted hut windows are miniature box geometry, not dots painted onto the field.
- Left and right: *distinct* curving, elevated wireform/plastic ramp paths, each with metal supports and visible entry/return mouths. They visibly cross scenery and cast shadows. Keep two orbits and the lock/scoop shots distinct.
- Upper tier: its own two independently playable flippers plus readable mouths. Lower tier: two larger flippers, slings, in/outlanes and shooter return.
- Center-to-lower field: three differently illuminated bumpers styled as small actual lantern mechanisms; physical posts, drop targets, screws, rubbers, and transparent protective plastics.
- Shootable inserts must remain *clean and legible* above painted art, especially from the single flipper perspective.

This is **not** permission to replace deterministic table coordinates with approximate SVG art positions. Use this composition as a visual requirement while working with the verified `TableDef` geometry.

## Visual study 2: Rescue Storm multiball

**Purpose:** same physical machine, visibly transformed by a genuine rules state.

- Three balls in play; no duplicate render of one ball.
- GI temporarily dims, ramp addressable-light chases sequence around raised paths, flashers pick out characters/village, butterfly and drone animate in short rule-triggered bursts.
- Animated DMD reports RESCUE STORM, ball count and jackpot. Never paint a text banner across a live playable surface or obstruct the ball.
- Light changes are driven by rule effects (lock → start → jackpot → super jackpot → end), not unrelated permanent looping effects.
- Keep a low/mid/high-tier rendering plan with consistent *readability* for each, on laptop and mobile.

## Visual study 3: The Ridge

**Purpose:** justify a secret micro-table as its own authored environment, not the same playfield at another zoom.

- Night hilltop overlooking the village with its own richly painted backdrop, a small elevated metal/plastic playfield, two physical upper flippers and new local shots/target lamps.
- Dedicated gate and a **physically traced, timed transfer** into and out of the Ridge. Do not teleport a free-running ball.
- Hero landmark: AMI/winged rescue beacon over a ridge under moonlight, with lit cottages and warm windows; not the Zuzu haunted bell setting.
- Transition in one eased camera move and out in one, only while the ball(s) are safely transferred. Camera is otherwise perfectly steady.
- Entry is secret and earned; its mode/rewards return to the same main table and leaderboard.

## Visual study 4: immersive Arcade shell

**Purpose:** solve the empty surrounding canvas and crowded retro-controls bar shown in the current screenshot.

- Desktop/tablet: cabinet fills an intentionally lit immersive room/background, not a tiny pinball column adrift in black. Viewport emphasizes the table; score, mode, guide and play/fullscreen controls form compact, optional adjacent interface.
- The live playfield must dominate on desktop; an overwide side panel must *not* shrink the physical machine to a phone-width column. Side UI may overlay or retract during play. Do not hardcode the exploratory sketch's relative widths.
- Phone/touch: canvas gets priority; scores, actionable guide and accessible controls are available without occluding ball, slings or flippers. Respect safe areas.
- No sudden camera/focus move when multiball starts or when the player operates flippers. Fullscreen must preserve aspect ratio and input.

## Production art separation

| Source | Deliverable | What the runtime must do |
| --- | --- | --- |
| ArtJob A | Main-field printed playfield illustration, orthographic and precise, high resolution | Register UVs/landmarks, preserve mouth and insert clearance; albedo texture and masks only |
| ArtJob B | Ridge illustrated playfield and hilltop backdrop | Separate mapped region; transition and collider alignment |
| ArtJob C | Backglass, apron, cabinet side-panel illustration | Clear theme and emotional hook around existing backbox/DMD, never text baked into generated art |
| 3D scene work | AMI robot head, butterfly, villages, drone, windmill, lantern bumpers, posts | Physical mesh depth, PBR, lighting and articulation, stable collider integration |
| 3D scene work | Both wireform ramps, clear plastics, inserts and metalwork | Meshes, rails, supports and shadows that match actual simulated ball tracks |
| Runtime | GI, flashers, inserts, animations, DMD and sound | Rule-synchronized show states, perf tiers, accessibility |

### ArtJob prompt: main-field printed illustration

> Vertical **orthographic top-down texture sheet** for a premium original pinball playfield called AMI Village Rescue. Magical miniature village at night, tiny colorful lit windows, cobbled paths, deep indigo-violet sky, radiant rainbow arcs, rescue-beacon motifs, butterflies, warm lanterns and a winding charity/rescue narrative. Richly layered painterly scenic illustration with finely controlled texture and high-frequency detail, jewel-tone turquoise, pink and electric blue balanced against warm bronze and candlelight. Built for a physical lacquered pinball playfield: **no perspective cabinet, no 3D rails, no flippers, no letters, no logos, no ramps painted into the floor, no UI**. Keep large clean, calm negative-space shot lanes, landmark/mask zones and bright inserts unobstructed. Original Kind Robots world. Portrait aspect ratio; output at highest supported resolution for supervised UV alignment.

### ArtJob prompt: Ridge

> Vertical orthographic pinball playfield art for the secret upper world, The Ridge: moonlit hilltop above AMI's village, glowing cottages, rescue beacon, mountainous distance, butterflies and night sky, warm silver-blue and amber light. Painted lacquered illustration intended to lie **beneath** separate real sculptural mini-playfield flippers, metalwork, target mechanisms and clear ramps. Complex storytelling in scenery but quiet sightlines near critical ball paths. **No rendered cabinet, no text, no fake flippers, no fake bumpers, no UI**. Coordinate landmarks with the existing Ridge UV/collider map before finalizing crop.

### ArtJob prompt: backglass and cabinet

> Premium physical pinball-machine backglass and cabinet-art illustration for AMI Village Rescue, original optimistic retro-fantasy: charismatic helpful robot with bright butterfly companion soaring above a lamp-lit village under a cosmic pastel rainbow, dramatic theatre lighting and layered clouds. Strong illustrative focal points, fine panel-art detail and vibrant cyan/pink/gold accents over midnight indigo. Leave a reserved blank rectangular area for an actual animated 128×32 dot matrix display. Separate variants for backglass, side decals and apron; **no lettering, no scores, no interface, no branded marks**.

### ArtJob prompt: room/attract background

> Ambient illustrated environment wrapping a playable pinball cabinet: immersive magical twilight arcade, star-filled sky, distant miniature village rooftops, rainbow glow, practical warm lanterns, textured workshop surfaces, cyan and pink accents, soft spatial depth. Composition leaves high-contrast negative space **directly behind the moving ball and flippers**. Designed as behind-the-table scenery, never as a layer covering a live rendered table, balls, or controls. No text.

**Job submission:** submit these through the existing durable Kind Robots ArtJob pipeline if available; record each ArtJob ID and actual generated file URL in the task note. Never claim a prompt is generated art or that a queued ArtJob completed. No paid generation without permission.

## Tasks and visual acceptance

These are **acceptance details for existing work**, not new parallel implementation tasks:

- `t-026`: fixed flipper-facing camera and two deterministic Ridge transfers.
- `t-027`: ArtJobs A/B and verified UV/collider/insert sightlines.
- `t-028`: physically sculpted, lit scenery and toys, modeled at depth.
- `t-029`: elevated mesh ramp/rings with chrome wireforms, supports and transparent parts.
- `t-030`: physical warm GI, light-show timing, lacquered cabinets and finished themed Arcade presentation.

**Review matrix:** at least nine screenshots: standard hero table, Ridge and multiball, each at phone, laptop and ultrawide/desktop; compare directly with the three quality-bar WebPs. Also capture an image *mid-ramp* and a shot *under a crossing wireform* showing true occlusion, reflections and vertical separation. Verify flipper-ball visibility, DMD readability, no frame chase, no glass/texture Z-fighting, clear inserts, and actual physics replay and game tests. A finished task count does not replace Silas's hands-on FX3-quality verdict (`t-016`).

## Artistic guardrails

1. Keep the optimism and charity/rescue theme of Kind Robots; don't copy Zuzu's haunted weird-west look.
2. Generated illustration must not pre-bake physical parts (a screenshot of a fake ramp still leaves a fake ramp).
3. Richness comes from authored material response, scenic layers and interactive mechanisms. Extra circles and glows are not a substitute.
4. The reference Zuzu images set the *finish level*, not a permissive shortcut of copying their assets.
5. This document and the exploratory visual studies are **unapproved options**, not a new Silas-approved direction superseding his 2026-10-10 camera/quality instructions.
