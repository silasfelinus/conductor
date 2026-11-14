# Pitch: Front door: Cthulhuquarium leaderboard link preview card
date: 2026-11-13
project-target: cthulhuquarium
expansion-kind: front door: link preview
delivery-status: shipped
status: awaiting-silas

## Delivered change
Shared Cthulhuquarium leaderboard links now unfurl with their own Top Keepers podium card instead of duplicating the browse page hero.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5135
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/43548818652
Verified: All 11 check runs on the final head completed green (TypeScript, layout contract, Changed-file Prettier, four contract shards); verifyGameLinkPreview and Prettier also run locally; every card rendered in headless Chromium and inspected. Merged is not deployed; live crawler unfurls not yet checked.
Art: delivered
Merge: 52df00cfe948c1ef4c967a95a4198ed58308a47f
Art URL: https://github.com/silasfelinus/kind_robots/blob/52df00cfe948c1ef4c967a95a4198ed58308a47f/public/aquarium-leaderboard/link-preview.webp

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
