# zuzu-pinball — task history archive

Full `note:` prose for completed zuzu-pinball tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-003 — Register isolated Zuzu Arcade cabinet, admin preview and discoverable admin nav

<!-- note:begin t-003 -->
Reuse the existing Arcade webgl engine and shell; create separate game id zuzu-pinball, game-specific state, assets, score namespace and lazy loader. Initial playable surface must live under /admin/zuzu-pinball, with a content/channels/admin tab requiredRole ADMIN. Keep /play unpublished until explicitly authorized. Audit sibling game registration and tests.

Scoped admin WebGL prototype implementation and verification test are on worker/zuzu-pinball-t003-admin-webgl-20261010-v5j8 in kind_robots. Separate game id and TableDef; preview inaccessible from public Arcade and score submissions disabled. Full geometry, modes and Croc sculpt belong to the dependent future tasks. CI and PR review are pending.

Merged kind_robots PR #3428 to main at a027022b51e71aab843908887aafdca1945bf054. Private /admin/zuzu-pinball with requiredRole ADMIN and discoverable Admin tab; distinct WebGL/Rapier table and River Croc scoop, new score namespace isolated from public Arcade scores, plus dedicated regression coverage. Reconciled newer main changes without force pushing; 33 check runs successful when merged. Production container image publication and Alexandria deployment are separate from merge; public /play launch remains gated under t-014. Next work t-004 must calibrate full physical geometry and shot paths; this is a starter greybox, not the final FX3-quality table.
<!-- note:end t-003 -->

## t-004 — Implement dimensioned Zuzu physical graybox, shooter lane and lower flippers

<!-- note:begin t-004 -->
Calibrate units, slope, gravity, ball radius, restitution, rubber materials, flipper torque, cradle and catch control, shooter-lane gate, one-way trough and ball serve. Unit/integration tests for all ball transitions. The SVG mockup is a design guide, not a tested geometry mesh.

Kind Robots physical starter graybox adds a one-way shooter gate and a real plunger trough stop, calibrates rest position to the 27 mm ball, and adds direct Rapier integration tests for held plunger, two launch powers feeding the main field, independently moving lower bats, and River Croc conservation. Changes are on worker/zuzu-pinball-t004-physical-lanes-20261010-q7k9. CI tests are pending; only merge verified trajectories and preserve public Arcade isolation. Art and elevated ramps remain subsequent roadmap tasks.

Reconciled completed physical graybox: Kind Robots PR #3468 merged at b0e204924613129cdd0c36367820c562659113e2. Physics trajectory, trough, flipper, and Croc regression test contracts landed with successful TypeScript and Contract Tests workflow checks. This clears t-005's dependency. Production deploy status unverified.
<!-- note:end t-004 -->

## t-005 — Build three physically distinct elevated ramps, two orbits and shot sensors

<!-- note:begin t-005 -->
Fabricate Village left switchback returning right, Abbey right crossover returning left, and central Bell spiral rising to the Abbey. Add orbit returns, safe sensors, ball collision sweeps and target animations. Prove each shot with captured trajectory and repeatable test scenario.

Prepared a dimensioned mechanical pass in kind_robots branch worker/zuzu-pinball-t005-elevated-shots-20261010-f81d: three genuine mesh floor/rail/roof ramps with independent paths, two physically guided orbit returns, shot switch chains and dedicated Rapier rolling/ball-conservation/shot-order regression tests. Typecheck, CI and target-preview validation remain pending.

2026-10-10 PT: Merged the first genuine 3D ramp engineering slice to kind_robots main in PR #3475 at 9366670948f6b05a9440a991f37fd967279ce968. Three physically distinct raised Rapier mesh ramp floor/rail/cover paths, two outer orbit return guides, ramp entry/crest/return sensor chains, Croc approach and crossover clearance tests, and seeded 24-tick ball conservation/shot-order checks are committed. 29/29 PR checks completed successful, including TypeScript, all contract tests, Prettier and production-image build. Follow-up required before marking t-005 done: demonstrate actual flipper-origin trajectories that enter, crest and exit EACH ramp at calibrated shot speeds, capture trajectory evidence, verify safe returns and no stuck balls in repeatable physics replay, then tune any competing Croc shot geometry. Admin preview only. Self-hosted Alexandria runtime deployment not verified; public release still gated.

2026-10-11 PT: Measured on real Rapier physics, the table made 0 of 9 shots from either
flipper: the inlane guides sloped the wrong way and balls drained past the flippers.
Kind Robots PR #3509 rebuilds the lower field (inlanes, outlanes, slings with caps, tip
gap wider than the ball), moves the Abbey seals into an in-line bank between the Village
and Bell mouths, gives the River Croc its own mouth beside a one-ball left orbit with
its spit landing on the right inlane, and fixes a shared ramp-cover pinch that held
balls on the Bell spiral. New test:zuzu-pinball-shots proves every shot from a measured
flip, checks that the ramps return to their inlanes and the Croc spit reaches the right
flipper, and runs bot games with no stranded ball. 50-game soak: 0 stuck balls. Coverage
is now 9/9.

Merged kind_robots PR #3509 to main at 30b29bbb59551f5155a33eb07ee10853afd5a40f with all
33 checks green, including the new test:zuzu-pinball-shots. This clears t-006 and t-008.
Production container deploy not verified (manual Unraid Force Update).
<!-- note:end t-005 -->

## t-006 — Build raised Abbey upper deck with two independent flippers

<!-- note:begin t-006 -->
A visible, physically elevated mini-playfield and upper left/right player controls (plus mirrored accessibility mode); ramp entry, deck targets, protected exits, and controlled ball returns to lower playfield.
Merged kind_robots#3557 (squash 64cf7bd): clear raised Abbey deck at the Bell spiral's end (fixes made spirals leaving the cabinet), upper flipper tier (mirrored by default, alone while B/Shift is held), three hollow-bell standups (toll opens the Mortuary), protected exit subway to the right inlane; verifier proves deck landing, each bell, nothing stranded or fallen.
<!-- note:end t-006 -->

## t-007 — Implement sling, pop bumper, drop bank, scoop, captive ball and tilt

<!-- note:begin t-007 -->
Three pops, four resetting drops, capture-and-eject scoop, trapped relic ball, calibrated slings, ball save and kickback. Implement nudge with warnings, bob threshold, temporary disables, tilt termination, and repeatable no-ball-trap/physics regression tests. Expose capture, switch debouncing and ball ledger hooks for River Croc (t-015).

Partial mechanical hardware implementation in Kind Robots PR #3480: a four-target Abbey seal drop bank, physical spinner, left-outlane kickback coil and targeted Rapier lifecycle test. Reconciled with the separately merged three-ramp layout without overwriting it. CI is pending. After merging, return t-007 to ready (not done): rules-driven reset, captive relic ball, Zuzu tilt and kickback arming, and performance/ trajectory QA remain required before dependent River Croc task t-015.

Completed a bounded hardware slice: Kind Robots PR #3480 merged as 7318576f39df4108f1a054b3faf923c0ec94e2d4, with four physical Abbey seal drops, a relic spinner, left-outlane kickback and passing Rapier lifecycle hardware tests. Preserved t-005's previously merged ramps. Formatting-only follow-up PR #3482 removes a one-time CI diagnostic and applies the exact Prettier output; merge-when-green is enabled. Re-arm this one-off task as ready, not done. Remaining work includes Zuzu-specific automatic bank reset, physically captive relic ball, tilt logic and warning rules, coil arming/ball save, robust geometry and multiball conservation tests. Do not unblock River Croc t-015 yet.

2026-10-11 PT: Kind Robots PR #3513 finishes the remainder. The engine gains captive
balls: a real Rapier ball in a lane of its own that never drains or counts. Zuzu's relic
sits in line behind the Abbey seals; with the seals down each strike raises the bonus
multiplier, and three strikes wake the crypt (the key for t-010). Fixes a trap where an
immediate seal reset could raise a drop target under a ball: seals now stay down until
the next ball. Tilt warnings and termination, kickback arming and ball save landed with
the t-008 rules (PR #3511). Hardware test: 20 relic strikes stay in the lane. 50-game
bot soak: 0 stuck balls.

Merged kind_robots PR #3513 at 5a47ecea29469fe63d8511b0df1c792a4c75f69b with all 31
checks green. Unblocks t-009 (multiball) and t-015 (River Croc jaw rig). Production
deploy not verified (manual Unraid Force Update).
<!-- note:end t-007 -->

## t-008 — Implement mode director, five story chapters, shot awards and DMD contracts

<!-- note:begin t-008 -->
Mode-state engine with Homestead, Storm Crow, Abbey, Children's Names and Last Bell. Lamp and DMD bindings, ball-to-ball chapter retention, skill shots, combo ladder, multiplier, extra ball, match and game over. Narrative readability never blocks the player from flipping.
2026-10-11 PT: Kind Robots PR #3511 gives the Zuzu table its own ruleset; until now it ran AMI Village Rescue's rules. The runtime now takes a PinballRuleset, with AMI's as the default and its reducer unchanged. The Mortuary tells five chapters in order: Homestead in Ash, Storm Crow Canyon, Abbey of Hollow Bells, The Children's Names and The Last Bell. Each is timed, and finishing it breaks one of five seals. Chapter progress is kept across balls, and after the Last Bell the story starts again at double value. The bell lane or all four Abbey seals reopen the Mortuary, and the seals also raise the bonus multiplier and relight the kickback. The Croc always pays, and his fifth swallow lights an extra ball. Also included: soft-plunge Mortuary skill shot, combos, ball save, bonus, tilt, match and game over, plus seal-track, multiplier and shoot-again lamps. New test:zuzu-pinball-rules covers every rule and plays bot games to game over.
Merged kind_robots PR #3511 at 6be257193188bc201c33a6fbaed63cabadcb3569 with all 33 checks green, including test:zuzu-pinball-rules. Production deploy not verified (manual Unraid Force Update).
<!-- note:end t-008 -->

## t-009 — Add physical lock and 3/4/6 ball multiballs with jackpots

<!-- note:begin t-009 -->
Real ball trough/serve count and Citadel lock, virtual lock fallback, Harvest Moon 3-ball, Storm Crow 4-ball, Last Bell 6-ball, bonus and super-jackpot escalation. Soak test multi-contact collisions and cleanup.
kind_robots#3553: Citadel physical lock at the bell-lane head (shelf slots, subway kickout to the left inlane), 6-ball ledger with self-healing virtual fallback, Harvest Moon 3-ball (staggered ramp jackpots, orbit-combo super), Storm Crow 4-ball (seals + both orbits, per-lane 3-rung ladders, bell-lane super), The Last Bell 6-ball wizard on the fifth seal (releases locks; six jackpots light the Bell spiral super), escalating supers, 10 s multiball ball save; soaks check the ledger every physics step.
Merged kind_robots#3553 (squash 9adece3): all three multiballs in one PR.
<!-- note:end t-009 -->

## t-010 — Build and balance unlockable hidden undercrypt mini-table

<!-- note:begin t-010 -->
Crypt trapdoor and isolated 3D mini-table with two mini flippers, skill targets and a valid mechanical kicker back to primary playfield. Prevent multiball leaks and unfair drains when transitioning scenes.
Merged kind_robots#3566 (squash 00e67b2): undercrypt behind the backbox (zone sub-table, camera, fading backbox), lit every third relic strike, entered by Mortuary subway only with one ball and no chapter/multiball, crypt flippers, three skull standups, HOME saucer, drain subway back to the Mortuary kicker. Also raised the contract-tests job timeout to 15 min (it was cancelled at 10 min after finishing every step).
<!-- note:end t-010 -->

## t-011 — Build production art assets, 3D cabinet, ramps, ball, plastics and themed toys

<!-- note:begin t-011 -->
Concept-art.svg is NOT final shipped 3D art. Use verified generated art jobs or original authored assets: Zuzu backglass and cabinet sides, moonlit village decals, 3D monastery, physical bell, figures, props, glass/chrome reflections and raised mechanical ramp model. Include the canonical scarred, giant River Croc as a rigged waterline jaw toy. Log prompts, seeds, sources, rights, destinations and asset state.
2026-10-11 PT (Silas: queue the final table art and the croc animation overnight): queued 11 krea2 ArtJob requests in projects/art-prompts.yaml (project zuzu-pinball, priority 110): the painted playfield (1024x2000), backglass (1536x640), raised Abbey deck (1280x1024), undercrypt (1024x1280), cabinet side (2048x1024), and six River Croc animation keyframes on seed 731731 (submerged, rising, mouth-open, captured, death-roll, spit), all to kind_robots public/images/pinball/zuzu-*.webp. Next: once delivered, verify each URL, then wire the playfield and backglass into ZUZU_LAST_BELL_GREYBOX.art (playfield region over the table rectangle, room.backglass) and hand the Croc frames to t-015's jaw rig. Queued is not delivered.
2026-10-11 PT art review. All 11 first renders are delivered and served (ArtJobs 36943-36953). Use: playfield, backglass, Abbey deck and undercrypt are good. The cabinet side came back framed as a cabinet photo with white surround and needs a crop. River Croc frames for the t-015 jaw rig: 1 submerged, 2 rising, 3 mouth open v2 (zuzu-river- croc-3-mouth-open-v2.webp, ArtJob 36954, jaws gaping, the one to use), 4 jaws clamped v2 (36955; closed jaws without a visible ball, usable because the renderer draws the real ball; a v3 asking for the ball is queued), 5 Death Roll (strong), 6 spit. The originals 3 and 4 came back closed-mouthed, because the shared seed pinned the pose; ignore them.
2026-10-11 PT: kind_robots PR #3531 merged at 7a2517a with all 31 checks green. The painted playfield is now the table's art.playfield over the whole table rectangle, and the backglass is room.backglass (Ghost Trail title as fallback). The admin banner shows the backglass. Rendered in headless Chromium at desktop and phone sizes; the art lines up under the mechanisms. The Abbey deck art goes to t-006 and the undercrypt art to t-010. The cabinet side render needs a crop, and there is no side-art slot in the renderer yet.
<!-- note:end t-011 -->

## t-012 — Addressable LED rail and bezel splash shows, sound, DMD animations, camera

<!-- note:begin t-012 -->
LED strip and insert light-map editor, GI, restrained strobes, mode cues, cabinet border art, animated high-score and callout scenes, layered sound mixing and camera sweeps that never impair flipper response. Provide static camera and reduced-motion settings. Add Croc mouth arming/capture/death-roll/spit cues, DMD and multiball callouts.
2026-10-12 PT: landed in three merged kind_robots PRs. #3568 (squash d54dd2d): 96-LED addressable rail round the cabinet, each mode in the brief's colour (amber Harvest, cyan Storm with restrained white lightning, gold Last Bell with a red comet, violet crypt, teal Watering Hole, a colour per chapter), ball-save ends, River Croc cues on his own LEDs (open glow, capture flare, alternating red death roll, white spit, rising), tilt dark, every flash at most 3 Hz, reduced motion holds still; engine TableDef.ledRail + ruleset.leds, one instanced draw call. #3570 (squash 69266fc): per-table DMD attract pages (Zuzu had been showing KIND PINBALL): ZUZU type-on, THE LAST BELL, a Croc jaws picture page, high score counting up; NEW HIGH SCORE game over; music bus ducks to 35% under every callout. #3573 (squash 4b53191): camera sweeps (shooter lane while the ball waits, pulled back in multiball), each framing the whole playfield so the flippers never leave the screen, debounced 45 ticks; a cabinet Camera moves/still switch, saved, defaulting to still under prefers-reduced-motion, cutting instead of panning; a test proves physics identical tick for tick either way. Not done here and moved to t-017: the insert light-map editor and cabinet border art.
<!-- note:end t-012 -->

## t-015 — Build River Croc waterline mouth capture, jaw rig and safe spit

<!-- note:begin t-015 -->
Explicit Silas requirement 2026-10-09: actual River Croc, a giant scarred watering-hole predator from the existing Zuzu gamebook and Showdown. The steel ball must be shootable into the open jaws at #07 (left-side Mortuary scoop replaced; right-hand story selector scoop remains). Build colliders, hit sensor, readable waterline aim cue, mechanical jaw, one-ball capture and deterministic Submerge/Rise/Open/Swallow/Death Roll/ Spit/Reset sequence. Spit to right inlane; ball ledger conservation, busy-mouth reject, timeout eject, safe tilt, multiball stress and unobstructed ramp clearance verified with repeatable trajectory tests.
2026-10-11 PT: kind_robots PR #3535 adds the River Croc's jaw gate (door croc-jaw, starts open, shuts on capture) and his cycle: open, captured, Death Roll, spit, submerged, rising, open. It also adds the sculpted animatronic toy (engine animatronics plus render/croc.ts) and the lamp aim cue. test:zuzu-pinball-croc covers busy-mouth reject, two-ball conservation and 200 rounds; 1,000 rounds passed locally with no drain during a hold.
Merged kind_robots#3535 (squash fbca13a): jaw gate, timed cycle, sculpted toy; a follow- up commit in the same PR fixed the jaws staying shut after a mid-chapter swallow (quiet ticks dropped the open effect).
<!-- note:end t-015 -->

## t-016 — Author River Croc Watering Hole mini-mode and Death Roll jackpot

<!-- note:begin t-016 -->
Add a Watering Hole mini-mode in Homestead chapter using River Croc's existing Zuzu canon, including coyote encounter reference; qualifying orbit-to-mouth combo awards Death Roll jackpot, unlit successful mouth shot earns spit-back consolation award. Waterline LEDs, DMD mouth closeup, water-spray and jaw-snap sound, accessible reduced-motion cues and trajectory-skill progression. Do not make the mouth an instant drain; every legitimate swallow safely ejects and awards something.
kind_robots#3545: Watering Hole opens on a Homestead swallow (30 s, gamebook coyote canon); orbit lights the mouth for the Death Roll (1M +500k each, window 6/5/4/3.5 s); unlit swallow pays spit-back; waterline LEDs, death-roll DMD close-up, jaw-snap/water- spray cues, reduced-motion toy; physics soak spits every swallow back.
Merged kind_robots#3545 (Silas added a one-line lint fix to the verifier before merging).
<!-- note:end t-016 -->

## t-017 — Insert light-map editor and cabinet border art

<!-- note:begin t-017 -->
The two t-012 brief items that did not land with the LED rail, DMD and camera work (kind_robots#3568, #3570, #3573). An insert light-map editor: a private tool to place and preview the table's inserts and flashers (and the LED rail's path) over the painted playfield, writing the positions back as table data, so art and lamp positions can be lined up by eye instead of by hand-edited coordinates. Cabinet border art: the side rails, apron and backbox trim art for the Last Bell cabinet, requested through the art queue, then drawn by the renderer's room and cabinet (render/room.ts), which has no side-art slot yet.
2026-10-12 PT: both halves merged. kind_robots#3583 (squash 28e10fa): the insert light- map editor on /admin/zuzu-pinball (admin only), the painted playfield with all 29 inserts, both flashers and the 96-LED rail as SVG; drag or arrow-nudge (1 mm, 5 with Shift) an insert and copy the moves back as table data; pure model in utils/arcade/pinball/lightMap.ts, verifier test:zuzu-pinball-light-map. kind_robots#3584 (squash 1d85d32): cabinet side art, a new art.room.cabinetSide slot painting both side panels with the weird-west panorama the art queue rendered in t-011 (a table without one still echoes its backglass). Apron and backbox-trim art have no art-queue entries; rails and trim stay chrome and black.
<!-- note:end t-017 -->

## t-018 — River Croc animatronic to Williams / Pinball FX quality

<!-- note:begin t-018 -->
Silas, 2026-10-12, after playing the table: "The croc animation however is very lackluster, nothing close to the quality of a Williams or pinballfx table ... it needs an upgrade." The t-015 toy is a 5 cm head of a few primitives easing between poses. Rebuild it as the table's signature toy: a sculpted head (lofted snout, eye bosses with slit pupils and blinking lids, nostrils, interlocking irregular teeth, gums and tongue, scarred scutes), a body and tail lying in the river behind it, spring-driven motion with anticipation, overshoot and settle, eyes and head that track the nearest ball, a living water surface (ripple rings, splash and spray particles, bubbles, wake), and staged beats for every phase: surfacing with eyes first, a snap with a head jerk and splash, a full-body death roll in a churn, a rear-and-lunge spit. Reduced motion keeps the poses and colour without rolls, shakes or flicker. Verified by close-up renders of every phase and the existing toy tests.
2026-10-12: done in kind_robots#3602 (merged 365c45f). The River Croc is rebuilt as a signature toy: lofted superelliptic head, jaw and body with baked vertex colour (29 draws, ~0.26 ms/frame); spring-driven jaw, sink, pitch, yaw and lunge; eyes and head that track the nearest ball; a 360 death roll on capture that settles upright; a spit lunge with a 180-droplet spray; a rippling translucent river with its own key and glow lights; and scale 1.3 so it reads from the play camera. Reduced motion keeps it still (no roll, tracking, spray, ripples or blink). verifyZuzuPinballCroc covers tracking, the roll, spray and reduced motion. A real-GPU look on main is still Silas's call; next iteration ideas (sound sync to the roll, a splash decal) go to new tasks if he wants them.
<!-- note:end t-018 -->

## t-019 — River Croc toy, second take: animated from Arthemy concept-quality art

<!-- note:begin t-019 -->
Silas, 2026-10-12, on the t-018 procedural 3D Croc: "I want another take on that croc. I want something closer to an animation style. Something that looks like our concept art. we've got shots of the crocodile attacking zuzu and the coyote. We should start with an image of that quality, built in arthemy or something like that, then generated out. None of this nintendo 64 quality graphic." References: the croc-and-coyote plate (ArtImage 243624, shipped as the gamebook's a1-the-shot), the music-video croc (242572) and the canonical croc (243495, scarred, algae, broken harpoon). Plan: (1) the key image, the Croc as the player sees him on the table, in the house Arthemy lane (projects/zuzu-pinball/art/T019-CROC-KEY.yaml, ArtJobs 37624-37629), Silas picks a seed; (2) generate it out: LTX/WAN first-to-last-frame clips per phase (submerged, rising, open, captured, death roll, spit) keyed onto a flat colour; (3) the table plays them as the toy, a keyed animated card standing in the watering hole over the existing scoop and jaw gate, replacing the procedural geometry. Reduced motion holds each phase's key frame.
October 12, 2026 PT: implementation merged. The River Croc is drawn from generated art in the concept art's inked western style. Key image: Arthemy house lane, Silas picked ArtImage 245776 (art/T019-CROC-KEY.yaml). Phase poses: Kontext edits (art/T019-CROC-POSES.yaml: gape 245782, submerged 245792, death roll 245788/245789). Clips: WAN (art/T019-CROC- CLIPS.yaml): TI2V-5B breathing and lurk loops; A14B first-last-frame snap, sink, rise, spit and a two-part death roll (245801-245806), after kind_robots#3608 fixed first-last frame (WanFirstLastFrameToVideo). tools/croc_atlas.py cuts every frame out of its white surround and packs a 101-frame atlas (kind_robots public/zuzu-pinball/river-croc.webp, 2.4 MB). The table plays it as an animated card lying in the painted pond with his snout at the scoop (kind_robots#3609 renderer + v1 atlas, #3613 v2 clips). Reduced motion holds one still per phase; the aim ring stays. Tests: croc, watering hole, stress (mean tick 1.36 ms), camera, LEDs, light map, shots. Headless renders only: the real-GPU look on kindrobots.org is Silas's call; next ideas if wanted: a larger card, a brighter submerged lurk, sound timed to the snap and roll.

October12 PT reviewer independently verified merged renderer kind_robots#3609 at0ee864c36903c5c0285f1b27eb4e67b4825dd75e and v2 atlas kind_robots#3613 at4f12ebd7a8fbecc1f9e501133601d774c7390c7d, all final-head checks completed green. conductor#6070 merged by original worker at43ecc535ec602a8eb6ee641d2a2917f011570be2. Independently passed1000 capture/spit cycles,24 Watering Hole swallows and 25 lifecycle plus3 six-ball stress replays. Final immutable GitHub assetHTTP200, 2404328bytes exactly match committed3840x2880RGBA atlas;101 nonempty cells. Close only t019 source/art integration; preserve t013 device QA and t014 human acceptance/publication gate. No deployment or realGPU verdict claimed.
<!-- note:end t-019 -->
