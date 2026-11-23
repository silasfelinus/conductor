# Pitch: The Jellybeans page says how the hunt works
date: 2026-11-23
project-target: kr-arcade
expansion-kind: front-door
delivery-status: in-progress
status: awaiting-silas

## Delivered change
The signed-in Jellybeans page described a delightful quest; it now says to find hidden jellybeans, earn three per game, and sign in free to track them.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5654
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/45142660780
Verified: Locally: verifyFrontDoorPolish.test.ts requires 'sign in free' and forbids 'delightful quest'.
Art: not-required
Playable preview: https://kindrobots.org/achievements
Canonical roadmap: projects/kr-arcade/roadmap.yaml task t-156
Next step: Auto-merge (squash) is enabled on kind_robots#5654; it lands once required CI checks pass. Record merge_sha and checks: passed after it merges.

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
