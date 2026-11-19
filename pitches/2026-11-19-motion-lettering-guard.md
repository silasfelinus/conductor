# Pitch: Dead Air: motion prompts cannot ask for lettering
date: 2026-11-19
project-target: dead-air
expansion-kind: quality
delivery-status: shipped
status: awaiting-silas

## Delivered change
The lettering guard that keeps fake text out of stills now also rejects text, caption and subtitle words in motion prompts, after a GPU clip baked fake subtitles into a film.

## Evidence
PR: https://github.com/silasfelinus/conductor/pull/7614
Checks: https://github.com/silasfelinus/conductor/actions/runs/44500303522
Verified: test_motion_prompts_are_lettering_guarded_like_stills rejects a subtitle motion prompt; all 13 authored episodes still pass --dry-run
Art: not-required
Merge: ee47c246decc3b86fe068a08702d0a9564b17942
Canonical roadmap: projects/dead-air/roadmap.yaml task t-010

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
