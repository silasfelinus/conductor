# Pitch: Live probe for hub URLs and honest 404s
date: 2026-11-17
project-target: interface-vision
expansion-kind: reliability
delivery-status: shipped
status: awaiting-silas

## Delivered change
A new read-only probe checks ten hub URLs redirect to loading pages and that unknown URLs answer 404 after each deploy.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5279
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/44062384383
Verified: node utils/scripts/checkFrontDoorRoutesLive.mjs against production before deploy: 11/11 problems reported, as expected
Art: not-required
Merge: 7a2aca97524bb0672292f3ae6d23d68a050d8b56
Playable preview: https://kindrobots.org/projects
Canonical roadmap: projects/interface-vision/roadmap.yaml task t-144

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
