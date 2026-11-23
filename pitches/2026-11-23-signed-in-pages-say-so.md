# Pitch: Chats and Themes describe themselves plainly
date: 2026-11-23
project-target: interface-vision
expansion-kind: front-door
delivery-status: in-progress
status: awaiting-silas

## Delivered change
Chats claimed 'curated messages from across our digital domains' though it needs a sign-in; it now says so, and Themes drops filler copy.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5654
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/45142660780
Verified: Locally: verifyFrontDoorPolish.test.ts requires 'sign in free' on Chats and forbids the old filler on Themes.
Art: not-required
Playable preview: https://kindrobots.org/themes
Canonical roadmap: projects/interface-vision/roadmap.yaml task t-104
Next step: Auto-merge (squash) is enabled on kind_robots#5654; it lands once required CI checks pass. Record merge_sha and checks: passed after it merges.

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
