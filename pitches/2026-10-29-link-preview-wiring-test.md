# Pitch: Front door: test that every previewed page is wired
date: 2026-10-29
project-target: interface-vision
expansion-kind: test hardening
delivery-status: shipped
status: awaiting-silas

## Delivered change
Adds an optional path to previews plus a test failing when a previewed page does not call its preview meta.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/4445
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/40944468183
Verified: All 21 check runs on the final head passed (first two heads failed Prettier and the lint ratchet and were fixed before merge). Link-preview test logic also run locally. Merged is not deployed; unfurls not yet checked in a live crawler.
Art: not-required
Merge: aeb58c1a87a3a0ef68dc73bfeece7dbdefffe3a6

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
