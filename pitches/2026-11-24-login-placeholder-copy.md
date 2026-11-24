# Pitch: Login drops placeholder copy
date: 2026-11-24
project-target: interface-vision
expansion-kind: front-door
delivery-status: shipped
status: awaiting-silas

## Delivered change
The login page still showed the placeholder subtitle 'Login here' and tooltip 'login and registration link here'; it now welcomes visitors back and points to free sign-up.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5728
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/45360025161
Verified: CI (Contract Tests run 45360025161, all 12 checks green on ceb7afa) and locally: verifyFrontDoorPolish.test.ts section 7 pins it. Live result pending the next deploy.
Art: not-required
Merge: 98ef87d1aa86f08a89ea32e8ea9b4f1c4967dba7
Playable preview: https://kindrobots.org/login
Canonical roadmap: projects/interface-vision/roadmap.yaml task t-105

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
