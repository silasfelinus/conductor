# Pitch: Dead Air: voiceover no longer peaks at full scale
date: 2026-11-18
project-target: dead-air
expansion-kind: quality
delivery-status: shipped
status: awaiting-silas

## Delivered change
The film mixer's limiter auto-level pushed every limited peak back to 0 dBFS; it now leaves about two decibels of headroom through the MP3 and AAC encodes.

## Evidence
PR: https://github.com/silasfelinus/conductor/pull/7574
Checks: https://github.com/silasfelinus/conductor/actions/runs/44289151925
Verified: MusicVideo 23 final measured -0.2 dBFS peak; worst-case synthetic voice measured 0.0 dBFS before and -1.1 dBFS after; new pytest fails on the old mix and passes on the new
Art: not-required
Merge: dceb70022938a06cc4b51ebc5734641430d99b98
Canonical roadmap: projects/dead-air/roadmap.yaml task t-004

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
