# Pitch: Sanctuary lists what it holds
date: 2026-11-25
project-target: interface-vision
expansion-kind: findability
delivery-status: shipped
status: awaiting-silas

## Delivered change
The /sanctuary page listed "mana" with no context; it now names the gift shop, forum, mana purse explained as the AI-art budget, and Silas's novel.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5811
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/45580005566
Verified: CI (Contract Tests run 45580005566, all 12 checks green on the PR head) and locally: verifyFrontDoorPolish.test.ts section 8 pins it. Live result pending the next deploy.
Art: not-required
Merge: 7bf856576937e6fd62194bac3fe8bfad1e482c4c
Playable preview: https://kindrobots.org/sanctuary
Canonical roadmap: projects/interface-vision/roadmap.yaml task t-144

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
