# AI Art Academy continuous-improvement checklist

Use this checklist for recurring `t-010` cycles so each pass produces a distinct, verifiable improvement instead of re-auditing the same blockers.

## Rotation

Choose the first useful lane that has not run in the previous cycle:

1. Front-end polish
2. Roadmap accuracy
3. Inspiration and preview assets
4. Curriculum depth

Record the lane, files changed, and verification in the task note before rearming `t-010`.

### Rotation state

- Last completed lane: Roadmap accuracy (lane 2), 2026-07-19 (~22:00-22:20 UTC). Milestone audit came back clean (no drift). Fixed a real tooling bug found while auditing: `scripts/check_pr_merged_drift.py` treated failed GitHub API lookups (this session type only has GitHub MCP tools, not direct REST/token access — every lookup 403'd) identically to confirmed-open PRs, so a 100%-failed run silently reported "No drift found" with exit 0, indistinguishable from a genuine clean audit. `check()`/`render()` now surface unresolved lookups explicitly and `main()` exits 2 (not 0) when anything couldn't be verified. Tests updated/added in `tests/test_check_pr_merged_drift.py`; full suite green (427 passed, 1 pre-existing skip). Conductor-only change, no kind_robots PR.
- Previously: Front-end polish (lane 1), 2026-07-19 (~19:04-19:15 UTC). Fixed `image-upload.vue`'s `addFiles()` silently dropping non-PNG/JPEG/WebP files (drag-and-drop bypasses the input's `accept` attribute) with zero user-visible feedback — now sets `error.value` to a skip-count message. kind_robots PR #547, merged 2026-07-19T19:14Z.
- Rechecked 2026-07-19 (~12:20-12:35 UTC): roadmap accuracy (lane 2) and a curriculum-depth (lane 4) spot-check both came back clean/unchanged that cycle — no drift, no new verifiable fact. See `t-010`'s RECHECKED note in `roadmap.yaml` for detail.
- Next preferred lane: Inspiration/preview assets (lane 3) is next in rotation order since lane 2 just ran — check `public/images/academy/styles/` before picking it (last confirmed absent 2026-07-19 08:11 UTC, unchecked this cycle). Fall back to curriculum depth (lane 4) if still blocked.
- Override the preferred lane only when it is blocked or a higher-severity reversible issue is newly verified; record that reason in the task note.

This explicit state is the handoff between recurring cycles. Update it in the same PR as each `t-010` improvement so the next Worker does not infer rotation from a long roadmap note.

## Current curriculum coverage

The Academy currently has 24 movement entries in `curriculum-outline.md`; all 24 are
now synced to `academyStyles.ts` (t-031 landed the Suprematism sync 2026-07-18; t-034
landed the Ashcan School sync 2026-07-18, kind_robots PR #464; this 2026-07-19 cycle
landed the American Regionalism sync, kind_robots PR #506). Before adding a 25th
movement, finish the known coverage gaps below unless a newly discovered issue is
more urgent.

| Area | Current state | Next verifiable action |
|---|---|---|
| Lesson seed entries | 24 movements in curriculum-outline.md; all 24 synced to `academyStyles.ts` (this cycle landed the American Regionalism sync, kind_robots PR #506, mirroring t-020/t-031/t-034) | No action needed until a 25th movement lands |
| Example works | 22 movements complete (t-013 landed Expressionism/Cubism/Bauhaus 2026-07-17; Suprematism shipped complete 2026-07-18); Ashcan School's 4 VERIFIED works are written up in curriculum-outline.md §23 but not yet in `examples.manifest.json` (confirmed absent: no `exampleWorks` field on the `ashcan-school` entry in `stores/seeds/academyStyles.ts` as of 2026-07-19). American Regionalism's 4 works are written up in curriculum-outline.md §24 (sourced, but marked "unverified this cycle" — `WebFetch` to museum hosts returned HTTP 402 through the session egress proxy) | Blocked on media-server write access — same blocker as t-033 (confirmed 2026-07-19: `examples.manifest.json` lives on `media.acrocatranch.com`, not in the kind_robots git repo; this session has `KR_API_TOKEN` but no `KR_RELAY_TOKEN`/`KR_RELAY_USER_ID` and found no in-repo upload path, so it cannot write the manifest or upload images from here). Research/sourcing is already done (curriculum-outline.md §23-24); only the write step remains, plus a direct-fetch spot-check of §24's four URLs when museum/Commons egress is open. Resume once a session with media-server/relay write access is available — do not re-attempt from a sandbox without it |
| Starter library | 21 starter images and provenance manifest complete — coverage intentionally movement-agnostic (2026-07-18: confirmed no movement-specific starters exist for any of the 8 movements added after v1, and an abstract Suprematist work would fail the library's own selection criteria; see starter-image-library.md) | Keep source-picker integration aligned with the manifest; no new starter entries needed |
| Style previews | 24 prompts queued (Suprematism queued 2026-07-18, `kind-robots-academy-style-preview-suprematism`; Ashcan School queued the same cycle it was added, `kind-robots-academy-style-preview-ashcan-school`; American Regionalism queued 2026-07-19, `kind-robots-academy-style-preview-american-regionalism`, all in `art-prompts.yaml`) | No action needed until a 25th movement lands |
| Remix configs | Registry exists; A/B generation blocked | Resume only after the relay, database, and approved generation path are available |
| Teaching scaffold | Written in `docs/teaching-notes.md`, covering all 24 movements including American Regionalism; wired into `academy-style-detail.vue`'s Try It / Reflect sections (t-023, done — verified 2026-07-18 via `grep -n "Try it\|Reflect" components/academy/academy-style-detail.vue` on kind_robots main) | No action needed; keep the Vue wiring aligned as new movements land |

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
