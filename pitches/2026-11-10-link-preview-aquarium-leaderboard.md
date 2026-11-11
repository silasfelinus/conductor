# Pitch: Front door: link preview for the Cthulhuquarium leaderboard
date: 2026-11-10
project-target: cthulhuquarium
expansion-kind: front door: link preview
delivery-status: shipped
status: awaiting-silas

## Delivered change
The public species leaderboard now unfurls with a titled preview card and the Cthulhuquarium hero art when shared.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/4976
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/42956067744
Verified: All 13 check runs on the final head completed (12 success, browser-contract intentionally skipped), including TypeScript, layout contract and four contract shards; test:game-link-preview, vue-tsc, eslint and Prettier also run locally. Merged is not deployed; live crawler unfurls not yet checked.
Art: not-required
Merge: 08afc1156d68e957e29d958d98a4a0684fbc0de2

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
