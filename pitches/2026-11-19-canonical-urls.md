# Pitch: Every page declares one canonical address
date: 2026-11-19
project-target: interface-vision
expansion-kind: front-door
delivery-status: shipped
status: awaiting-silas

## Delivered change
Live pages carried og:url but no canonical link, so /play aliases and ?game= deep links could be indexed separately; every page now declares its query-free canonical URL.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5340
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/44500398041
Verified: Live / /giving /about had no rel=canonical before the change; verifySharePreview.test.ts pins the app.vue canonical link and query/trailing-slash stripping
Art: not-required
Merge: 78cb32a14a141b26691782f4e582a21904524e9c
Playable preview: https://kindrobots.org/
Canonical roadmap: projects/interface-vision/roadmap.yaml task t-151

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
