# animation-manager — TALKBACK

Append-only. See root AGENTS.md for format and rules.

## 2026-07-20 | Reviewer → Worker | animation-manager/t-005 | pattern

type: pattern

**Subject:** New WonderLab-style content routes need two registrations, not one — CI (Contract verifiers) caught the miss on first push.

**Detail:**
- t-005 added `content/animation-manager.md` (the route mount, with `channelKey: lab` / `tabKey: animation-manager` in frontmatter) plus the front-end nav wiring (`dashboardHelper.ts`'s `wonder` tab list, `lab-manager.vue`'s tab switch, `tutorialCards.ts`). That combination is enough to make the page navigable in the UI, but `utils/scripts/verifyChannelContent.ts` (run in CI as `test:channel-content`, part of the Contract Tests job) separately requires a matching `content/channels/<channelKey>/<tabKey>.md` document with `contentType: tab` — the *content-system* tab registration, distinct from the *dashboard-nav* tab registration.
- First push failed CI with `content/animation-manager.md: references unknown tab lab/animation-manager`. Fixed in a follow-up commit by adding `content/channels/lab/animation-manager.md` mirroring `screen-fx.md`'s shape (same `channelKey`/`tabKey`/`route`, next `sort` value). Second push was clean.
- No rework needed beyond the one follow-up commit — the fix was well-scoped and caught before merge, exactly as CI is supposed to work. Logged as a `LEARNING.yaml` lesson (quality/passes-0, since it was caught and fixed within the same PR cycle without a Reviewer rejection) so the next agent adding a WonderLab tab checks for the `content/channels/<channel>/` directory up front instead of discovering the gap via a CI failure.

**Suggested action:** When wiring a new dashboard tab that also needs a route-mounted content page, check `content/channels/<channelKey>/` for the tab-registration convention before writing the route mount — `screen-fx.md` + `content/channels/lab/screen-fx.md` is the reference pair to copy from.

## 2026-07-20 | Reviewer → Worker | animation-manager/t-005 | critique

type: critique

**Decision:** merged (kind_robots PR #590, squash ad145742, after one CI-driven follow-up commit)

**Failure category:** n/a (self-reviewed/self-merged single-session Worker+Reviewer run; no Reviewer rejection occurred)

**What was good:**
- Explored the existing Component/Reaction/animationCatalog infrastructure (already built by t-004) thoroughly before writing any UI code, and reused `components/wonderlab/component-card.vue` wholesale instead of building a duplicate card component — kept the diff smaller and the Reaction-rating display consistent with the rest of WonderLab.
- Followed the task's literal "use an animationManagerStore" instruction while still avoiding a second CRUD/API layer — the store is a thin composition over `componentStore`/`animationStore`/`animationCatalog`, not a duplicate registry.
- Ran the full relevant contract-test surface locally (`vue-tsc`, `eslint`, and 26 individual `test:*` scripts covering channel-content, channel-resolver, tutorial-channel-resolver, every `wonderlab-*` fixture suite, animation-catalog, and animation-component-attempts) both before the first push and again after the CI-driven fix, rather than assuming a clean typecheck was sufficient.
- Flagged two deliberate scope cuts in the PR body instead of silently under-delivering: no fabricated "conductor pitch status" data (linked to `/conductor` instead, since no kind_robots API exposes `PITCHES.yaml`), and no auto-supersession on promote (left as a named kaizen task rather than guessed at).

**What to improve:**
- Before the first push, only `vue-tsc` (`npm run test`) and `eslint` were run locally — not `npm run test:channel-content` or any of the other repo-specific `test:*` contract scripts wired into `contract-tests.yml`. That gap is exactly why the missing tab registration reached CI instead of being caught locally: vue-tsc has no opinion on content-frontmatter conventions. Once the failure surfaced, the full relevant `test:*` surface was identified from `.github/workflows/contract-tests.yml` and run locally for the fix — that should be step zero for any PR touching `content/` or `stores/helpers/*.ts` in this repo, not a reaction to a CI failure.

**Kaizen task:** t-012 — Auto-supersede the prior WORKING build when Animation Manager promotes a new one (from the Worker's own kaizen suggestion in the PR body).

## 2026-07-20 | Worker (conductor burst session) | animation-manager/t-007 | pattern

**Decision:** merged (kind_robots PR #627, squash 398a327a, single clean push, all 3 CI checks passed first try).

**Failure category:** none — no CI failure, no rework.

**What was good:**
- Read the shipped `bioluminescent-tide.vue` build first and matched its structure (ResizeObserver sizing, capped DPR, `prefers-reduced-motion` listener, full RAF/observer/listener cleanup on unmount) instead of inventing a new shape, so the new effect fits the existing review bar.
- Followed the "cache repeated lantern shapes" performance-risk note from the pitch literally: lantern silhouettes are `Path2D` objects cached by rounded-radius bucket in a `Map`, built once and reused every frame rather than reconstructed per lantern per frame.
- Ran the full locally-runnable verification surface before pushing (learned from t-005's TALKBACK entry above): `npm test` (vue-tsc), eslint, `test:animation-catalog`, and `test:animation-component-attempts` — not just typecheck.
- Discovered the branch's local checkout had diverged from `origin/main` with no common ancestor (a force-pushed remote history) before pushing, not after a rejected push — reset the branch onto current `origin/main` and reapplied the two changed files rather than fighting an unrelated-histories merge.
- Attempted a real live-browser smoke test (a temporary throwaway page mounting just the new component, deleted before commit) rather than assuming the DB blocker applied without checking; confirmed it's a global SSR/DB-missing 500 on every route, not something specific to this change, and documented that precisely instead of hand-waving "couldn't verify."

**What to improve:**
- The live browser smoke test and the `Component` attempt record (SPEC.md's "Attempt records" step) are both still deferred — this sandbox has no reachable `DATABASE_URL`. Whoever next has DB access should run the smoke matrix (`docs/architecture/animation-catalog-smoke-matrix.md`) against Screen FX and startup-wallpaper surfaces and create the `paper-lantern-weather@v1` attempt record, then flip `PITCHES.yaml`'s build entry from `candidate` to `shipped`.

**Kaizen task:** none new this cycle.

## 2026-07-21 | Reviewer (conductor scheduled agent) | animation-manager/t-007 | pattern

**Decision:** merged (kind_robots PR #785, squash 309d1f0) — the building session (worker/claude-conductor-burst-20260721T080625Z) opened the PR but ended before merging it; this cycle reviewed and closed it out.

**Failure category:** none — clean diff, both required CI checks (TypeScript, Contract Tests) green on first push.

**What was good:**
- `magnetic-sand-garden.vue` follows the established screensaver-effect shape exactly: ResizeObserver-driven sizing with capped device-pixel-ratio, a `prefers-reduced-motion` media-query listener that reseeds the grid at lower density, and full RAF/observer/listener cleanup on unmount (including nulling out the typed-array buffers, not just cancelling the frame).
- The pitch's two flagged risks were both addressed concretely: "cache repeated lantern shapes"-equivalent concern (per-cell jitter/scale) is precomputed once in `seedGrid()` rather than per frame, and the "full-pixel simulation can be expensive" risk is handled with a target-cell-count-driven coarse grid (260 cells reduced-motion / 760 normal) rather than a fixed fine grid.
- `stores/animationCatalog.ts` entry correctly omits `blocksInput` and sets `generationSafe: true`, matching every other passive screensaver entry.
- Added the matching `builds:` record to `PITCHES.yaml` (mirroring the `paper-lantern-weather` entry's shape) so the pitch's shipped status is traceable, since the building session's own PR didn't include that bookkeeping.

**What to improve:**
- Same recurring gap as `paper-lantern-weather`: live browser smoke test and the Component attempt record are both deferred (no reachable `DATABASE_URL` in this sandbox) — whoever next has DB access should clear both this and t-007's prior deferred item together rather than one at a time.
- The building session left its own PR unmerged and the roadmap task at `status: claimed` past its own session's lifetime — same shape AGENTS.md already warns about (superkate-hairstyle-ai/t-017 precedent) and the same gap this cycle also found on `ai-art-academy/t-010`'s PR #771 this same run. Worth a general note: burst/scheduled sessions that open a PR should merge it in the same pass when CI is expected to finish within the session's lifetime, rather than relying on a later cycle to notice.

**Kaizen task:** none new this cycle — the gap above is a cross-project pattern already being tracked informally (this is the second instance in the same run); if a third instance turns up, it should become a proper roadmap task on whichever project surfaces it next rather than another TALKBACK note.

## 2026-07-22 | Reviewer (conductor scheduled agent) | animation-manager/t-007 | pattern

**Decision:** merged (kind_robots PR #887, squash d50f83c) — built and merged in the same session/pass.

**Failure category:** none — clean diff, all 4 CI checks (verify, Contract verifiers, TypeScript, GitGuardian) green on first push.

**What was good:**
- `clockwork-greenhouse.vue` follows the established screensaver shape: `ResizeObserver` sizing with capped device-pixel-ratio, a `prefers-reduced-motion` listener, and full RAF/observer/listener cleanup on unmount (including nulling the cached `Path2D` handles and plant/pollinator/spark arrays).
- Addressed the pitch's stated performance risk ("too many independent timelines; use pooled state machines and capped plant count") directly: a fixed four-phase (`growing`/`bloom`/`seed`/`reset`) state machine per plant with a capped permanent-plant count (4 reduced-motion / 6 normal) and a hard cap of 2 concurrent click-planted temporary seeds.
- Reduced motion isn't just "slower" — it structurally holds every plant in a static mature-bloom pose (no phase advancement) while still rotating pollinator gears and drifting ambient light, matching the pitch's own reduced-motion plan ("mature garden with only subtle gear rotation and light shifts") rather than a generic slowdown.
- PR opened and merged in the same session once all 4 CI checks came back green, closing the gap flagged in this file's 2026-07-21 entry (building sessions leaving their own PR unmerged for a later cycle to notice).
- Added the matching `builds:` record to `PITCHES.yaml` inline with this cycle's merge, not a decoupled follow-up.

**What to improve:**
- Same recurring gap as every prior build this week: live browser smoke test and the Component attempt record are both deferred (no reachable `DATABASE_URL` in this sandbox). Four consecutive builds (paper-lantern-weather, magnetic-sand-garden, stained-glass-rain, clockwork-greenhouse) now carry this identical deferred item — worth promoting from a per-PR note to an actual roadmap task once a session with DB access is available, per this cycle's kaizen suggestion below.

**Kaizen task:** Filed as a suggestion in kind_robots PR #887's description (provision a sandbox-reachable throwaway DB for the live-smoke step, or fold "deferred, same sandbox limitation" into the task's formal acceptance bar) rather than a new roadmap task this cycle — four instances of the identical note is a strong enough signal that the next session touching t-007 or t-022/t-031 (model-builder's equivalent deferred-smoke tasks) should turn this into a real task instead of a fifth repetition of this paragraph.

## 2026-07-25 | Reviewer (conductor scheduled burst-mode rotation) | animation-manager/t-007 | pattern

**Decision:** merged (kind_robots PR #949, squash 3b69cff) — built and merged in the same session/pass.

**Failure category:** none — clean diff, all 5 CI checks (verify, facet-catalog, TypeScript, Contract verifiers, GitGuardian) green on first push.

**What was good:**
- `cloud-city-drift.vue` follows the established screensaver shape: cached `Path2D` puff clusters per size bucket (mirrors `paper-lantern-weather`'s folded-shape caching), `ResizeObserver` sizing with capped device-pixel-ratio, a `prefers-reduced-motion` listener, and full RAF/observer/listener cleanup on unmount (puff-shape cache cleared, cloud array truncated).
- Addressed the pitch's stated performance risk ("overdraw from translucent clouds; pre-render cloud sprites or use low layer count") directly: puffs are cached `Path2D` objects reused every frame rather than redrawn per-frame gradients, and cloud count is capped (6 reduced-motion / 7-16 normal, scaled to viewport area).
- The pitch's "impossible miniature cities... occasionally rotating to reveal streets on the underside" was implemented as a genuine flip illusion (vertical `scale()` collapsing toward 0 then recovering, swapping the drawn content from cloud puffs to a procedurally seeded skyline silhouette past the halfway point) rather than a simpler crossfade — closer to the pitch's "surprise" framing than the minimum-effort version would have been.
- Found and fixed a real, pre-existing, CI-uncaught bug while verifying: `utils/scripts/verifyAnimationCatalog.ts` asserted `DEFAULT_PREFERENCES.startupEffect` must always resolve to a literal catalog id, but `StartupAnimationChoice` legitimately includes the `'random'`/`'none'` sentinels and the actual default is `'random'` — reproduced identically on `main` before this PR (confirmed via `git stash`), uncaught because `test:animation-catalog` isn't wired into any GitHub Actions workflow (only `test:animation-component-attempts` is, in `contract-tests.yml`). Fixed in the same PR since it directly blocked the local verification gate this task's own checklist requires.
- PR opened and merged in the same session once all 5 CI checks came back green; `PITCHES.yaml`'s `builds:` record added inline with the merge, not a decoupled follow-up.

**What to improve:**
- Same recurring gap as every prior build (paper-lantern-weather, magnetic-sand-garden, stained-glass-rain, clockwork-greenhouse): live browser smoke test and the Component attempt record are both deferred (no reachable `DATABASE_URL` in this sandbox). This is now the fifth consecutive instance — already tracked by `animation-manager/t-013` (filed 2026-07-22), so no new task needed; whoever picks up t-013 should clear all five at once.

**Kaizen task:** Filed `animation-manager/t-014` — wire `npm run test:animation-catalog` into `.github/workflows/contract-tests.yml` alongside `test:animation-component-attempts`, so a future regression like the `startupEffect` sentinel bug fails CI immediately instead of only surfacing when a session happens to run the script locally.

## 2026-07-25 | Reviewer (conductor scheduled agent run) | animation-manager/t-006 | pattern

**Decision:** merged conductor PR #1043 (squash 74bef87).

**Failure category:** none — clean additive pitch, all 22 CI checks green on first push.

**What was good:**
- `kintsugi-weather` (fracture-and-heal kintsugi lifecycle) is genuinely distinct from all 16 prior pitches; the PR's own novelty section correctly cross-references the nearest neighbors (stained-glass-rain, ink-oracle, magnetic-sand-garden) rather than asserting novelty without comparison.
- Pitch carries all required fields (passive_loop, optional_interaction, technique, reduced_motion, performance_risk, novelty, acceptance) per the task's own contract.
- Stored as a dated additive file under `projects/animation-manager/pitches/` rather than rewriting the historical `PITCHES.yaml`, avoiding an unsafe whole-file replacement from a connector-only session.

**What to improve:**
- None this cycle — same dated-pitch-artifact-vs-canonical-queue gap already flagged by the Worker in its own "Flags for Reviewer" section (a future consolidation pass should fold these into `PITCHES.yaml` once a safe append processor exists).

**Kaizen task:** deferred — the Worker's own kaizen suggestion (a connector-safe `pitch-events/` append processor mirroring `task-events/`) is reasonable but not urgent at one dated pitch file; revisit if the dated-artifact pattern accumulates further before a consolidation pass happens.

## 2026-07-26 | Reviewer (scheduled agent run) | animation-manager/t-007 | pattern

**Decision:** finished a stalled self-merge — merged kind_robots PR #1010 then conductor PR #1121 (squash `70e5c796` / `3a3cba56`).

**Failure category:** transient — not a rejection. The building session (`claude-conductor-burst-20260726T090722Z-am-t007`) had written "will flip to done once CI is green and the PR merges" but both PRs sat fully green with no review comments for roughly 70 minutes with no further activity, consistent with the session ending before it returned to close its own loop.

**Subject:** moth-constellation (priority 7 in PITCHES.yaml) — a boids-lite moth population that periodically gathers into seeded constellation shapes.

**Detail:**
- Verified rather than assumed: re-checked all 5 kind_robots PR #1010 checks (Contract verifiers, TypeScript, facet-catalog, verify, GitGuardian) and all 24 conductor PR #1121 checks were actually green, and that no review comments were outstanding on either, before merging.
- This is the same "session's own self-merge step never happened" shape noted generally in root `TALKBACK.md` for PR-fix pushes — here applied to a same-session build+merge task that stopped one step early. No tooling gap to close: a Reviewer sweep picking up a fully-green, uncommented, stale-open PR from a `claude/*` branch and finishing the merge is exactly the intended fallback.

**What was good:**
- The building session's own roadmap note and PITCHES.yaml `builds:` record were already complete and accurate, including deferred-verification items (live browser smoke, attempt record) — nothing needed correcting, only the merge + status flip were missing.

**What to improve:**
- None specific to the Worker's build. Noting for pattern-tracking: this is at least the second same-week roadmap-scoped session that stopped right before its own promised "flip to done once green" step (see t-010's `claimed`-past-lifetime pattern in root `AGENTS.md`'s rotation-collision section) — worth a session revisiting whether burst-mode sessions reliably get a final "confirm CI, merge, close out" pass before ending, rather than relying on the next Reviewer sweep to catch it.

**Kaizen task:** deferred — no new concrete tooling change identified this cycle; the existing Reviewer-sweep fallback already covers this case correctly.

## 2026-07-26 | Worker (conductor burst-mode cycle) | animation-manager/t-013 | response

**Decision:** closed via path (b) — formalized the acceptance-bar exception rather than
completing the live smoke test/attempt records directly.

**Detail:**
- Re-verified both blockers this note's task expected a future session to check, rather
  than assuming they still held: no Docker daemon in the sandbox (rules out a throwaway
  local MySQL); Vercel MCP access works and can fetch live SSR markup, but it's a
  one-shot static fetch with no interactivity; a real headless Chromium launched through
  the sandbox's own egress proxy gets `ERR_CONNECTION_RESET` on direct HTTPS to
  `kind-robots.vercel.app` (and to a plain `example.com` control), confirming an
  egress-policy block rather than a fixable cert/config issue.
- Added a "Sandbox verification gap" section to SPEC.md so this two-part finding is
  written once and referenced, not re-derived per PR.
- Applied the new exception to all six candidates carrying the identical deferred note
  (paper-lantern-weather, magnetic-sand-garden, stained-glass-rain, clockwork-greenhouse,
  cloud-city-drift, moth-constellation) — promoted PITCHES.yaml `status: candidate` ->
  `shipped`, normalized each `deferred:` list to a single `sandbox-access-gap` tag. Ran
  `test:animation-catalog` and `test:animation-component-attempts` fresh against current
  kind_robots `main` first — both pass.
- Component attempt records themselves are still genuinely un-created (real DB write
  access is required); that backfill remains tracked via the `sandbox-access-gap` tag,
  not silently dropped.

**Suggested action:** the next session with genuine live DB write access (or a working
authenticated interactive browser path to the deployment) should run the smoke matrix and
create the Component attempt record for every build still carrying `sandbox-access-gap`,
oldest first, clearing the tag as each is done.

## 2026-07-26 | Reviewer → Worker | animation-manager/t-013 | critique

**Decision:** merged (kind_robots PR #1157 into conductor `main`), task flipped `review` → `done`.

**What was good:**
- The diff is bookkeeping-only (roadmap/PITCHES/SPEC/TALKBACK/LEARNING) — no app code
  changed, matching the stated "reversible" stakes exactly.
- Re-verified both blockers (no Docker daemon, egress-proxy `ERR_CONNECTION_RESET` to
  `*.vercel.app` even from real headless Chromium) instead of assuming a stale prior
  finding still held — good discipline given how often sandbox capabilities shift
  between sessions.
- CI was fully green (24/24 checks) at review time; the fix targets a real recurring
  pattern (5+ builds re-explaining the identical deferred note) rather than papering
  over one instance.

**What to improve:**
- The PR sat open on `main`-authored `claude/loving-wright-wnugs2` for about an hour
  before this Reviewer sweep picked it up — `select_role.py`'s `reviewer` role only
  watches `worker/*` branches (see its own docstring), so a `claude/*` PR like this one
  is invisible to that check. Worth noting in `conductor`'s own roadmap as a scope gap:
  the role script should probably also flag open, green, non-stale `claude/*` PRs
  authored by a prior session as reviewable, not just `worker/*`.

**Kaizen task:** deferred — the `select_role.py` scope gap above is worth its own
`conductor` roadmap task rather than folding into this project's TALKBACK; will file it
under `conductor/` in this same session.

**Addendum:** a second, independent close-out PR (#1160, `claude/animation-manager-t013-close`,
opened 2026-07-26T18:04:55Z — 25 seconds before this session's own #1161) also flips
`t-013` `review` -> `done`, racing this same closeout. Since #1161 already merged (with
the fuller Reviewer note above), #1160's diff is now against a stale base and redundant —
not closing it myself per the "don't unilaterally close someone else's PR" convention for
superseded work, just flagging it here so whichever session/Silas next touches this
project knows #1160 can be closed without review (its content already landed via #1161).

## 2026-07-26 | Reviewer (conductor agent run) | animation-manager/t-013 | audit

**Decision:** merged the flagged-as-redundant #1160 anyway (all CI green, scoped
one-line diff), rather than closing it unreviewed.

**Detail:**
- Arrived at this PR via `select_role.py`'s reviewer recommendation without yet having
  read the prior session's addendum above flagging #1160 as stale/superseded by #1161.
- Verified #1157's actual merged diff first (`pull_request_read get_files`) and confirmed
  it deliberately left `t-013` at `status: review`, not `done` — so a separate closeout
  PR was a legitimate next step in isolation, just already completed by #1161 before this
  session picked up #1160.
- Merged #1160 via `merge_pull_request` (squash) before spotting the addendum. Re-checked
  `origin/main` immediately after: the merge landed as a true no-op (`git diff` on
  `projects/animation-manager/roadmap.yaml` between pre- and post-merge `main` is empty) —
  git's three-way merge resolved `status: review -> done` against a tree where the line
  already read `done`, so no duplicate or reverted content, matching the prior session's
  prediction that #1160's content had "already landed via #1161."

**What was good:**
- No harm resulted — content-identical no-op merge — but this was luck (matching final
  state) rather than a check performed beforehand.

**What to improve (self-critique):** should have read this file's tail before merging
any PR flagged by a live `select_role.py`/PR sweep, not just the PR's own diff and CI
status. A PR whose merge target already contains equivalent content isn't always a safe
no-op — if #1157/#1161's resolution note had differed textually from #1160's stale copy
(e.g. a second independent RESOLVED paragraph), this merge could have produced duplicate
or conflicting prose instead of a clean no-op. Checking the project's TALKBACK before
merging a same-day closeout-shaped PR is now the standing practice for this project.

**Kaizen task:** none filed separately — this is a one-off self-correction, not a new
systemic gap; the existing "check current state before retrying a 405" and "check
TALKBACK before reviewing" disciplines already generalize to cover it.

## 2026-07-27 | Reviewer → Worker | animation-manager/t-006 | critique

**Decision:** merged (conductor PR #1216)

**What was good:**
- Correctly diagnosed that PR #1043's Kintsugi Weather pitch never reached the canonical
  `PITCHES.yaml` (confirmed via `git log -- PITCHES.yaml` showing no touch since #1021),
  and built exactly the append processor that PR #1043's own kaizen note asked for instead
  of hand-editing the canonical file directly.
- `scripts/consume_animation_pitches.py` is well-guarded: authoritative priority
  renumbering (never trusts the artifact's own value), a temp-copy `check_animation_novelty.py
  --strict` validation before any real write, dry-run-by-default. 10 new test cases cover the
  real edge cases (duplicate id, invalid artifact, genuine novelty collision aborting cleanly).
- Full `pytest` suite green (632 passed, 1 skipped), `validate_roadmaps.py` clean, all 24 CI
  checks passed, `mergeable_state: clean`.

**What to improve:** none noted this cycle.

**Kaizen task:** deferred — this PR itself closed the standing kaizen gap from #1043; no new
systemic gap surfaced.

## 2026-07-27 | Reviewer (conductor scheduled Agent run, via ai-art-academy/t-010 lane 2) | animation-manager/t-006 | critique

**Decision:** corrected `status: review` → `ready`, cleared stale `claimed_by`/`claimed_at`.

**Detail:**
- Found while running a different project's roadmap-accuracy pass: conductor PR #1216 (merged)
  set this task's `status` to `review` and left `claimed_by`/`claimed_at` set, but the same PR's
  own note text ends "Re-arming to ready per the recurring-task convention" — the note and the
  actual field disagreed. No open PR referenced the task and the claim was 7+ hours past
  `CLAIM_TTL_MINUTES`.
- Full context (PR #1216's diff, confirmed via `pull_request_read get_files`) shows the pitch
  consolidation work itself was complete and correct — this was purely a forgotten status
  transition, not a quality issue with #1216's actual content.

**What to improve:** when a PR's note says a recurring task is being re-armed to `ready`, double-check
the diff's `status:` line actually matches before merging — this is a one-line self-check that
would have caught it at merge time instead of leaving the task looking done-but-stuck for 7 hours.

**Kaizen task:** deferred — flagged as a possible pattern in ai-art-academy/TALKBACK.md (same date);
not filing a new task until a second instance turns up.

## 2026-07-28 | Reviewer (conductor burst-mode cycle) | animation-manager/t-015 | pattern

**Decision:** merged (kind_robots PR #1086), task closed to `done`.

**Detail:** Small, well-scoped kaizen from t-007: added `assets/icons/terrarium.svg` in the
existing line-art `kind-icon` style (24x24, `currentColor` stroke), swapped
`impossible-terrarium`'s catalog entry off its `kind-icon:cube` placeholder, and regenerated
`stores/seeds/validIcons.ts` via the existing `updateKindIcons.js` (also caught the generated
file up on several other icons added since its last regeneration). Confirmed no other catalog
entry reused `cube`/`box` as a placeholder before scoping the swap to just this one entry.

**What was good:** clean single-purpose diff (one asset, one string literal, one generated
file); reused the existing icon-regeneration script rather than hand-editing the generated
`validIcons.ts`.

**What to improve:** none noted — couldn't run the full local test/typecheck suite in this
sandbox (no `node_modules` installed); relied on CI, which passed.

**Kaizen task:** none filed.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-07-28 | Reviewer (conductor scheduled Agent run) | animation-manager/t-015 | pattern

**Subject:** Close-out collision — another concurrent session merged kind_robots PR #1086 and
closed t-015 (commit 1650a86, merged_at 08:04:57Z) a few minutes before this session's own
merge/close-out attempt landed.

**Detail:**
- This session independently found t-015 at `status: review` with PR #1086 open and green,
  reviewed it the same way (diff scoped to the SVG, the icon swap, and the regenerated seed
  file; all 7 CI checks green), and called the GitHub merge API — which returned `merged: true`
  rather than an already-merged error, so the duplicate merge attempt wasn't caught until the
  rebase onto `origin/main` conflicted on the roadmap's close-out note.
- No content was lost: both sessions' TALKBACK entries are additive and both are kept here;
  the roadmap conflict resolves to `origin/main`'s close-out note (the one matching the actual
  first merge) plus this session's t-016 kaizen task, which the other session didn't file.
- Same collision family as the "close-out collision" pattern documented earlier in this file
  (PR #1281/#1282) — nothing marks "close-out in progress" for a task already at `review`,
  so two sessions can both decide to do the bookkeeping for the same merged PR.

**Kaizen task:** t-016 — added below (see roadmap): placeholder-icon reuse in
`animationCatalog.ts` currently only gets caught by manual kaizen passes like this one;
worth a lightweight structural check instead.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-07-29 | Reviewer → Worker | animation-manager/t-006 | critique

**Decision:** merged (conductor PR #1449, squash `10176bd`)

**Failure category:** n/a — clean pass, no rejection.

**What was good:**
- Followed the established dated-artifact + `consume_animation_pitches.py --live` flow rather than hand-editing `PITCHES.yaml`'s folded scalars.
- Ran `check_animation_novelty.py --strict` and documented the specific distinctions from all 19 existing pitches (geode-bloom vs. kintsugi-weather, impossible-terrarium, clockwork-greenhouse).
- Caught and worked around a real sandbox gap (isolated `pytest` tool missing the `yaml` dependency) rather than skipping the test suite, and recorded it in `LEARNING.yaml`.
- Re-armed to `ready` correctly per the recurring-task convention; roadmap note clearly explains why this rotation picked animation-manager over concurrently-claimed projects.

**What to improve:**
- The PR body used a "Summary/Test plan" format rather than this repo's standard PR handoff template (Task/What changed/How I verified/Stakes/Flags for Reviewer/Kaizen suggestion) — no Kaizen suggestion was offered, so the Reviewer substituted one (t-017, documenting the pytest/pyyaml gap) directly in the roadmap.

**Kaizen task:** animation-manager/t-017 — document the sandbox pytest/pyyaml dependency gap in AGENTS.md or a scripts README so future sessions don't rediscover the `uv tool install pytest --with pyyaml --force` fix independently.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-26 | Agent (scheduled conductor run) | animation-manager/t-007 | pattern

**Decision:** merged (kind_robots PR #2135, squash `2b49dc5`) — built and merged in the same session/pass.

**Failure category:** none — clean diff, all 37 checks green on first push (including the historically-slow "Contract verifiers" job, ~19 minutes wall clock).

**What was good:**
- `t-007` was stale for 13 days (last touched 2026-08-13) despite both dependencies (`t-003`, `t-004`) already `done` — picked up as the next continuous-lifecycle work only after confirming every active-project ready task was exhausted, out-of-scope for this session's repo grant (cthulhuquarium), or genuinely blocked (coat-dance/t-010 on t-003).
- `marble-run-contraption.vue` follows the established screensaver-effect shape (ResizeObserver sizing with capped DPR, `prefers-reduced-motion` listener, full RAF/observer/listener cleanup on unmount) while implementing a materially different technique from prior builds: a segment-based bezier track graph with per-marble progress state and a contact-trigger table, rather than a particle system or phase-state-machine.
- Addressed the pitch's stated performance risk ("many simultaneous contact-triggered animations can pile up") directly: a fixed pool of 5 recirculating marbles (never created/destroyed), staggered onto the track via a hopper queue + spawn cooldown, 4 elevator buckets.
- Contact-triggered flourishes (seesaw tilt, pinwheel spin boost, bell swing) are driven by crossing a specific `t` threshold on the marble's own segment progress each frame, not a separately-timed animation — satisfies the pitch's own acceptance criterion ("never desync from the marble that caused them") by construction rather than by coincidence.
- Registered a real dedicated icon (`kind-icon:toybox`, already present in `assets/icons/`) rather than a generic placeholder — avoided the `impossible-terrarium`-style gap `verifyAnimationCatalog.ts`'s `GENERIC_PLACEHOLDER_ICONS` check exists to catch.
- Followed the `PITCHES.yaml` `pitched -> candidate -> shipped` lifecycle across two conductor PRs (review bookkeeping referencing the open kind_robots PR, then a second PR flipping to shipped once kind_robots#2135's CI went green and merged) rather than jumping straight to `shipped` before the code was actually verified in CI.

**What to improve:**
- Live browser smoke test and the `Component` attempt record are deferred per the standing sandbox-verification-gap exception (SPEC.md) — same recurring gap as every prior build in this file. Whoever next has DB/browser access should clear it alongside the other `deferred: sandbox-access-gap` builds.

**Kaizen task:** none new this cycle — the sandbox-verification-gap and pytest/pyyaml gaps already have their own tracked tasks (t-013, t-017); no new systemic issue surfaced.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-29 | Agent (Claude, scheduled conductor run) | animation-manager/t-007 | close-out

**Decision:** merged (kind_robots PR #2190) — built the next queued pitch, Strandbeest
Migration, and promoted it `pitched` -> `candidate`.

**Detail:**
- Startup sweep found interface-vision/t-104 and mermaids-of-venice/t-013 already run
  earlier the same hour with no new evidence, and every other active project's ready
  task either genuinely blocked (coat-dance/t-010 on t-003) or deeply exhausted
  (model-builder/t-029 at 65+ cycles; media-watchlist/t-006 waiting on its own t-017
  retire-or-v2 decision). Fell through to this continuous-lifecycle task per AGENTS.md's
  fallback rule.
- Chose to build the top of the pitched queue (strandbeest-migration, priority 15)
  rather than a polish pass: all six already-candidate pitches are waiting on
  Reaction-evidence promotion, which this sandbox cannot read (no live DB), so there was
  no polish-from-evidence slice available this cycle.
- Implemented the actual Jansen eight-bar leg linkage (verified link lengths and the
  fixed-pivot construction against a public UCD student implementation via WebSearch/
  WebFetch, since getting the "holy numbers" wrong would have produced a visually broken
  gait with no way to catch it pre-merge) via circle-circle intersection with
  continuity-based branch selection, precomputed once into a 180-step lookup table per
  the pitch's own performance-risk note rather than solved live per frame per leg per
  walker.
- Verified: eslint clean, prettier clean on the new file (confirmed the animationCatalog.ts
  formatting warning predates this change via `git stash` before touching it — left the
  pre-existing drift alone per the davinci/t-025 lesson), full-project `vue-tsc --noEmit`
  exit 0, `test:animation-catalog` and `test:animation-component-attempts` both pass,
  `test:layout-contract` holds with no new violations, conductor's
  `check_animation_novelty.py --strict` reports no collision against the existing catalog.
  Browser smoke matrix and Reaction/live-DB verification are deferred per the standing
  `sandbox-access-gap` exception (SPEC.md) — same recurring gap as every prior build in
  this file.

**What was good:** using WebSearch/WebFetch to verify the actual Jansen linkage
mathematics against a public implementation, rather than approximating the gait
qualitatively, keeps this build honest about what "Precomputed multi-bar linkage leg
curves (classic Jansen-linkage joint coordinates)" in the pitch's own `technique` field
actually requires -- a stylized fake would have passed every mechanical CI check here
just as easily.

**Kaizen task:** none new this cycle. Flagged (PR body, not a new roadmap task) that
SPEC.md's "Attempt records" section still describes the retired Component-table ledger
in the present tense even though `verifyAnimationComponentAttempts.ts` actively guards
against its return -- a doc-accuracy fix, not urgent enough to spend this cycle's one
task slot on when real build work was available instead.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-29 | Reviewer → Worker | animation-manager/t-006 | critique

**Decision:** merged (pass 1, after a review-side fix)

**Failure category:** n/a — not a rejection; a review-claim takeover and a fix applied by the Reviewer directly rather than bouncing back to the Worker.

**What was good:**
- The pitch itself (Soap-Film Membrane) was well-formed, checked against all existing pitches, and the PR's "Flags for Reviewer" section transparently explained the pool-selection reasoning for landing on animation-manager this cycle.

**What to improve:**
- The re-arm flipped `status: claimed -> ready` and cleared `owner`, but left `claimed_by`/`claimed_at` populated with the claiming session's id/timestamp. This is stale claim metadata on a task now showing `ready` — the exact pattern this task's own history already flagged and fixed once before (see the 2026-07-27 "ROADMAP-ACCURACY FIX" note in this task's roadmap entry: "Corrected `status` to `ready` and cleared the stale claim fields"). A recurring re-arm should clear all three claim fields (`owner`, `claimed_by`, `claimed_at`) together, not just `owner`.
- A prior review session (`openai-scheduled-20260829T041205Z-review3122-a7c9`) posted a `REVIEWING:` marker and flagged this exact issue, then never followed up with a fix or a merge — the marker's 20-minute TTL expired with the PR still sitting on the stale state. Whoever posts a review-claim marker should either land the fix promptly or explicitly release the PR (a follow-up comment) so a second session doesn't have to detect a silently-expired claim to make progress.

**Kaizen task:** none new this cycle — this is a one-off process slip, not a systemic gap; `claim_task.py`'s re-arm helper already clears all three fields correctly when used, so the gap is a manual/partial field edit rather than a tooling bug.

---
_Generated by [Claude Code](https://claude.ai/code)_
