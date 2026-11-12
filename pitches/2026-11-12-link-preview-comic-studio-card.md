# Pitch: Front door: Comic Studio link preview card
date: 2026-11-12
project-target: interface-vision
expansion-kind: front door: link preview
delivery-status: shipped
status: awaiting-silas

## Delivered change
Shared Comic Studio links now unfurl with a designed card showing a three-panel comic page with a speech bubble and KAPOW instead of the generic site icon.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5074
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/43195149926
Verified: All 11 check runs on the final head completed green (TypeScript, layout contract, Changed-file Prettier, four contract shards); verifyGameLinkPreview test and Prettier also run locally; every card rendered in headless Chromium and inspected. Merged is not deployed; live crawler unfurls not yet checked.
Art: delivered
Merge: f78eb291f3c53b63fe26fa3e9b2911bbffeb8fe6
Art URL: https://github.com/silasfelinus/kind_robots/blob/f78eb291f3c53b63fe26fa3e9b2911bbffeb8fe6/public/comic-studio/link-preview.webp

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
