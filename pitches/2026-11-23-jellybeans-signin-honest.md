# Pitch: The Jellybeans page says how the hunt works
date: 2026-11-23
project-target: kr-arcade
expansion-kind: front-door
delivery-status: shipped
status: awaiting-silas

## Delivered change
The signed-in Jellybeans page described a delightful quest; it now says to find hidden jellybeans, earn three per game, and sign in free to track them.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5654
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/45142660780
Verified: CI (Contract Tests run 45142660780) and locally: verifyFrontDoorPolish.test.ts requires 'sign in free' and forbids 'delightful quest'. Live result pending the next deploy.
Art: not-required
Merge: 77bb91d155562e81213e1177ed01168a64483c29
Playable preview: https://kindrobots.org/achievements
Canonical roadmap: projects/kr-arcade/roadmap.yaml task t-156

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
