# Pitch: Wallet tooltip explains karma and mana
date: 2026-11-28
project-target: interface-vision
expansion-kind: front-door
delivery-status: shipped
status: awaiting-silas

## Delivered change
/wallet header tooltip named karma and mana balances with no meaning; it now says karma is earned by helping others and mana is what you spend to make AI art.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/6067
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/46132093166
Verified: CI (Contract Tests run 46132093166, all checks green on the PR head) and locally: verifyFrontDoorPolish.test.ts section 11 pins it. Live result pending the next deploy.
Art: not-required
Merge: 0a513b39a9a0bcfd6581ef474bd1f0d18645f63e
Playable preview: https://kindrobots.org/wallet
Canonical roadmap: projects/interface-vision/roadmap.yaml task t-104

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
