# Butterfly Gallery Animation Shot List

Status: implementation contract for `butterfly-gallery/t-013`, corrected by Silas 2026-09-19

This file translates `APPROVED-STAGE-SPEC.md` and `MOTION-STORYBOARD.md` into reusable motion actors. It does not redefine the first-visit intro or the DOM stretch-and-snap selected-image transition. All actors remain separate composable layers. No living thing is baked into the static warehouse background.

## 2026-09-19 canonical butterfly correction

The Kind Robots rainbow butterfly already has a canonical live implementation.

Use the visual grammar from `components/screenfx/butterfly-animation.vue` and the existing butterfly helpers/store:

- two simple asymmetric translucent wing lobes;
- radial-gradient rainbow color, with related/complementary wing tones;
- a tiny dark body;
- fast CSS wing flapping;
- runtime heading/bank/bob/fade motion;
- abstract luminous silhouette rather than a detailed illustrated insect.

This is the look visible in the Butterfly Scouts screensaver. It is intentional. Do **not** reinterpret Butterfly Gallery butterflies as Disney-like, anthropomorphic, face-bearing, highly detailed, or conventional cartoon butterflies.

For Butterfly Gallery, prefer extracting/reusing this DOM/CSS renderer and choreographing it inside the Gallery's own clipped animation surfaces. This guarantees the mascot stays visually canonical and lets motion use the real runtime dimensions instead of guessing a video canvas.

## Production geometry hold

Silas is manually installing the approved static Gallery assets on the media server under `/images/butterfly-gallery`.

Do not submit replacement motion jobs against guessed room/window geometry.

Any remaining generated animation that needs a background plate must wait until the final production asset is installed, then use the **exact final image/crop and exact target dimensions as the first frame/reference**.

Previously submitted Stage-2 video jobs 28725-28732, including cancelled/requeued jobs, are reference material only. They are not approved production animation and must not be polled, revived, or resubmitted merely because their queue state changes.

## Shared production rules

- User sorting must remain fully usable with every mascot layer absent.
- Butterflies are runtime DOM/CSS actors derived from the canonical Butterfly Scouts implementation unless Silas explicitly approves a different approach.
- No butterfly or robot is baked into the warehouse background.
- Runtime butterfly actors may carry/tow separate DOM/SVG/CSS picture-frame props.
- Runway actors must clip inside the real runway and disappear behind the central funnel by ordinary layer/overflow rules.
- The lower-right robot remains behind the dynamic foreground image pile.
- Reduced-motion mode suppresses mascot motion.
- Pause or stop ambient actors when the Gallery is hidden.
- Do not use generated example user art inside decorative frames.

## Job family A: upper runway passes

**Implementation:** runtime DOM/CSS/SVG choreography, not pre-rendered butterfly videos.

The actor surface is the actual `data-animation-slot="butterfly-runway"` runtime box. Motion paths derive from its measured width/height.

### A1: String tow

One canonical rainbow butterfly crosses the full runway while towing a small blank picture frame on a string. The frame lags and sways once before settling.

Target duration: 3 to 4 seconds, non-looping event.

### A2: Team carry

Two canonical butterflies carry one blank frame together. Their wing motion remains independent; the shared frame bobs slightly out of sync, then stabilizes.

Target duration: 3 to 4 seconds, non-looping event.

### A3: Solo struggler

One canonical butterfly carries an oversized blank frame, dips under the apparent weight, recovers altitude, and completes the crossing.

Target duration: 3.5 to 4.5 seconds, non-looping event.

### A4: Clean cross

One canonical butterfly escorts or lightly carries a modest blank frame in a smooth competent pass.

Target duration: 2.5 to 3.5 seconds, non-looping event.

### A5: Rare failed/drop gag

One or two canonical butterflies carry a blank frame. The frame slips downward near mid-pass, exits the clipped runway cleanly, and the butterflies recover.

Target duration: 3 to 4 seconds, non-looping event. Runtime scheduler controls rarity.

## Job family B: left foreground butterfly

**Implementation:** runtime DOM/CSS actor derived from the same canonical Butterfly Scouts wing renderer.

Canvas/surface: the existing `foreground-butterfly-slot` above the left bins.

### B1: Fly, hover, perch, idle, reset

Enter from outside the slot, flap into position, hover, settle on an implied edge, idle calmly with wing movement, then lift off/reset.

Target duration: 5 to 8 seconds logical loop with a calm idle segment.

Do not make the butterfly constantly orbit the bins. Runtime pauses may make the repeated loop feel intermittent.

## Job family C: lower-right Kind Robot

**Implementation:** generated loop is acceptable here because the robot has richer authored action than the abstract butterflies.

Do not generate until the final Gallery stage asset is installed and the exact lower-right target crop and dimensions are known.

Use the exact final production background crop as first frame/reference so lighting, perspective, palette, and environment match the page. The real dynamic picture pile remains a separate foreground DOM layer and must occlude the robot.

### C1: Picture sift loop

Robot reaches down behind the implied pile, lifts a simple blank picture/card, examines it with a small head tilt, lowers it, shuffles/reaches for another, and returns to neutral.

Target duration: 6 to 10 seconds loop.

No generated user artwork, text, logos, or baked pile.

## Job family D: central blank-state display

**Implementation:** keep the existing lightweight CSS/DOM blank-state loop unless Silas later rejects it in visual acceptance.

This state disappears immediately whenever a real ArtImage is selected.

The motion should remain calm, low-contrast, and abstract, with no mascot, fake art, or loading-spinner semantics.

## Runtime acceptance handoff

`t-014` remains waiting until Silas confirms the production Gallery assets are installed and real geometry can be measured.

When released, t-014 must verify:

- the canonical butterfly renderer is reused/extracted rather than visually reinterpreted;
- runway paths are computed from the real runtime slot dimensions;
- butterfly+frame props clip cleanly at the runway bounds and behind the funnel;
- the left butterfly is independently composable above the left bins;
- the lower-right robot matches the final production stage and reads correctly while partially occluded by the real foreground pile;
- blank-state motion remains lightweight and disappears when art is selected;
- no generated motion contains static butterflies/robots in the warehouse backdrop;
- hidden/reduced-motion states stop the relevant animation work.
