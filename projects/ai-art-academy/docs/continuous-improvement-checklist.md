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

- Last completed lane: Curriculum depth (lane 4), 2026-07-20 (~00:15-01:10 UTC). Lane 3
  (inspiration/preview assets) was tried first per the prior cycle's preferred-lane note
  and found genuinely blocked: `python scripts/consume_art_requests.py --id-prefix
  "kind-robots-academy-style-preview-" --live --limit 2` (added the `--id-prefix` filter
  this cycle so the run wouldn't also drain the other ~130 unrelated pending requests in
  the queue) successfully queued job 816 against `https://kind-robots.vercel.app/api/art/queue`
  but the home relay never claimed it — polled for 10+ minutes, `status` stayed `PENDING`,
  `claimedAt`/`claimedBy` stayed `null` the whole time. This is a fresh, direct confirmation
  of the same relay-down blocker t-004/t-009/t-033 already document (previously verified only
  as "directory still absent," never as a live queue attempt) — see t-010's RAN note in
  roadmap.yaml. Fell back to lane 4 per this checklist's own instruction: added a 25th
  movement, Persian Miniature Painting (`persian-miniature`, curriculum-outline.md §25) —
  the first non-Western/non-Japanese entry besides Ukiyo-e. All 3 example works fetched and
  confirmed **VERIFIED** directly (Wikimedia Commons file pages, PD-Mark/PD-Art tags,
  artist Kamal ud-Din Bihzad d. 1535, works dated 1488-1495 — both PUBLIC-DOMAIN-POLICY.md
  §1.3 prongs pass with a wide margin). Queued its style-preview prompt in art-prompts.yaml
  (`kind-robots-academy-style-preview-persian-miniature`, still blocked on the same relay
  issue as the other 24). Front-end sync to `academyStyles.ts` deliberately deferred to a
  future cycle, matching how t-020/t-031/t-034 landed prior movements as separate kind_robots
  PRs — conductor-docs-only change this cycle, no kind_robots PR.
- Previously: Roadmap accuracy (lane 2), 2026-07-19 (~22:00-22:20 UTC). Milestone audit came back clean (no drift). Fixed a real tooling bug found while auditing: `scripts/check_pr_merged_drift.py` treated failed GitHub API lookups (this session type only has GitHub MCP tools, not direct REST/token access — every lookup 403'd) identically to confirmed-open PRs, so a 100%-failed run silently reported "No drift found" with exit 0, indistinguishable from a genuine clean audit. `check()`/`render()` now surface unresolved lookups explicitly and `main()` exits 2 (not 0) when anything couldn't be verified. Tests updated/added in `tests/test_check_pr_merged_drift.py`; full suite green (427 passed, 1 pre-existing skip). Conductor-only change, no kind_robots PR.
- Before that: Front-end polish (lane 1), 2026-07-19 (~19:04-19:15 UTC). Fixed `image-upload.vue`'s `addFiles()` silently dropping non-PNG/JPEG/WebP files (drag-and-drop bypasses the input's `accept` attribute) with zero user-visible feedback — now sets `error.value` to a skip-count message. kind_robots PR #547, merged 2026-07-19T19:14Z.
- Next preferred lane: Front-end polish (lane 1) — rotation completes 1→2→3→4 and this
  cycle used lane 4 (lane 3 was attempted but blocked, not completed). Lane 3 remains
  blocked on home-relay reachability; do not re-probe it with a fresh live queue attempt
  until relay/DB state is confirmed to have changed (see `EGRESS-BLOCKERS.md` convention)
  — checking `GET /api/art/queue/<id>` on the still-pending job 816 first is cheaper than
  queuing a new one.
- Override the preferred lane only when it is blocked or a higher-severity reversible issue is newly verified; record that reason in the task note.

This explicit state is the handoff between recurring cycles. Update it in the same PR as each `t-010` improvement so the next Worker does not infer rotation from a long roadmap note.

## Current curriculum coverage

The Academy currently has 25 movement entries in `curriculum-outline.md`; the first
24 are synced to `academyStyles.ts` (t-031 landed the Suprematism sync 2026-07-18;
t-034 landed the Ashcan School sync 2026-07-18, kind_robots PR #464; the 2026-07-19
cycle landed the American Regionalism sync, kind_robots PR #506). Movement 25,
Persian Miniature Painting, was added 2026-07-20 (curriculum-outline.md §25 only —
sync to `academyStyles.ts` is a future kind_robots PR, not yet done). Before adding
a 26th movement, finish the known coverage gaps below unless a newly discovered
issue is more urgent.

| Area | Current state | Next verifiable action |
|---|---|---|
| Lesson seed entries | 25 movements in curriculum-outline.md; the first 24 are synced to `academyStyles.ts` (the American Regionalism sync, kind_robots PR #506, mirrored t-020/t-031/t-034). Persian Miniature Painting (§25, added 2026-07-20) is doc-only, not yet synced | Land a kind_robots PR adding the `persian-miniature` entry to `academyStyles.ts`, mirroring t-020/t-031/t-034/PR #506 |
| Example works | 23 movements complete, including Persian Miniature Painting (3 works, all **VERIFIED** by direct `WebFetch` of their Wikimedia Commons file pages this cycle — 2026-07-20 egress to commons.wikimedia.org worked, unlike the earlier `artic.edu` 402s). Ashcan School's 4 VERIFIED works are written up in curriculum-outline.md §23 but not yet in `examples.manifest.json` (confirmed absent: no `exampleWorks` field on the `ashcan-school` entry in `stores/seeds/academyStyles.ts` as of 2026-07-19). American Regionalism's 4 works are written up in curriculum-outline.md §24 (sourced, but marked "unverified this cycle" — `WebFetch` to museum hosts returned HTTP 402 through the session egress proxy) | Blocked on media-server write access — same blocker as t-033 (confirmed 2026-07-19: `examples.manifest.json` lives on `media.acrocatranch.com`, not in the kind_robots git repo; this session has `KR_API_TOKEN` but no `KR_RELAY_TOKEN`/`KR_RELAY_USER_ID` and found no in-repo upload path, so it cannot write the manifest or upload images from here). Research/sourcing is already done (curriculum-outline.md §23-25); only the write step remains, plus a direct-fetch spot-check of §24's four URLs when museum/Commons egress is open. Resume once a session with media-server/relay write access is available — do not re-attempt from a sandbox without it |
| Starter library | 21 starter images and provenance manifest complete — coverage intentionally movement-agnostic (2026-07-18: confirmed no movement-specific starters exist for any of the 8 movements added after v1, and an abstract Suprematist work would fail the library's own selection criteria; see starter-image-library.md) | Keep source-picker integration aligned with the manifest; no new starter entries needed |
| Style previews | 25 prompts queued (Suprematism queued 2026-07-18, `kind-robots-academy-style-preview-suprematism`; Ashcan School queued the same cycle it was added, `kind-robots-academy-style-preview-ashcan-school`; American Regionalism queued 2026-07-19, `kind-robots-academy-style-preview-american-regionalism`; Persian Miniature Painting queued 2026-07-20, `kind-robots-academy-style-preview-persian-miniature`, all in `art-prompts.yaml`). All 25 are still `status: pending` — the home relay is not claiming jobs (2026-07-20: a live `--live` queue attempt via the new `--id-prefix` filter got job 816 accepted by the API but never claimed after 10+ minutes) | Blocked on home-relay reachability, not on this queue. Re-run `python scripts/consume_art_requests.py --id-prefix "kind-robots-academy-style-preview-" --live` once relay/DB state is confirmed to have changed |
| Remix configs | Registry exists; A/B generation blocked | Resume only after the relay, database, and approved generation path are available |
| Teaching scaffold | Written in `docs/teaching-notes.md`, covering the first 24 movements through American Regionalism; wired into `academy-style-detail.vue`'s Try It / Reflect sections (t-023, done — verified 2026-07-18 via `grep -n "Try it\|Reflect" components/academy/academy-style-detail.vue` on kind_robots main). Persian Miniature Painting (§25) does not yet have a teaching-notes.md entry | Add a Persian Miniature Painting entry to teaching-notes.md alongside its front-end sync |

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
