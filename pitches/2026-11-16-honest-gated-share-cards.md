# Pitch: Share cards: honest about sign-in and private previews
date: 2026-11-16
project-target: slime-city
expansion-kind: front-door
delivery-status: shipped
status: awaiting-silas

## Delivered change
Shared Slime City links now say Sign in free to play, and admin-only gallery and studio cards say private preview instead of promising free browsing behind a login wall.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5248
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/43855819500
Verified: verifyFrontDoorPolish.test.ts derives gates from content frontmatter and checks 6 cards; verifyGameLinkPreview passed; five cards re-rendered in Chromium at 1200x630 and checked by eye
Art: delivered
Merge: 88b21a1b3703bfd4a46ba1886f65cef6f6633bd7
Playable preview: https://kindrobots.org/play/slime-city
Art URL: https://kindrobots.org/slime-city/link-preview.webp
Canonical roadmap: projects/slime-city/roadmap.yaml task t-063

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
