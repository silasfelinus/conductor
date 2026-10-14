# Pitch: Arcade soundtrack briefs and gesture-safe mixer
date: 2026-10-14
project-target: kr-arcade
expansion-kind: audio system
delivery-status: shipped
status: awaiting-silas

## Delivered change
Typed soundtrack briefs for seven cabinets and a mixer that crossfades scenes, ducks music under stingers and falls back to oscillators until a track decodes. Cabinets gain a persisted volume slider.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/3681
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/38526984311
Verified: Merged PR's aggregate 'Contract verifiers' check run completed with conclusion success; main commit confirmed. Recorded music files are not yet produced; only the mixer, briefs and an admin-gated job queue shipped.
Art: not-required
Merge: 5ad7219e82c48fe2d699cab1ed801f1469d666b7

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
