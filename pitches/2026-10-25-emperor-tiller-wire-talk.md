# Pitch: Emperor of Dust: Tiller exile talk, The Wire That Still Answers
date: 2026-10-25
project-target: emperor-of-dust
expansion-kind: encounter
delivery-status: shipped
status: awaiting-silas

## Delivered change
Adds hidden-follower talk tiller-exile with two costly choices, each leaving its own flag and a remembered epilogue line.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/4178
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/40190675183
Verified: All 21 check runs on the final head passed; secret-talks test extended and passing locally with Prettier clean. Merged is not deployed; not eyeballed in a browser.
Art: not-required
Merge: c77b75d9e4b6824976ac272e879943e3e83d6ef7

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
