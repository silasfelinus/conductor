# Pitch: Tab titles: every page names Kind Robots
date: 2026-11-18
project-target: interface-vision
expansion-kind: front-door
delivery-status: shipped
status: awaiting-silas

## Delivered change
Content pages such as Storybook, Memory Dungeon and Support showed bare tab titles with no site name; every tab, bookmark and search result now reads '<page> | Kind Robots'.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5309
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/44291475663
Verified: Live production titles checked before the change (Storybook, Navigation, Support, Memory Dungeon lacked the site name); siteTabTitle cases and the app.vue titleTemplate pinned in verifySharePreview.test.ts
Art: not-required
Merge: 6407369ba92f549b4584f9d3d24191284101eb78
Playable preview: https://kindrobots.org/storybook
Canonical roadmap: projects/interface-vision/roadmap.yaml task t-104

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
