# Pitch: Glitch Garden: Prism beam powers and patch multiplier
date: 2026-10-21
project-target: kr-arcade
expansion-kind: arcade mechanic
delivery-status: shipped
status: awaiting-silas

## Delivered change
Blooms carry a colour and lend beams pink split, gold pierce, cyan freeze or violet homing, with a x1 to x5 patch multiplier shown in the HUD.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/4002
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/39612300733
Verified: 18 check runs passed incl. TypeScript and Contract shards 1-4; new Prism test and existing Glitch Garden test pass under tsx. Merged is not deployed; t-088 stays open for sprinklers, data-driven gardens and double-density sprites.
Art: not-required
Merge: 878dd1c58032a82707361695d03bfd05e0dcc89e

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
