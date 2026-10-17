# Pitch: Brick Bloom: pollen mites in the Seedling House
date: 2026-10-17
project-target: kr-arcade
expansion-kind: arcade enemy
delivery-status: shipped
status: awaiting-silas

## Delivered change
A line of three pollen mites sways down in Seedling House walls 2-9; ball contact pops them and clearing the line pays a petal chain.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/3801
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/39019893828
Verified: First head failed TypeScript (TS2339 in the new test); fixed and re-run, all 18 check runs green on the final head, squash merge confirmed merged 09:12Z. Merged is not deployed.
Art: not-required
Merge: b44ef3c3050fa79c2e2940962a7299fb696085d0
Playable preview: https://kindrobots.org/play/brick-bloom

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
