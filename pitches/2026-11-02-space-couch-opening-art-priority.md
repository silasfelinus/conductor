# Pitch: Space Couch: priority paintings for the opening missions and Couchscope
date: 2026-11-02
project-target: game-of-captains
expansion-kind: first-time player art gap
delivery-status: in-progress
status: awaiting-silas

## Delivered change
A priority-950 auto-submit ledger commissions red-couch repaints of the three opening missions (whose only paintings predate the redesign, so the first stage shows filler), twelve constellation plates and the trolley question with its three answers.

## Evidence
PR: https://github.com/silasfelinus/conductor/pull/6979
Checks: https://github.com/silasfelinus/conductor/actions/runs/41551948571
Verified: All conductor PR checks passed; art_ledger_authoring reported 0 problems and the kind_robots live prompt contract passed 19 of 19 prompts before merge.
Art: queued
ArtJob IDs: [63467, 63468, 63469, 63470, 63471, 63472, 63473, 63474, 63475, 63476, 63477, 63478, 63479, 63480, 63481, 63482, 63483, 63484, 63485]
Next step: Once the ArtJobs render, add each DONE ArtImage id to kind_robots onboardingArt.ts and voyagePaintings.ts and verify the final URLs in game.

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
