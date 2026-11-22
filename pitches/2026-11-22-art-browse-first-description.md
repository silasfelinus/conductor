# Pitch: The Art page leads with what a visitor can do
date: 2026-11-22
project-target: interface-vision
expansion-kind: front-door
delivery-status: shipped
status: awaiting-silas

## Delivered change
The /art page shared an instruction, "Generate new images first"; it now says visitors can browse the robot-made gallery free with no account and sign in free to make their own.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5580
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/45024768044
Verified: Live og:description captured before the change; verifyFrontDoorPolish.test.ts forbids a leading "Generate" and requires the sign-in wording. Live result pending the next deploy.
Art: not-required
Merge: de1be6c6e1fff72cf66394bc4ef370b37eb31080
Playable preview: https://kindrobots.org/art
Canonical roadmap: projects/interface-vision/roadmap.yaml task t-144

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
