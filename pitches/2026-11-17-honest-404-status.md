# Pitch: Unknown links return a real 404 kept out of search
date: 2026-11-17
project-target: interface-vision
expansion-kind: front-door
delivery-status: shipped
status: awaiting-silas

## Delivered change
Every mistyped or stale link answered HTTP 200 with the generic site title; it now returns 404, titled Page not found, noindex.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5279
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/44062384383
Verified: checkFrontDoorRoutesLive.mjs found a nonsense URL answering 200 on production; contract test asserts SSR setResponseStatus 404 and noindex
Art: not-required
Merge: 7a2aca97524bb0672292f3ae6d23d68a050d8b56
Playable preview: https://kindrobots.org/no-such-page
Canonical roadmap: projects/interface-vision/roadmap.yaml task t-151

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
