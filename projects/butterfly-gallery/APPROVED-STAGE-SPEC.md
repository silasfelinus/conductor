# Butterfly Gallery — Approved Stage + Animation Contract

Status: **APPROVED DIRECTION — 2026-09-18**

This document locks the visual composition Silas approved after the mockup
iteration. Treat it as the production reference for /butterfly-gallery.
Do not re-theme the page into a cozy gallery, cluttered factory, dashboard,
or alternate visual metaphor without explicit new direction.

## Core visual

A bright, friendly, minimalist **industrial warehouse sorting room** rendered
with crisp Saturday-morning-cartoon / cel-shaded energy.

The room itself is spacious and calm. The color comes primarily from the UI,
the artwork, and animated mascot actors rather than from decorative clutter.

No extra page title/header is rendered inside the scene; Kind Robots' real app
header already exists above the route.

No random inspirational copy, signs, slogans, mascots, robots, butterflies,
workers, or other living/acting figures are baked into the static background.

If it looks alive or implies motion, it belongs in an animation/DOM layer.

## Static background layer

The background contains only environmental structure:

- industrial warehouse walls, beams, catwalks, railings, shelving, lamps;
- the structural frame for the long horizontal animation window/runway;
- the structural mount and **convex** yellow drop funnel;
- structural mounting rails/frames for the central display and side controls;
- an empty lower-right recess/area where the robot animation can live;
- enough open air and depth for animated butterflies to cross naturally.

The funnel is **convex**:
- the upper/middle neck is narrower;
- the lower bell/mouth flares wider than the section immediately above it;
- an artwork can visibly emerge downward from the mouth without requiring a
  geometrically impossible reveal.

Do not bake any example artwork, butterflies, robots, photo piles, UI labels,
or moving conveyor content into this layer.

## Layout

### Top runway / animation window

One long, single horizontal window spans most of the upper scene, behind the
yellow funnel.

This is a dedicated animation surface, not a static decorative picture.

It needs enough horizontal travel for reusable passes such as:
- butterfly towing a framed image on a string;
- two butterflies carrying a frame;
- one butterfly struggling under a frame;
- butterfly/frame combinations crossing left-to-right or right-to-left;
- occasional failed/drop gag.

The funnel visually interrupts/occludes the middle of the runway so actors can
pass **behind** it.

### Left: five configurable preset bins

Exactly five visible large destination bins form the default left rail.

They are custom **presets**, not hard-coded meanings. Silas decides what each
does. Examples in mockups are illustrative only:

1. 5★ + add to a special collection
2. 4★ + apply a favorite tag
3. 3★ + keep as-is
4. 2★ + move to a chosen folder/collection
5. 1★ + archive / low-star destination

A preset may combine multiple actions. Successful preset application marks the
art as processed/done unless that preset explicitly opts out.

The visual color ladder may stay rainbow-like, but the labels and actions are
data-driven.

### Center: primary artwork

The selected artwork is the visual focal point and should be larger than the
early mockups.

It sits inside one large industrial display/frame.

When an image is selected, it appears automatically in this display. The user
does not operate a crane or manually align it into the frame.

When no image is selected, the frame hosts the blank-state loop described below.

### Right rail

Three vertically stacked functions only:

1. **Image Info**
   - compact overview; not a large inspector;
   - filename/title, prompt excerpt, dimensions, checkpoint/resources, rating,
     collection/process state as appropriate;
   - expandable/details affordance can expose more without occupying the stage.

2. **Cleanup**
   - non-destructive cleanup/enhancement workflow;
   - exact behavior comes from archive/action APIs.

3. **Trash**
   - destructive/recoverable trash workflow according to Art Archive semantics.

Do not add Keep/Replace action tiles here unless later explicitly requested.

### Foreground image pile

The unsorted pile is **not in a box**.

It rises from below the viewport like the visible upper portion of something much
larger: only the top mass of overlapping image thumbnails is visible.

The hidden lower portion implies a huge backlog.

The pile is tall enough to very slightly overlap the bottom edge of the central
display, creating depth.

It is dynamic UI built from real/fixture ArtImages, not part of the background
illustration.

## Layer stack

Back to front:

1. static warehouse backdrop
2. top-runway animation surface
3. static/DOM structural UI: left bins, central frame, right rail
4. lower-right **robot animation** layer
5. foreground dynamic image pile, occluding part of the robot
6. foreground **butterfly animation** above the left bins
7. selected/dragged image proxy and transient drop animation
8. global app header outside the scene

The layering is intentional. In particular, the robot sits **behind** the pile
so images can visually cover its lower body/hands while it appears to sift
through them.

## Animation contract

Up to four ambient animations may run simultaneously.

### A. Top runway passes

Location: long horizontal upper window behind the funnel.

Form: reusable non-looping clips selected/scheduled with varied timing, or a
loop assembled from discrete passes.

Subjects: animated butterflies carrying framed art.

No butterflies or carried artwork are baked into the static runway background.

### B. Blank-state center loop

Location: central display, only when no artwork is selected.

Form: simple gentle loop. It should read as an intentionally idle display rather
than a missing-image error.

Possible motion: softly drifting abstract image cards, gentle rings, subtle
gallery-screen motion. No interaction requirement.

It is immediately replaced by the selected ArtImage.

### C. Foreground butterfly loop

Location: above/around the left preset bins.

One rainbow butterfly flies in, flaps/hovers, settles/perches, idles, and may
repeat/reset gracefully.

It is its own transparent/composable asset/layer.

No static butterfly exists behind it.

### D. Foreground robot loop

Location: lower-right, behind the foreground image pile.

A Kind Robot mascot casually sorts/sifts through art: picks up a picture,
examines it, puts it down, shuffles another, etc.

Simple repeating loop. The foreground image pile intentionally masks part of
the actor.

No static robot exists in the background.

### E. Artwork drop transition

This is transient, not an always-running fifth ambient loop.

When a selected artwork enters via the top funnel, use an exaggerated classic
cartoon **stretch-and-snap** transition:
- image begins near normal proportions;
- stretches comically long vertically as it shoots/falls from the funnel;
- recoils/snaps back to its true aspect ratio as it lands in the central frame.

Think Tex Avery-era squash-and-stretch physics, implemented as deterministic UI
animation rather than embedding the user's image in a generated video.

The funnel mouth is deliberately wide/convex enough that the artwork can emerge
cleanly.

## Motion safety + performance

- Every living/acting thing is a separate animated layer.
- prefers-reduced-motion disables mascot loops and replaces the drop with a
  short fade/scale.
- Hide/pause ambient loops when the page/tab is not visible.
- Animation failure never blocks sorting.
- The actual artwork and bins remain ordinary accessible DOM/UI.
- Never turn the whole page into one video.

## Approved implementation sequence

1. build dynamic pile + large selected display;
2. build five custom left bins;
3. build compact Image Info + Cleanup + Trash right rail;
4. build the static industrial scene/layer containers;
5. wire blank-state center loop slot;
6. add foreground pile occlusion + robot slot;
7. add left butterfly slot;
8. add upper runway/funnel animation slot;
9. add stretch-and-snap selected-image transition;
10. replace placeholders with animation-creator outputs.

This sequence lets the page become useful before any generated animation asset
is final.
