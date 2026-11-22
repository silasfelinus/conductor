# Pitch: Memory Dungeon says what it is in one line
date: 2026-11-22
project-target: memory-dungeon
expansion-kind: share
delivery-status: shipped
status: awaiting-silas

## Delivered change
Memory Dungeon links shared a 250-character pitch ending in "claim creative rewards from the prompt and art modeller"; they now say it is a memory card dungeon crawl, free in the browser with no account.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5580
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/45024768044
Verified: Live og:description captured before the change (2026-11-22 PT sitemap audit of all 29 URLs); verifyFrontDoorPolish.test.ts section 5 caps it at 160 characters, forbids "modeller"/"roguelite" and requires "free". Live result pending the next deploy.
Art: not-required
Merge: de1be6c6e1fff72cf66394bc4ef370b37eb31080
Playable preview: https://kindrobots.org/play/memory
Canonical roadmap: projects/memory-dungeon/roadmap.yaml task t-068

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
