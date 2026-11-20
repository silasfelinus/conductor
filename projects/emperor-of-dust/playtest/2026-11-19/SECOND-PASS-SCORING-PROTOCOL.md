# Emperor of Dust: second-pass scored playtest protocol

**Status:** executable review plan, not a completed playtest or human verdict. Conductor t-044 remains open until all five acts have independently scored complete playthrough evidence. This protocol fixes the missing scoring artifact identified in the 2026-10-21 SECOND-PASS-SYSTEMS-AUDIT.md.

## Required evidence before any score is accepted

For every reviewer, retain the tested Kind Robots commit SHA, seed, policy/persona, start-state source, full ordered day-by-day action trace, five-act transcript, ending, save/rewind events and all relevant resource and follower-state transitions. Reviewers must use ordinary game choices, never injected ending flags. Label any deterministic or model-simulated player explicitly; never call it human feedback. An absent trace or unreachable branch means **not tested**, not zero and not passed.

## Scoring rubric (1–5 per dimension, separately for each act)

| Dimension | 1: unacceptable | 3: functional but weak | 5: exceptional |
| --- | --- | --- | --- |
| Mood | Contradictory tone or interchangeable scenes | Consistent tone, limited memorable beats | Sustained stark tension with earned relief and dread |
| Challenge clarity | Requirements or risks hidden until punishment | Most options legible, occasional surprises | Stakes and uncertainty telegraphed without spoiling discovery |
| Uniqueness | Repeated choices and identical outcomes | Some distinct scenes, recurring stock structures | Act has its own identity, dilemmas and consequences |
| Choice quality | Fake binary or dominant free answer | Real tradeoffs with uneven branches | Multiple credible costly choices with distinct agency |
| Consequence | Outcomes forgotten or cosmetic | Some persistent effects and callbacks | Earlier decisions materially alter relationships, resources and finale |

Score only after reading the entire act **and** its later callbacks. Cite at least two concrete scene/day/action references per dimension, one positive and one negative when possible. If evidence is absent, mark **N/A** and explain. Do not average N/A as zero. Report per-act five scores and a total out of 25 only when all five dimensions are supported.

## Campaign matrix

Complete at least one trace per act reviewer and one whole-campaign trace for each of: merciful peacemaker, ruthless tyrant, neutralist, loyal Komodo ally, suspicious investigator, Abbey sympathizer, faction specialist, completionist, market exploiter, pacifist, intentionally unlucky, speedrunner, chaotic and ignores-optional-tasks. Sample multiple seeds and explicitly record failed/abandoned paths. Include Day 1 recruitment, Day 40 betrayal and Day 41 hideout transition, Day 50 finale and Day 51 saved epilogue.

## Quantitative acceptance table (fill from actual traces, not design promises)

| Metric | Evidence to collect |
| --- | --- |
| Brass/debt/wages | Daily balance and debt events, exploit attempts, bankruptcy/softlock outcomes |
| Dispatch | Quest offered/accepted/declined/expired, odds shown, actual result tier, 1–4 followers, 1–3-day durations |
| Followers | Recruitment order, away/injured/dead status, loyalty, romances, conversations, memorial and absence-sensitive text |
| Outcomes | Ending ID, earned prerequisites, unique aftermath, divergent prior choices |
| Save integrity | Round-trip at Days 1/11/21/31/41/51, rewind and post-rewind reshuffle, corruption/legacy cases |
| Art | Rendered file bytes, human visual keeper verdict, exported path, in-game placement and viewport screenshot; ArtJob DONE alone is insufficient |
| Responsive | Real browser screenshots and interaction at 390, 768, 820 and 1440 pixels, with overlap and accessibility findings |

## Reviewer record template

```yaml
reviewer: null
kind: model-simulation # or human, only if genuinely human
kind_robots_sha: null
seed: null
persona: null
trace_path: null
transcript_path: null
ending_id: null
acts:
  1: { mood: null, clarity: null, uniqueness: null, choices: null, consequence: null }
  2: { mood: null, clarity: null, uniqueness: null, choices: null, consequence: null }
  3: { mood: null, clarity: null, uniqueness: null, choices: null, consequence: null }
  4: { mood: null, clarity: null, uniqueness: null, choices: null, consequence: null }
  5: { mood: null, clarity: null, uniqueness: null, choices: null, consequence: null }
findings: []
```

## Existing evidence and known deficiencies

The 2026-10-21 second-pass systems audit verifies engine and dialogue improvements but explicitly does **not** score all acts. Its outstanding editorial concern is 104 Act II–V daily motif events retaining repeated branch structures. Later t-052 notes document 18 full 50-day guided campaigns with versioned saves at Days 1/11/21/31/41/51 and Day 31 rewind, but those deterministic checks do **not** substitute for the independent scored editorial read. Existing responsive audit route coverage is instrumentation, not reviewed deployed screenshots. Keep the five-act scoring and actual art delivery as distinct completion gates.

**Exit condition:** populate real reviewer records, preserve complete trace evidence, compare scores with the first playtest, repair actionable weaknesses, rerun affected campaigns and attach exact-head CI. Until then this file is a concrete acceptance instrument, not a pass certificate.
