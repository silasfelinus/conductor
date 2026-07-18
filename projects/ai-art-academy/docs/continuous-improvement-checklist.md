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

The Academy currently has 23 movement entries in `curriculum-outline.md`; 22 are
synced to `academyStyles.ts` (t-031 landed the Suprematism sync 2026-07-18). Ashcan
School (v1.3, added 2026-07-18) is docs-only so far — see t-034 below. Before adding
a 24th movement, finish the known coverage gaps below unless a newly discovered
issue is more urgent.

| Area | Current state | Next verifiable action |
|---|---|---|
| Lesson seed entries | 23 movements in curriculum-outline.md; 22 synced to `academyStyles.ts` — Ashcan School (v1.3) not yet synced | Land t-034 (sync Ashcan School into `academyStyles.ts`, mirroring t-018/t-020/t-031) |
| Example works | 22 movements complete (t-013 landed Expressionism/Cubism/Bauhaus 2026-07-17; Suprematism shipped complete 2026-07-18); Ashcan School's 4 VERIFIED works are written up in curriculum-outline.md §23 but not yet in `examples.manifest.json` | Land alongside t-034's seed sync |
| Starter library | 21 starter images and provenance manifest complete — coverage intentionally movement-agnostic (2026-07-18: confirmed no movement-specific starters exist for any of the 8 movements added after v1, and an abstract Suprematist work would fail the library's own selection criteria; see starter-image-library.md) | Keep source-picker integration aligned with the manifest; no new starter entries needed |
| Style previews | 22 prompts queued (Suprematism queued 2026-07-18, `kind-robots-academy-style-preview-suprematism` in `art-prompts.yaml`); Ashcan School not yet queued | Queue an Ashcan School style-preview prompt in `art-prompts.yaml`, mirroring t-022's pattern |
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
