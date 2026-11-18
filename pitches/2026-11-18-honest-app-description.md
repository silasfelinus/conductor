# Pitch: Home-screen install describes the site as it is today
date: 2026-11-18
project-target: interface-vision
expansion-kind: front-door
delivery-status: shipped
status: awaiting-silas

## Delivered change
The PWA manifest still called the site 'A friendly AI playground for humans and robots'; it now says free handmade games, illustrated stories and an art gallery, no ads, no account.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5309
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/44291475663
Verified: Live /manifest.webmanifest returned the outdated description; verifySharePreview.test.ts forbids it and requires the front-door wording
Art: not-required
Merge: 6407369ba92f549b4584f9d3d24191284101eb78
Playable preview: https://kindrobots.org/manifest.webmanifest
Canonical roadmap: projects/interface-vision/roadmap.yaml task t-151

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
