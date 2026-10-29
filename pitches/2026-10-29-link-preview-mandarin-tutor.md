# Pitch: Front door: link preview for Mandarin Tutor
date: 2026-10-29
project-target: interface-vision
expansion-kind: front door link preview
delivery-status: shipped
status: awaiting-silas

## Delivered change
Shared links to the Mandarin Tutor now unfurl with a title and description instead of a bare URL.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/4445
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/40944468183
Verified: All 21 check runs on the final head passed (first two heads failed Prettier and the lint ratchet and were fixed before merge). Link-preview test logic also run locally. Merged is not deployed; unfurls not yet checked in a live crawler.
Art: not-required
Merge: aeb58c1a87a3a0ef68dc73bfeece7dbdefffe3a6

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
