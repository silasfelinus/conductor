# Pitch: Art gallery shares a light card
date: 2026-11-21
project-target: interface-vision
expansion-kind: share
delivery-status: shipped
status: awaiting-silas

## Delivered change
The Art gallery and studio shared a 310 KB image; it now shares a 175 KB card of the same art, and the Emperor of Dust and Zuzu Showdown fallbacks now match their light cards.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5513
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/44907130373
Verified: Live og:image measured at 309736 bytes before; verifySharePreview.test.ts checks every committed share card against the 250 KB budget. Live result pending the next Force Update.
Art: not-required
Merge: d142dd965e7e0244814746ed49f072dbbc9232b3
Playable preview: https://kindrobots.org/art
Canonical roadmap: projects/interface-vision/roadmap.yaml task t-144

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
