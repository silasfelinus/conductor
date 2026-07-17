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
- one faithful black-and-white coloring-page master

A complete book therefore contains 36 proposal records and 72 final interior art files,
plus separate cover assets.

## Proposal ledger

Each book owns a `proposals.yaml` ledger. A proposal record keeps the creative and
production history together:

- slot, stable id, working title, and proposed art prompt or prompt reference
- inspirations and exploratory candidates
- accepted color and accepted black-and-white working files
- confirmed final-draft color and black-and-white files
- notes, provenance, and unresolved review questions

“Accepted” and “final” are deliberately different:

- **inspiration/candidate** means useful reference, not a production decision
- **accepted** means Silas approved that file as the working composition or counterpart
- **final** means the revised, print-ready draft passed the pair and quality checks
- **final pair** requires both final files and confirmation that they depict the same
  composition, identity, pose, and major scene details

Never silently promote a file because it exists in a directory. Never regenerate an
accepted composition from scratch merely because its counterpart or polish pass is missing.

## Frictionless production loop

Run:

```bash
python scripts/coloring_proposal_status.py --check
```

The report identifies structural problems, progress totals, and the next incomplete action
for each book. A normal Worker pass should advance a small, reviewable batch rather than
attempting an entire book:

1. reconcile discovered files into the ledger
2. fill a missing proposal title or prompt
3. attach inspirations or generate a missing candidate
4. record an accepted color or BW working file
5. create the missing faithful counterpart
6. revise and confirm final color and BW drafts
7. package only after all 36 final pairs exist

The production order is editorial priority, not permission to lose later-book ideas.
Hollywood Recast and Kind Robots may collect proposals and inspirations while Monster
Recast is in production, but final production attention stays on the earliest unfinished
book.

## Guardrails

- Preserve accepted composition, body type, age, scars, anatomy, perspective, contact
  points, and visual hook when making a counterpart or revision.
- One file per image. No collage or contact sheet.
- Final color masters use strong clean contours and bounded color.
- Final BW masters are faithful line-art counterparts, not simplified redesigns.
- Keep prompt/model/job/source metadata.
- Publishing, POD accounts or listings, production spend, and public Character release
  remain human-gated.
