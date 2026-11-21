# Pitch: The site map says what it is when shared
date: 2026-11-21
project-target: interface-vision
expansion-kind: front-door
delivery-status: shipped
status: awaiting-silas

## Delivered change
The /navigation page shared as All roads lead to here, your central hub; it now says every Kind Robots game, story and studio is on one map, free with no account.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5513
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/44907130373
Verified: Live og:description captured before the change; verifySharePreview.test.ts forbids the old line and pins the new description. Live result pending the next Force Update.
Art: not-required
Merge: d142dd965e7e0244814746ed49f072dbbc9232b3
Playable preview: https://kindrobots.org/navigation
Canonical roadmap: projects/interface-vision/roadmap.yaml task t-105

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
