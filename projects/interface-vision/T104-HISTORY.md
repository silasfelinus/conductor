# interface-vision/t-104 — slice history archive

This file is the archaeology index for interface-vision/t-104, the recurring "drive live
front-end consistency onto shared kr-* components and composition rules" umbrella.

Slices 1–234 accumulated their progress notes directly in the task's `note:` field in
`roadmap.yaml`, growing it to roughly 395KB. By slice 234 that single field was the
dominant contributor pushing the whole Kind-Robots projection snapshot
(`scripts/sync_kind_robots_projection.py`) to 4,000,134 bytes against its 4,000,000-byte
transport limit — failing `tests/test_sync_kind_robots_projection.py` and
`scripts/sync_projects.py` in CI. Discovered and fixed while closing out slice 234
(conductor PR #4117, 2026-09-11).

The complete verbose slice-by-slice history through slice 234 is permanently available at
Conductor commit
[`647b18a5fb24378a168583ccb8ac461916aef4ca`](https://github.com/silasfelinus/conductor/blob/647b18a5fb24378a168583ccb8ac461916aef4ca/projects/interface-vision/roadmap.yaml)
(search that file for `id: t-104`). Do not restore that text into the live roadmap; use it
when you need to know exactly which class/primitive/file a specific past slice touched.

## What's established (as of slice 234)

Primitive families closed so far: `kr-container`/`kr-container-wide`, `kr-panel*`
(including `-muted`/`-tint` size variants), `kr-icon-*` (the bare colored/sizeless
glyph pool, all sizes), `kr-img-cover`, `kr-input`/`kr-input-muted`/`kr-input-sm`/
`kr-input-xs`, `kr-select-sm`/`kr-select-muted`, `kr-checkbox-primary-sm`,
`kr-textarea`/`kr-textarea-muted`, `kr-btn-outline-xs`, and more. `assets/css/
tailwind.css`'s `@layer components` block in kind_robots is the authoritative current
list — it stays accurate even as this roadmap note history is trimmed; this archive is
provenance, not the source of truth for what exists.

## Kaizen for the next slice

Both DaisyUI form-control candidates named in slice 233's kaizen note (`kr-input-xs`,
`kr-select-muted`) are now closed as of slice 234. A fresh full-repo class-frequency
survey (outside the families listed above) is needed to find the next target.

## Slice 270 (this session)

Fresh full-repo class-frequency survey outside every now-closed family (kr-spinner-*,
kr-input-*, kr-btn-*, kr-badge-*, kr-icon-*, kr-loading-*, kr-text-error-xs) found
`text-error text-sm` -- the `-sm` sibling of `.kr-text-error-xs` -- at 10 exact
occurrences across 8 files, plus 18 subset-match occurrences across 16 more files
carrying extra background/border/padding/layout wrapper tokens around the same
error-caption role. Opened `.kr-text-error-sm` and migrated all 28 occurrences across
23 files via a new codemod (`kr_text_error_sm_codemod.py`). No color/behavior/API/
schema/route/geometry change. vue-tsc, eslint (3 pre-existing unrelated errors
confirmed via git stash), test:layout-contract (0 new violations), test:kr-class-coverage
(OK), a full production build, and prettier drift on 11 files confirmed pre-existing via
git stash -- all clean before opening the kind_robots PR.

Slice 270 merged as silasfelinus/kind_robots#2716 (text-error text-sm -> kr-text-error-sm),
all 51 kind_robots PR checks green before merging. Return the recurring consistency
umbrella to ready for the next bounded slice. Kaizen for the next slice: run a fresh
full-repo class-frequency survey (`kr_class_frequency_survey.py`) outside every now-closed
family to pick the next target -- no specific candidate queued.

## For future slices: keep the live note short

Append each slice's progress to this file's own history (or a dated section below),
**not** back into `roadmap.yaml`'s `note:` field — that is exactly the growth pattern
that caused the payload-limit failure this file exists to fix. Keep the roadmap task's
`note:` field to a short "what's established + what's next" pointer, updated in place
rather than grown.
