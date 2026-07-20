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

- Last completed lane: Curriculum depth (lane 4, coverage-gap follow-up), 2026-07-20
  (~10:04-10:35 UTC). Lane 3 (inspiration/preview assets) was next preferred per the
  prior cycle's note, tried first: `GET /api/art/queue/816` (the job queued at
  ~00:14 UTC) still showed `status: PENDING` with `updatedAt` unchanged since
  creation, ~10 hours later — the home relay has not touched it, same blocker
  signature as every prior check. Fell back to lane 4 per the checklist's own
  instruction, and per its "finish known coverage gaps before a 26th movement" rule
  picked the one non-blocked gap in the coverage table: added a Persian Miniature
  Painting row (#25) to `docs/teaching-notes.md`'s per-style table (mode `prompt`,
  difficulty **Hard** — the movement's inverted spatial logic, "distant figures placed
  higher not smaller," fights the same "preserve composition" tension already
  documented for cubism/de-stijl/suprematism) and bumped the section header from
  "24 movements" to "25". Also added the missing `persian-miniature` placeholder row
  to `style-lora-registry.md`'s curriculum-slug-mapping table (mirroring the existing
  `ashcan-school`/`american-regionalism` "not yet in the registry" convention — no
  LoRA search performed this cycle). Conductor-docs-only change; no kind_robots PR
  needed (teaching-notes.md and style-lora-registry.md are conductor-repo docs, not
  synced into the kind_robots front end). Left two related gaps unfixed, out of this
  cycle's scope: `curriculum-outline.md` never got a "v1.5 addition re-check" public-
  domain-policy paragraph for §25 (every other addition since v1.1 has one; the
  underlying VERIFIED research already exists in §25 itself, so this is a low-risk
  writeup, not new research) and persian-miniature is not yet categorized in
  `curriculum-outline.md`'s "Lesson-only vs remixable" strong/good-but-watch tier
  lists. Both are candidates for the next lane-4 or lane-2 cycle.
- Last completed lane: Roadmap accuracy (lane 2), 2026-07-20 (~08:06-08:30 UTC). Ran
  `scripts/check_pr_merged_drift.py` (clean, no drift) and `scripts/audit_roadmaps.py`
  (only 2 pre-existing info-level `APPROVAL_WITHOUT_GATE` findings for this project,
  t-002/t-011 — not defects, no warnings/errors). Found a real, verifiable staleness
  bug while auditing t-033's blocker chain: `docs/t-013-remaining-example-works.md`
  (written 2026-07-17) listed `examples.manifest.json` and its 3 example-work images
  as files to commit directly into the `kind_robots` git repo, but the 2026-07-19
  finding already on record (this file's "Example works" coverage row) established
  that manifest lives on `media.acrocatranch.com`, not in git — the handoff doc
  predated that discovery and never got corrected, so a future session with
  home-relay access could easily follow its stale file list and commit to paths the
  contract verifier never reads. Confirmed via `kind_robots` source
  (`utils/scripts/mediaContractSource.ts`: `examples.manifest.json` is read through
  `mediaSourceDescription()`/`readMediaText()` against `MEDIA_ROOT` or
  `https://media.acrocatranch.com`, never the git tree) and a live check
  (`get_file_contents` on `public/images/academy/examples/` 404s — the directory
  does not exist in the repo). Corrected the handoff doc in place (split "Files to
  change" into an in-repo half — `academyStyles.ts` only — and a media-server half
  routed through the home relay) and added a short pointer note to t-033 in
  roadmap.yaml. Conductor-only change, no kind_robots PR (nothing to commit there
  yet — t-033/t-035 remain genuinely blocked on home-relay write access, unchanged).
- Previously: Front-end polish (lane 1), 2026-07-20 (~06:06-06:20 UTC). Dispatched
  an Explore subagent over all 7 in-scope files with an explicit exclusion list of every
  previously-fixed bug class. Found a real, verifiable bug: `image-upload.vue`'s
  `handleBatchUpload()` left `queuedFiles` untouched after a partial failure, so retrying
  re-uploaded the entire original batch — including already-succeeded files — creating
  duplicate `ArtImage` rows and duplicate collection/model attachments. Fixed by splicing
  succeeded files out of the queue (revoking their object URLs) as soon as the batch
  result comes back, so a retry only resends the files that actually failed. kind_robots
  PR #622 (branch `claude/keen-fermat-be7jf0`), merging once CI is green.
- Previously: Curriculum depth (lane 4, follow-up), 2026-07-20 (~04:10-04:40 UTC).
  Lane 3 (inspiration/preview assets) was next preferred, tried first, and reconfirmed
  blocked: a fresh `--live` queue attempt (job 855) sat PENDING/unclaimed after 10+ minutes,
  same signature as every prior check — home relay still down. Fell back to lane 4, but the
  prior cycle had already fully researched Persian Miniature Painting, so this cycle finished
  that cycle's own deferred follow-up instead: synced `persian-miniature` into kind_robots'
  `stores/seeds/academyStyles.ts` (era c. 1400-1600, sortYear 1400, inserted between
  `renaissance` and `northern-renaissance`). kind_robots PR #616, merged squash `99ba5ff3`,
  all 3 CI checks green. `exampleWorks`/`previewImageSrc` deferred to a future task (real
  image files still needed). Split conductor's t-035 so the completed sync half doesn't keep
  blocking on the still-down relay half. Curriculum content is now 25/25 synced.
- Previously: Front-end polish (lane 1), 2026-07-20 (~02:16-02:30 UTC). Dispatched
  an Explore-style search over all 7 in-scope files plus their `academyStore.ts`/
  `styleHelper.ts` dependencies, cross-checked against `git log` on each file to confirm
  which prior PRs already touched it. Found a real, verifiable gap: `art-styler.vue`'s
  `handleDrop` silently discarded any dragged file whose `type` didn't start with `image/`
  (or had no MIME type) — `isDragging` reset, no error, no state change, total silence.
  This is the same drag-and-drop silent-rejection bug class already fixed in
  `image-upload.vue` (PR #547), but that PR never touched `art-styler.vue`, which has its
  own independent drop handler. Fixed by reusing the component's existing `errorMessage`
  feedback pattern (already used in `selectStarterEntry`/`runStyleTransfer`'s catch blocks)
  rather than adding new UI. kind_robots PR #603 (branch
  `claude/ai-art-academy-t010-art-styler-drop-feedback`): all 3 CI checks green
  (TypeScript, Contract verifiers, GitGuardian), merged squash `2bf1bf7`.
  Everything else in the 7-file set was checked and ruled out: focus-restoration,
  `aria-*` wiring, `showRemixButton` contract, Set-based file-identity keys, and the
  `aria-pressed` grids are all already correct per prior cycles (#275/#301/#385/#397/#515/
  #520/#544/#547).
- Previously: Curriculum depth (lane 4), 2026-07-20 (~00:15-01:10 UTC). Lane 3
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
- Next preferred lane: Front-end polish (lane 1) — this cycle completed lane 4
  (fell back from lane 3, still blocked). Lane 3 was reconfirmed blocked 2026-07-20
  ~10:04Z by directly polling `GET /api/art/queue/816` (fresh, authenticated —
  `status: PENDING`, `updatedAt` unchanged since the job was queued ~00:14Z, ~10
  hours with zero relay activity); a future cycle should queue and poll a *new* job
  rather than re-check 816 again, since 816 itself will never resolve once the relay
  is back (it's not being retried). If lane 1 is exhausted or blocked, lane 4's two
  freshly-identified small gaps (curriculum-outline.md's missing v1.5 policy re-check
  paragraph for §25; persian-miniature not yet in the remix-quality tier lists) are
  ready-to-pick fallbacks before reaching for lane 2.
- Override the preferred lane only when it is blocked or a higher-severity reversible issue is newly verified; record that reason in the task note.

This explicit state is the handoff between recurring cycles. Update it in the same PR as each `t-010` improvement so the next Worker does not infer rotation from a long roadmap note.

## Current curriculum coverage

The Academy currently has 25 movement entries in `curriculum-outline.md`, and all 25
are now synced to `academyStyles.ts` (t-031 landed the Suprematism sync 2026-07-18;
t-034 landed the Ashcan School sync 2026-07-18, kind_robots PR #464; the 2026-07-19
cycle landed the American Regionalism sync, kind_robots PR #506; the 2026-07-20
~04:10-04:40 UTC cycle landed the Persian Miniature Painting sync, kind_robots PR
#616). Before adding a 26th movement, finish the known coverage gaps below unless a
newly discovered issue is more urgent.

| Area | Current state | Next verifiable action |
|---|---|---|
| Lesson seed entries | All 25 movements in curriculum-outline.md are synced to `academyStyles.ts` (Persian Miniature Painting landed 2026-07-20, kind_robots PR #616, mirroring t-020/t-031/t-034/PR #506) | Coverage complete for the current 25-movement curriculum; sync the next movement when one is added |
| Example works | 23 movements complete, including Persian Miniature Painting (3 works, all **VERIFIED** by direct `WebFetch` of their Wikimedia Commons file pages this cycle — 2026-07-20 egress to commons.wikimedia.org worked, unlike the earlier `artic.edu` 402s). Ashcan School's 4 VERIFIED works are written up in curriculum-outline.md §23 but not yet in `examples.manifest.json` (confirmed absent: no `exampleWorks` field on the `ashcan-school` entry in `stores/seeds/academyStyles.ts` as of 2026-07-19). American Regionalism's 4 works are written up in curriculum-outline.md §24 (sourced, but marked "unverified this cycle" — `WebFetch` to museum hosts returned HTTP 402 through the session egress proxy) | Blocked on media-server write access — same blocker as t-033 (confirmed 2026-07-19: `examples.manifest.json` lives on `media.acrocatranch.com`, not in the kind_robots git repo; this session has `KR_API_TOKEN` but no `KR_RELAY_TOKEN`/`KR_RELAY_USER_ID` and found no in-repo upload path, so it cannot write the manifest or upload images from here). Research/sourcing is already done (curriculum-outline.md §23-25); only the write step remains, plus a direct-fetch spot-check of §24's four URLs when museum/Commons egress is open. Resume once a session with media-server/relay write access is available — do not re-attempt from a sandbox without it |
| Starter library | 21 starter images and provenance manifest complete — coverage intentionally movement-agnostic (2026-07-18: confirmed no movement-specific starters exist for any of the 8 movements added after v1, and an abstract Suprematist work would fail the library's own selection criteria; see starter-image-library.md) | Keep source-picker integration aligned with the manifest; no new starter entries needed |
| Style previews | 25 prompts queued (Suprematism queued 2026-07-18, `kind-robots-academy-style-preview-suprematism`; Ashcan School queued the same cycle it was added, `kind-robots-academy-style-preview-ashcan-school`; American Regionalism queued 2026-07-19, `kind-robots-academy-style-preview-american-regionalism`; Persian Miniature Painting queued 2026-07-20, `kind-robots-academy-style-preview-persian-miniature`, all in `art-prompts.yaml`). All 25 are still `status: pending` — the home relay is not claiming jobs (2026-07-20: a live `--live` queue attempt via the new `--id-prefix` filter got job 816 accepted by the API but never claimed after 10+ minutes) | Blocked on home-relay reachability, not on this queue. Re-run `python scripts/consume_art_requests.py --id-prefix "kind-robots-academy-style-preview-" --live` once relay/DB state is confirmed to have changed |
| Remix configs | Registry exists; A/B generation blocked | Resume only after the relay, database, and approved generation path are available |
| Teaching scaffold | Written in `docs/teaching-notes.md`, now covering all 25 movements including Persian Miniature Painting (row 25 added 2026-07-20, this cycle); wired into `academy-style-detail.vue`'s Try It / Reflect sections (t-023, done — verified 2026-07-18 via `grep -n "Try it\|Reflect" components/academy/academy-style-detail.vue` on kind_robots main) | Coverage complete for the current 25-movement curriculum; add the next movement's row when one is added |

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
