# Pitch: Dreams tooltip says how a dream starts
date: 2026-11-28
project-target: interface-vision
expansion-kind: front-door
delivery-status: shipped
status: awaiting-silas

## Delivered change
/dreams header tooltip read "prompts, images, and chat bend the experience together"; it now says start a dream from a prompt or picture, then steer it with other visitors.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/6067
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/46132093166
Verified: CI (Contract Tests run 46132093166, all checks green on the PR head) and locally: verifyFrontDoorPolish.test.ts section 11 pins it. Live result pending the next deploy.
Art: not-required
Merge: 0a513b39a9a0bcfd6581ef474bd1f0d18645f63e
Playable preview: https://kindrobots.org/dreams
Canonical roadmap: projects/interface-vision/roadmap.yaml task t-145

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
