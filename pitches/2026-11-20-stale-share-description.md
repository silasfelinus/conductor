# Pitch: Share descriptions never borrow another page subtitle
date: 2026-11-20
project-target: interface-vision
expansion-kind: share
delivery-status: shipped
status: awaiting-silas

## Delivered change
The app shell fell back to the page store subtitle even when it described a different page, so dedicated pages could share Welcome to Kind Robots; the fallback is now guarded per route.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5416
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/44715055903
Verified: verifySharePreview.test.ts forbids the bare pageStore.subtitle fallback and requires the describesPath guard.
Art: not-required
Merge: 80196ac9ed4a836461033233232b773471d4d8c8
Playable preview: https://kindrobots.org/
Canonical roadmap: projects/interface-vision/roadmap.yaml task t-104

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
