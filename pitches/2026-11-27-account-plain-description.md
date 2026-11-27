# Pitch: Account drops "privacy and consent" jargon
date: 2026-11-27
project-target: interface-vision
expansion-kind: front-door
delivery-status: shipped
status: awaiting-silas

## Delivered change
/account described "tune privacy and consent"; it now says choose your privacy settings, pick which newsletter emails you get, and that a free sign-in opens it.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5992
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/46013025036
Verified: CI (Contract Tests run 46013025036, all checks green on the PR head) and locally: verifyFrontDoorPolish.test.ts section 10 pins it. Live result pending the next deploy.
Art: not-required
Merge: 406f4b812320f33b2db86b2f0ad904c2097aab66
Playable preview: https://kindrobots.org/account
Canonical roadmap: projects/interface-vision/roadmap.yaml task t-105

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
