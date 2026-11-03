# Pitch: Space Couch: the mission briefing becomes a four-step console deck
date: 2026-11-02
project-target: game-of-captains
expansion-kind: first-time player onboarding fix from playtest notes
delivery-status: shipped
status: awaiting-silas

## Delivered change
The thirteen-section scrolling briefing form is now four full-panel steps (Course, Captain, Ship, Away team) with art-led route, room and officer cards, the captain's bad idea on the shared choice hand, a big odds readout and one console action row.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/4686
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/41556697787
Verified: All 14 check runs on the final head passed, including the layout contract one-scroll rule and 184 seeded trace voyages; all four steps were screenshotted locally at desktop and phone widths. Merged is not deployed.
Art: not-required
Merge: 0ad8f0d709f754b960f72de585df06767e9bd882

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
