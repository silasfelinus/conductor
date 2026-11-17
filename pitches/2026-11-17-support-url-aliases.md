# Pitch: Guessable support and shop URLs reach giving and the gift shop
date: 2026-11-17
project-target: interface-vision
expansion-kind: support
delivery-status: shipped
status: awaiting-silas

## Delivered change
Visitors typing /donate, /give, /support, /shop or /giftshop hit soft 404s; they now land on the giving and gift shop tabs.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5279
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/44062384383
Verified: Contract test checks every alias target is a real channel tab, content page or Vue page and shadows nothing
Art: not-required
Merge: 7a2aca97524bb0672292f3ae6d23d68a050d8b56
Playable preview: https://kindrobots.org/donate
Canonical roadmap: projects/interface-vision/roadmap.yaml task t-143

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
