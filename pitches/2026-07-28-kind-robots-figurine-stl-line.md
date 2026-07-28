# Pitch: Kind Robots Figurine Line — first real product on the approved `stl-3d` type

date: 2026-07-28
project-target: digital-storefront
status: awaiting-silas

## The idea

`digital-storefront/product-types.yaml` already approves `stl-3d` ("3D printables
(STL)") as a product type, and `model-builder`'s own design (`PROJECT-BRIEF.md`,
Reward Deck section) already specs the exact pipeline needed to produce one:
`threeDPrompt` → reference image → generated GLB (Hunyuan3D) → mesh inspection/repair
→ verified STL conversion/export → print-readiness review (manifold geometry, wall
thickness, orientation, supports). Both halves exist on paper; neither has ever been
run end-to-end to produce an actual sellable file. This pitch asks to run that
pipeline for real on one or two well-loved Kind Robots characters and list the result
as the storefront's first `stl-3d` product — a desktop figurine buyers can print at
home or order pre-printed later.

## Why it's worth doing

- **Both halves already exist; nothing new needs inventing.** The product type is
  pre-approved (no `product-types.yaml` change, no new pitch needed for that part),
  and `model-builder/t-012` already designed the exact Hunyuan3D → mesh-repair →
  STL → print-readiness sequence. This pitch is "connect two proven plans," not
  "AI but for figurines."
- **model-builder's own brief is explicit that nothing gets labeled STL or
  print-ready until those stages *actually* run** — right now that's still true
  for every existing Reward/Character in the system. Someone has to be the first
  real run, or the design stays permanently theoretical.
- **Clear human benefit and a natural fit for the site's existing character IP** —
  Kind Robots characters already have art, lore, and a fan-facing identity; a
  physical figurine is a low-effort extension of assets that already exist,
  not a new content pipeline.
- **Ships in a testable slice.** One reference figurine proves the pipeline before
  any commitment to a full product line, mirroring how model-builder's own roadmap
  already prefers "prove with one reference run" over building broad first (see
  its Character Deck / Dream-expansion reference-run tasks).

## Rough effort

medium — the generation + mesh-repair + STL-export steps are compute/pipeline work,
not novel design; print-readiness review for a single test figure is a bounded,
one-time verification pass.

## Suggested first task

In `model-builder`, run the existing spec'd pipeline end-to-end for exactly one
approved Kind Robots character's `ITEM`-type Reward (pick one that already has a
`threeDPrompt`/reference image, per the Reward Deck contract): generate the GLB,
run mesh inspection/repair, produce a verified manifold STL, and do the
print-readiness review (wall thickness, orientation, supports) called for in
`PROJECT-BRIEF.md`. Do not label anything print-ready until that review actually
passes. If it passes, hand the verified STL to `digital-storefront` to list as the
first `stl-3d` product (price, thumbnail render, and listing copy — no code changes
needed there since the product type and checkout path are already shipped). If the
pipeline reveals gaps (e.g. Hunyuan3D output isn't manifold without extra repair
tooling), that finding is itself useful output — document it as a `model-builder`
kaizen task rather than treating it as pitch failure.

## Existing-work check

Closest existing work inspected: `projects/digital-storefront/product-types.yaml`
(confirms `stl-3d` is pre-approved but unused by any current catalog item — checked
`projects/digital-storefront/roadmap.yaml`, which has no STL-specific product task);
`projects/model-builder/roadmap.yaml` t-012 and `PROJECT-BRIEF.md`'s Reward Deck
section (confirms the GLB→repair→STL→print-readiness sequence is designed but
explicitly not yet run for real — "nothing is labeled STL or print-ready unless
those stages actually occurred"); `pinball-hero/roadmap.yaml`'s 3D-printed-parts
work (a different, retired, single-purpose project — its printable-parts scope
doesn't cover general character figurines and the project itself is retired per
`project-overrides.yaml`). No existing pitch, shipped feature, or roadmap task
proposes turning a Kind Robots character into a sellable printable figurine.
