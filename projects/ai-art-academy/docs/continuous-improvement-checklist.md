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

- Last completed lane: Roadmap accuracy (lane 2, fallback), 2026-07-21
  (~22:05-22:35 UTC, claude-conductor-scheduled-20260721T220455Z-t010). Lane 1
  (front-end polish) was next preferred per the prior cycle's note and was
  tried first, but this session's designated kind_robots branch
  (`claude/keen-fermat-87rn74`) turned out to be unsafe to develop or push
  from: local `HEAD` is 114 commits behind `origin/main` and, separately, 67
  commits ahead of it, with a combined diff of 13,728 files / ~138k insertions
  relative to `origin/main` — almost entirely unrelated automated "WonderLab
  rollout"/"draft inventory"/"curated-publish" commits spanning
  2026-07-21T01:46-15:02 local time, never pushed to origin. A handful of the
  67 (ruler-hooked, kind-robots/t-042, davinci/t-014, appmaker/t-009, and this
  project's own t-010 Mughal sync) match already-merged conductor PRs
  #811-#814/#822 by commit message, so part of the gap is just staleness on
  top of the branch's own merged work — but the bulk (WonderLab rollouts
  032-041 plus draft-inventory commits) is new, unreviewed content with no
  corresponding conductor task tracking it. Did not push, force-push, reset,
  or rebase this branch. Filed conductor/t-078 (soft needs-human) so a
  session with fuller context — or Silas — can decide whether to preserve,
  rebase, or discard it; lane 1 may stay blocked by this until t-078 resolves,
  a distinct blocker from the home-relay one below. Fell back to lane 2:
  `audit_roadmaps.py` (0 errors, 44 info, same baseline; the 14 warnings are
  all in other projects) and `check_pr_merged_drift.py` (0 claimed/review PRs
  to check) both clean; all 6 milestones re-verified against actual task
  statuses — still accurate, no drift. Spot-checked lane 3's headline blocker
  for currency (not claiming the lane, just checking before leaving it for
  the next cycle): job 816 (the id t-035's note used to name as the "cheapest
  recheck") shows `status: DONE`, `claimedAt: 2026-07-20T12:51:03Z` — but
  t-035's own 2026-07-21T04:20 UTC entry already caught and dismissed this
  exact reading as a stale one-off completion, not evidence of current
  availability, so it isn't new information. Checked the 3 most recently
  queued preview jobs instead (1229, 1242, 1275, spanning 2026-07-20 to
  2026-07-21): all still `PENDING` with no `claimedAt`, confirmed live this
  cycle — consistent with every prior cycle back to 2026-07-18, no change.
  t-035 stays blocked. Next preferred lane is inspiration/preview assets
  (lane 3) if lane 1 is still blocked when the next cycle runs — re-probe
  with a fresh job id, not 816/1229/1242/1275 again.
- Last completed lane: Curriculum depth (lane 4, documentation-accuracy
  follow-up), 2026-07-21 (~19:10-19:30 UTC,
  claude-conductor-agentrun-20260721T1910Z-t010). Lane 3 (inspiration/preview
  assets) was next preferred per the prior cycle's note, tried first with a
  genuinely fresh queued job (job 1275, greek-vase-painting.webp, not 1242 or
  earlier): timed out after 60s still queued, same never-claimed home-relay
  signature as every prior check since 2026-07-18. Fell back to lane 4. Found
  a real, verifiable documentation-staleness bug while checking this lane's
  headline "known gap": this section (below) and its coverage table both
  still said Mughal Miniature Painting (§27) "has not yet been synced" to
  `academyStyles.ts`, but kind_robots PR #814 already landed that exact sync
  and merged at 2026-07-21T16:12:09Z (confirmed via `get_file_contents` on
  kind_robots' current `stores/seeds/academyStyles.ts` — the `mughal-miniature`
  entry is present with `recognitionCues`/`artists`/`failureMode`/`remix`
  fields matching the curriculum doc) — the ~16:06 UTC cycle that opened #814
  and the ~16:20 UTC Reviewer pass that merged it both updated the roadmap's
  RAN note but neither updated this checklist's summary prose, so it drifted
  one merge behind its own rotation-state entry (same staleness *shape* as
  the coat-dance/t-010 and ai-art-academy/t-010 self-corrections logged
  earlier in this file, just in a doc this task also maintains rather than
  `status:`). Corrected the "Current curriculum coverage" section and table
  below to 27/27 synced. With the sync gap now closed, every remaining
  coverage-table row (example works, style previews, remix configs) is
  blocked solely on the same home-relay-down signature reconfirmed this
  cycle — no other unblocked lane-4 work remains before a 28th movement.
  `scripts/audit_roadmaps.py` — 0 errors, same baseline, no new findings.
  Conductor-docs-only change; no kind_robots PR needed (nothing to sync,
  the front-end already has it). Next preferred lane is front-end polish
  (lane 1) — this cycle ran lane 4, so lane 1 is next in the 1→2→3→4
  rotation.
- Last completed lane: Roadmap accuracy (lane 2), 2026-07-21 (~16:30 UTC,
  claude-conductor-scheduled-20260721T1630Z-t010). `audit_roadmaps.py` and
  `check_pr_merged_drift.py` both clean; all 6 milestones re-verified
  programmatically against actual task statuses — no drift. Did not re-probe
  lane 3's home-relay blocker (checked fresh by the immediately-prior cycle
  the same day). Next preferred lane: 3 (inspiration/preview assets), fall
  back to lane 4 if still blocked.
- Before that: Front-end polish (lane 1), 2026-07-21 (~16:06-16:20 UTC,
  claude-conductor-burst-20260721T1600Z / merged by a Reviewer pass at
  ~16:20 UTC). Synced the mughal-miniature entry (added the prior cycle)
  into `stores/seeds/academyStyles.ts`. kind_robots PR #814, all 3 CI checks
  green, merged squash `eb1c7e2`.
- Before that: Curriculum depth (lane 4), 2026-07-21 (~14:00-14:40 UTC,
  claude-conductor-burst-20260721T1400Z). Lane 3 (inspiration/preview assets) was
  tried first per the prior cycle's preferred-lane note, with a genuinely fresh
  queued job (not 1229): `python scripts/consume_art_requests.py --id-prefix
  "kind-robots-academy-style-preview-" --live --limit 1 --timeout 60` queued job
  1242 for `greek-vase-painting.webp` but it timed out after 60s still
  queued/running — same unclaimed-home-relay signature documented since
  2026-07-18 (jobs 816/855/957/1014/1175/1184/1229). Fell back to lane 4 per the
  checklist's own instruction. Added a 27th movement, Mughal Miniature Painting
  (`mughal-miniature`, curriculum-outline.md §27) — a related but visually
  distinct Indo-Persian tradition from `persian-miniature` (naturalistic faces,
  atmospheric recession, sparing local gold vs. Persian's flat unshaded fields
  and inverted perspective), previously identified as off-register for the
  Persian lesson during the 2026-07-20 LoRA search and deferred as its own
  future entry. All 3 example works fetched and confirmed **VERIFIED** directly
  (Wikimedia Commons file pages): Basawan's *The Young Emperor Akbar Arrests the
  Insolent Shah Abu'l-Maali* (Art Institute of Chicago, CC0 1.0), Bichitr's
  *Jahangir Preferring a Sufi Shaikh to Kings* (Freer Gallery/Smithsonian,
  pre-1931 publication), and Ustad Mansur's *Turkey Cock* (V&A, life+100) — all
  three artists' documented activity ends well before 1956 (Basawan fl.
  1560-1600, Bichitr active into the 1640s at latest, Mansur d. 1624), clearing
  PUBLIC-DOMAIN-POLICY.md §1.3's both-prongs test with a wide margin. Queued its
  style-preview prompt in art-prompts.yaml
  (`kind-robots-academy-style-preview-mughal-miniature`), still blocked on the
  same relay issue as the other 26. Added a remix-quality risk note (flagged,
  milder version of `persian-miniature`'s tension — the two lessons' likeliest
  failure mode is collapsing into one generic "Indo-Persian miniature" filter).
  Front-end sync to `academyStyles.ts` deliberately deferred to a future cycle,
  matching how t-020/t-031/t-034/t-010(07-20) landed prior movements as separate
  kind_robots PRs. Conductor-docs-only change this cycle; no kind_robots PR
  needed. Next preferred lane is front-end polish (lane 1) — this cycle ran
  lane 4, so lane 1 is next in the 1→2→3→4 rotation.
- Last completed lane: Roadmap accuracy (lane 2), 2026-07-21 (~10:12-10:20 UTC,
  claude-conductor-scheduled-20260721T1012Z). `audit_roadmaps.py` clean (0
  errors, 11 warnings, 45 info, same baseline); `check_pr_merged_drift.py`'s
  22 candidates were all this task's own historical PR references, direct-
  checked the newest (kind_robots#789) via GitHub MCP — confirmed merged, no
  drift. Re-verified milestones m2/m3/m5/m6 against every task in each
  bucket directly — all four already correct, no drift found this cycle.
  Rechecked t-019's blocker (still 404) and lane 3 (home relay) with a fresh
  queued job (1229) — still times out unclaimed, same signature since
  2026-07-18. Next preferred lane is inspiration/preview assets (lane 3,
  recheck with a fresh job, not 1229) falling back to lane 4 if still
  blocked.
- Last completed lane: Front-end polish (lane 1), 2026-07-21 (~08:20-08:35 UTC,
  claude-conductor-agentrun-20260721T0811Z). Dispatched an Explore subagent over
  the full in-scope surface (art-styler.vue, image-upload.vue, all
  components/academy/*.vue, academyStore.ts, styleHelper.ts, academyStyles.ts)
  with this checklist's exclusion list of every bug class already fixed in
  prior cycles. Found a real, verifiable gap: `image-upload.vue`'s
  `handleBatchUpload()` populated `succeededFiles` purely to drive the
  per-thumbnail success checkmark overlay, but in every real code path the
  same synchronous tick immediately spliced those items out of `queuedFiles`
  (or cleared the whole queue on a fully-clean batch) before Vue ever flushed
  a DOM update showing the checkmark — the overlay markup and its backing
  `Set` were dead code in every real path, distinct from the already-fixed
  message/error-ordering bug in the same function. Fixed by awaiting
  `nextTick()` plus a short `setTimeout` (700ms) after populating
  `succeededFiles`, before the queue is pruned/cleared, so the checkmark
  actually gets a frame to paint; preserved the existing
  clearQueue-before-message-assignment ordering unchanged. Verified: `npx
  eslint`/`npx prettier --check` clean, full-project `npm run test`
  (`vue-tsc --noEmit`) exit 0. kind_robots PR #789 (branch
  `claude/vigilant-edison-imk3ia`). Next preferred lane is roadmap accuracy
  (lane 2) — this cycle ran lane 1, so lane 2 is next in the 1→2→3→4
  rotation.
- Administrative cycle (not a rotation lane), 2026-07-21 (~08:11-08:14 UTC,
  claude-conductor-agentrun-20260721T0811Z). The ~07:15Z cycle below (lane 4)
  left kind_robots PR #771 open without merging it and without recording its
  own rotation-state entry here — this cycle closed both gaps: verified both
  required CI checks green (TypeScript, Contract Tests) and merged PR #771
  (squash `296fafb`), then backfilled the missing entry below. Next preferred
  lane is still front-end polish (lane 1), unchanged from the 06:11 cycle's
  pointer — the 07:15 cycle's sync work was itself deferred lane-4 follow-up
  from that cycle's own findings, not a fresh rotation pick.
- Last completed lane: Curriculum depth (lane 4, sync follow-up), 2026-07-21
  (~07:11-07:15 UTC, session claude/keen-fermat-mzq52d). Synced
  `song-dynasty-landscape` (curriculum-outline.md §26, added the immediately-
  prior lane-4 cycle) into kind_robots' `stores/seeds/academyStyles.ts` — core
  lesson fields only (name/era/sortYear/region/keyIdeas/recognitionCues/
  artists/remix), positioned between `illuminated-manuscript` and `gothic`
  (era c. 950-1130, `sortYear: 950`), mirroring the persian-miniature sync
  pattern (PR #616). `exampleWorks`/`previewImageSrc` deferred to t-033
  (media-server write access still unavailable). kind_robots PR #771: both CI
  checks green, merged (see administrative-cycle entry above — this cycle's
  own PR was left open rather than merged in the same pass).
- Last completed lane: Roadmap accuracy (lane 2), 2026-07-21 (~06:11-06:30 UTC,
  claude-conductor-scheduled-burst-20260721T0611Z). Ran `scripts/audit_roadmaps.py`
  (same 0-errors/11-warnings/46-info baseline, no findings touching this project)
  and re-verified milestones m1-m6 against current task statuses directly (not just
  spot-checked) — all six already match their tasks' actual statuses, no drift.
  Reconfirmed t-019 (`public/images/academy/styles/` still 404s on kind_robots) and
  t-033/t-004/t-009 blockers unchanged, same signatures as every prior check.
  `check_pr_merged_drift.py`'s 23 candidates were all this task's own historical PR
  references (unverifiable via this sandbox's 403'd direct API, as usual) — not new
  drift, just noise from this task's own fresh claim. Found and closed a real,
  concrete documentation gap instead: Song Dynasty Landscape Painting (§26, added
  the immediately-prior cycle) was missing from every downstream coverage doc this
  checklist tracks — `docs/teaching-notes.md` had no row 26 (and still said
  "24"/"25 movements" in two places, both stale since the §26 addition landed —
  corrected both plus added the row), `docs/style-lora-registry.md`'s curriculum-slug-mapping table had no
  entry at all (not even a placeholder, unlike `ashcan-school`/`american-regionalism`'s
  convention — added one), and `docs/curriculum-outline.md`'s "Lesson-only vs
  remixable" tier lists never classified it (added to "Flagged as likely-poor
  remixers," reasoning: the movement's core identity is a specific composition — a
  single dominant vertical peak, tiny human figures — that most user photos won't
  have, the same "preserve composition fights the style's own logic" tension as
  `persian-miniature`) plus its missing "v1.6 addition re-check" PUBLIC-DOMAIN-POLICY.md
  paragraph (present for every other addition since v1.1; all three artists died
  ~900-1000 years ago and all three example works predate 1930 by centuries — the
  widest safety margin of any addition so far). Verified the registry's `styles:`
  YAML block still parses clean after the edit. Conductor-docs-only change; no
  kind_robots PR needed. Next preferred lane is inspiration/preview assets (lane 3,
  recheck with a fresh queued job, not 1184) falling back to lane 4 if still blocked.
- Last completed lane: Front-end polish (lane 1), 2026-07-21 (~05:05-05:57 UTC,
  claude-conductor-scheduled-burst-20260721T0505Z). Dispatched an Explore
  subagent over the full in-scope surface (art-styler.vue, image-upload.vue,
  all components/academy/*.vue, academyStore.ts, styleHelper.ts,
  academyStyles.ts) with this checklist's exclusion list of already-fixed bug
  classes. Found a real, verifiable rendering bug: `art-styler.vue`'s
  `sourceImageSrc`/`resultImageSrc` computeds treated `img.path` as a URL
  fallback whenever `img.imagePath` was empty. `ArtImage.path` is a real URL
  only for folder-synced collections; every upload flow (this component,
  image-upload.vue, art-maker.vue, the add-bot/-character/-reward/-scenario
  targets) instead writes a bracketed placeholder tag like `'[UploadedImage]'`
  into it, and `imagePath` is only populated outside production
  (`server/utils/UploadArtImage.ts`). In production, selecting an uploaded
  gallery image as a remix source rendered a broken-image icon in both the
  "Ready to style" banner and the Source/Result comparison panel, even though
  a usable `thumbnailData` payload had just been fetched and was sitting
  unused one branch below. Fixed with a small `isPlaceholderImagePath()`
  guard so the fallback chain skips a bracketed tag and falls through to
  `thumbnailData`/`imageData`; folder-synced images (genuine URL in `path`)
  are unaffected. Noted for a future cycle, not fixed here: two competing
  shared resolvers already exist (`utils/artImageSource.ts`'s
  `isProbablyPath()`, which already handles this case correctly, and
  `utils/artImageSrc.ts`'s `resolveArtImageSrc`, which has the same bug this
  fix just patched locally) but neither is used by any Academy/art-styler
  component, and the two files collision-warn on a duplicated `ArtImageLike`
  export at build time — consolidating onto one of them is a bigger, separate
  refactor. Verified: `npx eslint`/`npx prettier --check` clean, full-project
  `npm run test` (`vue-tsc --noEmit`) exit 0. kind_robots PR #745 (branch
  `claude/keen-fermat-vev7uz`): all 3 CI checks green (TypeScript, Contract
  verifiers, GitGuardian) — merged, 1 commit/15 additions/2 deletions/1 file,
  matching this session's diff exactly with no drift. Next preferred lane is
  roadmap accuracy (lane 2) — this cycle ran lane 1, so lane 2 is next in the
  1→2→3→4 rotation.
- Last completed lane: Curriculum depth (lane 4), 2026-07-21 (~04:05-04:35 UTC,
  claude-conductor-scheduled-burst-20260721T0405Z). Lane 3 (inspiration/preview
  assets) was tried first per the prior cycle's preferred-lane note, with a
  genuinely fresh job (1184, greek-vase-painting.webp — not 816/855/957/1014/1175):
  `python scripts/consume_art_requests.py --id-prefix "kind-robots-academy-style-preview-"
  --live --limit 1 --timeout 90` queued it (200 OK) but it timed out after 90s
  still queued; a direct `GET /api/art/queue/1184` confirmed `status: PENDING`,
  `claimedAt`/`claimedBy` both null, `updatedAt` identical to `createdAt` — same
  never-claimed signature as every prior probe, home relay still down. Fell back
  to lane 4 per this checklist's own instruction. Added a 26th movement, Song
  Dynasty Landscape Painting (`song-dynasty-landscape`, curriculum-outline.md
  §26) — the second non-Western entry (after persian-miniature) and the first
  from East Asia beyond Ukiyo-e. All 3 example works fetched and confirmed
  **VERIFIED** directly via `WebFetch` of their Wikimedia Commons file pages:
  Fan Kuan's *Travelers Among Mountains and Streams* (d. c. 1030, National Palace
  Museum Taipei), Guo Xi's *Early Spring* (d. c. 1090, National Palace Museum
  Taipei), and Xu Daoning's *Fishermen on a Mountain Stream* (d. 1052,
  Nelson-Atkins Museum of Art) — all three carry Creative Commons Public Domain
  Mark 1.0 tags and pass PUBLIC-DOMAIN-POLICY.md §1.3 with a wide margin (all
  three artists died roughly 900-1000 years ago; works date to c. 1000-1072).
  Queued its style-preview prompt in art-prompts.yaml
  (`kind-robots-academy-style-preview-song-dynasty-landscape`), still blocked on
  the same relay issue as the other 25. Front-end sync to `academyStyles.ts` and
  a `style-lora-registry.md`/`teaching-notes.md` entry deliberately deferred to
  future cycles, matching how persian-miniature (t-020/t-031/t-034/PR #616
  pattern) landed across separate cycles rather than one. `scripts/audit_roadmaps.py`
  confirmed the same 0-errors/11-warnings/46-info baseline after the change.
  Conductor-docs-only change; no kind_robots PR needed. Next preferred lane is
  front-end polish (lane 1) — this cycle ran lane 4, so lane 1 is next in the
  1->2->3->4 rotation.
- Last completed lane: Roadmap accuracy (lane 2), 2026-07-21 (~03:00-03:10 UTC,
  claude-conductor-scheduled-burst-20260721). Ran `scripts/audit_roadmaps.py`
  (same 0-errors/11-warnings/46-info baseline, only the 2 pre-existing
  `APPROVAL_WITHOUT_GATE` info findings for this project) and
  `scripts/check_pr_merged_drift.py` (all 20 candidates unverifiable via this
  session's sandboxed API access, per usual — cross-checked manually via
  GitHub MCP `pull_request_read`). Found and fixed a real, verifiable
  cross-project staleness bug (not in ai-art-academy itself, but the kind the
  drift script surfaces): `coat-dance/t-010` sat at `status: review`
  referencing kind_robots PR #650, but that PR merged 2026-07-20T16:12:43Z —
  over a day earlier. The task's own note already said the remaining scope
  (art-relay-blocked asset gen, admin Placements click) was "kept ready,"
  confirming the intended post-merge state was `ready`, but the `status:`
  field was never flipped — same bug class as the 2026-07-21 ~01:00 UTC
  ai-art-academy/t-010 self-correction (a status field silently stuck one
  step behind its own note). Fixed by setting `coat-dance/t-010` to
  `status: ready`, `owner: null`, clearing `claimed_by`/`claimed_at`, and
  recording the drift-fix rationale in its note. Also spot-checked
  `kind_robots#834` (referenced in this project's own t-010 history) —
  confirmed already correctly documented as a prior no-op-diff merge, not
  live drift. Did not re-probe t-019/t-033 (public/images/academy/styles/
  still-404 and home-relay-down blockers) — both were fresh-checked only
  ~2 hours earlier this same day with no signal anything changed, per this
  checklist's own blocker-discipline rule. Conductor-docs-only change; no
  kind_robots PR needed. Next preferred lane is inspiration/preview assets
  (lane 3, recheck with a fresh queued job, not 1175) falling back to lane 4
  if still blocked.
- Last completed lane: Front-end polish (lane 1), 2026-07-21 (~02:35-02:45 UTC,
  claude-conductor-agentrun-20260721T0235Z). Dispatched an Explore subagent over
  the in-scope Academy surface (art-styler.vue, image-upload.vue, all
  components/academy/*.vue, academyStore.ts, styleHelper.ts) with the checklist's
  full exclusion list of already-fixed bug classes. Found a real, verifiable gap:
  `academy-remix.vue`'s `<academy-style-detail>` usage (the Remix Studio sidebar)
  had no `:key`, so switching styles in the embedded `art-styler` grid patched the
  same component instance in place instead of remounting it — `academy-style-detail.vue`
  only calls `markLessonViewed()` in `onMounted`, so every style opened this way
  after the first in a session silently never got credited as viewed (no
  checkmark, no `lessonsViewedCount` increment, no error, miss persisted to
  `localStorage`). Same bug class PR #646 already fixed in
  `academy-styles-browser.vue`, but that fix never touched this component's
  independent instance — confirmed by reading both files directly before fixing.
  Fixed by adding `:key="academyStore.selectedStyle.slug"`, mirroring the
  existing `academy-styles-browser.vue` pattern exactly. Verified: `npx eslint`
  and `npx prettier --check` both clean, full-project `npm run test`
  (`vue-tsc --noEmit`) exit 0. kind_robots PR #737 (branch
  `claude/vigilant-edison-3owhvw`): all 3 CI checks green (TypeScript, Contract
  verifiers, GitGuardian) — merged squash `5ad8b57`. Next preferred lane is
  roadmap accuracy (lane 2) — this cycle ran lane 1, so lane 2 is next in the
  1→2→3→4 rotation.
- Last completed lane: Curriculum depth (lane 4, LoRA-registry follow-up),
  2026-07-21 (~02:11-02:35 UTC, claude-conductor-agentrun-20260721T0211Z). Lane 3
  (inspiration/preview assets) was next preferred per the prior cycle's note, tried
  first with a genuinely fresh queued job (job 1175, greek-vase-painting.webp, not
  1173/1014/957/855/816): `status: PENDING`, unclaimed, `updatedAt` unchanged since
  creation — same never-claimed signature as every prior check since 2026-07-18,
  home relay still down. Fell back to lane 4 per the checklist's own instruction.
  `neoclassicism` (curriculum §6, one of the original 16 target styles) had no
  registry entry at all — deferred across many prior cycles in favor of newer
  movements. With Hugging Face and Civitai both freshly confirmed reachable
  (`recheck_egress_blocks.py`, both HTTP 200), searched for the movement's central
  figure and found `NobodyButMeow/french-neoclassic-portrait-style-jacques-louis-david`
  (Civitai, FLUX.1 D) — trained exclusively on 19 Jacques-Louis David portraits
  (d. 1825), disclosed provenance, no-login download verified end-to-end (followed
  the actual `307` redirect to `b2.civitai.com` → `200`, not just the page).
  Promoted `neoclassicism` to LoRA mode in `style-lora-registry.md` (v1.5 update,
  curriculum-slug-mapping table, machine-readable block, full per-style notes).
  Also rechecked `artic.edu` (American Regionalism §24 example works, still
  unverified from a prior cycle): still blocked, now bot-challenged rather than a
  `402` — logged to `EGRESS-BLOCKERS.md`, same practical outcome, not re-litigated
  in prose here. `scripts/audit_roadmaps.py` — 0 errors, same 11-warning/46-info
  baseline. Conductor-docs-only change; no kind_robots PR needed (the registry is a
  conductor-repo doc, not synced into the kind_robots front end). Next preferred
  lane is front-end polish (lane 1) — this cycle ran lane 4, so lane 1 is next in
  the 1→2→3→4 rotation.
- Last completed lane: Roadmap accuracy (lane 2), 2026-07-21 (~01:00-01:20 UTC,
  claude-conductor-burst-20260721T0100Z). Found and fixed a process-accuracy bug
  in `t-010` itself: the immediately-prior cycle's note said it would rearm to
  `ready` once kind_robots PR #733 merged, and the conductor PR that recorded
  that note (#942) only appended the note text — it never flipped the `status:`
  field — so `t-010` sat at `status: claimed` with a fresh (non-stale) claim and
  no session actively working it, even though #733 had already merged. Fixed by
  setting `status: ready` directly. Also reconfirmed `t-019` still genuinely
  blocked (`public/images/academy/styles/` still 404s on kind_robots) and
  re-checked lane 3 with one fresh queued job (job 1173, greek-vase-painting.webp)
  — still unclaimed after queuing, same home-relay-down signature as every prior
  check since 2026-07-18. `scripts/audit_roadmaps.py` clean (same 2 pre-existing
  info findings); milestones m1-m6 re-verified against current task statuses, no
  drift. Conductor-docs-only change; no kind_robots PR needed. Next preferred
  lane is inspiration/preview assets (lane 3, recheck with a fresh queued job,
  not 1173) falling back to lane 4 if still blocked.
- Last completed lane: Front-end polish (lane 1), 2026-07-21 (~00:11-00:25 UTC,
  claude-conductor-scheduled-20260721T0011Z). Dispatched an Explore subagent over
  the full in-scope surface with an explicit exclusion list of every bug class
  already fixed in prior cycles. Found a real, verifiable gap: `art-styler.vue`'s
  `handleFileSelect` (the browse/click file-input path) passed any OS-picked file
  straight to `processUploadedFile()` with zero type validation, while its sibling
  `handleDrop` (drag-and-drop path) validated via `file.type.startsWith('image/')`
  — most OS file dialogs let a user switch to "All Files" even with `accept` set,
  so a non-image selected via browse could silently produce a broken preview or an
  opaque backend error on style transfer. Extracted a shared
  `isAcceptedImageFile()` predicate (exact match against `image/png` /
  `image/jpeg` / `image/webp`) and applied it to both handlers, also tightening
  `handleDrop`'s looser `startsWith('image/')` check (previously let GIF/SVG/
  BMP/TIFF through silently, contradicting the "PNG · JPEG · WebP" UI copy).
  Verified: `npx eslint` clean, `npx prettier --check` clean, full-project
  `npm run test` (`vue-tsc --noEmit`) exit 0. kind_robots PR #733 (branch
  `claude/vigilant-edison-w3m45u`). Next preferred lane is roadmap accuracy
  (lane 2) — this cycle ran lane 1, so lane 2 is next in the 1→2→3→4 rotation.
- Last completed lane: Curriculum depth (lane 4, LoRA-registry follow-up),
  2026-07-20 (~22:10-22:35 UTC, claude-conductor-agentrun-20260720T2210Z). Lane 3
  (inspiration/preview assets) was next preferred per the prior cycle's note,
  tried first with a genuinely fresh queued job (job 1014, greek-vase-painting.webp,
  not 816/855/957): timed out after 90s, direct API check confirmed
  `status: PENDING` with `updatedAt` unchanged since `createdAt` — same
  never-claimed signature as every prior attempt, home relay still down. Fell
  back to lane 4 per the checklist's own instruction. `docs/style-lora-registry.md`
  had no entry at all for `persian-miniature` (added to the curriculum two cycles
  earlier) — with Hugging Face and Civitai both freshly confirmed reachable this
  cycle (`recheck_egress_blocks.py`, both HTTP 200), ran a real LoRA search
  instead of deferring it again. Found `batchku/storai-persian-miniature`
  (Hugging Face, FLUX.1-dev, no login) but did not promote it: the model card
  discloses no training artists/artwork, so the dead-70-years ethical boundary
  can't be confirmed — same standard already applied to the rejected `gothic`
  Civitai candidate (S-8). Added `persian-miniature` as an 11th prompt-mode
  registry entry (machine-readable block, curriculum-slug-mapping table, and a
  full per-style notes section documenting the LoRA search and rejection
  rationale), `prompt_hint` copied verbatim from `curriculum-outline.md` §25's
  remix_hint. Verified the registry's `styles:` YAML block still parses clean
  (23 entries, 11 prompt / 12 lora, `persian-miniature` present) and
  `scripts/audit_roadmaps.py` reports the same 0-errors/11-warnings/46-info
  baseline as before this change, none touching this project.
  Conductor-docs-only change; no kind_robots PR needed this cycle (the registry
  is a conductor-repo doc, not synced into the kind_robots front end). Next
  preferred lane is front-end polish (lane 1) — this cycle ran lane 4, so lane 1
  is next in the 1→2→3→4 rotation.
- Last completed lane: Roadmap accuracy (lane 2), 2026-07-20 (~20:00-20:20 UTC,
  claude-conductor-burst-20260720T2000Z). Spot-checked PR-merge drift via GitHub
  MCP `pull_request_read` (kind_robots#672, kind_robots#650, conductor#868 — all
  confirmed merged, no drift). `scripts/audit_roadmaps.py` clean (same 2
  pre-existing info findings). Reconfirmed t-019 still blocked (`public/images/academy/styles/`
  still 404s). Found and fixed a real milestone-accuracy bug: m6 ("Continuous
  improvement loop") was `status: done` but carries t-035 (non-recurring,
  `status: ready`) — flipped m6 to `in-progress` to match. Moves ai-art-academy's
  computed progress from 77.5% to 72.5% on the next STATUS.md regen — a real
  correction. Conductor-docs-only change; no kind_robots PR needed. Next
  preferred lane is inspiration/preview assets (lane 3, recheck with a fresh
  queued job, not 957) falling back to lane 4 if still blocked.
- Last completed lane: Front-end polish (lane 1), 2026-07-20 (~18:12-18:35 UTC,
  claude-conductor-agent-20260720T1830Z). Dispatched an Explore subagent over
  all 5 Academy components plus art-styler.vue/image-upload.vue with an
  exclusion list of every pattern already fixed in prior cycles (aria-pressed,
  aria-label/aria-controls, focus-management, dead no-op handlers, duplicated
  local state, search-field coverage, stale copy). Found a real, verifiable
  bug in `image-upload.vue`'s `handleBatchUpload()`: on a fully-successful
  batch, the function set the success confirmation banner text
  (`message.value = uploadStore.message ?? ''`) and then immediately called
  `clearQueue()`, which unconditionally resets `message.value`/`error.value`
  back to `''` on the very next line — so the "✓ N images uploaded" banner
  never rendered on the happy path (the most common outcome). The
  failure/partial-failure path was unaffected since `clearQueue()` isn't
  called there, which is why the asymmetry survived this many polish cycles.
  Fixed by reordering so `clearQueue()` runs before the message/error
  assignment. Verified: `npx eslint`, `npx prettier --check` both clean;
  full-project `npm run test` (`vue-tsc --noEmit`) exit 0. kind_robots PR #672
  (branch `claude/vigilant-edison-gkpke6`): all 3 CI checks green (TypeScript,
  Contract verifiers, GitGuardian) — merged squash `070a7b8`. Next preferred
  lane is roadmap accuracy (lane 2) — this cycle ran lane 1, so lane 2 is next
  in the 1→2→3→4 rotation.
- Last completed lane: Curriculum depth (lane 4, coverage-gap follow-up),
  2026-07-20 (~17:12-17:26 UTC). Lane 3 (inspiration/preview assets) was next
  preferred per the prior cycle's note, tried first with a *fresh* queued job
  (job 957, greek-vase-painting.webp) rather than re-polling job 816: the
  queueing script hit a one-off `Connection reset by peer` mid-poll and
  aborted early, but a direct follow-up `curl` to the same job's status
  endpoint returned cleanly with `status: PENDING` and `updatedAt` unchanged
  since creation — confirming the connection reset was a transient network
  blip, not new evidence about relay state, and the underlying "not claimed"
  blocker is unchanged. Fell back to lane 4 per the checklist's own
  instruction and picked its two already-identified small gaps: added the
  missing v1.5-addition (2026-07-20) PUBLIC-DOMAIN-POLICY.md re-check
  paragraph for §25 (Persian Miniature Painting) to `curriculum-outline.md`,
  and added `persian-miniature` to the "Flagged as likely-poor remixers" tier
  list (same spatial-logic-vs-composition-preservation tension already
  flagged for `cubism`, and already called out for this movement in
  `teaching-notes.md` row 25). Conductor-docs-only change; no kind_robots PR
  needed.
- Last completed lane: Roadmap accuracy (lane 2), 2026-07-20 (~14:11-14:35 UTC). Ran
  `scripts/check_pr_merged_drift.py` (clean) and `scripts/audit_roadmaps.py` (same 2
  pre-existing info-level findings, not defects). Reconfirmed t-019 still genuinely
  blocked (`public/images/academy/styles/` still 404s on kind_robots). Found and fixed
  a real staleness bug: t-033's note claimed kind-robots/t-038 as a live co-blocker of
  the "Contract verifiers" CI check, but t-038 has been `done` since 2026-07-18
  (resolved ~6 minutes after t-033's note was written) — confirmed the check is
  healthy on recent kind_robots PRs (#646, #648). Corrected t-033's note so its
  remaining blocker reads as solely the Academy examples-manifest home-relay
  write-access issue. Conductor-docs-only change; no kind_robots PR needed.
- Last completed lane: Front-end polish (lane 1), 2026-07-20 (~12:07-12:30 UTC).
  Dispatched a general-purpose subagent over all 7 in-scope files with an explicit
  exclusion list of every previously-fixed bug class (PRs #275, #301, #332, #371,
  #380, #383, #385, #387, #397, #515, #520, #544, #547, #603, #622). Found a real,
  verifiable data-correctness bug: `academy-styles-browser.vue` shares a single
  unkeyed `academy-style-detail` instance across style switches — its click handler
  moves `expandedSlug` directly between two non-null slugs without ever passing
  through `null`, so Vue patches the same instance in place instead of remounting
  it when the user picks a new tile without closing the panel first.
  `academy-style-detail.vue` only calls `markLessonViewed()` in `onMounted`, so
  every style opened this way after the first silently stopped being credited as
  viewed — no checkmark, no `lessonsViewedCount` increment, no error.
  `academy-timeline.vue` was confirmed unaffected (each style has its own keyed
  `v-for` `<li>`, so it always mounts a distinct instance). Fixed with
  `:key="expandedStyle.slug"` on the `academy-style-detail` usage in
  `academy-styles-browser.vue`, forcing a remount per style. Verified prettier
  clean; no local `node_modules` in this sandbox, so eslint/vue-tsc relied on
  kind_robots CI this cycle (all 3 checks green: TypeScript, Contract verifiers,
  GitGuardian). kind_robots PR #646 (branch `claude/keen-fermat-y6jjjw`), merged
  squash `98cfdc8`.
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
- (This trailing bullet is now superseded by the entries above — the current
  "next preferred lane" pointer lives at the end of the most recent entry at
  the top of this list, not here. Left in place as historical record rather
  than pruned, per this task's own no-prune convention, but do not read it as
  live state.)
- Override the preferred lane only when it is blocked or a higher-severity reversible issue is newly verified; record that reason in the task note.

This explicit state is the handoff between recurring cycles. Update it in the same PR as each `t-010` improvement so the next Worker does not infer rotation from a long roadmap note.

## Current curriculum coverage

The Academy currently has 27 movement entries in `curriculum-outline.md`, all 27 of
them synced to `academyStyles.ts` (t-031 landed the Suprematism sync 2026-07-18; t-034
landed the Ashcan School sync 2026-07-18, kind_robots PR #464; the 2026-07-19 cycle
landed the American Regionalism sync, kind_robots PR #506; the 2026-07-20 ~04:10-04:40
UTC cycle landed the Persian Miniature Painting sync, kind_robots PR #616; the
2026-07-21 ~07:11-07:15 UTC cycle landed the Song Dynasty Landscape Painting sync,
kind_robots PR #771, merged ~08:14 UTC; the 2026-07-21 ~16:06-16:20 UTC cycle landed
the Mughal Miniature Painting sync, kind_robots PR #814, merged 16:12:09Z). Before
adding a 28th movement, finish the known coverage gaps below unless a newly
discovered issue is more urgent — as of the 2026-07-21 ~19:10 UTC cycle, every
remaining gap is blocked solely on home-relay reachability.

| Area | Current state | Next verifiable action |
|---|---|---|
| Lesson seed entries | 27 of 27 movements in curriculum-outline.md are synced to `academyStyles.ts` (Persian Miniature Painting landed 2026-07-20, kind_robots PR #616; Song Dynasty Landscape Painting landed 2026-07-21, kind_robots PR #771; Mughal Miniature Painting landed 2026-07-21, kind_robots PR #814 — mirroring t-020/t-031/t-034/PR #506) | Complete — no open action until a 28th movement is added |
| Example works | 24 movements complete, including Persian Miniature Painting (3 works, all **VERIFIED** by direct `WebFetch` of their Wikimedia Commons file pages — 2026-07-20 egress to commons.wikimedia.org worked, unlike the earlier `artic.edu` 402s), Song Dynasty Landscape Painting (3 works, all **VERIFIED** the same way, 2026-07-21), and Mughal Miniature Painting (3 works, all **VERIFIED** the same way, 2026-07-21). Ashcan School's 4 VERIFIED works are written up in curriculum-outline.md §23 but not yet in `examples.manifest.json` (confirmed absent: no `exampleWorks` field on the `ashcan-school` entry in `stores/seeds/academyStyles.ts` as of 2026-07-19). American Regionalism's 4 works are written up in curriculum-outline.md §24 (sourced, but marked "unverified this cycle" — `WebFetch` to museum hosts returned HTTP 402 through the session egress proxy) | Blocked on media-server write access — same blocker as t-033 (confirmed 2026-07-19: `examples.manifest.json` lives on `media.acrocatranch.com`, not in the kind_robots git repo; this session has `KR_API_TOKEN` but no `KR_RELAY_TOKEN`/`KR_RELAY_USER_ID` and found no in-repo upload path, so it cannot write the manifest or upload images from here). Research/sourcing is already done (curriculum-outline.md §23-27); only the write step remains, plus a direct-fetch spot-check of §24's four URLs when museum/Commons egress is open. Resume once a session with media-server/relay write access is available — do not re-attempt from a sandbox without it |
| Starter library | 21 starter images and provenance manifest complete — coverage intentionally movement-agnostic (2026-07-18: confirmed no movement-specific starters exist for any of the 8 movements added after v1, and an abstract Suprematist work would fail the library's own selection criteria; see starter-image-library.md) | Keep source-picker integration aligned with the manifest; no new starter entries needed |
| Style previews | 27 prompts queued (Suprematism queued 2026-07-18, `kind-robots-academy-style-preview-suprematism`; Ashcan School queued the same cycle it was added, `kind-robots-academy-style-preview-ashcan-school`; American Regionalism queued 2026-07-19, `kind-robots-academy-style-preview-american-regionalism`; Persian Miniature Painting queued 2026-07-20, `kind-robots-academy-style-preview-persian-miniature`; Song Dynasty Landscape Painting queued 2026-07-21, `kind-robots-academy-style-preview-song-dynasty-landscape`; Mughal Miniature Painting queued 2026-07-21, `kind-robots-academy-style-preview-mughal-miniature`; all in `art-prompts.yaml`). All 27 are still `status: pending` — the home relay is not claiming jobs (2026-07-20 ~10:04Z: job 816 accepted but never claimed after 10+ minutes; 2026-07-20 ~17:12Z: fresh job 957 also accepted but still `status: PENDING`/unclaimed; 2026-07-21 ~04:06Z: fresh job 1184 also accepted but still `status: PENDING`/unclaimed; 2026-07-21 ~14:xx UTC: fresh job 1242 also accepted but still `status: PENDING`/unclaimed, `updatedAt` unchanged since creation) | Blocked on home-relay reachability, not on this queue. Re-run `python scripts/consume_art_requests.py --id-prefix "kind-robots-academy-style-preview-" --live` with a fresh job (not 816, 855, 957, 1014, 1175, 1184, or 1242) once relay/DB state is confirmed to have changed |
| Remix configs | Registry exists; A/B generation blocked | Resume only after the relay, database, and approved generation path are available |
| Teaching scaffold | Written in `docs/teaching-notes.md`, covering all 27 movements including Mughal Miniature Painting (row 27 added 2026-07-21, this cycle); wired into `academy-style-detail.vue`'s Try It / Reflect sections (t-023, done — verified 2026-07-18 via `grep -n "Try it\|Reflect" components/academy/academy-style-detail.vue` on kind_robots main) | Coverage complete; no open action |

## Blocker discipline

Do not re-probe a blocker when the roadmap already contains fresh evidence with the same failure signature. Recheck only when capabilities, credentials, egress, relay state, database state, or instructions materially change.

A soft blocker never consumes the whole recurring cycle. Rotate to another lane and land a reversible improvement.

## Completion test

A `t-010` cycle is complete when all of the following are true:

- exactly one primary lane was selected;
- the change is scoped and reversible;
- verification is recorded;
- no live generation, publishing, deployment, spend, secrets, or production mutation occurred;
- **if the cycle opened a kind_robots PR, its CI status was polled and the PR was
  either merged or explicitly left open with a documented reason** (do not treat
  "PR opened" as the cycle's terminal state — a green, unmerged PR stranded at
  session end is not done; see the PR #814/t-036 incident below);
- the recurring task is rearmed to `ready` after merge.

Kaizen from a Reviewer pass, 2026-07-21 (t-036): a lane-1 cycle opened kind_robots
PR #814 (all 3 CI checks green) but ended the session without merging it or
rearming `t-010`, leaving the recurring task stranded at `status: claimed` with an
unmerged-but-green PR — the same failure shape as the earlier PR #942 incident
logged in this task's own roadmap note (2026-07-21 ~01:00 UTC: status field never
flipped after a merge). A later Reviewer-role session had to notice the open PR,
verify CI, and merge + rearm manually. The bullet above closes this gap for every
lane, not just lane 1 — any cycle that opens a kind_robots PR owns polling its CI
and merging (or explicitly parking it) before the cycle ends.
