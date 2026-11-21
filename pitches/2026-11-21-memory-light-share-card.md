# Pitch: Memory Dungeon shares a light title card
date: 2026-11-21
project-target: memory-dungeon
expansion-kind: share
delivery-status: shipped
status: awaiting-silas

## Delivered change
Memory Dungeon links shared a 643 KB full-size backdrop that chat apps skip; they now share a 1200px 205 KB card of the same title art, also used on the front-door directory.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5513
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/44907130373
Verified: Live og:image measured at 643088 bytes before; verifySharePreview.test.ts pins a 250 KB budget for committed share cards and forbids the media-volume fallback for this route. Live result pending the next Force Update.
Art: not-required
Merge: d142dd965e7e0244814746ed49f072dbbc9232b3
Playable preview: https://kindrobots.org/play/memory
Canonical roadmap: projects/memory-dungeon/roadmap.yaml task t-068

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
