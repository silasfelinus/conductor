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

The Academy currently has 23 movement entries in `curriculum-outline.md`; all 23 are
synced to `academyStyles.ts` (t-031 landed the Suprematism sync 2026-07-18; t-034
landed the Ashcan School sync 2026-07-18, kind_robots PR #464, merged). Before adding
a 24th movement, finish the known coverage gaps below unless a newly discovered
issue is more urgent.

| Area | Current state | Next verifiable action |
|---|---|---|
| Lesson seed entries | 23 movements in curriculum-outline.md; all 23 synced to `academyStyles.ts` (t-034 landed the Ashcan School sync 2026-07-18, kind_robots PR #464) | No action needed until a 24th movement lands |
| Example works | 22 movements complete (t-013 landed Expressionism/Cubism/Bauhaus 2026-07-17; Suprematism shipped complete 2026-07-18); Ashcan School's 4 VERIFIED works are written up in curriculum-outline.md §23 but not yet in `examples.manifest.json` | Follow-up pass: add Ashcan School's 4 example works to `examples.manifest.json`, mirroring t-013 (t-034's own note scoped this out of the seed-sync PR) |
| Starter library | 21 starter images and provenance manifest complete — coverage intentionally movement-agnostic (2026-07-18: confirmed no movement-specific starters exist for any of the 8 movements added after v1, and an abstract Suprematist work would fail the library's own selection criteria; see starter-image-library.md) | Keep source-picker integration aligned with the manifest; no new starter entries needed |
| Style previews | 23 prompts queued (Suprematism queued 2026-07-18, `kind-robots-academy-style-preview-suprematism`; Ashcan School queued the same cycle it was added, `kind-robots-academy-style-preview-ashcan-school`, both in `art-prompts.yaml`) | No action needed until a 24th movement lands |
| Remix configs | Registry exists; A/B generation blocked | Resume only after the relay, database, and approved generation path are available |
| Teaching scaffold | Written in `docs/teaching-notes.md`, covering all 23 movements including Ashcan School; wired into `academy-style-detail.vue`'s Try It / Reflect sections (t-023, done — verified 2026-07-18 via `grep -n "Try it\|Reflect" components/academy/academy-style-detail.vue` on kind_robots main) | No action needed; keep the Vue wiring aligned as new movements land |

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
