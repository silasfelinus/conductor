# Pitch: Guessable contact, help and shop URLs reach real pages
date: 2026-11-20
project-target: interface-vision
expansion-kind: front-door
delivery-status: shipped
status: awaiting-silas

## Delivered change
Eleven URLs a first-time visitor might type, such as /contact, /help and /gallery, returned 404; each now redirects to the matching About, Art, Sanctuary or Giving page.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5416
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/44715055903
Verified: Live curl showed 404 for all eleven before the change; verifyFrontDoorRoutes.test.ts checks each target is a real tab or page and no alias shadows one. Live redirects not yet re-checked after deploy.
Art: not-required
Merge: 80196ac9ed4a836461033233232b773471d4d8c8
Playable preview: https://kindrobots.org/contact
Canonical roadmap: projects/interface-vision/roadmap.yaml task t-144

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
