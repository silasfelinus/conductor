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

- Last completed lane: Curriculum depth (lane 4), 2026-07-27 (scheduled conductor
  agent run, session claude-scheduled-20260727T000607Z-aa-t010-lane4-precisionism).
  Per the prior cycle's note, lane 2 (roadmap accuracy) had just run
  (2026-07-26T23:03:57Z), so lane 3 was next in the 1→2→3→4 rotation.
  Re-probed lane 3 with `scripts/recheck_render_queue.py`: still `growing` —
  PENDING=144 (up from 114), oldestPending job 2017 now ~61.1h old (up from
  ~57.1h), 24h window newly-PENDING=142 vs. DONE=34. Fell back to lane 4 per
  the checklist's own fallback rule (see RENDER-BACKLOG.md for the full
  stamped entry). Promoted Precisionism from
  `docs/curriculum-candidates/precisionism.md` into `curriculum-outline.md`
  as section 33 (v1.13): the candidate named four figures (Demuth, Sheeler,
  Crawford, O'Keeffe) but only Demuth (d. 1935) clears
  PUBLIC-DOMAIN-POLICY.md §1.3's 1956 death-date prong — the other three
  died after 1956 and are excluded from the generation target and from
  exhibited example works, named only as historical-context prose (matching
  how Picasso/Braque and Thomas Hart Benton are handled elsewhere in
  curriculum-outline.md). Verified all three of Demuth's example works
  directly via live Wikimedia Commons file pages (*My Egypt* 1927, PD-Art
  PD-old-auto-expired; *I Saw the Figure 5 in Gold* 1928, Met Open Access
  CC0 1.0; *Incense of a New Church* 1921, PD-Art PD-old-auto-expired). Did
  every axis together in one pass, following the Hudson River School cycle's
  precedent rather than backfilling piecemeal: skeleton YAML entry, section
  33 prose, a remix-quality paragraph in "Lesson-only vs remixable", a
  `v1.13 addition re-check` public-domain paragraph, a
  `style-lora-registry.md` row, `teaching-notes.md` row 33, and
  `kind-robots-academy-style-preview-precisionism` in `art-prompts.yaml`.
  Marked `docs/curriculum-candidates/precisionism.md` itself `PROMOTED`.
  Updated this checklist's "Current curriculum coverage" table (32→33 across
  every row) and rotation state. Front-end sync to `academyStyles.ts`
  deliberately deferred, matching every prior promotion. Verified:
  `yaml.safe_load` on curriculum-outline.md's machine-readable skeleton (33
  entries, no duplicate slugs, `precisionism` present) and on
  `art-prompts.yaml` (201 requests, no duplicate ids); `scripts/audit_roadmaps.py`
  and `scripts/validate_roadmaps.py` both clean after all edits.
  Conductor-docs-only change (curriculum-outline.md, style-lora-registry.md,
  teaching-notes.md, art-prompts.yaml, this checklist, the candidate file,
  roadmap.yaml, RENDER-BACKLOG.md); no kind_robots PR needed this cycle. Next
  preferred lane is front-end polish (lane 1) — this cycle ran lane 4 (via
  fallback from a blocked lane 3), so lane 1 is next in the 1→2→3→4
  rotation. Rearmed to `ready`.
- Last completed lane: Roadmap accuracy (lane 2), 2026-07-26T23:03:57Z
  (claude-scheduled-20260726T230357Z-aa-t010-lane2, scheduled conductor
  agent run; entry backfilled 2026-07-27, this cycle — the run itself was
  already recorded in `continuous-improvement-run-log.md` and the task's own
  `continuous_improvement`/note fields, but this rotation-state section
  skipped a matching entry, the same one-cycle-lag gap this section calls
  out elsewhere). Flipped milestone m3 (Curriculum content) from
  `in-progress` to `done` — all 4 of its tasks were already `status: done`.
  Condensed t-035's stacked home-relay recheck notes into one current-state
  block. `audit_roadmaps.py`/`validate_roadmaps.py` clean; `check_pr_merged_drift.py`
  skipped (GitHub API 403'd this session) in favor of a manual GitHub MCP
  check (conductor 0 open PRs, kind_robots 1 — Silas's own unrelated draft
  #1025). Conductor-docs-only change; no kind_robots PR needed. Next
  preferred lane was inspiration assets (lane 3), per the 1→2→3→4 rotation.
- Last completed lane: Curriculum depth (lane 4), 2026-07-26 (scheduled conductor
  agent run). Preferred lane was inspiration/preview assets (lane 3); re-probed
  via `scripts/recheck_render_queue.py` (RENDER-BACKLOG.md's own shared-ledger
  tool, per t-081's kaizen — cheaper and more accountable than a hand-rolled
  stats check) and found the backlog still `growing`: PENDING=114 (down from
  135 but still net-growing per 24h window throughput, PENDING+112 vs.
  DONE+58), oldest job (2017) now ~57h old (up from ~53h). Fell back to lane 4
  per this checklist's fallback convention. Promoted Hudson River School from
  `docs/curriculum-candidates/hudson-river-school.md` into `curriculum-outline.md`
  as section 32 (v1.12) — live-verified the one remaining unverified example
  work (*The Oxbow*, Thomas Cole) via `WebFetch` of its Wikimedia Commons file
  page (Public Domain Mark 1.0, author died 1848); the other two example works
  were already verified in the source candidate. While choosing what to
  promote, found the prior lane-4 cycle's Nabis (§31) promotion had itself
  left two gaps this checklist hadn't previously caught: no entry in
  curriculum-outline.md's own machine-readable skeleton YAML block, and no
  `v1.11 addition re-check` public-domain paragraph. Backfilled both for The
  Nabis in the same pass. This cycle's Hudson River School promotion got
  every axis done together instead: skeleton entry, section 32 prose, a
  remix-quality paragraph in "Lesson-only vs remixable", a `v1.12 addition
  re-check` paragraph, a style-lora-registry.md row, teaching-notes.md row 32,
  and `kind-robots-academy-style-preview-hudson-river-school` in
  `art-prompts.yaml` (mirroring the existing 31 entries' shared-subject prompt
  shape). Marked `docs/curriculum-candidates/hudson-river-school.md` itself
  PROMOTED. Verified: `yaml.safe_load` on both the curriculum-outline.md
  machine-readable skeleton (32 entries, no duplicate slugs, `hudson-river-school`
  and `the-nabis` both present) and `art-prompts.yaml` (200 requests, no
  duplicate ids); `scripts/audit_roadmaps.py` (0 errors, 0 warnings, 56 info)
  and `scripts/validate_roadmaps.py` (valid) both clean after all edits.
  Conductor-docs-only change; no kind_robots PR needed (front-end sync
  deliberately deferred, matching every prior promotion). Next preferred lane
  is front-end polish (lane 1), per the 1->2->3->4 rotation (a
  blocked-then-fallback cycle doesn't reset the sequence). Rearming to ready.
- Last completed lane: Roadmap accuracy (lane 2), 2026-07-26 (~18:05-18:25 UTC,
  claude-conductor-burst-20260726T1802Z-aa-t010-lane2, scheduled burst-mode
  cycle). Per the prior cycle's note, lane 2 was next after lane 4 ran.
  `scripts/audit_roadmaps.py`: 0 errors, 0 warnings, 56 info — a real
  improvement over the long-standing 12-warning baseline (the
  `ACTIVE_PROJECT_ALL_DONE`/`ACTIVE_PROJECT_NO_OPEN_TASKS` warnings this
  checklist has left alone since 2026-07-20 pending Silas's call) — confirmed
  this is because `project-overrides.yaml` was updated 2026-07-26 to flip
  several of those exact projects (global-ui, ecosystem-map, humboldt-scoop,
  packmaker, engagement, challenge-center, superkate-services-calculator) to
  `finished`, resolving the warnings for real rather than the audit going
  quiet. `scripts/validate_roadmaps.py`: valid. `scripts/check_pr_merged_drift.py`
  flagged 2 unresolved candidates: this task's own kind_robots#1017 (my own
  in-progress claim, not drift) and animation-manager/t-013's historical
  kind_robots#887 reference (spot-checked via GitHub MCP `pull_request_read` —
  confirmed merged 2026-07-22, but t-013 itself is mid-closeout by a concurrent
  session with its own open PR #1160, not this project's concern). All 6
  milestones re-verified programmatically against actual task statuses — no
  drift (m1 done/0 open, m2 in-progress/t-004 ready, m3 in-progress/t-033
  needs-human, m4 done/0 open, m5 in-progress/t-009+t-019 ready, m6
  in-progress/t-010 claimed+t-035 ready). Spot-checked t-019's blocker for
  currency: `public/images/academy/styles/` still 404s in kind_robots (via
  GitHub MCP `get_file_contents`) — no change. Per t-004's own standing
  instruction, did NOT re-run the render-queue-stats check this cycle (no
  reason to believe it moved since the 2026-07-26T13:06Z reading).
  **Real finding, not just a clean audit:** the immediately-prior lane-4
  cycle's Nabis promotion (above) updated curriculum-outline.md and
  style-lora-registry.md but silently skipped the two per-movement follow-ups
  every prior addition (§17-30) got in the *same* cycle — a `teaching-notes.md`
  row and an `art-prompts.yaml` style-preview prompt — leaving The Nabis
  quietly behind on both axes the same way ashcan-school once fell behind on
  example works (t-041's kaizen). Backfilled both this cycle: row 31 in
  `teaching-notes.md` (mirroring row 30's shape, sourced from
  curriculum-outline.md §31's key-ideas/recognition-cues and the "Lesson-only
  vs remixable" section's existing Nabis risk paragraph — no new facts
  invented) and `kind-robots-academy-style-preview-the-nabis` in
  `art-prompts.yaml` (mirroring the other 30 entries' shared-subject prompt
  shape exactly). Also fixed the "Current curriculum coverage" section below,
  which still said "30 movement entries" / "before adding a 31st movement" —
  stale since the lane-4 cycle above already added the 31st. Verified
  `yaml.safe_load` on `art-prompts.yaml` (200 requests, 31 style-preview
  entries, `the-nabis` present) and re-ran `scripts/audit_roadmaps.py` /
  `scripts/validate_roadmaps.py` after all edits — still 0 errors, 0 warnings,
  valid. Conductor-docs-only change (this checklist + teaching-notes.md +
  art-prompts.yaml + roadmap.yaml); no kind_robots PR needed. Next preferred
  lane is inspiration/preview assets (lane 3) — this cycle ran lane 2, so
  lane 3 is next in the 1→2→3→4 rotation; re-probe with a fresh queued job
  per t-004/t-035's blocker-discipline convention.
- Last completed lane: Curriculum depth (lane 4), 2026-07-26 (~16:07-16:20 UTC,
  claude-conductor-agentrun-20260726T160754-aa-t010-nabis-promote, scheduled
  agent run). Preferred lane was inspiration/preview assets (lane 3); re-probed
  via `GET /api/art/queue/stats` first (cheaper than a live job) and found the
  backlog unchanged-to-slightly-worse (136 PENDING vs. 132 last check, oldest
  ~53h vs. ~50h) plus a new `WinError 10061` connection-refused signature from
  the relay's own ComfyUI call — fell back to lane 4 per this checklist's own
  rule. Promoted the most complete unpromoted entry in
  `docs/curriculum-candidates/` (The Nabis) into `curriculum-outline.md` as
  section 31 (v1.11), sourcing and verifying its 3 required example works via
  live Wikimedia Commons file-page fetches (Sérusier's *The Talisman*,
  Vuillard's *The Yellow Curtain*, Denis's *Homage to Cézanne* — all confirmed
  public domain). Also updated `style-lora-registry.md`'s mapping table and
  marked the candidate file itself promoted. Note: this Rotation-state section
  had drifted 2 cycles stale (the front-end-polish/PR#1015 and roadmap-
  accuracy/PR#1149 cycles both said in the run log that they updated this
  section but hadn't actually — fixed now by recording this entry directly;
  no separate task filed since it's a one-line self-correcting drift, not a
  recurring pattern yet). Next preferred lane is front-end polish (lane 1),
  per the 1->2->3->4 rotation (a blocked-then-fallback cycle doesn't reset the
  sequence, same convention as every prior lane-3-blocked cycle).
- Last completed lane: Roadmap accuracy (lane 2), 2026-07-25 (~21:05-21:15 UTC,
  claude-conductor-burst-20260725T2100Z-t010-lane2, scheduled burst-mode cycle).
  Per the prior cycle's note, lane 2 was next after lane 1 ran.
  `scripts/audit_roadmaps.py` clean (0 errors, 12 warnings, 42 info — identical
  to the immediately-prior lane-2 cycle's baseline). `scripts/check_pr_merged_drift.py`
  flagged 42 unverifiable-via-sandbox candidates (up from 31, purely from this
  task's and model-builder/t-029's growing PR-reference history); spot-checked
  the newest (kind_robots#962) via GitHub MCP `pull_request_read` — confirmed
  merged, 10/-0/1-file, no drift. All 6 milestones re-verified programmatically
  against actual task statuses — no drift. Spot-checked t-019's blocker for
  currency: `public/images/academy/styles/` still absent in kind_robots — no
  change. Conductor-docs-only change (roadmap.yaml + this checklist); no
  kind_robots PR needed. Next preferred lane is inspiration/preview assets
  (lane 3) — this cycle ran lane 2, so lane 3 is next in the 1→2→3→4 rotation;
  re-probe with a fresh queued job.
- Last completed lane: Front-end polish (lane 1), 2026-07-25 (~20:03-20:27 UTC,
  claude-conductor-agentrun-20260725T2003Z-t010-lane1, scheduled agent run). Per
  the prior cycle's note, lane 1 was next after lane 2 ran (it hadn't run since
  ~15:06 UTC, over 4 hours). Dispatched a general-purpose subagent over the
  in-scope surface with this checklist's exclusion list of every bug class
  already fixed across PRs #275-#955+. Found a real, previously-unfixed gap in
  `art-styler.vue`'s `handleFileSelect()`/`handleDrop()`: the MIME-rejection
  branches (added in PR #733) only ever set `errorMessage`, never clearing a
  leftover `successMessage` from a prior generation, so a stale "Style
  applied!" banner could render right alongside a new rejection error — every
  other selection path in the file already clears both messages together.
  Fixed by adding `successMessage.value = ''` to both rejection branches.
  `npx prettier --check` reproduces one pre-existing, unrelated warning
  (confirmed present on main too); `npx eslint`/`nuxi prepare` couldn't run in
  this sandbox (known limitation). kind_robots PR #962: all 5 CI checks green,
  merged squash `bfbfb792`. Next preferred lane is roadmap accuracy (lane 2) —
  this cycle ran lane 1, so lane 2 is next in the 1→2→3→4 rotation. Rearmed to
  `ready`.
- Last completed lane: Roadmap accuracy (lane 2), 2026-07-25 (~19:03-19:10 UTC,
  claude-conductor-agentrun-20260725T1903Z-t010-lane2, scheduled agent run). Per
  the prior cycle's note, lane 2 was next after lane 3 ran (with a front-end-sync
  fallback). `scripts/audit_roadmaps.py` clean (0 errors, 12 warnings, 42 info —
  same established baseline, info count down slightly from 44 to 42 as tasks
  closed out, not a new finding). `scripts/check_pr_merged_drift.py` flagged its
  usual 31 unverifiable-via-sandbox candidates; spot-checked the newest
  (kind_robots#952) via GitHub MCP `pull_request_read` — confirmed merged,
  34/-4/1-file, matches this checklist's own record exactly, no drift. All 6
  milestones re-verified programmatically against actual task statuses — no
  drift. Spot-checked t-019's blocker for currency: `public/images/academy/styles/`
  still absent in kind_robots, consistent with lane 3's just-completed
  relay-backlog finding — no change. Conductor-docs-only change (roadmap.yaml +
  this checklist); no kind_robots PR needed. Next preferred lane is front-end
  polish (lane 1) — it hasn't run since the ~15:06 UTC cycle (over 4 hours),
  more overdue than any other lane at this point. Rearmed to `ready`.
- Last completed lane: Inspiration/preview assets (lane 3), 2026-07-25
  (~17:35-18:10 UTC, claude-conductor-burst-20260725T1800Z-t010-lane3, scheduled
  burst-mode cycle). Per the prior cycle's note, lane 3 was next after lane 2 ran,
  with instructions to re-probe with a fresh queued job rather than assume either
  the old fully-stuck signature or a clean recovery. Checked `GET
  /api/art/queue/stats`: relay remains in the "backlogged, not stuck" state first
  seen last cycle (RUNNING 1, DONE 1445/24h; 52 PENDING, oldest ~31h old, down
  slightly from 59/~30h) — progressing, not regressed, but still impractically
  slow for a live probe. Queued a genuinely fresh job (2296,
  greek-vase-painting.webp, not 816/855/957/1014/1175/1184/1242/1426) via
  `consume_art_requests.py --live --limit 1 --timeout 75`: still queued/running
  after 75s, consistent with the backlog depth rather than a new failure mode.
  Per the checklist's own fallback rule, did not burn the whole cycle on a
  known-slow blocker: while checking, found all three of this task's own most
  recent curriculum-depth (lane 4) additions — Fayum Mummy Portraits (§28,
  2026-07-22), Vienna Secession (§29, 2026-07-24), and Joseon Dynasty Korean Genre
  Painting (§30, 2026-07-25) — were still un-synced to kind_robots'
  `stores/seeds/academyStyles.ts` (confirmed via direct `grep` on the live file:
  only 27 of 30 curriculum slugs present), a real backlog since front-end sync
  had been deliberately deferred each time it was added. Synced all three in one
  kind_robots PR, following the mughal-miniature/persian-miniature/etc. entry
  shape exactly (slug, name, era, sortYear, region, keyIdeas, recognitionCues,
  artists, failureMode, remix.template) sourced directly from this task's own
  curriculum-outline.md §28-30 and teaching-notes.md rows 28-30 — no new research,
  pure transcription of already-VERIFIED content. `npx prettier --check` on the
  changed file matches main's pre-existing (unrelated) formatting-check failure
  exactly — confirmed by stashing the change and re-running against main's
  version of the file, same warning, so not a regression introduced by this PR;
  kept the diff scoped to only the three new entries (reverted an incidental
  quote-style reformat prettier made to the pre-existing Ustad Mansur note).
  `npx eslint`/`nuxi prepare` could not run in this sandbox (no `node_modules`,
  `@nuxt/kit` unresolved — same known limitation as every prior lane-1/lane-3
  cycle); relied on kind_robots CI instead. Updated this checklist's "Current
  curriculum coverage" section to 30/30 synced and refreshed the style-previews
  row with the new backlog numbers and job id. Next preferred lane is roadmap
  accuracy (lane 2) — this cycle ran lane 3 (with a front-end-sync fallback), so
  lane 2 is next in the 1→2→3→4 rotation, though lane 1 (front-end polish) hasn't
  run since the ~15:06 UTC cycle and may also be due; whichever session picks up
  next should use judgment if both look overdue. Rearmed to `ready`.
- Last completed lane: Roadmap accuracy (lane 2), 2026-07-25 (~17:05-17:30 UTC,
  claude-conductor-burst-20260725T1700Z-t010-lane2, scheduled burst-mode cycle).
  Per the prior cycle's note, lane 2 was next after lane 1 ran. `audit_roadmaps.py`
  (0 errors, 12 warnings, 44 info — same baseline) clean. `check_pr_merged_drift.py`
  flagged its usual 31 unverifiable-via-sandbox candidates (all this task's own
  historical PR references); spot-checked the newest, kind_robots#952, via GitHub
  MCP `pull_request_read` — confirmed merged, diff matches this checklist's own
  record exactly, no drift. All 6 milestones re-verified programmatically against
  actual task statuses (m1 done/0 open, m2 in-progress/t-004 needs-human, m3
  in-progress/t-033 needs-human, m4 done/0 open, m5 in-progress/t-009 needs-human
  + t-019 ready, m6 in-progress/t-010 claimed + t-035 ready) — all six already
  match, no drift. While spot-checking lane 3's relay health with a fresh,
  authenticated `GET /api/art/queue/stats` (not a queued job this time — cheaper
  check, same intent), found the relay is no longer in the fully-stuck
  never-claimed state every prior lane-3 check has hit since 2026-07-18
  (RUNNING: 1, DONE: 1438 in the last 24h) but is backlogged (59 PENDING, oldest
  ~30h old) and its `recentFailed` list surfaced a genuine, previously-undocumented
  production bug distinct from the coloring-book/t-030 seed-overflow finding: three
  daily-dream reward-art jobs (2219/2220/2221, all from 2026-07-24 21:37-21:47 UTC)
  permanently FAILED with "Kind Robots media job imagePath must begin with
  public/images/" even though their `imagePath` (`public/rewards/favor/*.webp`)
  is the project's own correct, established convention for reward art (confirmed:
  `public/rewards/` is a real top-level directory in kind_robots, sibling to
  `public/images/`, matching 18 existing `art-prompts.yaml` entries and the header
  note in `scripts/dream_slug_image_cleanup.py`). Root-caused to
  `ops/home-server/relay_media_agent.py`'s `direct_media_relative()`, which only
  recognizes `public/images/...`. Not fixed inline — different project (dream-cycle,
  not ai-art-academy) and out of lane 2's docs-only scope, and a naive fix would
  silently write the file to the wrong physical folder on Silas's box rather than
  just failing loudly (see the filed task for why). Filed as
  `dream-cycle/t-019` (ready) with full root-cause detail, exact job ids, and the
  two fix-shape options for whoever picks it up, per hard rule 6. Conductor-docs-only
  change (this checklist + `dream-cycle/roadmap.yaml`); no kind_robots PR needed.
  Next preferred lane is inspiration/preview assets (lane 3) — this cycle ran lane
  2, so lane 3 is next in the 1→2→3→4 rotation; per the relay-stats check above,
  re-probe with a fresh queued job rather than assuming either the old
  fully-stuck signature or a clean recovery.
- Last completed lane: Front-end polish (lane 1), 2026-07-25 (~15:06-15:33 UTC,
  claude-conductor-scheduled-20260725T1506Z-t010-lane1, scheduled agent run). Per
  the prior cycle's note, lane 1 was next after lane 4 ran. Dispatched a
  general-purpose subagent over the in-scope surface with this checklist's
  exclusion list of every bug class already fixed across PRs #275-#1022. Found a
  real, previously-unfixed gap in `art-styler.vue`'s `runStyleTransfer()`: no
  interactive selection element (style grid, source tabs, gallery/starter
  selection, upload dropzone, "Clear source") was disabled while `isGenerating`
  was true, so switching style/source or clearing the source mid-generation let
  the original request's `resultImage`/`successMessage`/`errorMessage` write
  land on top of the new selection once it resolved — silently reattaching a
  stale result or reviving a cleared preview. Distinct from the prior
  source-selection token races (PRs #831/#849/#899, which guard the *selection
  fetches* against each other) — this guards the *generation call* against
  later selection changes. Fixed with a `generationToken` counter following the
  established `sourceSelectionToken` pattern, bumped by every selection-changing
  action; the `generated` event still fires unconditionally so downstream
  credit (`academyStore.markStyleRemixed`) is unaffected. Verified: eslint/
  prettier clean, full-project `vue-tsc --noEmit` 0 new errors (pre-existing
  unrelated Prisma-schema errors elsewhere confirmed present on main before this
  change). kind_robots PR #952, all 5 CI checks green, merged squash `7b0193b`.
  Next preferred lane is roadmap accuracy (lane 2) — this cycle ran lane 1, so
  lane 2 is next in the 1→2→3→4 rotation.
- Last completed lane: Curriculum depth (lane 4), 2026-07-25 (~14:30-15:05 UTC,
  claude-conductor-agentrun-20260725T1430Z-t010-lane4, scheduled agent run,
  falling forward from a blocked lane 3 — same live art-generation relay check
  as every prior lane-3 attempt since 2026-07-18). Per the prior cycle's note,
  lane 2 (roadmap accuracy) had just run, so lane 3 was next in the 1→2→3→4
  rotation; lane 3 stayed blocked (same session claim note, not re-probed this
  pass since the immediately-prior cycle already reconfirmed it fresh), so this
  cycle fell forward to lane 4. Added a 30th movement: Joseon Dynasty Korean
  Genre Painting (`joseon-genre-painting`, curriculum-outline.md §30) — a
  fourth non-Western entry and the first from Korea, chosen specifically for
  visual distinctness from every existing Asian entry (Song Dynasty's
  monumental monochrome peaks, Ukiyo-e's flat multi-block color, Mughal's dense
  courtly ornament): loose economical brush-line genre scenes of Joseon-era
  commoners on nearly blank paper, no background, no gold, no dense border.
  All three example works confirmed **VERIFIED** directly via WebFetch of their
  live Wikimedia Commons file pages (this session had working egress to
  `commons.wikimedia.org`): Kim Hong-do's *Ssireum* (Korean Wrestling) and
  *Seodang* (The Village School), both late 18th century from his *Danwon
  pungsokdo cheop* album (National Treasure 527), rights template `PD-Art
  (PD-old-100)` plus Creative Commons Public Domain Mark 1.0; and Sin Yun-bok's
  *Wolha jeongin* (Moonlit Lovers), c. 1805, rights template reading "life plus
  70 years or fewer" plus the same PD Mark 1.0. Both artists (Kim Hong-do,
  1745-c.1806; Sin Yun-bok, 1758-after 1813) died over 200 years ago and all
  three works predate the 1930 US-publication cutoff by over a century —
  clears PUBLIC-DOMAIN-POLICY.md §1.3's both-prongs rule with a wide margin,
  matching the §22-23/§25-27/§29 direct-file-page-verification precedent
  rather than a web-search-snippet check. Deliberately chose Kim Hong-do's
  tamer genre scenes (wrestling, a classroom) and Sin Yun-bok's most
  G-rated well-known work (a fully-clothed moonlit courtship scene) over
  either artist's more explicit "chunhwado"/erotic-genre output, consistent
  with the Academy's general-audience framing — not a PD-policy requirement,
  but worth recording since Sin Yun-bok's oeuvre includes both registers.
  Queued the style-preview prompt in `art-prompts.yaml`
  (`kind-robots-academy-style-preview-joseon-genre-painting`), still subject to
  the same lane-3 backlog/blocker as the other 29. Added the placeholder row
  to `style-lora-registry.md`'s curriculum-slug-mapping table and row 30 to
  `teaching-notes.md` (mode `prompt`, difficulty Medium — flagged risk: the
  model likely keeps the source photo's real background under a thin
  ink-wash filter instead of genuinely emptying the frame, reading as generic
  "sumi-e" rather than pungsokhwa's actual near-blank-paper look). Also added
  a distinguishing-risk paragraph to curriculum-outline.md's "Lesson-only vs
  remixable" section contrasting this movement's "empty the frame" risk with
  `song-dynasty-landscape`'s "discard-the-photo's-composition" risk, since
  both share the same ink-and-wash family but fail in opposite directions.
  Front-end sync to `academyStyles.ts` deliberately deferred to a future
  cycle, matching how persian-miniature/song-dynasty-landscape/
  mughal-miniature/fayum-mummy-portraits/vienna-secession landed across
  separate cycles. Verified the curriculum-outline.md machine-readable
  skeleton parses as 30 entries (`yaml.safe_load` on the extracted block) and
  `art-prompts.yaml` parses clean (188 requests). Conductor-docs-only change;
  no kind_robots PR needed this cycle (front-end sync deferred, as above).
  Updated this checklist's rotation state; next preferred lane is front-end
  polish (lane 1) — this cycle ran lane 4, so lane 1 is next in the
  1→2→3→4 rotation.
- Last completed lane: Roadmap accuracy (lane 2), 2026-07-25 (~13:04-13:20 UTC,
  claude-conductor-agentrun-scheduled-t010-lane2, scheduled agent run). Per the
  prior cycle's note, lane 2 was next after lane 1 ran. `audit_roadmaps.py` (0
  errors, 12 warnings, 44 info — same baseline) and `check_pr_merged_drift.py`
  (30 unverifiable-via-sandbox candidates, spot-checked the newest kind_robots#947
  via GitHub MCP — confirmed merged, no drift) both clean. All 6 milestones
  re-verified programmatically against actual task statuses — no drift. While
  spot-checking lane 3's relay health, found and filed a genuine unrelated
  production bug: `coloring-book/t-030` — 17+ ArtJobs permanently failing on a
  seed-overflow error (`ArtImage.seed` is a 32-bit Prisma `Int`, but the shared
  fallback seed generator produces values up to 10^15). Root-caused to specific
  file:line locations via a subagent reading kind_robots source; not fixed
  inline (different project, out of lane 2's docs-only scope — filed as a new
  `ready` task instead, per hard rule 6). Conductor-docs-only change; no
  kind_robots PR needed. Next preferred lane is inspiration/preview assets
  (lane 3, recheck with a fresh queued job).
- Last completed lane: Front-end polish (lane 1), 2026-07-25 (~12:05-12:20 UTC,
  claude-conductor-burst-20260725T120528-t010, scheduled burst-mode cycle). Per
  the prior cycle's note, lane 1 was next after lane 4 ran. Found a real,
  previously-unfixed bug in `image-upload.vue`'s `handleBatchUpload()`: the
  `isUploading` flag flips back to `false` as soon as the network call
  settles, but the handler keeps running afterward (checkmark-display pause +
  queue filtering), leaving the Upload/Remove/Clear buttons re-enabled and the
  function's own re-entry guard bypassable during that window — a second
  click could re-upload already-succeeded files, creating duplicate
  `ArtImage` rows. Fixed with a new `isFinalizingUpload` flag held for the
  whole function body. kind_robots PR #947, all 5 CI checks green, merged
  squash `5d9148a`. See the full RAN entry on the roadmap task for details.
  Next preferred lane is roadmap accuracy (lane 2).
- Last completed lane: Curriculum depth (lane 4), 2026-07-24 (~16:45-17:10 UTC,
  claude-conductor-agentrun-20260724T1730Z-t010b, scheduled agent run). Per the
  prior cycle's note, lane 3 (inspiration/preview assets) was next — tried first
  with a genuinely fresh queued job (job 2195, greek-vase-painting.webp, not
  1426/1173/957/etc.): `GET /api/art/queue/stats` shows the home relay is no
  longer fully stalled (a real change from every prior cycle's "never claimed"
  signature) — `RUNNING: 1`, `DONE: 46` in the last 24h window, 141 images
  created — but severely backlogged: 132 jobs `PENDING`, oldest queued at
  11:00 UTC (~5.8h old at check time) and job 2195 itself still `PENDING`
  after a 45s wait. This is a queue-depth/throughput problem on hardware this
  sandbox can't act on (per BOUNDARY.md), not the same failure mode as the
  earlier fully-stuck signature — worth noting for whoever next checks lane 3,
  since "still blocked" no longer accurately describes it; "queued but slow"
  does. Fell back to lane 4 per the checklist's own fallback rule. Added a
  29th movement: Vienna Secession (`vienna-secession`, curriculum-outline.md
  §29) — a single-named-artist (Gustav Klimt, d. 1918) entry whose defining
  visual signature (flat ornamental gold-leaf pattern beside a photorealistic
  face) is distinct from every prior gold-adjacent entry (`byzantine-mosaic`'s
  tesserae, `illuminated-manuscript`'s gold-as-illumination, `gothic`'s gold
  ground). All three example works (*The Kiss* 1907-08, *Portrait of Adele
  Bloch-Bauer I* 1907, *Judith I* 1901) confirmed **VERIFIED** directly via
  the Wikimedia Commons API's `extmetadata` rights-status categories
  (`PD-old-100-expired`, `CC-PD-Mark`) — this session had working egress to
  `commons.wikimedia.org` (confirmed via direct `curl` to the MediaWiki API).
  Queued the style-preview prompt in `art-prompts.yaml`
  (`kind-robots-academy-style-preview-vienna-secession`), still subject to the
  same lane-3 backlog as the other 28. Added the placeholder row to
  `style-lora-registry.md` and row 29 to `teaching-notes.md` (mode `prompt`,
  difficulty Medium — flagged risk: the model may gild the whole image
  uniformly and lose the defining ornament/face contrast). Front-end sync to
  `academyStyles.ts` deliberately deferred to a future cycle, matching how
  persian-miniature/song-dynasty-landscape/mughal-miniature/fayum-mummy-portraits
  landed across separate cycles. Verified the curriculum-outline.md machine-
  readable skeleton parses as 29 entries (`yaml.safe_load` on the extracted
  block) and `art-prompts.yaml` parses clean. `tests/test_audit_roadmaps_policy.py`,
  `tests/test_validate_roadmaps.py`, `tests/test_roadmap_claims.py` pass
  (18/18); `scripts/audit_roadmaps.py` — 0 errors, 12 warnings, 44 info,
  unchanged from the prior cycle's post-fix baseline. Conductor-docs-only
  change; no kind_robots PR needed this cycle (front-end sync deferred, as
  above). Updated this checklist's rotation state; next preferred lane is
  front-end polish (lane 1) — this cycle ran lane 4, so lane 1 is next in the
  1→2→3→4 rotation.
- Last completed lane: Roadmap accuracy (lane 2), 2026-07-24 (~16:07-16:20 UTC,
  claude-conductor-burst-20260724T1730Z-t010, scheduled burst-mode cycle). Per
  the prior cycle's note, lane 2 was next in the 1→2→3→4 rotation after lane 1
  ran last. Ran `scripts/check_pr_merged_drift.py` (0 claimed/review PR
  references outstanding, nothing to reconcile) and `scripts/audit_roadmaps.py`
  (41 roadmaps, 0 errors, 13 warnings, 44 info). Diffed the warning set against
  the established 12-warning baseline (the `ACTIVE_PROJECT_ALL_DONE`/
  `ACTIVE_PROJECT_NO_OPEN_TASKS` pattern across art-generator-connect, davinci,
  ecosystem-map, humboldt-scoop, packmaker, sketchy — left alone again, same
  reasoning as every prior cycle: flipping `project-overrides.yaml` status
  needs Silas's call, not a guess) and found one genuinely new finding:
  `SLUG_MISMATCH` on `music-mentor` — its `roadmap.yaml` had
  `project: Music Mentor` instead of the directory slug `music-mentor` (the
  only mismatch across all 41 roadmaps besides the `_template` placeholder).
  This was not cosmetic: `scripts/next_ready_task.py` and `scripts/run_worker.py`
  both resolve the task's project identifier via `roadmap.get('project') or
  slug`, so any music-mentor task reaching `ready` would have surfaced as
  `Music Mentor/t-XXX` — a string `scripts/claim_task.py` can't resolve to a
  directory, breaking the claim step for that project's only real task queue.
  It also silently excluded music-mentor from `ROADMAP-AUDIT.md`'s project
  inventory table entirely (confirmed: the table jumped from row 37
  `ruler-hooked` straight to row 38 `dream-cycle` before the fix; music-mentor
  now appears correctly as row 38 with dream-cycle shifted to 39). Fixed by
  changing the field to `project: music-mentor`; verified no other script or
  data file keys off the literal string `"Music Mentor"` for lookups (only
  `art-prompts.yaml` prose/labels, which are display text, not identifiers).
  Re-ran both scripts after the fix: 12 warnings (SLUG_MISMATCH gone),
  regenerated `ROADMAP-AUDIT.json`/`.md`. Cross-checked ai-art-academy's own
  6 milestones programmatically against actual task statuses — all consistent
  (`done` milestones fully done, `in-progress` milestones have exactly the
  expected non-done tasks), no drift. `tests/test_audit_roadmaps_policy.py`
  and `tests/test_validate_roadmaps.py` pass (10/10). Conductor-only change,
  no kind_robots PR needed. Next preferred lane is inspiration/preview assets
  (lane 3) — this cycle ran lane 2, so lane 3 is next in the 1→2→3→4 rotation
  (lane 1 already ran this rotation on 2026-07-23).
- Last completed lane: Front-end polish (lane 1), 2026-07-23 (~16:11-16:18 UTC,
  claude-conductor-burst-20260723T1611Z-t010, scheduled burst-mode cycle). Per
  the prior cycle's note, lane 1 was next in the 1→2→3→4 rotation after lane 4
  ran last. Dispatched an Explore subagent to read the full checklist (building
  the exclusion list of every bug class already fixed across PRs #275-#849)
  plus every in-scope file in full. Found a real, previously-unfixed gap:
  `applySourceImageId()` — the `sourceImageId`-prop/deep-link path used by
  `/coloring-page?imageId=...` — was never wired into the `sourceSelectionToken`
  guard PR #849 introduced for the other three source-selection paths
  (upload/starter/gallery). Since `pages/coloring-page.vue` derives the prop
  reactively from `route.query.imageId` on an instance Vue Router reuses across
  query-only navigations, a slow deep-link fetch could resolve after the user
  had already picked a different source and silently overwrite it back — a
  genuine, reachable data-correctness race. Fixed by bringing
  `applySourceImageId()` into the same token guard (capture before the await,
  bail if stale after) and bumping the token in `clearSourceImage()` too,
  matching the existing pattern exactly. Verified: `npx eslint`/
  `npx prettier --check` clean on the changed file; full-project `npm run test`
  (`vue-tsc --noEmit`) confirmed zero new errors from this change. While
  polling CI, found main itself red since Build Bench (PR #897) merged
  without its own CI confirmed green: `build-bench.vue`'s "Run both" button
  called a bare `runBoth` (only `store.runBoth` exists) and
  `buildBenchStore.ts`'s `engineDef()` fallback didn't type-narrow under
  `noUncheckedIndexedAccess`. Fixed both in the same PR so CI goes green
  instead of staying red for the next push. kind_robots PR #899. Next
  preferred lane is roadmap accuracy (lane 2) — this cycle ran lane 1, so
  lane 2 is next in the 1→2→3→4 rotation.
- Last completed lane: Curriculum depth (lane 4), 2026-07-22 (~16:06 UTC,
  claude-conductor-burst-20260722T1606Z-t010, scheduled burst-mode cycle). Per
  the prior cycle's note, lane 3 (inspiration/preview assets) was next
  preferred — tried first with a genuinely fresh queued job (job 1426,
  greek-vase-painting.webp, not 816/855/957/1014/1175/1184/1242):
  `consume_art_requests.py --id-prefix "kind-robots-academy-style-preview-"
  --live --limit 1 --timeout 60` queued it but it timed out after 60s still
  queued/running — same never-claimed home-relay signature as every check
  since 2026-07-18. Also confirmed `commons.wikimedia.org` freshly reachable
  (`recheck_egress_blocks.py`, HTTP 200) before falling back. Fell back to
  lane 4 per this checklist's own instruction; per its "finish known coverage
  gaps before a 29th movement" rule, checked whether any non-relay-blocked gap
  remained first — none did (same conclusion as the 2026-07-21 ~19:10 UTC
  cycle) — so added a 28th movement instead: Fayum Mummy Portraits
  (`fayum-mummy-portraits`, curriculum-outline.md §28), the third non-Western
  entry and the first anonymous-artist entry since Byzantine Mosaic (§2). All
  3 example works confirmed **VERIFIED** directly against the Met Collection
  API (`collectionapi.metmuseum.org/public/collection/v1/objects/<id>`),
  reading each object's own `isPublicDomain` field rather than a third-party
  Commons tag — a stronger verification method than the WebFetch-Commons-page
  method used for §17-27: *Portrait of the Boy Eutyches* (Met 18.9.2, A.D.
  100-150), *Portrait of a Thin-Faced Man* (Met 09.181.3, A.D. 140-170), and
  *Portrait of a Young Woman with a Gilded Wreath* (Met 09.181.7, A.D.
  120-140) — all CC0, all anonymous ancient painters, clearing
  PUBLIC-DOMAIN-POLICY.md §1.3 with the widest margin of any addition so far
  (no named artist at all, ~1,800 years past any death-based cutoff). Also
  noticed and backfilled a real, pre-existing documentation gap while in this
  section: §27 (Mughal Miniature Painting, added 2026-07-21) never got its
  "v1.7 addition re-check" paragraph in the Public-domain safety check
  section, unlike every other addition since v1.1 — added it alongside the
  new v1.8 paragraph. Queued the style-preview prompt in `art-prompts.yaml`
  (`kind-robots-academy-style-preview-fayum-mummy-portraits`), still blocked
  on the same relay issue as the other 27. Added the curriculum-slug-mapping
  placeholder row to `style-lora-registry.md` (no dedicated LoRA search this
  cycle) and row 28 to `docs/teaching-notes.md`'s per-style table (mode
  `prompt`, difficulty **Medium** — flagged in curriculum-outline.md's remix
  tier list as the most photorealistic style in the curriculum, so its
  biggest risk is under-cooking into a generic "vintage photo" filter rather
  than the movement's actual signature traits). Front-end sync to
  `academyStyles.ts` deliberately deferred to a future cycle, matching how
  persian-miniature/song-dynasty-landscape/mughal-miniature landed across
  separate cycles. Verified `yaml.safe_load` parses clean on both
  `art-prompts.yaml` and this project's `roadmap.yaml`, and that the
  curriculum-outline.md machine-readable skeleton still parses as 28 entries.
  `scripts/audit_roadmaps.py` not re-run this cycle (no roadmap-status field
  changed by this lane's work beyond this task's own claim/rearm). Updated
  this checklist's rotation state and curriculum-coverage table above.
  Conductor-docs-only change; no kind_robots PR needed this cycle (nothing to
  sync yet — front-end sync is the deferred follow-up). Next preferred lane
  is front-end polish (lane 1) — this cycle ran lane 4, so lane 1 is next in
  the 1→2→3→4 rotation. Rearmed to `ready`.
- Last completed lane: Roadmap accuracy (lane 2), 2026-07-22 (~04:12-04:19 UTC,
  claude-conductor-scheduled-20260722T0412Z-t010). Per the prior cycle's note,
  lane 2 was next in the 1→2→3→4 rotation after lane 1 ran last. Did not
  re-probe lane 3's home-relay blocker — the immediately-prior cycle
  (~02:11-02:36 UTC, under two hours earlier) already reconfirmed it fresh
  with job 1319, no material change since. `scripts/audit_roadmaps.py` found
  real drift this cycle, not just a clean re-check: warnings had risen from
  the prior 14-warning baseline to 18 after conductor/t-079's new
  `DUPLICATE_YAML_KEY` check (PR #1005, landed 2026-07-21 evening) caught a
  genuine instance in `sketchy/roadmap.yaml` t-007 — a duplicate
  `claimed_by`/`claimed_at` pair (once before the task's `note:`, once after)
  introduced by a burst cycle appending its PROGRESS note without removing
  the original fields; both values were 3 seconds apart from the same
  session so no data was actually wrong, but YAML's last-wins semantics made
  it a latent trap for the next edit — removed the earlier duplicate. Also
  found 4 new `SOFT_NEEDS_HUMAN` warnings (conductor/t-034, conductor/t-073,
  kind-robots/t-037, kind-robots/t-043) — all four are genuinely hard gates
  (three are "Pitch: ..." tasks awaiting Silas's read/approve-or-reject
  decision, which no agent can make on the pitch author's own behalf; the
  fourth, conductor/t-073, is a GitHub branch-protection Settings change no
  available MCP tool can make) but none carried an explicit `gate_human`
  marker for the audit's heuristic to recognize, so all four got
  `gate_human: true` added — accurate metadata, not a status change, and
  resolves the false positive permanently rather than re-flagging it every
  cycle. The remaining 12 warnings (`ACTIVE_PROJECT_ALL_DONE`/
  `ACTIVE_PROJECT_NO_OPEN_TASKS` across art-generator-connect, davinci,
  ecosystem-map, humboldt-scoop, packmaker, sketchy) are a known,
  already-escalated pattern (see TALKBACK.md 2026-07-20 ecosystem-map/t-006
  entry) — flipping `project-overrides.yaml` status to `finished`/`paused`
  has precedent requiring Silas's in-session approval (see the `challenge-center`
  entry's comment), so left unchanged rather than guessed at again.
  `scripts/check_pr_merged_drift.py` flagged its usual 27 unverifiable-via-
  sandbox candidates (all this task's own historical PR references); spot-
  checked the newest, kind_robots#849, via GitHub MCP `pull_request_read` —
  confirmed merged, 24/-4/1-file, matches this file's own record exactly, no
  drift. All 6 milestones re-verified programmatically (each milestone's
  `status:` cross-checked against every task assigned to it via
  `milestone:`) — m1 (done, 0 open), m2 (in-progress, t-004 open), m3
  (in-progress, t-033 open), m4 (done, 0 open), m5 (in-progress, t-009/t-019
  open), m6 (in-progress, t-010 recurring + t-035 open) — all six already
  match, no drift. Conductor-docs-only change (roadmap.yaml x3 + this
  checklist); no kind_robots PR needed. Next preferred lane is inspiration
  and preview assets (lane 3, recheck with a fresh queued job, not 1319)
  falling back to lane 4 if still blocked.
- Last completed lane: Front-end polish (lane 1), 2026-07-22 (~02:11-02:35 UTC,
  claude-conductor-agentrun-20260722T0211Z-t010). Lane 3 (inspiration/preview
  assets) was next preferred per the prior cycle's note, tried first with a
  genuinely fresh queued job (1319, greek-vase-painting.webp): polled every
  30s for 8 rounds (~4 minutes) and it stayed `PENDING`/unclaimed the whole
  time — same never-claimed home-relay signature as every check since
  2026-07-18. Fell back toward lane 4, but its own coverage table shows every
  remaining lane-4 gap already blocked on the same relay/media-server-write
  issue (no unblocked action available before a 28th movement), so fell
  through to lane 1 instead. Dispatched an Explore subagent to read every
  in-scope Academy file in full (art-styler.vue 1600 lines, image-upload.vue
  833 lines, all components/academy/*.vue, academyStore.ts, styleHelper.ts,
  academyStyles.ts) against the exclusion list of every bug class already
  fixed in prior cycles. Found a real, verifiable cross-tab race in
  `art-styler.vue`: the source-tab buttons and gallery thumbnails are never
  disabled while a starter image is loading, so a user could click a starter
  thumbnail (slow fetch begins), switch to Gallery or Upload, pick a
  different image, and have the stale starter fetch silently overwrite that
  newer selection once it finally resolved — `selectStarterEntry()`'s success
  path wrote `uploadedImageData`/`selectedSourceImage` unconditionally, and
  the existing `gallerySelectionToken` guard only covered gallery-to-gallery
  races, not races against the other two tabs. Fixed by widening the token
  into a single `sourceSelectionToken` shared by `processUploadedFile()`,
  `selectStarterEntry()`, and `selectGalleryImage()`, so whichever selection
  happens last always wins. Caught and fixed a self-introduced regression
  during implementation before verifying: gating the `finally` block's
  `isLoadingStarterImage.value = false` reset on the token would have left
  every starter thumbnail permanently disabled (via `:disabled` in the
  template) after any stale race, since nothing else resets that flag — left
  it unconditional. Verified: `npx eslint`/`npx prettier --check` clean,
  full-project `npm run test` (`vue-tsc --noEmit`) exit 0 both before and
  after rebasing onto latest main. kind_robots PR #849, all 4 CI checks green
  (Contract verifiers, TypeScript, verify, GitGuardian), merged squash
  `f9a26d8a`. Next preferred lane is roadmap accuracy (lane 2) — this cycle
  ran lane 1, so lane 2 is next in the 1→2→3→4 rotation.
- Last completed lane: Roadmap accuracy (lane 2), 2026-07-22 (~01:40-01:50 UTC,
  claude-conductor-burst-20260722T0140Z-t010). Per blocker discipline, did not
  re-probe lane 3's home-relay blocker — the immediately-prior cycle (~00:17-00:40
  UTC, less than an hour earlier) already re-confirmed it fresh with job 1307, no
  material change since. `scripts/audit_roadmaps.py` — same 0-errors/14-warnings/
  44-info baseline, no findings touching this project. Verified the newest
  cross-repo PR reference (kind_robots#840, the immediately-prior lane-1 cycle's
  fix) via GitHub MCP `pull_request_read` — confirmed merged 2026-07-22T00:29:43Z,
  matches the checklist's own record, no drift. Re-verified all 6 milestones
  programmatically (each milestone's `status:` field cross-checked against every
  task assigned to it via `milestone:`) rather than spot-checking: m1 (done, 2/2
  tasks done), m2 (in-progress, t-004 open), m3 (in-progress, t-033 open), m4
  (done, 15/15 tasks done), m5 (in-progress, t-009/t-019 open), m6 (in-progress,
  t-010 recurring + t-035 open) — all six already match their tasks' actual
  statuses, no drift found. Conductor-docs-only change (this checklist +
  roadmap.yaml note); no kind_robots PR needed. Next preferred lane is
  inspiration/preview assets (lane 3, recheck with a fresh queued job, not 1307)
  falling back to lane 4 if still blocked.
- Last completed lane: Front-end polish (lane 1), 2026-07-22 (~00:17-00:40 UTC,
  claude-conductor-agentrun-20260722T0016Z-t010). Lane 3 (inspiration/preview
  assets) re-probed first with a fresh queued job (1307, greek-vase-painting.webp)
  — still unclaimed after queuing, same never-claimed home-relay signature since
  2026-07-18. Lane 4 deliberately skipped (the immediately-prior cycle's reasoning
  still holds: every remaining curriculum-depth gap is relay-blocked, not
  research-blocked). Dispatched a subagent to read every in-scope Academy file in
  full and found a real, verifiable gap in `art-styler.vue`'s
  `selectStarterEntry()`: `selectedStarterFile.value` was assigned only after the
  fetch resolved, in the same synchronous block as the `finally` clearing the
  loading flag — with no `await` between them, Vue batched both reactive writes
  into one render, so the loading-spinner state for starter thumbnails was dead
  code (unchanged since the starters feature shipped in #366). Fixed by setting
  `selectedStarterFile.value` immediately on click, with a rollback to `null` in
  the `catch` block. Verified: `npx eslint`/`npx prettier --check` clean,
  full-project `npm run test` (`vue-tsc --noEmit`) exit 0. kind_robots PR #840,
  all 4 CI checks green, merged squash `cc0b0ebf`. Next preferred lane is roadmap
  accuracy (lane 2) — this cycle ran lane 1, so lane 2 is next in the 1→2→3→4
  rotation.
- **Note (rotation collision):** the two entries below both cite session label
  `claude-conductor-scheduled-20260721T220455Z-t010` but are two distinct
  concurrent sessions that reused the same label (see root `TALKBACK.md`
  2026-07-21, coat-dance/t-001 for the same pattern) — not one session
  contradicting itself. Each did real, non-duplicate work on a different
  branch, so both are kept.
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
  rebase, or discard it. Fell back to lane 2:
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
  t-035 stays blocked.
- Last completed lane: Front-end polish (lane 1), 2026-07-21 (~22:04-22:21 UTC,
  claude-conductor-scheduled-20260721T220455Z-t010). Dispatched an Explore
  subagent over the full in-scope surface (art-styler.vue, image-upload.vue,
  all components/academy/*.vue, academyStore.ts, styleHelper.ts,
  academyStyles.ts) with this checklist's exclusion list of every bug class
  already fixed in prior cycles. Found a real, verifiable race condition in
  `art-styler.vue`'s `selectGalleryImage()`: rapid clicks on two different
  not-yet-cached gallery thumbnails fire overlapping `getArtImageById()`
  fetches with no way to discard a stale response — whichever resolves last
  unconditionally wins regardless of click order, silently snapping
  `selectedSourceImage` back to a no-longer-selected image. Fixed with a
  monotonic `gallerySelectionToken` guard on both the success and catch
  branches' writes to `selectedSourceImage.value`; the `galleryThumbs` cache
  write still happens unconditionally (harmless). Verified: `npx
  eslint`/`npx prettier --check` clean, full-project `npm run test`
  (`vue-tsc --noEmit`) exit 0. kind_robots PR #831 (branch
  `claude/vigilant-edison-kjvawv`): all 3 CI checks green (TypeScript,
  Contract verifiers, GitGuardian) — merged squash `5920dbe4`.
- Both lane 1 and lane 2 ran this rotation (see collision note above). Next
  preferred lane is inspiration and preview assets (lane 3) — lane 3 stayed
  blocked on the home-relay preview-job backlog as of the lane-2 cycle's
  spot check above; re-probe with a fresh job id.
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

The Academy currently has 33 movement entries in `curriculum-outline.md` —
Precisionism (§33) was promoted from
`docs/curriculum-candidates/precisionism.md` this cycle (2026-07-27,
scheduled agent run, lane 4 — lane 3/inspiration-assets re-confirmed blocked
via `scripts/recheck_render_queue.py`, PENDING=144/oldestPending~61h/still
`growing`, before falling back). Precisionism's source candidate named four
figures (Demuth, Sheeler, Crawford, O'Keeffe) but only Demuth (d. 1935)
clears PUBLIC-DOMAIN-POLICY.md's 1956 death-date cutoff — the other three
died after 1956 and are excluded from the generation target and from
exhibited example works, named only as historical-context prose (same
treatment as Picasso/Braque in Cubism and Thomas Hart Benton in American
Regionalism). Verified all three of Demuth's example works (*My Egypt* 1927,
*I Saw the Figure 5 in Gold* 1928, *Incense of a New Church* 1921) directly
via live Wikimedia Commons file pages. Did every axis together in one cycle:
skeleton YAML entry, section 33 prose (key ideas, recognition cues, artist
note, 3 verified example works, remix_hint), a remix-quality paragraph in
"Lesson-only vs remixable", a `v1.13 addition re-check` public-domain
paragraph, a `style-lora-registry.md` row, `teaching-notes.md` row 33, and
`kind-robots-academy-style-preview-precisionism` in `art-prompts.yaml`.
Marked `docs/curriculum-candidates/precisionism.md` itself `PROMOTED`.
Front-end sync to `academyStyles.ts` remains deferred, matching the
established persian-miniature/song-dynasty-landscape/mughal-miniature/etc.
pattern. Before adding a 34th movement, finish the known coverage gaps below
unless a newly discovered issue is more urgent — every remaining gap is
blocked solely on home-relay/media-server reachability, not on research or
write access to this repo.

| Area | Current state | Next verifiable action |
|---|---|---|
| Lesson seed entries | 30 of 33 movements in curriculum-outline.md are synced to `academyStyles.ts` (Fayum Mummy Portraits, Vienna Secession, and Joseon Dynasty Korean Genre Painting landed together 2026-07-25 — mirroring t-020/t-031/t-034/PR #506/#616/#771/#814; The Nabis §31, Hudson River School §32, and Precisionism §33, added 2026-07-26/2026-07-27, front-end sync deliberately deferred per the same pattern) | Sync The Nabis, Hudson River School, and Precisionism into `academyStyles.ts` as a follow-up (lane 1 or lane 3 cycle), then sync each future new movement the same way |
| Example works | 25 movements complete, including Persian Miniature Painting (3 works, all **VERIFIED** by direct `WebFetch` of their Wikimedia Commons file pages — 2026-07-20 egress to commons.wikimedia.org worked, unlike the earlier `artic.edu` 402s), Song Dynasty Landscape Painting (3 works, all **VERIFIED** the same way, 2026-07-21), and Mughal Miniature Painting (3 works, all **VERIFIED** the same way, 2026-07-21). Fayum Mummy Portraits (3 works, **VERIFIED** against the Met Collection API's `isPublicDomain` field, 2026-07-22), Vienna Secession (3 works, **VERIFIED** via the Wikimedia Commons API, 2026-07-24), Joseon Dynasty Korean Genre Painting (3 works, **VERIFIED** via direct Wikimedia Commons file pages, 2026-07-25), The Nabis (3 works, **VERIFIED** via direct Wikimedia Commons file pages, 2026-07-26), Hudson River School (3 works, all **VERIFIED** via direct Wikimedia Commons file pages — 2 already verified in the source candidate, the third, *The Oxbow*, live-verified this cycle, 2026-07-26), and Precisionism (3 works, all **VERIFIED** via direct Wikimedia Commons file pages, 2026-07-27) are all written up but not yet in `examples.manifest.json`. Ashcan School's 4 VERIFIED works are written up in curriculum-outline.md §23 but not yet in `examples.manifest.json` (confirmed absent: no `exampleWorks` field on the `ashcan-school` entry in `stores/seeds/academyStyles.ts` as of 2026-07-19). American Regionalism's 4 works are written up in curriculum-outline.md §24 (sourced, but marked "unverified this cycle" — `WebFetch` to museum hosts returned HTTP 402 through the session egress proxy) | Blocked on media-server write access — same blocker as t-033 (confirmed 2026-07-19: `examples.manifest.json` lives on `media.acrocatranch.com`, not in the kind_robots git repo; this session has `KR_API_TOKEN` but no `KR_RELAY_TOKEN`/`KR_RELAY_USER_ID` and found no in-repo upload path, so it cannot write the manifest or upload images from here). Research/sourcing is already done (curriculum-outline.md §23-33); only the write step remains, plus a direct-fetch spot-check of §24's four URLs when museum/Commons egress is open. Resume once a session with media-server/relay write access is available — do not re-attempt from a sandbox without it |
| Starter library | 21 starter images and provenance manifest complete — coverage intentionally movement-agnostic (2026-07-18: confirmed no movement-specific starters exist for any of the 8 movements added after v1, and an abstract Suprematist work would fail the library's own selection criteria; see starter-image-library.md) | Keep source-picker integration aligned with the manifest; no new starter entries needed |
| Style previews | 33 prompts queued (all 33 movements have a `kind-robots-academy-style-preview-*` entry in `art-prompts.yaml`, including Fayum Mummy Portraits, Vienna Secession, Joseon Dynasty Korean Genre Painting, The Nabis, Hudson River School, and Precisionism — the last added this cycle, 2026-07-27 lane 4). All 33 are still `status: pending` — the home relay is no longer in the fully-stuck never-claimed state seen 2026-07-18 through 2026-07-24 but is still backlogged and growing (`GET /api/art/queue/stats` this cycle, via `scripts/recheck_render_queue.py`: PENDING=144, oldest job 2017 ~61h old, 24h window newly-PENDING 142 vs. DONE 34 — see RENDER-BACKLOG.md for the full stamped entry) | Blocked on home-relay backlog depth, not on this queue. Re-run `python scripts/consume_art_requests.py --id-prefix "kind-robots-academy-style-preview-" --live` with a fresh job once the backlog has visibly drained (check `oldestPending`/`queueDepth.PENDING` via `scripts/recheck_render_queue.py` before re-probing with a full queued job — do not re-probe if RENDER-BACKLOG.md's newest entry is still recent and shows the same `growing` signature) |
| Remix configs | Registry exists; A/B generation blocked | Resume only after the relay, database, and approved generation path are available |
| Teaching scaffold | Written in `docs/teaching-notes.md`, covering all 33 movements including Fayum Mummy Portraits (row 28), Vienna Secession (row 29), Joseon Dynasty Korean Genre Painting (row 30), The Nabis (row 31), Hudson River School (row 32), and Precisionism (row 33 — added this cycle, 2026-07-27 lane 4); wired into `academy-style-detail.vue`'s Try It / Reflect sections (t-023, done — verified 2026-07-18 via `grep -n "Try it\|Reflect" components/academy/academy-style-detail.vue` on kind_robots main) | Coverage complete; no open action |

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
