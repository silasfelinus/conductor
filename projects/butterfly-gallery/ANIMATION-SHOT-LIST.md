# Butterfly Gallery Animation Shot List

Status: implementation contract for `butterfly-gallery/t-013`

This file translates `APPROVED-STAGE-SPEC.md` and `MOTION-STORYBOARD.md` into reusable animation-creator jobs. It does not redefine the first-visit intro or the DOM stretch-and-snap selected-image transition. All actors remain separate composable layers. No living thing is baked into the static warehouse background.

## Shared production rules

- Visual language: bright minimalist Saturday-morning-cartoon / cel-shaded Kind Robots warehouse, crisp silhouettes, cheerful rainbow butterfly palette, no photorealism.
- Every mascot clip must be reusable without text, labels, UI chrome, example gallery art, or a baked warehouse background.
- Prefer transparent/composable output where the animation backend supports it. If transparency is unavailable, render against a flat removable key background and record that limitation with the job.
- Preserve a stable actor identity across variants. Butterflies are rainbow Kind Robots mascots, not generic realistic insects. The robot is the established friendly Kind Robot mascot.
- Keep motion readable at small sizes. Avoid particle showers, camera moves, zooms, cuts, or scenery motion.
- Runway clips are discrete non-looping passes. Left-butterfly, robot, and blank-state assets are loops with clean reset points.
- Reduced-motion mode does not play these clips. Runtime visibility/pause behavior belongs to later implementation tasks.
- Generated project art uses ArtJob priority **200**. Do not use the Resource/LoRA preview-refill priority lane.

## Job family A: upper runway passes

Canvas contract: wide transparent/composable strip suitable for the long horizontal runway. Actor and carried frame stay vertically compact enough to clear the runway. Motion traverses the full canvas so the runtime can clip it and occlude the middle behind the convex funnel.

### A1 — String tow

**Job key:** `butterfly-gallery/runway-string-tow-v1`

**Motion:** one rainbow butterfly flies steadily across frame while towing a small empty picture frame on a visibly taut string. The frame lags, sways once, then settles. No crash or stop.

**Duration target:** 3.0–4.0 s, non-looping.

**Variants:** left-to-right and right-to-left. Mirror at runtime only if the frame/string geometry remains believable; otherwise render both directions.

### A2 — Team carry

**Job key:** `butterfly-gallery/runway-team-carry-v1`

**Motion:** two rainbow butterflies carry one empty frame together, briefly bob out of sync, correct themselves, and continue cleanly across the runway.

**Duration target:** 3.0–4.0 s, non-looping.

### A3 — Solo struggler

**Job key:** `butterfly-gallery/runway-solo-struggle-v1`

**Motion:** one determined butterfly carries an oversized empty frame. It dips under the weight, flaps hard, recovers altitude, and completes the crossing. Comedic effort, not distress.

**Duration target:** 3.5–4.5 s, non-looping.

### A4 — Clean cross

**Job key:** `butterfly-gallery/runway-clean-cross-v1`

**Motion:** one butterfly escorts or lightly carries a modest empty frame in a smooth, competent crossing. This is the quiet baseline pass so every runway event is not a gag.

**Duration target:** 2.5–3.5 s, non-looping.

### A5 — Rare failed/drop gag

**Job key:** `butterfly-gallery/runway-drop-gag-v1`

**Motion:** one or two butterflies carry an empty frame; the frame slips downward out of their grasp near mid-pass, the butterflies make one startled correction beat, then continue/recover. The dropped frame exits the asset cleanly rather than exploding or leaving debris.

**Duration target:** 3.0–4.0 s, non-looping.

**Runtime frequency:** rare. The scheduler, not the asset, controls rarity.

## Job family B: left foreground butterfly

Canvas contract: transparent/composable actor layer sized for the air above the five left bins. No bin art or warehouse scenery in the clip.

### B1 — Fly, hover, perch, idle, reset

**Job key:** `butterfly-gallery/left-butterfly-perch-loop-v1`

**Motion beats:** enter from outside the layer; flap into position; hover for a beat; settle/perch on an implied invisible edge; small wing/antenna idle; lift off and exit/reset gracefully.

**Duration target:** 5–8 s seamless logical loop, with at least one calm 1–2 s idle segment.

**Constraint:** do not make the butterfly continuously orbit the bins. The loop should feel intermittent even when repeated with runtime pauses.

## Job family C: lower-right Kind Robot

Canvas contract: transparent/composable lower-right actor. Compose the robot so its lower body and hands may be partially hidden by the dynamic foreground image pile without destroying the readable upper-body action.

### C1 — Picture sift loop

**Job key:** `butterfly-gallery/robot-picture-sift-loop-v1`

**Motion beats:** robot reaches down behind the implied pile; lifts a simple blank picture/card; examines it with a small head tilt; lowers it; shuffles/reaches for another; returns to neutral.

**Duration target:** 6–10 s loop.

**Constraint:** cards are neutral placeholders only, with no generated user artwork, text, logos, or baked pile. The real pile is DOM UI in front of this layer.

## Job family D: central blank-state display

Canvas contract: central-frame interior only. This is not a mascot requirement and must disappear immediately when a real ArtImage is selected.

### D1 — Gentle gallery idle

**Job key:** `butterfly-gallery/blank-state-idle-loop-v1`

**Motion:** sparse abstract picture-card outlines or soft rings drift subtly within the frame, then return to their starting composition. Calm, low-contrast, unmistakably intentional idle state rather than a loading spinner.

**Duration target:** 6–10 s seamless loop.

**Constraint:** no butterflies, robot, words, loading icon, fake artwork, or attention-grabbing pulse.

## Animation-creator queue manifest

Create one animation-creator job for each key below. `priority: 200` is mandatory for every generated Butterfly Gallery asset.

| Job key | Mode | Priority | Output intent |
| --- | --- | ---: | --- |
| `butterfly-gallery/runway-string-tow-v1` | non-looping | 200 | upper runway pass |
| `butterfly-gallery/runway-team-carry-v1` | non-looping | 200 | upper runway pass |
| `butterfly-gallery/runway-solo-struggle-v1` | non-looping | 200 | upper runway pass |
| `butterfly-gallery/runway-clean-cross-v1` | non-looping | 200 | upper runway baseline |
| `butterfly-gallery/runway-drop-gag-v1` | non-looping | 200 | rare upper runway gag |
| `butterfly-gallery/left-butterfly-perch-loop-v1` | loop | 200 | left foreground actor |
| `butterfly-gallery/robot-picture-sift-loop-v1` | loop | 200 | lower-right actor behind pile |
| `butterfly-gallery/blank-state-idle-loop-v1` | loop | 200 | empty central display |

For each queued job, persist the job key, prompt/version, source/reference asset IDs if used, backend/workflow identity, output path/asset ID, and render result so `t-014` can inspect and catalog attempts without guessing provenance.

## Acceptance handoff to t-014

`t-013` is complete when this shot/job contract exists and the animation-creator queue has an unambiguous manifest. `t-014` owns generation, inspection, rejection/rerender decisions, and cataloging of the actual clips. It must verify:

- runway passes can traverse the full runway and disappear behind the funnel;
- the left butterfly remains independently composable above the bins;
- the robot reads correctly when partially occluded by the real foreground pile;
- blank-state motion is gentle and contains no fake user art;
- no generated clip contains a static warehouse backdrop or baked UI;
- every accepted asset retains reproducible job/provenance metadata.
