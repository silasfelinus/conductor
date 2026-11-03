# Pitch: Space Couch: a funnier three-question Couchscope with a trolley problem
date: 2026-11-02
project-target: game-of-captains
expansion-kind: first-time player onboarding fix from playtest notes
delivery-status: shipped
status: awaiting-silas

## Delivered change
The captain personality quiz drops from four questions to three; the vague future-self and miracle-invoice questions are replaced by a cake-trolley trolley problem (brace for frosting, risk survey, multi-track drift) and a concrete DO NOT WEAR crown, while the painted sun-and-moon question stays first and old four-answer saves keep their sign.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/4686
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/41556697787
Verified: All 14 check runs on the final head passed, including vue-tsc, layout contract, four contract shards and full adversarial voyages. Walked the quiz in a local dev build at 1280x720 and 390x844. Merged is not deployed.
Art: not-required
Merge: 0ad8f0d709f754b960f72de585df06767e9bd882

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
