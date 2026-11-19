# Pitch: Search results can name the site Kind Robots
date: 2026-11-19
project-target: interface-vision
expansion-kind: front-door
delivery-status: shipped
status: awaiting-silas

## Delivered change
The home page now emits schema.org WebSite structured data so search engines label results with the site name Kind Robots instead of guessing from the domain.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5340
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/44500398041
Verified: buildWebsiteJsonLd name/url and the home-only emission pinned in verifySharePreview.test.ts; live rich-results test not yet run after deploy
Art: not-required
Merge: 78cb32a14a141b26691782f4e582a21904524e9c
Playable preview: https://kindrobots.org/
Canonical roadmap: projects/interface-vision/roadmap.yaml task t-105

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
