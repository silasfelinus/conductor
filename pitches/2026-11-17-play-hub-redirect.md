# Pitch: Front door: kindrobots.org/play opens the arcade
date: 2026-11-17
project-target: kr-arcade
expansion-kind: front-door
delivery-status: shipped
status: awaiting-silas

## Delivered change
Typing kindrobots.org/play or /games showed a bare Page not found panel; both now redirect to the arcade hall.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5279
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/44062384383
Verified: Live probe found /play and /games answering HTTP 200 soft 404s; verifyFrontDoorRoutes.test.ts pins the 302 targets in contract shard 4
Art: not-required
Merge: 7a2aca97524bb0672292f3ae6d23d68a050d8b56
Playable preview: https://kindrobots.org/play
Canonical roadmap: projects/kr-arcade/roadmap.yaml task t-169

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
