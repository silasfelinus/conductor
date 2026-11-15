# Pitch: Front door: Space Couch link preview card
date: 2026-11-15
project-target: game-of-captains
expansion-kind: front-door
delivery-status: shipped
status: awaiting-silas

## Delivered change
Shared Space Couch links now unfurl with a designed titled card built from the red-sofa bridge art instead of an untitled splash image.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5209
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/43696882768
Verified: verifyGameLinkPreview.test.ts passed locally and in CI; card rendered in Chromium at 1200x630 and checked by eye
Art: delivered
Merge: c24cef2ba52ed83a79c02f7f6e72500f7fbcfa90
Playable preview: https://kindrobots.org/play/game-of-captains
Art URL: https://kindrobots.org/game-of-captains/link-preview.webp
Canonical roadmap: projects/game-of-captains/roadmap.yaml task t-041

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
