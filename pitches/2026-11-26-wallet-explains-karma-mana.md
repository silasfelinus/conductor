# Pitch: Wallet explains karma and mana
date: 2026-11-26
project-target: interface-vision
expansion-kind: front-door
delivery-status: shipped
status: awaiting-silas

## Delivered change
/wallet listed "karma balance, mana balance" with no meaning; it now explains karma, says mana is the budget you spend to make AI art, and notes a free account opens it.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5887
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/45788017303
Verified: CI (Contract Tests run 45788017303, all 12 checks green on the PR head) and locally: verifyFrontDoorPolish.test.ts section 9 pins it. Live result pending the next deploy.
Art: not-required
Merge: 2c4d1405eca0b3480d4fdec5b862b898f4840aba
Playable preview: https://kindrobots.org/wallet
Canonical roadmap: projects/interface-vision/roadmap.yaml task t-105

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
