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
