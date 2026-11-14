# Pitch: Front door: Emperor of Dust link preview card
date: 2026-11-14
project-target: emperor-of-dust
expansion-kind: front door: link preview
delivery-status: shipped
status: awaiting-silas

## Delivered change
Shared Emperor of Dust links now unfurl with a titled card framing the fortress art instead of an untitled cropped painting.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5150
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/43582526638
Verified: All 12 check runs on the final head completed green (TypeScript, layout contract, Changed-file Prettier, four contract shards, Contract verifiers); verifyGameLinkPreview and Prettier also run locally; every card rendered in headless Chromium and inspected. Merged is not deployed; live crawler unfurls not yet checked.
Art: delivered
Merge: ff3c764a527d3121018ae40e368a0185687e77a1
Art URL: https://github.com/silasfelinus/kind_robots/blob/ff3c764a527d3121018ae40e368a0185687e77a1/public/emperor-of-dust/link-preview.webp

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
