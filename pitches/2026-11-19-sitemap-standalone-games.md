# Pitch: Sitemap lists Ghost Trail and Sliding Tile Gallery
date: 2026-11-19
project-target: interface-vision
expansion-kind: front-door
delivery-status: shipped
status: awaiting-silas

## Delivered change
Two public arcade games with their own pages and link previews were missing from sitemap.xml, so search engines were never told they exist; both are now listed.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5340
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/44500398041
Verified: Live /play/zuzu-ghost-trail and /play/sliding-tile-gallery return 200 but were absent from the live sitemap; contract requires each listed route to have a page and an arcade tab and forbids duplicate URLs
Art: not-required
Merge: 78cb32a14a141b26691782f4e582a21904524e9c
Playable preview: https://kindrobots.org/sitemap.xml
Canonical roadmap: projects/interface-vision/roadmap.yaml task t-144

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
