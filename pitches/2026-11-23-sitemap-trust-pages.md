# Pitch: Who-made-this, privacy and sign-up pages are in the sitemap
date: 2026-11-23
project-target: interface-vision
expansion-kind: findability
delivery-status: shipped
status: awaiting-silas

## Delivered change
The public /silas, /privacy and /register pages were missing from sitemap.xml, so search engines were never told about them.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5654
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/45142660780
Verified: CI (Contract Tests run 45142660780) and locally: verifySharePreview.test.ts requires all three in the sitemap and backed by real content pages. Live result pending the next deploy.
Art: not-required
Merge: 77bb91d155562e81213e1177ed01168a64483c29
Playable preview: https://kindrobots.org/sitemap.xml
Canonical roadmap: projects/interface-vision/roadmap.yaml task t-144

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
