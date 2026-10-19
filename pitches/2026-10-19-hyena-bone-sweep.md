# Pitch: Zuzu Showdown: Hyena Matriarch gets Bone Sweep
date: 2026-10-19
project-target: zuzu-showdown
expansion-kind: fighter move
delivery-status: shipped
status: awaiting-silas

## Delivered change
The Hyena Matriarch gains Bone Sweep (DP+K), a low sweep that knocks a standing opponent down, with input-map and hit/knockdown tests.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/3859
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/39226456644
Verified: 17 check runs passed; Hyena and related verifiers pass. The conductor fighters.yaml mirror was not updated. Merged is not deployed.
Art: blocked
Merge: 19de0353f82de53dfaa21218266e2aead9fe5008

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
