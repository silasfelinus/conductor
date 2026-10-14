# Pitch: In-game art style picker and description beside choices
date: 2026-10-14
project-target: shifting-desks
expansion-kind: gameplay UI
delivery-status: shipped
status: awaiting-silas

## Delivered change
An Art button with current-style thumbnail opens the picture picker mid-game and repaints every card immediately. From tablet width the card description sits above the choices; phones keep it on the card.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/3683
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/38530779948
Verified: Merged PR's head-commit 'Shifting Desks gameplay contract' run completed success, as did the other PR contract workflows listed for that head; main commit confirmed.
Art: not-required
Merge: f0501ce3bddb2941ddb7a63c7361fa72a78eb206

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
