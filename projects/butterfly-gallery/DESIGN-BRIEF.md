# Butterfly Gallery — Design Brief

## Product

Butterfly Gallery is the theatrical art-sorting surface Silas originally
imagined for Kind Robots: a functional curation tool presented as a living
gallery workshop where rainbow butterflies carry, drop, drag, and sort framed
pictures.

Route: `/butterfly-gallery`

Placement: Kind Robots **Plan** channel, **Projects** tab.

The route is a private/admin curation surface. It may display mature private art,
so it must use the same mature-viewer restrictions as the source data.

## Boundary with Art Archive

Butterfly Gallery and Art Archive are intentionally separate projects.

**Art Archive owns:**
- scanning `PRIVATE_PATH`;
- filesystem identity/reconciliation;
- ArchiveEntry state;
- importing private/mature ArtImages;
- folder-derived collections;
- checkpoint/LoRA provenance matching;
- missing-resource inventory;
- safe move/trash filesystem semantics;
- archive APIs.

**Butterfly Gallery owns:**
- the sorting/culling experience;
- the painting pile;
- selected central frame;
- customizable visual bins;
- drag/drop/click/keyboard curation interaction;
- the animated gallery room;
- butterfly motion;
- presentation of metadata;
- triggering archive actions and ordinary ArtJobs through existing APIs.

Butterfly Gallery must never scan `/app/private` itself or duplicate provenance
matching. Until the Art Archive read/action contract is ready, Gallery development
uses a fixture/adapter with the same shape.

## Experience

### Entry

The first entrance is a short non-looping vignette.

A trapdoor in the ceiling opens. Framed pictures tumble into a loose pile near
the bottom of the room. Rainbow butterflies react: one attempts a heroic solo
lift, another tows a frame by string, perhaps a pair struggle together. The
animation resolves into the exact steady-state scene the user will work in.

Target duration is roughly 2–4 seconds. It is immediately skippable, remembered
for the intended page/session scope, and replaced by a minimal transition under
`prefers-reduced-motion`.

The intro is flavor, never a loading hostage. Data can load concurrently and the
work surface must become usable even if an animation asset fails.

### Steady-state composition

The page reads vertically and spatially:

- **upper room:** ceiling/trapdoor plus a peekaboo window or opening;
- **left rail:** cleanup/unresolved/action bins;
- **center:** selected artwork in a large presentation frame;
- **right rail:** keep/classify/rating/preset bins;
- **bottom center:** the visible top of the unsorted painting pile;
- **background:** warm/dusky gallery-workshop scene with intermittent butterflies.

The room should be visually calmer than the butterflies. Let mascot color provide
the rainbow. User artwork remains the strongest visual object on screen.

### Painting pile

The pile is functional, not just scenery.

Only a small number of top items render as overlapping framed thumbnails with
light rotation and hover/focus lift. A remaining count communicates queue depth.
Selecting an item lifts it into the central frame. Successful sorting causes the
next candidate to rise naturally into place.

For very large queues, pagination/virtualization happens behind the metaphor.
Never render hundreds of originals just to look like a pile.

### Central frame

The selected image receives the most visual territory.

It sits in a reusable presentation frame and has an adjacent/below metadata
drawer for prompt, negative prompt, checkpoint, LoRAs, rating, processed state,
collections, match state, and extracted provenance.

Quick-action controls remain available even when the user ignores drag/drop.

### Bins

Bins are visual destinations rather than anonymous rectangles. They may read as
gallery carts, archive crates, ornate trays, hanging frames, or other coherent
room objects, but their hit targets and labels remain clear.

Each bin has:
- id;
- label;
- side: left/right;
- icon;
- kind;
- action payload;
- sort order;
- enabled state.

Initial useful kinds include:
- processed/unprocessed;
- rating 1–5;
- trash;
- add to collection;
- needs review;
- move;
- generation/action preset.

The visual grammar may use left for cleanup/unresolved and right for
classification/keep actions, but customization is authoritative.

Every bin action has drag, click/tap, and keyboard paths.

## Motion language

Motion is modular. Do not solve the page as one giant looping background video.

### Reusable butterfly clips

Produce separate non-looping clips for:

1. **String carrier** — a butterfly tows a frame dangling from a string.
2. **Team lift** — two butterflies awkwardly carry one frame.
3. **Solo struggler** — one butterfly slowly loses altitude under a heavy frame.
4. **Frame dragger** — a butterfly drags/slides a frame along a ledge or floor.
5. **Peekaboo scout** — a butterfly appears in the opening, pauses, disappears.
6. **Cross-window flight** — a clean reusable background pass.
7. **Oops/drop gag** — a rare dropped blank frame or failed carry.

The humor comes from differing levels of competence, not from constant chaos.

### Ambient system

Ambient butterflies mostly live behind the working UI, especially in the
peekaboo window. Schedule intermittent clips with varied timing instead of a
permanent synchronized loop. Pause or simplify when hidden and under reduced
motion.

### Interaction motion

Use fast deterministic UI animation for:
- thumbnail lifting out of pile;
- settling into the central frame;
- bin hover/highlight;
- successful bin acceptance;
- pile reshuffle / next-image rise.

Avoid freeform physics that makes valid drops difficult.

## Functional flow

1. Route loads and begins data fetch.
2. Intro plays or is skipped.
3. User picks an image from the pile.
4. Image appears in central frame.
5. User inspects metadata if needed.
6. User drags to a bin, clicks a bin/action, or uses a keyboard shortcut.
7. Action adapter calls the archive/API contract.
8. Success animates the image into the destination.
9. Next image is selected.
10. Filters/queue state update without a full page reload.

## Presets

Custom bins can bind to reusable generation/action presets such as:
- add LoRA;
- replace LoRA;
- switch checkpoint;
- append prompt fragment;
- replace prompt fragment;
- change CFG/steps/sampler/seed behavior;
- create an additional render;
- request a replacement render.

These actions use the existing archive adapters and durable ArtJob system.
Butterfly Gallery never creates a parallel render queue.

## File actions

Butterfly Gallery does not implement filesystem policy itself.

Move/trash bins call the Art Archive's root-confined safe operations. A normal
Trash action remains recoverable according to Art Archive semantics. Automatic
Gallery behavior never deletes bytes.

## Accessibility

Whimsy is optional; functionality is not.

Requirements:
- skip intro;
- reduced-motion path;
- keyboard/focus access to every bin;
- visible focus and selected state;
- click/tap alternative to drag;
- semantic labels for visual bins;
- useful screen-reader status after actions;
- no information conveyed only by animation;
- touch-friendly target sizes.

## Responsive behavior

Desktop gets the full theatrical composition.

Tablet may narrow the bin rails while preserving the central frame.

On phones, bins may become bottom/side trays or drawers while retaining the same
actions. Do not scale the entire desktop scene down until it becomes a dollhouse.

The painting pile can simplify into a compact overlapping stack/filmstrip on
small screens while preserving the metaphor.

## Art assets

Static/layered assets:
- gallery room background;
- trapdoor closed/open;
- painting pile base;
- central empty frame;
- left/right bin shells;
- peekaboo window/opening;
- optional strings/dust/rainbow trail overlays.

Motion assets:
- reusable butterfly clips from the shot list;
- trapdoor/picture-fall intro elements where asset motion is more appropriate
  than DOM animation.

User images should remain separate from decorative frame assets so arbitrary
private artwork can be inserted without regenerating the scene.

## Build order

1. **Functional shell:** route, store, fixture adapter, pile, frame, bins,
   metadata, first actions.
2. **Static stage:** room composition, frame, pile, window, bin art.
3. **Motion:** intro, butterfly clips, ambient scheduler, micro-interactions.
4. **Power tools:** custom bins, presets, batch mode, ArtJob actions.
5. **Integration/polish:** real Art Archive feed, privacy tests, performance,
   responsive work, accessibility, final human visual acceptance.

## Definition of done

Butterfly Gallery is done when the private admin user can open it from Plan,
watch/skip the short gallery intro, select real private ArtImages from a painting
pile, inspect them in a central frame, and efficiently classify or act on them
through customizable left/right bins using drag, click/touch, or keyboard.

The page feels unmistakably Kind Robots because rainbow butterflies inhabit the
space and move artwork with charmingly uneven competence, but sorting remains
faster than the theater around it.
