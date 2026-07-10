---
slug: monster-recast
title: Monster Recast
type: coloring-book
status: approved
priority: high
created: 2026-07-10
home_set: projects/coloring-book/sets/monster-recast/
built_pr: null
---

## The idea
The first coloring book: classic horror and sci-fi movie-monster lineages recast
through gender, presentation, body, age, scale, and theatrical framing — camp and
queer-positive while keeping the menace and monstrosity that make horror work.
Progressive teen horror, ~PG-13 (per the home README; NOT all-ages). Original
characters evoking archetypes — never reproducing protected designs. Silas named
and approved this concept directly (2026-07-10 session) and has since expanded and
steered it through direct commits.

## Book shape
No longer locked at 28 pages: a 34-concept homage pool plus six group-page seeds,
targeting 28–32 solo/scene concepts and 4–6 ensemble pages (32–38 illustrated
interior pages) plus a full-color cover. Rank the pool after rough studies; may
split into volumes. `homage-concepts.yaml` is the authoritative pool. Full plan in
the home set.

## Style direction
Canonical paired-master workflow per `sets/monster-recast/STYLE-GUIDE.md`:
colored graphic master first (thick black linework, flat bounded color), then a
faithful black-and-white coloring-page conversion preserving pose, anatomy,
identity, and hook.

## Production state
Design/concept stage DONE and expanded (coloring-book t-012 + Silas's pool
expansion, 2026-07-10). Three approved master pairs already exist (Frieda
Krueger, TV Boy, Masking Up — see `approved/manifest.yaml`, the source of truth
for confirmed approvals). Remaining stages map to coloring-book roadmap tasks —
an idler day advances whichever is next:
1. Concept-art candidates from the homage pool (t-007)
2. Selection + design finalization (t-013)
3. kind_robots Character collection (t-014)
4. Coloring-page conversion (t-015)
5. Digital + print-ready package assembly (t-016), then PAUSE — publishing/POD
   stay hard-gated.
MANDATORY before any set work: run `python scripts/coloring_approved_status.py
--check`. Approved designs are never regenerated for production; the exploratory
queue continues unchanged. Follow the home project's specs and update BOTH the
coloring-book task status and this Build log. If the Worker is already actively
building these tasks through normal priority, the idler picks a different queued
creation instead of double-claiming — one owner per task, always.

## Notes from Silas
- (leave notes here — agents fold them in before building and never edit this section)

## Build log
- 2026-07-10 | scheduler card created; design stage already complete in home project (coloring-book t-012)
- 2026-07-10 | card synced to home-set reality: concept pool expanded to 34 (README "concept-expanded"), colored-master-first STYLE-GUIDE adopted, approved manifest + preflight requirement recorded, 3 approved pairs (Frieda Krueger, TV Boy, Masking Up), t-016 assembly stage added
