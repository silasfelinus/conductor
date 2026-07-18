# AI Art Academy continuous-improvement checklist

Use this checklist for recurring `t-010` cycles so each pass produces a distinct, verifiable improvement instead of re-auditing the same blockers.

## Rotation

Choose the first useful lane that has not run in the previous cycle:

1. Front-end polish
2. Roadmap accuracy
3. Inspiration and preview assets
4. Curriculum depth

Record the lane, files changed, and verification in the task note before rearming `t-010`.

## Current curriculum coverage

The Academy currently has 22 movement entries, all 22 synced to `academyStyles.ts`
(t-031 landed the Suprematism sync 2026-07-18). Before adding a 23rd movement,
finish the known coverage gaps below unless a newly discovered issue is more urgent.

| Area | Current state | Next verifiable action |
|---|---|---|
| Lesson seed entries | 22 movements in curriculum-outline.md; all 22 synced to `academyStyles.ts` (t-031 done) | Keep curriculum and `academyStyles.ts` slug order aligned as new movements land |
| Example works | 22 movements complete (t-013 landed Expressionism/Cubism/Bauhaus 2026-07-17; Suprematism shipped complete 2026-07-18) | Spot-check VERIFIED URLs opportunistically; no known gaps |
| Starter library | 21 starter images and provenance manifest complete — coverage intentionally movement-agnostic (2026-07-18: confirmed no movement-specific starters exist for any of the 8 movements added after v1, and an abstract Suprematist work would fail the library's own selection criteria; see starter-image-library.md) | Keep source-picker integration aligned with the manifest; no new starter entries needed |
| Style previews | 22 prompts queued (Suprematism queued 2026-07-18, `kind-robots-academy-style-preview-suprematism` in `art-prompts.yaml`) | Generate images only through the approved pipeline, then wire `previewImageSrc` (t-019) |
| Remix configs | Registry exists; A/B generation blocked | Resume only after the relay, database, and approved generation path are available |
| Teaching scaffold | Written in `docs/teaching-notes.md` | Wire the scaffold into lesson detail when the corresponding front-end task is ready; add a Suprematism row when that lands |

## Blocker discipline

Do not re-probe a blocker when the roadmap already contains fresh evidence with the same failure signature. Recheck only when capabilities, credentials, egress, relay state, database state, or instructions materially change.

A soft blocker never consumes the whole recurring cycle. Rotate to another lane and land a reversible improvement.

## Completion test

A `t-010` cycle is complete when all of the following are true:

- exactly one primary lane was selected;
- the change is scoped and reversible;
- verification is recorded;
- no live generation, publishing, deployment, spend, secrets, or production mutation occurred;
- the recurring task is rearmed to `ready` after merge.
