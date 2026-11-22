# Pitch: Zuzu Showdown's link preview describes the game
date: 2026-11-22
project-target: interface-vision
expansion-kind: share
delivery-status: shipped
status: awaiting-silas

## Delivered change
Zuzu Showdown shared only "Duels with Zuzu and friends."; it now names a 2D fighter with nine fighters, Story mode, versus and training, playable with keyboard, gamepad or touch.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5580
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/45024768044
Verified: Live og:description captured before the change; verifyGameLinkPreview length rules pass and verifyFrontDoorPolish.test.ts forbids the old line and requires "fighter". Live result pending the next deploy.
Art: not-required
Merge: de1be6c6e1fff72cf66394bc4ef370b37eb31080
Playable preview: https://kindrobots.org/play/zuzu-showdown
Canonical roadmap: projects/interface-vision/roadmap.yaml task t-105

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
