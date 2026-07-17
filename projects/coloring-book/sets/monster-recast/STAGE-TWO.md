# Monster Recast — Stage Two

This file replaces GitHub issue #414 as the durable project-local handoff for Monster Recast production. The Conductor Worker selects roadmap tasks, not broad standalone issues, so execution remains owned by `projects/coloring-book/roadmap.yaml`.

The structured companion is `stage-two-handoff.yaml`.

## What is already true

Everything physically present in `approved/` is approved to move into **stage two** as a working base. A working base may be a colored master, a black-and-white base, or a complete pair; it is not automatically a final page.

The dated July 12 inventory recorded:

- 27 approved WebP files
- 18 represented concepts
- 9 complete color/BW pairs
- 8 BW-only working bases
- 1 color-only working base

Run this before any selection, refinement, conversion, queue edit, or count update:

```bash
python scripts/coloring_approved_status.py --check
```

The scan is authoritative for the live filesystem. The counts above are a migration snapshot, not permission to ignore newer files.

## Roadmap ownership

### `t-007` — exploration

Finish paired first-pass color and black-and-white studies for concepts not represented in `approved/`. Use `unapproved-art-jobs.yaml`, the objective quality gate, and vision curation. Exploration may produce optional alternatives, but it must not replace an accepted production base without Silas explicitly promoting it.

### `t-013` — selection and stage-two refinement

This task owns the inventory reconciliation that was stranded in issue #414:

- map every file in `approved/` to its canonical concept ID and working title
- record whether each concept has color, BW, or a complete pair
- surface filename drift and duplicates without silently renaming or deleting binaries
- verify the provisional `masked-countess` → `mr-018` Doctor Feast mapping
- preserve accepted composition, anatomy, body type, scars, age, creature structure, perspective, contact points, and visual joke
- repair pairs whose composition or identity diverges
- record source asset, prompt, workflow/model, seed/job metadata, and output path

Existing approved bases may enter this work without waiting for unrelated exploratory renders.

### `t-015` — faithful coloring conversion

This task owns missing counterparts and final line-art conversion:

- identify the eight BW-only concepts needing colored masters
- identify the one color-only concept needing faithful line art
- convert from the selected colored composition rather than redesigning the page
- apply `STYLE-GUIDE.md`: serious theatrical camp, thick black contours, bounded color, organized high detail, coherent contact points, and no collage

### `t-016` — packaging

Packaging begins only after selection, private Character creation, and coloring conversion are complete. Publishing, POD accounts or listings, spend, storefront release, and public Character release remain out of scope.

## Captain Hook addition

The proposed canonical addition is `mr-035`, **The Ticking Captain**:

A formidable older woman pirate captain with a weathered, powerful body and an original articulated prosthetic hook-hand is pursued across impossible seas by a vast clockwork marine predator whose brass gill plates tick like a ship chronometer. At a low storm-deck angle, she braces at the wheel, catches snapping rigging with the hook, and stares down the luminous predator beneath the hull.

The hook opens into a nested compass-and-chronometer claw whose hands point directly toward the predator. The commercial version needs an original captain identity, ship, costume system, prosthetic mechanism, time curse, and marine species.

Do not use Disney-specific likeness, mustache, red-coat design, feathered hat, crocodile design, typography, supporting characters, or exact scene recreation.

The canonical integration work remains explicit in `stage-two-handoff.yaml`: add the concept to `homage-concepts.yaml`, add its scene prompt to `art-modeler-request.yaml`, and queue its paired color/BW studies in `unapproved-art-jobs.yaml`.

## Done means

Stage two is ready to run cleanly when:

1. `approved/` and `approved/manifest.yaml` agree at the per-file level.
2. The Captain Hook lineage exists in the canonical concept and generation manifests.
3. Missing counterpart work is identified and queued.
4. Existing approved bases can be refined without reinventing accepted designs.
5. Roadmap tasks `t-007`, `t-013`, and `t-015` remain the authoritative execution queue.
