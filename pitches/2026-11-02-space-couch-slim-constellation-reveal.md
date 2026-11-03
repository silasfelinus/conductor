# Pitch: Space Couch: slimmer constellation reveal with a painted plate per sign
date: 2026-11-02
project-target: game-of-captains
expansion-kind: first-time player onboarding fix from playtest notes
delivery-status: shipped
status: awaiting-silas

## Delivered change
The busy result page now shows only the constellation name, epithet, HR finding and forecast with two buttons, and each of the twelve signs reads its own painted plate key instead of one generic star-dot drawing.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/4686
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/41556697787
Verified: All 14 check runs on the final head passed; the Stars contract asserts the per-sign plate key, and the reveal was screenshotted locally at desktop and phone widths. Merged is not deployed.
Art: not-required
Merge: 0ad8f0d709f754b960f72de585df06767e9bd882

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
