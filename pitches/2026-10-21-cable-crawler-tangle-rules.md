# Pitch: Cable Crawler: Team Tangle and Tangle Race rules
date: 2026-10-21
project-target: kr-arcade
expansion-kind: multiplayer mode
delivery-status: in-progress
status: awaiting-silas

## Delivered change
Pure rules for two to four cables, shared-battery Team Tangle, sparks-based Tangle Race and harmless plug-against-plug bumps.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/4000
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/39611435592
Verified: 18 checks green after one re-run of a stuck TypeScript job; rules test prints ok. Merged but not wired into the game.
Art: not-required
Merge: 5dbbac335f7ab51bda43e0c0e700201bac95ea02
Next step: Seat 2-4 cables in the single-body cableCrawler.ts, read the players frames, add mode-select entries and set registry maxPlayers.

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
