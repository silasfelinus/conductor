# Pitch: Not-found page offers a way back instead of jargon
date: 2026-11-17
project-target: interface-vision
expansion-kind: front-door
delivery-status: shipped
status: awaiting-silas

## Delivered change
The not-found panel said No Nuxt Content page was found with no exit; it now explains and links Play, Home and Support.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5279
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/44062384383
Verified: Contract test forbids the framework jargon and requires the three NuxtLinks; layout-contract one-header rule passes
Art: not-required
Merge: 7a2aca97524bb0672292f3ae6d23d68a050d8b56
Playable preview: https://kindrobots.org/no-such-page
Canonical roadmap: projects/interface-vision/roadmap.yaml task t-104

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
