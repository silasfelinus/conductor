# Pitch: Bots page drops the promptbots jargon
date: 2026-11-24
project-target: interface-vision
expansion-kind: front-door
delivery-status: shipped
status: awaiting-silas

## Delivered change
The /bots page described itself as 'View the many promptbots'; it now says meet the chatbots, each with its own personality, and pick one to talk to.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5728
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/45360025161
Verified: CI (Contract Tests run 45360025161, all 12 checks green on ceb7afa) and locally: verifyFrontDoorPolish.test.ts section 7 pins it. Live result pending the next deploy.
Art: not-required
Merge: 98ef87d1aa86f08a89ea32e8ea9b4f1c4967dba7
Playable preview: https://kindrobots.org/bots
Canonical roadmap: projects/interface-vision/roadmap.yaml task t-104

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
