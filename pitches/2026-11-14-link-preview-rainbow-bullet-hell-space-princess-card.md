# Pitch: Front door: Rainbow Bullet Hell link preview card
date: 2026-11-14
project-target: rainbow-bullet-hell-space-princess
expansion-kind: front door: link preview
delivery-status: shipped
status: awaiting-silas

## Delivered change
Shared Rainbow Bullet Hell links now unfurl with a full-size titled card instead of a blurry 320x182 late-boss thumbnail.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5150
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/43582526638
Verified: All 12 check runs on the final head completed green (TypeScript, layout contract, Changed-file Prettier, four contract shards, Contract verifiers); verifyGameLinkPreview and Prettier also run locally; every card rendered in headless Chromium and inspected. Merged is not deployed; live crawler unfurls not yet checked.
Art: delivered
Merge: ff3c764a527d3121018ae40e368a0185687e77a1
Art URL: https://github.com/silasfelinus/kind_robots/blob/ff3c764a527d3121018ae40e368a0185687e77a1/public/rainbow-bullet-hell-space-princess/link-preview.webp

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
