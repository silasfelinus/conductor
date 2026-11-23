# Pitch: The 404 page says Page not found
date: 2026-11-23
project-target: interface-vision
expansion-kind: front-door
delivery-status: in-progress
status: awaiting-silas

## Delivered change
A visitor who hit a missing page saw a browser tab reading 'Direction | Kind Robots'; it now reads 'Page not found' and links the site map.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5654
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/45142660780
Verified: Locally: verifyFrontDoorPolish.test.ts section 6 pins the title and the /navigation link; verifyNoShadowedContentRoutes passes.
Art: not-required
Playable preview: https://kindrobots.org/this-page-does-not-exist
Canonical roadmap: projects/interface-vision/roadmap.yaml task t-151
Next step: Auto-merge (squash) is enabled on kind_robots#5654; it lands once required CI checks pass. Record merge_sha and checks: passed after it merges.

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
