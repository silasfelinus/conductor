# Butterfly Gallery Animation Shot List

Status: production motion contract, updated by Silas 2026-09-19

The static production assets are installed and served from
`/images/butterfly-gallery`. Animation generation is now allowed, but all NEW
Butterfly Gallery animation ArtJobs must use **priority 0**, the lowest normal
queue band. Kind Robots claims pending jobs by priority descending, so this work
must remain behind the existing art backlog even though Butterfly Gallery itself
is a high-priority agent project.

## Canonical Gallery butterfly

Use `/images/butterfly-gallery/gallery-butterfly-start.png` as the Butterfly
Gallery butterfly visual reference.

This is intentionally more illustrated and expressive than the procedural
Butterfly Scouts screensaver while still reading as the same rainbow-butterfly
universe. For this feature, do not substitute the procedural Butterfly Scouts
DOM/CSS renderer. Runway butterflies are smaller versions of this illustrated
Gallery butterfly, animated through LTX/WAN or the current image-to-video path.

## Production references

- room: `/images/butterfly-gallery/room.png`
- window frame: `/images/butterfly-gallery/window.png`
- runway background: `/images/butterfly-gallery/runway-background.png`
- runway foreground/occlusion helper: `/images/butterfly-gallery/runway-foreground-mask.png`
- funnel/drop tube: `/images/butterfly-gallery/drop-tube.png`
- central frame: `/images/butterfly-gallery/frame.png`
- foreground pile: `/images/butterfly-gallery/pile.png`
- alternate pile reference: `/images/butterfly-gallery/pile-alt.png`
- Gallery butterfly: `/images/butterfly-gallery/gallery-butterfly-start.png`
- robot starter: `/images/butterfly-gallery/robot-sift-start.png`
- blank display base: `/images/butterfly-gallery/display-blank-state.png`

Do not invent dimensions or alternate backgrounds. Use the actual production
asset/crop for the target slot as the first-frame/context image.

## A. Upper runway passes

Use `runway-background.png` as the static scene and
`gallery-butterfly-start.png` as the butterfly reference. Portraits/frames
should be blank or generic props, never generated example user art.

Each is a short non-looping pass suitable for random scheduling:

1. **String tow** — one small Gallery butterfly tows a blank portrait frame on a string.
2. **Team carry** — two small Gallery butterflies carry one medium blank frame.
3. **Solo struggler** — one butterfly carries an oversized frame, dips, recovers, exits.
4. **Clean cross** — one butterfly makes a competent smooth carry across the runway.
5. **Rare fumble** — a carried blank frame slips/drops while the butterfly recovers.

The actual window/funnel layering is handled by the page. Keep the animated
scene compatible with the real runway crop and avoid adding static actors that
would remain frozen between actions.

## B. Left foreground butterfly

Source: `gallery-butterfly-start.png`.

Create a simple loop: fly in, hover/flap, settle/perch, calm idle wing movement,
then reset/leave. This is a close-up personality beat, so retain the illustrated
butterfly's expressive shape rather than simplifying it into the screensaver
particle look.

## C. Lower-right Kind Robot

Source: `robot-sift-start.png` plus the exact lower-right production stage crop.

Loop: reach into the implied pile, lift a picture/card, inspect with a small head
tilt, lower/set it aside, shuffle/reach again, return to neutral. The real dynamic
picture pile remains a separate foreground DOM layer and must occlude the robot.

## D. Central blank state

The existing CSS/DOM blank-state animation remains acceptable. If a generated
replacement is later requested, use `display-blank-state.png` as the exact
first frame/reference and keep the motion calm and low-contrast.

## Queue and retry policy

- NEW animation ArtJobs: **priority 0**.
- Never raise them merely because Butterfly Gallery is a high-priority project.
- Old jobs 28725-28732 are superseded and should not be revived as production.
- Re-render only a specific failed/rejected new job, not the whole set.
- Preserve stable job keys/provenance so accepted clips can be cataloged.
- Hidden/offscreen and `prefers-reduced-motion` states must pause/suppress motion
  when clips are integrated.
