# Pitch: Slime City, Monstrique and Hybridizer are in the sitemap
date: 2026-11-21
project-target: interface-vision
expansion-kind: findability
delivery-status: shipped
status: awaiting-silas

## Delivered change
Three public games with their own page, arcade tab and link preview were missing from the sitemap, so search engines were never told they exist; all three are now listed.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5513
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/44907130373
Verified: Live /sitemap.xml had 26 URLs without them; verifySharePreview.test.ts now requires every arcade tab backed by a play page to be in the sitemap. Live result pending the next Force Update.
Art: not-required
Merge: d142dd965e7e0244814746ed49f072dbbc9232b3
Playable preview: https://kindrobots.org/sitemap.xml
Canonical roadmap: projects/interface-vision/roadmap.yaml task t-151

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
