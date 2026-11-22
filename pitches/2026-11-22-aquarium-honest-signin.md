# Pitch: Cthulhuquarium says playing needs a free sign-in
date: 2026-11-22
project-target: interface-vision
expansion-kind: front-door
delivery-status: shipped
status: awaiting-silas

## Delivered change
Cthulhuquarium links promised a coin-dropping aquarium without saying a tank needs an account; they now say browsing players' tanks is free and raising your own needs a free sign-in.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5580
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/45024768044
Verified: The in-page tutorial opens with "Sign in and Charlotte Fishmonger gives you your first creature"; verifyFrontDoorPolish.test.ts now requires "sign in" in the page description. Live result pending the next deploy.
Art: not-required
Merge: de1be6c6e1fff72cf66394bc4ef370b37eb31080
Playable preview: https://kindrobots.org/play/aquarium
Canonical roadmap: projects/interface-vision/roadmap.yaml task t-151

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
