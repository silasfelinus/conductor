# Pitch: Arcade share links: daily phone and tablet cold-open probe
date: 2026-11-18
project-target: kr-arcade
expansion-kind: share
delivery-status: shipped
status: awaiting-silas

## Delivered change
Every showcase cabinet link is now opened daily in a fresh browser at phone and tablet size, failing on login walls, page errors or a lost way back.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5309
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/44291475663
Verified: checkArcadeColdOpenLive.mjs run live from this session reported 22/22 showcase cold opens clean on kindrobots.org; the new workflow job is pinned in verifySharePreview.test.ts
Art: not-required
Merge: 6407369ba92f549b4584f9d3d24191284101eb78
Playable preview: https://kindrobots.org/play/arcade?game=seed-lander
Canonical roadmap: projects/kr-arcade/roadmap.yaml task t-169

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
