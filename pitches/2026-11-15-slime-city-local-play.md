# Pitch: Slime City: calm LOCAL PLAY instead of STORY SYNC ERROR
date: 2026-11-15
project-target: slime-city
expansion-kind: bug-fix
delivery-status: shipped
status: awaiting-silas

## Delivered change
Signed-in visitors outside the Slime City admin preview no longer see a red STORY SYNC ERROR badge; the lab plays and saves on their device with a neutral notice.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5209
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/43696882768
Verified: verifySlimeCityPreviewGate.test.ts, AccountBoundary and StorySave passed locally; full test:slime-city-lab contract shards passed in CI
Art: not-required
Merge: c24cef2ba52ed83a79c02f7f6e72500f7fbcfa90
Playable preview: https://kindrobots.org/play/slime-city
Canonical roadmap: projects/slime-city/roadmap.yaml task t-067

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
