# Pitch: Brick Bloom: ladybot ring guarding Vine Hall crates
date: 2026-10-21
project-target: kr-arcade
expansion-kind: arcade stage
delivery-status: in-progress
status: awaiting-silas

## Delivered change
Five orbiting ladybot dots shield a crate on Vine Hall walls 3b and 4b, scoring per pop with a bonus for the last one; module and test only.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/3999
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/39611320232
Verified: 18 checks green; ring module merged and tested but not yet wired into the cabinet, so nothing is visible in play.
Art: not-required
Merge: 0bc6c6a9654e90a5ab31436752633d6f67336f41
Next step: Wire the ring into utils/arcade/games/brickBloom.ts on the two Vine Hall walls, draw it, then Mister Mulch and the Tangle Rose.

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
