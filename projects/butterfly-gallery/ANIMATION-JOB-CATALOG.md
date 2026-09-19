# Butterfly Gallery — Animation Job Catalog (t-014)

Submitted 2026-09-19 by `claude-scheduled-20260919T123845Z-butterflygallery-t014`
via `POST https://kindrobots.org/api/art/enqueue` (Bearer `KR_API_TOKEN`), per
`ANIMATION-SHOT-LIST.md` and the roadmap's `t-014` note. All 7 jobs were
submitted at **priority 0** (the deliberate lowest queue band — RENDER
PRIORITY OVERRIDE, 2026-09-19), `projectSlug: butterfly-gallery`,
`isPublic: false`, `isMature: false`, `engine: ltx`, `outputFormat: webp`,
`renderScale: 1` (direct render, no latent upscale pass). Each request's
`firstImageBase64` was built by fetching the named production PNG over HTTPS
from `https://kindrobots.org/images/butterfly-gallery/<file>` and
base64-encoding it — the images are not in the kind_robots git checkout
(gitignored, served from the media server).

Every job was confirmed registered as `PENDING` via
`GET /api/art/queue/:id` immediately after submission (see the per-job
`Confirmed` column). These are **superseding, brand-new job ids
(28739–28745)** — the earlier Stage-2 jobs 28725–28732 remain superseded per
the roadmap note and were not touched or revived.

## Source images used (fetched, dimensions confirmed via `file`)

| File | Pixel size | Used for |
|---|---|---|
| `runway-background.png` | 2172 × 724 (exact 3:1) | first frame for all 5 runway shots (A) |
| `gallery-butterfly-start.png` | 1254 × 1254 (1:1) | first frame for the left foreground loop (B); the canonical Gallery-butterfly character reference described in every prompt |
| `robot-sift-start.png` | 1254 × 1254 (1:1) | first frame for the lower-right robot loop (C) |
| `display-blank-state.png` | 1448 × 1086 | fetched for reference only — NOT submitted; per the roadmap note the central blank state may keep its existing CSS/DOM loop, so no ArtJob was queued for it |

Output dimensions were chosen to preserve each source's exact aspect ratio
while staying comfortably under the endpoint's 2048px max and favoring a
fast render at this lowest priority tier (`renderScale: 1`, no upscale
chain): 768×256 (exact 3:1, matches `runway-background.png`) for the runway
shots, 768×768 (exact 1:1) for both loops. `presetId` is passed as
descriptive metadata only (the server does not derive width/height/etc. from
it — those are supplied directly in the request) and was chosen as the
closest matching shape: `ltx-12gb-quick` for the short non-looping runway
passes, `ltx-startup-webp` for the two looping close-ups.

## A. Upper runway passes (5 shots, non-looping, `runway-background.png` first frame)

| Shot | Job key / idempotencyKey suffix | jobId | Engine | Preset | Dimensions | Duration/FPS | Loop | Priority | Confirmed |
|---|---|---|---|---|---|---|---|---|---|
| String tow | `runway-string-tow` | **28739** | ltx | ltx-12gb-quick | 768×256 | 3s / 16fps | false | 0 | PENDING |
| Team carry | `runway-team-carry` | **28740** | ltx | ltx-12gb-quick | 768×256 | 3s / 16fps | false | 0 | PENDING |
| Solo struggler | `runway-solo-struggler` | **28741** | ltx | ltx-12gb-quick | 768×256 | 3s / 16fps | false | 0 | PENDING |
| Clean cross | `runway-clean-cross` | **28742** | ltx | ltx-12gb-quick | 768×256 | 3s / 16fps | false | 0 | PENDING |
| Rare fumble | `runway-rare-fumble` | **28743** | ltx | ltx-12gb-quick | 768×256 | 3s / 16fps | false | 0 | PENDING |

Prompts (full text submitted as `promptString`; `negativePrompt` shared
across all five — see below):

1. **String tow (28739):** "A small illustrated rainbow-winged Gallery
   butterfly (matching the reference image exactly: expressive round eyes,
   layered rainbow-gradient wings, delicate curled antennae) flies steadily
   along a bright industrial warehouse runway window, towing a single BLANK
   generic portrait picture frame that dangles behind it on a thin taut
   string. The frame swings gently with the butterfly's wingbeats as it tows
   the empty frame from one side of the runway toward the other. The frame
   stays completely blank/generic, no artwork inside it. Warm even studio
   lighting, smooth smallscale character animation, clean background
   matching the existing runway plate."

2. **Team carry (28740):** "Two small illustrated rainbow-winged Gallery
   butterflies (matching the reference image: rounded expressive eyes,
   layered rainbow-gradient wings) fly side by side along the bright
   warehouse runway window, awkwardly and cooperatively carrying one medium
   BLANK generic portrait frame together between them, gripping opposite
   top corners of the frame with their front legs. Their flight is slightly
   uneven and effortful as they coordinate to keep the frame level while
   crossing the runway. The frame stays completely blank, no artwork inside
   it. Warm even studio lighting, clean background matching the existing
   runway plate."

3. **Solo struggler (28741):** "A small illustrated rainbow-winged Gallery
   butterfly (matching the reference image: rounded expressive eyes,
   layered rainbow-gradient wings) struggles to carry an oversized BLANK
   generic portrait frame, much bigger than itself, along the bright
   warehouse runway window. It dips down noticeably under the frame's
   weight partway across, wobbles unsteadily side to side, then flaps hard
   to recover altitude and continues on, finally exiting the far side of
   the runway still carrying the frame. The frame stays completely blank,
   no artwork inside it. Warm even studio lighting, clean background
   matching the existing runway plate."

4. **Clean cross (28742):** "A small illustrated rainbow-winged Gallery
   butterfly (matching the reference image: rounded expressive eyes,
   layered rainbow-gradient wings) confidently and smoothly carries a
   modest BLANK generic portrait frame in a single steady, competent, level
   flight straight across the bright warehouse runway window from one side
   to the other, with no wobble or hesitation. The frame stays completely
   blank, no artwork inside it. Warm even studio lighting, smooth confident
   flight animation, clean background matching the existing runway plate."

5. **Rare fumble (28743):** "A small illustrated rainbow-winged Gallery
   butterfly (matching the reference image: rounded expressive eyes,
   layered rainbow-gradient wings) is carrying a BLANK generic portrait
   frame along the bright warehouse runway window when the frame suddenly
   slips loose from its grip mid-carry and begins to fall; the butterfly
   darts down and flaps urgently to catch and recover it, wings fluttering
   rapidly in a startled recovery motion, then steadies and continues on
   with the frame back in its grip. The frame stays completely blank, no
   artwork inside it. Warm even studio lighting, clean background matching
   the existing runway plate."

Shared runway `negativePrompt`: "procedural particle screensaver look, plain
generic butterfly icon, extra background characters, rendered example
artwork inside frame, text, watermark, logo, blurry, distorted anatomy,
extra limbs, low quality, jpeg artifacts, warped background architecture,
visible finished painting or photo inside the frame, colored artwork in
frame, static frozen background actors, other robots"

## B. Left foreground butterfly loop (1 shot, looping, `gallery-butterfly-start.png` first frame)

| Shot | jobId | Engine | Preset | Dimensions | Duration/FPS | Loop | Priority | Confirmed |
|---|---|---|---|---|---|---|---|---|
| Left butterfly loop | **28744** | ltx | ltx-startup-webp | 768×768 | 4s / 16fps | true | 0 | PENDING |

Prompt: "Close-up of the illustrated rainbow-winged Gallery butterfly
exactly as shown in the reference image: expressive round eyes, layered
rainbow-gradient wings, delicate curled antennae, full character
personality preserved (not a simplified particle or screensaver icon). It
flies in from off-frame, hovers in place flapping its wings, settles and
perches gently, then holds a calm idle wing-flutter for a moment, before
resetting and leaving frame the way it came so the loop can repeat
seamlessly. Warm soft studio lighting, expressive charming character
animation, plain uncluttered background so the loop composites cleanly
over the gallery scene."

Negative prompt: "procedural particle screensaver look, plain generic
butterfly icon, extra background characters, rendered example artwork
inside frame, text, watermark, logo, blurry, distorted anatomy, extra
limbs, low quality, jpeg artifacts, warped background architecture"

## C. Lower-right Kind Robot loop (1 shot, looping, `robot-sift-start.png` first frame)

| Shot | jobId | Engine | Preset | Dimensions | Duration/FPS | Loop | Priority | Confirmed |
|---|---|---|---|---|---|---|---|---|
| Lower-right robot loop | **28745** | ltx | ltx-startup-webp | 768×768 | 4s / 16fps | true | 0 | PENDING |

Prompt: "The Kind Robots sifting robot exactly as shown in the reference
image reaches down into an implied pile of pictures just below frame, lifts
up a single picture or card in its gripper, inspects it with a small
curious head tilt from side to side, then lowers the picture and sets it
aside out of frame, before reaching down again to shuffle through the
implied pile and pick up another, finally returning to a neutral resting
pose. Calm, methodical, charming robotic motion. Warm even studio lighting,
plain uncluttered background so the loop composites cleanly behind the
live foreground picture pile."

Negative prompt: "procedural particle screensaver look, plain generic
butterfly icon, extra background characters, rendered example artwork
inside frame, text, watermark, logo, blurry, distorted anatomy, extra
limbs, low quality, jpeg artifacts, warped background architecture"

## Full job-id summary

| jobId | Shot | Loop | Priority | Status confirmed at submission time |
|---|---|---|---|---|
| 28739 | A1 string tow | no | 0 | PENDING |
| 28740 | A2 team carry | no | 0 | PENDING |
| 28741 | A3 solo struggler | no | 0 | PENDING |
| 28742 | A4 clean cross | no | 0 | PENDING |
| 28743 | A5 rare fumble | no | 0 | PENDING |
| 28744 | B left butterfly loop | yes | 0 | PENDING |
| 28745 | C lower-right robot loop | yes | 0 | PENDING |

## What was NOT done here (by design — see the follow-on task)

These are async renders behind the existing priority-100/200 backlog at
priority 0 (deliberately last in line). Actually splicing the finished
clips into `pages/butterfly-gallery.vue`'s reserved animation slots
(occlusion by the funnel/pile, the real horizontal runway window,
independent composability of the left loop, partial-occlusion legibility of
the robot loop, and reduced-motion/visibility gating) is out of scope for
this task and is tracked by the follow-on integration task created
alongside this catalog (see the roadmap for its id and full acceptance
criteria, carried over unchanged from t-014's own note).

Do not requeue or "helpfully" resubmit any of jobs 28725–28732 — those are
explicitly superseded Stage-2 references, not live work.
