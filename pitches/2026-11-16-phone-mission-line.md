# Pitch: Homepage: malaria mission line wraps on phones
date: 2026-11-16
project-target: interface-vision
expansion-kind: front-door
delivery-status: shipped
status: awaiting-silas

## Delivered change
The homepage line Free games, no ads, helping fund mosquito nets was cut off mid-word at phone width and now wraps so first visitors read the whole mission.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5248
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/43855819500
Verified: Observed truncation at 390px on production; verifyFrontDoorPolish.test.ts pins no-truncate; layout-contract passed
Art: not-required
Merge: 88b21a1b3703bfd4a46ba1886f65cef6f6633bd7
Playable preview: https://kindrobots.org/
Canonical roadmap: projects/interface-vision/roadmap.yaml task t-143

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
