# Pitch: Space Couch: all twelve officers on one screen with three visible seats
date: 2026-11-02
project-target: game-of-captains
expansion-kind: first-time player onboarding fix from playtest notes
delivery-status: shipped
status: awaiting-silas

## Delivered change
Crew selection drops its two-page roster for a single 4x3 portrait grid with three seats above it that fill as officers are tapped, show portrait and name, carry a release button, and number the chosen cards.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/4686
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/41556697787
Verified: All 14 check runs on the final head passed; tapping three officers was exercised in Playwright at 1280x720 and 390x844 with screenshots of empty and filled seats. Merged is not deployed.
Art: not-required
Merge: 0ad8f0d709f754b960f72de585df06767e9bd882

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
