# Pitch: Arcade share links: daily check now fails on a broken unfurl
date: 2026-11-18
project-target: kr-arcade
expansion-kind: share
delivery-status: shipped
status: awaiting-silas

## Delivered change
Live strict crawler check found all 34 cabinets unfurling as themselves for Facebook, Discord and Twitter, so the scheduled check now fails on any unfurl regression.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5309
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/44291475663
Verified: checkArcadeShareLive.ts --unfurl --strict-unfurl against kindrobots.org reported 34 cabinets, 0 missing title art, 0 unfurl problems; workflow strictness pinned in verifySharePreview.test.ts
Art: not-required
Merge: 6407369ba92f549b4584f9d3d24191284101eb78
Playable preview: https://kindrobots.org/play/arcade?game=battery-maze
Canonical roadmap: projects/kr-arcade/roadmap.yaml task t-171

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
