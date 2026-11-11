# Pitch: Front door: Brainstorm link preview card
date: 2026-11-11
project-target: brainstorm
expansion-kind: front door: link preview
delivery-status: shipped
status: awaiting-silas

## Delivered change
Shared Brainstorm links now unfurl with a designed card showing idea bubbles orbiting a lightbulb instead of the generic site icon.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5004
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/42991827605
Verified: All 11 check runs on the final head completed green, including TypeScript, layout contract, Changed-file Prettier and four contract shards; verifyGameLinkPreview test and Prettier also run locally; every card rendered in headless Chromium and inspected. Merged is not deployed; live crawler unfurls not yet checked.
Art: delivered
Merge: e8c086791176cfee29884928d1f5223d634328a4
Art URL: https://github.com/silasfelinus/kind_robots/blob/e8c086791176cfee29884928d1f5223d634328a4/public/brainstorm/link-preview.webp

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
