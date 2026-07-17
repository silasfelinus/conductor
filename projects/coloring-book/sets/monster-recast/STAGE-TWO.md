# Monster Recast — Production Stage

This file preserves the useful handoff from closed GitHub issue #414. The canonical
execution task is now `coloring-book/t-022`, and the canonical per-page production
state is `proposals.yaml`.

Read `../../PRODUCTION-MODEL.md` first.

## Book contract

Monster Recast is book one. It has exactly 36 interior proposal slots and a separate
cover. Every proposal aims to finish with:

- one accepted and then confirmed final color master
- one accepted and then confirmed final black-and-white master
- a faithful pair relationship: same composition, identity, pose, anatomy, and major
  scene details

A file in `approved/` is an approved **working base**, not automatically a final draft.

## Current migration snapshot

The dated July 12 handoff recorded:

- 27 WebP files in `approved/`
- 18 represented concepts
- 9 complete color/BW working pairs
- 8 BW-only working bases
- 1 color-only working base

Run both checks before production:

```bash
python scripts/coloring_approved_status.py --check
python scripts/coloring_proposal_status.py --check
```

The filesystem scan reports what exists. `proposals.yaml` records what each file means.
Do not infer acceptance or final status merely from directory presence.

## Immediate next action

Reconcile every physical file in `approved/` into the matching proposal record:

- preserve exact filenames and record aliases/duplicates instead of silently renaming
- distinguish inspiration/candidate, accepted working file, and confirmed final file
- verify the provisional `masked-countess` mapping rather than assuming it is `mr-018`
- preserve the three explicitly accepted legacy pairs already seeded in the ledger
- clear `inventory_snapshot.requires_directory_reconciliation` only when the per-file
  mapping is complete

After reconciliation, `t-022` advances a small batch at a time. It may fill prompts,
attach inspiration, generate or curate candidates, record accepted files, create a
faithful missing counterpart, or confirm final drafts. It does not wait for unrelated
exploration before improving an accepted base.

## The Ticking Captain

`mr-035`, **The Ticking Captain**, is now a numbered proposal in `proposals.yaml`.

A formidable older woman pirate captain with a weathered, powerful body and an
original articulated compass-and-chronometer hook is pursued by a vast clockwork
marine predator whose brass gills tick like a ship chronometer. The commercial version
requires an original captain identity, ship, costume system, prosthetic mechanism,
time curse, and marine species.

Do not use a Disney-specific likeness, familiar red-coat design, feathered hat,
crocodile design, typography, supporting characters, or exact scene recreation.

## Completion

Monster Recast production is complete when all 36 proposal records have confirmed
final color and BW files. Then `t-022` stops recurring and `t-025` owns packaging and
kind_robots registration. Publishing, POD accounts/listings, spend, and public
Character release remain human-gated.
