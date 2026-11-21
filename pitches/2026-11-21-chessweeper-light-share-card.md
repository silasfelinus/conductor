# Pitch: Chessweeper shares a light title card
date: 2026-11-21
project-target: chessweeper
expansion-kind: share
delivery-status: shipped
status: awaiting-silas

## Delivered change
Chessweeper links shared a 582 KB highlight image that chat apps skip; they now share a 1200px 175 KB card of the same title art, also used on the front-door directory.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5513
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/44907130373
Verified: Live og:image measured at 582348 bytes before; the new card was viewed with its title intact and the share-preview contract checks its size. Live result pending the next Force Update.
Art: not-required
Merge: d142dd965e7e0244814746ed49f072dbbc9232b3
Playable preview: https://kindrobots.org/play/chessweeper
Canonical roadmap: projects/chessweeper/roadmap.yaml task t-003

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
