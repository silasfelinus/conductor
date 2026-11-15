# Pitch: Front door: Slime City duel invite link preview
date: 2026-11-15
project-target: slime-city
expansion-kind: front-door
delivery-status: shipped
status: awaiting-silas

## Delivered change
Shared Slime City duel invite links previously had no social preview at all; the PvP page now carries its own meta and a code-drawn You have been challenged card.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5209
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/43696882768
Verified: verifyGameLinkPreview.test.ts passed locally and in CI; card rendered in Chromium at 1200x630 and checked by eye
Art: delivered
Merge: c24cef2ba52ed83a79c02f7f6e72500f7fbcfa90
Playable preview: https://kindrobots.org/play/slime-city-pvp
Art URL: https://kindrobots.org/slime-city-pvp/link-preview.webp
Canonical roadmap: projects/slime-city/roadmap.yaml task t-063

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
