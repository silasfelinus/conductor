# Pitch: Chessweeper and The Ruler Is Hooked share with their own card
date: 2026-11-20
project-target: interface-vision
expansion-kind: share
delivery-status: shipped
status: awaiting-silas

## Delivered change
Links to Chessweeper shared as Welcome to Kind Robots and The Ruler Is Hooked as Ruler Hooked on the generic arcade splash; both now share their own title, blurb and art and appear in the sitemap.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5416
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/44715055903
Verified: Live og:title/og:description captured before the change; verifySharePreview.test.ts pins both preview titles and sitemap coverage.
Art: not-required
Merge: 80196ac9ed4a836461033233232b773471d4d8c8
Playable preview: https://kindrobots.org/play/chessweeper
Canonical roadmap: projects/interface-vision/roadmap.yaml task t-151

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
