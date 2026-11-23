# Pitch: The login page says what an account is for
date: 2026-11-23
project-target: interface-vision
expansion-kind: front-door
delivery-status: shipped
status: awaiting-silas

## Delivered change
The login page promised a 'suite of AI-enhanced tools'; it now says a free account saves game progress and art, and games stay free without one.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5654
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/45142660780
Verified: CI (Contract Tests run 45142660780) and locally: verifyFrontDoorPolish.test.ts forbids 'AI-enhanced'/'suite of' and requires 'free' and 'without one'. Live result pending the next deploy.
Art: not-required
Merge: 77bb91d155562e81213e1177ed01168a64483c29
Playable preview: https://kindrobots.org/login
Canonical roadmap: projects/interface-vision/roadmap.yaml task t-105

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
