# Pitch: Register page says what a free account is for
date: 2026-11-20
project-target: interface-vision
expansion-kind: front-door
delivery-status: shipped
status: awaiting-silas

## Delivered change
The register page preview read Registration with a list of jargon like jellybean tracking and prompt retention; it now says Create a free account and that games stay free without one.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5416
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/44715055903
Verified: verifyFrontDoorPolish.test.ts pins the new title and forbids the old jargon in the description.
Art: not-required
Merge: 80196ac9ed4a836461033233232b773471d4d8c8
Playable preview: https://kindrobots.org/register
Canonical roadmap: projects/interface-vision/roadmap.yaml task t-105

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
