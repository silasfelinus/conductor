# Coloring Book Production Model

This project produces three books in this order:

1. **Monster Recast** (`monster-recast`)
2. **Hollywood Recast** (`hollywood-recast`) — the title has no “2”
3. **Kind Robots** (`kind-robots`)

Do not use the old ambiguous `HR` shorthand for both recast books. Use `MR`, `HWR`,
and `KR` when a short prefix is unavoidable.

## Fixed book shape

Each book tracks exactly **36 interior illustration proposals**. The cover is separate
and does not consume one of the 36 slots.

Each proposal is intended to finish as a matched pair:

- one final color master
- one faithful black-and-white coloring-page master derived from the accepted color composition

A complete book therefore contains 36 proposal records and 72 final interior art files,
plus separate cover assets.

## Proposal ledger

Each book owns a `proposals.yaml` ledger. A proposal record keeps the creative and
production history together:

- slot, stable id, working title, and proposed **color** art prompt or prompt reference
- inspirations and exploratory candidates, including optional early BW studies
- accepted color and accepted black-and-white working files
- confirmed final-draft color and black-and-white files
- notes, provenance, and unresolved review questions

“Accepted” and “final” are deliberately different:

- **inspiration/candidate** means useful reference, not a production decision
- **accepted color** means Silas approved the composition, identity, pose, body, scene, and visual hook
- **accepted BW** means a faithful coloring-page counterpart was approved from that accepted color
- **final** means the revised, print-ready draft passed pair and quality checks
- **final pair** requires both final files and confirmation that they depict the same composition,
  identity, pose, and major scene details

Never silently promote a file because it exists in a directory. Never regenerate an
accepted composition from scratch merely because its counterpart or polish pass is missing.

## Color-first production loop

The canonical color queue is:

```text
projects/coloring-book/color-art-jobs.yaml
```

It contains all 108 proposals and marks accepted Monster Recast colors as `approved`.
Everything else begins as a pending color proposal ArtJob.

A normal Worker pass is **18 images**, approximately half a book—not one to six isolated
prompt edits. One pass may prepare, submit, retrieve, or review up to 18 items from the same
stage. The default queue order is book order, then slot order.

Run:

```bash
python scripts/coloring_proposal_status.py --check
python scripts/consume_coloring_book_color_art.py
```

The production stages are:

1. maintain 36 named color prompts for each book
2. submit pending color proposal ArtJobs in batches of 18
3. review rendered color proposals in batches of up to 18
4. record an accepted color master or revise and resubmit the color prompt
5. only after a color is accepted, derive a faithful BW coloring-page counterpart
6. create/review BW counterparts in batches of 18
7. revise and confirm final color and BW drafts
8. package only after all 36 final pairs exist

An early BW study may remain attached as inspiration, but it does not drive ongoing design
iterations and it must not outrank the accepted color master.

The production order is editorial priority, not permission to lose later-book ideas.
All three books may have complete prompts and queued color jobs while Monster Recast remains
the first book to finish.

## Guardrails

- Preserve accepted composition, body type, age, scars, anatomy, perspective, contact points,
  and visual hook when making a counterpart or revision.
- One file per image. No collage or contact sheet.
- Final color masters use strong clean contours and bounded color.
- Final BW masters are faithful line-art counterparts, not simplified redesigns.
- Keep prompt/model/job/source metadata.
- The designated Kind Robots logo proposal may use the supplied/canonical logo as a reference;
  other pages should not generate logos or readable text.
- Publishing, POD accounts or listings, production spend, and public Character release remain
  human-gated.
