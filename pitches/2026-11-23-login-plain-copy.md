# Pitch: The login page says what an account is for
date: 2026-11-23
project-target: interface-vision
expansion-kind: front-door
delivery-status: in-progress
status: awaiting-silas

## Delivered change
The login page promised a 'suite of AI-enhanced tools'; it now says a free account saves game progress and art, and games stay free without one.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5654
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/45142660780
Verified: Locally: verifyFrontDoorPolish.test.ts forbids 'AI-enhanced'/'suite of' and requires 'free' and 'without one'.
Art: not-required
Playable preview: https://kindrobots.org/login
Canonical roadmap: projects/interface-vision/roadmap.yaml task t-105
Next step: Auto-merge (squash) is enabled on kind_robots#5654; it lands once required CI checks pass. Record merge_sha and checks: passed after it merges.

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
