# Pitch: Seed Lander: Tandem and Relay pod rules with medal tiers
date: 2026-10-21
project-target: kr-arcade
expansion-kind: multiplayer mode
delivery-status: in-progress
status: awaiting-silas

## Delivered change
Pure rules for a shared cargo hold, a double-plant bonus, Relay handoff between pods and crew medal tiers against par.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/4003
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/39613621578
Verified: 18 checks green; Tandem test prints ok. Merged but the cabinet is not wired to it.
Art: not-required
Merge: dfd57a6ca11b54c5c06d911d16d378ed65183501
Next step: Wire two pods into seedLander.ts, set registry maxPlayers 2 and draw the medal boards.

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
