# Pitch: Stories says what it is
date: 2026-11-24
project-target: interface-vision
expansion-kind: front-door
delivery-status: shipped
status: awaiting-silas

## Delivered change
The /stories page linked from the home page read 'A surreal odyssey powered by ChatGPT'; it now says you pick a story scenario and turn it into an illustrated Storybook story.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5728
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/45360025161
Verified: CI (Contract Tests run 45360025161, all 12 checks green on ceb7afa) and locally: verifyFrontDoorPolish.test.ts section 7 pins it. Live result pending the next deploy.
Art: not-required
Merge: 98ef87d1aa86f08a89ea32e8ea9b4f1c4967dba7
Playable preview: https://kindrobots.org/stories
Canonical roadmap: projects/interface-vision/roadmap.yaml task t-151

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
